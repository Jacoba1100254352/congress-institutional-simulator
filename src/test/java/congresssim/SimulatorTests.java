package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.BillOutcome;
import congresssim.institution.Chamber;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

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
        committeeGateBlocksBillsBeforeFloor();
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
        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.8, 0.9, 0.20, 0.0, 0.50);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        assertFalse(
                ProposalAccessRules.viabilityScreen(0.35, 0.85).evaluate(bill, context).granted(),
                "Low-support or distant bills should be denied proposal access."
        );
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

        Bill bill = new Bill("B-test", "Test Bill", "L-1", 0.0, 0.1, 0.60, 0.0, 0.50);
        BillOutcome outcome = new CommitteeGatekeepingProcess("test committee", committee, floorWouldPass)
                .consider(bill, new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0));

        assertFalse(outcome.enacted(), "Committee rejection should prevent enactment.");
        assertTrue(
                outcome.agendaDisposition() == AgendaDisposition.COMMITTEE_REJECTED,
                "Committee rejection should be recorded as the agenda disposition."
        );
    }

    private static void simulatorProducesOneReportPerScenario() {
        WorldSpec spec = new WorldSpec(31, 8, 0.70, 0.65, 0.45, 0.60, 0.50);
        List<ScenarioReport> reports = new Simulator().compare(ScenarioCatalog.defaultScenarios(), spec, 3, 1234L);
        assertTrue(reports.size() == ScenarioCatalog.defaultScenarios().size(), "Expected one report per scenario.");
        for (ScenarioReport report : reports) {
            assertTrue(report.totalBills() == 24, "Expected 3 runs * 8 bills.");
            assertTrue(report.productivity() >= 0.0 && report.productivity() <= 1.0, "Productivity must be a ratio.");
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
