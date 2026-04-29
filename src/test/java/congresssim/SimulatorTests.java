package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.BillOutcome;
import congresssim.institution.Chamber;
import congresssim.institution.ChallengeEscalationProcess;
import congresssim.institution.ChallengeTokenAllocation;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.List;
import java.util.Random;

public final class SimulatorTests {
    private SimulatorTests() {
    }

    public static void main(String[] args) {
        simpleMajorityRequiresMoreYaysThanNays();
        defaultPassRequiresBlockingSupermajority();
        proposalAccessCanDenyLowViabilityBills();
        proposalCostsCanDenyLowValueBills();
        crossBlocCosponsorshipRequiresOutsideSupport();
        challengeVouchersRouteHighRiskBillsToActiveVote();
        challengeEscalationRoutesBroadlyContestedBillsToActiveVote();
        committeeGateBlocksBillsBeforeFloor();
        committeeInformationMovesPublicSignalTowardBenefit();
        committeeCompositionPresetsSelectDifferentMembers();
        scenarioKeysSelectExpectedScenarios();
        campaignRunnerWritesReports();
        simulatorProducesOneReportPerScenario();
        System.out.println("All simulator tests passed.");
    }

    private static void simpleMajorityRequiresMoreYaysThanNays() {
        AffirmativeThresholdRule rule = AffirmativeThresholdRule.simpleMajority();
        assertTrue(rule.passes(6, 4), "6-4 should pass simple majority.");
        assertFalse(rule.passes(5, 5), "5-5 should fail simple majority.");
        assertFalse(rule.passes(4, 6), "4-6 should fail simple majority.");
    }

    private static void defaultPassRequiresBlockingSupermajority() {
        DefaultPassUnlessVetoedRule rule = new DefaultPassUnlessVetoedRule(2.0 / 3.0);
        assertTrue(rule.passes(4, 6), "6 nays out of 10 should not clear a 2/3 block threshold.");
        assertFalse(rule.passes(3, 7), "7 nays out of 10 should block default passage.");
    }

