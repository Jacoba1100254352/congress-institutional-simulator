package congresssim.simulation.catalog;

import congresssim.simulation.*;

import congresssim.institution.accountability.EligibilityDiagnosticsProcess;
import congresssim.institution.accountability.EligibilityRule;
import congresssim.institution.accountability.LawRegistryProcess;
import congresssim.institution.accountability.ProposalBondProcess;
import congresssim.institution.accountability.ProposalCreditProcess;
import congresssim.institution.accountability.QuadraticAttentionBudgetProcess;
import congresssim.institution.accountability.SunsetTrialProcess;
import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.agenda.AgendaLotteryProcess;
import congresssim.institution.agenda.ChallengeEscalationProcess;
import congresssim.institution.agenda.ChallengeTokenAllocation;
import congresssim.institution.agenda.ChallengeVoucherProcess;
import congresssim.institution.agenda.ProposalAccessProcess;
import congresssim.institution.agenda.ProposalAccessRules;
import congresssim.institution.bargaining.AlternativeSelectionRule;
import congresssim.institution.bargaining.AmendmentMediationProcess;
import congresssim.institution.bargaining.CoalitionCosponsorshipProcess;
import congresssim.institution.bargaining.CompetingAlternativesProcess;
import congresssim.institution.bargaining.MultiRoundAmendmentProcess;
import congresssim.institution.bargaining.MultidimensionalPackageBargainingProcess;
import congresssim.institution.bargaining.OmnibusBargainingProcess;
import congresssim.institution.bargaining.PackageBargainingProcess;
import congresssim.institution.chamber.BicameralConflictMode;
import congresssim.institution.chamber.BicameralOriginRule;
import congresssim.institution.chamber.BicameralProcess;
import congresssim.institution.chamber.BicameralRoutingProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberArchitectureSignalProcess;
import congresssim.institution.chamber.ConferenceCommitteeProcess;
import congresssim.institution.chamber.ConstitutionalCourtArchitectureProcess;
import congresssim.institution.chamber.DistrictPopulationProcess;
import congresssim.institution.chamber.PresidentialVetoProcess;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.committee.CommitteeGatekeepingProcess;
import congresssim.institution.committee.CommitteeInformationProcess;
import congresssim.institution.committee.CommitteePowerConfig;
import congresssim.institution.committee.CommitteePowerProcess;
import congresssim.institution.committee.CommitteeRoleMode;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.DistributionalHarmProcess;
import congresssim.institution.distribution.HarmWeightedThresholdProcess;
import congresssim.institution.lobbying.BudgetedLobbyingProcess;
import congresssim.institution.lobbying.InfluenceSystemProcess;
import congresssim.institution.lobbying.LobbyAuditProcess;
import congresssim.institution.lobbying.LobbyTransparencyProcess;
import congresssim.institution.publicinput.CitizenInitiativeProcess;
import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.publicinput.CitizenPanelReviewProcess;
import congresssim.institution.publicinput.ConstituentPublicWillProcess;
import congresssim.institution.publicinput.PublicObjectionWindowProcess;
import congresssim.institution.review.ExAnteReviewMode;
import congresssim.institution.review.ExAnteReviewProcess;
import congresssim.institution.review.IndependentInstitutionBundle;
import congresssim.institution.review.JudicialReviewProcess;
import congresssim.institution.strategy.DemocraticDeteriorationProcess;
import congresssim.institution.strategy.InstitutionalNormErosionProcess;
import congresssim.institution.strategy.LongHorizonStrategyProcess;
import congresssim.institution.strategy.ProposerStrategyProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.institution.voting.DefaultPassUnlessVetoedRule;
import congresssim.institution.voting.VotingRule;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

import static congresssim.simulation.catalog.BroadSystemScenarioBuilders.*;
import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.*;
import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.*;
import static congresssim.simulation.catalog.SharedScenarioBuilders.*;

/**
 * Broad non-default system builders used by the breadth-first catalog family.
 */
final class BroadSystemScenarioBuilders {
    private BroadSystemScenarioBuilders() {
    }

