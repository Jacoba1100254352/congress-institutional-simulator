package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.HarmWeightedThresholdProcess;
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
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;


public final class A4BadFaithHarmClaimAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A4";
	private static final String CASE_KEY = "bad-faith-harm-claim-pressure";
	private static final String MECHANISM_FAMILY = "harm_weighted_majority";
	private static final String BASELINE_SCENARIO = "harm-weighted-benign-majority";
	private static final String ATTACK_SCENARIO = "harm-weighted-a4-bad-faith-claims";
	private static final String BUDGET_UNIT = "harm_claims_filed";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a4.jsonl";
	private static final double HARM_REVIEW_THRESHOLD = 0.46;
	private static final double BASELINE_LEGAL_ATTENTION = 0.035;
	private static final String CLAIM_BOUNDARY =
			"A4 executable pilot only. Rows use same generated worlds and bill ids for targeted synthetic "
			+ "harm-claim cases under benign and bad-faith claim signals with medium-information harm-claim "
			+ "budgets. This is not an empirical claim-filing, litigation, or legal-review frequency estimate, "
			+ "not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		double harmClaimShift() {
			return Math.min(0.460, 0.150 + (0.050 * budgetValue));
		}

		double affectedSupportShift() {
			return Math.min(0.360, 0.090 + (0.035 * budgetValue));
		}

		double compensationCostShift() {
			return Math.min(0.240, 0.035 * budgetValue);
		}

		double legalAttentionSpend() {
			return 0.120 * budgetValue;
		}

		double legalAttentionPerReview() {
			return BASELINE_LEGAL_ATTENTION + 0.060 + (0.025 * budgetValue);
		}
	}

	private record ClaimStrategy(String action, String target, double direction) {
		boolean exaggerates() {
			return direction > 0.0;
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			Bill attackedClaimBill,
			BillOutcome baseline,
			BillOutcome attacked,
			boolean baselineHarmReview,
			boolean attackedHarmReview,
			boolean falsePositiveBlock,
			boolean falsePositiveBurden,
			boolean falseNegativeClearance,
			double falsePositiveBurdenAdded,
			double concentratedHarmPassageAdded,
			double highBenefitBlockageLoss,
			double administrativeBurdenAdded,
			boolean success
	) {}

	private A4BadFaithHarmClaimAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a4.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a4-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a4-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a4-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a4.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a4-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a4-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a4-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = harmClaimWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 4704);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : attackConfigs()) {
				LegislativeProcess baselineProcess = process(
						world,
						BASELINE_LEGAL_ATTENTION,
						"A4 benign harm-weighted baseline"
				);
				LegislativeProcess attackedProcess = process(
						world,
						config.legalAttentionPerReview(),
						"A4 bad-faith harm-claim process"
				);
				Random baselineRandom = new Random(mix(seed, run, 5104 + config.budgetValue()));
				Random attackedRandom = new Random(mix(seed, run, 5104 + config.budgetValue()));
				PolicyState baselinePolicy = world.initialPolicy();
				PolicyState attackedPolicy = world.initialPolicy();
				List<Bill> worldBills = world.bills();
				for (int billIndex = 0; billIndex < worldBills.size(); billIndex++) {
					Bill originalBill = harmClaimCaseBill(worldBills.get(billIndex), billIndex);
					Bill attackedBill = attackBill(originalBill, config, billIndex);
					BillOutcome baseline = baselineProcess.consider(
							originalBill,
							new VoteContext(world.partyPositions(), baselineRandom, baselinePolicy.position())
					);
					BillOutcome attacked = attackedProcess.consider(
							attackedBill,
							new VoteContext(world.partyPositions(), attackedRandom, attackedPolicy.position())
					);
					traces.add(trace(run, worldSeed, billIndex, config, originalBill, attackedBill, baseline, attacked));
					baselinePolicy = new PolicyState(baseline.statusQuoAfter());
					attackedPolicy = new PolicyState(attacked.statusQuoAfter());
				}
			}
		}
		return traces;
	}

	private static WorldSpec harmClaimWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.74,
				0.66,
				0.46,
				0.62,
				0.42,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.BASELINE
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			double legalAttentionPerReview,
			String name
	) {
		Chamber ordinary = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		Chamber highHarm = new Chamber(
				"Congress harm review",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.supermajority(0.64)
		);
		LegislativeProcess inner = new HarmWeightedThresholdProcess(name, ordinary, highHarm, HARM_REVIEW_THRESHOLD);
		return new InstrumentedHarmReviewProcess(name, inner, legalAttentionPerReview);
	}

	private static Bill harmClaimCaseBill(Bill bill, int billIndex) {
		if (billIndex % 2 == 0) {
			double revisedSupport = Math.max(bill.publicSupport(), 0.620);
			double revisedBenefit = Math.max(bill.publicBenefit(), 0.700);
			double revisedIdeology = Values.clamp(bill.ideologyPosition() * 0.42, -1.0, 1.0);
			return bill.withAmendment(revisedIdeology, revisedSupport, revisedBenefit)
			           .withAffectedGroup(
					           bill.affectedGroup(),
					           Math.max(bill.affectedGroupSupport(), 0.660),
					           Math.min(bill.concentratedHarm(), 0.280),
					           Math.min(bill.compensationCost(), 0.120)
			           )
			           .withPublicBenefitUncertainty(Math.min(bill.publicBenefitUncertainty(), 0.240));
		}
		double revisedSupport = Math.max(Math.min(bill.publicSupport(), 0.650), 0.540);
		double revisedBenefit = Math.min(bill.publicBenefit(), 0.390);
		double revisedIdeology = Values.clamp(bill.ideologyPosition() * 0.38, -1.0, 1.0);
		return bill.withAmendment(revisedIdeology, revisedSupport, revisedBenefit)
		           .withLobbyActivity(
				           Math.max(bill.lobbyPressure(), 0.420),
				           revisedSupport,
				           revisedBenefit,
				           Math.max(bill.privateGain(), 0.620),
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0
		           )
		           .withAffectedGroup(
				           bill.affectedGroup(),
				           Math.min(bill.affectedGroupSupport(), 0.340),
				           Math.max(bill.concentratedHarm(), 0.610),
				           Math.max(bill.compensationCost(), 0.300)
		           )
		           .withPublicBenefitUncertainty(Math.max(bill.publicBenefitUncertainty(), 0.420));
	}

	private static Bill attackBill(Bill bill, AttackConfig config, int billIndex) {
		ClaimStrategy strategy = strategy(billIndex);
		double revisedHarm = Values.clamp(
				bill.concentratedHarm() + (strategy.direction() * config.harmClaimShift()),
				0.0,
				1.0
		);
		double revisedAffectedSupport = Values.clamp(
				bill.affectedGroupSupport() - (strategy.direction() * config.affectedSupportShift()),
				0.0,
				1.0
		);
		double revisedCompensationCost = Values.clamp(
				bill.compensationCost() + (strategy.direction() * config.compensationCostShift()),
				0.0,
				1.0
		);
		double revisedUncertainty = Values.clamp(
				bill.publicBenefitUncertainty() + (0.030 * config.budgetValue()),
				0.0,
				1.0
		);
		return bill.withAffectedGroup(
					bill.affectedGroup(),
					revisedAffectedSupport,
					revisedHarm,
					revisedCompensationCost
				)
		           .withPublicBenefitUncertainty(revisedUncertainty)
		           .withAttentionSpend(config.legalAttentionSpend());
	}

	private static ClaimStrategy strategy(int billIndex) {
		if (billIndex % 2 == 0) {
			return new ClaimStrategy("exaggerate_harm", "target_rivals", 1.0);
		}
		return new ClaimStrategy("understate_ally_harm", "understate_ally_harm", -1.0);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			Bill attackedClaimBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		boolean baselineReview = harmReviewTriggered(originalBill);
		boolean attackedReview = harmReviewTriggered(attackedClaimBill);
		boolean falsePositiveBurden = !baselineReview && attackedReview && originalBill.concentratedHarm() < HARM_REVIEW_THRESHOLD;
		boolean falsePositiveBlock = falsePositiveBurden
				&& baseline.enacted()
				&& !attacked.enacted()
				&& originalBill.publicBenefit() >= 0.55;
		boolean falseNegativeClearance = baselineReview
				&& !attackedReview
				&& !baseline.enacted()
				&& attacked.enacted()
				&& originalBill.concentratedHarm() >= HARM_REVIEW_THRESHOLD;
		double falsePositiveBurdenAdded = falsePositiveBurden ? administrativeBurden(attacked) - administrativeBurden(baseline) : 0.0;
		double baselineHarmPassage = baseline.enacted() ? originalBill.concentratedHarm() : 0.0;
		double attackedHarmPassage = attacked.enacted() ? originalBill.concentratedHarm() : 0.0;
		double concentratedHarmPassageAdded = attackedHarmPassage - baselineHarmPassage;
		double highBenefitBlockageLoss = falsePositiveBlock ? originalBill.publicBenefit() : 0.0;
		double administrativeBurdenAdded = administrativeBurden(attacked) - administrativeBurden(baseline);
		boolean success = falsePositiveBlock
				|| falseNegativeClearance
				|| falsePositiveBurdenAdded > 0.120
				|| concentratedHarmPassageAdded > 0.080
				|| administrativeBurdenAdded > 0.220;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				originalBill,
				attackedClaimBill,
				baseline,
				attacked,
				baselineReview,
				attackedReview,
				falsePositiveBlock,
				falsePositiveBurden,
				falseNegativeClearance,
				falsePositiveBurdenAdded,
				concentratedHarmPassageAdded,
				highBenefitBlockageLoss,
				administrativeBurdenAdded,
				success
		);
	}

	private static List<AttackConfig> attackConfigs() {
		List<AttackConfig> configs = new ArrayList<>();
		for (int budget : List.of(1, 3, 6)) {
			configs.add(new AttackConfig(budget, InformationLevel.MEDIUM));
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
		jsonArray(builder, "attackActionList", actionList(trace.config(), strategy(trace.billIndex())));
		jsonObject(builder, "preAttackFeatures", billJson(trace.originalBill()));
		jsonObject(builder, "postAttackFeatures", billJson(trace.attackedClaimBill()));
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,meanFalsePositiveBurdenAdded,medianFalsePositiveBurdenAdded,worstFalsePositiveBurdenAdded,falsePositiveBlockRate,falseNegativeClearanceRate,meanConcentratedHarmPassageAdded,worstConcentratedHarmPassageAdded,meanHighBenefitBlockageLoss,worstHighBenefitBlockageLoss,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("bad_faith_harm_claims")).append(',')
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
			       .append(format(mean(group, TraceRow::falsePositiveBurdenAdded))).append(',')
			       .append(format(median(group, TraceRow::falsePositiveBurdenAdded))).append(',')
			       .append(format(max(group, TraceRow::falsePositiveBurdenAdded))).append(',')
			       .append(format(rate(group, TraceRow::falsePositiveBlock))).append(',')
			       .append(format(rate(group, TraceRow::falseNegativeClearance))).append(',')
			       .append(format(mean(group, TraceRow::concentratedHarmPassageAdded))).append(',')
			       .append(format(max(group, TraceRow::concentratedHarmPassageAdded))).append(',')
			       .append(format(mean(group, TraceRow::highBenefitBlockageLoss))).append(',')
			       .append(format(max(group, TraceRow::highBenefitBlockageLoss))).append(',')
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
		builder.append("# A4 Bad-Faith Harm-Claim Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a4_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A4 bad-faith harm claimant\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | False-positive block | False-negative clearance | Median FP burden added | Worst FP burden added | Mean harm passage added | Mean admin burden added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(rate(group, TraceRow::falsePositiveBlock))).append(" | ")
			       .append(format(rate(group, TraceRow::falseNegativeClearance))).append(" | ")
			       .append(format(median(group, TraceRow::falsePositiveBurdenAdded))).append(" | ")
			       .append(format(max(group, TraceRow::falsePositiveBurdenAdded))).append(" | ")
			       .append(format(mean(group, TraceRow::concentratedHarmPassageAdded))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A4 beyond aggregate loose-claims mapping, but the robustness breakout remains below manuscript gate because A7-A9 executable sweeps, recovery/correction metrics, broader mechanism coverage, seed sensitivity, and external harm-claim validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a4-run-v0", true);
		property(builder, 1, "status", "partial_a4_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a4-summary.csv",
				"reports/adversarial-stress-a4-summary.md",
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

	private static boolean harmReviewTriggered(Bill bill) {
		return bill.concentratedHarm() >= HARM_REVIEW_THRESHOLD;
	}

	private static double administrativeBurden(BillOutcome outcome) {
		return outcome.bill().attentionSpend()
				+ supplemental(outcome, "legalReviewBurden")
				+ (0.220 * supplemental(outcome, "harmReviewTriggered"));
	}

	private static double supplemental(BillOutcome outcome, String key) {
		return outcome.signals().supplementalMetrics().getOrDefault(key, 0.0);
	}

	private static List<String> actionList(AttackConfig config, ClaimStrategy strategy) {
		List<String> actions = new ArrayList<>();
		actions.add(strategy.action());
		actions.add(strategy.target());
		for (int i = 0; i < config.budgetValue(); i++) {
			actions.add("duplicate_claims");
		}
		actions.add("legal_attention_units");
		return actions;
	}

	private static String billJson(Bill bill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"ideologyPosition\":" + format(bill.ideologyPosition()) + ","
				+ "\"publicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"affectedGroup\":\"" + json(bill.affectedGroup()) + "\","
				+ "\"affectedGroupSupport\":" + format(bill.affectedGroupSupport()) + ","
				+ "\"concentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"minorityHarm\":" + format(minorityHarm(bill)) + ","
				+ "\"compensationCost\":" + format(bill.compensationCost()) + ","
				+ "\"publicBenefitUncertainty\":" + format(bill.publicBenefitUncertainty()) + ","
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
				+ "\"harmReviewTriggered\":" + format(supplemental(outcome, "harmReviewTriggered")) + ","
				+ "\"legalReviewBurden\":" + format(supplemental(outcome, "legalReviewBurden")) + ","
				+ "\"selectedBill\":" + billJson(outcome.bill())
				+ "}";
	}

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(trace.attacked().finalReason()) + "\","
				+ "\"baselineHarmReviewTriggered\":" + trace.baselineHarmReview() + ","
				+ "\"attackedHarmReviewTriggered\":" + trace.attackedHarmReview() + ","
				+ "\"trueConcentratedHarm\":" + format(trace.originalBill().concentratedHarm()) + ","
				+ "\"claimedConcentratedHarm\":" + format(trace.attackedClaimBill().concentratedHarm()) + ","
				+ "\"trueAffectedGroupSupport\":" + format(trace.originalBill().affectedGroupSupport()) + ","
				+ "\"claimedAffectedGroupSupport\":" + format(trace.attackedClaimBill().affectedGroupSupport()) + ","
				+ "\"harmReviewThreshold\":" + format(HARM_REVIEW_THRESHOLD)
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"falsePositiveBurdenAdded\":" + format(trace.falsePositiveBurdenAdded()) + ","
				+ "\"falsePositiveBurden\":" + trace.falsePositiveBurden() + ","
				+ "\"falsePositiveBlock\":" + trace.falsePositiveBlock() + ","
				+ "\"falseNegativeClearance\":" + trace.falseNegativeClearance() + ","
				+ "\"concentratedHarmPassageAdded\":" + format(trace.concentratedHarmPassageAdded()) + ","
				+ "\"highBenefitBlockageLoss\":" + format(trace.highBenefitBlockageLoss()) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline())) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attacked())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"baselineLegalReviewBurden\":" + format(supplemental(trace.baseline(), "legalReviewBurden")) + ","
				+ "\"attackedLegalReviewBurden\":" + format(supplemental(trace.attacked(), "legalReviewBurden")) + ","
				+ "\"baselineClaimAttentionSpend\":" + format(trace.baseline().bill().attentionSpend()) + ","
				+ "\"attackedClaimAttentionSpend\":" + format(trace.attacked().bill().attentionSpend())
				+ "}";
	}

	private static double minorityHarm(Bill bill) {
		double consentDeficit = 1.0 - bill.affectedGroupSupport();
		return Values.clamp(bill.concentratedHarm() * consentDeficit, 0.0, 1.0);
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

	private record InstrumentedHarmReviewProcess(
			String name,
			LegislativeProcess innerProcess,
			double legalAttentionPerReview
	) implements LegislativeProcess
	{
		@Override
		public BillOutcome consider(Bill bill, VoteContext context) {
			boolean harmReviewTriggered = harmReviewTriggered(bill);
			BillOutcome outcome = innerProcess.consider(bill, context);
			return outcome.withSignals(OutcomeSignals.diagnostics(Map.of(
					"harmReviewTriggered", harmReviewTriggered ? 1.0 : 0.0,
					"legalReviewBurden", harmReviewTriggered ? legalAttentionPerReview : 0.0
			)));
		}
	}
}
