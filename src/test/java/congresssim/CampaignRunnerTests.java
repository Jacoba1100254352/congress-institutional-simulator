package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.calibration.CalibrationRunner;
import congresssim.calibration.CalibrationRunner.CalibrationRunResult;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.experiment.CampaignRow;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.AgendaLotteryProcess;
import congresssim.institution.AlternativeSelectionRule;
import congresssim.institution.AmendmentMediationProcess;
import congresssim.institution.BillOutcome;
import congresssim.institution.BudgetedLobbyingProcess;
import congresssim.institution.Chamber;
import congresssim.institution.ChallengeEscalationProcess;
import congresssim.institution.ChallengeTokenAllocation;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CitizenPanelMode;
import congresssim.institution.CitizenPanelReviewProcess;
import congresssim.institution.CoalitionCosponsorshipProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.CompetingAlternativesProcess;
import congresssim.institution.ConstituentPublicWillProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.DistributionalHarmProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.MultiRoundAmendmentProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalBondProcess;
import congresssim.institution.ProposalCreditProcess;
import congresssim.institution.PublicObjectionWindowProcess;
import congresssim.institution.QuadraticAttentionBudgetProcess;
import congresssim.institution.SunsetTrialProcess;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.Scenario;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldGenerator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
import congresssim.model.SimulationWorld;
import congresssim.model.Vote;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.Set;

import static congresssim.TestSupport.*;
final class CampaignRunnerTests {
    private CampaignRunnerTests() {
    }

    static void run() {
        campaignRunnerWritesReports();
        tinyCampaignGoldenMetricsStayStable();
        campaignRunnerWritesWeightedCsvWithStableSchema();
        timelineCampaignHasOrderedContentionCases();
        strategyCampaignIncludesDeepAdaptiveSystems();
        paperCampaignUsesSingleCanonicalEvidenceBase();
        paperCampaignSeedRobustnessSmokeTest();
        calibrationRunnerWritesEmpiricalScreeningReports();
        allPredefinedCampaignScenarioListsIncludeCurrentBenchmark();
    }


    private static void campaignRunnerWritesReports() {
        try {
            Path outputDir = Path.of("out", "test-campaign");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v0.csv"));
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v0.md"));

            CampaignResult result = CampaignRunner.runV0(outputDir, 1, 11, 4, 77L);
            assertTrue(Files.exists(result.csvPath()), "Campaign should write a CSV artifact.");
            assertTrue(Files.exists(result.markdownPath()), "Campaign should write a Markdown artifact.");
            assertTrue(Files.exists(result.manifestPath()), "Campaign should write a provenance manifest.");
            assertTrue(
                    Files.readString(result.markdownPath()).contains("Simulation Campaign v0"),
                    "Campaign Markdown should identify the report."
            );
        } catch (Exception exception) {
            throw new AssertionError("Campaign report generation failed.", exception);
        }
    }

    private static void tinyCampaignGoldenMetricsStayStable() {
        try {
            Path outputDir = Path.of("out", "test-campaign-golden");
            Files.createDirectories(outputDir);
            CampaignResult result = CampaignRunner.runV0(outputDir, 1, 11, 4, 77L);

            CampaignRow simpleMajority = findRow(result, "baseline", "simple-majority");
            CampaignRow supermajority = findRow(result, "baseline", "supermajority-60");
            CampaignRow defaultPass = findRow(result, "baseline", "default-pass");
            CampaignRow informedGuarded = findRow(result, "baseline", "default-pass-informed-guarded");

            assertNear(simpleMajority.report().productivity(), 0.250, 0.0005, "Golden simple-majority productivity drifted.");
            assertNear(simpleMajority.report().averagePublicBenefit(), 0.702, 0.0005, "Golden simple-majority welfare drifted.");
            assertNear(supermajority.report().productivity(), 0.000, 0.0005, "Golden supermajority productivity drifted.");
            assertNear(defaultPass.report().productivity(), 0.500, 0.0005, "Golden default-pass productivity drifted.");
            assertNear(defaultPass.report().controversialPassageRate(), 0.500, 0.0005, "Golden default-pass low-support passage drifted.");
            assertNear(defaultPass.report().averagePolicyShift(), 0.558, 0.0005, "Golden default-pass policy shift drifted.");
            assertNear(informedGuarded.report().floorConsiderationRate(), 0.250, 0.0005, "Golden informed-guarded floor rate drifted.");
            assertNear(informedGuarded.report().accessDenialRate(), 0.500, 0.0005, "Golden informed-guarded access denial drifted.");
            assertNear(informedGuarded.report().committeeRejectionRate(), 0.250, 0.0005, "Golden informed-guarded committee rejection drifted.");
        } catch (Exception exception) {
            throw new AssertionError("Golden campaign regression failed.", exception);
        }
    }


