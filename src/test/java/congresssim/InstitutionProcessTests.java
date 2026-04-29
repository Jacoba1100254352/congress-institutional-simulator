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
import congresssim.institution.ProposerStrategyProcess;
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

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.Set;

import static congresssim.TestSupport.*;
final class InstitutionProcessTests {
    private InstitutionProcessTests() {
    }

    static void run() {
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
        strategicLobbyingReallocatesChannelStrategy();
        strategicLobbyingAdaptsBudgetAndDefensiveThreat();
        amendmentMediationMovesRiskyBillsTowardMedian();
        distributionalHarmProcessCompensatesAffectedGroups();
        lawRegistryReviewsAndRepealsBadActiveLaws();
        competingAlternativesSelectCompromiseBeforeFinalVote();
        citizenPanelRoutesUncertifiedBillsToReview();
        agendaLotteryRationsFloorSlots();
        quadraticAttentionBudgetDeniesExpensiveProposals();
        publicObjectionWindowRoutesContestedBills();
        constituentPublicWillRevisesSignals();
        proposalBondForfeitsLowQualityBills();
        proposerStrategyModeratesThenWithdrawsWeakBills();
        proposerStrategyAdaptsTimingHarmAndLobbyExposure();
        coalitionCosponsorshipRecordsSponsors();
        multiRoundMediationReducesHarm();
        strategicAlternativesRecordDecoys();
        challengeVouchersReportTokenExhaustion();
        publicInterestScreenBlocksCapturedBillsButAllowsAntiLobbyingReforms();
        lobbyAuditCanReverseCapturedEnactments();
        challengeVouchersRouteHighRiskBillsToActiveVote();
        challengeEscalationRoutesBroadlyContestedBillsToActiveVote();
        committeeGateBlocksBillsBeforeFloor();
        committeeInformationMovesPublicSignalTowardBenefit();
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

    private static void strategicLobbyingReallocatesChannelStrategy() {
        Bill firstBill = new Bill("B-first", "First Bill", "L-1", 0.0, 0.85, 0.35, 0.42, 0.20, 0.55, 0.40, false, "energy", 0.0, 0.0);
        Bill secondBill = new Bill("B-second", "Second Bill", "L-1", 0.0, 0.85, 0.35, 0.42, 0.20, 0.55, 0.40, false, "energy", 0.0, 0.0);
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(1L), 0.0);
        List<LobbyGroup> groups = List.of(new LobbyGroup(
                "G-adaptive",
                "energy",
                Map.of("energy", 1.0),
                0.85,
                5.0,
                0.9,
                1.0,
                0.5,
                0.4,
                LobbyCaptureStrategy.DIRECT_PRESSURE,
                0.5
        ));
        LegislativeProcess capturePressuredBill = new LegislativeProcess() {
            private int calls;

            @Override
            public String name() {
                return "adaptive lobby capture";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                calls++;
                if (calls == 1) {
                    assertTrue(bill.directLobbySpend() > bill.agendaLobbySpend(), "Initial direct-pressure strategy should spend most on direct pressure.");
                } else {
                    assertTrue(bill.agendaLobbySpend() > bill.directLobbySpend(), "Strategic lobbying should reallocate toward agenda access after a failed extreme proposal.");
                }
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "not enacted");
            }
        };

        BudgetedLobbyingProcess process = new BudgetedLobbyingProcess(
                "adaptive channel lobbying test",
                capturePressuredBill,
                groups,
                0.45,
                0.44,
                0.35,
                true
        );

