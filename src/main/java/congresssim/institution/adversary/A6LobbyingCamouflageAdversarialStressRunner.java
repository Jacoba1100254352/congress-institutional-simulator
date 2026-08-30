package congresssim.institution.adversary;


import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategies;
import congresssim.institution.agenda.ProposalAccessProcess;
import congresssim.institution.agenda.ProposalAccessRules;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.lobbying.InfluenceSystemProcess;
import congresssim.institution.lobbying.LobbyAuditProcess;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.model.Bill;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
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
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;


public final class A6LobbyingCamouflageAdversarialStressRunner
{
	private static final String ADVERSARY_ID = "A6";
	private static final String CASE_KEY = "lobbying-camouflage-pressure";
	private static final String MECHANISM_FAMILY = "anti_capture_public_interest_influence_system";
	private static final String BASELINE_SCENARIO = "anti-capture-visible-lobbying-baseline";
	private static final String ATTACK_SCENARIO = "anti-capture-a6-lobbying-camouflage";
	private static final String BUDGET_UNIT = "camouflage_units";
	private static final String TRACE_ARTIFACT = "reports/adversarial-failure-traces-a6.jsonl";
	private static final double CAPTURED_LATENT_RISK_THRESHOLD = 0.56;
	private static final String CLAIM_BOUNDARY =
			"A6 executable pilot only. Rows use same generated worlds and bill ids for synthetic latent "
			+ "capture targets under a transparent anti-capture influence-system baseline and a camouflaged "
			+ "proxy/shadow-lobbying attack. Latent capture risk is traced separately from observed screen "
			+ "risk. This is not an empirical campaign-finance, lobbying-disclosure, or proxy-sponsorship "
			+ "estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional "
			+ "ranking.";

	private record AttackConfig(int budgetValue, InformationLevel informationLevel) {
		String key() {
			return informationLevel.key() + "-budget-" + budgetValue;
		}

		int proxySponsors() {
			int bonus = informationLevel == InformationLevel.HIGH ? 1 : 0;
			return Math.min(9, Math.max(1, budgetValue + bonus));
		}

		double issueFramingShift() {
			double base = informationLevel == InformationLevel.HIGH ? 0.120 : 0.080;
			double slope = informationLevel == InformationLevel.HIGH ? 0.045 : 0.035;
			return Math.min(informationLevel == InformationLevel.HIGH ? 0.420 : 0.320, base + (slope * budgetValue));
		}

		double visiblePressureMultiplier() {
			double base = informationLevel == InformationLevel.HIGH ? 0.500 : 0.620;
			double slope = informationLevel == InformationLevel.HIGH ? 0.065 : 0.055;
			return Math.max(informationLevel == InformationLevel.HIGH ? 0.100 : 0.220, base - (slope * budgetValue));
		}

		double reportedPrivateGainMultiplier() {
			double base = informationLevel == InformationLevel.HIGH ? 0.700 : 0.780;
			double slope = informationLevel == InformationLevel.HIGH ? 0.050 : 0.040;
			return Math.max(informationLevel == InformationLevel.HIGH ? 0.320 : 0.450, base - (slope * budgetValue));
		}

		double shadowLobbyTolerance() {
			double base = informationLevel == InformationLevel.HIGH ? 0.460 : 0.360;
			double slope = informationLevel == InformationLevel.HIGH ? 0.060 : 0.050;
			return Math.min(informationLevel == InformationLevel.HIGH ? 0.860 : 0.700, base + (slope * budgetValue));
		}

		double disclosureEnforcement() {
			double base = informationLevel == InformationLevel.HIGH ? 0.300 : 0.420;
			return Math.max(0.120, base - (0.025 * budgetValue));
		}

		double watchdogCapacity() {
			double base = informationLevel == InformationLevel.HIGH ? 0.360 : 0.500;
			return Math.max(0.160, base - (0.030 * budgetValue));
		}

		double publicMatchingStrength() {
			return informationLevel == InformationLevel.HIGH ? 0.120 : 0.180;
		}

		double spendScale() {
			double base = informationLevel == InformationLevel.HIGH ? 0.760 : 0.620;
			double slope = informationLevel == InformationLevel.HIGH ? 0.110 : 0.090;
			return Math.min(1.60, base + (slope * budgetValue));
		}
	}