    private static void campaignRunnerWritesWeightedCsvWithStableSchema() {
        try {
            Path outputDir = Path.of("out", "test-campaign-v18");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v18.csv"));
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v18.md"));

            CampaignResult result = CampaignRunner.runV18(outputDir, 1, 17, 3, 91L);
            assertTrue(result.rows().size() > 0, "Weighted campaign should produce result rows.");

            Set<String> cases = new HashSet<>();
            Set<String> scenarios = new HashSet<>();
            double caseWeightSum = 0.0;
            for (CampaignRow row : result.rows()) {
                scenarios.add(row.scenarioKey());
                if (cases.add(row.caseKey())) {
                    caseWeightSum += row.caseWeight();
                }
            }
            assertTrue(cases.size() == 4, "v18 should include the four weighted party-system cases.");
            assertTrue(Math.abs(caseWeightSum - 1.0) < 0.000001, "v18 case weights should sum to one.");
            assertTrue(scenarios.size() == 39, "v18 should exercise the full current roadmap-completion scenario set.");
            assertTrue(scenarios.contains("current-system"), "v18 should include the current-system benchmark.");
            assertTrue(scenarios.contains("default-pass-adaptive-proposers"), "v18 should include adaptive proposer behavior.");
            assertTrue(scenarios.contains("default-pass-strategic-lobbying"), "v18 should include strategic lobbying behavior.");

            String csv = Files.readString(result.csvPath());
            List<String> lines = csv.lines().filter(line -> !line.isBlank()).toList();
            assertTrue(lines.size() == result.rows().size() + 1, "CSV should contain one header plus one line per campaign row.");
            assertTrue(lines.getFirst().contains("directionalScore"), "CSV should expose oriented display scores.");
            assertTrue(lines.getFirst().contains("representativeQuality"), "CSV should expose representative quality.");
            assertTrue(lines.getFirst().contains("riskControl"), "CSV should expose inverted risk-control score.");
            int headerColumns = csvColumnCount(lines.getFirst());
            assertTrue(headerColumns >= 70, "CSV should expose the expanded metric schema.");
            for (int i = 1; i < lines.size(); i++) {
                assertTrue(
                        csvColumnCount(lines.get(i)) == headerColumns,
                        "Every CSV row should match the header column count."
                );
            }

            String markdown = Files.readString(result.markdownPath());
            assertTrue(markdown.contains("## Case Weights"), "Weighted campaigns should document case weights in Markdown.");
            assertTrue(markdown.contains("## Metric Direction Legend"), "Markdown should explain metric direction.");
            assertTrue(markdown.contains("Directional score ↑"), "Markdown scenario table should label oriented scores.");
            assertTrue(markdown.contains("Low-support ↓"), "Markdown scenario table should label lower-is-better metrics.");
            assertTrue(markdown.contains("Weighted Two Major Plus Minors"), "Markdown should include party-system case names.");
        } catch (Exception exception) {
            throw new AssertionError("Weighted campaign report generation failed.", exception);
        }
    }

    private static void timelineCampaignHasOrderedContentionCases() {
        try {
            Path outputDir = Path.of("out", "test-campaign-v19");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v19.csv"));
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v19.md"));

            CampaignResult result = CampaignRunner.runV19(outputDir, 2, 17, 6, 92L);
            assertTrue(result.rows().size() > 0, "Timeline campaign should produce result rows.");

            Set<String> cases = new HashSet<>();
            Set<String> scenarios = new HashSet<>();
            for (CampaignRow row : result.rows()) {
                cases.add(row.caseKey());
                scenarios.add(row.scenarioKey());
            }
            assertTrue(cases.size() == 6, "v19 should include six ordered timeline cases.");
            assertTrue(scenarios.contains("current-system"), "v19 should include the current-system benchmark.");
            assertTrue(scenarios.contains("presidential-veto"), "v19 should retain affirmative institutional baselines.");
            assertTrue(scenarios.contains("simple-majority-alternatives-pairwise"), "v19 should include the non-default policy-tournament comparison.");

            CampaignRow firstCurrent = findRow(result, "era-1-low-contention", "current-system");
            CampaignRow lastCurrent = findRow(result, "era-6-crisis", "current-system");
            assertTrue(
                    contentionIndex(lastCurrent.report()) > contentionIndex(firstCurrent.report()),
                    "The current-system benchmark should become more contentious along the stylized timeline."
            );

            String csv = Files.readString(result.csvPath());
            List<String> lines = csv.lines().filter(line -> !line.isBlank()).toList();
            int headerColumns = csvColumnCount(lines.getFirst());
            for (int i = 1; i < lines.size(); i++) {
                assertTrue(
                        csvColumnCount(lines.get(i)) == headerColumns,
                        "Timeline CSV rows should match the header column count."
                );
            }

            String markdown = Files.readString(result.markdownPath());
            assertTrue(markdown.contains("## Timeline Contention Path"), "Timeline campaign should document the longitudinal path.");
            assertTrue(markdown.contains("Era 6 Crisis"), "Timeline Markdown should include the crisis-era case.");
        } catch (Exception exception) {
            throw new AssertionError("Timeline campaign report generation failed.", exception);
        }
    }

