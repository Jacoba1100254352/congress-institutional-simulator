package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.bargaining.MultiRoundAmendmentProcess;
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

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;


public final class A2PoisonPillAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A2";
	private static final String CASE_KEY = "poison-pill-sequencing-pressure";
	private static final String MECHANISM_FAMILY = "multi_round_amendment_majority";
	private static final String BASELINE_SCENARIO = "multi-round-amendment-benign";
	private static final String ATTACK_SCENARIO = "multi-round-amendment-a2-poison-pill";
	private static final String BUDGET_UNIT = "amendment_slots";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a2.jsonl";
	private static final String CLAIM_BOUNDARY =
			"A2 executable pilot only. Rows use same generated worlds and bill ids for benign amendment "
			+ "and poison-pill/sequencing attack cells with synthetic amendment-slot budgets. This is not "
			+ "an empirical rider frequency estimate, not a full A1-A9 adversarial sweep, and not evidence "
			+ "for real-world institutional ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		double poisonPillProbability() {
			double base = informationLevel == InformationLevel.HIGH ? 0.62 : 0.38;
			return Math.min(0.92, base + (0.045 * budgetValue));
		}

		double roundCost() {
			return informationLevel == InformationLevel.HIGH ? 0.018 : 0.024;
		}

		double proposerConcessionLimit() {
			return informationLevel == InformationLevel.HIGH ? 1.35 : 1.18;
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			BillOutcome baseline,
			BillOutcome attacked,
			double publicBenefitLoss,
			double publicSupportLoss,
			double concentratedHarmAdded,
			double policyShiftLoss,
			double amendmentOverloadAdded,
			boolean success
	) {}

	private A2PoisonPillAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a2.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a2-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a2-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a2-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a2.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a2-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a2-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a2-run-manifest.json"));
	}

	public static void runSummaryOnly(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a2-summary.csv"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a2-summary.csv"));
	}

	private static void validateRunParameters(int runs, int legislators, int bills) {
		if (runs <= 0 || legislators <= 0 || bills <= 0) {
			throw new IllegalArgumentException("Runs, legislators, and bills must all be positive.");
		}
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = poisonPillWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 2702);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : attackConfigs()) {
				LegislativeProcess baselineProcess = process(
						world,
						config.budgetValue(),
						config.roundCost(),
						config.proposerConcessionLimit(),
						0.0,
						"A2 benign amendment baseline"
				);
				LegislativeProcess attackedProcess = process(
						world,
						config.budgetValue(),
						config.roundCost(),
						config.proposerConcessionLimit(),
						config.poisonPillProbability(),
						"A2 poison-pill attacked amendment process"
				);
				Random baselineRandom = new Random(mix(seed, run, 3102 + config.budgetValue()));
				Random attackedRandom = new Random(mix(seed, run, 3102 + config.budgetValue()));
				PolicyState baselinePolicy = world.initialPolicy();
				PolicyState attackedPolicy = world.initialPolicy();
				List<Bill> worldBills = world.bills();
				for (int billIndex = 0; billIndex < worldBills.size(); billIndex++) {
					Bill bill = worldBills.get(billIndex);
					BillOutcome baseline = baselineProcess.consider(
							bill,
							new VoteContext(world.partyPositions(), baselineRandom, baselinePolicy.position())
					);
					BillOutcome attacked = attackedProcess.consider(
							bill,
							new VoteContext(world.partyPositions(), attackedRandom, attackedPolicy.position())
					);
					traces.add(trace(run, worldSeed, billIndex, config, bill, baseline, attacked));
					baselinePolicy = new PolicyState(baseline.statusQuoAfter());
					attackedPolicy = new PolicyState(attacked.statusQuoAfter());
				}
			}
		}
		return traces;
	}

	private static WorldSpec poisonPillWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.72,
				0.64,
				0.38,
				0.66,
				0.46,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.HIGH_BENEFIT_EXTREME_REFORM
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			int maxRounds,
			double roundCost,
			double proposerConcessionLimit,
			double poisonPillProbability,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		return new MultiRoundAmendmentProcess(
				name,
				new UnicameralProcess(name, chamber),
				world.legislators(),
				maxRounds,
				roundCost,
				proposerConcessionLimit,
				poisonPillProbability
		);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		double publicBenefitLoss = baseline.bill().publicBenefit() - attacked.bill().publicBenefit();
		double publicSupportLoss = baseline.bill().publicSupport() - attacked.bill().publicSupport();
		double concentratedHarmAdded = attacked.bill().concentratedHarm() - baseline.bill().concentratedHarm();
		double policyShiftLoss = Math.abs(baseline.statusQuoAfter() - baseline.statusQuoBefore())
				- Math.abs(attacked.statusQuoAfter() - attacked.statusQuoBefore());
		double amendmentOverloadAdded = supplemental(attacked, "amendmentOverload") - supplemental(baseline, "amendmentOverload");
		boolean highBenefitBlocked = baseline.enacted() && !attacked.enacted() && baseline.bill().publicBenefit() >= 0.55;
		boolean harmfulRiderPassed = attacked.enacted() && (publicBenefitLoss > 0.050 || concentratedHarmAdded > 0.050);
		boolean supportCollapse = publicSupportLoss > 0.075;
		boolean success = highBenefitBlocked || harmfulRiderPassed || supportCollapse;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				originalBill,
				baseline,
				attacked,
				publicBenefitLoss,
				publicSupportLoss,
				concentratedHarmAdded,
				policyShiftLoss,
				amendmentOverloadAdded,
				success
		);
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
		jsonObject(builder, "preAttackFeatures", billJson(trace.originalBill()));
		jsonObject(builder, "postAttackFeatures", billJson(trace.attacked().bill()));
		jsonObject(builder, "institutionalPath", pathJson(trace.baseline(), trace.attacked()));
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessCount,attackSuccessRate,meanPublicBenefitLoss,medianPublicBenefitLoss,worstPublicBenefitLoss,meanPublicSupportLoss,medianPublicSupportLoss,worstPublicSupportLoss,meanConcentratedHarmAdded,medianConcentratedHarmAdded,worstConcentratedHarmAdded,highBenefitBlockageRate,harmfulRiderPassageRate,meanAmendmentOverloadAdded,worstAmendmentOverloadAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("poison_pill_sequencing")).append(',')
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
			       .append(format(mean(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(median(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(max(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(mean(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(median(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(max(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(mean(group, TraceRow::concentratedHarmAdded))).append(',')
			       .append(format(median(group, TraceRow::concentratedHarmAdded))).append(',')
			       .append(format(max(group, TraceRow::concentratedHarmAdded))).append(',')
			       .append(format(highBenefitBlockageRate(group))).append(',')
			       .append(format(harmfulRiderPassageRate(group))).append(',')
			       .append(format(mean(group, TraceRow::amendmentOverloadAdded))).append(',')
			       .append(format(max(group, TraceRow::amendmentOverloadAdded))).append(',')
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
		builder.append("# A2 Poison-Pill Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a2_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A2 poison-pill or sequencing actor\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | Median benefit loss | Worst benefit loss | Median support loss | Harm added | High-benefit blockage | Harmful rider passage | Overload added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(median(group, TraceRow::publicBenefitLoss))).append(" | ")
			       .append(format(max(group, TraceRow::publicBenefitLoss))).append(" | ")
			       .append(format(median(group, TraceRow::publicSupportLoss))).append(" | ")
			       .append(format(median(group, TraceRow::concentratedHarmAdded))).append(" | ")
			       .append(format(highBenefitBlockageRate(group))).append(" | ")
			       .append(format(harmfulRiderPassageRate(group))).append(" | ")
			       .append(format(mean(group, TraceRow::amendmentOverloadAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A2 beyond unsupported planning, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader mechanism coverage, multi-seed replication, and external validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a2-run-v0", true);
		property(builder, 1, "status", "partial_a2_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a2-summary.csv",
				"reports/adversarial-stress-a2-summary.md",
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

	private static double highBenefitBlockageRate(List<TraceRow> rows) {
		return rate(rows, row -> row.baseline().enacted() && !row.attacked().enacted() && row.baseline().bill().publicBenefit() >= 0.55);
	}

	private static double harmfulRiderPassageRate(List<TraceRow> rows) {
		return rate(rows, row -> row.attacked().enacted() && (row.publicBenefitLoss() > 0.050 || row.concentratedHarmAdded() > 0.050));
	}

	private static double supplemental(BillOutcome outcome, String key) {
		return outcome.signals().supplementalMetrics().getOrDefault(key, 0.0);
	}

	private static List<String> actionList(AttackConfig config) {
		List<String> actions = new ArrayList<>();
		if (config.budgetValue() >= 1) {
			actions.add("sequence_polarizing_amendment_first");
		}
		for (int i = 0; i < config.budgetValue(); i++) {
			actions.add("attach_harmful_rider");
		}
		if (config.informationLevel() == InformationLevel.HIGH) {
			actions.add("target_high_benefit_low_initial_support_bill");
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
				+ "\"amendmentMovement\":" + format(bill.amendmentMovement())
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

	private static String pathJson(BillOutcome baseline, BillOutcome attacked) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(baseline.finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(attacked.finalReason()) + "\","
				+ "\"baselinePoisonPillRate\":" + format(supplemental(baseline, "poisonPillRate")) + ","
				+ "\"attackedPoisonPillRate\":" + format(supplemental(attacked, "poisonPillRate")) + ","
				+ "\"baselineAmendmentRoundUse\":" + format(supplemental(baseline, "amendmentRoundUse")) + ","
				+ "\"attackedAmendmentRoundUse\":" + format(supplemental(attacked, "amendmentRoundUse"))
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"publicBenefitLoss\":" + format(trace.publicBenefitLoss()) + ","
				+ "\"publicSupportLoss\":" + format(trace.publicSupportLoss()) + ","
				+ "\"concentratedHarmAdded\":" + format(trace.concentratedHarmAdded()) + ","
				+ "\"policyShiftLoss\":" + format(trace.policyShiftLoss()) + ","
				+ "\"amendmentOverloadAdded\":" + format(trace.amendmentOverloadAdded()) + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineAmendmentOverload\":" + format(supplemental(trace.baseline(), "amendmentOverload")) + ","
				+ "\"attackedAmendmentOverload\":" + format(supplemental(trace.attacked(), "amendmentOverload")) + ","
				+ "\"amendmentOverloadAdded\":" + format(trace.amendmentOverloadAdded())
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
