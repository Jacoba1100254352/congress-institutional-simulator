package congresssim;


import congresssim.institution.adversary.AdversaryCatalog;
import congresssim.institution.adversary.AdversaryCatalogExporter;
import congresssim.institution.adversary.AdversarySpec;
import congresssim.institution.adversary.A1A8AdversarialReplicationSeedRunner;
import congresssim.institution.adversary.A1CloneDecoyAdversarialStressRunner;
import congresssim.institution.adversary.A2PoisonPillAdversarialStressRunner;
import congresssim.institution.adversary.A3PublicInputAdversarialStressRunner;
import congresssim.institution.adversary.A4BadFaithHarmClaimAdversarialStressRunner;
import congresssim.institution.adversary.A5ProposalFloodingAdversarialStressRunner;
import congresssim.institution.adversary.A6LobbyingCamouflageAdversarialStressRunner;
import congresssim.institution.adversary.A7AdministrativeOverloadAdversarialStressRunner;
import congresssim.institution.adversary.A8PublicSupportDistortionAdversarialStressRunner;
import congresssim.institution.adversary.A9MixedAdversaryPortfolioStressRunner;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static congresssim.TestSupport.assertTrue;


final class AdversaryCatalogTests
{
	private AdversaryCatalogTests() {
	}

	static void run() {
		firstWaveAdversaryCatalogHasRequiredSchema();
		exporterWritesMachineReadableManifest();
		a1RunnerWritesTraceAndSummaryArtifacts();
		a2RunnerWritesTraceAndSummaryArtifacts();
		a3RunnerWritesTraceAndSummaryArtifacts();
		a4RunnerWritesTraceAndSummaryArtifacts();
		a5RunnerWritesTraceAndSummaryArtifacts();
		a6RunnerWritesTraceAndSummaryArtifacts();
		a7RunnerWritesTraceAndSummaryArtifacts();
		a8RunnerWritesTraceAndSummaryArtifacts();
		a1ThroughA8SummaryOnlyModesOmitTraceArtifacts();
		a9RunnerWritesTraceAndSummaryArtifacts();
		a9SummaryOnlyModeOmitsTraceArtifacts();
	}

	private static void firstWaveAdversaryCatalogHasRequiredSchema() {
		Set<String> ids = new HashSet<>();
		for (AdversarySpec spec : AdversaryCatalog.firstWave()) {
			assertTrue(ids.add(spec.id()), "Adversary ids must be unique.");
			assertTrue(spec.id().matches("A[1-9]"), "First-wave adversary ids should use the A1-A9 convention.");
			assertTrue(!spec.actorType().isBlank(), "Actor type should be documented for " + spec.id());
			assertTrue(!spec.objective().isBlank(), "Objective should be documented for " + spec.id());
			assertTrue(!spec.informationLevels().isEmpty(), "Information levels should be documented for " + spec.id());
			assertTrue(!spec.budgetUnits().isEmpty(), "Budget units should be documented for " + spec.id());
			assertTrue(!spec.strategySet().isEmpty(), "Strategy set should be documented for " + spec.id());
			assertTrue(!spec.successMetric().isBlank(), "Success metric should be documented for " + spec.id());
			assertTrue(!spec.degradationMetric().isBlank(), "Degradation metric should be documented for " + spec.id());
		}
		assertTrue(ids.size() == 9, "The first-wave catalog should cover A1 through A9.");
		assertTrue(AdversaryCatalog.requiredTraceFields().contains("attackActionList"), "Trace schema should include attack actions.");
		assertTrue(AdversaryCatalog.requiredTraceFields().contains("baselineOutcome"), "Trace schema should include baseline outcome.");
		assertTrue(AdversaryCatalog.requiredTraceFields().contains("attackedOutcome"), "Trace schema should include attacked outcome.");
		assertTrue(AdversaryCatalog.requiredTraceFields().contains("successFlag"), "Trace schema should include success flag.");
	}

