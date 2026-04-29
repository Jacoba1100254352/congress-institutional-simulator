package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
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
            assertTrue(markdown.contains("Weighted Two Major Plus Minors"), "Markdown should include party-system case names.");
        } catch (Exception exception) {
            throw new AssertionError("Weighted campaign report generation failed.", exception);
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

}
