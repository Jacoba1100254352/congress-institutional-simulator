package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.bargaining.AlternativeSelectionRule;
import congresssim.institution.bargaining.CompetingAlternativesProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.model.Bill;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;
import congresssim.simulation.PartySystemProfile;
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


public final class A1CloneDecoyAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A1";
	private static final String CASE_KEY = "clone-decoy-pressure";
	private static final String MECHANISM_FAMILY = "policy_tournament_pairwise_majority";
	private static final String BASELINE_SCENARIO = "simple-majority-alternatives-pairwise";
	private static final String ATTACK_SCENARIO = "simple-majority-alternatives-a1-clone-decoy";
	private static final String BUDGET_UNIT = "proposal_slots";
	private static final String CLAIM_BOUNDARY =
			"A1 executable pilot only. Rows use same generated worlds and bill ids for baseline and attacked "
			+ "policy-tournament cells with synthetic clone/decoy budgets. This is not an empirical attack-rate "
			+ "estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.";

	private record BudgetConfig(int value, int clones, int decoys) {}

	private record AttackConfig(BudgetConfig budget, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budget.value();
		}

		double supportBoostScale() {
			return informationLevel == InformationLevel.HIGH ? 0.45 : 0.62;
		}

		double agendaOverloadPenalty() {
			return informationLevel == InformationLevel.HIGH ? 0.035 : 0.020;
		}

		double badFaithPenalty() {
			return informationLevel == InformationLevel.HIGH ? 0.100 : 0.060;
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
			double policyShiftLoss,
			double adminCostAdded,
			boolean success
	) {}

	private A1CloneDecoyAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = cloneDecoyWorldSpec(legislators, bills);
		List<AttackConfig> configs = attackConfigs();
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 1701);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : configs) {
				LegislativeProcess baselineProcess = process(world, 0, 0, 1.0, 0.0, 0.0, "A1 baseline pairwise tournament");
				LegislativeProcess attackedProcess = process(
						world,
						config.budget().clones(),
						config.budget().decoys(),
						config.supportBoostScale(),
						config.agendaOverloadPenalty(),
						config.badFaithPenalty(),
						"A1 clone/decoy attacked pairwise tournament"
				);
				Random baselineRandom = new Random(mix(seed, run, 2101 + config.budget().value()));
				Random attackedRandom = new Random(mix(seed, run, 2101 + config.budget().value()));
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

	private static WorldSpec cloneDecoyWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				Math.max(1, bills * 2),
				4,
				0.80,
				0.76,
				0.62,
				0.54,
				0.24,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			int clones,
			int decoys,
			double supportBoostScale,
			double agendaOverloadPenalty,
			double badFaithPenalty,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		return new CompetingAlternativesProcess(
				name,
				new UnicameralProcess(name, chamber),
				world.legislators(),
				AlternativeSelectionRule.PAIRWISE_MAJORITY,
				4,
				true,
				clones,
				decoys,
				supportBoostScale,
				agendaOverloadPenalty,
				badFaithPenalty
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
		double policyShiftLoss = Math.abs(baseline.statusQuoAfter() - baseline.statusQuoBefore())
				- Math.abs(attacked.statusQuoAfter() - attacked.statusQuoBefore());
		double adminCostAdded = attacked.bill().attentionSpend() - baseline.bill().attentionSpend();
		boolean baselineWeakMandate = baseline.enacted() && baseline.bill().publicSupport() < 0.50;
		boolean attackedWeakMandate = attacked.enacted() && attacked.bill().publicSupport() < 0.50;
		boolean highBenefitBlocked = baseline.enacted() && !attacked.enacted() && baseline.bill().publicBenefit() >= 0.55;
		boolean success = publicBenefitLoss > 0.020
				|| publicSupportLoss > 0.020
				|| highBenefitBlocked
				|| (!baselineWeakMandate && attackedWeakMandate);
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
				policyShiftLoss,
				adminCostAdded,
				success
		);
	}

	private static List<AttackConfig> attackConfigs() {
		List<BudgetConfig> budgets = List.of(
				new BudgetConfig(1, 1, 0),
				new BudgetConfig(3, 2, 1),
				new BudgetConfig(6, 3, 3)
		);
		List<AttackConfig> configs = new ArrayList<>();
		for (InformationLevel level : List.of(InformationLevel.MEDIUM, InformationLevel.HIGH)) {
			for (BudgetConfig budget : budgets) {
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
		jsonProperty(builder, "budgetValue", Integer.toString(trace.config().budget().value()), false);
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,meanPublicBenefitLoss,medianPublicBenefitLoss,worstPublicBenefitLoss,meanPublicSupportLoss,medianPublicSupportLoss,worstPublicSupportLoss,enactmentLossRate,lowSupportAddedRate,meanAdminCostAdded,worstAdminCostAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("clone_decoy_pressure")).append(',')
			       .append(csv(CASE_KEY)).append(',')
			       .append(csv(BASELINE_SCENARIO)).append(',')
			       .append(csv(ATTACK_SCENARIO)).append(',')
			       .append(csv(MECHANISM_FAMILY)).append(',')
			       .append(csv(BUDGET_UNIT)).append(',')
			       .append(config.budget().value()).append(',')
			       .append(csv(config.informationLevel().key())).append(',')
			       .append(runs).append(',')
			       .append(legislators).append(',')
			       .append(bills).append(',')
			       .append(group.size()).append(',')
			       .append(format(rate(group, TraceRow::success))).append(',')
			       .append(format(mean(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(median(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(max(group, TraceRow::publicBenefitLoss))).append(',')
			       .append(format(mean(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(median(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(max(group, TraceRow::publicSupportLoss))).append(',')
			       .append(format(enactmentLossRate(group))).append(',')
			       .append(format(lowSupportAddedRate(group))).append(',')
			       .append(format(mean(group, TraceRow::adminCostAdded))).append(',')
			       .append(format(max(group, TraceRow::adminCostAdded))).append(',')
			       .append(csv("not_modeled")).append(',')
			       .append(csv("reports/adversarial-failure-traces.jsonl")).append(',')
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
		builder.append("# Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a1_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A1 clone/decoy proposer\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `reports/adversarial-failure-traces.jsonl`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | Median benefit loss | Worst benefit loss | Median support loss | Worst support loss | Enactment loss rate | Low-support added | Mean admin cost added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budget().value()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(median(group, TraceRow::publicBenefitLoss))).append(" | ")
			       .append(format(max(group, TraceRow::publicBenefitLoss))).append(" | ")
			       .append(format(median(group, TraceRow::publicSupportLoss))).append(" | ")
			       .append(format(max(group, TraceRow::publicSupportLoss))).append(" | ")
			       .append(format(enactmentLossRate(group))).append(" | ")
			       .append(format(lowSupportAddedRate(group))).append(" | ")
			       .append(format(mean(group, TraceRow::adminCostAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A1 beyond schema-only planning, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader mechanism coverage, multi-seed replication, and external validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-run-v0", true);
		property(builder, 1, "status", "partial_a1_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-summary.csv",
				"reports/adversarial-stress-summary.md",
				"reports/adversarial-failure-traces.jsonl"
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

	private static double enactmentLossRate(List<TraceRow> rows) {
		return rate(rows, row -> row.baseline().enacted() && !row.attacked().enacted());
	}

	private static double lowSupportAddedRate(List<TraceRow> rows) {
		return rate(rows, row -> !weakMandate(row.baseline()) && weakMandate(row.attacked()));
	}

	private static boolean weakMandate(BillOutcome outcome) {
		return outcome.enacted() && outcome.bill().publicSupport() < 0.50;
	}

	private static List<String> actionList(AttackConfig config) {
		List<String> actions = new ArrayList<>();
		for (int i = 0; i < config.budget().clones(); i++) {
			actions.add("add_near_duplicate_clone");
		}
		for (int i = 0; i < config.budget().decoys(); i++) {
			actions.add("add_support_splitting_decoy");
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

	private static String pathJson(BillOutcome baseline, BillOutcome attacked) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(baseline.finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(attacked.finalReason()) + "\","
				+ "\"baselineStrategicDecoys\":" + baseline.signals().strategicDecoys() + ","
				+ "\"attackedStrategicDecoys\":" + attacked.signals().strategicDecoys() + ","
				+ "\"baselineAlternativesConsidered\":" + baseline.signals().alternativesConsidered() + ","
				+ "\"attackedAlternativesConsidered\":" + attacked.signals().alternativesConsidered()
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"publicBenefitLoss\":" + format(trace.publicBenefitLoss()) + ","
				+ "\"publicSupportLoss\":" + format(trace.publicSupportLoss()) + ","
				+ "\"policyShiftLoss\":" + format(trace.policyShiftLoss()) + ","
				+ "\"adminCostAdded\":" + format(trace.adminCostAdded()) + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted() + ","
				+ "\"weakMandateAdded\":" + (!weakMandate(trace.baseline()) && weakMandate(trace.attacked()))
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineAttentionSpend\":" + format(trace.baseline().bill().attentionSpend()) + ","
				+ "\"attackedAttentionSpend\":" + format(trace.attacked().bill().attentionSpend()) + ","
				+ "\"attentionSpendAdded\":" + format(trace.adminCostAdded())
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