	private static void exporterWritesMachineReadableManifest() {
		try {
			Path outputDir = Path.of("out", "test-adversary-catalog");
			Files.createDirectories(outputDir);
			AdversaryCatalogExporter.write(outputDir);
			Path csv = outputDir.resolve("adversary-catalog.csv");
			Path markdown = outputDir.resolve("adversary-catalog.md");
			Path manifest = outputDir.resolve("adversarial-stress-manifest.json");
			assertTrue(Files.exists(csv), "Catalog exporter should write CSV.");
			assertTrue(Files.exists(markdown), "Catalog exporter should write Markdown.");
			assertTrue(Files.exists(manifest), "Catalog exporter should write JSON manifest.");
			assertTrue(Files.readString(csv).contains("\"A1\""), "Catalog CSV should include A1.");
			assertTrue(Files.readString(markdown).contains("Required Trace Fields"), "Catalog Markdown should document trace fields.");
			String json = Files.readString(manifest);
			assertTrue(json.contains("\"manifestVersion\""), "Manifest should include a version.");
			assertTrue(json.contains("\"firstWaveAdversaries\""), "Manifest should include adversary specs.");
			assertTrue(json.contains("\"requiredTraceFields\""), "Manifest should include trace fields.");
		} catch (Exception exception) {
			throw new AssertionError("Adversary catalog export failed.", exception);
		}
	}

