package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.agenda.AgendaDisposition;
import congresssim.institution.agenda.AgendaLotteryProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.model.Bill;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.ProposalShockProfile;
import congresssim.simulation.WorldGenerator;
import congresssim.simulation.WorldSpec;
import congresssim.util.Values;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;


public final class A5ProposalFloodingAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A5";
	private static final String CASE_KEY = "proposal-flooding-pressure";
	private static final String MECHANISM_FAMILY = "fixed_capacity_agenda_lottery_majority";
	private static final String BASELINE_SCENARIO = "agenda-lottery-benign-majority";
	private static final String ATTACK_SCENARIO = "agenda-lottery-a5-proposal-flood";
	private static final String BUDGET_UNIT = "proposal_slots";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a5.jsonl";
	private static final double BASELINE_SLOT_SHARE = 0.46;
	private static final String CLAIM_BOUNDARY =
			"A5 executable pilot only. Rows use same generated worlds and original bill ids for a fixed-capacity "
			+ "agenda-lottery majority baseline and an attacked agenda pool with synthetic flood proposals. "
			+ "This is not an empirical bill-volume, agenda-control, or lobbying-support estimate, not a full "
			+ "A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		int floodProposalCount(int baseBills) {
			return Math.max(1, (baseBills * budgetValue) / 3);
		}

		double processingCostPerProposal() {
			return informationLevel == InformationLevel.MEDIUM ? 0.010 : 0.008;
		}

		double floorSlotCost() {
			return informationLevel == InformationLevel.MEDIUM ? 0.055 : 0.040;
		}

		double lobbySupport() {
			return informationLevel == InformationLevel.MEDIUM ? 0.58 : 0.18;
		}
	}

	private record BatchResult(
			Map<String, BillOutcome> originalOutcomes,
			List<BillOutcome> floodOutcomes,
			BatchDiagnostics diagnostics
	) {}

	private record BatchDiagnostics(
			int proposalPoolSize,
			int agendaSlots,
			int originalFloorConsidered,
			int floodFloorConsidered,
			int originalEnacted,
			int floodEnacted,
			int lowSupportFloodEnacted,
			double originalPolicyYield,
			double floodPolicyYield,
			double proposalProcessingBurden
	) {}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			BillOutcome baseline,
			BillOutcome attacked,
			BatchDiagnostics baselineDiagnostics,
			BatchDiagnostics attackedDiagnostics,
			double considerationDecline,
			double highBenefitCrowdout,
			double highBenefitBlockageLoss,
			double lowSupportFloodEnactedPerRun,
			double policyYieldLoss,
			double administrativeBurdenAdded,
			boolean success
	) {}

	private A5ProposalFloodingAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a5.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a5-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a5-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a5-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a5.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a5-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a5-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a5-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = proposalFloodWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 5705);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			List<Bill> originalBills = world.bills();
			int agendaSlots = agendaSlots(originalBills.size());
			for (AttackConfig config : attackConfigs()) {
				List<Bill> floodBills = floodBills(originalBills, config, run, seed);
				List<Bill> attackedPool = new ArrayList<>(originalBills);
				attackedPool.addAll(floodBills);
				BatchResult baseline = runBatch(
						world,
						originalBills,
						originalBills,
						agendaSlots,
						new Random(mix(seed, run, 6105 + config.budgetValue())),
						0.0,
						"A5 benign fixed-capacity agenda lottery"
				);
				BatchResult attacked = runBatch(
						world,
						attackedPool,
						interleavedSchedule(originalBills, floodBills),
						agendaSlots,
						new Random(mix(seed, run, 6105 + config.budgetValue())),
						config.processingCostPerProposal() * floodBills.size(),
						"A5 attacked fixed-capacity agenda lottery"
				);
				for (int billIndex = 0; billIndex < originalBills.size(); billIndex++) {
					Bill bill = originalBills.get(billIndex);
					BillOutcome baselineOutcome = baseline.originalOutcomes().get(bill.id());
					BillOutcome attackedOutcome = attacked.originalOutcomes().get(bill.id());
					traces.add(trace(
							run,
							worldSeed,
							billIndex,
							config,
							bill,
							baselineOutcome,
							attackedOutcome,
							baseline.diagnostics(),
							attacked.diagnostics()
					));
				}
			}
		}
		return traces;
	}

	private static WorldSpec proposalFloodWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.66,
				0.68,
				0.58,
				0.58,
				0.42,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.HIGH_BENEFIT_EXTREME_REFORM
		);
	}

	private static BatchResult runBatch(
			SimulationWorld world,
			List<Bill> agendaPool,
			List<Bill> schedule,
			int agendaSlots,
			Random random,
			double proposalProcessingBurden,
			String name
	) {
		LegislativeProcess process = process(world, agendaPool, agendaSlots, name);
		PolicyState policy = world.initialPolicy();
		Map<String, BillOutcome> originalOutcomes = new HashMap<>();
		List<BillOutcome> floodOutcomes = new ArrayList<>();
		for (Bill bill : schedule) {
			BillOutcome outcome = process.consider(
					bill,
					new VoteContext(world.partyPositions(), random, policy.position())
			);
			if (isFloodBill(bill)) {
				floodOutcomes.add(outcome);
			} else {
				originalOutcomes.put(bill.id(), outcome);
			}
			policy = new PolicyState(outcome.statusQuoAfter());
		}
		return new BatchResult(
				Map.copyOf(originalOutcomes),
				List.copyOf(floodOutcomes),
				diagnostics(agendaPool.size(), agendaSlots, originalOutcomes.values().stream().toList(), floodOutcomes, proposalProcessingBurden)
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			List<Bill> agendaPool,
			int agendaSlots,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		double slotShare = Math.min(1.0, Math.max(0.0, (double) agendaSlots / agendaPool.size()));
		return new AgendaLotteryProcess(
				name,
				new UnicameralProcess(name + " floor", chamber),
				agendaPool,
				slotShare,
				true
		);
	}

	private static BatchDiagnostics diagnostics(
			int proposalPoolSize,
			int agendaSlots,
			List<BillOutcome> originalOutcomes,
			List<BillOutcome> floodOutcomes,
			double proposalProcessingBurden
	) {
		int originalFloor = count(originalOutcomes, A5ProposalFloodingAdversarialStressRunner::floorConsidered);
		int floodFloor = count(floodOutcomes, A5ProposalFloodingAdversarialStressRunner::floorConsidered);
		int originalEnacted = count(originalOutcomes, BillOutcome::enacted);
		int floodEnacted = count(floodOutcomes, BillOutcome::enacted);
		int lowSupportFloodEnacted = count(
				floodOutcomes,
				outcome -> outcome.enacted() && outcome.bill().publicSupport() < 0.50
		);
		return new BatchDiagnostics(
				proposalPoolSize,
				agendaSlots,
				originalFloor,
				floodFloor,
				originalEnacted,
				floodEnacted,
				lowSupportFloodEnacted,
				policyYield(originalOutcomes),
				policyYield(floodOutcomes),
				proposalProcessingBurden
		);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			BillOutcome baseline,
			BillOutcome attacked,
			BatchDiagnostics baselineDiagnostics,
			BatchDiagnostics attackedDiagnostics
	) {
		double considerationDecline = (floorConsidered(baseline) ? 1.0 : 0.0)
				- (floorConsidered(attacked) ? 1.0 : 0.0);
		boolean highBenefit = originalBill.publicBenefit() >= 0.55;
		double highBenefitCrowdout = highBenefit && considerationDecline > 0.0 ? 1.0 : 0.0;
		double highBenefitBlockageLoss = highBenefit && baseline.enacted() && !attacked.enacted()
				? originalBill.publicBenefit()
				: 0.0;
		double lowSupportFloodEnactedPerRun = attackedDiagnostics.lowSupportFloodEnacted();
		double policyYieldLoss = (baseline.enacted() ? originalBill.publicBenefit() : 0.0)
				- (attacked.enacted() ? originalBill.publicBenefit() : 0.0);
		double administrativeBurdenAdded = administrativeBurden(attackedDiagnostics, config)
				- administrativeBurden(baselineDiagnostics, config);
		boolean success = highBenefitCrowdout > 0.0
				|| highBenefitBlockageLoss > 0.0
				|| lowSupportFloodEnactedPerRun > 0.0
				|| floodFloorSlotShare(attackedDiagnostics) >= 0.10
				|| administrativeBurdenAdded > 0.200;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				originalBill,
				baseline,
				attacked,
				baselineDiagnostics,
				attackedDiagnostics,
				considerationDecline,
				highBenefitCrowdout,
				highBenefitBlockageLoss,
				lowSupportFloodEnactedPerRun,
				policyYieldLoss,
				administrativeBurdenAdded,
				success
		);
	}

	private static List<AttackConfig> attackConfigs() {
		List<AttackConfig> configs = new ArrayList<>();
		for (InformationLevel level : List.of(InformationLevel.LOW, InformationLevel.MEDIUM)) {
			for (int budget : List.of(1, 3, 6)) {
				configs.add(new AttackConfig(budget, level));
			}
		}
		return configs;
	}

	private static int agendaSlots(int baseBills) {
		return Math.clamp((int) Math.round(baseBills * BASELINE_SLOT_SHARE), 1, baseBills);
	}

	private static List<Bill> interleavedSchedule(List<Bill> originalBills, List<Bill> floodBills) {
		List<Bill> schedule = new ArrayList<>();
		int floodCursor = 0;
		int floodPerOriginal = Math.max(1, (int) Math.ceil((double) floodBills.size() / originalBills.size()));
		for (Bill originalBill : originalBills) {
			for (int i = 0; i < floodPerOriginal && floodCursor < floodBills.size(); i++) {
				schedule.add(floodBills.get(floodCursor));
				floodCursor++;
			}
			schedule.add(originalBill);
		}
		while (floodCursor < floodBills.size()) {
			schedule.add(floodBills.get(floodCursor));
			floodCursor++;
		}
		return schedule;
	}

	private static List<Bill> floodBills(List<Bill> originalBills, AttackConfig config, int runIndex, long seed) {
		int count = config.floodProposalCount(originalBills.size());
		List<Bill> bills = new ArrayList<>();
		Random random = new Random(mix(seed, runIndex, 6505 + (config.budgetValue() * 13) + config.informationLevel().ordinal()));
		for (int i = 0; i < count; i++) {
			Bill anchor = originalBills.get(i % originalBills.size());
			bills.add(floodBill(anchor, config, random, i));
		}
		return bills;
	}

	private static Bill floodBill(Bill anchor, AttackConfig config, Random random, int index) {
		double direction = Math.signum(anchor.proposerIdeology() == 0.0 ? random.nextGaussian() : anchor.proposerIdeology());
		if (direction == 0.0) {
			direction = random.nextBoolean() ? 1.0 : -1.0;
		}
		double ideology = Values.clamp((0.30 * anchor.ideologyPosition()) + (0.18 * direction) + random.nextGaussian() * 0.10, -1.0, 1.0);
		double support = config.informationLevel() == InformationLevel.MEDIUM
				? Values.clamp(0.430 + random.nextGaussian() * 0.045, 0.20, 0.49)
				: Values.clamp(0.360 + random.nextGaussian() * 0.090, 0.05, 0.55);
		double benefit = config.informationLevel() == InformationLevel.MEDIUM
				? Values.clamp(0.300 + random.nextGaussian() * 0.090, 0.05, 0.52)
				: Values.clamp(0.240 + random.nextGaussian() * 0.110, 0.02, 0.55);
		double lobbyPressure = Values.clamp(config.lobbySupport() + random.nextGaussian() * 0.16, -1.0, 1.0);
		double salience = config.informationLevel() == InformationLevel.MEDIUM
				? Values.clamp(0.720 + random.nextGaussian() * 0.080, 0.0, 1.0)
				: Values.clamp(0.640 + random.nextGaussian() * 0.140, 0.0, 1.0);
		double privateGain = config.informationLevel() == InformationLevel.MEDIUM
				? Values.clamp(0.640 + random.nextGaussian() * 0.100, 0.0, 1.0)
				: Values.clamp(0.380 + random.nextGaussian() * 0.160, 0.0, 1.0);
		double affectedSupport = Values.clamp(support - 0.08 + random.nextGaussian() * 0.080, 0.0, 1.0);
		double harm = config.informationLevel() == InformationLevel.MEDIUM
				? Values.clamp(0.300 + random.nextGaussian() * 0.110, 0.0, 1.0)
				: Values.clamp(0.260 + random.nextGaussian() * 0.150, 0.0, 1.0);
		double compensationCost = Values.clamp(harm * 0.28, 0.0, 1.0);
		Bill bill = new Bill(
				"F-A5-" + config.key() + "-" + (index + 1),
				"Flood Proposal " + (index + 1),
				anchor.proposerId(),
				anchor.proposerIdeology(),
				ideology,
				support,
				benefit,
				lobbyPressure,
				salience,
				privateGain,
				false,
				anchor.issueDomain(),
				0.0,
				0.0,
				anchor.affectedGroup(),
				affectedSupport,
				harm,
				compensationCost
		);
		return bill.withPublicBenefitUncertainty(Values.clamp(0.360 + random.nextGaussian() * 0.120, 0.0, 1.0))
		           .withAttentionSpend(config.processingCostPerProposal());
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
		jsonObject(builder, "preAttackFeatures", billJson(trace.originalBill()));
		jsonObject(builder, "postAttackFeatures", attackFeatureJson(trace));
		jsonObject(builder, "institutionalPath", pathJson(trace));
		jsonObject(builder, "baselineOutcome", outcomeJson(trace.baseline()));
		jsonObject(builder, "attackedOutcome", outcomeJson(trace.attacked()));
		jsonProperty(builder, "successFlag", Boolean.toString(trace.success()), false);
		jsonObject(builder, "metricDeltas", metricDeltaJson(trace));
		jsonObject(builder, "administrativeBurden", administrativeBurdenJson(trace));
		jsonProperty(builder, "recoveryStatus", "not_modeled", true);
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,meanConsiderationDecline,highBenefitCrowdoutRate,highBenefitBlockageRate,meanLowSupportFloodEnactedPerRun,meanPolicyYieldLoss,worstPolicyYieldLoss,meanFloodFloorSlots,meanFloodFloorSlotShare,meanProposalLoadAdded,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("proposal_flooding")).append(',')
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
			       .append(format(rate(group, TraceRow::success))).append(',')
			       .append(format(mean(group, TraceRow::considerationDecline))).append(',')
			       .append(format(rate(group, row -> row.highBenefitCrowdout() > 0.0))).append(',')
			       .append(format(rate(group, row -> row.highBenefitBlockageLoss() > 0.0))).append(',')
			       .append(format(mean(group, TraceRow::lowSupportFloodEnactedPerRun))).append(',')
			       .append(format(mean(group, TraceRow::policyYieldLoss))).append(',')
			       .append(format(max(group, TraceRow::policyYieldLoss))).append(',')
			       .append(format(mean(group, row -> row.attackedDiagnostics().floodFloorConsidered()))).append(',')
			       .append(format(mean(group, row -> floodFloorSlotShare(row.attackedDiagnostics())))).append(',')
			       .append(format(mean(group, row -> row.attackedDiagnostics().proposalPoolSize() - row.baselineDiagnostics().proposalPoolSize()))).append(',')
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(format(max(group, TraceRow::administrativeBurdenAdded))).append(',')
			       .append(csv("not_modeled")).append(',')
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
		builder.append("# A5 Proposal-Flooding Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a5_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A5 proposal flooder\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | High-benefit crowdout | High-benefit blockage | Low-support flood enacted/run | Flood floor slots | Flood slot share | Mean proposal load added | Mean admin burden added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(rate(group, row -> row.highBenefitCrowdout() > 0.0))).append(" | ")
			       .append(format(rate(group, row -> row.highBenefitBlockageLoss() > 0.0))).append(" | ")
			       .append(format(mean(group, TraceRow::lowSupportFloodEnactedPerRun))).append(" | ")
			       .append(format(mean(group, row -> row.attackedDiagnostics().floodFloorConsidered()))).append(" | ")
			       .append(format(mean(group, row -> floodFloorSlotShare(row.attackedDiagnostics())))).append(" | ")
			       .append(format(mean(group, row -> row.attackedDiagnostics().proposalPoolSize() - row.baselineDiagnostics().proposalPoolSize()))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A5 beyond aggregate proposal-flooding mapping, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader agenda and review mechanisms, multi-seed replication, and external agenda-load validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a5-run-v0", true);
		property(builder, 1, "status", "partial_a5_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a5-summary.csv",
				"reports/adversarial-stress-a5-summary.md",
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

	private static int count(Iterable<BillOutcome> outcomes, OutcomeFlag flag) {
		int count = 0;
		for (BillOutcome outcome : outcomes) {
			if (flag.value(outcome)) {
				count++;
			}
		}
		return count;
	}

	private static double policyYield(Iterable<BillOutcome> outcomes) {
		double value = 0.0;
		for (BillOutcome outcome : outcomes) {
			if (outcome.enacted()) {
				value += outcome.bill().publicBenefit();
			}
		}
		return value;
	}

	private static boolean floorConsidered(BillOutcome outcome) {
		return outcome.agendaDisposition() == AgendaDisposition.FLOOR_CONSIDERED;
	}

	private static boolean isFloodBill(Bill bill) {
		return bill.id().startsWith("F-A5-");
	}

	private static double floodFloorSlotShare(BatchDiagnostics diagnostics) {
		if (diagnostics.agendaSlots() == 0) {
			return 0.0;
		}
		return (double) diagnostics.floodFloorConsidered() / diagnostics.agendaSlots();
	}

	private static double administrativeBurden(BatchDiagnostics diagnostics, AttackConfig config) {
		return diagnostics.proposalProcessingBurden()
				+ (diagnostics.floodFloorConsidered() * config.floorSlotCost());
	}

	private static List<String> actionList(AttackConfig config) {
		List<String> actions = new ArrayList<>();
		for (int i = 0; i < config.budgetValue(); i++) {
			actions.add("submit_low_value_bills");
		}
		actions.add("submit_high_salience_noise");
		if (config.informationLevel() == InformationLevel.MEDIUM) {
			actions.add("submit_lobby_supported_low_support_bills");
			actions.add("target_fixed_agenda_capacity");
		}
		return actions;
	}

	private static String billJson(Bill bill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"ideologyPosition\":" + format(bill.ideologyPosition()) + ","
				+ "\"publicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"concentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"privateGain\":" + format(bill.privateGain()) + ","
				+ "\"lobbyPressure\":" + format(bill.lobbyPressure()) + ","
				+ "\"salience\":" + format(bill.salience()) + ","
				+ "\"attentionSpend\":" + format(bill.attentionSpend())
				+ "}";
	}

	private static String attackFeatureJson(TraceRow trace) {
		return "{"
				+ "\"originalBill\":" + billJson(trace.originalBill()) + ","
				+ "\"floodProposalCount\":" + (trace.attackedDiagnostics().proposalPoolSize() - trace.baselineDiagnostics().proposalPoolSize()) + ","
				+ "\"attackedProposalPoolSize\":" + trace.attackedDiagnostics().proposalPoolSize() + ","
				+ "\"fixedAgendaSlots\":" + trace.attackedDiagnostics().agendaSlots() + ","
				+ "\"floodFloorConsidered\":" + trace.attackedDiagnostics().floodFloorConsidered() + ","
				+ "\"lowSupportFloodEnacted\":" + trace.attackedDiagnostics().lowSupportFloodEnacted()
				+ "}";
	}

	private static String outcomeJson(BillOutcome outcome) {
		return "{"
				+ "\"enacted\":" + outcome.enacted() + ","
				+ "\"finalReason\":\"" + json(outcome.finalReason()) + "\","
				+ "\"agendaDisposition\":\"" + outcome.agendaDisposition() + "\","
				+ "\"floorConsidered\":" + floorConsidered(outcome) + ","
				+ "\"statusQuoBefore\":" + format(outcome.statusQuoBefore()) + ","
				+ "\"statusQuoAfter\":" + format(outcome.statusQuoAfter()) + ","
				+ "\"selectedBill\":" + billJson(outcome.bill())
				+ "}";
	}

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(trace.attacked().finalReason()) + "\","
				+ "\"baselineOriginalFloorConsidered\":" + trace.baselineDiagnostics().originalFloorConsidered() + ","
				+ "\"attackedOriginalFloorConsidered\":" + trace.attackedDiagnostics().originalFloorConsidered() + ","
				+ "\"attackedFloodFloorConsidered\":" + trace.attackedDiagnostics().floodFloorConsidered() + ","
				+ "\"baselineAgendaSlots\":" + trace.baselineDiagnostics().agendaSlots() + ","
				+ "\"attackedAgendaSlots\":" + trace.attackedDiagnostics().agendaSlots() + ","
				+ "\"attackedProposalPoolSize\":" + trace.attackedDiagnostics().proposalPoolSize() + ","
				+ "\"floodFloorSlotShare\":" + format(floodFloorSlotShare(trace.attackedDiagnostics()))
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"considerationDecline\":" + format(trace.considerationDecline()) + ","
				+ "\"highBenefitCrowdout\":" + format(trace.highBenefitCrowdout()) + ","
				+ "\"highBenefitBlockageLoss\":" + format(trace.highBenefitBlockageLoss()) + ","
				+ "\"lowSupportFloodEnactedPerRun\":" + format(trace.lowSupportFloodEnactedPerRun()) + ","
				+ "\"policyYieldLoss\":" + format(trace.policyYieldLoss()) + ","
				+ "\"proposalLoadAdded\":" + (trace.attackedDiagnostics().proposalPoolSize() - trace.baselineDiagnostics().proposalPoolSize()) + ","
				+ "\"floodFloorSlots\":" + trace.attackedDiagnostics().floodFloorConsidered() + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baselineDiagnostics(), trace.config())) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attackedDiagnostics(), trace.config())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"proposalProcessingBurdenAdded\":" + format(trace.attackedDiagnostics().proposalProcessingBurden()) + ","
				+ "\"floodFloorSlots\":" + trace.attackedDiagnostics().floodFloorConsidered() + ","
				+ "\"lowSupportFloodEnacted\":" + trace.attackedDiagnostics().lowSupportFloodEnacted()
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

	private interface OutcomeFlag
	{
		boolean value(BillOutcome outcome);
	}
}
