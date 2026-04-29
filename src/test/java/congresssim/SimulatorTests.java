package congresssim;

import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.util.List;

public final class SimulatorTests {
    private SimulatorTests() {
    }

    public static void main(String[] args) {
        simpleMajorityRequiresMoreYaysThanNays();
        defaultPassRequiresBlockingSupermajority();
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

    private static void simulatorProducesOneReportPerScenario() {
        WorldSpec spec = new WorldSpec(31, 8, 0.70, 0.65, 0.45, 0.60, 0.50);
        List<ScenarioReport> reports = new Simulator().compare(ScenarioCatalog.defaultScenarios(), spec, 3, 1234L);
        assertTrue(reports.size() == ScenarioCatalog.defaultScenarios().size(), "Expected one report per scenario.");
        for (ScenarioReport report : reports) {
            assertTrue(report.totalBills() == 24, "Expected 3 runs * 8 bills.");
            assertTrue(report.productivity() >= 0.0 && report.productivity() <= 1.0, "Productivity must be a ratio.");
        }
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