    private static void strategyCampaignIncludesDeepAdaptiveSystems() {
        try {
            Path outputDir = Path.of("out", "test-campaign-v20");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v20.csv"));
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v20.md"));

            CampaignResult result = CampaignRunner.runV20(outputDir, 1, 17, 4, 94L);
            Set<String> scenarios = new HashSet<>();
            for (CampaignRow row : result.rows()) {
                scenarios.add(row.scenarioKey());
            }

            assertTrue(scenarios.contains("current-system"), "v20 should include the current-system benchmark.");
            assertTrue(scenarios.contains("default-pass-adaptive-proposers-lobbying"), "v20 should include adaptive proposers with strategic lobbying.");
            assertTrue(scenarios.contains("default-pass-deep-strategy-bundle"), "v20 should include the combined deep-strategy bundle.");
            assertTrue(Files.readString(result.markdownPath()).contains("Simulation Campaign v20"), "v20 Markdown should identify the report.");
        } catch (Exception exception) {
            throw new AssertionError("Strategy campaign report generation failed.", exception);
        }
    }

    private static void paperCampaignUsesSingleCanonicalEvidenceBase() {
        try {
            Path outputDir = Path.of("out", "test-campaign-v21-paper");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v21-paper.csv"));
            Files.deleteIfExists(outputDir.resolve("simulation-campaign-v21-paper.md"));

            CampaignResult result = CampaignRunner.runV21Paper(outputDir, 1, 17, 4, 95L);
            Set<String> cases = new HashSet<>();
            Set<String> scenarios = new HashSet<>();
            for (CampaignRow row : result.rows()) {
                cases.add(row.caseKey());
                scenarios.add(row.scenarioKey());
            }

            assertTrue(cases.contains("baseline"), "v21-paper should include broad assumption cases.");
            assertTrue(cases.contains("party-system-two-major-minors"), "v21-paper should include party-system sensitivity cases.");
            assertTrue(cases.contains("era-6-crisis"), "v21-paper should include timeline stress cases.");
            assertTrue(scenarios.contains("current-system"), "v21-paper should include the current-system benchmark.");
            assertTrue(scenarios.contains("committee-regular-order"), "v21-paper should include committee-first regular order.");
            assertTrue(scenarios.contains("parliamentary-coalition-confidence"), "v21-paper should include a coalition-confidence design.");
            assertTrue(scenarios.contains("simple-majority-alternatives-pairwise"), "v21-paper should include non-default policy tournaments.");
            assertTrue(scenarios.contains("harm-weighted-majority"), "v21-paper should include harm-weighted thresholds.");
            assertTrue(scenarios.contains("risk-routed-majority"), "v21-paper should include adaptive risk routing.");
            assertTrue(scenarios.contains("default-pass"), "v21-paper should retain default pass as one stress-test family.");
            assertTrue(Files.readString(result.markdownPath()).contains("Simulation Campaign v21 Paper"), "v21-paper Markdown should identify the report.");

            String csv = Files.readString(result.csvPath());
            assertTrue(csv.contains("party-system-two-major-minors"), "v21-paper CSV should contain party-system rows.");
            assertTrue(csv.contains("era-6-crisis"), "v21-paper CSV should contain timeline rows.");
            assertTrue(csv.contains("risk-routed-majority"), "v21-paper CSV should contain broad paper comparison scenarios.");
        } catch (Exception exception) {
            throw new AssertionError("Paper campaign report generation failed.", exception);
        }
    }