    static Scenario majorityWithCommitteeRegularOrder() {
        return new Scenario() {
            @Override
            public String name() {
                return "Committee-first regular order";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.86, 0.42, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.34, 0.82),
                        process
                );
            }
        };
    }

    static Scenario leadershipCartelMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Leadership agenda cartel + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.54,
                                0.42,
                                0.34,
                                0.18,
                                0.22,
                                0.16
                        ),
                        simpleMajorityFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    static Scenario clotureConferenceAndJudicialReview() {
        return new Scenario() {
            @Override
            public String name() {
                return "Cloture, conference, and judicial review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.MAJORITY_CONTROLLED,
                        17
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber house = new Chamber(
                        "House",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate cloture",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess process = new ConferenceCommitteeProcess(
                        name(),
                        house,
                        senate,
                        0.45,
                        chamberMedian(world.legislators()),
                        0.32,
                        0.30
                );
                process = new PresidentialVetoProcess(
                        process,
                        presidentFromWorld(world),
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                process = new JudicialReviewProcess(name(), process, 0.48, 0.66, 0.46);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.78, 0.48, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.56,
                                0.44,
                                0.30,
                                0.18,
                                0.18,
                                0.14
                        ),
                        process
                );
            }
        };
    }

    static Scenario citizenInitiativeReferendum() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen initiative and referendum";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenInitiativeProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.58,
                        0.54,
                        0.42,
                        0.32
                );
            }
        };
    }

    static Scenario majorityWithDistrictPopulation() {
        return new Scenario() {
            @Override
            public String name() {
                return "District-population public-will model";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new DistrictPopulationProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        7,
                        0.42,
                        0.66,
                        0.72
                );
            }
        };
    }

    static Scenario parliamentaryCoalitionConfidence() {
        return new Scenario() {
            @Override
            public String name() {
                return "Parliamentary coalition confidence";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposalCreditProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        1.30,
                        0.34,
                        3.20,
                        0.48,
                        0.76,
                        0.36,
                        0.68,
                        0.50
                );
                return new CoalitionCosponsorshipProcess(
                        name(),
                        process,
                        world.legislators(),
                        3,
                        2,
                        0.14,
                        0.46,
                        false,
                        true
                );
            }
        };
    }

    static Scenario majorityWithPublicInterestScreen() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority + public-interest screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.58, 2.35, 0.56),
                        simpleMajorityFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    static Scenario majorityWithCitizenAssemblyThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen assembly threshold gate";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.62),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.14,
                        0.61
                );
            }
        };
    }

    static Scenario majorityWithCitizenAssemblyManipulationStress() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen assembly under manipulation stress";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        45,
                        0.24,
                        0.50,
                        0.86,
                        0.59
                );
            }
        };
    }

    static Scenario majorityWithAgendaLottery(boolean weighted) {
        return new Scenario() {
            @Override
            public String name() {
                return weighted ? "Weighted agenda lottery + majority" : "Random agenda lottery + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AgendaLotteryProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.bills(),
                        weighted ? 0.46 : 0.42,
                        weighted
                );
            }
        };
    }

    static Scenario majorityWithQuadraticAttentionBudget() {
        return new Scenario() {
            @Override
            public String name() {
                return "Quadratic attention budget + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new QuadraticAttentionBudgetProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        11.5,
                        4
                );
            }
        };
    }

    static Scenario majorityWithProposalBonds() {
        return new Scenario() {
            @Override
            public String name() {
                return "Proposal bonds + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalBondProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        2.20,
                        0.20,
                        4.50,
                        0.40,
                        1.15,
                        0.38,
                        0.70
                );
            }
        };
    }

    static Scenario majorityWithHarmWeightedThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Harm-weighted double majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber highHarm = new Chamber(
                        "Legislature harm review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.64)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.46);
            }
        };
    }

    static Scenario majorityWithLooseHarmClaims() {
        return new Scenario() {
            @Override
            public String name() {
                return "Harm-weighted majority + loose harm claims";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber highHarm = new Chamber(
                        "Legislature loose-claim review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.64)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.22);
            }
        };
    }

    static Scenario majorityWithDistributionalCompensation(boolean requireConsent) {
        return new Scenario() {
            @Override
            public String name() {
                return requireConsent
                        ? "Affected-group consent + majority"
                        : "Compensation amendments + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new DistributionalHarmProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.42,
                        requireConsent ? 0.48 : 0.42,
                        requireConsent ? 0.72 : 0.58,
                        requireConsent ? 0.42 : 0.30,
                        requireConsent
                );
            }
        };
    }

    static Scenario majorityWithPackageBargaining() {
        return new Scenario() {
            @Override
            public String name() {
                return "Package bargaining + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PackageBargainingProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.32,
                        0.10,
                        0.08,
                        0.70
                );
            }
        };
    }

    static Scenario majorityWithMultidimensionalPackageBargaining() {
        return new Scenario() {
            @Override
            public String name() {
                return "Multidimensional package bargaining + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new MultidimensionalPackageBargainingProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.28,
                        4,
                        0.66,
                        0.38,
                        0.54
                );
            }
        };
    }

    static Scenario majorityWithOmnibusBargaining() {
        return new Scenario() {
            @Override
            public String name() {
                return "Omnibus bargaining + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new OmnibusBargainingProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        6,
                        0.58,
                        0.62,
                        0.70
                );
            }
        };
    }

    static Scenario majorityWithLawRegistry() {
        return new Scenario() {
            @Override
            public String name() {
                return "Active-law registry + majority review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LawRegistryProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        5,
                        0.34,
                        0.58,
                        0.82
                );
            }
        };
    }

    static Scenario majorityWithPublicObjectionWindow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Public objection window + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.62),
                        0.42,
                        0.06,
                        false
                );
            }
        };
    }

    static Scenario majorityWithAstroturfObjectionWindow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Public objection window + astroturf stress";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        0.30,
                        0.18,
                        false
                );
            }
        };
    }

    static Scenario majorityWithAntiCaptureBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority + anti-capture bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                        process
                );
                process = new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        0.58,
                        0.62,
                        0.62,
                        0.05,
                        true
                );
            }
        };
    }

    static Scenario majorityWithInfluenceSystem() {
        return new Scenario() {
            @Override
            public String name() {
                return "Campaign-finance influence system";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.46, 0.62, 2.30, 0.54),
                        process
                );
                return new InfluenceSystemProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.68,
                        0.62,
                        0.66,
                        0.34
                );
            }
        };
    }

    static Scenario majorityWithConstitutionalCourtArchitecture() {
        return new Scenario() {
            @Override
            public String name() {
                return "Constitutional court architecture";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new DistributionalHarmProcess(
                        name(),
                        process,
                        0.42,
                        0.44,
                        0.62,
                        0.30,
                        false
                );
                return new ConstitutionalCourtArchitectureProcess(
                        name(),
                        process,
                        13,
                        0.35,
                        0.64,
                        0.72,
                        0.76,
                        0.82,
                        true
                );
            }
        };
    }

    static Scenario riskRoutedMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Risk-routed majority legislature";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.025,
                        1.15,
                        0.08
                );
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.12,
                        0.62
                );
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.30,
                        0.58
                );
            }
        };
    }

    static Scenario portfolioHybridLegislature() {
        return new Scenario() {
            @Override
            public String name() {
                return "Portfolio hybrid legislature";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy standard = VotingStrategies.standard();
                VotingStrategy antiCapture = VotingStrategies.antiCapture();

                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, standard);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, standard),
                        world.legislators(),
                        3,
                        0.023,
                        1.18,
                        0.055
                );
                middleLane = new CompetingAlternativesProcess(
                        name(),
                        middleLane,
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        0,
                        0,
                        0.92,
                        0.012,
                        0.0
                );
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, antiCapture),
                        supermajorityFloorProcess(name(), world, antiCapture, 0.65),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.84,
                        0.12,
                        0.62
                );
                highRiskLane = new DistributionalHarmProcess(
                        name(),
                        highRiskLane,
                        0.40,
                        0.43,
                        0.66,
                        0.31,
                        false
                );
                LegislativeProcess process = new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.28,
                        0.56
                );
                process = new LobbyAuditProcess(name(), process, 0.08, 0.70, 0.46, 0.50, true);
                process = new ProposalBondProcess(name(), process, 2.70, 0.22, 4.80, 0.24, 0.78, 0.30, 0.90);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.40, 0.70, 2.80, 0.52),
                        process
                );
                process = new LobbyTransparencyProcess(name(), 0.70, 0.30, process);
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.20,
                        0.40,
                        0.32,
                        0.48,
                        0.45,
                        0.40,
                        0.06,
                        true
                );
                return new LawRegistryProcess(name(), process, 4, 0.32, 0.58, 0.76);
            }
        };
    }

    static Scenario expandedPortfolioHybridLegislature() {
        return new Scenario() {
            @Override
            public String name() {
                return "Expanded portfolio hybrid legislature";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy standard = VotingStrategies.standard();
                VotingStrategy antiCapture = VotingStrategies.antiCapture();
                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, standard);
                LegislativeProcess middleLane = new OmnibusBargainingProcess(
                        name(),
                        new CompetingAlternativesProcess(
                                name(),
                                simpleMajorityFloorProcess(name(), world, standard),
                                world.legislators(),
                                AlternativeSelectionRule.PAIRWISE_MAJORITY,
                                4,
                                true,
                                0,
                                0,
                                0.92,
                                0.012,
                                0.0
                        ),
                        5,
                        0.56,
                        0.66,
                        0.68
                );
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, antiCapture),
                        supermajorityFloorProcess(name(), world, antiCapture, 0.65),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.84,
                        0.12,
                        0.62
                );
                highRiskLane = new DistributionalHarmProcess(
                        name(),
                        highRiskLane,
                        0.40,
                        0.43,
                        0.66,
                        0.31,
                        false
                );
                LegislativeProcess process = new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.28,
                        0.56
                );
                process = new ConstitutionalCourtArchitectureProcess(
                        name(),
                        process,
                        13,
                        0.32,
                        0.66,
                        0.76,
                        0.82,
                        0.84,
                        true
                );
                process = new InfluenceSystemProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.72,
                        0.66,
                        0.70,
                        0.28
                );
                process = new DistrictPopulationProcess(name(), process, world.legislators(), 7, 0.36, 0.68, 0.70);
                process = new LongHorizonStrategyProcess(name(), process, world.legislators(), 20, 0.62, 0.72);
                process = new ProposalBondProcess(name(), process, 2.70, 0.22, 4.80, 0.24, 0.78, 0.30, 0.90);
                return new LawRegistryProcess(name(), process, 4, 0.32, 0.58, 0.76);
            }
        };
    }

    static Scenario riskRoutedNoCitizenReviewMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Risk-routed majority without citizen review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.025,
                        1.15,
                        0.08
                );
                LegislativeProcess highRiskLane = supermajorityFloorProcess(name(), world, strategy, 0.64);
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.30,
                        0.58
                );
            }
        };
    }

    static Scenario normErosionMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Endogenous norm erosion + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposerStrategyProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        0.58,
                        0.58,
                        0.46
                );
                return new InstitutionalNormErosionProcess(
                        name(),
                        process,
                        0.18,
                        0.42,
                        0.16
                );
            }
        };
    }

    static Scenario longHorizonLearningMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Long-horizon strategic learning";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.024,
                        1.14,
                        0.06
                );
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.18,
                        0.40,
                        0.30,
                        true
                );
                return new LongHorizonStrategyProcess(
                        name(),
                        process,
                        world.legislators(),
                        20,
                        0.68,
                        0.70
                );
            }
        };
    }

    static Scenario democraticDeteriorationMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Democratic deterioration stress + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposerStrategyProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        0.62,
                        0.56,
                        0.44
                );
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.34,
                        true
                );
                return new DemocraticDeteriorationProcess(
                        name(),
                        process,
                        0.16,
                        0.38,
                        0.46,
                        0.34,
                        0.42,
                        0.10
                );
            }
        };
    }
}