	private static void a1RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a1-adversarial-stress");
			Files.createDirectories(outputDir);
			A1CloneDecoyAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-run-manifest.json");
			assertTrue(Files.exists(summary), "A1 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A1 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A1 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A1 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a1_executable_pilot"), "A1 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 36"), "A1 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A1 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 36, "Tiny A1 run should produce six cells times six generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A1\""), "A1 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A1 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A1 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A1 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A1 adversarial stress runner failed.", exception);
		}
	}

	private static void a2RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a2-adversarial-stress");
			Files.createDirectories(outputDir);
			A2PoisonPillAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a2-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a2-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a2.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a2-run-manifest.json");
			assertTrue(Files.exists(summary), "A2 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A2 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A2 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A2 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a2_executable_pilot"), "A2 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 18"), "A2 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A2 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 18, "Tiny A2 run should produce six cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A2\""), "A2 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A2 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A2 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A2 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A2 adversarial stress runner failed.", exception);
		}
	}

	private static void a3RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a3-adversarial-stress");
			Files.createDirectories(outputDir);
			A3PublicInputAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a3-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a3-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a3.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a3-run-manifest.json");
			assertTrue(Files.exists(summary), "A3 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A3 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A3 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A3 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a3_executable_pilot"), "A3 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 18"), "A3 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A3 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 18, "Tiny A3 run should produce six cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A3\""), "A3 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A3 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A3 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A3 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A3 adversarial stress runner failed.", exception);
		}
	}

	private static void a4RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a4-adversarial-stress");
			Files.createDirectories(outputDir);
			A4BadFaithHarmClaimAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a4-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a4-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a4.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a4-run-manifest.json");
			assertTrue(Files.exists(summary), "A4 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A4 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A4 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A4 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a4_executable_pilot"), "A4 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 9"), "A4 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 4, "A4 summary should contain one header and three medium-information budget rows.");
			assertTrue(traceLines.size() == 9, "Tiny A4 run should produce three cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A4\""), "A4 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A4 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A4 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A4 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A4 adversarial stress runner failed.", exception);
		}
	}

	private static void a5RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a5-adversarial-stress");
			Files.createDirectories(outputDir);
			A5ProposalFloodingAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a5-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a5-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a5.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a5-run-manifest.json");
			assertTrue(Files.exists(summary), "A5 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A5 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A5 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A5 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a5_executable_pilot"), "A5 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 18"), "A5 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A5 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 18, "Tiny A5 run should produce six cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A5\""), "A5 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A5 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A5 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A5 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A5 adversarial stress runner failed.", exception);
		}
	}

	private static void a6RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a6-adversarial-stress");
			Files.createDirectories(outputDir);
			A6LobbyingCamouflageAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a6-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a6-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a6.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a6-run-manifest.json");
			assertTrue(Files.exists(summary), "A6 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A6 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A6 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A6 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a6_executable_pilot"), "A6 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 18"), "A6 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A6 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 18, "Tiny A6 run should produce six cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A6\""), "A6 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A6 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A6 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A6 trace should include attacked outcome.");
		} catch (Exception exception) {
			throw new AssertionError("A6 adversarial stress runner failed.", exception);
		}
	}

	private static void a7RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a7-adversarial-stress");
			Files.createDirectories(outputDir);
			A7AdministrativeOverloadAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a7-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a7-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a7.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a7-run-manifest.json");
			assertTrue(Files.exists(summary), "A7 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A7 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A7 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A7 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a7_executable_pilot"), "A7 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 18"), "A7 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 7, "A7 summary should contain one header and six budget/information rows.");
			assertTrue(traceLines.size() == 18, "Tiny A7 run should produce six cells times three generated bills.");
			assertTrue(traceLines.getFirst().contains("\"adversaryId\":\"A7\""), "A7 trace should identify the adversary.");
			assertTrue(traceLines.getFirst().contains("\"attackActionList\""), "A7 trace should include attack actions.");
			assertTrue(traceLines.getFirst().contains("\"baselineOutcome\""), "A7 trace should include baseline outcome.");
			assertTrue(traceLines.getFirst().contains("\"attackedOutcome\""), "A7 trace should include attacked outcome.");
			assertTrue(traceLines.getFirst().contains("\"recoveryMetrics\""), "A7 trace should include recovery metrics.");
		} catch (Exception exception) {
			throw new AssertionError("A7 adversarial stress runner failed.", exception);
		}
	}

	private static void a8RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a8-adversarial-stress");
			Files.createDirectories(outputDir);
			A8PublicSupportDistortionAdversarialStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a8-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a8-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a8.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a8-run-manifest.json");
			assertTrue(Files.exists(summary), "A8 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A8 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A8 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A8 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a8_executable_pilot"), "A8 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"summaryRows\": 18"), "A8 run manifest should count summary rows.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 54"), "A8 run manifest should count trace rows.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 19, "A8 summary should contain one header and eighteen mechanism/budget/information rows.");
			assertTrue(traceLines.size() == 54, "Tiny A8 run should produce eighteen cells times three generated bills.");
			String firstTrace = traceLines.getFirst();
			assertTrue(firstTrace.contains("\"adversaryId\":\"A8\""), "A8 trace should identify the adversary.");
			assertTrue(firstTrace.contains("\"attackActionList\""), "A8 trace should include attack actions.");
			assertTrue(firstTrace.contains("\"generatedPublicSupport\""), "A8 trace should preserve generated support for evaluation.");
			assertTrue(firstTrace.contains("\"attackedInputFeatures\""), "A8 trace should expose the manipulated input signal.");
			assertTrue(firstTrace.contains("\"correctionMetrics\""), "A8 trace should include signal-correction metrics.");
			assertTrue(firstTrace.contains("\"attackedObjectionWindows\":0"), "A8 should not invoke A3 objection windows.");
			assertTrue(firstTrace.contains("\"attackedCitizenReviews\":0"), "A8 should not invoke A3 citizen panels.");
			assertTrue(traceLines.stream().anyMatch(line -> line.contains("\"mechanismFamily\":\"signal_reliant_majority\"")),
					"A8 traces should include the signal-reliant path.");
			assertTrue(traceLines.stream().anyMatch(line -> line.contains("\"mechanismFamily\":\"constituent_verified_majority\"")),
					"A8 traces should include the constituent-verified path.");
		} catch (Exception exception) {
			throw new AssertionError("A8 adversarial stress runner failed.", exception);
		}
	}

	private static void a9RunnerWritesTraceAndSummaryArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a9-adversarial-stress");
			Files.createDirectories(outputDir);
			A9MixedAdversaryPortfolioStressRunner.run(outputDir, 1, 15, 3, 12345L);
			Path summary = outputDir.resolve("adversarial-stress-a9-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a9-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a9.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a9-run-manifest.json");
			assertTrue(Files.exists(summary), "A9 runner should write summary CSV.");
			assertTrue(Files.exists(markdown), "A9 runner should write summary Markdown.");
			assertTrue(Files.exists(traces), "A9 runner should write JSONL traces.");
			assertTrue(Files.exists(manifest), "A9 runner should write a run manifest.");
			assertTrue(Files.readString(markdown).contains("partial_a9_executable_pilot"), "A9 Markdown should label pilot status.");
			assertTrue(Files.readString(manifest).contains("\"summaryRows\": 18"), "A9 run manifest should count summary rows.");
			assertTrue(Files.readString(manifest).contains("\"traceRows\": 54"), "A9 run manifest should count trace rows.");
			assertTrue(Files.readString(manifest).contains("\"mixedOnlySuccessRows\""), "A9 manifest should count mixed-only successes.");
			List<String> summaryLines = Files.readAllLines(summary);
			List<String> traceLines = Files.readAllLines(traces);
			assertTrue(summaryLines.size() == 19, "A9 summary should contain one header and eighteen portfolio/budget/information rows.");
			assertTrue(summaryLines.getFirst().contains("attackSuccessCount"), "A9 summary should report exact success counts alongside rates.");
			assertTrue(traceLines.size() == 54, "Tiny A9 run should produce eighteen cells times three generated bills.");
			String firstTrace = traceLines.getFirst();
			assertTrue(firstTrace.contains("\"adversaryId\":\"A9\""), "A9 trace should identify the adversary.");
			assertTrue(firstTrace.contains("\"portfolioAllocation\""), "A9 trace should include exact portfolio allocation.");
			assertTrue(firstTrace.contains("\"sameBudgetSingleControls\""), "A9 trace should include full-budget single controls.");
			assertTrue(firstTrace.contains("\"allocatedComponentControls\""), "A9 trace should include allocated-component controls.");
			assertTrue(firstTrace.contains("\"mixedOnlySuccess\""), "A9 trace should label the strict mixed-only success flag consistently.");
			assertTrue(firstTrace.contains("\"interactionMetrics\""), "A9 trace should include interaction metrics.");
			assertTrue(firstTrace.contains("\"recoveryMetrics\""), "A9 trace should include correction or recovery metrics.");
			assertTrue(traceLines.stream().anyMatch(line -> line.contains("\"portfolioKey\":\"clone-decoy-poison-pill\"")),
					"A9 traces should include the A1+A2 portfolio.");
			assertTrue(traceLines.stream().anyMatch(line -> line.contains("\"portfolioKey\":\"astroturf-harm-claims\"")),
					"A9 traces should include the A3+A4 portfolio.");
			assertTrue(traceLines.stream().anyMatch(line -> line.contains("\"portfolioKey\":\"flood-camouflage-support-distortion\"")),
					"A9 traces should include the A5+A6+A8 portfolio.");
		} catch (Exception exception) {
			throw new AssertionError("A9 adversarial stress runner failed.", exception);
		}
	}

	private static void a9SummaryOnlyModeOmitsTraceArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a9-adversarial-summary-only");
			Files.createDirectories(outputDir);
			Path summary = outputDir.resolve("adversarial-stress-a9-summary.csv");
			Path markdown = outputDir.resolve("adversarial-stress-a9-summary.md");
			Path traces = outputDir.resolve("adversarial-failure-traces-a9.jsonl");
			Path manifest = outputDir.resolve("adversarial-stress-a9-run-manifest.json");
			Files.deleteIfExists(summary);
			Files.deleteIfExists(markdown);
			Files.deleteIfExists(traces);
			Files.deleteIfExists(manifest);

			A9MixedAdversaryPortfolioStressRunner.runSummaryOnly(outputDir, 1, 15, 3, 54321L);

			assertTrue(Files.exists(summary), "A9 summary-only mode should write the summary CSV.");
			assertTrue(Files.readAllLines(summary).size() == 19, "A9 summary-only mode should retain all eighteen cells.");
			assertTrue(!Files.exists(markdown), "A9 summary-only mode should not write Markdown.");
			assertTrue(!Files.exists(traces), "A9 summary-only mode should not write per-bill traces.");
			assertTrue(!Files.exists(manifest), "A9 summary-only mode should not write a standalone run manifest.");
		} catch (Exception exception) {
			throw new AssertionError("A9 summary-only adversarial stress runner failed.", exception);
		}
	}

	private static void a1ThroughA8SummaryOnlyModesOmitTraceArtifacts() {
		try {
			Path outputDir = Path.of("out", "test-a1-a8-adversarial-summary-only");
			Files.createDirectories(outputDir);
			try (var existing = Files.list(outputDir)) {
				for (Path path : existing.toList()) {
					Files.delete(path);
				}
			}

			A1A8AdversarialReplicationSeedRunner.run(outputDir, 1, 15, 3, 98765L);

			try (var generated = Files.list(outputDir)) {
				List<Path> artifacts = generated.sorted().toList();
				assertTrue(artifacts.size() == 8, "A1-A8 summary-only mode should write exactly eight artifacts.");
				for (Path artifact : artifacts) {
					assertTrue(artifact.getFileName().toString().endsWith(".csv"), "A1-A8 summary-only artifacts should all be CSV summaries.");
					String header = Files.readAllLines(artifact).getFirst();
					assertTrue(header.contains("attackSuccessCount"), "A1-A8 summaries should report exact success counts.");
				}
			}
		} catch (Exception exception) {
			throw new AssertionError("A1-A8 summary-only adversarial replication runner failed.", exception);
		}
	}
}