        process.consider(firstBill, context);
        process.consider(secondBill, context);
    }

    private static void strategicLobbyingAdaptsBudgetAndDefensiveThreat() {
        Bill reformBill = new Bill(
                "B-reform",
                "Lobbying Reform",
                "L-1",
                0.0,
                0.05,
                0.72,
                0.74,
                0.15,
                0.82,
                0.70,
                true,
                "democracy",
                0.0,
                0.0
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(4L), 0.0);
        List<LobbyGroup> groups = List.of(new LobbyGroup(
                "G-threat",
                "energy",
                Map.of("energy", 0.8, "democracy", 1.0),
                0.85,
                8.0,
                0.9,
                1.4,
                0.5,
                0.9,
                LobbyCaptureStrategy.PUBLIC_CAMPAIGN,
                0.25
        ));
        List<Double> defensiveSpends = new java.util.ArrayList<>();
        LegislativeProcess rejectReform = new LegislativeProcess() {
            @Override
            public String name() {
                return "reject reform";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                defensiveSpends.add(bill.defensiveLobbySpend());
                return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "reform blocked");
            }
        };

        BudgetedLobbyingProcess process = new BudgetedLobbyingProcess(
                "adaptive defensive lobbying",
                rejectReform,
                groups,
                0.32,
                0.44,
                0.38,
                true
        );

        process.consider(reformBill, context);
        process.consider(reformBill, context);
        process.consider(reformBill, context);

        assertTrue(defensiveSpends.size() == 3, "The adaptive lobby test should observe all three reform attempts.");
        assertTrue(defensiveSpends.get(0) > 0.0, "Anti-lobbying reform should trigger defensive spending.");
        assertTrue(
                defensiveSpends.get(2) >= defensiveSpends.get(1) || defensiveSpends.get(1) >= defensiveSpends.get(0),
                "Repeated reform threats should increase or sustain defensive lobbying intensity."
        );
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


    private static void agendaLotteryRationsFloorSlots() {
        Bill firstBill = new Bill("B-lottery-1", "Lottery Bill 1", "L-1", 0.0, 0.10, 0.65, 0.70, 0.0, 0.40);
        Bill secondBill = new Bill("B-lottery-2", "Lottery Bill 2", "L-2", 0.0, -0.10, 0.55, 0.60, 0.0, 0.40);
        AgendaLotteryProcess process = new AgendaLotteryProcess(
                "lottery test",
                labeledProcess("selected by lottery"),
                List.of(firstBill, secondBill),
                0.50,
                false
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(3L), 0.0);

        BillOutcome firstOutcome = process.consider(firstBill, context);
        BillOutcome secondOutcome = process.consider(secondBill, context);

        int denied = (firstOutcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED ? 1 : 0)
                + (secondOutcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED ? 1 : 0);
        assertTrue(denied == 1, "A half-size agenda lottery should admit exactly one of two bills.");
    }


    private static void quadraticAttentionBudgetDeniesExpensiveProposals() {
        QuadraticAttentionBudgetProcess process = new QuadraticAttentionBudgetProcess(
                "attention test",
                labeledProcess("attention admitted"),
                List.of(legislator("L-1")),
                2.0,
                4
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(4L), 0.0);
        Bill costlyBill = new Bill("B-costly", "Costly Bill", "L-1", 0.0, 0.95, 0.10, 0.20, 0.80, 0.95);

        BillOutcome outcome = process.consider(costlyBill, context);

        assertTrue(outcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED, "Insufficient attention credits should deny costly proposals.");
    }


    private static void publicObjectionWindowRoutesContestedBills() {
        PublicObjectionWindowProcess process = new PublicObjectionWindowProcess(
                "objection test",
                labeledProcess("default lane"),
                labeledProcess("active review lane"),
                0.20,
                0.0,
                false
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(5L), 0.0);
        Bill contestedBill = new Bill(
                "B-objection",
                "Contested Bill",
                "L-1",
                0.0,
                0.90,
                0.10,
                0.15,
                0.70,
                0.90,
                0.80,
                false,
                "housing",
                0.0,
                0.0,
                "low-income",
                0.10,
                0.80,
                0.20
        );

        BillOutcome outcome = process.consider(contestedBill, context);

        assertTrue(outcome.finalReason().equals("active review lane"), "Contested bills should route to active review.");
        assertTrue(outcome.signals().objectionWindows() == 1, "Triggered objection windows should be recorded.");
    }


    private static void constituentPublicWillRevisesSignals() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.45, 0.8, 0.4, 0.9, 0.1, 0.8, -0.35, 0.9, 0.8),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.3, 0.9, 0.1, 0.9, -0.05, 0.8, 0.7),
                new Legislator("L-3", "Right", 0.45, 0.7, 0.5, 0.8, 0.1, 0.8, 0.10, 0.7, 0.6)
        );
        Bill bill = new Bill(
                "B-public-will",
                "Public Will Bill",
                "L-1",
                -0.45,
                -0.20,
                0.20,
                0.75,
                0.0,
                0.30,
                0.10,
                false,
                "health",
                0.0,
                0.0,
                "patients",
                0.20,
                0.25,
                0.10
        ).withPublicBenefitUncertainty(0.60);
        VoteContext context = new VoteContext(Map.of("Left", -0.45, "Center", 0.0, "Right", 0.45), new Random(9L), 0.0);

        BillOutcome outcome = new ConstituentPublicWillProcess(
                "public will test",
                labeledProcess("public will revised"),
                legislators,
                1.0,
                0.25
        ).consider(bill, context);

        assertTrue(outcome.signals().publicWillReviews() == 1, "Public-will review should be recorded.");
        assertTrue(outcome.signals().publicSignalMovement() > 0.0, "Public-will review should move at least one signal.");
        assertTrue(outcome.signals().districtAlignment() > bill.publicSupport(), "District estimate should raise support for a district-aligned bill.");
        assertTrue(outcome.bill().publicSupport() > bill.publicSupport(), "Bill support should be revised toward district public will.");
        assertTrue(outcome.bill().publicBenefitUncertainty() < bill.publicBenefitUncertainty(), "Public-will review should reduce uncertainty when update strength is high.");
    }


    private static void proposalBondForfeitsLowQualityBills() {
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
        ProposalBondProcess process = new ProposalBondProcess(
                "bond test",
                enactEverything,
                2.0,
                0.0,
                2.0,
                0.25,
                0.65,
                0.40,
                0.10
        );
        VoteContext context = new VoteContext(Map.of("Test", 0.0), new Random(10L), 0.0);
        Bill lowQualityBill = new Bill("B-bond", "Low Quality Bond Bill", "L-1", 0.0, 0.85, 0.12, 0.18, 0.80, 0.90);

        BillOutcome outcome = process.consider(lowQualityBill, context);

        assertTrue(outcome.enacted(), "A proposer with a sufficient bond balance should reach final enactment.");
        assertTrue(outcome.signals().proposalBondReviews() == 1, "Proposal-bond review should be recorded.");
        assertTrue(outcome.signals().proposalBondForfeiture() > 0.0, "Low-quality enacted bills should forfeit part of the bond.");
    }

    private static void proposerStrategyModeratesThenWithdrawsWeakBills() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Right", 0.75, 0.4, 0.6, 0.5, 0.2, 0.5),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-3", "Left", -0.55, 0.8, 0.4, 0.8, 0.1, 0.8)
        );
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
        ProposerStrategyProcess process = new ProposerStrategyProcess(
                "adaptive proposer test",
                enactEverything,
                legislators,
                0.80,
                0.55,
                0.35
        );
        VoteContext context = new VoteContext(Map.of("Right", 0.75, "Center", 0.0, "Left", -0.55), new Random(15L), 0.0);
        Bill weakBill = new Bill(
                "B-weak",
                "Weak Strategic Bill",
                "L-1",
                0.75,
                0.95,
                0.10,
                0.12,
                0.90,
                0.92,
                0.90,
                false,
                "energy",
                0.0,
                0.0,
                "workers",
                0.10,
                0.80,
                0.30
        );

        List<BillOutcome> outcomes = new java.util.ArrayList<>();
        for (int i = 0; i < 8; i++) {
            outcomes.add(process.consider(weakBill, context));
        }
        BillOutcome first = outcomes.getFirst();
        long enacted = outcomes.stream().filter(BillOutcome::enacted).count();
        long denied = outcomes.stream()
                .filter(outcome -> outcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED)
                .count();

        assertTrue(first.bill().amendmentMovement() > 0.0, "Adaptive proposers should moderate high-risk bills before voting.");
        assertTrue(Math.abs(first.bill().ideologyPosition()) < Math.abs(weakBill.ideologyPosition()), "Adaptive proposer moderation should move toward the median/status quo.");
        assertTrue(first.enacted(), "Initial weak proposals should still be able to reach the downstream process.");
        assertTrue(enacted >= 2, "Trust should decline over repeated bad enactments rather than collapsing immediately.");
        assertTrue(denied >= 1, "Repeated poor outcomes should eventually make proposers delay or withdraw risky bills.");
    }

    private static void proposerStrategyAdaptsTimingHarmAndLobbyExposure() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Right", 0.70, 0.4, 0.6, 0.5, 0.2, 0.5),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.4, 0.9, 0.1, 0.9),
                new Legislator("L-3", "Left", -0.55, 0.8, 0.4, 0.8, 0.1, 0.8)
        );
        List<Bill> revisedBills = new java.util.ArrayList<>();
        LegislativeProcess recorder = new LegislativeProcess() {
            @Override
            public String name() {
                return "record revised bills";
            }

            @Override
            public BillOutcome consider(Bill bill, VoteContext context) {
                revisedBills.add(bill);
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
        ProposerStrategyProcess process = new ProposerStrategyProcess(
                "adaptive proposer harm/lobby test",
                recorder,
                legislators,
                0.88,
                0.50,
                0.30
        );
        VoteContext context = new VoteContext(Map.of("Right", 0.70, "Center", 0.0, "Left", -0.55), new Random(21L), 0.0);
        Bill riskyBill = new Bill(
                "B-harm-lobby",
                "Captured Harm Bill",
                "L-1",
                0.70,
                0.92,
                0.12,
                0.22,
                0.95,
                0.86,
                0.84,
                false,
                "energy",
                0.0,
                0.0,
                "workers",
                0.05,
                0.88,
                0.72
        );

        for (int i = 0; i < 10; i++) {
            process.consider(riskyBill, context);
        }

        assertTrue(!revisedBills.isEmpty(), "At least one risky proposal should reach the downstream process after adaptation.");
        Bill firstRevised = revisedBills.getFirst();
        assertTrue(
                firstRevised.concentratedHarm() < riskyBill.concentratedHarm(),
                "Adaptive amendment posture should reduce concentrated harm on high-risk bills."
        );
        assertTrue(
                firstRevised.lobbyPressure() < riskyBill.lobbyPressure(),
                "Adaptive proposers should reduce lobby exposure on high-capture-risk bills."
        );
        assertTrue(
                revisedBills.size() < 10,
                "Adaptive proposal volume and timing should suppress some repeated risky submissions."
        );
    }


    private static void coalitionCosponsorshipRecordsSponsors() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.45, 0.8, 0.4, 0.9, 0.1, 0.8, -0.40, 0.8, 0.4),
                new Legislator("L-2", "Center", -0.02, 0.9, 0.3, 0.9, 0.1, 0.9, -0.05, 0.8, 0.8),
                new Legislator("L-3", "Right", 0.40, 0.9, 0.4, 0.9, 0.1, 0.9, 0.10, 0.8, 0.7),
                new Legislator("L-4", "Right", 0.55, 0.8, 0.5, 0.8, 0.1, 0.8, 0.15, 0.7, 0.6)
        );
        Bill bill = new Bill(
                "B-coalition",
                "Coalition Bill",
                "L-1",
                -0.45,
                0.02,
                0.72,
                0.78,
                0.0,
                0.40,
                0.10,
                false,
                "housing",
                0.0,
                0.0,
                "renters",
                0.62,
                0.18,
                0.10
        );
        VoteContext context = new VoteContext(Map.of("Left", -0.45, "Center", 0.0, "Right", 0.45), new Random(11L), 0.0);

        BillOutcome outcome = new CoalitionCosponsorshipProcess(
                "coalition test",
                labeledProcess("coalition admitted"),
                legislators,
                2,
                2,
                0.20,
                0.45,
                true,
                true
        ).consider(bill, context);

        assertTrue(outcome.agendaDisposition() == AgendaDisposition.FLOOR_CONSIDERED, "A broad coalition should reach the floor.");
        assertTrue(outcome.signals().cosponsorshipReviews() == 1, "Cosponsorship review should be recorded.");
        assertTrue(outcome.signals().crossBlocAdmissions() == 1, "Admitted cross-bloc bills should be counted.");
        assertTrue(outcome.signals().affectedGroupSponsors() == 1, "Affected-group sponsor participation should be counted.");
        assertTrue(outcome.bill().cosponsorCount() >= 2, "The revised bill should store cosponsor count.");
        assertTrue(outcome.bill().publicSupport() > bill.publicSupport(), "Credit discount should boost support signal for broad sponsorship.");
    }


    private static void multiRoundMediationReducesHarm() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.50, 0.9, 0.3, 0.9, 0.1, 0.9, -0.45, 0.9, 0.8),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.3, 0.9, 0.1, 0.9, 0.0, 0.8, 0.9),
                new Legislator("L-3", "Right", 0.55, 0.7, 0.4, 0.8, 0.1, 0.8, 0.20, 0.7, 0.7)
        );
        Bill harmfulBill = new Bill(
                "B-multiround",
                "Multi-Round Bill",
                "L-3",
                0.55,
                0.85,
                0.22,
                0.64,
                0.10,
                0.85,
                0.20,
                false,
                "labor",
                0.0,
                0.0,
                "workers",
                0.18,
                0.85,
                0.32
        ).withPublicBenefitUncertainty(0.65);
        VoteContext context = new VoteContext(Map.of("Left", -0.50, "Center", 0.0, "Right", 0.55), new Random(12L), 0.0);

        BillOutcome outcome = new MultiRoundAmendmentProcess(
                "multi-round test",
                labeledProcess("multi-round revised"),
                legislators,
                4,
                0.01,
                1.20,
                0.0
        ).consider(harmfulBill, context);

        assertTrue(outcome.bill().amendmentMovement() > 0.0, "Multi-round mediation should record amendment movement.");
        assertTrue(outcome.bill().concentratedHarm() < harmfulBill.concentratedHarm(), "Mediation should reduce concentrated harm.");
        assertTrue(outcome.bill().compensationAdded(), "High-harm mediation should add compensation.");
        assertTrue(Math.abs(outcome.bill().ideologyPosition()) < Math.abs(harmfulBill.ideologyPosition()), "Mediation should move content toward compromise.");
    }


    private static void strategicAlternativesRecordDecoys() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Left", -0.50, 0.8, 0.4, 0.8, 0.1, 0.8),
                new Legislator("L-2", "Center", 0.0, 0.9, 0.3, 0.9, 0.1, 0.9),
                new Legislator("L-3", "Right", 0.50, 0.8, 0.4, 0.8, 0.1, 0.8)
        );
        Bill bill = new Bill("B-strategy", "Strategic Alternative Bill", "L-3", 0.50, 0.75, 0.42, 0.62, 0.0, 0.70);
        VoteContext context = new VoteContext(Map.of("Left", -0.50, "Center", 0.0, "Right", 0.50), new Random(13L), 0.0);

        BillOutcome outcome = new CompetingAlternativesProcess(
                "strategic alternatives test",
                labeledProcess("strategic selected"),
                legislators,
                AlternativeSelectionRule.PAIRWISE_MAJORITY,
                4,
                true,
                2,
                2
        ).consider(bill, context);

        assertTrue(outcome.signals().alternativeRounds() == 1, "Alternative tournament should still record the main round.");
        assertTrue(outcome.signals().strategicAlternativeRounds() == 1, "Strategic-alternative diagnostics should be recorded.");
        assertTrue(outcome.signals().strategicDecoys() == 4, "Clone and decoy proposals should be counted.");
    }


    private static void challengeVouchersReportTokenExhaustion() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "Opposition", -0.9, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-2", "Opposition", -0.7, 0.7, 0.6, 0.8, 0.2, 0.8),
                new Legislator("L-3", "Sponsor", 0.8, 0.4, 0.6, 0.5, 0.2, 0.5)
        );
        Bill badBill = new Bill("B-no-token", "Unchallenged Bad Bill", "L-3", 0.8, 0.95, 0.05, 0.10, 0.8, 0.95);
        VoteContext context = new VoteContext(Map.of("Opposition", -0.8, "Sponsor", 0.8), new Random(14L), 0.0);

        BillOutcome outcome = new ChallengeVoucherProcess(
                "exhausted challenge test",
                legislators,
                (legislator, testedBill, voteContext) -> Vote.NAY,
                ChallengeTokenAllocation.PARTY,
                0,
                0.10,
                labeledProcess("unused challenged path")
        ).consider(badBill, context);

        assertFalse(outcome.challenged(), "No challenge should occur when all token banks are empty.");
        assertTrue(outcome.enacted(), "Tokenless default-pass bills should enact by default.");
        assertTrue(outcome.signals().challengeTokenExhaustions() == 1, "Token exhaustion should be diagnosed.");
        assertTrue(outcome.signals().falseNegativePasses() == 1, "Bad unchallenged enactment should be counted as a false negative.");
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

}
