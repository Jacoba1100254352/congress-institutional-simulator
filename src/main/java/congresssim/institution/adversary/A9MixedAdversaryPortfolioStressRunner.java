package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.bargaining.AlternativeSelectionRule;
import congresssim.institution.bargaining.CompetingAlternativesProcess;
import congresssim.institution.bargaining.MultiRoundAmendmentProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.distribution.HarmWeightedThresholdProcess;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.publicinput.CitizenPanelReviewProcess;
import congresssim.institution.publicinput.PublicObjectionWindowProcess;
import congresssim.institution.review.AdministrativeReviewCapacityProcess;
import congresssim.institution.review.AdministrativeReviewCapacityProcess.CapacitySnapshot;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.model.Bill;
import congresssim.model.SimulationWorld;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.ProposalShockProfile;
import congresssim.simulation.Scenario;
import congresssim.simulation.WorldGenerator;
import congresssim.simulation.WorldSpec;
import congresssim.simulation.catalog.ScenarioCatalog;
import congresssim.util.Values;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;


/**
 * Runs fixed-budget mixed attacks against paired single-attack controls.
 */
public final class A9MixedAdversaryPortfolioStressRunner
{
	private static final String ADVERSARY_ID = "A9";
	private static final String CASE_KEY = "mixed-adversary-portfolio";
	private static final String BUDGET_UNIT = "joint_attack_units";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a9.jsonl";
	private static final double CAPACITY_UNITS = 18.0;
	private static final double RECOVERY_UNITS_PER_CYCLE = 3.60;
	private static final double MINIMUM_DEFENDED_COVERAGE = 0.72;
	private static final int MAX_RECOVERY_CYCLES = 240;
	private static final double INTERACTION_EPSILON = 0.010;
	private static final String CLAIM_BOUNDARY =
			"A9 executable pilot only. Each row pairs the same generated world, target bill, status quo, "
			+ "and vote-random seed across a no-attack baseline, a fixed-total-budget mixed portfolio, "
			+ "full-budget single-attack controls, and single-action controls at the mixed allocation. "
			+ "The three portfolios implement the combinations specified in the experiment plan: A1+A2, "
			+ "A3+A4, and A5+A6+A8. Interaction coefficients, resource conversion, review capacity, and "
			+ "recovery behavior are synthetic stress assumptions, not empirical coordination rates, not "
			+ "a general mechanism ranking, and not evidence for real-world institutional adoption.";

	private enum ActionType
	{
		A1("A1", "add_clone_or_decoy"),
		A2("A2", "deploy_poison_pill_or_sequence"),
		A3("A3", "coordinate_astroturf_public_input"),
		A4("A4", "distort_harm_claim"),
		A5("A5", "submit_capacity_consuming_proposals"),
		A6("A6", "camouflage_lobbying_and_capture"),
		A8("A8", "distort_public_support_signal");

		private final String adversaryId;
		private final String actionKey;

		ActionType(String adversaryId, String actionKey) {
			this.adversaryId = adversaryId;
			this.actionKey = actionKey;
		}

		String adversaryId() {
			return adversaryId;
		}

		String actionKey() {
			return actionKey;
		}
	}

	private enum PortfolioKind
	{
		SELECTION_AMENDMENT(
				"clone-decoy-poison-pill",
				"selection_amendment_pairwise_majority",
				"selection-amendment-benign",
				"selection-amendment-a9-mixed",
				List.of(ActionType.A1, ActionType.A2)
		),
		PUBLIC_INPUT_HARM(
				"astroturf-harm-claims",
				"public_input_harm_review_majority",
				"public-input-harm-benign",
				"public-input-harm-a9-mixed",
				List.of(ActionType.A3, ActionType.A4)
		),
		FLOOD_CAPTURE_SIGNAL(
				"flood-camouflage-support-distortion",
				"portfolio_capacity_capture_signal",
				"portfolio-capacity-benign",
				"portfolio-capacity-a9-mixed",
				List.of(ActionType.A5, ActionType.A6, ActionType.A8)
		);

		private final String key;
		private final String mechanismFamily;
		private final String baselineScenario;
		private final String attackedScenario;
		private final List<ActionType> actions;

		PortfolioKind(
				String key,
				String mechanismFamily,
				String baselineScenario,
				String attackedScenario,
				List<ActionType> actions
		) {
			this.key = key;
			this.mechanismFamily = mechanismFamily;
			this.baselineScenario = baselineScenario;
			this.attackedScenario = attackedScenario;
			this.actions = actions;
		}

		String key() {
			return key;
		}

		String mechanismFamily() {
			return mechanismFamily;
		}

		String baselineScenario() {
			return baselineScenario;
		}

		String attackedScenario() {
			return attackedScenario;
		}

		List<ActionType> actions() {
			return actions;
		}
	}

	private record AttackConfig(
			PortfolioKind portfolio,
			int budgetValue,
			InformationLevel informationLevel
	) {
		String key() {
			return portfolio.key() + "-" + informationLevel.key() + "-budget-" + budgetValue;
		}

		double informationMultiplier() {
			return informationLevel == InformationLevel.HIGH ? 1.18 : 1.0;
		}
	}

	private record AttackPlan(Map<ActionType, Integer> allocations)
	{
		AttackPlan {
			allocations = Map.copyOf(allocations);
			for (Map.Entry<ActionType, Integer> entry : allocations.entrySet()) {
				if (entry.getValue() < 0) {
					throw new IllegalArgumentException("Attack allocations must be nonnegative.");
				}
			}
		}

		static AttackPlan none() {
			return new AttackPlan(Map.of());
		}

		static AttackPlan single(ActionType action, int units) {
			return new AttackPlan(units == 0 ? Map.of() : Map.of(action, units));
		}

		int units(ActionType action) {
			return allocations.getOrDefault(action, 0);
		}

		int totalUnits() {
			return allocations.values().stream().mapToInt(Integer::intValue).sum();
		}

		List<ActionType> activeActions() {
			return allocations.entrySet().stream()
			                  .filter(entry -> entry.getValue() > 0)
			                  .map(Map.Entry::getKey)
			                  .sorted(Comparator.comparing(Enum::ordinal))
			                  .toList();
		}
	}

	private record ProcessHarness(
			LegislativeProcess process,
			AdministrativeReviewCapacityProcess capacityProcess
	) {}

	private record ControlResult(
			ActionType action,
			int budgetUnits,
			Bill inputBill,
			BillOutcome outcome,
			double degradation,
			boolean adverseFailure,
			double administrativeBurdenAdded
	) {}

