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
 * Default-pass, policy-tournament, challenge, and adjacent safeguard builders.
 */
final class DefaultPassScenarioBuilders {
    private DefaultPassScenarioBuilders() {
    }

    static Scenario simpleMajorityWithMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Unicameral majority + mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return mediationProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world
                );
            }
        };
    }

    static Scenario defaultPassWithMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + mediated amendments";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return mediationProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world
                );
            }
        };
    }

    static Scenario defaultPassWithLobbyFirewall() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby firewall";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                return defaultPassFloorProcess(name(), world, strategy);
            }
        };
    }

    static Scenario defaultPassWithLobbyTransparency() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby transparency";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LobbyTransparencyProcess(
                        name(),
                        0.72,
                        0.30,
                        defaultPassFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    static Scenario defaultPassWithPublicInterestScreen() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + public-interest screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.54, 0.58, 2.40, 0.58),
                        defaultPassFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    static Scenario defaultPassWithLobbyAudit() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + anti-capture audit";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LobbyAuditProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        0.08,
                        0.70,
                        0.48,
                        0.50,
                        true
                );
            }
        };
    }

    static Scenario defaultPassWithAntiCaptureBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + anti-capture bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                        process
                );
                return new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
            }
        };
    }

    static Scenario defaultPassWithBudgetedLobbying(boolean includeTransparency, boolean includeAntiCaptureBundle) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeAntiCaptureBundle) {
                    return "Default pass + budgeted lobbying + anti-capture bundle";
                }
                if (includeTransparency) {
                    return "Default pass + budgeted lobbying + transparency";
                }
                return "Default pass + budgeted lobbying";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = includeAntiCaptureBundle
                        ? VotingStrategies.antiCapture()
                        : VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                if (includeAntiCaptureBundle) {
                    process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                    process = new ProposalAccessProcess(
                            name(),
                            ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                            process
                    );
                }
                if (includeTransparency) {
                    process = new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
                }
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.35
                );
            }
        };
    }

    static Scenario defaultPassWithBudgetedLobbyingAndMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + budgeted lobbying + mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = mediationProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world
                );
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.35
                );
            }
        };
    }

    static Scenario defaultPassWithStrategicLobbying() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + strategic lobbying";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new BudgetedLobbyingProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        true
                );
            }
        };
    }

    static Scenario defaultPassWithAdaptiveProposers(boolean includeStrategicLobbying) {
        return new Scenario() {
            @Override
            public String name() {
                return includeStrategicLobbying
                        ? "Default pass + adaptive proposers + strategic lobbying"
                        : "Default pass + adaptive proposers";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                if (includeStrategicLobbying) {
                    process = new BudgetedLobbyingProcess(
                            name(),
                            process,
                            world.lobbyGroups(),
                            0.24,
                            0.46,
                            0.38,
                            true
                    );
                }
                return new ProposerStrategyProcess(
                        name(),
                        process,
                        world.legislators(),
                        0.72,
                        0.56,
                        0.42
                );
            }
        };
    }

    static Scenario defaultPassWithDeepStrategyBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive strategy bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new MultiRoundAmendmentProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.024,
                        1.18,
                        0.07
                );
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        0.42,
                        0.40,
                        0.30,
                        0.08,
                        true
                );
                return new ProposerStrategyProcess(
                        name(),
                        process,
                        world.legislators(),
                        0.80,
                        0.52,
                        0.36
                );
            }
        };
    }

    static Scenario defaultPassWithDeepLobbying(
            String scenarioName,
            double publicFinancingStrength,
            double publicAdvocateStrength,
            double blindReviewStrength,
            double defensiveCapShare
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = publicAdvocateStrength > 0.0 || publicFinancingStrength > 0.0
                        ? VotingStrategies.antiCapture()
                        : VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        publicFinancingStrength,
                        publicAdvocateStrength,
                        blindReviewStrength,
                        defensiveCapShare
                );
            }
        };
    }

    static Scenario defaultPassWithCitizenPanel(String scenarioName, CitizenPanelMode mode) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess certifiedProcess = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess uncertifiedProcess = switch (mode) {
                    case AGENDA_PRIORITY -> certifiedProcess;
                    case DEFAULT_PASS_ELIGIBILITY, ACTIVE_VOTE_ROUTING -> simpleMajorityFloorProcess(name(), world, strategy);
                    case THRESHOLD_ADJUSTMENT -> supermajorityFloorProcess(name(), world, strategy, 0.60);
                };
                return new CitizenPanelReviewProcess(
                        name(),
                        certifiedProcess,
                        uncertifiedProcess,
                        mode,
                        mode == CitizenPanelMode.AGENDA_PRIORITY ? 41 : 73,
                        0.18,
                        mode == CitizenPanelMode.ACTIVE_VOTE_ROUTING ? 0.78 : 0.68,
                        mode == CitizenPanelMode.THRESHOLD_ADJUSTMENT ? 0.18 : 0.24,
                        mode == CitizenPanelMode.AGENDA_PRIORITY ? 0.56 : 0.60
                );
            }
        };
    }

    static Scenario defaultPassWithAgendaLottery(String scenarioName, boolean weighted) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AgendaLotteryProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.bills(),
                        weighted ? 0.46 : 0.42,
                        weighted
                );
            }
        };
    }

    static Scenario defaultPassWithQuadraticAttentionBudget() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + quadratic attention budget";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new QuadraticAttentionBudgetProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        11.5,
                        4
                );
            }
        };
    }

    static Scenario defaultPassWithPublicObjectionWindow(boolean repealMode) {
        return new Scenario() {
            @Override
            public String name() {
                return repealMode
                        ? "Default pass + public repeal window"
                        : "Default pass + public objection window";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        repealMode ? 0.50 : 0.42,
                        0.06,
                        repealMode
                );
            }
        };
    }

    static Scenario defaultPassWithConstituentPublicWill(boolean includeCitizenPanel) {
        return new Scenario() {
            @Override
            public String name() {
                return includeCitizenPanel
                        ? "Default pass + constituent public will + citizen panel"
                        : "Default pass + constituent public will";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process;
                if (includeCitizenPanel) {
                    LegislativeProcess certified = defaultPassFloorProcess(name(), world, strategy);
                    LegislativeProcess uncertified = simpleMajorityFloorProcess(name(), world, strategy);
                    process = new CitizenPanelReviewProcess(
                            name(),
                            certified,
                            uncertified,
                            CitizenPanelMode.ACTIVE_VOTE_ROUTING,
                            73,
                            0.14,
                            0.80,
                            0.16,
                            0.60
                    );
                } else {
                    process = defaultPassFloorProcess(name(), world, strategy);
                }
                return new ConstituentPublicWillProcess(name(), process, world.legislators(), 0.74, 0.45);
            }
        };
    }

    static Scenario defaultPassWithProposalBonds(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                return includeChallengeVouchers
                        ? "Default pass + proposal bonds + challenge"
                        : "Default pass + proposal bonds";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new ProposalBondProcess(name(), process, 2.20, 0.20, 4.50, 0.40, 1.15, 0.38, 0.70);
            }
        };
    }

    static Scenario defaultPassWithCoalitionSponsorship(
            String scenarioName,
            boolean requireAffectedGroupSponsor,
            boolean applyAgendaCreditDiscount
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CoalitionCosponsorshipProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        requireAffectedGroupSponsor ? 3 : 2,
                        1,
                        0.12,
                        requireAffectedGroupSponsor ? 0.50 : 0.48,
                        requireAffectedGroupSponsor,
                        applyAgendaCreditDiscount
                );
            }
        };
    }

    static Scenario defaultPassWithMultiRoundMediation(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                return includeChallengeVouchers
                        ? "Default pass + multi-round mediation + challenge"
                        : "Default pass + multi-round mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new MultiRoundAmendmentProcess(name(), process, world.legislators(), 3, 0.025, 1.15, 0.08);
            }
        };
    }

    static Scenario defaultPassWithStrategicAlternatives() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + strategic policy tournament";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        4,
                        4,
                        0.45,
                        0.035,
                        0.10
                );
            }
        };
    }

    static Scenario simpleMajorityWithStrategicAlternatives() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority ratification + strategic policy tournament";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        4,
                        4,
                        0.45,
                        0.035,
                        0.10
                );
            }
        };
    }

    static Scenario defaultPassWithHarmWeightedThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + harm-weighted threshold";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber highHarm = new Chamber(
                        "Legislature harm review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.48);
            }
        };
    }

    static Scenario defaultPassWithDistributionalCompensation(boolean requireConsent) {
        return new Scenario() {
            @Override
            public String name() {
                return requireConsent
                        ? "Default pass + affected-group consent"
                        : "Default pass + compensation amendments";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new DistributionalHarmProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        0.42,
                        requireConsent ? 0.48 : 0.42,
                        requireConsent ? 0.72 : 0.58,
                        requireConsent ? 0.42 : 0.30,
                        requireConsent
                );
            }
        };
    }

    static Scenario simpleMajorityWithCompetingAlternatives(
            String scenarioName,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        selectionRule,
                        generatedAlternatives,
                        includeStatusQuo
                );
            }
        };
    }

    static Scenario defaultPassWithCompetingAlternatives(
            String scenarioName,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        selectionRule,
                        generatedAlternatives,
                        includeStatusQuo
                );
            }
        };
    }

    static LegislativeProcess mediationProcess(
            String name,
            LegislativeProcess innerProcess,
            SimulationWorld world
    ) {
        return new AmendmentMediationProcess(
                name,
                innerProcess,
                world.legislators(),
                0.22,
                0.72,
                0.58,
                0.28,
                0.14
        );
    }

    static Scenario defaultPassWithProposalAccess() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + proposal access screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                LegislativeProcess floor = new UnicameralProcess(name(), chamber);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        floor
                );
            }
        };
    }

    static Scenario defaultPassWithChallengeVouchers() {
        return defaultPassWithChallengeVouchers(
                "Default pass + challenge vouchers",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82
        );
    }

    static Scenario defaultPassWithChallengeVouchers(
            String scenarioName,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner,
            double challengeThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        allocation,
                        tokensPerOwner,
                        challengeThreshold,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
            }
        };
    }

    static Scenario defaultPassWithChallengePath(
            String scenarioName,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner,
            double challengeThreshold,
            ChallengePath challengePath
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess challengedProcess = challengedProcess(name(), world, strategy, challengePath);
                return new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        allocation,
                        tokensPerOwner,
                        challengeThreshold,
                        challengedProcess
                );
            }
        };
    }

    static LegislativeProcess challengedProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy,
            ChallengePath challengePath
    ) {
        return switch (challengePath) {
            case SIMPLE_MAJORITY -> simpleMajorityFloorProcess(name, world, strategy);
            case SUPERMAJORITY -> supermajorityFloorProcess(name, world, strategy, 0.60);
            case COMMITTEE_REVIEW -> {
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
                yield new CommitteeGatekeepingProcess(name, committee, simpleMajorityFloorProcess(name, world, strategy));
            }
            case INFORMATION_PLUS_ACTIVE -> {
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.EXPERT,
                        17
                );
                yield new CommitteeInformationProcess(
                        name,
                        committeeMembers,
                        0.90,
                        0.35,
                        simpleMajorityFloorProcess(name, world, strategy)
                );
            }
        };
    }

    static Scenario defaultPassWithChallengeEscalation(
            String scenarioName,
            int minimumChallengers,
            double challengeThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new ChallengeEscalationProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        minimumChallengers,
                        challengeThreshold,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
            }
        };
    }

    static Scenario defaultPassWithChallengeVouchersAndInformation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + challenge vouchers + info";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess challengeProcess = new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        10,
                        0.82,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
                return new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, challengeProcess);
            }
        };
    }

    static Scenario defaultPassWithCrossBlocCosponsorship(
            String scenarioName,
            int minimumCosponsors,
            int minimumOutsideBlocs,
            double minimumIdeologicalDistance,
            double cosponsorThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.crossBlocCosponsorship(
                                world.legislators(),
                                minimumCosponsors,
                                minimumOutsideBlocs,
                                minimumIdeologicalDistance,
                                cosponsorThreshold
                        ),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    static Scenario defaultPassWithCrossBlocCosponsorshipAndChallenge() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + cross-bloc cosponsors + challenge";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess challengeProcess = new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.82,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.crossBlocCosponsorship(
                                world.legislators(),
                                2,
                                1,
                                0.12,
                                0.52
                        ),
                        challengeProcess
                );
            }
        };
    }

    static Scenario defaultPassWithAdaptiveTrack(boolean useChallengeMiddleLane) {
        return defaultPassWithAdaptiveTrack(
                useChallengeMiddleLane,
                0.34,
                0.58,
                useChallengeMiddleLane
                        ? "Default pass + adaptive tracks + challenge"
                        : "Default pass + adaptive tracks"
        );
    }

    static Scenario defaultPassWithAdaptiveTrack(
            boolean useChallengeMiddleLane,
            double fastLaneMaximumRisk,
            double highRiskMinimumRisk,
            String scenarioName
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = useChallengeMiddleLane
                        ? challengeMiddleLane(name(), world, strategy)
                        : simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess highRiskLane = informedGuardrailProcess(name(), world, strategy);
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        fastLaneMaximumRisk,
                        highRiskMinimumRisk
                );
            }
        };
    }

    static Scenario defaultPassWithAdaptiveTrackCitizenHighRisk() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive tracks + citizen high-risk";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess certified = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess uncertified = supermajorityFloorProcess(name(), world, strategy, 0.60);
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        certified,
                        uncertified,
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.12,
                        0.62
                );
                return new AdaptiveTrackProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        highRiskLane,
                        0.34,
                        0.58
                );
            }
        };
    }

    static Scenario defaultPassWithAdaptiveTrackSupermajorityHighRisk() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive tracks + supermajority high-risk";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AdaptiveTrackProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.60),
                        0.34,
                        0.58
                );
            }
        };
    }

    static Scenario defaultPassWithSunsetTrial(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeChallengeVouchers) {
                    return "Default pass + sunset trial + challenge";
                }
                return "Default pass + sunset trial";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new SunsetTrialProcess(
                        name(),
                        innerProcess,
                        0.38,
                        0.56
                );
            }
        };
    }

    static Scenario defaultPassWithLawRegistry(boolean includeChallengeVouchers) {
        return defaultPassWithLawRegistry(
                includeChallengeVouchers,
                5,
                0.34,
                0.58,
                0.82,
                includeChallengeVouchers
                        ? "Default pass + law registry + challenge"
                        : "Default pass + law registry"
        );
    }

    static Scenario defaultPassWithLawRegistry(
            boolean includeChallengeVouchers,
            int reviewDelayRounds,
            double provisionalRiskThreshold,
            double renewalThreshold,
            double rollbackRate,
            String scenarioName
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new LawRegistryProcess(
                        name(),
                        innerProcess,
                        reviewDelayRounds,
                        provisionalRiskThreshold,
                        renewalThreshold,
                        rollbackRate
                );
            }
        };
    }

    static Scenario defaultPassWithProposalCredits(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeChallengeVouchers) {
                    return "Default pass + earned proposal credits + challenge";
                }
                return "Default pass + earned proposal credits";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new ProposalCreditProcess(
                        name(),
                        innerProcess,
                        1.15,
                        0.30,
                        3.00,
                        0.56,
                        1.00,
                        0.28,
                        0.75,
                        0.60
                );
            }
        };
    }

    static Scenario defaultPassWithProposalCost() {
        return defaultPassWithProposalCost("Default pass + proposal costs", 0.34, 0.22, 0.18);
    }

    static Scenario defaultPassWithProposalCost(
            String scenarioName,
            double baseCost,
            double publicCreditWeight,
            double lobbyCreditWeight
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.proposalCost(baseCost, publicCreditWeight, lobbyCreditWeight),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    static Scenario defaultPassWithLobbySurchargeCost() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby-surcharge proposal costs";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.lobbySurchargeCost(0.32, 0.48, 0.42),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    static Scenario defaultPassWithMemberQuota() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + member proposal quota";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.memberQuota(3),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    static Scenario defaultPassWithCostAndGuardrails() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + costs + informed guardrails";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );

                LegislativeProcess process = new UnicameralProcess(name(), floorChamber);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, process);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        process
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.proposalCost(0.34, 0.22, 0.18),
                        process
                );
            }
        };
    }

    static Scenario defaultPassWithCommitteeGate(String name, CommitteeComposition composition) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        CommitteeFactory.select(world.legislators(), composition, 17),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new CommitteeGatekeepingProcess(
                        name(),
                        committee,
                        new UnicameralProcess(name(), floorChamber)
                );
            }
        };
    }

    static Scenario defaultPassWithInformation(
            String name,
            CommitteeComposition composition,
            boolean includeAccessAndGate
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 17);
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                LegislativeProcess process = new UnicameralProcess(name(), floorChamber);
                if (includeAccessAndGate) {
                    Chamber committee = new Chamber(
                            "Committee",
                            committeeMembers,
                            strategy,
                            AffirmativeThresholdRule.simpleMajority()
                    );
                    process = new CommitteeGatekeepingProcess(name(), committee, process);
                }
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, process);
                if (includeAccessAndGate) {
                    process = new ProposalAccessProcess(
                            name(),
                            ProposalAccessRules.viabilityScreen(0.35, 0.85),
                            process
                    );
                }
                return process;
            }
        };
    }

    static Scenario defaultPassWithAccessAndCommitteeGate() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + access + committee";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        CommitteeFactory.select(world.legislators(), CommitteeComposition.REPRESENTATIVE, 17),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess committeeGate = new CommitteeGatekeepingProcess(
                        name(),
                        committee,
                        new UnicameralProcess(name(), floorChamber)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        committeeGate
                );
            }
        };
    }
}