	private record TraceRow(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill latentBill,
			Bill camouflagedBill,
			BillOutcome baseline,
			BillOutcome attacked,
			double latentCaptureRisk,
			double baselineObservedScreenRisk,
			double attackedObservedScreenRisk,
			double observedScreenRiskDecline,
			double baselineShadowShare,
			double attackedShadowShare,
			double shadowShareAdded,
			double baselineDetectionRate,
			double attackedDetectionRate,
			double watchdogDetectionDecline,
			double visibleSpendDecline,
			double captureEnactmentAdded,
			double privateGainPersistence,
			double administrativeBurdenAdded,
			boolean antiCaptureBypass,
			boolean visibleSpendDeclineWithCapturePersistence,
			boolean success
	) {}

	private A6LobbyingCamouflageAdversarialStressRunner() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		run(outputDir, 5, 101, 60, 20260428L);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		Files.createDirectories(outputDir);
		List<TraceRow> traces = runTraces(runs, legislators, bills, seed);
		writeTraceJsonl(outputDir.resolve("adversarial-failure-traces-a6.jsonl"), traces, runs, legislators, bills, seed);
		writeSummaryCsv(outputDir.resolve("adversarial-stress-a6-summary.csv"), traces, runs, legislators, bills, seed);
		writeSummaryMarkdown(outputDir.resolve("adversarial-stress-a6-summary.md"), traces, runs, legislators, bills, seed);
		writeRunManifest(outputDir.resolve("adversarial-stress-a6-run-manifest.json"), traces, runs, legislators, bills, seed);
		System.out.println("Wrote " + outputDir.resolve("adversarial-failure-traces-a6.jsonl"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a6-summary.csv"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a6-summary.md"));
		System.out.println("Wrote " + outputDir.resolve("adversarial-stress-a6-run-manifest.json"));
	}

	private static List<TraceRow> runTraces(int runs, int legislators, int bills, long seed) {
		WorldGenerator generator = new WorldGenerator();
		WorldSpec worldSpec = camouflageWorldSpec(legislators, bills);
		List<TraceRow> traces = new ArrayList<>();
		for (int run = 0; run < runs; run++) {
			long worldSeed = mix(seed, run, 6706);
			SimulationWorld world = generator.generate(worldSpec, worldSeed);
			for (AttackConfig config : attackConfigs()) {
				List<Bill> worldBills = world.bills();
				for (int billIndex = 0; billIndex < worldBills.size(); billIndex++) {
					Random caseRandom = new Random(mix(seed, run, 7106 + (config.budgetValue() * 17) + billIndex));
					Bill latentBill = latentCaptureBill(worldBills.get(billIndex), caseRandom, billIndex);
					Bill camouflagedBill = camouflagedBill(latentBill, config, caseRandom);
					BillOutcome baseline = baselineProcess(world, latentBill, config).consider(
							latentBill,
							new VoteContext(world.partyPositions(), new Random(mix(seed, run, 7506 + billIndex)), 0.0)
					);
					BillOutcome attacked = attackedProcess(world, camouflagedBill, config).consider(
							camouflagedBill,
							new VoteContext(world.partyPositions(), new Random(mix(seed, run, 7506 + billIndex)), 0.0)
					);
					traces.add(trace(run, worldSeed, billIndex, config, latentBill, camouflagedBill, baseline, attacked));
				}
			}
		}
		return traces;
	}

	private static WorldSpec camouflageWorldSpec(int legislators, int bills) {
		return new WorldSpec(
				legislators,
				bills,
				4,
				0.68,
				0.64,
				0.82,
				0.44,
				0.38,
				PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
				1.0,
				ProposalShockProfile.BASELINE
		);
	}

	private static LegislativeProcess baselineProcess(SimulationWorld world, Bill bill, AttackConfig config) {
		return process(
				world,
				baselineLobbyGroups(bill, config),
				0.800,
				0.640,
				0.780,
				0.140,
				"A6 transparent anti-capture baseline"
		);
	}

	private static LegislativeProcess attackedProcess(SimulationWorld world, Bill bill, AttackConfig config) {
		return process(
				world,
				camouflageLobbyGroups(bill, config),
				config.disclosureEnforcement(),
				config.publicMatchingStrength(),
				config.watchdogCapacity(),
				config.shadowLobbyTolerance(),
				"A6 camouflaged proxy/shadow lobbying process"
		);
	}

	private static LegislativeProcess process(
			SimulationWorld world,
			List<LobbyGroup> lobbyGroups,
			double disclosureEnforcement,
			double publicMatchingStrength,
			double watchdogCapacity,
			double shadowLobbyTolerance,
			String name
	) {
		Chamber chamber = new Chamber(
				"Congress",
				world.legislators(),
				VotingStrategies.antiCapture(),
				AffirmativeThresholdRule.simpleMajority()
		);
		LegislativeProcess process = new UnicameralProcess(name + " floor", chamber);
		process = new LobbyAuditProcess(name, process, 0.10, 0.72, 0.45, 0.55, true);
		process = new ProposalAccessProcess(
				name,
				ProposalAccessRules.publicInterestScreen(0.50, 0.58, 2.35, 0.56),
				process
		);
		return new InfluenceSystemProcess(
				name,
				process,
				lobbyGroups,
				disclosureEnforcement,
				publicMatchingStrength,
				watchdogCapacity,
				shadowLobbyTolerance
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

	private static Bill latentCaptureBill(Bill anchor, Random random, int billIndex) {
		double direction = Math.signum(anchor.proposerIdeology() == 0.0 ? random.nextGaussian() : anchor.proposerIdeology());
		if (direction == 0.0) {
			direction = random.nextBoolean() ? 1.0 : -1.0;
		}
		double ideology = Values.clamp((0.35 * anchor.ideologyPosition()) + (0.34 * direction) + (random.nextGaussian() * 0.08), -1.0, 1.0);
		double support = Values.clamp(0.300 + (0.120 * anchor.publicSupport()) + (random.nextGaussian() * 0.045), 0.18, 0.50);
		double benefit = Values.clamp(0.180 + (0.180 * anchor.publicBenefit()) + (random.nextGaussian() * 0.050), 0.08, 0.46);
		double lobbyPressure = Values.clamp(0.680 + (0.130 * Math.max(0.0, anchor.lobbyPressure())) + (random.nextGaussian() * 0.060), 0.50, 0.96);
		double salience = Values.clamp(0.680 + (0.180 * anchor.salience()) + (random.nextGaussian() * 0.060), 0.48, 0.98);
		double privateGain = Values.clamp(0.700 + (0.180 * anchor.privateGain()) + (random.nextGaussian() * 0.055), 0.56, 0.98);
		double affectedSupport = Values.clamp(support - 0.10 + (random.nextGaussian() * 0.055), 0.04, 0.55);
		double harm = Values.clamp(0.360 + (0.120 * privateGain) + (random.nextGaussian() * 0.070), 0.10, 0.88);
		double compensationCost = Values.clamp(0.080 + (0.180 * harm), 0.0, 1.0);
		Bill bill = new Bill(
				anchor.id(),
				"A6 Latent Capture Target " + (billIndex + 1),
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
		return bill.withPublicBenefitUncertainty(Values.clamp(0.300 + random.nextGaussian() * 0.100, 0.0, 1.0));
	}

	private static Bill camouflagedBill(Bill latentBill, AttackConfig config, Random random) {
		double revisedPressure = Values.clamp(latentBill.lobbyPressure() * config.visiblePressureMultiplier(), -1.0, 1.0);
		double revisedSupport = Values.clamp(
				latentBill.publicSupport() + (0.58 * config.issueFramingShift()) + (random.nextGaussian() * 0.030),
				0.0,
				1.0
		);
		double revisedBenefit = Values.clamp(
				latentBill.publicBenefit() + (0.48 * config.issueFramingShift()) + (random.nextGaussian() * 0.028),
				0.0,
				1.0
		);
		double revisedPrivateGain = Values.clamp(
				latentBill.privateGain() * config.reportedPrivateGainMultiplier(),
				0.0,
				1.0
		);
		double revisedSalience = Values.clamp(latentBill.salience() + (0.35 * config.issueFramingShift()), 0.0, 1.0);
		Bill bill = latentBill.withLobbyActivity(
				revisedPressure,
				revisedSupport,
				revisedBenefit,
				revisedPrivateGain,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0,
				0.0
		);
		bill = bill.withPublicSignal(revisedSupport, revisedSalience);
		return bill.withCosponsorship(
				           latentBill.cosponsorCount() + (2 * config.proxySponsors()),
				           latentBill.outsideBlocCosponsorCount() + config.proxySponsors(),
				           false
		           )
		           .withAttentionSpend(0.040 * config.proxySponsors());
	}

	private static List<LobbyGroup> baselineLobbyGroups(Bill bill, AttackConfig config) {
		List<LobbyGroup> groups = new ArrayList<>();
		groups.add(lobbyGroup("A6-visible-primary", bill, 2.20 + (0.18 * config.budgetValue()), LobbyCaptureStrategy.DIRECT_PRESSURE, 0.82, 0.72));
		groups.add(lobbyGroup("A6-visible-information", bill, 1.60 + (0.12 * config.budgetValue()), LobbyCaptureStrategy.INFORMATION_DISTORTION, 0.76, 0.66));
		return groups;
	}

	private static List<LobbyGroup> camouflageLobbyGroups(Bill bill, AttackConfig config) {
		List<LobbyGroup> groups = new ArrayList<>();
		int proxySponsors = config.proxySponsors();
		double totalBudget = Math.min(9.20, (1.60 + (0.42 * config.budgetValue())) * config.spendScale());
		double budgetPerProxy = Math.min(3.20, totalBudget / proxySponsors);
		for (int i = 0; i < proxySponsors; i++) {
			LobbyCaptureStrategy strategy = switch (i % 4) {
				case 0 -> LobbyCaptureStrategy.INFORMATION_DISTORTION;
				case 1 -> LobbyCaptureStrategy.AGENDA_ACCESS;
				case 2 -> LobbyCaptureStrategy.PUBLIC_CAMPAIGN;
				default -> LobbyCaptureStrategy.BALANCED;
			};
			double intensity = config.informationLevel() == InformationLevel.HIGH ? 0.88 : 0.78;
			double bias = config.informationLevel() == InformationLevel.HIGH ? 0.90 : 0.78;
			groups.add(lobbyGroup("A6-proxy-" + config.key() + "-" + (i + 1), bill, budgetPerProxy, strategy, intensity, bias));
		}
		return groups;
	}

	private static LobbyGroup lobbyGroup(
			String id,
			Bill bill,
			double budget,
			LobbyCaptureStrategy strategy,
			double influenceIntensity,
			double informationBias
	) {
		Map<String, Double> preferences = new LinkedHashMap<>();
		preferences.put(bill.issueDomain(), 1.0);
		preferences.put("general", 0.42);
		return new LobbyGroup(
				id,
				bill.issueDomain(),
				preferences,
				Values.clamp(bill.ideologyPosition() + (0.12 * Math.signum(bill.ideologyPosition())), -1.0, 1.0),
				Values.clamp(budget, 0.0, 10.0),
				Values.clamp(influenceIntensity, 0.0, 1.0),
				0.70,
				Values.clamp(informationBias, 0.0, 1.0),
				0.76,
				strategy,
				0.44
		);
	}

	private static TraceRow trace(
			int runIndex,
			long worldSeed,
			int billIndex,
			AttackConfig config,
			Bill latentBill,
			Bill camouflagedBill,
			BillOutcome baseline,
			BillOutcome attacked
	) {
		double latentCaptureRisk = LobbyCaptureScoring.captureRisk(latentBill);
		double baselineObservedScreenRisk = LobbyCaptureScoring.captureRisk(latentBill);
		double attackedObservedScreenRisk = LobbyCaptureScoring.captureRisk(camouflagedBill);
		double observedScreenRiskDecline = baselineObservedScreenRisk - attackedObservedScreenRisk;
		double baselineShadowShare = signal(baseline, "shadowLobbyingShare");
		double attackedShadowShare = signal(attacked, "shadowLobbyingShare");
		double shadowShareAdded = attackedShadowShare - baselineShadowShare;
		double baselineDetectionRate = signal(baseline, "watchdogDetectionRate");
		double attackedDetectionRate = signal(attacked, "watchdogDetectionRate");
		double watchdogDetectionDecline = baselineDetectionRate - attackedDetectionRate;
		double visibleSpendDecline = visibleSpend(baseline) - visibleSpend(attacked);
		double captureEnactmentAdded = capturedEnacted(attacked, latentBill) - capturedEnacted(baseline, latentBill);
		double privateGainPersistence = attacked.bill().privateGain() - latentBill.privateGain();
		double administrativeBurdenAdded = administrativeBurden(attacked, config, true) - administrativeBurden(baseline, config, false);
		boolean antiCaptureBypass = antiCaptureBlocked(baseline)
				&& capturedEnacted(attacked, latentBill) > 0.0
				&& latentCaptureRisk >= CAPTURED_LATENT_RISK_THRESHOLD;
		boolean visibleSpendDeclineWithCapturePersistence = visibleSpendDecline > 0.050
				&& capturedEnacted(attacked, latentBill) > 0.0
				&& attacked.bill().privateGain() >= 0.50;
		boolean success = antiCaptureBypass
				|| visibleSpendDeclineWithCapturePersistence
				|| (capturedEnacted(attacked, latentBill) > capturedEnacted(baseline, latentBill)
				&& (shadowShareAdded > 0.120 || observedScreenRiskDecline > 0.100));
		return new TraceRow(
				runIndex,
				worldSeed,
				billIndex,
				config,
				latentBill,
				camouflagedBill,
				baseline,
				attacked,
				latentCaptureRisk,
				baselineObservedScreenRisk,
				attackedObservedScreenRisk,
				observedScreenRiskDecline,
				baselineShadowShare,
				attackedShadowShare,
				shadowShareAdded,
				baselineDetectionRate,
				attackedDetectionRate,
				watchdogDetectionDecline,
				visibleSpendDecline,
				captureEnactmentAdded,
				privateGainPersistence,
				administrativeBurdenAdded,
				antiCaptureBypass,
				visibleSpendDeclineWithCapturePersistence,
				success
		);
	}

	private static boolean antiCaptureBlocked(BillOutcome outcome) {
		return !outcome.enacted()
				&& (outcome.agendaDisposition() == congresssim.institution.agenda.AgendaDisposition.ACCESS_DENIED
				|| outcome.finalReason().contains("anti-capture")
				|| outcome.finalReason().contains("public-interest screen"));
	}

	private static double capturedEnacted(BillOutcome outcome, Bill latentBill) {
		if (!outcome.enacted()) {
			return 0.0;
		}
		boolean latentCaptured = LobbyCaptureScoring.captureRisk(latentBill) >= CAPTURED_LATENT_RISK_THRESHOLD;
		boolean postCapture = LobbyCaptureScoring.captureRisk(outcome.bill()) >= 0.42
				|| outcome.bill().privateGain() >= 0.50
				|| LobbyCaptureScoring.publicInterestScore(outcome.bill()) < 0.50;
		return latentCaptured && postCapture ? 1.0 : 0.0;
	}

	private static double administrativeBurden(BillOutcome outcome, AttackConfig config, boolean attacked) {
		double shadowShare = signal(outcome, "shadowLobbyingShare");
		double detectionRate = signal(outcome, "watchdogDetectionRate");
		double proxyBurden = attacked ? (0.035 * config.proxySponsors()) + (0.300 * config.issueFramingShift()) : 0.0;
		return proxyBurden
				+ (0.080 * outcome.bill().attentionSpend())
				+ (0.040 * outcome.bill().lobbySpend())
				+ (0.220 * shadowShare * (1.0 - detectionRate));
	}

	private static double visibleSpend(BillOutcome outcome) {
		return outcome.bill().lobbySpend() * (1.0 - signal(outcome, "shadowLobbyingShare"));
	}

	private static double hiddenSpend(BillOutcome outcome) {
		return outcome.bill().lobbySpend() * signal(outcome, "shadowLobbyingShare");
	}

	private static double signal(BillOutcome outcome, String key) {
		return outcome.signals().supplementalMetrics().getOrDefault(key, 0.0);
	}

	private static long mix(long seed, int run, int stream) {
		long value = seed;
		value ^= 0x9E3779B97F4A7C15L + ((long) run << 6) + ((long) run >> 2);
		value ^= 0xBF58476D1CE4E5B9L * (stream + 37L);
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
		jsonObject(builder, "preAttackFeatures", preAttackJson(trace));
		jsonObject(builder, "postAttackFeatures", postAttackJson(trace));
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
		builder.append("adversaryId,attackFamily,caseKey,baselineScenario,attackedScenario,mechanismFamily,budgetUnit,budgetValue,informationLevel,runs,legislators,baseBillsPerRun,traceRows,attackSuccessRate,antiCaptureBypassRate,captureEnactmentAddedRate,visibleSpendDeclineWithCapturePersistenceRate,meanLatentCaptureRisk,meanObservedScreenRiskDecline,meanShadowShareAdded,meanWatchdogDetectionDecline,meanVisibleSpendDecline,meanProxySponsors,meanPrivateGainPersistence,meanAdministrativeBurdenAdded,worstAdministrativeBurdenAdded,recoveryStatus,traceArtifact,claimBoundary\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append(csv(ADVERSARY_ID)).append(',')
			       .append(csv("lobbying_camouflage")).append(',')
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
			       .append(format(rate(group, TraceRow::antiCaptureBypass))).append(',')
			       .append(format(rate(group, row -> row.captureEnactmentAdded() > 0.0))).append(',')
			       .append(format(rate(group, TraceRow::visibleSpendDeclineWithCapturePersistence))).append(',')
			       .append(format(mean(group, TraceRow::latentCaptureRisk))).append(',')
			       .append(format(mean(group, TraceRow::observedScreenRiskDecline))).append(',')
			       .append(format(mean(group, TraceRow::shadowShareAdded))).append(',')
			       .append(format(mean(group, TraceRow::watchdogDetectionDecline))).append(',')
			       .append(format(mean(group, TraceRow::visibleSpendDecline))).append(',')
			       .append(format(mean(group, row -> row.config().proxySponsors()))).append(',')
			       .append(format(mean(group, TraceRow::privateGainPersistence))).append(',')
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
		builder.append("# A6 Lobbying-Camouflage Adversarial Stress Summary\n\n");
		builder.append("Status: `partial_a6_executable_pilot`.\n\n");
		builder.append(CLAIM_BOUNDARY).append("\n\n");
		builder.append("- Adversary: A6 lobbying camouflage actor\n");
		builder.append("- Same-seed generated-world runs: ").append(runs).append('\n');
		builder.append("- Legislators: ").append(legislators).append('\n');
		builder.append("- Base bills per run: ").append(bills).append('\n');
		builder.append("- Trace rows: ").append(traces.size()).append('\n');
		builder.append("- Trace artifact: `").append(TRACE_ARTIFACT).append("`\n");
		builder.append("- Recovery metrics: not modeled in this pilot\n\n");
		builder.append("| Information | Budget | Trace rows | Success rate | Anti-capture bypass | Capture enactment added | Visible-spend decline + capture | Shadow share added | Detection decline | Observed risk decline | Mean admin burden added |\n");
		builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
		for (AttackConfig config : attackConfigs()) {
			List<TraceRow> group = traces.stream().filter(trace -> trace.config().equals(config)).toList();
			builder.append("| ")
			       .append(config.informationLevel().key()).append(" | ")
			       .append(config.budgetValue()).append(" | ")
			       .append(group.size()).append(" | ")
			       .append(format(rate(group, TraceRow::success))).append(" | ")
			       .append(format(rate(group, TraceRow::antiCaptureBypass))).append(" | ")
			       .append(format(rate(group, row -> row.captureEnactmentAdded() > 0.0))).append(" | ")
			       .append(format(rate(group, TraceRow::visibleSpendDeclineWithCapturePersistence))).append(" | ")
			       .append(format(mean(group, TraceRow::shadowShareAdded))).append(" | ")
			       .append(format(mean(group, TraceRow::watchdogDetectionDecline))).append(" | ")
			       .append(format(mean(group, TraceRow::observedScreenRiskDecline))).append(" | ")
			       .append(format(mean(group, TraceRow::administrativeBurdenAdded))).append(" |\n");
		}
		builder.append("\nGate status: this moves A6 beyond a defensive-backlash proxy, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader anti-capture mechanisms, multi-seed replication, and external lobbying-disclosure validation remain incomplete.\n");
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
		property(builder, 1, "manifestVersion", "adversarial-stress-a6-run-v0", true);
		property(builder, 1, "status", "partial_a6_executable_pilot", true);
		property(builder, 1, "adversaryId", ADVERSARY_ID, true);
		property(builder, 1, "seed", Long.toString(seed), false, true);
		property(builder, 1, "runs", Integer.toString(runs), false, true);
		property(builder, 1, "legislators", Integer.toString(legislators), false, true);
		property(builder, 1, "baseBillsPerRun", Integer.toString(bills), false, true);
		property(builder, 1, "traceRows", Integer.toString(traces.size()), false, true);
		arrayProperty(builder, 1, "outputs", List.of(
				"reports/adversarial-stress-a6-summary.csv",
				"reports/adversarial-stress-a6-summary.md",
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

	private static List<String> actionList(AttackConfig config) {
		List<String> actions = new ArrayList<>();
		for (int i = 0; i < config.budgetValue(); i++) {
			actions.add("split_lobbying_spend");
		}
		actions.add("route_through_proxy_sponsors");
		actions.add("mask_private_gain_as_technical_information");
		if (config.informationLevel() == InformationLevel.HIGH) {
			actions.add("target_public_interest_screen_thresholds");
			actions.add("shift_activity_to_shadow_channels");
		}
		return actions;
	}

	private static String preAttackJson(TraceRow trace) {
		return "{"
				+ "\"latentBill\":" + billJson(trace.latentBill()) + ","
				+ "\"latentCaptureRisk\":" + format(trace.latentCaptureRisk()) + ","
				+ "\"baselineObservedScreenRisk\":" + format(trace.baselineObservedScreenRisk()) + ","
				+ "\"baselinePublicInterestScore\":" + format(LobbyCaptureScoring.publicInterestScore(trace.latentBill())) + ","
				+ "\"baselinePrivateGainRatio\":" + format(LobbyCaptureScoring.privateGainRatio(trace.latentBill()))
				+ "}";
	}

	private static String postAttackJson(TraceRow trace) {
		return "{"
				+ "\"camouflagedBill\":" + billJson(trace.camouflagedBill()) + ","
				+ "\"attackedObservedScreenRisk\":" + format(trace.attackedObservedScreenRisk()) + ","
				+ "\"observedScreenRiskDecline\":" + format(trace.observedScreenRiskDecline()) + ","
				+ "\"proxySponsors\":" + trace.config().proxySponsors() + ","
				+ "\"shadowLobbyTolerance\":" + format(trace.config().shadowLobbyTolerance()) + ","
				+ "\"disclosureEnforcement\":" + format(trace.config().disclosureEnforcement()) + ","
				+ "\"watchdogCapacity\":" + format(trace.config().watchdogCapacity())
				+ "}";
	}

	private static String outcomeJson(BillOutcome outcome) {
		return "{"
				+ "\"enacted\":" + outcome.enacted() + ","
				+ "\"finalReason\":\"" + json(outcome.finalReason()) + "\","
				+ "\"agendaDisposition\":\"" + outcome.agendaDisposition() + "\","
				+ "\"statusQuoBefore\":" + format(outcome.statusQuoBefore()) + ","
				+ "\"statusQuoAfter\":" + format(outcome.statusQuoAfter()) + ","
				+ "\"averageYayShare\":" + format(outcome.averageYayShare()) + ","
				+ "\"shadowLobbyingShare\":" + format(signal(outcome, "shadowLobbyingShare")) + ","
				+ "\"watchdogDetectionRate\":" + format(signal(outcome, "watchdogDetectionRate")) + ","
				+ "\"campaignFinanceCaptureIndex\":" + format(signal(outcome, "campaignFinanceCaptureIndex")) + ","
				+ "\"influenceSystemResilience\":" + format(signal(outcome, "influenceSystemResilience")) + ","
				+ "\"selectedBill\":" + billJson(outcome.bill())
				+ "}";
	}

	private static String pathJson(TraceRow trace) {
		return "{"
				+ "\"baselineFinalReason\":\"" + json(trace.baseline().finalReason()) + "\","
				+ "\"attackedFinalReason\":\"" + json(trace.attacked().finalReason()) + "\","
				+ "\"baselineBlockedByAntiCapture\":" + antiCaptureBlocked(trace.baseline()) + ","
				+ "\"attackedCapturedEnacted\":" + (capturedEnacted(trace.attacked(), trace.latentBill()) > 0.0) + ","
				+ "\"antiCaptureBypass\":" + trace.antiCaptureBypass() + ","
				+ "\"visibleSpendDeclineWithCapturePersistence\":" + trace.visibleSpendDeclineWithCapturePersistence()
				+ "}";
	}

	private static String metricDeltaJson(TraceRow trace) {
		return "{"
				+ "\"captureEnactmentAdded\":" + format(trace.captureEnactmentAdded()) + ","
				+ "\"observedScreenRiskDecline\":" + format(trace.observedScreenRiskDecline()) + ","
				+ "\"shadowShareAdded\":" + format(trace.shadowShareAdded()) + ","
				+ "\"watchdogDetectionDecline\":" + format(trace.watchdogDetectionDecline()) + ","
				+ "\"visibleSpendDecline\":" + format(trace.visibleSpendDecline()) + ","
				+ "\"privateGainPersistence\":" + format(trace.privateGainPersistence()) + ","
				+ "\"baselineEnacted\":" + trace.baseline().enacted() + ","
				+ "\"attackedEnacted\":" + trace.attacked().enacted()
				+ "}";
	}

	private static String administrativeBurdenJson(TraceRow trace) {
		return "{"
				+ "\"baselineBurden\":" + format(administrativeBurden(trace.baseline(), trace.config(), false)) + ","
				+ "\"attackedBurden\":" + format(administrativeBurden(trace.attacked(), trace.config(), true)) + ","
				+ "\"administrativeBurdenAdded\":" + format(trace.administrativeBurdenAdded()) + ","
				+ "\"proxySponsors\":" + trace.config().proxySponsors() + ","
				+ "\"baselineVisibleSpend\":" + format(visibleSpend(trace.baseline())) + ","
				+ "\"attackedVisibleSpend\":" + format(visibleSpend(trace.attacked())) + ","
				+ "\"baselineHiddenSpend\":" + format(hiddenSpend(trace.baseline())) + ","
				+ "\"attackedHiddenSpend\":" + format(hiddenSpend(trace.attacked()))
				+ "}";
	}

	private static String billJson(Bill bill) {
		return "{"
				+ "\"billId\":\"" + json(bill.id()) + "\","
				+ "\"ideologyPosition\":" + format(bill.ideologyPosition()) + ","
				+ "\"publicSupport\":" + format(bill.publicSupport()) + ","
				+ "\"publicBenefit\":" + format(bill.publicBenefit()) + ","
				+ "\"publicInterestScore\":" + format(LobbyCaptureScoring.publicInterestScore(bill)) + ","
				+ "\"captureRisk\":" + format(LobbyCaptureScoring.captureRisk(bill)) + ","
				+ "\"privateGainRatio\":" + format(LobbyCaptureScoring.privateGainRatio(bill)) + ","
				+ "\"privateGain\":" + format(bill.privateGain()) + ","
				+ "\"lobbyPressure\":" + format(bill.lobbyPressure()) + ","
				+ "\"lobbySpend\":" + format(bill.lobbySpend()) + ","
				+ "\"directLobbySpend\":" + format(bill.directLobbySpend()) + ","
				+ "\"agendaLobbySpend\":" + format(bill.agendaLobbySpend()) + ","
				+ "\"informationLobbySpend\":" + format(bill.informationLobbySpend()) + ","
				+ "\"publicCampaignSpend\":" + format(bill.publicCampaignSpend()) + ","
				+ "\"litigationThreatSpend\":" + format(bill.litigationThreatSpend()) + ","
				+ "\"cosponsorCount\":" + bill.cosponsorCount() + ","
				+ "\"outsideBlocCosponsorCount\":" + bill.outsideBlocCosponsorCount() + ","
				+ "\"attentionSpend\":" + format(bill.attentionSpend())
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