	private record RecoveryResult(
			boolean applicable,
			boolean overloadObserved,
			boolean capacityRecovered,
			int recoveryCycles,
			double backlogBeforeRecovery,
			double backlogAfterRecovery,
			double remainingCapacityShare
	) {
		static RecoveryResult notApplicable() {
			return new RecoveryResult(false, false, false, 0, 0.0, 0.0, 1.0);
		}

		String status(PortfolioKind portfolio) {
			if (!applicable) {
				return portfolio == PortfolioKind.PUBLIC_INPUT_HARM
						? "same_case_review_only"
						: "not_modeled_for_selection_amendment";
			}
			if (!overloadObserved) {
				return "not_needed";
			}
			return capacityRecovered
					? "capacity_recovered_outcomes_not_replayed"
					: "residual_overload_after_recovery_window";
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			AttackPlan mixedPlan,
			Bill latentBill,
			Bill mixedInputBill,
			BillOutcome baseline,
			BillOutcome mixed,
			List<ControlResult> sameBudgetSingles,
			List<ControlResult> allocatedComponentSingles,
			ControlResult strongestSingle,
			double mixedDegradation,
			double strongestSingleDegradation,
			double interactionDegradation,
			double componentLossSum,
			double superadditiveLoss,
			boolean mixedFailure,
			boolean anySameBudgetSingleFailure,
			boolean mixedDominatesStrongestSingle,
			boolean mixedOnlySuccess,
			double administrativeBurdenAdded,
			double strongestSingleAdministrativeBurdenAdded,
			double queueOverflowAdded,
			RecoveryResult recovery
	) {
		TraceRow withRecovery(RecoveryResult result) {
			return new TraceRow(
					runIndex,
					worldSeed,
					billIndex,
					config,
					mixedPlan,
					latentBill,
					mixedInputBill,
					baseline,
					mixed,
					sameBudgetSingles,
					allocatedComponentSingles,
					strongestSingle,
					mixedDegradation,
					strongestSingleDegradation,
					interactionDegradation,
					componentLossSum,
					superadditiveLoss,
					mixedFailure,
					anySameBudgetSingleFailure,
					mixedDominatesStrongestSingle,
					mixedOnlySuccess,
					administrativeBurdenAdded,
					strongestSingleAdministrativeBurdenAdded,
					queueOverflowAdded,
					result
			);
		}
	}

	private A9MixedAdversaryPortfolioStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a9.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a9-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a9-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a9-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a9.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a9-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a9-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a9-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			for (PortfolioKind portfolio : PortfolioKind.values()) {
				long worldSeed = mix(seed, run, 8909 + (portfolio.ordinal() * 211));
				SimulationWorld world = generator.generate(worldSpec(portfolio, legislators, bills), worldSeed);
				for (InformationLevel informationLevel : List.of(InformationLevel.MEDIUM, InformationLevel.HIGH)) {
					for (int budget : List.of(4, 8, 12)) {
						AttackConfig config = new AttackConfig(portfolio, budget, informationLevel);
						traces.addAll(runCell(world, worldSeed, run, config, seed));
					}
				}
			}
		}
		return traces;
	}

	private static List<TraceRow> runCell(
			SimulationWorld world,
			long worldSeed,
			int runIndex,
			AttackConfig config,
			long seed
	) {
		AttackPlan baselinePlan = AttackPlan.none();
		AttackPlan mixedPlan = mixedPlan(config.portfolio(), config.budgetValue());
		if (mixedPlan.totalUnits() != config.budgetValue()) {
			throw new IllegalStateException("Mixed allocation must equal the fixed joint budget.");
		}

		ProcessHarness baselineHarness = processHarness(world, config, baselinePlan, "A9 baseline");
		ProcessHarness mixedHarness = processHarness(world, config, mixedPlan, "A9 mixed portfolio");
		Map<ActionType, ProcessHarness> fullBudgetHarnesses = new EnumMap<>(ActionType.class);
		Map<ActionType, ProcessHarness> componentHarnesses = new EnumMap<>(ActionType.class);
		for (ActionType action : config.portfolio().actions()) {
			fullBudgetHarnesses.put(
					action,
					processHarness(world, config, AttackPlan.single(action, config.budgetValue()), "A9 full single " + action.adversaryId())
			);
			componentHarnesses.put(
					action,
					processHarness(world, config, AttackPlan.single(action, mixedPlan.units(action)), "A9 component " + action.adversaryId())
			);
		}

		List<TraceRow> cellTraces = new ArrayList<>();
		for (int billIndex = 0; billIndex < world.bills().size(); billIndex++) {
			Bill latentBill = caseBill(config.portfolio(), world.bills().get(billIndex), billIndex);
			long voteSeed = mix(
					seed,
					runIndex,
					9709 + (config.portfolio().ordinal() * 1009) + (config.budgetValue() * 31)
							+ (config.informationLevel().ordinal() * 101) + billIndex
			);
			BillOutcome baseline = consider(
					baselineHarness,
					config,
					baselinePlan,
					latentBill,
					latentBill,
					voteSeed,
					world
			);
			Bill mixedInput = attackBill(config, mixedPlan, latentBill, billIndex);
			BillOutcome mixed = consider(
					mixedHarness,
					config,
					mixedPlan,
					latentBill,
					mixedInput,
					voteSeed,
					world
			);

			List<ControlResult> fullBudgetControls = new ArrayList<>();
			List<ControlResult> componentControls = new ArrayList<>();
			for (ActionType action : config.portfolio().actions()) {
				AttackPlan fullPlan = AttackPlan.single(action, config.budgetValue());
				Bill fullInput = attackBill(config, fullPlan, latentBill, billIndex);
				BillOutcome fullOutcome = consider(
						fullBudgetHarnesses.get(action),
						config,
						fullPlan,
						latentBill,
						fullInput,
						voteSeed,
						world
				);
				fullBudgetControls.add(controlResult(action, config.budgetValue(), latentBill, fullInput, baseline, fullOutcome, config.portfolio()));

				int componentUnits = mixedPlan.units(action);
				AttackPlan componentPlan = AttackPlan.single(action, componentUnits);
				Bill componentInput = attackBill(config, componentPlan, latentBill, billIndex);
				BillOutcome componentOutcome = consider(
						componentHarnesses.get(action),
						config,
						componentPlan,
						latentBill,
						componentInput,
						voteSeed,
						world
				);
				componentControls.add(controlResult(action, componentUnits, latentBill, componentInput, baseline, componentOutcome, config.portfolio()));
			}
			cellTraces.add(trace(
					runIndex,
					worldSeed,
					billIndex,
					config,
					mixedPlan,
					latentBill,
					mixedInput,
					baseline,
					mixed,
					fullBudgetControls,
					componentControls
			));
		}

		RecoveryResult recovery = recover(mixedHarness);
		return cellTraces.stream().map(trace -> trace.withRecovery(recovery)).toList();
	}

	private static AttackPlan mixedPlan(PortfolioKind portfolio, int budget) {
		EnumMap<ActionType, Integer> allocation = new EnumMap<>(ActionType.class);
		if (portfolio.actions().size() == 2) {
			allocation.put(portfolio.actions().get(0), budget / 2);
			allocation.put(portfolio.actions().get(1), budget - (budget / 2));
		} else {
			int base = budget / 3;
			int remainder = budget % 3;
			for (int index = 0; index < portfolio.actions().size(); index++) {
				allocation.put(portfolio.actions().get(index), base + (index < remainder ? 1 : 0));
			}
		}
		return new AttackPlan(allocation);
	}

	private static WorldSpec worldSpec(PortfolioKind portfolio, int legislators, int bills) {
		return switch (portfolio) {
			case SELECTION_AMENDMENT -> new WorldSpec(
					legislators,
					bills,
					4,
					0.76,
					0.70,
					0.46,
					0.60,
					0.36,
					PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
					1.0,
					ProposalShockProfile.HIGH_BENEFIT_EXTREME_REFORM
			);
			case PUBLIC_INPUT_HARM -> new WorldSpec(
					legislators,
					bills,
					4,
					0.76,
					0.68,
					0.50,
					0.58,
					0.40,
					PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
					1.0,
					ProposalShockProfile.BASELINE
			);
			case FLOOD_CAPTURE_SIGNAL -> new WorldSpec(
					legislators,
					bills,
					4,
					0.72,
					0.70,
					0.78,
					0.48,
					0.34,
					PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
					1.0,
					ProposalShockProfile.POPULAR_HARMFUL_BILL
			);
		};
	}

	private static Bill caseBill(PortfolioKind portfolio, Bill bill, int billIndex) {
		return switch (portfolio) {
			case SELECTION_AMENDMENT -> selectionCaseBill(bill, billIndex);
			case PUBLIC_INPUT_HARM -> publicInputHarmCaseBill(bill, billIndex);
			case FLOOD_CAPTURE_SIGNAL -> floodCaptureCaseBill(bill, billIndex);
		};
	}

	private static Bill selectionCaseBill(Bill bill, int billIndex) {
		if (billIndex % 3 != 0) {
			return bill;
		}
		double support = Math.max(bill.publicSupport(), 0.640);
		double benefit = Math.max(bill.publicBenefit(), 0.700);
		return bill.withAmendment(
				Values.clamp(bill.ideologyPosition() * 0.55, -1.0, 1.0),
				support,
				benefit
		).withAffectedGroup(
				bill.affectedGroup(),
				Math.max(bill.affectedGroupSupport(), 0.580),
				Math.min(bill.concentratedHarm(), 0.320),
				bill.compensationCost()
		);
	}

	private static Bill publicInputHarmCaseBill(Bill bill, int billIndex) {
		if (billIndex % 2 == 0) {
			double support = Math.max(bill.publicSupport(), 0.680);
			double benefit = Math.max(bill.publicBenefit(), 0.740);
			return bill.withAmendment(
					Values.clamp(bill.ideologyPosition() * 0.40, -1.0, 1.0),
					support,
					benefit
			).withAffectedGroup(
					bill.affectedGroup(),
					Math.max(bill.affectedGroupSupport(), 0.680),
					Math.min(Math.max(bill.concentratedHarm(), 0.300), 0.360),
					Math.min(bill.compensationCost(), 0.150)
			).withPublicBenefitUncertainty(Math.min(bill.publicBenefitUncertainty(), 0.220));
		}
		double support = Math.min(bill.publicSupport(), 0.480);
		double benefit = Math.min(bill.publicBenefit(), 0.360);
		return bill.withAmendment(
				Values.clamp(bill.ideologyPosition() * 0.35, -1.0, 1.0),
				support,
				benefit
		).withLobbyActivity(
				Math.max(bill.lobbyPressure(), 0.480),
				support,
				benefit,
				Math.max(bill.privateGain(), 0.640),
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0
		).withAffectedGroup(
				bill.affectedGroup(),
				Math.min(bill.affectedGroupSupport(), 0.320),
				Math.max(bill.concentratedHarm(), 0.640),
				Math.max(bill.compensationCost(), 0.320)
		).withPublicBenefitUncertainty(Math.max(bill.publicBenefitUncertainty(), 0.440));
	}

	private static Bill floodCaptureCaseBill(Bill bill, int billIndex) {
		if (billIndex % 2 != 0) {
			return bill;
		}
		double support = Math.max(Math.min(bill.publicSupport(), 0.620), 0.540);
		double benefit = Math.min(bill.publicBenefit(), 0.390);
		return bill.withAmendment(
				Values.clamp(bill.ideologyPosition() * 0.42, -1.0, 1.0),
				support,
				benefit
		).withLobbyActivity(
				Math.max(bill.lobbyPressure(), 0.560),
				support,
				benefit,
				Math.max(bill.privateGain(), 0.680),
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0
		).withAffectedGroup(
				bill.affectedGroup(),
				Math.min(bill.affectedGroupSupport(), 0.300),
				Math.max(bill.concentratedHarm(), 0.620),
				Math.max(bill.compensationCost(), 0.300)
		).withPublicBenefitUncertainty(Math.max(bill.publicBenefitUncertainty(), 0.420));
	}

	private static ProcessHarness processHarness(
			SimulationWorld world,
			AttackConfig config,
			AttackPlan plan,
			String name
	) {
		return switch (config.portfolio()) {
			case SELECTION_AMENDMENT -> new ProcessHarness(
					selectionAmendmentProcess(world, config, plan, name),
					null
			);
			case PUBLIC_INPUT_HARM -> new ProcessHarness(
					publicInputHarmProcess(world, config, plan, name),
					null
			);
			case FLOOD_CAPTURE_SIGNAL -> capacityProcess(world, name);
		};
	}

	private static LegislativeProcess selectionAmendmentProcess(
			SimulationWorld world,
			AttackConfig config,
			AttackPlan plan,
			String name
	) {
		int cloneDecoyUnits = plan.units(ActionType.A1);
		int poisonUnits = plan.units(ActionType.A2);
		int interactionUnits = Math.min(cloneDecoyUnits, poisonUnits);
		Chamber chamber = new Chamber(
				name + " chamber",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		double poisonProbability = poisonUnits == 0
				? 0.0
				: Math.min(
						0.94,
						0.16 + (0.044 * poisonUnits * config.informationMultiplier()) + (0.030 * interactionUnits)
				);
		LegislativeProcess amendments = new MultiRoundAmendmentProcess(
				name + " amendment path",
				new UnicameralProcess(name + " floor", chamber),
				world.legislators(),
				3 + Math.min(9, poisonUnits),
				config.informationLevel() == InformationLevel.HIGH ? 0.018 : 0.022,
				config.informationLevel() == InformationLevel.HIGH ? 1.32 : 1.18,
				poisonProbability
		);
		int clones = (cloneDecoyUnits + 1) / 2;
		int decoys = cloneDecoyUnits / 2;
		double overloadPenalty = cloneDecoyUnits == 0
				? 0.0
				: Math.min(0.180, (0.007 * cloneDecoyUnits) + (0.010 * interactionUnits));
		double badFaithPenalty = cloneDecoyUnits == 0
				? 0.0
				: Math.min(0.340, 0.025 + (0.005 * cloneDecoyUnits) + (0.022 * interactionUnits));
		return new CompetingAlternativesProcess(
				name,
				amendments,
				world.legislators(),
				AlternativeSelectionRule.PAIRWISE_MAJORITY,
				4,
				true,
				clones,
				decoys,
				config.informationLevel() == InformationLevel.HIGH ? 0.46 : 0.58,
				overloadPenalty,
				badFaithPenalty
		);
	}

	private static LegislativeProcess publicInputHarmProcess(
			SimulationWorld world,
			AttackConfig config,
			AttackPlan plan,
			String name
	) {
		int publicInputUnits = plan.units(ActionType.A3);
		int harmClaimUnits = plan.units(ActionType.A4);
		Chamber ordinary = new Chamber(
				name + " ordinary chamber",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		Chamber highHarm = new Chamber(
				name + " harm-review chamber",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.supermajority(0.64)
		);
		LegislativeProcess harm = new HarmWeightedThresholdProcess(name, ordinary, highHarm, 0.46);
		harm = new InstrumentedHarmReviewProcess(name, harm, 0.035 + (0.045 * harmClaimUnits));
		LegislativeProcess block = new PublicInputBlockProcess(name + " public-input gate");

		int panelSize = publicInputUnits == 0 ? 96 : Math.max(24, 92 - (5 * publicInputUnits));
		double panelNoise = publicInputUnits == 0
				? 0.035
				: Math.min(0.300, 0.045 + (0.012 * publicInputUnits * config.informationMultiplier()));
		double informationQuality = publicInputUnits == 0
				? 0.780
				: Math.max(0.360, 0.760 - (0.020 * publicInputUnits * config.informationMultiplier()));
		double manipulationRisk = publicInputUnits == 0
				? 0.025
				: Math.min(0.760, 0.040 + (0.032 * publicInputUnits * config.informationMultiplier()));
		double certificationThreshold = publicInputUnits == 0 ? 0.540 : 0.570;
		LegislativeProcess panel = new CitizenPanelReviewProcess(
				name + " citizen panel",
				harm,
				block,
				CitizenPanelMode.THRESHOLD_ADJUSTMENT,
				panelSize,
				panelNoise,
				informationQuality,
				manipulationRisk,
				certificationThreshold
		);
		double objectionThreshold = publicInputUnits == 0
				? 0.665
				: Math.max(0.380, 0.650 - (0.018 * publicInputUnits * config.informationMultiplier()));
		double objectionNoise = publicInputUnits == 0
				? 0.012
				: Math.min(0.200, 0.020 + (0.011 * publicInputUnits * config.informationMultiplier()));
		return new PublicObjectionWindowProcess(
				name,
				harm,
				panel,
				objectionThreshold,
				objectionNoise,
				false
		);
	}

	private static ProcessHarness capacityProcess(SimulationWorld world, String name) {
		Scenario portfolio = ScenarioCatalog.scenariosForKeys(List.of("portfolio-hybrid-legislature")).getFirst();
		LegislativeProcess defended = portfolio.buildProcess(world);
		Chamber overflowChamber = new Chamber(
				name + " overflow chamber",
				world.legislators(),
				VotingStrategies.antiCapture(),
				AffirmativeThresholdRule.simpleMajority()
		);
		LegislativeProcess overflow = new UnicameralProcess(name + " anti-capture overflow", overflowChamber);
		AdministrativeReviewCapacityProcess capacity = new AdministrativeReviewCapacityProcess(
				name,
				defended,
				overflow,
				CAPACITY_UNITS,
				RECOVERY_UNITS_PER_CYCLE,
				MINIMUM_DEFENDED_COVERAGE
		);
		return new ProcessHarness(capacity, capacity);
	}

	private static Bill attackBill(
			AttackConfig config,
			AttackPlan plan,
			Bill latentBill,
			int billIndex
	) {
		Bill attacked = latentBill;
		if (plan.units(ActionType.A3) > 0) {
			attacked = applyPublicInputAttack(attacked, latentBill, plan.units(ActionType.A3), config);
		}
		if (plan.units(ActionType.A4) > 0) {
			attacked = applyHarmClaimAttack(attacked, latentBill, plan.units(ActionType.A4), config, billIndex);
		}
		if (plan.units(ActionType.A6) > 0) {
			attacked = applyCamouflageAttack(attacked, plan.units(ActionType.A6), config);
		}
		if (plan.units(ActionType.A8) > 0) {
			attacked = applySupportDistortion(attacked, latentBill, plan.units(ActionType.A8), config);
		}
		return attacked;
	}

	private static Bill applyPublicInputAttack(
			Bill bill,
			Bill latentBill,
			int units,
			AttackConfig config
	) {
		double direction = latentHighRisk(latentBill) ? 1.0 : -1.0;
		double shift = Math.min(0.180, (0.036 + (0.008 * units)) * config.informationMultiplier());
		double revisedSupport = Values.clamp(bill.publicSupport() + (direction * shift), 0.0, 1.0);
		double revisedSalience = Values.clamp(
				bill.salience() + Math.min(0.240, 0.040 + (0.012 * units)),
				0.0,
				1.0
		);
		return bill.withPublicSignal(revisedSupport, revisedSalience)
		           .withLobbyActivity(
				           bill.lobbyPressure(),
				           revisedSupport,
				           bill.privateGain(),
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           1.60 * units,
				           0.0
		           )
		           .withAttentionSpend(0.18 * units);
	}

	private static Bill applyHarmClaimAttack(
			Bill bill,
			Bill latentBill,
			int units,
			AttackConfig config,
			int billIndex
	) {
		boolean understate = latentHighRisk(latentBill) || billIndex % 2 != 0;
		double direction = understate ? -1.0 : 1.0;
		double harmShift = Math.min(0.420, (0.055 + (0.024 * units)) * config.informationMultiplier());
		double supportShift = Math.min(0.320, (0.035 + (0.017 * units)) * config.informationMultiplier());
		double revisedHarm = Values.clamp(bill.concentratedHarm() + (direction * harmShift), 0.0, 1.0);
		double revisedAffectedSupport = Values.clamp(
				bill.affectedGroupSupport() - (direction * supportShift),
				0.0,
				1.0
		);
		double revisedCost = Values.clamp(
				bill.compensationCost() + (direction * Math.min(0.260, 0.020 * units)),
				0.0,
				1.0
		);
		return bill.withAffectedGroup(bill.affectedGroup(), revisedAffectedSupport, revisedHarm, revisedCost)
		           .withPublicBenefitUncertainty(
				           Values.clamp(bill.publicBenefitUncertainty() + (0.018 * units), 0.0, 1.0)
		           )
		           .withAttentionSpend(0.12 * units);
	}

	private static Bill applyCamouflageAttack(Bill bill, int units, AttackConfig config) {
		double intensity = Math.min(0.90, 0.135 * units * config.informationMultiplier());
		double revisedLobbyPressure = Values.clamp(bill.lobbyPressure() * (1.0 - intensity), -1.0, 1.0);
		double revisedPrivateGain = Values.clamp(bill.privateGain() * (1.0 - (0.78 * intensity)), 0.0, 1.0);
		double routedSpend = 0.22 * units;
		return bill.withLobbyActivity(
				revisedLobbyPressure,
				bill.publicSupport(),
				bill.publicBenefit(),
				revisedPrivateGain,
				routedSpend,
				0.0,
				routedSpend * 0.08,
				routedSpend * 0.16,
				routedSpend * 0.48,
				routedSpend * 0.20,
				routedSpend * 0.08
		).withAttentionSpend(0.08 * units);
	}

	private static Bill applySupportDistortion(
			Bill bill,
			Bill latentBill,
			int units,
			AttackConfig config
	) {
		double direction = latentHighRisk(latentBill) ? 1.0 : -1.0;
		double shift = Math.min(0.260, 0.026 * units * config.informationMultiplier());
		double revisedSupport = Values.clamp(bill.publicSupport() + (direction * shift), 0.0, 1.0);
		double revisedSalience = Values.clamp(bill.salience() + Math.min(0.220, 0.014 * units), 0.0, 1.0);
		return bill.withPublicSignal(revisedSupport, revisedSalience)
		           .withLobbyActivity(
				           bill.lobbyPressure(),
				           revisedSupport,
				           bill.privateGain(),
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           2.40 * units,
				           0.0
		           )
		           .withAttentionSpend(0.24 * units);
	}

	private static BillOutcome consider(
			ProcessHarness harness,
			AttackConfig config,
			AttackPlan plan,
			Bill latentBill,
			Bill inputBill,
			long voteSeed,
			SimulationWorld world
	) {
		if (harness.capacityProcess() != null) {
			harness.capacityProcess().submitExternalDemand(externalDemand(config, plan, latentBill));
		}
		return harness.process().consider(
				inputBill,
				new VoteContext(world.partyPositions(), new Random(voteSeed), world.initialPolicy().position())
		);
	}

	private static double externalDemand(AttackConfig config, AttackPlan plan, Bill latentBill) {
		int floodingUnits = plan.units(ActionType.A5);
		if (floodingUnits == 0) {
			return 0.0;
		}
		double targeting = config.informationLevel() == InformationLevel.HIGH && latentHighRisk(latentBill) ? 1.12 : 1.0;
		return 1.60 * floodingUnits * targeting;
	}

	private static ControlResult controlResult(
			ActionType action,
			int budgetUnits,
			Bill latentBill,
			Bill inputBill,
			BillOutcome baseline,
			BillOutcome outcome,
			PortfolioKind portfolio
	) {
		double degradation = degradation(portfolio, latentBill, baseline, outcome);
		return new ControlResult(
				action,
				budgetUnits,
				inputBill,
				outcome,
				degradation,
				adverseFailure(portfolio, latentBill, baseline, outcome, degradation),
				Math.max(0.0, administrativeBurden(outcome) - administrativeBurden(baseline))
		);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			AttackPlan mixedPlan,
			Bill latentBill,
			Bill mixedInput,
			BillOutcome baseline,
			BillOutcome mixed,
			List<ControlResult> sameBudgetSingles,
			List<ControlResult> componentSingles
	) {
		ControlResult strongestSingle = sameBudgetSingles.stream()
				.max(Comparator.comparingDouble(ControlResult::degradation)
				               .thenComparing(control -> control.action().adversaryId()))
				.orElseThrow();
		double mixedDegradation = degradation(config.portfolio(), latentBill, baseline, mixed);
		double strongestSingleDegradation = strongestSingle.degradation();
		double interactionDegradation = mixedDegradation - strongestSingleDegradation;
		double componentLossSum = componentSingles.stream().mapToDouble(ControlResult::degradation).sum();
		double superadditiveLoss = mixedDegradation - componentLossSum;
		boolean mixedFailure = adverseFailure(config.portfolio(), latentBill, baseline, mixed, mixedDegradation);
		boolean anySingleFailure = sameBudgetSingles.stream().anyMatch(ControlResult::adverseFailure);
		boolean mixedDominates = interactionDegradation > INTERACTION_EPSILON;
		boolean mixedOnlySuccess = mixedFailure && !anySingleFailure;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				mixedPlan,
				latentBill,
				mixedInput,
				baseline,
				mixed,
				List.copyOf(sameBudgetSingles),
				List.copyOf(componentSingles),
				strongestSingle,
				mixedDegradation,
				strongestSingleDegradation,
				interactionDegradation,
				componentLossSum,
				superadditiveLoss,
				mixedFailure,
				anySingleFailure,
				mixedDominates,
				mixedOnlySuccess,
				Math.max(0.0, administrativeBurden(mixed) - administrativeBurden(baseline)),
				strongestSingle.administrativeBurdenAdded(),
				Math.max(0.0, metric(mixed, "administrativeQueueOverflow") - metric(baseline, "administrativeQueueOverflow")),
				null
		);
	}

	private static double degradation(
			PortfolioKind portfolio,
			Bill latentBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		return Math.max(
				0.0,
				adverseOutcomeScore(portfolio, latentBill, attacked)
						- adverseOutcomeScore(portfolio, latentBill, baseline)
		);
	}

	private static double adverseOutcomeScore(
			PortfolioKind portfolio,
			Bill latentBill,
			BillOutcome outcome
	) {
		if (portfolio == PortfolioKind.SELECTION_AMENDMENT) {
			Bill selected = outcome.bill();
			if (outcome.enacted()) {
				return Values.clamp(
						(0.44 * (1.0 - selected.publicBenefit()))
								+ (0.24 * (1.0 - selected.publicSupport()))
								+ (0.18 * selected.concentratedHarm())
								+ (0.14 * selected.privateGain()),
						0.0,
						1.0
				);
			}
			return Values.clamp(
					(0.72 * Math.max(0.0, latentBill.publicBenefit() - 0.52))
							+ (0.28 * Math.max(0.0, latentBill.publicSupport() - 0.52)),
					0.0,
					1.0
			);
		}
		if (outcome.enacted()) {
			return latentRisk(latentBill);
		}
		return Values.clamp(
				(0.74 * Math.max(0.0, latentBill.publicBenefit() - 0.56))
						+ (0.26 * Math.max(0.0, latentBill.publicSupport() - 0.54)),
				0.0,
				1.0
		);
	}

	private static boolean adverseFailure(
			PortfolioKind portfolio,
			Bill latentBill,
			BillOutcome baseline,
			BillOutcome attacked,
			double degradation
	) {
		if (degradation <= 0.020) {
			return false;
		}
		boolean highBenefitBlock = baseline.enacted()
				&& !attacked.enacted()
				&& latentBill.publicBenefit() >= 0.620;
		boolean riskyEnactment = !baseline.enacted()
				&& attacked.enacted()
				&& latentHighRisk(latentBill);
		if (portfolio != PortfolioKind.SELECTION_AMENDMENT) {
			return highBenefitBlock || riskyEnactment;
		}
		double benefitLoss = baseline.bill().publicBenefit() - attacked.bill().publicBenefit();
		double supportLoss = baseline.bill().publicSupport() - attacked.bill().publicSupport();
		double harmAdded = attacked.bill().concentratedHarm() - baseline.bill().concentratedHarm();
		return highBenefitBlock || benefitLoss > 0.050 || supportLoss > 0.050 || harmAdded > 0.050;
	}

	private static boolean latentHighRisk(Bill bill) {
		return latentRisk(bill) >= 0.480
				|| bill.publicBenefit() < 0.420
				|| AffectedGroupScoring.minorityHarm(bill) >= 0.240
				|| LobbyCaptureScoring.captureRisk(bill) >= 0.500;
	}

	private static double latentRisk(Bill bill) {
		return Values.clamp(
				(0.30 * (1.0 - bill.publicBenefit()))
						+ (0.24 * AffectedGroupScoring.minorityHarm(bill))
						+ (0.24 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.12 * bill.publicBenefitUncertainty())
						+ (0.10 * (1.0 - bill.publicSupport())),
				0.0,
				1.0
		);
	}

	private static RecoveryResult recover(ProcessHarness harness) {
		if (harness.capacityProcess() == null) {
			return RecoveryResult.notApplicable();
		}
		CapacitySnapshot before = harness.capacityProcess().snapshot();
		CapacitySnapshot after = before;
		int cycles = 0;
		while (!after.fullReviewReady() && cycles < MAX_RECOVERY_CYCLES) {
			after = harness.capacityProcess().advanceRecoveryCycle();
			cycles++;
		}
		return new RecoveryResult(
				true,
				before.everOverloaded(),
				after.fullReviewReady(),
				cycles,
				before.backlogUnits(),
				after.backlogUnits(),
				after.remainingCapacityShare()
		);
	}

	private static boolean correctionAttempted(TraceRow trace) {
		return switch (trace.config().portfolio()) {
			case SELECTION_AMENDMENT -> false;
			case PUBLIC_INPUT_HARM -> trace.mixed().signals().objectionWindows() > 0
					|| trace.mixed().signals().citizenReviews() > 0
					|| metric(trace.mixed(), "harmReviewTriggered") >= 0.50;
			case FLOOD_CAPTURE_SIGNAL -> trace.recovery().overloadObserved();
		};
	}

	private static boolean recoveryCorrectionFailure(TraceRow trace) {
		return trace.mixedFailure() && correctionAttempted(trace);
	}

	private static double administrativeBurden(BillOutcome outcome) {
		OutcomeSignals signals = outcome.signals();
		return (0.050 * outcome.bill().attentionSpend())
				+ (0.120 * signals.publicWillReviews())
				+ (0.140 * signals.objectionWindows())
				+ (0.180 * signals.citizenReviews())
				+ (0.100 * signals.lawReviews())
				+ (0.080 * signals.proposalBondReviews())
				+ metric(outcome, "legalReviewBurden")
				+ metric(outcome, "administrativeReviewDemand")
				+ metric(outcome, "administrativeExternalDemand")
				+ (0.10 * metric(outcome, "administrativeQueueOverflow"))
				+ (0.40 * metric(outcome, "administrativeOverflowFallback"));
	}

	private static double metric(BillOutcome outcome, String key) {
		return outcome.signals().supplementalMetrics().getOrDefault(key, 0.0);
	}

	private static long mix(long seed, int run, int stream) {
		long value = seed;
		value ^= 0x9E3779B97F4A7C15L + ((long) run << 6) + ((long) run >> 2);
		value ^= 0xBF58476D1CE4E5B9L * (stream + 31L);
		return value;
	}

	private static List<AttackConfig> attackConfigs() {
		List<AttackConfig> configs = new ArrayList<>();
		for (PortfolioKind portfolio : PortfolioKind.values()) {
			for (InformationLevel level : List.of(InformationLevel.MEDIUM, InformationLevel.HIGH)) {
				for (int budget : List.of(4, 8, 12)) {
					configs.add(new AttackConfig(portfolio, budget, level));
				}
			}
		}
		return configs;
	}

	private static List<TraceRow> group(List<TraceRow> traces, AttackConfig config) {
		return traces.stream().filter(trace -> trace.config().equals(config)).toList();
	}

	private static void writeTraceJsonl(
			Path path,
			List<TraceRow> traces,
			int runs,
			int legislators,
			int bills,
			long seed
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		for (TraceRow trace : traces) {
			builder.append(traceJson(trace, runs, legislators, bills, seed)).append('\n');
		}
		Files.writeString(path, builder.toString());
	}

	private static String traceJson(TraceRow trace, int runs, int legislators, int bills, long seed) {
		AdversarySpec spec = AdversaryCatalog.find(ADVERSARY_ID).orElseThrow();
		StringBuilder builder = new StringBuilder();
		builder.append('{');
		jsonProperty(builder, "seed", Long.toString(seed), false);
		jsonProperty(builder, "worldSeed", Long.toString(trace.worldSeed()), false);
		jsonProperty(builder, "runIndex", Integer.toString(trace.runIndex()), false);
		jsonProperty(builder, "billIndex", Integer.toString(trace.billIndex()), false);
		jsonProperty(builder, "runs", Integer.toString(runs), false);
		jsonProperty(builder, "legislators", Integer.toString(legislators), false);
		jsonProperty(builder, "baseBillsPerRun", Integer.toString(bills), false);
		jsonProperty(builder, "caseKey", CASE_KEY, true);
		jsonProperty(builder, "scenarioKey", trace.config().portfolio().attackedScenario(), true);
		jsonProperty(builder, "baselineScenarioKey", trace.config().portfolio().baselineScenario(), true);
		jsonProperty(builder, "mechanismFamily", trace.config().portfolio().mechanismFamily(), true);
		jsonProperty(builder, "portfolioKey", trace.config().portfolio().key(), true);
		jsonProperty(builder, "adversaryId", ADVERSARY_ID, true);
		jsonProperty(builder, "actorType", spec.actorType(), true);
		jsonProperty(builder, "objective", spec.objective(), true);
		jsonProperty(builder, "budgetUnit", BUDGET_UNIT, true);
		jsonProperty(builder, "budgetValue", Integer.toString(trace.config().budgetValue()), false);
		jsonProperty(builder, "informationLevel", trace.config().informationLevel().key(), true);
		jsonArray(builder, "attackActionList", actionList(trace));
		jsonObject(builder, "portfolioAllocation", allocationJson(trace));
		jsonObject(builder, "preAttackFeatures", billJson(trace.latentBill(), trace.latentBill()));
		jsonObject(builder, "attackedInputFeatures", billJson(trace.mixedInputBill(), trace.latentBill()));
		jsonObject(builder, "postAttackFeatures", billJson(trace.mixed().bill(), trace.latentBill()));
		jsonObject(builder, "institutionalPath", pathJson(trace));
		jsonObject(builder, "baselineOutcome", outcomeJson(trace.baseline(), trace.latentBill()));
		jsonObject(builder, "attackedOutcome", outcomeJson(trace.mixed(), trace.latentBill()));
		jsonObject(builder, "strongestSameBudgetSingle", controlJson(trace.strongestSingle(), trace.latentBill()));
		jsonObjectArray(builder, "sameBudgetSingleControls", trace.sameBudgetSingles(), trace.latentBill());
		jsonObjectArray(builder, "allocatedComponentControls", trace.allocatedComponentSingles(), trace.latentBill());
		jsonProperty(builder, "successFlag", Boolean.toString(trace.mixedOnlySuccess()), false);
		jsonObject(builder, "metricDeltas", metricDeltaJson(trace));
		jsonObject(builder, "interactionMetrics", interactionJson(trace));
		jsonObject(builder, "administrativeBurden", administrativeBurdenJson(trace));
		jsonProperty(builder, "recoveryStatus", trace.recovery().status(trace.config().portfolio()), true);
		jsonObject(builder, "recoveryMetrics", recoveryJson(trace));
		jsonProperty(builder, "claimBoundary", CLAIM_BOUNDARY, true);
		removeTrailingComma(builder);
		builder.append('}');
		return builder.toString();
	}

	private static void writeSummaryCsv(
			Path path,
			List<TraceRow> traces,
			int runs,
			int legislators,
			int bills,
			long seed
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,portfolioKey,componentAdversaries,componentCount,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,mixedFailureRate,anySameBudgetSingleFailureRate,mixedDominatesStrongestSingleRate,meanMixedDegradation,medianMixedDegradation,worstMixedDegradation,meanStrongestSingleDegradation,medianStrongestSingleDegradation,worstStrongestSingleDegradation,meanInteractionDegradation,medianInteractionDegradation,worstInteractionDegradation,positiveInteractionRate,meanSuperadditiveLoss,medianSuperadditiveLoss,worstSuperadditiveLoss,superadditiveRate,recoveryCorrectionAttemptRate,recoveryCorrectionFailureRate,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,meanStrongestSingleAdministrativeBurdenAdded,meanQueueOverflowAdded,worstQueueOverflowAdded,meanAttackerResourceSpend,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = group(traces, config);
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("mixed_adversary_portfolio")).append(',')
			       .append(csv(CASE_KEY)).append(',')
			       .append(csv(config.portfolio().baselineScenario())).append(',')
			       .append(csv(config.portfolio().attackedScenario())).append(',')
			       .append(csv(config.portfolio().mechanismFamily())).append(',')
			       .append(csv(config.portfolio().key())).append(',')
			       .append(csv(componentIds(config.portfolio()))).append(',')
			       .append(config.portfolio().actions().size()).append(',')
			       .append(csv(BUDGET_UNIT)).append(',')
			       .append(config.budgetValue()).append(',')
			       .append(csv(config.informationLevel().key())).append(',')
			       .append(runs).append(',')
			       .append(legislators).append(',')
			       .append(bills).append(',')
			       .append(group.size()).append(',')
			       .append(format(rate(group, TraceRow::mixedOnlySuccess))).append(',')
			       .append(format(rate(group, TraceRow::mixedFailure))).append(',')
			       .append(format(rate(group, TraceRow::anySameBudgetSingleFailure))).append(',')
			       .append(format(rate(group, TraceRow::mixedDominatesStrongestSingle))).append(',')
			       .append(format(mean(group, TraceRow::mixedDegradation))).append(',')
			       .append(format(median(group, TraceRow::mixedDegradation))).append(',')
			       .append(format(max(group, TraceRow::mixedDegradation))).append(',')
			       .append(format(mean(group, TraceRow::strongestSingleDegradation))).append(',')
			       .append(format(median(group, TraceRow::strongestSingleDegradation))).append(',')
			       .append(format(max(group, TraceRow::strongestSingleDegradation))).append(',')
			       .append(format(mean(group, TraceRow::interactionDegradation))).append(',')
			       .append(format(median(group, TraceRow::interactionDegradation))).append(',')
			       .append(format(max(group, TraceRow::interactionDegradation))).append(',')
			       .append(format(rate(group, trace -> trace.interactionDegradation() > INTERACTION_EPSILON))).append(',')
			       .append(format(mean(group, TraceRow::superadditiveLoss))).append(',')
			       .append(format(median(group, TraceRow::superadditiveLoss))).append(',')
			       .append(format(max(group, TraceRow::superadditiveLoss))).append(',')
			       .append(format(rate(group, trace -> trace.superadditiveLoss() > INTERACTION_EPSILON))).append(',')
			       .append(format(rate(group, A9MixedAdversaryPortfolioStressRunner::correctionAttempted))).append(',')
			       .append(format(rate(group, A9MixedAdversaryPortfolioStressRunner::recoveryCorrectionFailure))).append(',')
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(format(max(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(format(mean(group, TraceRow::strongestSingleAdministrativeBurdenAdded))).append(',')
			       .append(format(mean(group, TraceRow::queueOverflowAdded))).append(',')
			       .append(format(max(group, TraceRow::queueOverflowAdded))).append(',')
			       .append(format(mean(group, trace -> trace.mixedPlan().totalUnits()))).append(',')
			       .append(csv(recoveryStatus(group))).append(',')
			       .append(csv(TRACE_ARTIFACT)).append(',')
			       .append(csv(CLAIM_BOUNDARY)).append('\n');
		}
		Files.writeString(path, builder.toString());
	}

	private static void writeSummaryMarkdown(
			Path path,
			List<TraceRow> traces,
			int runs,
			int legislators,
			int bills,
			long seed
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		builder.append("# A9 Mixed-Adversary Portfolio Stress Summary\n\n");
		builder.append("Status: `partial_a9_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A9 mixed adversary portfolio\n");
		builder.append("- Same-world, same-bill, same-status-quo, same-vote-seed runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Portfolio families: 3\n");
		builder.append("- Joint budgets: 4, 8, and 12 exact attack units\n");
		builder.append("- Information levels: medium and high\n");
		builder.append("- Summary cells: ").append(attackConfigs().size()).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Success metric: mixed adverse failure with no adverse failure in any full-budget constituent control\n");
		builder.append("- Interaction metric: mixed degradation minus the strongest full-budget single degradation\n");
		builder.append("- Superadditive metric: mixed degradation minus the sum of allocated-component single degradations\n\n");
		builder.append("| Portfolio | Components | Information | Budget | Rows | Mixed-only success | Mixed failure | Any single failure | Mixed dominates | Median mixed degradation | Median strongest single | Median interaction | Worst interaction | Superadditive rate | Correction failure | Mean admin burden |\n");
		builder.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = group(traces, config);
			builder.append("| ").append(config.portfolio().key()).append(" | ")
			       .append(componentIds(config.portfolio())).append(" | ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::mixedOnlySuccess))).append(" | ")
			       .append(format(rate(group, TraceRow::mixedFailure))).append(" | ")
			       .append(format(rate(group, TraceRow::anySameBudgetSingleFailure))).append(" | ")
			       .append(format(rate(group, TraceRow::mixedDominatesStrongestSingle))).append(" | ")
			       .append(format(median(group, TraceRow::mixedDegradation))).append(" | ")
			       .append(format(median(group, TraceRow::strongestSingleDegradation))).append(" | ")
			       .append(format(median(group, TraceRow::interactionDegradation))).append(" | ")
			       .append(format(max(group, TraceRow::interactionDegradation))).append(" | ")
			       .append(format(rate(group, trace -> trace.superadditiveLoss() > INTERACTION_EPSILON))).append(" | ")
			       .append(format(rate(group, A9MixedAdversaryPortfolioStressRunner::recoveryCorrectionFailure))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" |\n");
		}
		builder.append("\nGate status: this completes bounded executable coverage for A1-A9 and supplies the required mixed-only comparison design. The robustness breakout remains below manuscript gate until the result is replicated across additional seeds and mechanism variants, temporal or substantive correction is expanded, and external validation anchors the synthetic attack and capacity assumptions.\n");
		Files.writeString(path, builder.toString());
	}

	private static void writeRunManifest(
			Path path,
			List<TraceRow> traces,
			int runs,
			int legislators,
			int bills,
			long seed
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		builder.append("{\n");
		property(builder, 1, "manifestVersion", "adversarial-stress-a9-run-v0", true);
		property(builder, 1, "status", "partial_a9_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "portfolioCount", Integer.toString(PortfolioKind.values().length), false, true);
		property(builder, 1, "summaryRows", Integer.toString(attackConfigs().size()), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		property(builder, 1, "mixedOnlySuccessRows", Long.toString(traces.stream().filter(TraceRow::mixedOnlySuccess).count()), false, true);
		property(builder, 1, "pairingDesign", "same_world_same_bill_same_status_quo_same_vote_seed_with_full_and_component_single_controls", true);
		arrayProperty(builder, 1, "portfolioKeys", List.of(
				PortfolioKind.SELECTION_AMENDMENT.key(),
				PortfolioKind.PUBLIC_INPUT_HARM.key(),
				PortfolioKind.FLOOD_CAPTURE_SIGNAL.key()
		), true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a9-summary.csv",
				"reports/adversarial-stress-a9-summary.md",
				TRACE_ARTIFACT
		), true);
		property(builder, 1, "claimBoundary", CLAIM_BOUNDARY, true);
		builder.append("\t\"gateStatus\": \"not_manuscript_ready\"\n");
		builder.append("}\n");
		Files.writeString(path, builder.toString());
	}

	private interface Metric
	{
		double value(TraceRow trace);
	}

	private interface Flag
	{
		boolean value(TraceRow trace);
	}

	private static double mean(List<TraceRow> rows, Metric metric) {
		if (rows.isEmpty()) {
			return 0.0;
		}
		double sum = 0.0;
		for (TraceRow row : rows) {
			sum += metric.value(row);
		}
		return sum / rows.size();
	}

	private static double median(List<TraceRow> rows, Metric metric) {
		if (rows.isEmpty()) {
			return 0.0;
		}
		List<Double> values = rows.stream().map(metric::value).sorted().toList();
		int middle = values.size() / 2;
		if (values.size() % 2 == 1) {
			return values.get(middle);
		}
		return (values.get(middle - 1) + values.get(middle)) / 2.0;
	}

	private static double max(List<TraceRow> rows, Metric metric) {
		return rows.stream().map(metric::value).max(Comparator.naturalOrder()).orElse(0.0);
	}

	private static double rate(List<TraceRow> rows, Flag flag) {
		if (rows.isEmpty()) {
			return 0.0;
		}
		int count = 0;
		for (TraceRow row : rows) {
			if (flag.value(row)) {
				count++;
			}
		}
		return (double) count / rows.size();
	}

	private static String recoveryStatus(List<TraceRow> rows) {
		return rows.stream()
		           .map(trace -> trace.recovery().status(trace.config().portfolio()))
		           .distinct()
		           .sorted()
		           .collect(Collectors.joining("+"));
	}

	private static String componentIds(PortfolioKind portfolio) {
		return portfolio.actions().stream().map(ActionType::adversaryId).collect(Collectors.joining("+"));
	}

	private static List<String> actionList(TraceRow trace) {
		List<String> actions = new ArrayList<>();
		actions.add("coordinate_fixed_budget_portfolio");
		for (ActionType action : trace.config().portfolio().actions()) {
			for (int unit = 0; unit < trace.mixedPlan().units(action); unit++) {
				actions.add(action.actionKey());
			}
		}
		actions.add("compare_to_full_budget_single_controls");
		actions.add("compare_to_allocated_component_controls");
		return actions;
	}

	private static String allocationJson(TraceRow trace) {
		StringBuilder builder = new StringBuilder("{");
		for (ActionType action : trace.config().portfolio().actions()) {
			jsonProperty(builder, action.adversaryId(), Integer.toString(trace.mixedPlan().units(action)), false);
		}
		jsonProperty(builder, "total", Integer.toString(trace.mixedPlan().totalUnits()), false);
		removeTrailingComma(builder);
		return builder.append('}').toString();
	}

	private static String billJson(Bill bill, Bill latentBill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"observablePublicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"generatedPublicSupport\":" + format(latentBill.publicSupport()) + ","
				+ "\"supportSignalError\":" + format(Math.abs(bill.publicSupport() - latentBill.publicSupport())) + ","
				+ "\"observablePublicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"generatedPublicBenefit\":" + format(latentBill.publicBenefit()) + ","
				+ "\"observableAffectedGroupSupport\":" + format(bill.affectedGroupSupport()) + ","
				+ "\"generatedAffectedGroupSupport\":" + format(latentBill.affectedGroupSupport()) + ","
				+ "\"observableConcentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"generatedConcentratedHarm\":" + format(latentBill.concentratedHarm()) + ","
				+ "\"observablePrivateGain\":" + format(bill.privateGain()) + ","
				+ "\"generatedPrivateGain\":" + format(latentBill.privateGain()) + ","
				+ "\"lobbyPressure\":" + format(bill.lobbyPressure()) + ","
				+ "\"salience\":" + format(bill.salience()) + ","
				+ "\"publicSignalMovement\":" + format(bill.publicSignalMovement()) + ","
				+ "\"lobbySpend\":" + format(bill.lobbySpend()) + ","
				+ "\"publicCampaignSpend\":" + format(bill.publicCampaignSpend()) + ","
				+ "\"attentionSpend\":" + format(bill.attentionSpend())
				+ "}";
	}

	private static String outcomeJson(BillOutcome outcome, Bill latentBill) {
		return "{"
				+ "\"enacted\":" + outcome.enacted() + ","
				+ "\"finalReason\":\"" + json(outcome.finalReason()) + "\","
				+ "\"agendaDisposition\":\"" + outcome.agendaDisposition() + "\","
				+ "\"averageYayShare\":" + format(outcome.averageYayShare()) + ","
				+ "\"statusQuoBefore\":" + format(outcome.statusQuoBefore()) + ","
				+ "\"statusQuoAfter\":" + format(outcome.statusQuoAfter()) + ","
				+ "\"selectedBill\":" + billJson(outcome.bill(), latentBill)
				+ "}";
	}

	private static String controlJson(ControlResult control, Bill latentBill) {
		return "{"
				+ "\"componentAdversaryId\":\"" + control.action().adversaryId() + "\","
				+ "\"budgetUnits\":" + control.budgetUnits() + ","
				+ "\"inputFeatures\":" + billJson(control.inputBill(), latentBill) + ","
				+ "\"outcome\":" + outcomeJson(control.outcome(), latentBill) + ","
				+ "\"degradation\":" + format(control.degradation()) + ","
				+ "\"adverseFailure\":" + control.adverseFailure() + ","
				+ "\"administrativeBurdenAdded\":" + format(control.administrativeBurdenAdded())
				+ "}";
	}

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"portfolioKey\":\"" + trace.config().portfolio().key() + "\","
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"mixedFinalReason\":\"" + json(trace.mixed().finalReason()) + "\","
				+ "\"baselineObjectionWindows\":" + trace.baseline().signals().objectionWindows() + ","
				+ "\"mixedObjectionWindows\":" + trace.mixed().signals().objectionWindows() + ","
				+ "\"baselineCitizenReviews\":" + trace.baseline().signals().citizenReviews() + ","
				+ "\"mixedCitizenReviews\":" + trace.mixed().signals().citizenReviews() + ","
				+ "\"baselineHarmReview\":" + format(metric(trace.baseline(), "harmReviewTriggered")) + ","
				+ "\"mixedHarmReview\":" + format(metric(trace.mixed(), "harmReviewTriggered")) + ","
				+ "\"baselineAdministrativeCoverage\":" + format(metric(trace.baseline(), "administrativeReviewCoverage")) + ","
				+ "\"mixedAdministrativeCoverage\":" + format(metric(trace.mixed(), "administrativeReviewCoverage")) + ","
				+ "\"mixedOverflowFallback\":" + format(metric(trace.mixed(), "administrativeOverflowFallback")) + ","
				+ "\"baselineYayShare\":" + format(trace.baseline().averageYayShare()) + ","
				+ "\"mixedYayShare\":" + format(trace.mixed().averageYayShare())
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"mixedFailure\":" + trace.mixedFailure() + ","
				+ "\"anySameBudgetSingleFailure\":" + trace.anySameBudgetSingleFailure() + ","
					+ "\"mixedOnlySuccess\":" + trace.mixedOnlySuccess() + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"mixedEnacted\":" + trace.mixed().enacted() + ","
				+ "\"mixedDegradation\":" + format(trace.mixedDegradation()) + ","
				+ "\"strongestSameBudgetSingleDegradation\":" + format(trace.strongestSingleDegradation()) + ","
				+ "\"queueOverflowAdded\":" + format(trace.queueOverflowAdded())
				+ "}";
	}

	private static String interactionJson(TraceRow trace) {
		return "{"
				+ "\"strongestSameBudgetSingleAdversaryId\":\"" + trace.strongestSingle().action().adversaryId() + "\","
				+ "\"mixedDegradation\":" + format(trace.mixedDegradation()) + ","
				+ "\"strongestSameBudgetSingleDegradation\":" + format(trace.strongestSingleDegradation()) + ","
				+ "\"interactionDegradation\":" + format(trace.interactionDegradation()) + ","
				+ "\"mixedDominatesStrongestSingle\":" + trace.mixedDominatesStrongestSingle() + ","
				+ "\"allocatedComponentLossSum\":" + format(trace.componentLossSum()) + ","
				+ "\"superadditiveLoss\":" + format(trace.superadditiveLoss()) + ","
				+ "\"superadditive\":" + (trace.superadditiveLoss() > INTERACTION_EPSILON)
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline())) + ","
				+ "\"mixedBurden\":" + format(administrativeBurden(trace.mixed())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"strongestSingleAdministrativeBurdenAdded\":" + format(trace.strongestSingleAdministrativeBurdenAdded()) + ","
				+ "\"attackerResourceSpend\":" + format(trace.mixedPlan().totalUnits())
				+ "}";
	}

	private static String recoveryJson(TraceRow trace) {
		return "{"
				+ "\"correctionAttempted\":" + correctionAttempted(trace) + ","
				+ "\"recoveryCorrectionFailure\":" + recoveryCorrectionFailure(trace) + ","
				+ "\"overloadObserved\":" + trace.recovery().overloadObserved() + ","
				+ "\"capacityRecovered\":" + trace.recovery().capacityRecovered() + ","
				+ "\"recoveryCycles\":" + trace.recovery().recoveryCycles() + ","
				+ "\"backlogBeforeRecovery\":" + format(trace.recovery().backlogBeforeRecovery()) + ","
				+ "\"backlogAfterRecovery\":" + format(trace.recovery().backlogAfterRecovery()) + ","
				+ "\"remainingCapacityShare\":" + format(trace.recovery().remainingCapacityShare())
				+ "}";
	}

	private static void jsonProperty(StringBuilder builder, String key, String value, boolean quote) {
		builder.append('"').append(json(key)).append("\":");
		if (quote) {
			builder.append('"').append(json(value)).append('"');
		} else {
			builder.append(value);
		}
		builder.append(',');
	}

	private static void jsonArray(StringBuilder builder, String key, List<String> values) {
		builder.append('"').append(json(key)).append("\":[");
		builder.append(values.stream().map(value -> "\"" + json(value) + "\"").collect(Collectors.joining(",")));
		builder.append("],");
	}

	private static void jsonObject(StringBuilder builder, String key, String objectJson) {
		builder.append('"').append(json(key)).append("\":").append(objectJson).append(',');
	}

	private static void jsonObjectArray(
			StringBuilder builder,
			String key,
			List<ControlResult> controls,
			Bill latentBill
	) {
		builder.append('"').append(json(key)).append("\":[");
		builder.append(controls.stream()
		                       .map(control -> controlJson(control, latentBill))
		                       .collect(Collectors.joining(",")));
		builder.append("],");
	}

	private static void removeTrailingComma(StringBuilder builder) {
		if (!builder.isEmpty() && builder.charAt(builder.length() - 1) == ',') {
			builder.setLength(builder.length() - 1);
		}
	}

	private static void property(StringBuilder builder, int tabs, String key, String value, boolean quote, boolean comma) {
		builder.append("\t".repeat(tabs)).append('"').append(json(key)).append("\": ");
		if (quote) {
			builder.append('"').append(json(value)).append('"');
		} else {
			builder.append(value);
		}
		if (comma) {
			builder.append(',');
		}
		builder.append('\n');
	}

	private static void property(StringBuilder builder, int tabs, String key, String value, boolean comma) {
		property(builder, tabs, key, value, true, comma);
	}

	private static void arrayProperty(StringBuilder builder, int tabs, String key, List<String> values, boolean comma) {
		builder.append("\t".repeat(tabs))
		       .append('"').append(json(key)).append("\": [")
		       .append(values.stream().map(value -> "\"" + json(value) + "\"").collect(Collectors.joining(", ")))
		       .append(']');
		if (comma) {
			builder.append(',');
		}
		builder.append('\n');
	}

	private static String csv(String value) {
		return "\"" + value.replace("\"", "\"\"") + "\"";
	}

	private static String json(String value) {
		return value.replace("\\", "\\\\").replace("\"", "\\\"");
	}

	private static String format(double value) {
		return String.format(Locale.ROOT, "%.6f", value);
	}

	private record PublicInputBlockProcess(String name) implements LegislativeProcess
	{
		@Override
		public BillOutcome consider(Bill bill, VoteContext context) {
			return BillOutcome.accessDenied(
					bill,
					context.currentPolicyPosition(),
					"blocked after citizen-panel certification failure"
			).withSignals(OutcomeSignals.diagnostic("publicInputGateBlock", 1.0));
		}
	}

	private record InstrumentedHarmReviewProcess(
			String name,
			LegislativeProcess innerProcess,
			double legalAttentionPerReview
	) implements LegislativeProcess
	{
		@Override
		public BillOutcome consider(Bill bill, VoteContext context) {
			boolean harmReviewTriggered = bill.concentratedHarm() >= 0.46;
			BillOutcome outcome = innerProcess.consider(bill, context);
			return outcome.withSignals(OutcomeSignals.diagnostics(Map.of(
					"harmReviewTriggered", harmReviewTriggered ? 1.0 : 0.0,
					"legalReviewBurden", harmReviewTriggered ? legalAttentionPerReview : 0.0
			)));
		}
	}
}