    private static void paperCampaignSeedRobustnessSmokeTest() {
        try {
            long[] seeds = {95L, 96L, 97L};
            int expectedRows = -1;
            double currentProductivityTotal = 0.0;
            double defaultProductivityTotal = 0.0;
            for (long seed : seeds) {
                Path outputDir = Path.of("out", "test-campaign-v21-paper-seed-" + seed);
                Files.createDirectories(outputDir);
                CampaignResult result = CampaignRunner.runV21Paper(outputDir, 1, 17, 4, seed);
                if (expectedRows < 0) {
                    expectedRows = result.rows().size();
                }
                assertTrue(result.rows().size() == expectedRows, "Seed robustness runs should keep the same row count.");

                CampaignRow current = findRow(result, "baseline", "current-system");
                CampaignRow defaultPass = findRow(result, "baseline", "default-pass");
                assertTrue(Double.isFinite(current.report().productivity()), "Current-system productivity should be finite.");
                assertTrue(Double.isFinite(defaultPass.report().productivity()), "Default-pass productivity should be finite.");
                currentProductivityTotal += current.report().productivity();
                defaultProductivityTotal += defaultPass.report().productivity();
            }

            assertTrue(
                    (defaultProductivityTotal / seeds.length) > (currentProductivityTotal / seeds.length),
                    "Open default-pass should remain the productivity stress-test extreme across smoke-test seeds."
            );
        } catch (Exception exception) {
            throw new AssertionError("Paper campaign seed robustness smoke test failed.", exception);
        }
    }

    private static void calibrationRunnerWritesEmpiricalScreeningReports() {
        try {
            Path outputDir = Path.of("out", "test-calibration");
            Files.createDirectories(outputDir);
            Files.deleteIfExists(outputDir.resolve("calibration-baseline.csv"));
            Files.deleteIfExists(outputDir.resolve("calibration-baseline.md"));

            CalibrationRunResult result = CalibrationRunner.run(outputDir, 120, 101, 60, 20260428L);
            assertTrue(Files.exists(result.csvPath()), "Calibration runner should write a CSV report.");
            assertTrue(Files.exists(result.markdownPath()), "Calibration runner should write a Markdown report.");
            assertTrue(Files.exists(result.manifestPath()), "Calibration runner should write a provenance manifest.");
            assertTrue(result.rows().size() >= 6, "Calibration runner should evaluate every benchmark range.");
            assertTrue(
                    result.rows().stream().allMatch(CalibrationRunner.CalibrationRow::passed),
                    "Executable calibration should pass all tracked benchmark screens."
            );

            String csv = Files.readString(result.csvPath());
            assertTrue(csv.contains("observed"), "Calibration CSV should include observed simulator values.");
            assertTrue(csv.contains("current-system-enactment-rate"), "Calibration CSV should include current-system attrition.");

            String markdown = Files.readString(result.markdownPath());
            assertTrue(markdown.contains("Calibration Baseline"), "Calibration Markdown should identify the report.");
            assertTrue(markdown.contains("passed checks"), "Calibration Markdown should summarize pass/fail results.");
            String manifest = Files.readString(result.manifestPath());
            assertTrue(manifest.contains("\"provenanceFormat\""), "Calibration manifest should use stable tracked provenance.");
            assertTrue(manifest.contains("\"sha256\""), "Calibration manifest should include artifact checksums.");
        } catch (Exception exception) {
            throw new AssertionError("Calibration report generation failed.", exception);
        }
    }

    @SuppressWarnings("unchecked")
    private static void allPredefinedCampaignScenarioListsIncludeCurrentBenchmark() {
        try {
            for (Field field : CampaignRunner.class.getDeclaredFields()) {
                if (!field.getName().endsWith("_SCENARIOS")) {
                    continue;
                }
                if (!Modifier.isStatic(field.getModifiers()) || !List.class.isAssignableFrom(field.getType())) {
                    continue;
                }
                field.setAccessible(true);
                List<String> scenarios = (List<String>) field.get(null);
                assertTrue(
                        scenarios.contains("current-system"),
                        field.getName() + " should include the current-system benchmark."
                );
            }
        } catch (IllegalAccessException exception) {
            throw new AssertionError("Could not inspect campaign scenario lists.", exception);
        }
    }

    private static CampaignRow findRow(CampaignResult result, String caseKey, String scenarioKey) {
        return result.rows()
                .stream()
                .filter(row -> row.caseKey().equals(caseKey) && row.scenarioKey().equals(scenarioKey))
                .findFirst()
                .orElseThrow(() -> new AssertionError("Missing campaign row: " + caseKey + "/" + scenarioKey));
    }

    private static void assertNear(double actual, double expected, double tolerance, String message) {
        assertTrue(Math.abs(actual - expected) <= tolerance, message + " Expected " + expected + ", actual " + actual);
    }

    private static double contentionIndex(ScenarioReport report) {
        return (0.50 * report.gridlockRate())
                + (0.30 * (1.0 - report.compromiseScore()))
                + (0.20 * report.controversialPassageRate());
    }

}