    private static void proposalAccessCanDenyLowViabilityBills() {
        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.8, 0.9, 0.20, 0.75, 0.0, 0.50);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        assertFalse(
                ProposalAccessRules.viabilityScreen(0.35, 0.85).evaluate(bill, context).granted(),
                "Low-support or distant bills should be denied proposal access."
        );
    }

    private static void proposalCostsCanDenyLowValueBills() {
        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.0, 0.02, 0.15, 0.20, 0.0, 0.20);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        assertFalse(
                ProposalAccessRules.proposalCost(0.34, 0.22, 0.18).evaluate(bill, context).granted(),
                "Low-value proposals should fail the proposal-cost screen."
        );
    }

    private static void crossBlocCosponsorshipRequiresOutsideSupport() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.45, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-2", "Left", -0.35, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-3", "Center", -0.05, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-4", "Center", 0.10, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-5", "Right", 0.45, 0.7, 0.6, 0.8, 0.2, 0.8)
        );
        VoteContext context = new VoteContext(Map.of("Left", -0.40, "Center", 0.02, "Right", 0.45), new Random(1L), 0.0);
        Bill bridgeBill = new Bill("B-bridge", "Bridge Bill", "L-1", -0.45, 0.02, 0.75, 0.80, 0.0, 0.50);
        Bill narrowBill = new Bill("B-narrow", "Narrow Bill", "L-1", -0.45, -0.55, 0.35, 0.35, 0.6, 0.50);

        assertTrue(
                ProposalAccessRules.crossBlocCosponsorship(legislators, 2, 1, 0.18, 0.58)
                        .evaluate(bridgeBill, context)
                        .granted(),
                "Broad, moderate bills should be able to earn cross-bloc access."
        );
        assertFalse(
                ProposalAccessRules.crossBlocCosponsorship(legislators, 2, 1, 0.18, 0.58)
                        .evaluate(narrowBill, context)
                        .granted(),
                "Narrow, low-support bills should fail the cross-bloc gate."
        );
    }

    private static void challengeVouchersRouteHighRiskBillsToActiveVote() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Opposition", -0.9, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-2", "Opposition", -0.7, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-3", "Sponsor", 0.8, 0.4, 0.6, 0.5, 0.2, 0.5)
        );
        LegislativeProcess activeVote = new LegislativeProcess() {
            @Override
            public String name() {
                return "active vote";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                return new BillOutcome(
                        bill,
                        context.currentPolicyPosition(),
                        context.currentPolicyPosition(),
                        false,
                        List.of(),
                        congresssim.institution.PresidentialAction.none(),
                        "failed active vote"
                );
            }
        };

        Bill bill = new Bill("B-risk", "Risky Bill", "L-3", 0.8, 0.95, 0.05, 0.15, 0.6, 0.90);
        VoteContext context = new VoteContext(Map.of("Opposition", -0.8, "Sponsor", 0.8), new Random(2L), 0.0);
        BillOutcome outcome = new ChallengeVoucherProcess(
                "challenge test",
                legislators,
                (legislator, testedBill, voteContext) -> Vote.NAY,
                ChallengeTokenAllocation.PARTY,
                1,
                0.10,
                activeVote
        ).consider(bill, context);

        assertTrue(outcome.challenged(), "High-risk bills should consume a challenge voucher.");
        assertFalse(outcome.enacted(), "Challenged bills should use the configured active-vote path.");
    }

    private static void challengeEscalationRoutesBroadlyContestedBillsToActiveVote() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Opposition", -0.9, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-2", "Opposition", -0.7, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-3", "Sponsor", 0.8, 0.4, 0.6, 0.5, 0.2, 0.5)
        );
        LegislativeProcess activeVote = new LegislativeProcess() {
            @Override
            public String name() {
                return "active vote";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                return new BillOutcome(
                        bill,
                        context.currentPolicyPosition(),
                        context.currentPolicyPosition(),
                        false,
                        List.of(),
                        congresssim.institution.PresidentialAction.none(),
                        "failed active vote"
                );
            }
        };

        Bill bill = new Bill("B-risk", "Risky Bill", "L-3", 0.8, 0.95, 0.05, 0.15, 0.6, 0.90);
        VoteContext context = new VoteContext(Map.of("Opposition", -0.8, "Sponsor", 0.8), new Random(2L), 0.0);
        BillOutcome outcome = new ChallengeEscalationProcess(
                "challenge escalation test",
                legislators,
                (legislator, testedBill, voteContext) -> Vote.NAY,
                2,
                0.10,
                activeVote
        ).consider(bill, context);

        assertTrue(outcome.challenged(), "Broadly contested bills should trigger q-member escalation.");
        assertFalse(outcome.enacted(), "Escalated bills should use the configured active-vote path.");
    }

    private static void committeeGateBlocksBillsBeforeFloor() {
        List<Legislator> committeeMembers = List.of(
                legislator("L-1"),
                legislator("L-2"),
                legislator("L-3")
        );
        VotingStrategy alwaysNay = (legislator, bill, context) -> Vote.NAY;
        Chamber committee = new Chamber(
                "Committee",
                committeeMembers,
                alwaysNay,
                AffirmativeThresholdRule.simpleMajority()
        );
        LegislativeProcess floorWouldPass = new LegislativeProcess() {
            @Override
            public String name() {
                return "floor would pass";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                return new BillOutcome(
                        bill,
                        context.currentPolicyPosition(),
                        bill.ideologyPosition(),
                        true,
                        List.of(),
                        congresssim.institution.PresidentialAction.none(),
                        "floor would pass"
                );
            }
        };

        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.0, 0.1, 0.60, 0.70, 0.0, 0.50);
        BillOutcome outcome = new CommitteeGatekeepingProcess("test committee", committee, floorWouldPass)
                .consider(bill, new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0));

        assertFalse(outcome.enacted(), "Committee rejection should prevent enactment.");
        assertTrue(
                outcome.agendaDisposition() == AgendaDisposition.COMMITTEE_REJECTED,
                "Committee rejection should be recorded as the agenda disposition."
        );
    }

    private static void committeeInformationMovesPublicSignalTowardBenefit() {
        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.0, 0.1, 0.20, 0.90, 0.0, 0.50);
        List<Legislator> committeeMembers = List.of(
                new Legislator("L-1", "Test", 0.0, 1.0, 0.2, 1.0, 0.0, 1.0),
                new Legislator("L-2", "Test", 0.0, 1.0, 0.2, 1.0, 0.0, 1.0)
        );
        LegislativeProcess captureBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                return new BillOutcome(
                        bill,
                        context.currentPolicyPosition(),
                        context.currentPolicyPosition(),
                        false,
                        List.of(),
                        congresssim.institution.PresidentialAction.none(),
                        "captured"
                );
            }
        };

        BillOutcome outcome = new CommitteeInformationProcess(
                "test information",
                committeeMembers,
                1.0,
                0.0,
                captureBill
        ).consider(bill, new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0));

        assertTrue(
                outcome.bill().publicSupport() > bill.publicSupport(),
                "Information review should move perceived public support toward public benefit."
        );
        assertTrue(
                outcome.bill().publicSupport() < bill.publicBenefit(),
                "Information review should improve the signal without making it perfectly omniscient."
        );
    }

    private static void committeeCompositionPresetsSelectDifferentMembers() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "A", -0.9, 0.1, 0.5, 0.2, 0.1, 0.2),
                new Legislator("L-2", "A", -0.4, 0.2, 0.5, 0.2, 0.2, 0.2),
                new Legislator("L-3", "B", 0.0, 1.0, 0.5, 1.0, 0.0, 1.0),
                new Legislator("L-4", "B", 0.4, 0.4, 0.5, 0.4, 0.8, 0.4),
                new Legislator("L-5", "B", 0.9, 0.3, 0.5, 0.3, 1.0, 0.3)
        );

        List<Legislator> expert = CommitteeFactory.select(legislators, CommitteeComposition.EXPERT, 2);
        List<Legislator> captured = CommitteeFactory.select(legislators, CommitteeComposition.CAPTURED, 2);

        assertTrue(expert.stream().anyMatch(legislator -> legislator.id().equals("L-3")), "Expert committee should select public-interest members.");
        assertTrue(captured.stream().anyMatch(legislator -> legislator.id().equals("L-5")), "Captured committee should select lobby-sensitive members.");
    }

    private static void simulatorProducesOneReportPerScenario() {
        WorldSpec spec = new WorldSpec(31, 8, 3, 0.70, 0.65, 0.45, 0.60, 0.50);
        List<ScenarioReport> reports = new Simulator().compare(ScenarioCatalog.defaultScenarios(), spec, 3, 1234L);
        assertTrue(reports.size() == ScenarioCatalog.defaultScenarios().size(), "Expected one report per scenario.");
        for (ScenarioReport report : reports) {
            assertTrue(report.totalBills() == 24, "Expected 3 runs * 8 bills.");
            assertTrue(report.productivity() >= 0.0 && report.productivity() <= 1.0, "Productivity must be a ratio.");
        }
    }

    private static void scenarioKeysSelectExpectedScenarios() {
        assertTrue(
                ScenarioCatalog.scenariosForKeys(List.of("default-pass", "default-pass-guarded")).size() == 2,
                "Scenario keys should select a focused scenario subset."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-challenge"),
                "Scenario catalog should expose CLI-facing keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-escalation-q12-s082"),
                "Scenario catalog should expose tokenless escalation sweep keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-cross-bloc"),
                "Scenario catalog should expose cross-bloc cosponsorship keys."
        );
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

    private static Legislator legislator(String id) {
        return new Legislator(id, "Test", 0.0, 0.5, 0.5, 0.5, 0.5, 0.5);
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void assertFalse(boolean condition, String message) {
        assertTrue(!condition, message);
    }
}
