package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
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
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;


public final class A7AdministrativeOverloadAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A7";
	private static final String CASE_KEY = "administrative-overload-coalition";
	private static final String MECHANISM_FAMILY = "portfolio_hybrid_administrative_review_capacity";
	private static final String BASELINE_SCENARIO = "portfolio-hybrid-capacity-baseline";
	private static final String ATTACK_SCENARIO = "portfolio-hybrid-a7-administrative-overload";
	private static final String BUDGET_UNIT = "coalition_demand_units";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a7.jsonl";
	private static final double CAPACITY_UNITS = 18.0;
	private static final double RECOVERY_UNITS_PER_CYCLE = 3.60;
	private static final double MINIMUM_DEFENDED_COVERAGE = 0.72;
	private static final int MAX_RECOVERY_CYCLES = 240;
	private static final String CLAIM_BOUNDARY =
			"A7 executable pilot only. Rows pair the same generated worlds and target bill ids under a "
			+ "portfolio-hybrid safeguard path with a shared synthetic review-capacity budget. The attack "
			+ "injects fixed-budget proposal, objection, harm-claim, panel-noise, camouflage, and review "
			+ "demand before each target; overflow uses an explicitly traced ordinary-majority fallback. "
			+ "Capacity, backlog, and recovery-cycle values are modeling assumptions, not empirical agency "
			+ "or congressional staffing estimates, not a full A1-A9 sweep, and not evidence for real-world "
			+ "institutional ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		double informationMultiplier() {
			return informationLevel == InformationLevel.HIGH ? 1.18 : 1.0;
		}

		double proposalDemand() {
			return budgetValue * 0.42 * informationMultiplier();
		}

		double objectionDemand() {
			return budgetValue * 0.32 * informationMultiplier();
		}

		double harmClaimDemand() {
			return budgetValue * 0.28 * informationMultiplier();
		}

		double panelNoiseDemand() {
			return budgetValue * 0.24 * informationMultiplier();
		}

		double camouflageDemand() {
			return budgetValue * 0.18 * informationMultiplier();
		}

		double externalDemand() {
			return proposalDemand()
					+ objectionDemand()
					+ harmClaimDemand()
					+ panelNoiseDemand()
					+ camouflageDemand();
		}

		double attackIntensity() {
			return Values.clamp((budgetValue / 6.0) * informationMultiplier(), 0.0, 1.0);
		}
	}

	private record RecoveryResult(
			boolean overloadObserved,
			boolean recovered,
			int recoveryCycles,
			double backlogBeforeRecovery,
			double backlogAfterRecovery,
			double remainingCapacityShare
	) {
		String status() {
			if (!overloadObserved) {
				return "not_needed";
			}
			return recovered ? "recovered_after_attack_window" : "residual_overload_after_recovery_window";
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill latentBill,
			Bill attackedInputBill,
			BillOutcome baseline,
			BillOutcome attacked,
			CapacitySnapshot baselineCapacity,
			CapacitySnapshot attackedCapacity,
			double latentRisk,
			double queueOverflowAdded,
			double reviewCoverageLoss,
			double administrativeBurdenAdded,
			double riskControlDegradationAdded,
			boolean capacitySaturated,
			boolean overflowFallback,
			boolean riskControlFailureAdded,
			boolean highBenefitBlockAdded,
			boolean success,
			RecoveryResult recovery
	) {
		TraceRow withRecovery(RecoveryResult result) {
			return new TraceRow(
					runIndex,
					worldSeed,
					billIndex,
					config,
					latentBill,
					attackedInputBill,
					baseline,
					attacked,
					baselineCapacity,
					attackedCapacity,
					latentRisk,
					queueOverflowAdded,
					reviewCoverageLoss,
					administrativeBurdenAdded,
					riskControlDegradationAdded,
					capacitySaturated,
					overflowFallback,
					riskControlFailureAdded,
					highBenefitBlockAdded,
					success,
					result
			);
		}
	}

	private A7AdministrativeOverloadAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a7.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a7-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a7-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a7-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a7.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a7-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a7-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a7-run-manifest.json"));
	}

	public static void runSummaryOnly(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a7-summary.csv"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a7-summary.csv"));
	}

	private static void validateRunParameters(int runs, int legislators, int bills) {
		if (runs <= 0 || legislators <= 0 || bills <= 0) {
			throw new IllegalArgumentException("Runs, legislators, and bills must all be positive.");
		}
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = overloadWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 6707);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : attackConfigs()) {
				AdministrativeReviewCapacityProcess baselineProcess = capacityProcess(
						world,
						"A7 portfolio capacity baseline"
				);
				AdministrativeReviewCapacityProcess attackedProcess = capacityProcess(
						world,
						"A7 overloaded portfolio capacity"
				);
				List<TraceRow> configTraces = new ArrayList<>();
				for (int billIndex = 0; billIndex < world.bills().size(); billIndex++) {
					Bill latentBill = world.bills().get(billIndex);
					Bill attackedInput = attackedBill(latentBill, config);
					long voteSeed = mix(seed, run, 7707 + (config.budgetValue() * 29) + billIndex);
					BillOutcome baseline = baselineProcess.consider(
							latentBill,
							new VoteContext(world.partyPositions(), new Random(voteSeed), 0.0)
					);
					attackedProcess.submitExternalDemand(config.externalDemand());
					BillOutcome attacked = attackedProcess.consider(
							attackedInput,
							new VoteContext(world.partyPositions(), new Random(voteSeed), 0.0)
					);
					configTraces.add(trace(
							run,
							worldSeed,
							billIndex,
							config,
							latentBill,
							attackedInput,
							baseline,
							attacked,
							baselineProcess.snapshot(),
							attackedProcess.snapshot()
					));
				}
				RecoveryResult recovery = recover(attackedProcess);
				for (TraceRow trace : configTraces) {
					traces.add(trace.withRecovery(recovery));
				}
			}
		}
		return traces;
	}

	private static WorldSpec overloadWorldSpec(int legislators, int bills) {
		return new WorldSpec(
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
	}

	private static AdministrativeReviewCapacityProcess capacityProcess(SimulationWorld world, String name) {
		Scenario portfolio = ScenarioCatalog.scenariosForKeys(List.of("portfolio-hybrid-legislature")).getFirst();
		LegislativeProcess defended = portfolio.buildProcess(world);
		Chamber ordinaryChamber = new Chamber(
				name + " overflow chamber",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		LegislativeProcess overflow = new UnicameralProcess(name + " ordinary-majority overflow", ordinaryChamber);
		return new AdministrativeReviewCapacityProcess(
				name,
				defended,
				overflow,
				CAPACITY_UNITS,
				RECOVERY_UNITS_PER_CYCLE,
				MINIMUM_DEFENDED_COVERAGE
		);
	}

	private static Bill attackedBill(Bill bill, AttackConfig config) {
		double intensity = config.attackIntensity();
		double supportBoost = (0.035 + (0.075 * intensity))
				* (config.informationLevel() == InformationLevel.HIGH ? 1.10 : 1.0);
		double revisedSupport = Values.clamp(bill.publicSupport() + supportBoost, 0.0, 1.0);
		double revisedSalience = Values.clamp(bill.salience() + 0.06 + (0.10 * intensity), 0.0, 1.0);
		Bill attacked = bill.withPublicSignal(revisedSupport, revisedSalience);

		double revisedHarm = Values.clamp(bill.concentratedHarm() * (1.0 - (0.28 * intensity)), 0.0, 1.0);
		double revisedAffectedSupport = Values.clamp(
				bill.affectedGroupSupport() + 0.04 + (0.18 * intensity),
				0.0,
				1.0
		);
		attacked = attacked.withAffectedGroup(
				bill.affectedGroup(),
				revisedAffectedSupport,
				revisedHarm,
				bill.compensationCost()
		);

		double revisedLobbyPressure = Values.clamp(
				bill.lobbyPressure() * (1.0 - (0.36 * intensity)),
				-1.0,
				1.0
		);
		double revisedPrivateGain = Values.clamp(
				bill.privateGain() * (1.0 - (0.30 * intensity)),
				0.0,
				1.0
		);
		double spend = 0.70 * config.budgetValue() * config.informationMultiplier();
		attacked = attacked.withLobbyActivity(
				revisedLobbyPressure,
				attacked.publicSupport(),
				attacked.publicBenefit(),
				revisedPrivateGain,
				spend,
				0.0,
				spend * 0.12,
				spend * 0.22,
				spend * 0.18,
				spend * 0.34,
				spend * 0.14
		);
		attacked = attacked.withPublicBenefitUncertainty(
				Values.clamp(bill.publicBenefitUncertainty() + (0.10 * intensity), 0.0, 1.0)
		);
		return attacked.withAttentionSpend(config.externalDemand());
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill latentBill,
			Bill attackedInput,
			BillOutcome baseline,
			BillOutcome attacked,
			CapacitySnapshot baselineCapacity,
			CapacitySnapshot attackedCapacity
	) {
		double latentRisk = latentRisk(latentBill);
		double queueOverflowAdded = Math.max(
				0.0,
				metric(attacked, "administrativeQueueOverflow")
						- metric(baseline, "administrativeQueueOverflow")
		);
		double reviewCoverageLoss = Math.max(
				0.0,
				metric(baseline, "administrativeReviewCoverage")
						- metric(attacked, "administrativeReviewCoverage")
		);
		double administrativeBurdenAdded = Math.max(
				0.0,
				administrativeBurden(attacked) - administrativeBurden(baseline)
		);
		boolean capacitySaturated = metric(attacked, "administrativeCapacitySaturated") >= 0.50;
		boolean overflowFallback = metric(attacked, "administrativeOverflowFallback") >= 0.50;
		boolean latentHighRisk = latentRisk >= 0.48
				|| latentBill.publicBenefit() < 0.42
				|| AffectedGroupScoring.minorityHarm(latentBill) >= 0.22;
		boolean riskControlFailureAdded = latentHighRisk && !baseline.enacted() && attacked.enacted();
		boolean highBenefitBlockAdded = latentBill.publicBenefit() >= 0.66
				&& baseline.enacted()
				&& !attacked.enacted();
		double riskControlDegradationAdded = Math.max(
				0.0,
				adverseOutcomeScore(attacked, latentBill) - adverseOutcomeScore(baseline, latentBill)
		);
		boolean success = capacitySaturated || overflowFallback;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				latentBill,
				attackedInput,
				baseline,
				attacked,
				baselineCapacity,
				attackedCapacity,
				latentRisk,
				queueOverflowAdded,
				reviewCoverageLoss,
				administrativeBurdenAdded,
				riskControlDegradationAdded,
				capacitySaturated,
				overflowFallback,
				riskControlFailureAdded,
				highBenefitBlockAdded,
				success,
				null
		);
	}

	private static RecoveryResult recover(AdministrativeReviewCapacityProcess process) {
		CapacitySnapshot before = process.snapshot();
		int cycles = 0;
		CapacitySnapshot after = before;
		while (!after.fullReviewReady() && cycles < MAX_RECOVERY_CYCLES) {
			after = process.advanceRecoveryCycle();
			cycles++;
		}
		return new RecoveryResult(
				before.everOverloaded(),
				after.fullReviewReady(),
				cycles,
				before.backlogUnits(),
				after.backlogUnits(),
				after.remainingCapacityShare()
		);
	}

	private static double latentRisk(Bill bill) {
		return Values.clamp(
				(0.32 * (1.0 - bill.publicBenefit()))
						+ (0.24 * AffectedGroupScoring.minorityHarm(bill))
						+ (0.22 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.12 * bill.publicBenefitUncertainty())
						+ (0.10 * (1.0 - bill.publicSupport())),
				0.0,
				1.0
		);
	}

	private static double adverseOutcomeScore(BillOutcome outcome, Bill latentBill) {
		if (outcome.enacted()) {
			return latentRisk(latentBill);
		}
		return Math.max(0.0, latentBill.publicBenefit() - 0.60) * 0.65;
	}

	private static double administrativeBurden(BillOutcome outcome) {
		return metric(outcome, "administrativeReviewDemand")
				+ metric(outcome, "administrativeExternalDemand")
				+ (0.10 * metric(outcome, "administrativeQueueOverflow"))
				+ (0.40 * metric(outcome, "administrativeOverflowFallback"))
				+ (0.14 * outcome.signals().objectionWindows())
				+ (0.18 * outcome.signals().citizenReviews())
				+ (0.10 * outcome.signals().lawReviews())
				+ (0.08 * outcome.signals().proposalBondReviews());
	}

	private static double metric(BillOutcome outcome, String key) {
		return outcome.signals().supplementalMetrics().getOrDefault(key, 0.0);
	}

	private static List<AttackConfig> attackConfigs() {
		List<AttackConfig> configs = new ArrayList<>();
		for (InformationLevel level : List.of(InformationLevel.MEDIUM, InformationLevel.HIGH)) {
			for (int budget : List.of(1, 3, 6)) {
				configs.add(new AttackConfig(budget, level));
			}
		}
		return configs;
	}

	private static long mix(long seed, int run, int stream) {
		long value = seed;
		value ^= 0x9E3779B97F4A7C15L + ((long) run << 6) + ((long) run >> 2);
		value ^= 0xBF58476D1CE4E5B9L * (stream + 31L);
		return value;
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
		jsonProperty(builder, "scenarioKey", ATTACK_SCENARIO, true);
		jsonProperty(builder, "baselineScenarioKey", BASELINE_SCENARIO, true);
		jsonProperty(builder, "mechanismFamily", MECHANISM_FAMILY, true);
		jsonProperty(builder, "adversaryId", ADVERSARY_ID, true);
		jsonProperty(builder, "actorType", spec.actorType(), true);
		jsonProperty(builder, "objective", spec.objective(), true);
		jsonProperty(builder, "budgetUnit", BUDGET_UNIT, true);
		jsonProperty(builder, "budgetValue", Integer.toString(trace.config().budgetValue()), false);
		jsonProperty(builder, "informationLevel", trace.config().informationLevel().key(), true);
		jsonArray(builder, "attackActionList", actionList(trace.config()));
		jsonObject(builder, "preAttackFeatures", billJson(trace.latentBill()));
		jsonObject(builder, "postAttackFeatures", billJson(trace.attackedInputBill()));
		jsonObject(builder, "institutionalPath", pathJson(trace));
		jsonObject(builder, "baselineOutcome", outcomeJson(trace.baseline()));
		jsonObject(builder, "attackedOutcome", outcomeJson(trace.attacked()));
		jsonProperty(builder, "successFlag", Boolean.toString(trace.success()), false);
		jsonObject(builder, "metricDeltas", metricDeltaJson(trace));
		jsonObject(builder, "administrativeBurden", administrativeBurdenJson(trace));
		jsonProperty(builder, "recoveryStatus", trace.recovery().status(), true);
		jsonObject(builder, "recoveryMetrics", recoveryJson(trace.recovery()));
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessCount,attackSuccessRate,capacitySaturationRate,overflowFallbackRate,meanQueueOverflowAdded,medianQueueOverflowAdded,worstQueueOverflowAdded,meanReviewCoverageLoss,riskControlFailureAddedRate,highBenefitBlockAddedRate,meanRiskControlDegradationAdded,medianRiskControlDegradationAdded,worstRiskControlDegradationAdded,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryRate,meanRecoveryCycles,worstRecoveryCycles,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("administrative_overload_coalition")).append(',')
			       .append(csv(CASE_KEY)).append(',')
			       .append(csv(BASELINE_SCENARIO)).append(',')
			       .append(csv(ATTACK_SCENARIO)).append(',')
			       .append(csv(MECHANISM_FAMILY)).append(',')
			       .append(csv(BUDGET_UNIT)).append(',')
			       .append(config.budgetValue()).append(',')
			       .append(csv(config.informationLevel().key())).append(',')
			       .append(runs).append(',')
			       .append(legislators).append(',')
			       .append(bills).append(',')
			       .append(group.size()).append(',')
			       .append(group.stream().filter(TraceRow::success).count()).append(',')
			       .append(format(rate(group, TraceRow::success))).append(',')
			       .append(format(rate(group, TraceRow::capacitySaturated))).append(',')
			       .append(format(rate(group, TraceRow::overflowFallback))).append(',')
			       .append(format(mean(group, TraceRow::queueOverflowAdded))).append(',')
			       .append(format(median(group, TraceRow::queueOverflowAdded))).append(',')
			       .append(format(max(group, TraceRow::queueOverflowAdded))).append(',')
			       .append(format(mean(group, TraceRow::reviewCoverageLoss))).append(',')
			       .append(format(rate(group, TraceRow::riskControlFailureAdded))).append(',')
			       .append(format(rate(group, TraceRow::highBenefitBlockAdded))).append(',')
			       .append(format(mean(group, TraceRow::riskControlDegradationAdded))).append(',')
			       .append(format(median(group, TraceRow::riskControlDegradationAdded))).append(',')
			       .append(format(max(group, TraceRow::riskControlDegradationAdded))).append(',')
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(format(max(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(format(recoveryRate(group))).append(',')
			       .append(format(mean(group, trace -> trace.recovery().recoveryCycles()))).append(',')
			       .append(format(max(group, trace -> trace.recovery().recoveryCycles()))).append(',')
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
		builder.append("# A7 Administrative-Overload Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a7_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A7 administrative overload coalition\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Capacity / recovery units per cycle: ").append(format(CAPACITY_UNITS))
		       .append(" / ").append(format(RECOVERY_UNITS_PER_CYCLE)).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metric: no-case cycles until queue clearance and defended-path readiness, capped at ")
		       .append(MAX_RECOVERY_CYCLES).append(" cycles\n\n");
		builder.append("| Information | Budget | Trace rows | Success | Saturation | Overflow fallback | Median queue added | Worst queue added | Risk-control failure added | Median risk degradation | Mean admin burden added | Recovery rate | Mean recovery cycles |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(rate(group, TraceRow::capacitySaturated))).append(" | ")
			       .append(format(rate(group, TraceRow::overflowFallback))).append(" | ")
			       .append(format(median(group, TraceRow::queueOverflowAdded))).append(" | ")
			       .append(format(max(group, TraceRow::queueOverflowAdded))).append(" | ")
			       .append(format(rate(group, TraceRow::riskControlFailureAdded))).append(" | ")
			       .append(format(median(group, TraceRow::riskControlDegradationAdded))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" | ")
			       .append(format(recoveryRate(group))).append(" | ")
			       .append(format(mean(group, trace -> trace.recovery().recoveryCycles()))).append(" |\n");
		}
		builder.append("\nGate status: this supplies the first bounded A7 capacity-saturation and recovery pilot, but the robustness breakout remains below manuscript gate because broader mechanism coverage, multi-seed sensitivity, substantive correction, and external validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a7-run-v0", true);
		property(builder, 1, "status", "partial_a7_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		property(builder, 1, "capacityUnits", format(CAPACITY_UNITS), false, true);
		property(builder, 1, "recoveryUnitsPerCycle", format(RECOVERY_UNITS_PER_CYCLE), false, true);
		property(builder, 1, "maximumRecoveryCycles", Integer.toString(MAX_RECOVERY_CYCLES), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a7-summary.csv",
				"reports/adversarial-stress-a7-summary.md",
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
		int mid = values.size() / 2;
		if (values.size() % 2 == 1) {
			return values.get(mid);
		}
		return (values.get(mid - 1) + values.get(mid)) / 2.0;
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
		boolean anyOverload = rows.stream().anyMatch(trace -> trace.recovery().overloadObserved());
		if (!anyOverload) {
			return "not_needed";
		}
		return rows.stream().allMatch(trace -> trace.recovery().recovered())
				? "recovered_after_attack_window"
				: "residual_overload_after_recovery_window";
	}

	private static double recoveryRate(List<TraceRow> rows) {
		List<TraceRow> eligible = rows.stream()
				.filter(trace -> trace.recovery().overloadObserved())
				.toList();
		return rate(eligible, trace -> trace.recovery().recovered());
	}

	private static List<String> actionList(AttackConfig config) {
		List<String> actions = new ArrayList<>(List.of(
				"submit_proposal_flood",
				"file_repetitive_objections",
				"file_bad_faith_harm_claims",
				"increase_panel_noise",
				"camouflage_target_lobbying",
				"consume_shared_review_capacity"
		));
		if (config.informationLevel() == InformationLevel.HIGH) {
			actions.add("target_high_risk_review_queue");
		}
		return actions;
	}

	private static String billJson(Bill bill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"publicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"salience\":" + format(bill.salience()) + ","
				+ "\"lobbyPressure\":" + format(bill.lobbyPressure()) + ","
				+ "\"privateGain\":" + format(bill.privateGain()) + ","
				+ "\"concentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"affectedGroupSupport\":" + format(bill.affectedGroupSupport()) + ","
				+ "\"publicBenefitUncertainty\":" + format(bill.publicBenefitUncertainty()) + ","
				+ "\"publicCampaignSpend\":" + format(bill.publicCampaignSpend()) + ","
				+ "\"attentionSpend\":" + format(bill.attentionSpend())
				+ "}";
	}

	private static String outcomeJson(BillOutcome outcome) {
		return "{"
				+ "\"enacted\":" + outcome.enacted() + ","
				+ "\"finalReason\":\"" + json(outcome.finalReason()) + "\","
				+ "\"agendaDisposition\":\"" + outcome.agendaDisposition() + "\","
				+ "\"statusQuoBefore\":" + format(outcome.statusQuoBefore()) + ","
				+ "\"statusQuoAfter\":" + format(outcome.statusQuoAfter()) + ","
				+ "\"selectedBill\":" + billJson(outcome.bill())
				+ "}";
	}

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(trace.attacked().finalReason()) + "\","
				+ "\"baselineReviewCoverage\":" + format(metric(trace.baseline(), "administrativeReviewCoverage")) + ","
				+ "\"attackedReviewCoverage\":" + format(metric(trace.attacked(), "administrativeReviewCoverage")) + ","
				+ "\"baselineQueueOverflow\":" + format(metric(trace.baseline(), "administrativeQueueOverflow")) + ","
				+ "\"attackedQueueOverflow\":" + format(metric(trace.attacked(), "administrativeQueueOverflow")) + ","
				+ "\"baselineCapacityRemainingShare\":" + format(trace.baselineCapacity().remainingCapacityShare()) + ","
				+ "\"attackedCapacityRemainingShare\":" + format(trace.attackedCapacity().remainingCapacityShare()) + ","
				+ "\"capacitySaturated\":" + trace.capacitySaturated() + ","
				+ "\"overflowFallback\":" + trace.overflowFallback() + ","
				+ "\"baselineFastRoutes\":" + trace.baseline().signals().fastLaneRoutes() + ","
				+ "\"baselineMiddleRoutes\":" + trace.baseline().signals().middleLaneRoutes() + ","
				+ "\"baselineHighRiskRoutes\":" + trace.baseline().signals().highRiskRoutes() + ","
				+ "\"attackedFastRoutes\":" + trace.attacked().signals().fastLaneRoutes() + ","
				+ "\"attackedMiddleRoutes\":" + trace.attacked().signals().middleLaneRoutes() + ","
				+ "\"attackedHighRiskRoutes\":" + trace.attacked().signals().highRiskRoutes()
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"latentRisk\":" + format(trace.latentRisk()) + ","
				+ "\"queueOverflowAdded\":" + format(trace.queueOverflowAdded()) + ","
				+ "\"reviewCoverageLoss\":" + format(trace.reviewCoverageLoss()) + ","
				+ "\"riskControlDegradationAdded\":" + format(trace.riskControlDegradationAdded()) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"capacitySaturated\":" + trace.capacitySaturated() + ","
				+ "\"overflowFallback\":" + trace.overflowFallback() + ","
				+ "\"riskControlFailureAdded\":" + trace.riskControlFailureAdded() + ","
				+ "\"highBenefitBlockAdded\":" + trace.highBenefitBlockAdded() + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"budgetedExternalDemand\":" + format(trace.config().externalDemand()) + ","
				+ "\"proposalDemand\":" + format(trace.config().proposalDemand()) + ","
				+ "\"objectionDemand\":" + format(trace.config().objectionDemand()) + ","
				+ "\"harmClaimDemand\":" + format(trace.config().harmClaimDemand()) + ","
				+ "\"panelNoiseDemand\":" + format(trace.config().panelNoiseDemand()) + ","
				+ "\"camouflageDemand\":" + format(trace.config().camouflageDemand()) + ","
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline())) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attacked())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"attackedQueueOverflow\":" + format(metric(trace.attacked(), "administrativeQueueOverflow"))
				+ "}";
	}

	private static String recoveryJson(RecoveryResult recovery) {
		return "{"
				+ "\"overloadObserved\":" + recovery.overloadObserved() + ","
				+ "\"recovered\":" + recovery.recovered() + ","
				+ "\"recoveryCycles\":" + recovery.recoveryCycles() + ","
				+ "\"backlogBeforeRecovery\":" + format(recovery.backlogBeforeRecovery()) + ","
				+ "\"backlogAfterRecovery\":" + format(recovery.backlogAfterRecovery()) + ","
				+ "\"remainingCapacityShare\":" + format(recovery.remainingCapacityShare())
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
		return String.format(java.util.Locale.ROOT, "%.6f", value);
	}
}
