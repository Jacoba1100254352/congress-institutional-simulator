package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.publicinput.CitizenPanelReviewProcess;
import congresssim.institution.publicinput.PublicObjectionWindowProcess;
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
import java.util.Random;
import java.util.stream.Collectors;


public final class A3PublicInputAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A3";
	private static final String CASE_KEY = "public-input-manipulation-pressure";
	private static final String MECHANISM_FAMILY = "public_objection_and_citizen_panel_majority";
	private static final String BASELINE_SCENARIO = "public-input-benign-majority";
	private static final String ATTACK_SCENARIO = "public-input-a3-manipulated-majority";
	private static final String BUDGET_UNIT = "public_attention_units";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a3.jsonl";
	private static final String CLAIM_BOUNDARY =
			"A3 executable pilot only. Rows use same generated worlds and bill ids for benign public-input "
			+ "and manipulated objection/panel cells with synthetic public-attention budgets. This is not "
			+ "an empirical astroturf, public-comment, or panel-manipulation frequency estimate, not a full "
			+ "A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		double signalShift() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.070 : 0.045;
			return Math.min(0.190, base + (0.015 * budgetValue));
		}

		double salienceBoost() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.080 : 0.055;
			return Math.min(0.220, base + (0.018 * budgetValue));
		}

		double publicCampaignSpend() {
			double scale = informationLevel == InformationLevel.MEDIUM ? 3.4 : 2.2;
			return scale * budgetValue;
		}

		double attentionSpend() {
			double scale = informationLevel == InformationLevel.MEDIUM ? 0.115 : 0.085;
			return scale * budgetValue;
		}

		double objectionThreshold() {
			double informationAdjustment = informationLevel == InformationLevel.MEDIUM ? 0.040 : 0.015;
			return Math.max(0.360, 0.640 - informationAdjustment - (0.030 * budgetValue));
		}

		double objectionNoise() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.045 : 0.030;
			return Math.min(0.190, base + (0.018 * budgetValue));
		}

		int panelSize() {
			int base = informationLevel == InformationLevel.MEDIUM ? 44 : 58;
			return Math.max(18, base - (4 * budgetValue));
		}

		double panelNoise() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.120 : 0.090;
			return Math.min(0.300, base + (0.018 * budgetValue));
		}

		double informationQuality() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.500 : 0.620;
			return Math.max(0.340, base - (0.018 * budgetValue));
		}

		double manipulationRisk() {
			double base = informationLevel == InformationLevel.MEDIUM ? 0.420 : 0.260;
			return Math.min(0.760, base + (0.040 * budgetValue));
		}

		double certificationThreshold() {
			return informationLevel == InformationLevel.MEDIUM ? 0.605 : 0.575;
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			Bill attackedInputBill,
			BillOutcome baseline,
			BillOutcome attacked,
			double publicBenefitLoss,
			double publicSupportLoss,
			double publicPreferenceDistortionAdded,
			double publicSignalMovementAdded,
			double administrativeBurdenAdded,
			boolean falsePositiveBlock,
			boolean falseNegativeClearance,
			boolean lowSupportEnactmentAdded,
			boolean success
	) {}

	private record Distortion(double direction, String target) {}

	private A3PublicInputAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a3.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a3-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a3-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a3-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a3.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a3-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a3-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a3-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = publicInputWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 3703);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : attackConfigs()) {
				LegislativeProcess baselineProcess = process(world, config, false, "A3 benign public-input baseline");
				LegislativeProcess attackedProcess = process(world, config, true, "A3 manipulated public-input process");
				Random baselineRandom = new Random(mix(seed, run, 4103 + config.budgetValue()));
				Random attackedRandom = new Random(mix(seed, run, 4103 + config.budgetValue()));
				PolicyState baselinePolicy = world.initialPolicy();
				PolicyState attackedPolicy = world.initialPolicy();
				List<Bill> worldBills = world.bills();
				for (int billIndex = 0; billIndex < worldBills.size(); billIndex++) {
					Bill bill = worldBills.get(billIndex);
					Bill attackedBill = attackBill(bill, config);
					BillOutcome baseline = baselineProcess.consider(
							bill,
							new VoteContext(world.partyPositions(), baselineRandom, baselinePolicy.position())
					);
					BillOutcome attacked = attackedProcess.consider(
							attackedBill,
							new VoteContext(world.partyPositions(), attackedRandom, attackedPolicy.position())
					);
					traces.add(trace(run, worldSeed, billIndex, config, bill, attackedBill, baseline, attacked));
					baselinePolicy = new PolicyState(baseline.statusQuoAfter());
					attackedPolicy = new PolicyState(attacked.statusQuoAfter());
				}
			}
		}
		return traces;
	}

	private static WorldSpec publicInputWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.78,
				0.70,
				0.50,
				0.58,
				0.36,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.PUBLIC_OPINION_ERROR
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			AttackConfig config,
			boolean attacked,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		LegislativeProcess floor = new UnicameralProcess(name + " floor", chamber);
		LegislativeProcess block = new PublicInputBlockProcess(name + " public-input gate");
		LegislativeProcess panel = new CitizenPanelReviewProcess(
				name + " citizen panel",
				floor,
				block,
				CitizenPanelMode.THRESHOLD_ADJUSTMENT,
				attacked ? config.panelSize() : 96,
				attacked ? config.panelNoise() : 0.035,
				attacked ? config.informationQuality() : 0.780,
				attacked ? config.manipulationRisk() : 0.025,
				attacked ? config.certificationThreshold() : 0.540
		);
		return new PublicObjectionWindowProcess(
				name,
				floor,
				panel,
				attacked ? config.objectionThreshold() : 0.665,
				attacked ? config.objectionNoise() : 0.012,
				false
		);
	}

	private static Bill attackBill(Bill bill, AttackConfig config) {
		Distortion distortion = distortion(bill, config);
		double revisedSupport = Values.clamp(
				bill.publicSupport() + (distortion.direction() * config.signalShift()),
				0.0,
				1.0
		);
		double revisedSalience = Values.clamp(
				bill.salience() + config.salienceBoost(),
				0.0,
				1.0
		);
		double revisedLobbyPressure = Values.clamp(
				bill.lobbyPressure() + (0.030 * config.budgetValue() * distortion.direction()),
				-1.0,
				1.0
		);
		return bill.withPublicSignal(revisedSupport, revisedSalience)
		           .withLobbyActivity(
				           revisedLobbyPressure,
				           revisedSupport,
				           bill.privateGain(),
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           0.0,
				           config.publicCampaignSpend(),
				           0.0
		           )
		           .withAttentionSpend(config.attentionSpend());
	}

	private static Distortion distortion(Bill bill, AttackConfig config) {
		if (config.informationLevel() == InformationLevel.MEDIUM) {
			boolean highBenefit = bill.publicBenefit() >= 0.56 && bill.privateGain() <= bill.publicBenefit();
			boolean harmfulOrCaptured = bill.concentratedHarm() >= 0.36
					|| bill.privateGain() > bill.publicBenefit() + 0.10
					|| bill.lobbyPressure() > 0.35;
			if (highBenefit) {
				return new Distortion(-1.0, "suppress_high_benefit_support");
			}
			if (harmfulOrCaptured) {
				return new Distortion(1.0, "inflate_support_for_harmful_or_captured_bill");
			}
		}
		if (bill.salience() >= 0.54 || bill.publicSupport() >= 0.58) {
			return new Distortion(-1.0, "coordinate_objections_against_visible_bill");
		}
		return new Distortion(1.0, "inflate_cheap_public_signal");
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill originalBill,
			Bill attackedInputBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		double publicBenefitLoss = baseline.bill().publicBenefit() - attacked.bill().publicBenefit();
		double publicSupportLoss = baseline.bill().publicSupport() - attacked.bill().publicSupport();
		double publicPreferenceDistortionAdded = distortion(attacked.bill()) - distortion(baseline.bill());
		double publicSignalMovementAdded = signalMovement(attacked) - signalMovement(baseline);
		double administrativeBurdenAdded = administrativeBurden(attacked) - administrativeBurden(baseline);
		boolean falsePositiveBlock = baseline.enacted()
				&& !attacked.enacted()
				&& (originalBill.publicBenefit() >= 0.56 || originalBill.publicSupport() >= 0.55);
		boolean falseNegativeClearance = !baseline.enacted()
				&& attacked.enacted()
				&& (originalBill.publicBenefit() < 0.46
				|| originalBill.concentratedHarm() >= 0.38
				|| originalBill.privateGain() > originalBill.publicBenefit() + 0.12);
		boolean lowSupportEnactmentAdded = !weakMandateOnOriginalSupport(baseline, originalBill)
				&& attacked.enacted()
				&& originalBill.publicSupport() < 0.50;
		boolean success = falsePositiveBlock
				|| falseNegativeClearance
				|| lowSupportEnactmentAdded
				|| publicPreferenceDistortionAdded > 0.050
				|| administrativeBurdenAdded > 0.250;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				originalBill,
				attackedInputBill,
				baseline,
				attacked,
				publicBenefitLoss,
				publicSupportLoss,
				publicPreferenceDistortionAdded,
				publicSignalMovementAdded,
				administrativeBurdenAdded,
				falsePositiveBlock,
				falseNegativeClearance,
				lowSupportEnactmentAdded,
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
		Distortion distortion = distortion(trace.originalBill(), trace.config());
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
		jsonArray(builder, "attackActionList", actionList(trace.config(), distortion));
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,meanPublicPreferenceDistortionAdded,medianPublicPreferenceDistortionAdded,worstPublicPreferenceDistortionAdded,meanPublicSignalMovementAdded,medianPublicSignalMovementAdded,worstPublicSignalMovementAdded,falsePositiveBlockRate,falseNegativeClearanceRate,lowSupportEnactmentAddedRate,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("public_input_manipulation")).append(',')
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
			       .append(format(mean(group, TraceRow::publicPreferenceDistortionAdded))).append(',')
			       .append(format(median(group, TraceRow::publicPreferenceDistortionAdded))).append(',')
			       .append(format(max(group, TraceRow::publicPreferenceDistortionAdded))).append(',')
			       .append(format(mean(group, TraceRow::publicSignalMovementAdded))).append(',')
			       .append(format(median(group, TraceRow::publicSignalMovementAdded))).append(',')
			       .append(format(max(group, TraceRow::publicSignalMovementAdded))).append(',')
			       .append(format(rate(group, TraceRow::falsePositiveBlock))).append(',')
			       .append(format(rate(group, TraceRow::falseNegativeClearance))).append(',')
			       .append(format(rate(group, TraceRow::lowSupportEnactmentAdded))).append(',')
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
		builder.append("# A3 Public-Input Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a3_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A3 public-input manipulator\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | Median distortion added | Worst distortion added | Median signal movement added | False-positive block | False-negative clearance | Low-support enactment added | Mean admin burden added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(median(group, TraceRow::publicPreferenceDistortionAdded))).append(" | ")
			       .append(format(max(group, TraceRow::publicPreferenceDistortionAdded))).append(" | ")
			       .append(format(median(group, TraceRow::publicSignalMovementAdded))).append(" | ")
			       .append(format(rate(group, TraceRow::falsePositiveBlock))).append(" | ")
			       .append(format(rate(group, TraceRow::falseNegativeClearance))).append(" | ")
			       .append(format(rate(group, TraceRow::lowSupportEnactmentAdded))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A3 beyond aggregate pilot mapping, but the robustness breakout remains below manuscript gate because temporal correction, broader mechanism coverage, multi-seed replication, and external validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a3-run-v0", true);
		property(builder, 1, "status", "partial_a3_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a3-summary.csv",
				"reports/adversarial-stress-a3-summary.md",
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

	private static boolean weakMandateOnOriginalSupport(BillOutcome outcome, Bill originalBill) {
		return outcome.enacted() && originalBill.publicSupport() < 0.50;
	}

	private static double distortion(Bill bill) {
		return Math.abs(bill.publicSupport() - bill.publicBenefit());
	}

	private static double signalMovement(BillOutcome outcome) {
		return outcome.bill().publicSignalMovement() + outcome.signals().publicSignalMovement();
	}

	private static double administrativeBurden(BillOutcome outcome) {
		OutcomeSignals signals = outcome.signals();
		return outcome.bill().attentionSpend()
				+ (0.120 * signals.objectionWindows())
				+ (0.180 * signals.citizenReviews())
				+ (0.090 * Math.max(0, signals.citizenReviews() - signals.citizenCertifications()))
				+ (0.120 * signals.publicWillReviews());
	}

	private static List<String> actionList(AttackConfig config, Distortion distortion) {
		List<String> actions = new ArrayList<>();
		if (distortion.direction() < 0.0) {
			actions.add("file_noisy_objections");
		} else {
			actions.add("inflate_cheap_public_signal");
		}
		for (int i = 0; i < config.budgetValue(); i++) {
			actions.add("coordinate_repetitive_claims");
		}
		if (config.budgetValue() >= 3) {
			actions.add("increase_panel_noise");
		}
		if (config.informationLevel() == InformationLevel.MEDIUM) {
			actions.add("bias_panel_inputs");
			actions.add(distortion.target());
		}
		return actions;
	}

	private static String billJson(Bill bill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"ideologyPosition\":" + format(bill.ideologyPosition()) + ","
				+ "\"publicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"publicPreferenceDistortion\":" + format(distortion(bill)) + ","
				+ "\"publicSignalMovement\":" + format(bill.publicSignalMovement()) + ","
				+ "\"concentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"privateGain\":" + format(bill.privateGain()) + ","
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

	private static String pathJson(BillOutcome baseline, BillOutcome attacked) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(baseline.finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(attacked.finalReason()) + "\","
				+ "\"baselineObjectionWindows\":" + baseline.signals().objectionWindows() + ","
				+ "\"attackedObjectionWindows\":" + attacked.signals().objectionWindows() + ","
				+ "\"baselineCitizenReviews\":" + baseline.signals().citizenReviews() + ","
				+ "\"attackedCitizenReviews\":" + attacked.signals().citizenReviews() + ","
				+ "\"baselineCitizenCertifications\":" + baseline.signals().citizenCertifications() + ","
				+ "\"attackedCitizenCertifications\":" + attacked.signals().citizenCertifications() + ","
				+ "\"baselineCitizenLegitimacy\":" + format(baseline.signals().citizenLegitimacy()) + ","
				+ "\"attackedCitizenLegitimacy\":" + format(attacked.signals().citizenLegitimacy()) + ","
				+ "\"baselinePublicSignalMovement\":" + format(signalMovement(baseline)) + ","
				+ "\"attackedPublicSignalMovement\":" + format(signalMovement(attacked))
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"publicBenefitLoss\":" + format(trace.publicBenefitLoss()) + ","
				+ "\"publicSupportLoss\":" + format(trace.publicSupportLoss()) + ","
				+ "\"publicPreferenceDistortionAdded\":" + format(trace.publicPreferenceDistortionAdded()) + ","
				+ "\"publicSignalMovementAdded\":" + format(trace.publicSignalMovementAdded()) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"falsePositiveBlock\":" + trace.falsePositiveBlock() + ","
				+ "\"falseNegativeClearance\":" + trace.falseNegativeClearance() + ","
				+ "\"lowSupportEnactmentAdded\":" + trace.lowSupportEnactmentAdded() + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline())) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attacked())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"baselineObjectionWindows\":" + trace.baseline().signals().objectionWindows() + ","
				+ "\"attackedObjectionWindows\":" + trace.attacked().signals().objectionWindows() + ","
				+ "\"baselineCitizenReviews\":" + trace.baseline().signals().citizenReviews() + ","
				+ "\"attackedCitizenReviews\":" + trace.attacked().signals().citizenReviews()
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
}
