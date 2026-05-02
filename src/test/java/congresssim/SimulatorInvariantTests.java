package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.experiment.CampaignRow;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.MetricDefinition;
import congresssim.simulation.MetricDirection;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.Scenario;
import congresssim.simulation.catalog.ScenarioCatalog;
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

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.Set;

import static congresssim.TestSupport.*;
final class SimulatorInvariantTests {
    private SimulatorInvariantTests() {
    }

    static void run() {
        simulatorReportsAreDeterministicAndBounded();
        metricDirectionMetadataCoversCoreMetrics();
        simulatorProducesOneReportPerScenario();
    }


    private static void simulatorReportsAreDeterministicAndBounded() {
        WorldSpec spec = new WorldSpec(
                31,
                10,
                5,
                0.72,
                0.66,
                0.48,
                0.64,
                0.55,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                0.40
        );
        List<Scenario> scenarios = ScenarioCatalog.scenariosForKeys(List.of(
                "default-pass",
                "default-pass-challenge",
                "default-pass-compensation",
                "default-pass-citizen-certificate",
                "default-pass-alternatives-pairwise",
                "default-pass-weighted-agenda-lottery"
        ));
        Simulator simulator = new Simulator();
        List<ScenarioReport> first = simulator.compare(scenarios, spec, 3, 5150L);
        List<ScenarioReport> second = simulator.compare(scenarios, spec, 3, 5150L);

        assertTrue(first.equals(second), "Simulator reports should be deterministic for a fixed seed.");
        for (ScenarioReport report : first) {
            assertTrue(report.totalBills() == 30, "Report should count runs times generated bills.");
            assertTrue(report.enactedBills() >= 0 && report.enactedBills() <= report.totalBills(), "Enacted bills should be bounded by total bills.");
            assertRatio(report.productivity(), "Productivity should be a ratio.");
            assertRatio(report.averageEnactedSupport(), "Average enacted support should be a ratio.");
            assertRatio(report.averagePublicBenefit(), "Average public benefit should be a ratio.");
            assertRatio(report.cooperationScore(), "Cooperation score should be a ratio.");
            assertRatio(report.compromiseScore(), "Compromise score should be a ratio.");
            assertRatio(report.representativeQualityScore(), "Representative quality should be a directional ratio.");
            assertRatio(report.riskControlScore(), "Risk control should be a directional ratio.");
            assertRatio(report.administrativeFeasibilityScore(), "Administrative feasibility should be a directional ratio.");
            assertRatio(report.directionalScore(), "Directional score should be a directional ratio.");
            assertRatio(report.gridlockRate(), "Gridlock rate should be a ratio.");
            assertRatio(report.controversialPassageRate(), "Low-support passage should be a ratio.");
            assertRatio(report.weakPublicMandatePassageRate(), "Weak public-mandate passage should be a ratio.");
            assertRatio(report.popularBillFailureRate(), "Popular bill failure rate should be a ratio.");
            assertTrue(report.averagePolicyShift() >= 0.0 && report.averagePolicyShift() <= 2.0, "Average policy shift should stay within the policy range.");
            assertTrue(report.averageProposerGain() >= 0.0 && report.averageProposerGain() <= 2.0, "Average proposer gain should stay within the policy range.");
            assertRatio(report.lobbyCaptureIndex(), "Lobby capture index should be a ratio.");
            assertRatio(report.publicAlignmentScore(), "Public alignment should be a ratio.");
            assertRatio(report.antiLobbyingSuccessRate(), "Anti-lobbying success should be a ratio.");
            assertTrue(report.privateGainRatio() >= 0.0 && report.privateGainRatio() <= 5.0, "Private gain ratio should stay within the configured cap.");
            assertNonNegativeFinite(report.lobbySpendPerBill(), "Lobby spend per bill should be finite and nonnegative.");
            assertRatio(report.defensiveLobbyingShare(), "Defensive lobbying share should be a ratio.");
            assertNonNegativeFinite(report.captureReturnOnSpend(), "Capture return on spend should be finite and nonnegative.");
            assertRatio(report.publicPreferenceDistortion(), "Public-preference distortion should be a ratio.");
            assertRatio(report.administrativeCostIndex(), "Administrative cost should be a ratio.");
            assertRatio(report.amendmentRate(), "Amendment rate should be a ratio.");
            assertNonNegativeFinite(report.averageAmendmentMovement(), "Average amendment movement should be finite and nonnegative.");
            assertRatio(report.minorityHarmIndex(), "Minority harm should be a ratio.");
            assertRatio(report.concentratedHarmPassageRate(), "Concentrated-harm passage rate should be a ratio.");
            assertRatio(report.compensationRate(), "Compensation rate should be a ratio.");
            assertRatio(report.legitimacyScore(), "Legitimacy should be a ratio.");
            assertRatio(report.reversalRate(), "Reversal rate should be a ratio.");
            assertRatio(report.lowSupportActiveLawShare(), "Low-support active-law share should be a ratio.");
            assertRatio(report.statusQuoWinRate(), "Status-quo win rate should be a ratio.");
            assertRatio(report.citizenReviewRate(), "Citizen review rate should be a ratio.");
            assertRatio(report.citizenCertificationRate(), "Citizen certification rate should be a ratio.");
            assertRatio(report.citizenLegitimacy(), "Citizen legitimacy should be a ratio.");
            assertRatio(report.objectionWindowRate(), "Objection-window rate should be a ratio.");
            assertRatio(report.repealWindowReversalRate(), "Repeal-window reversal rate should be a ratio.");
            assertRatio(report.fastLaneRate(), "Fast lane rate should be a ratio.");
            assertRatio(report.middleLaneRate(), "Middle lane rate should be a ratio.");
            assertRatio(report.highRiskLaneRate(), "High-risk lane rate should be a ratio.");
            assertRatio(report.challengeExhaustionRate(), "Challenge exhaustion rate should be a ratio.");
            assertRatio(report.falseNegativePassRate(), "False-negative pass rate should be a ratio.");
            assertRatio(report.publicWillReviewRate(), "Public-will review rate should be a ratio.");
            assertRatio(report.crossBlocAdmissionRate(), "Cross-bloc admission rate should be a ratio.");
            assertRatio(report.affectedGroupSponsorshipRate(), "Affected-group sponsorship rate should be a ratio.");
            assertNonNegativeFinite(report.alternativeDiversity(), "Alternative diversity should be finite and nonnegative.");
            assertNonNegativeFinite(report.publicBenefitPerLobbyDollar(), "Public benefit per lobby dollar should be finite and nonnegative.");
            assertNonNegativeFinite(report.attentionSpendPerBill(), "Attention spend per bill should be finite and nonnegative.");
            assertNonNegativeFinite(report.averageCosponsors(), "Average cosponsors should be finite and nonnegative.");
            assertNonNegativeFinite(report.strategicDecoyRate(), "Strategic decoy rate should be finite and nonnegative.");
            assertRatio(report.proposerAccessGini(), "Proposer access Gini should be a ratio.");
            assertRatio(report.welfarePerSubmittedBill(), "Welfare per submitted bill should be a ratio.");
            assertTrue(report.vetoes() >= 0, "Veto count should be nonnegative.");
            assertTrue(report.overriddenVetoes() >= 0 && report.overriddenVetoes() <= report.vetoes(), "Overridden vetoes should be bounded by vetoes.");
            assertRatio(report.interChamberConflictRate(), "Inter-chamber conflict rate should be a ratio.");
            assertRatio(report.secondChamberKillRate(), "Second-chamber kill rate should be a ratio.");
            assertRatio(report.conferenceRate(), "Conference rate should be a ratio.");
            assertRatio(report.conferenceSuccessRate(), "Conference success rate should be a ratio.");
            assertNonNegativeFinite(report.routingDelayCost(), "Routing delay cost should be finite and nonnegative.");
            assertNonNegativeFinite(report.shuttleRoundsToAgreement(), "Shuttle rounds to agreement should be finite and nonnegative.");
            assertRatio(report.suspensiveOverrideRate(), "Suspensive override rate should be a ratio.");
            assertRatio(report.bicameralDeadlockRate(), "Bicameral deadlock rate should be a ratio.");
            assertRatio(report.dischargePetitionRate(), "Discharge petition rate should be a ratio.");
            assertRatio(report.committeeOverrideRate(), "Committee override rate should be a ratio.");
            assertRatio(report.committeeHearingRate(), "Committee hearing rate should be a ratio.");
            assertNonNegativeFinite(report.committeeQueueDelay(), "Committee queue delay should be finite and nonnegative.");
            assertRatio(report.committeeAmendmentValueAdded(), "Committee amendment value-added should be a ratio.");
            assertRatio(report.populationSeatDistortion(), "Population-seat distortion should be a ratio.");
            assertRatio(report.democraticResponsiveness(), "Democratic responsiveness should be a ratio.");
            assertRatio(report.seatVoteDistortion(), "Seat-vote distortion should be a ratio.");
            assertRatio(report.constituencyServiceConcentration(), "Constituency-service concentration should be a ratio.");
            assertRatio(report.regionalTransferBias(), "Regional transfer bias should be a ratio.");
            for (String key : ScenarioReport.SUPPLEMENTAL_METRIC_KEYS) {
                assertRatio(report.supplementalMetric(key), "Supplemental metric " + key + " should be a ratio.");
            }
        }
    }

