package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.publicinput.ConstituentPublicWillProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.model.Bill;
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
import java.util.Locale;
import java.util.Random;
import java.util.stream.Collectors;


public final class A8PublicSupportDistortionAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A8";
	private static final String CASE_KEY = "public-support-distortion";
	private static final String BUDGET_UNIT = "public_campaign_units";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a8.jsonl";
	private static final String CLAIM_BOUNDARY =
			"A8 executable pilot only. Rows pair the same generated world, bill, status quo, formal process, "
			+ "and vote-random stream while an outside campaign changes only the observable public-support and "
			+ "salience signal plus traced campaign/attention spend. Generated support, public benefit, affected-"
			+ "group support, concentrated harm, and private gain remain latent evaluation values. The signal-"
			+ "reliant and constituent-verified paths use no objection window or citizen panel, separating this "
			+ "pilot from A3 formal public-input manipulation. Signal shifts and verification strengths are "
			+ "synthetic assumptions, not empirical campaign effects or district-opinion estimates, not a full "
			+ "A1-A9 sweep, and not evidence for real-world institutional ranking.";

	private enum MechanismVariant
	{
		SIGNAL_RELIANT(
				"signal_reliant_majority",
				"signal-reliant-majority",
				false,
				"not_applicable_no_signal_verification"
		),
		CONSTITUENT_VERIFIED(
				"constituent_verified_majority",
				"constituent-verified-majority",
				true,
				"same_case_constituent_signal_correction_computed"
		);

		private final String mechanismFamily;
		private final String scenarioStem;
		private final boolean verifiesSignal;
		private final String correctionStatus;

		MechanismVariant(
				String mechanismFamily,
				String scenarioStem,
				boolean verifiesSignal,
				String correctionStatus
		) {
			this.mechanismFamily = mechanismFamily;
			this.scenarioStem = scenarioStem;
			this.verifiesSignal = verifiesSignal;
			this.correctionStatus = correctionStatus;
		}

		String mechanismFamily() {
			return mechanismFamily;
		}

		String baselineScenario() {
			return scenarioStem + "-baseline";
		}

		String attackedScenario() {
			return scenarioStem + "-a8-distorted";
		}

		boolean verifiesSignal() {
			return verifiesSignal;
		}

		String correctionStatus() {
			return correctionStatus;
		}
	}

	private record AttackConfig(int budgetValue, InformationLevel informationLevel)
	{
		double signalShift() {
			double base = switch (informationLevel) {
				case LOW -> 0.035;
				case MEDIUM -> 0.060;
				case HIGH -> 0.085;
			};
			return Math.min(0.240, base + (0.018 * budgetValue));
		}

		double salienceBoost() {
			double base = switch (informationLevel) {
				case LOW -> 0.030;
				case MEDIUM -> 0.045;
				case HIGH -> 0.060;
			};
			return Math.min(0.180, base + (0.010 * budgetValue));
		}

		double publicCampaignSpend() {
			return 3.0 * budgetValue;
		}

		double attentionSpend() {
			return 0.45 * budgetValue;
		}

		int proxyEndorsements() {
			return budgetValue;
		}
	}

	private record AttackTarget(double direction, String key) {}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			MechanismVariant mechanism,
			AttackTarget target,
			Bill latentBill,
			Bill attackedInputBill,
			BillOutcome baseline,
			BillOutcome attacked,
			double inputSignalDistortion,
			double residualSignalDistortion,
			double targetedSignalMovement,
			double generatedSupportErrorAdded,
			double publicBenefitSignalErrorAdded,
			double publicPreferenceDistortionAdded,
			double signalCorrection,
			double correctionShare,
			double attackerResourceSpend,
			double administrativeBurdenAdded,
			boolean signalDistortionSuccess,
			boolean falseConsensusSignal,
			boolean falseOppositionSignal,
			boolean lowSupportEnactmentAdded,
			boolean popularFailureAdded,
			boolean highBenefitBlockAdded,
			boolean harmfulEnactmentAdded,
			boolean decisionFailureAdded,
			boolean success
	) {}

	private A8PublicSupportDistortionAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a8.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a8-summary.csv"), traces, runs, legislators, bills);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a8-summary.md"), traces, runs, legislators, bills);
		writeRunManifest(outputDir.resolve("adversarial-stress-a8-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a8.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a8-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a8-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a8-run-manifest.json"));
	}

	public static void runSummaryOnly(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		validateRunParameters(runs, legislators, bills);
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a8-summary.csv"), traces, runs, legislators, bills);
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a8-summary.csv"));
	}

	private static void validateRunParameters(int runs, int legislators, int bills) {
		if (runs <= 0 || legislators <= 0 || bills <= 0) {
			throw new IllegalArgumentException("Runs, legislators, and bills must all be positive.");
		}
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = publicSupportWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 8808);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (MechanismVariant mechanism : MechanismVariant.values()) {
				for (AttackConfig config : attackConfigs()) {
					LegislativeProcess baselineProcess = process(world, mechanism, "A8 truthful-signal baseline");
					LegislativeProcess attackedProcess = process(world, mechanism, "A8 distorted public-support signal");
					for (int billIndex = 0; billIndex < world.bills().size(); billIndex++) {
						Bill latentBill = world.bills().get(billIndex);
						AttackTarget target = target(latentBill, config);
						Bill attackedInputBill = attackBill(latentBill, config, target);
						long voteSeed = mix(
								seed,
								run,
								9208 + (mechanism.ordinal() * 1000) + (config.informationLevel().ordinal() * 100)
										+ (config.budgetValue() * 10) + billIndex
						);
						double statusQuo = world.initialPolicy().position();
						BillOutcome baseline = baselineProcess.consider(
								latentBill,
								new VoteContext(world.partyPositions(), new Random(voteSeed), statusQuo)
						);
						BillOutcome attacked = attackedProcess.consider(
								attackedInputBill,
								new VoteContext(world.partyPositions(), new Random(voteSeed), statusQuo)
						);
						traces.add(trace(
								run,
								worldSeed,
								billIndex,
								config,
								mechanism,
								target,
								latentBill,
								attackedInputBill,
								baseline,
								attacked
						));
					}
				}
			}
		}
		return traces;
	}

	private static WorldSpec publicSupportWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.66,
				0.66,
				0.54,
				0.62,
				0.42,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.PUBLIC_OPINION_ERROR
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			MechanismVariant mechanism,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.standard(),
				AffirmativeThresholdRule.simpleMajority()
		);
		LegislativeProcess floor = new UnicameralProcess(name + " floor", chamber);
		if (!mechanism.verifiesSignal()) {
			return floor;
		}
		return new ConstituentPublicWillProcess(
				name + " constituent verification",
				floor,
				world.legislators(),
				0.70,
				0.24
		);
	}

	private static AttackTarget target(Bill bill, AttackConfig config) {
		if (config.informationLevel() == InformationLevel.LOW) {
			return bill.publicSupport() < 0.50
					? new AttackTarget(1.0, "manufacture_threshold_consensus")
					: new AttackTarget(-1.0, "suppress_threshold_consensus");
		}
		if (config.informationLevel() == InformationLevel.MEDIUM) {
			boolean harmfulOrCaptured = bill.concentratedHarm() >= 0.38
					|| bill.privateGain() > bill.publicBenefit() + 0.12
					|| bill.lobbyPressure() > 0.42;
			if (harmfulOrCaptured) {
				return new AttackTarget(1.0, "inflate_harm_or_capture_proxy");
			}
			if (bill.publicBenefit() >= 0.56 || bill.publicSupport() >= 0.58) {
				return new AttackTarget(-1.0, "suppress_benefit_or_support_proxy");
			}
			return bill.publicSupport() < 0.50
					? new AttackTarget(1.0, "manufacture_threshold_consensus")
					: new AttackTarget(-1.0, "suppress_threshold_consensus");
		}
		double quality = (0.58 * bill.publicBenefit())
				+ (0.18 * bill.affectedGroupSupport())
				- (0.32 * bill.concentratedHarm())
				- (0.24 * Math.max(0.0, bill.privateGain() - bill.publicBenefit()));
		return quality >= 0.43
				? new AttackTarget(-1.0, "suppress_high_latent_policy_quality")
				: new AttackTarget(1.0, "inflate_low_latent_policy_quality");
	}

	private static Bill attackBill(Bill bill, AttackConfig config, AttackTarget target) {
		double revisedSupport = Values.clamp(
				bill.publicSupport() + (target.direction() * config.signalShift()),
				0.0,
				1.0
		);
		double revisedSalience = Values.clamp(bill.salience() + config.salienceBoost(), 0.0, 1.0);
		Bill revised = bill.withPublicSignal(revisedSupport, revisedSalience);
		double addedCampaignSpend = Math.min(config.publicCampaignSpend(), 100.0 - revised.publicCampaignSpend());
		revised = revised.withLobbyActivity(
				revised.lobbyPressure(),
				revised.publicSupport(),
				revised.publicBenefit(),
				revised.privateGain(),
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				addedCampaignSpend,
				0.0
		);
		double addedAttentionSpend = Math.min(config.attentionSpend(), 100.0 - revised.attentionSpend());
		return revised.withAttentionSpend(addedAttentionSpend);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			MechanismVariant mechanism,
			AttackTarget target,
			Bill latentBill,
			Bill attackedInputBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		double inputSignalDistortion = Math.abs(attackedInputBill.publicSupport() - latentBill.publicSupport());
		double residualSignalDistortion = Math.abs(attacked.bill().publicSupport() - baseline.bill().publicSupport());
		double targetedSignalMovement = target.direction()
				* (attacked.bill().publicSupport() - baseline.bill().publicSupport());
		double generatedSupportErrorAdded = Math.abs(attacked.bill().publicSupport() - latentBill.publicSupport())
				- Math.abs(baseline.bill().publicSupport() - latentBill.publicSupport());
		double publicBenefitSignalErrorAdded = Math.abs(attacked.bill().publicSupport() - latentBill.publicBenefit())
				- Math.abs(baseline.bill().publicSupport() - latentBill.publicBenefit());
		double publicPreferenceDistortionAdded = Math.abs(attacked.averageYayShare() - latentBill.publicSupport())
				- Math.abs(baseline.averageYayShare() - latentBill.publicSupport());
		double signalCorrection = inputSignalDistortion - residualSignalDistortion;
		double correctionShare = inputSignalDistortion == 0.0 ? 0.0 : signalCorrection / inputSignalDistortion;
		double attackerResourceSpend = (attackedInputBill.publicCampaignSpend() - latentBill.publicCampaignSpend())
				+ (attackedInputBill.attentionSpend() - latentBill.attentionSpend());
		double administrativeBurdenAdded = administrativeBurden(attacked) - administrativeBurden(baseline);
		boolean falseConsensusSignal = latentBill.publicSupport() < 0.50
				&& baseline.bill().publicSupport() < 0.50
				&& attacked.bill().publicSupport() >= 0.50;
		boolean falseOppositionSignal = latentBill.publicSupport() >= 0.50
				&& baseline.bill().publicSupport() >= 0.50
				&& attacked.bill().publicSupport() < 0.50;
		boolean lowSupportEnactmentAdded = !baseline.enacted()
				&& attacked.enacted()
				&& latentBill.publicSupport() < 0.50;
		boolean popularFailureAdded = baseline.enacted()
				&& !attacked.enacted()
				&& latentBill.publicSupport() >= 0.50;
		boolean highBenefitBlockAdded = baseline.enacted()
				&& !attacked.enacted()
				&& latentBill.publicBenefit() >= 0.56;
		boolean harmfulEnactmentAdded = !baseline.enacted()
				&& attacked.enacted()
				&& (latentBill.concentratedHarm() >= 0.38
						|| latentBill.privateGain() > latentBill.publicBenefit() + 0.12
						|| latentBill.publicBenefit() < 0.44);
		boolean decisionFailureAdded = lowSupportEnactmentAdded
				|| popularFailureAdded
				|| highBenefitBlockAdded
				|| harmfulEnactmentAdded;
		boolean signalDistortionSuccess = targetedSignalMovement >= 0.040
				&& generatedSupportErrorAdded >= 0.020;
		boolean success = signalDistortionSuccess || decisionFailureAdded;
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				mechanism,
				target,
				latentBill,
				attackedInputBill,
				baseline,
				attacked,
				inputSignalDistortion,
				residualSignalDistortion,
				targetedSignalMovement,
				generatedSupportErrorAdded,
				publicBenefitSignalErrorAdded,
				publicPreferenceDistortionAdded,
				signalCorrection,
				correctionShare,
				attackerResourceSpend,
				administrativeBurdenAdded,
				signalDistortionSuccess,
				falseConsensusSignal,
				falseOppositionSignal,
				lowSupportEnactmentAdded,
				popularFailureAdded,
				highBenefitBlockAdded,
				harmfulEnactmentAdded,
				decisionFailureAdded,
				success
		);
	}

	private static List<AttackConfig> attackConfigs() {
		List<AttackConfig> configs = new ArrayList<>();
		for (InformationLevel level : List.of(InformationLevel.LOW, InformationLevel.MEDIUM, InformationLevel.HIGH)) {
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
		jsonProperty(builder, "scenarioKey", trace.mechanism().attackedScenario(), true);
		jsonProperty(builder, "baselineScenarioKey", trace.mechanism().baselineScenario(), true);
		jsonProperty(builder, "mechanismFamily", trace.mechanism().mechanismFamily(), true);
		jsonProperty(builder, "adversaryId", ADVERSARY_ID, true);
		jsonProperty(builder, "actorType", spec.actorType(), true);
		jsonProperty(builder, "objective", spec.objective(), true);
		jsonProperty(builder, "budgetUnit", BUDGET_UNIT, true);
		jsonProperty(builder, "budgetValue", Integer.toString(trace.config().budgetValue()), false);
		jsonProperty(builder, "informationLevel", trace.config().informationLevel().key(), true);
		jsonArray(builder, "attackActionList", actionList(trace));
		jsonObject(builder, "preAttackFeatures", billJson(trace.latentBill(), trace.latentBill()));
		jsonObject(builder, "attackedInputFeatures", billJson(trace.attackedInputBill(), trace.latentBill()));
		jsonObject(builder, "postAttackFeatures", billJson(trace.attacked().bill(), trace.latentBill()));
		jsonObject(builder, "institutionalPath", pathJson(trace));
		jsonObject(builder, "baselineOutcome", outcomeJson(trace.baseline(), trace.latentBill()));
		jsonObject(builder, "attackedOutcome", outcomeJson(trace.attacked(), trace.latentBill()));
		jsonProperty(builder, "successFlag", Boolean.toString(trace.success()), false);
		jsonObject(builder, "metricDeltas", metricDeltaJson(trace));
		jsonObject(builder, "administrativeBurden", administrativeBurdenJson(trace));
		jsonObject(builder, "correctionMetrics", correctionMetricsJson(trace));
		jsonProperty(builder, "recoveryStatus", trace.mechanism().correctionStatus(), true);
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
			int bills
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessCount,attackSuccessRate,signalDistortionSuccessRate,decisionFailureAddedRate,meanInputSignalDistortion,meanResidualSignalDistortion,medianResidualSignalDistortion,worstResidualSignalDistortion,meanGeneratedSupportErrorAdded,medianGeneratedSupportErrorAdded,worstGeneratedSupportErrorAdded,meanPublicBenefitSignalErrorAdded,worstPublicBenefitSignalErrorAdded,meanPublicPreferenceDistortionAdded,worstPublicPreferenceDistortionAdded,meanSignalCorrection,meanCorrectionShare,falseConsensusSignalRate,falseOppositionSignalRate,lowSupportEnactmentAddedRate,popularFailureAddedRate,highBenefitBlockAddedRate,harmfulEnactmentAddedRate,meanAttackerResourceSpend,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (MechanismVariant mechanism : MechanismVariant.values()) {
			for (AttackConfig config : attackConfigs()) {
				List<TraceRow> group = group(traces, mechanism, config);
				builder.append(csv(ADVERSARY_ID)).append(',')
				       .append(csv("public_support_distortion")).append(',')
				       .append(csv(CASE_KEY)).append(',')
				       .append(csv(mechanism.baselineScenario())).append(',')
				       .append(csv(mechanism.attackedScenario())).append(',')
				       .append(csv(mechanism.mechanismFamily())).append(',')
				       .append(csv(BUDGET_UNIT)).append(',')
				       .append(config.budgetValue()).append(',')
				       .append(csv(config.informationLevel().key())).append(',')
				       .append(runs).append(',')
				       .append(legislators).append(',')
				       .append(bills).append(',')
				       .append(group.size()).append(',')
				       .append(group.stream().filter(TraceRow::success).count()).append(',')
				       .append(format(rate(group, TraceRow::success))).append(',')
				       .append(format(rate(group, TraceRow::signalDistortionSuccess))).append(',')
				       .append(format(rate(group, TraceRow::decisionFailureAdded))).append(',')
				       .append(format(mean(group, TraceRow::inputSignalDistortion))).append(',')
				       .append(format(mean(group, TraceRow::residualSignalDistortion))).append(',')
				       .append(format(median(group, TraceRow::residualSignalDistortion))).append(',')
				       .append(format(max(group, TraceRow::residualSignalDistortion))).append(',')
				       .append(format(mean(group, TraceRow::generatedSupportErrorAdded))).append(',')
				       .append(format(median(group, TraceRow::generatedSupportErrorAdded))).append(',')
				       .append(format(max(group, TraceRow::generatedSupportErrorAdded))).append(',')
				       .append(format(mean(group, TraceRow::publicBenefitSignalErrorAdded))).append(',')
				       .append(format(max(group, TraceRow::publicBenefitSignalErrorAdded))).append(',')
				       .append(format(mean(group, TraceRow::publicPreferenceDistortionAdded))).append(',')
				       .append(format(max(group, TraceRow::publicPreferenceDistortionAdded))).append(',')
				       .append(format(mean(group, TraceRow::signalCorrection))).append(',')
				       .append(format(mean(group, TraceRow::correctionShare))).append(',')
				       .append(format(rate(group, TraceRow::falseConsensusSignal))).append(',')
				       .append(format(rate(group, TraceRow::falseOppositionSignal))).append(',')
				       .append(format(rate(group, TraceRow::lowSupportEnactmentAdded))).append(',')
				       .append(format(rate(group, TraceRow::popularFailureAdded))).append(',')
				       .append(format(rate(group, TraceRow::highBenefitBlockAdded))).append(',')
				       .append(format(rate(group, TraceRow::harmfulEnactmentAdded))).append(',')
				       .append(format(mean(group, TraceRow::attackerResourceSpend))).append(',')
				       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(',')
				       .append(format(max(group, TraceRow::administrativeBurdenAdded))).append(',')
				       .append(csv(mechanism.correctionStatus())).append(',')
				       .append(csv(TRACE_ARTIFACT)).append(',')
				       .append(csv(CLAIM_BOUNDARY)).append('\n');
			}
		}
		Files.writeString(path, builder.toString());
	}

	private static void writeSummaryMarkdown(
			Path path,
			List<TraceRow> traces,
			int runs,
			int legislators,
			int bills
	) throws IOException {
		StringBuilder builder = new StringBuilder();
		builder.append("# A8 Public-Support Distortion Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a8_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A8 public-support distortion actor\n");
		builder.append("- Same-world, same-bill, same-status-quo, same-vote-random runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Mechanism paths: signal-reliant majority; constituent-verified majority\n");
		builder.append("- Budget/information cells per path: 9\n");
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- A3 boundary: no objection window or citizen panel is used in either A8 path\n");
		builder.append("- Correction metric: same-case signal attenuation by constituent verification, not post-enactment recovery\n\n");
		builder.append("| Mechanism | Information | Budget | Rows | Success | Decision failure added | Median residual distortion | Worst support error added | Mean correction share | False consensus | False opposition | Low-support enactment | Popular failure |\n");
		builder.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (MechanismVariant mechanism : MechanismVariant.values()) {
			for (AttackConfig config : attackConfigs()) {
				List<TraceRow> group = group(traces, mechanism, config);
				builder.append("| ").append(mechanism.mechanismFamily()).append(" | ")
				       .append(config.informationLevel().key()).append(" | ")
				       .append(config.budgetValue()).append(" | ")
				       .append(group.size()).append(" | ")
				       .append(format(rate(group, TraceRow::success))).append(" | ")
				       .append(format(rate(group, TraceRow::decisionFailureAdded))).append(" | ")
				       .append(format(median(group, TraceRow::residualSignalDistortion))).append(" | ")
				       .append(format(max(group, TraceRow::generatedSupportErrorAdded))).append(" | ")
				       .append(format(mean(group, TraceRow::correctionShare))).append(" | ")
				       .append(format(rate(group, TraceRow::falseConsensusSignal))).append(" | ")
				       .append(format(rate(group, TraceRow::falseOppositionSignal))).append(" | ")
				       .append(format(rate(group, TraceRow::lowSupportEnactmentAdded))).append(" | ")
				       .append(format(rate(group, TraceRow::popularFailureAdded))).append(" |\n");
			}
		}
		builder.append("\nGate status: this supplies the first bounded A8 direct signal-distortion and same-case correction pilot, but the robustness breakout remains below manuscript gate because broad mechanism coverage, multi-seed replication, temporal recovery/correction, and external validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a8-run-v0", true);
		property(builder, 1, "status", "partial_a8_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "summaryRows", Integer.toString(MechanismVariant.values().length * attackConfigs().size()), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		property(builder, 1, "pairingDesign", "same_world_same_bill_same_status_quo_same_vote_random", true);
		arrayProperty(builder, 1, "mechanismFamilies", List.of(
				MechanismVariant.SIGNAL_RELIANT.mechanismFamily(),
				MechanismVariant.CONSTITUENT_VERIFIED.mechanismFamily()
		), true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a8-summary.csv",
				"reports/adversarial-stress-a8-summary.md",
				TRACE_ARTIFACT
		), true);
		property(builder, 1, "claimBoundary", CLAIM_BOUNDARY, true);
		builder.append("\t\"gateStatus\": \"not_manuscript_ready\"\n");
		builder.append("}\n");
		Files.writeString(path, builder.toString());
	}

	private static List<TraceRow> group(
			List<TraceRow> traces,
			MechanismVariant mechanism,
			AttackConfig config
	) {
		return traces.stream()
		             .filter(trace -> trace.mechanism() == mechanism && trace.config().equals(config))
		             .toList();
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

	private static double administrativeBurden(BillOutcome outcome) {
		OutcomeSignals signals = outcome.signals();
		return (0.050 * outcome.bill().attentionSpend())
				+ (0.120 * signals.publicWillReviews())
				+ (0.060 * signals.publicSignalMovement());
	}

	private static List<String> actionList(TraceRow trace) {
		List<String> actions = new ArrayList<>();
		for (int i = 0; i < trace.config().budgetValue(); i++) {
			actions.add("deploy_public_campaign_unit");
		}
		actions.add("amplify_distorted_salience");
		actions.add(trace.target().key());
		for (int i = 0; i < trace.config().proxyEndorsements(); i++) {
			actions.add("route_proxy_endorsement");
		}
		switch (trace.config().informationLevel()) {
			case LOW -> actions.add("use_visible_threshold_scan");
			case MEDIUM -> actions.add("use_support_harm_and_capture_proxies");
			case HIGH -> actions.add("target_latent_policy_quality");
		}
		return actions;
	}

	private static String billJson(Bill bill, Bill latentBill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"observablePublicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"generatedPublicSupport\":" + format(latentBill.publicSupport()) + ","
				+ "\"supportSignalError\":" + format(Math.abs(bill.publicSupport() - latentBill.publicSupport())) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"affectedGroupSupport\":" + format(bill.affectedGroupSupport()) + ","
				+ "\"concentratedHarm\":" + format(bill.concentratedHarm()) + ","
				+ "\"privateGain\":" + format(bill.privateGain()) + ","
				+ "\"salience\":" + format(bill.salience()) + ","
				+ "\"publicSignalMovement\":" + format(bill.publicSignalMovement()) + ","
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

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"mechanismFamily\":\"" + trace.mechanism().mechanismFamily() + "\","
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(trace.attacked().finalReason()) + "\","
				+ "\"baselinePublicWillReviews\":" + trace.baseline().signals().publicWillReviews() + ","
				+ "\"attackedPublicWillReviews\":" + trace.attacked().signals().publicWillReviews() + ","
				+ "\"baselineObjectionWindows\":" + trace.baseline().signals().objectionWindows() + ","
				+ "\"attackedObjectionWindows\":" + trace.attacked().signals().objectionWindows() + ","
				+ "\"baselineCitizenReviews\":" + trace.baseline().signals().citizenReviews() + ","
				+ "\"attackedCitizenReviews\":" + trace.attacked().signals().citizenReviews() + ","
				+ "\"baselineFinalPublicSupport\":" + format(trace.baseline().bill().publicSupport()) + ","
				+ "\"attackedInputPublicSupport\":" + format(trace.attackedInputBill().publicSupport()) + ","
				+ "\"attackedFinalPublicSupport\":" + format(trace.attacked().bill().publicSupport()) + ","
				+ "\"baselineYayShare\":" + format(trace.baseline().averageYayShare()) + ","
				+ "\"attackedYayShare\":" + format(trace.attacked().averageYayShare())
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"inputSignalDistortion\":" + format(trace.inputSignalDistortion()) + ","
				+ "\"residualSignalDistortion\":" + format(trace.residualSignalDistortion()) + ","
				+ "\"targetedSignalMovement\":" + format(trace.targetedSignalMovement()) + ","
				+ "\"generatedSupportErrorAdded\":" + format(trace.generatedSupportErrorAdded()) + ","
				+ "\"publicBenefitSignalErrorAdded\":" + format(trace.publicBenefitSignalErrorAdded()) + ","
				+ "\"publicPreferenceDistortionAdded\":" + format(trace.publicPreferenceDistortionAdded()) + ","
				+ "\"signalDistortionSuccess\":" + trace.signalDistortionSuccess() + ","
				+ "\"falseConsensusSignal\":" + trace.falseConsensusSignal() + ","
				+ "\"falseOppositionSignal\":" + trace.falseOppositionSignal() + ","
				+ "\"lowSupportEnactmentAdded\":" + trace.lowSupportEnactmentAdded() + ","
				+ "\"popularFailureAdded\":" + trace.popularFailureAdded() + ","
				+ "\"highBenefitBlockAdded\":" + trace.highBenefitBlockAdded() + ","
				+ "\"harmfulEnactmentAdded\":" + trace.harmfulEnactmentAdded() + ","
				+ "\"decisionFailureAdded\":" + trace.decisionFailureAdded() + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline())) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attacked())) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"attackerResourceSpend\":" + format(trace.attackerResourceSpend()) + ","
				+ "\"baselinePublicWillReviews\":" + trace.baseline().signals().publicWillReviews() + ","
				+ "\"attackedPublicWillReviews\":" + trace.attacked().signals().publicWillReviews()
				+ "}";
	}

	private static String correctionMetricsJson(TraceRow trace) {
		return "{"
				+ "\"correctionStatus\":\"" + trace.mechanism().correctionStatus() + "\","
				+ "\"inputSignalDistortion\":" + format(trace.inputSignalDistortion()) + ","
				+ "\"residualSignalDistortion\":" + format(trace.residualSignalDistortion()) + ","
				+ "\"signalCorrection\":" + format(trace.signalCorrection()) + ","
				+ "\"correctionShare\":" + format(trace.correctionShare())
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
		return String.format(Locale.ROOT, "%.6f", value);
	}
}
