package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaDisposition;
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
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.CompetingAlternativesProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.DistributionalHarmProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalCreditProcess;
import congresssim.institution.SunsetTrialProcess;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
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
        adaptiveTrackRoutesBillsByRisk();
        sunsetTrialExpiresRiskyLowBenefitBills();
        proposalCreditsLearnFromProposalQuality();
        lobbyTransparencyReducesCapturedBillPressure();
        budgetedLobbyingSpendsDefensivelyAgainstAntiLobbyingReforms();
        budgetedLobbyingRecordsChannelSpecificSpend();
        amendmentMediationMovesRiskyBillsTowardMedian();
        distributionalHarmProcessCompensatesAffectedGroups();
        lawRegistryReviewsAndRepealsBadActiveLaws();
        competingAlternativesSelectCompromiseBeforeFinalVote();
        citizenPanelRoutesUncertifiedBillsToReview();
        publicInterestScreenBlocksCapturedBillsButAllowsAntiLobbyingReforms();
        lobbyAuditCanReverseCapturedEnactments();
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

    private static void adaptiveTrackRoutesBillsByRisk() {
        LegislativeProcess fast = labeledProcess("fast lane");
        LegislativeProcess middle = labeledProcess("middle lane");
        LegislativeProcess highRisk = labeledProcess("high-risk lane");
        AdaptiveTrackProcess process = new AdaptiveTrackProcess(
                "adaptive test",
                fast,
                middle,
                highRisk,
                0.34,
                0.58
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill lowRisk = new Bill("B-low", "Low Risk", "L-1", 0.0, 0.05, 0.85, 0.80, -0.2, 0.20);
        Bill highRiskBill = new Bill("B-high", "High Risk", "L-1", 0.0, 0.90, 0.15, 0.20, 0.8, 0.90);

        assertTrue(
                process.consider(lowRisk, context).finalReason().equals("fast lane"),
                "Low-risk bills should use the fast lane."
        );
        assertTrue(
                process.consider(highRiskBill, context).finalReason().equals("high-risk lane"),
                "High-risk bills should use the high-risk review lane."
        );
    }

    private static void sunsetTrialExpiresRiskyLowBenefitBills() {
        LegislativeProcess enactEverything = new LegislativeProcess() {
            @Override
            public String name() {
                return "enact everything";
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
                        "enacted"
                );
            }
        };
        SunsetTrialProcess process = new SunsetTrialProcess("sunset test", enactEverything, 0.20, 0.56);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill badRiskyBill = new Bill("B-bad", "Bad Risky Bill", "L-1", 0.0, 0.95, 0.10, 0.10, 0.8, 0.95);
        Bill strongBill = new Bill("B-good", "Good Bill", "L-1", 0.0, 0.40, 0.85, 0.85, 0.0, 0.50);

        BillOutcome expired = process.consider(badRiskyBill, context);
        BillOutcome renewed = process.consider(strongBill, context);

        assertFalse(expired.enacted(), "Risky low-benefit bills should expire after sunset review.");
        assertTrue(expired.statusQuoAfter() == context.currentPolicyPosition(), "Expired trials should roll back the status quo.");
        assertTrue(renewed.enacted(), "Strong bills should survive sunset review.");
    }

    private static void proposalCreditsLearnFromProposalQuality() {
        LegislativeProcess enactEverything = new LegislativeProcess() {
            @Override
            public String name() {
                return "enact everything";
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
                        "enacted"
                );
            }
        };
        ProposalCreditProcess process = new ProposalCreditProcess(
                "credit test",
                enactEverything,
                1.00,
                0.0,
                2.0,
                0.40,
                0.40,
                0.30,
                0.90,
                0.90
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill strongBill = new Bill("B-good", "Good Bill", "L-1", 0.0, 0.05, 0.90, 0.90, -0.2, 0.20);
        Bill weakBill = new Bill("B-bad", "Bad Bill", "L-1", 0.0, 0.95, 0.05, 0.05, 0.9, 0.95);

        assertTrue(process.consider(strongBill, context).enacted(), "High-quality proposals should be able to earn credit.");
        assertTrue(process.consider(weakBill, context).enacted(), "A sponsor with earned credits can still spend them on a bad bill.");
        assertTrue(
                process.consider(weakBill, context).agendaDisposition() == AgendaDisposition.ACCESS_DENIED,
                "Low-quality proposals should deplete earned credits and block later proposals."
        );
    }

    private static void lobbyTransparencyReducesCapturedBillPressure() {
        Bill capturedBill = new Bill("B-capture", "Capture Bill", "L-1", 0.0, 0.10, 0.40, 0.20, 0.90, 0.70, 0.90, false);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        LegislativeProcess captureRevisedBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture revised bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(
                        bill.lobbyPressure() < capturedBill.lobbyPressure(),
                        "Transparency should reduce effective lobby pressure."
                );
                assertTrue(
                        bill.publicSupport() < capturedBill.publicSupport(),
                        "Transparency should create public backlash against high-capture bills."
                );
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "captured");
            }
        };

        new LobbyTransparencyProcess("transparency test", 0.75, 0.40, captureRevisedBill)
                .consider(capturedBill, context);
    }

    private static void budgetedLobbyingSpendsDefensivelyAgainstAntiLobbyingReforms() {
        Bill antiLobbyingBill = new Bill("B-reform", "Anti-Lobbying Reform", "L-1", 0.0, 0.05, 0.75, 0.85, -0.30, 0.85, 0.0, true, "democracy", 0.0, 0.0);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        List<LobbyGroup> groups = List.of(new LobbyGroup("G-1", "democracy", 0.7, 2.0, 0.8, 2.0, 0.6, 0.6));
        LegislativeProcess capturePressuredBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture pressured bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(bill.lobbySpend() > 0.0, "Budgeted lobbying should spend against salient reform.");
                assertTrue(bill.defensiveLobbySpend() > 0.0, "Anti-lobbying reform should be marked as defensive spend.");
                assertTrue(bill.lobbyPressure() < antiLobbyingBill.lobbyPressure(), "Defensive lobbying should increase pressure against reform.");
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "captured");
            }
        };

        new BudgetedLobbyingProcess("budgeted lobbying test", capturePressuredBill, groups, 0.30, 0.50, 0.25)
                .consider(antiLobbyingBill, context);
    }

    private static void budgetedLobbyingRecordsChannelSpecificSpend() {
        Bill captureBill = new Bill("B-capture", "Capture Bill", "L-1", 0.0, 0.55, 0.28, 0.30, 0.45, 0.80, 0.80, false, "energy", 0.0, 0.0);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        List<LobbyGroup> groups = List.of(new LobbyGroup(
                "G-info",
                "energy",
                Map.of("energy", 1.0),
                0.50,
                2.0,
                0.9,
                1.0,
                0.9,
                0.4,
                LobbyCaptureStrategy.INFORMATION_DISTORTION,
                0.05
        ));
        LegislativeProcess capturePressuredBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture channel bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(bill.lobbySpend() > 0.0, "Channel lobbying should spend on aligned bills.");
                assertTrue(bill.informationLobbySpend() > bill.directLobbySpend(), "Information strategy should allocate most spending to information distortion.");
                assertTrue(bill.publicBenefit() < captureBill.publicBenefit(), "Information distortion should lower perceived public benefit.");
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "captured");
            }
        };

        new BudgetedLobbyingProcess(
                "channel lobbying test",
                capturePressuredBill,
                groups,
                0.35,
                0.50,
                0.25,
                0.0,
                0.0,
                0.0,
                1.0
        ).consider(captureBill, context);
    }

    private static void amendmentMediationMovesRiskyBillsTowardMedian() {
        Bill riskyBill = new Bill("B-mediate", "Risky Bill", "L-3", 0.9, 0.95, 0.18, 0.32, 0.70, 0.90);
        VoteContext context = new VoteContext(Map.of("Left", -0.6, "Center", 0.0, "Right", 0.6), new Random(1L), 0.0);
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.6, 0.7, 0.4, 0.8, 0.2, 0.8),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-3", "Right", 0.6, 0.7, 0.4, 0.8, 0.2, 0.8)
        );
        LegislativeProcess captureBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture mediated bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(bill.amendmentMovement() > 0.0, "Mediation should record policy movement.");
                assertTrue(
                        Math.abs(bill.ideologyPosition()) < Math.abs(riskyBill.ideologyPosition()),
                        "Mediation should move risky bills toward the chamber median/status quo."
                );
                assertTrue(
                        bill.publicSupport() >= riskyBill.publicSupport(),
                        "Mediation should not reduce the public-support signal for a moderated bill."
                );
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "captured");
            }
        };

        new AmendmentMediationProcess(
                "mediation test",
                captureBill,
                legislators,
                0.0,
                0.90,
                0.70,
                0.20,
                0.10
        ).consider(riskyBill, context);
    }

    private static void distributionalHarmProcessCompensatesAffectedGroups() {
        Bill harmfulBill = new Bill(
                "B-harm",
                "Harmful Bill",
                "L-1",
                0.0,
                0.35,
                0.70,
                0.72,
                0.0,
                0.60,
                0.10,
                false,
                "housing",
                0.0,
                0.0,
                "low-income",
                0.18,
                0.80,
                0.20
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        LegislativeProcess captureBill = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture compensated bill";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(bill.compensationAdded(), "High-harm bills should receive compensation amendments.");
                assertTrue(bill.concentratedHarm() < harmfulBill.concentratedHarm(), "Compensation should reduce concentrated harm.");
                assertTrue(bill.affectedGroupSupport() > harmfulBill.affectedGroupSupport(), "Compensation should improve affected-group support.");
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "captured");
            }
        };

        new DistributionalHarmProcess("distribution test", captureBill, 0.40, 0.40, 0.60, 0.25, false)
                .consider(harmfulBill, context);
    }

    private static void lawRegistryReviewsAndRepealsBadActiveLaws() {
        LegislativeProcess enactEverything = new LegislativeProcess() {
            @Override
            public String name() {
                return "enact everything";
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
                        "enacted"
                );
            }
        };
        LawRegistryProcess process = new LawRegistryProcess("registry test", enactEverything, 1, 0.10, 0.80, 1.0);
        VoteContext firstContext = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill badLaw = new Bill("B-bad-law", "Bad Law", "L-1", 0.0, 0.80, 0.12, 0.12, 0.80, 0.90);
        Bill nextBill = new Bill("B-next", "Next Bill", "L-1", 0.0, 0.10, 0.80, 0.80, 0.0, 0.20);

        process.consider(badLaw, firstContext);
        BillOutcome reviewed = process.consider(
                nextBill,
                new VoteContext(Map.of("Test", 0.0), new Random(2L), badLaw.ideologyPosition())
        );

        assertTrue(reviewed.signals().lawReviews() > 0, "Registry should review due provisional laws.");
        assertTrue(reviewed.signals().lawReversals() > 0, "Low-benefit active laws should be reversed.");
        assertTrue(reviewed.statusQuoAfter() < badLaw.ideologyPosition(), "Registry reversal should roll back status-quo movement.");
    }

    private static void competingAlternativesSelectCompromiseBeforeFinalVote() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.4, 0.8, 0.4, 0.8, 0.1, 0.8),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-3", "Right", 0.4, 0.8, 0.4, 0.8, 0.1, 0.8)
        );
        LegislativeProcess captureSelected = new LegislativeProcess() {
            @Override
            public String name() {
                return "capture selected alternative";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                assertTrue(
                        Math.abs(bill.ideologyPosition()) < 0.20,
                        "Median-selection tournaments should advance a compromise alternative."
                );
                return new BillOutcome(
                        bill,
                        context.currentPolicyPosition(),
                        bill.ideologyPosition(),
                        true,
                        List.of(),
                        congresssim.institution.PresidentialAction.none(),
                        "selected alternative enacted"
                );
            }
        };
        Bill narrowBill = new Bill("B-alt", "Narrow Bill", "L-1", 0.8, 0.90, 0.36, 0.42, 0.20, 0.70);
        VoteContext context = new VoteContext(Map.of("Left", -0.4, "Center", 0.0, "Right", 0.4), new Random(1L), 0.0);

        BillOutcome outcome = new CompetingAlternativesProcess(
                "alternative test",
                captureSelected,
                legislators,
                AlternativeSelectionRule.CLOSEST_TO_CHAMBER_MEDIAN,
                1,
                false
        ).consider(narrowBill, context);

        assertTrue(outcome.enacted(), "Selected alternatives should continue to final yes/no ratification.");
        assertTrue(outcome.signals().alternativeRounds() == 1, "Alternative tournaments should record a tournament round.");
        assertTrue(outcome.signals().alternativesConsidered() == 2, "Original bill plus generated alternative should be counted.");
    }

    private static void citizenPanelRoutesUncertifiedBillsToReview() {
        LegislativeProcess certified = labeledProcess("certified default lane");
        LegislativeProcess uncertified = labeledProcess("uncertified active lane");
        CitizenPanelReviewProcess process = new CitizenPanelReviewProcess(
                "citizen panel test",
                certified,
                uncertified,
                CitizenPanelMode.DEFAULT_PASS_ELIGIBILITY,
                75,
                0.0,
                1.0,
                0.0,
                0.60
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill weakBill = new Bill(
                "B-jury",
                "Weak Bill",
                "L-1",
                0.0,
                0.80,
                0.15,
                0.10,
                0.40,
                0.80,
                0.70,
                false,
                "housing",
                0.0,
                0.0,
                "low-income",
                0.10,
                0.80,
                0.20
        );

        BillOutcome outcome = process.consider(weakBill, context);

        assertTrue(outcome.finalReason().equals("uncertified active lane"), "Uncertified bills should route to the configured review lane.");
        assertTrue(outcome.signals().citizenReviews() == 1, "Citizen panels should record review activity.");
        assertTrue(outcome.signals().citizenCertifications() == 0, "Low-legitimacy bills should not be certified.");
        assertFalse(outcome.bill().citizenCertified(), "The revised bill should retain the certification result.");
    }

    private static void publicInterestScreenBlocksCapturedBillsButAllowsAntiLobbyingReforms() {
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill capturedBill = new Bill("B-capture", "Capture Bill", "L-1", 0.0, 0.10, 0.30, 0.18, 0.95, 0.80, 0.95, false);
        Bill antiLobbyingBill = new Bill("B-reform", "Anti-Lobbying Reform", "L-1", 0.0, 0.05, 0.62, 0.82, -0.80, 0.80, 0.0, true);

        assertFalse(
                ProposalAccessRules.publicInterestScreen(0.54, 0.58, 2.40, 0.58)
                        .evaluate(capturedBill, context)
                        .granted(),
                "High-private-gain, low-public-interest bills should fail the public-interest screen."
        );
        assertTrue(
                ProposalAccessRules.publicInterestScreen(0.54, 0.58, 2.40, 0.58)
                        .evaluate(antiLobbyingBill, context)
                        .granted(),
                "Public-benefit anti-lobbying reforms should clear the screen despite lobby opposition."
        );
    }

    private static void lobbyAuditCanReverseCapturedEnactments() {
        LegislativeProcess enactEverything = new LegislativeProcess() {
            @Override
            public String name() {
                return "enact everything";
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
                        "enacted"
                );
            }
        };
        LobbyAuditProcess process = new LobbyAuditProcess("audit test", enactEverything, 1.0, 0.0, 0.20, 0.60, true);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        Bill capturedBill = new Bill("B-capture", "Capture Bill", "L-1", 0.0, 0.80, 0.15, 0.10, 0.95, 0.90, 0.95, false);

        BillOutcome outcome = process.consider(capturedBill, context);
        assertFalse(outcome.enacted(), "Failed anti-capture audits should reverse captured enactments when configured.");
        assertTrue(outcome.statusQuoAfter() == context.currentPolicyPosition(), "Audit reversals should roll back the status quo.");
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
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-adaptive-track"),
                "Scenario catalog should expose adaptive-track keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-sunset-trial"),
                "Scenario catalog should expose sunset-trial keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-earned-credits"),
                "Scenario catalog should expose earned proposal-credit keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-anti-capture-bundle"),
                "Scenario catalog should expose anti-capture scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-budgeted-lobbying"),
                "Scenario catalog should expose budgeted-lobbying scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-mediation"),
                "Scenario catalog should expose mediation scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-budgeted-lobbying-mediation"),
                "Scenario catalog should expose budgeted lobbying plus mediation scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-alternatives-pairwise"),
                "Scenario catalog should expose competing-alternatives scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-lobby-channel-bundle"),
                "Scenario catalog should expose lobbying-channel scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-citizen-certificate"),
                "Scenario catalog should expose citizen-panel scenario keys."
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

    private static LegislativeProcess labeledProcess(String label) {
        return new LegislativeProcess() {
            @Override
            public String name() {
                return label;
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
                        label
                );
            }
        };
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