    private static void metricDirectionMetadataCoversCoreMetrics() {
        assertTrue(
                MetricDefinition.require("productivity").direction() == MetricDirection.HIGHER_IS_BETTER,
                "Productivity should be marked higher-is-better."
        );
        assertTrue(
                MetricDefinition.require("lowSupport").direction() == MetricDirection.LOWER_IS_BETTER,
                "Low-support passage should be marked lower-is-better."
        );
        assertTrue(
                MetricDefinition.require("weakPublicMandatePassage").direction() == MetricDirection.LOWER_IS_BETTER,
                "Weak public-mandate passage should be marked lower-is-better."
        );
        assertTrue(
                MetricDefinition.require("administrativeCost").direction() == MetricDirection.LOWER_IS_BETTER,
                "Administrative cost should be marked lower-is-better."
        );
        assertTrue(
                MetricDefinition.require("policyShift").direction() == MetricDirection.DIAGNOSTIC,
                "Policy shift should remain diagnostic, not automatically good or bad."
        );
        assertTrue(
                MetricDefinition.definitions().size() >= 30,
                "Metric direction registry should cover the report's core metrics."
        );
        assertRatio(MetricDefinition.lowerIsBetter(0.25), "Metric inversion should produce a ratio.");
        assertTrue(
                MetricDefinition.lowerIsBetter(1.0, 2.0) == 0.5,
                "Range-aware metric inversion should normalize policy distances."
        );
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

}
