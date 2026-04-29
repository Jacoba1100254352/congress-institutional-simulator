package congresssim.simulation;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaLotteryProcess;
import congresssim.institution.AlternativeSelectionRule;
import congresssim.institution.AmendmentMediationProcess;
import congresssim.institution.BicameralProcess;
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
import congresssim.institution.HarmWeightedThresholdProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.MultiRoundAmendmentProcess;
import congresssim.institution.PresidentialVetoProcess;
import congresssim.institution.ProposalAccessProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalBondProcess;
import congresssim.institution.ProposalCreditProcess;
import congresssim.institution.ProposerStrategyProcess;
import congresssim.institution.PublicObjectionWindowProcess;
import congresssim.institution.QuadraticAttentionBudgetProcess;
import congresssim.institution.SunsetTrialProcess;
import congresssim.institution.UnicameralProcess;
import congresssim.institution.VotingRule;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

public final class ScenarioCatalog {
    private ScenarioCatalog() {
    }

    public static List<Scenario> defaultScenarios() {
        return entries().stream().map(ScenarioEntry::scenario).toList();
    }

    public static List<Scenario> scenariosForKeys(List<String> keys) {
        Map<String, Scenario> byKey = new LinkedHashMap<>();
        for (ScenarioEntry entry : entries()) {
            byKey.put(entry.key(), entry.scenario());
        }

        List<Scenario> scenarios = new ArrayList<>();
        for (String key : keys) {
            Scenario scenario = byKey.get(key);
            if (scenario == null) {
                throw new IllegalArgumentException("Unknown scenario key: " + key);
            }
            scenarios.add(scenario);
        }
        return scenarios;
    }

    public static List<String> scenarioKeys() {
        return entries().stream().map(ScenarioEntry::key).toList();
    }

    private static List<ScenarioEntry> entries() {
        return List.of(
                new ScenarioEntry("simple-majority", unicameral("Unicameral simple majority", AffirmativeThresholdRule.simpleMajority())),
                new ScenarioEntry("simple-majority-mediation", simpleMajorityWithMediation()),
                new ScenarioEntry("simple-majority-lobby-firewall", unicameral(
                        "Unicameral majority + lobby firewall",
                        AffirmativeThresholdRule.simpleMajority(),
                        VotingStrategies.antiCapture()
                )),
                new ScenarioEntry("supermajority-60", unicameral("Unicameral 60 percent passage", AffirmativeThresholdRule.supermajority(0.60))),
                new ScenarioEntry("current-system", currentSystem()),
                new ScenarioEntry("default-pass", unicameral("Default pass unless 2/3 block", new DefaultPassUnlessVetoedRule(2.0 / 3.0))),
                new ScenarioEntry("default-pass-mediation", defaultPassWithMediation()),
                new ScenarioEntry("default-pass-lobby-firewall", defaultPassWithLobbyFirewall()),
                new ScenarioEntry("default-pass-lobby-transparency", defaultPassWithLobbyTransparency()),
                new ScenarioEntry("default-pass-public-interest-screen", defaultPassWithPublicInterestScreen()),
                new ScenarioEntry("default-pass-lobby-audit", defaultPassWithLobbyAudit()),
                new ScenarioEntry("default-pass-anti-capture-bundle", defaultPassWithAntiCaptureBundle()),
                new ScenarioEntry("default-pass-budgeted-lobbying", defaultPassWithBudgetedLobbying(false, false)),
                new ScenarioEntry("default-pass-budgeted-lobbying-transparency", defaultPassWithBudgetedLobbying(true, false)),
                new ScenarioEntry("default-pass-budgeted-lobbying-bundle", defaultPassWithBudgetedLobbying(true, true)),
                new ScenarioEntry("default-pass-budgeted-lobbying-mediation", defaultPassWithBudgetedLobbyingAndMediation()),
                new ScenarioEntry("default-pass-democracy-vouchers", defaultPassWithDeepLobbying(
                        "Default pass + democracy vouchers",
                        0.72,
                        0.00,
                        0.00,
                        1.00
                )),
                new ScenarioEntry("default-pass-public-advocate", defaultPassWithDeepLobbying(
                        "Default pass + equal-access public advocate",
                        0.00,
                        0.74,
                        0.00,
                        1.00
                )),
                new ScenarioEntry("default-pass-blind-lobby-review", defaultPassWithDeepLobbying(
                        "Default pass + blind sponsor/lobby review",
                        0.00,
                        0.00,
                        0.78,
                        1.00
                )),
                new ScenarioEntry("default-pass-defensive-lobby-cap", defaultPassWithDeepLobbying(
                        "Default pass + defensive lobbying cap",
                        0.00,
                        0.00,
                        0.00,
                        0.025
                )),
                new ScenarioEntry("default-pass-lobby-channel-bundle", defaultPassWithDeepLobbying(
                        "Default pass + channel anti-capture bundle",
                        0.58,
                        0.62,
                        0.62,
                        0.05
                )),
                new ScenarioEntry("default-pass-citizen-certificate", defaultPassWithCitizenPanel(
                        "Default pass + citizen certificate",
                        CitizenPanelMode.DEFAULT_PASS_ELIGIBILITY
                )),
                new ScenarioEntry("default-pass-citizen-active-routing", defaultPassWithCitizenPanel(
                        "Default pass + citizen active-vote routing",
                        CitizenPanelMode.ACTIVE_VOTE_ROUTING
                )),
                new ScenarioEntry("default-pass-citizen-threshold", defaultPassWithCitizenPanel(
                        "Default pass + citizen threshold adjustment",
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT
                )),
                new ScenarioEntry("default-pass-citizen-agenda", defaultPassWithCitizenPanel(
                        "Default pass + citizen agenda priority",
                        CitizenPanelMode.AGENDA_PRIORITY
                )),
                new ScenarioEntry("default-pass-weighted-agenda-lottery", defaultPassWithAgendaLottery(
                        "Default pass + weighted agenda lottery",
                        true
                )),
                new ScenarioEntry("default-pass-random-agenda-lottery", defaultPassWithAgendaLottery(
                        "Default pass + random agenda lottery",
                        false
                )),
                new ScenarioEntry("default-pass-quadratic-attention", defaultPassWithQuadraticAttentionBudget()),
                new ScenarioEntry("default-pass-public-objection", defaultPassWithPublicObjectionWindow(false)),
                new ScenarioEntry("default-pass-repeal-window", defaultPassWithPublicObjectionWindow(true)),
                new ScenarioEntry("default-pass-constituent-public-will", defaultPassWithConstituentPublicWill(false)),
                new ScenarioEntry("default-pass-constituent-citizen-panel", defaultPassWithConstituentPublicWill(true)),
                new ScenarioEntry("default-pass-proposal-bonds", defaultPassWithProposalBonds(false)),
                new ScenarioEntry("default-pass-proposal-bonds-challenge", defaultPassWithProposalBonds(true)),
                new ScenarioEntry("default-pass-cross-bloc-credit-discount", defaultPassWithCoalitionSponsorship(
                        "Default pass + cross-bloc credit discount",
                        false,
                        true
                )),
                new ScenarioEntry("default-pass-affected-sponsor-gate", defaultPassWithCoalitionSponsorship(
                        "Default pass + affected-group sponsor gate",
                        true,
                        true
                )),
                new ScenarioEntry("default-pass-multiround-mediation", defaultPassWithMultiRoundMediation(false)),
                new ScenarioEntry("default-pass-multiround-mediation-challenge", defaultPassWithMultiRoundMediation(true)),
                new ScenarioEntry("default-pass-alternatives-strategic", defaultPassWithStrategicAlternatives()),
                new ScenarioEntry("default-pass-adaptive-proposers", defaultPassWithAdaptiveProposers(false)),
                new ScenarioEntry("default-pass-adaptive-proposers-lobbying", defaultPassWithAdaptiveProposers(true)),
                new ScenarioEntry("default-pass-strategic-lobbying", defaultPassWithStrategicLobbying()),
                new ScenarioEntry("default-pass-deep-strategy-bundle", defaultPassWithDeepStrategyBundle()),
                new ScenarioEntry("default-pass-adaptive-track-lenient", defaultPassWithAdaptiveTrack(false, 0.42, 0.68, "Default pass + adaptive tracks lenient")),
                new ScenarioEntry("default-pass-adaptive-track-strict", defaultPassWithAdaptiveTrack(false, 0.24, 0.48, "Default pass + adaptive tracks strict")),
                new ScenarioEntry("default-pass-adaptive-track-citizen-high-risk", defaultPassWithAdaptiveTrackCitizenHighRisk()),
                new ScenarioEntry("default-pass-adaptive-track-supermajority-high-risk", defaultPassWithAdaptiveTrackSupermajorityHighRisk()),
                new ScenarioEntry("default-pass-law-registry-fast-review", defaultPassWithLawRegistry(false, 2, 0.34, 0.58, 0.82, "Default pass + law registry fast review")),
                new ScenarioEntry("default-pass-law-registry-slow-review", defaultPassWithLawRegistry(false, 8, 0.34, 0.58, 0.62, "Default pass + law registry slow partial review")),
                new ScenarioEntry("default-pass-cost-public-waiver", defaultPassWithProposalCost(
                        "Default pass + proposal costs + public waiver",
                        0.34,
                        0.50,
                        0.00
                )),
                new ScenarioEntry("default-pass-cost-lobby-surcharge", defaultPassWithLobbySurchargeCost()),
                new ScenarioEntry("default-pass-member-quota", defaultPassWithMemberQuota()),
                new ScenarioEntry("default-pass-harm-threshold", defaultPassWithHarmWeightedThreshold()),
                new ScenarioEntry("default-pass-compensation", defaultPassWithDistributionalCompensation(false)),
                new ScenarioEntry("default-pass-affected-consent", defaultPassWithDistributionalCompensation(true)),
                new ScenarioEntry("simple-majority-alternatives-pairwise", simpleMajorityWithCompetingAlternatives(
                        "Unicameral majority + pairwise alternatives",
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true
                )),
                new ScenarioEntry("default-pass-alternatives-benefit", defaultPassWithCompetingAlternatives(
                        "Default pass + public-benefit alternatives",
                        AlternativeSelectionRule.HIGHEST_PUBLIC_BENEFIT,
                        4,
                        true
                )),
                new ScenarioEntry("default-pass-alternatives-support", defaultPassWithCompetingAlternatives(
                        "Default pass + public-support alternatives",
                        AlternativeSelectionRule.HIGHEST_PUBLIC_SUPPORT,
                        4,
                        true
                )),
                new ScenarioEntry("default-pass-alternatives-median", defaultPassWithCompetingAlternatives(
                        "Default pass + median-seeking alternatives",
                        AlternativeSelectionRule.CLOSEST_TO_CHAMBER_MEDIAN,
                        4,
                        true
                )),
                new ScenarioEntry("default-pass-alternatives-pairwise", defaultPassWithCompetingAlternatives(
                        "Default pass + pairwise policy tournament",
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true
                )),
                new ScenarioEntry("default-pass-obstruction-substitute", defaultPassWithCompetingAlternatives(
                        "Default pass + obstruction-with-substitute",
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        3,
                        true
                )),
                new ScenarioEntry("default-pass-challenge", defaultPassWithChallengeVouchers()),
                new ScenarioEntry("default-pass-challenge-info", defaultPassWithChallengeVouchersAndInformation()),
                new ScenarioEntry("default-pass-cross-bloc", defaultPassWithCrossBlocCosponsorship(
                        "Default pass + cross-bloc cosponsors",
                        2,
                        1,
                        0.12,
                        0.52
                )),
                new ScenarioEntry("default-pass-cross-bloc-strong", defaultPassWithCrossBlocCosponsorship(
                        "Default pass + strong cross-bloc cosponsors",
                        6,
                        1,
                        0.20,
                        0.58
                )),
                new ScenarioEntry("default-pass-cross-bloc-challenge", defaultPassWithCrossBlocCosponsorshipAndChallenge()),
                new ScenarioEntry("default-pass-adaptive-track", defaultPassWithAdaptiveTrack(false)),
                new ScenarioEntry("default-pass-adaptive-track-challenge", defaultPassWithAdaptiveTrack(true)),
                new ScenarioEntry("default-pass-sunset-trial", defaultPassWithSunsetTrial(false)),
                new ScenarioEntry("default-pass-sunset-challenge", defaultPassWithSunsetTrial(true)),
                new ScenarioEntry("default-pass-law-registry", defaultPassWithLawRegistry(false)),
                new ScenarioEntry("default-pass-law-registry-challenge", defaultPassWithLawRegistry(true)),
                new ScenarioEntry("default-pass-earned-credits", defaultPassWithProposalCredits(false)),
                new ScenarioEntry("default-pass-earned-credits-challenge", defaultPassWithProposalCredits(true)),
                new ScenarioEntry("default-pass-challenge-party-t3-s082", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=3 s=.82",
                        ChallengeTokenAllocation.PARTY,
                        3,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t6-s082", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=6 s=.82",
                        ChallengeTokenAllocation.PARTY,
                        6,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t15-s082", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=15 s=.82",
                        ChallengeTokenAllocation.PARTY,
                        15,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t25-s082", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=25 s=.82",
                        ChallengeTokenAllocation.PARTY,
                        25,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-proportional", defaultPassWithChallengeVouchers(
                        "Default pass + proportional party challenge vouchers",
                        ChallengeTokenAllocation.PARTY_PROPORTIONAL,
                        10,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-minority-bonus", defaultPassWithChallengeVouchers(
                        "Default pass + minority-bonus challenge vouchers",
                        ChallengeTokenAllocation.PARTY_MINORITY_BONUS,
                        8,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-supermajority", defaultPassWithChallengePath(
                        "Default pass + challenge to 60 percent vote",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.82,
                        ChallengePath.SUPERMAJORITY
                )),
                new ScenarioEntry("default-pass-challenge-committee", defaultPassWithChallengePath(
                        "Default pass + challenge to committee review",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.82,
                        ChallengePath.COMMITTEE_REVIEW
                )),
                new ScenarioEntry("default-pass-challenge-info-active", defaultPassWithChallengePath(
                        "Default pass + challenge to info + active vote",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.82,
                        ChallengePath.INFORMATION_PLUS_ACTIVE
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s050", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=10 s=.50",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.50
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s065", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=10 s=.65",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.65
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s100", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=10 s=1.00",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        1.00
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s125", defaultPassWithChallengeVouchers(
                        "Default pass + party challenge vouchers t=10 s=1.25",
                        ChallengeTokenAllocation.PARTY,
                        10,
                        1.25
                )),
                new ScenarioEntry("default-pass-challenge-member-t1-s082", defaultPassWithChallengeVouchers(
                        "Default pass + member challenge vouchers t=1 s=.82",
                        ChallengeTokenAllocation.LEGISLATOR,
                        1,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-member-t2-s082", defaultPassWithChallengeVouchers(
                        "Default pass + member challenge vouchers t=2 s=.82",
                        ChallengeTokenAllocation.LEGISLATOR,
                        2,
                        0.82
                )),
                new ScenarioEntry("default-pass-challenge-member-t3-s082", defaultPassWithChallengeVouchers(
                        "Default pass + member challenge vouchers t=3 s=.82",
                        ChallengeTokenAllocation.LEGISLATOR,
                        3,
                        0.82
                )),
                new ScenarioEntry("default-pass-escalation-q6-s082", defaultPassWithChallengeEscalation(
                        "Default pass + q=6 challenge escalation s=.82",
                        6,
                        0.82
                )),
                new ScenarioEntry("default-pass-escalation-q12-s082", defaultPassWithChallengeEscalation(
                        "Default pass + q=12 challenge escalation s=.82",
                        12,
                        0.82
                )),
                new ScenarioEntry("default-pass-escalation-q20-s082", defaultPassWithChallengeEscalation(
                        "Default pass + q=20 challenge escalation s=.82",
                        20,
                        0.82
                )),
                new ScenarioEntry("default-pass-access", defaultPassWithProposalAccess()),
                new ScenarioEntry("default-pass-cost", defaultPassWithProposalCost()),
                new ScenarioEntry("default-pass-cost-guarded", defaultPassWithCostAndGuardrails()),
                new ScenarioEntry("default-pass-committee", defaultPassWithCommitteeGate(
                        "Default pass + representative committee gate",
                        CommitteeComposition.REPRESENTATIVE
                )),
                new ScenarioEntry("default-pass-committee-majority", defaultPassWithCommitteeGate(
                        "Default pass + majority-controlled committee",
                        CommitteeComposition.MAJORITY_CONTROLLED
                )),
                new ScenarioEntry("default-pass-committee-polarized", defaultPassWithCommitteeGate(
                        "Default pass + polarized committee",
                        CommitteeComposition.POLARIZED
                )),
                new ScenarioEntry("default-pass-committee-captured", defaultPassWithCommitteeGate(
                        "Default pass + captured committee",
                        CommitteeComposition.CAPTURED
                )),
                new ScenarioEntry("default-pass-info", defaultPassWithInformation(
                        "Default pass + representative committee info",
                        CommitteeComposition.REPRESENTATIVE,
                        false
                )),
                new ScenarioEntry("default-pass-info-expert", defaultPassWithInformation(
                        "Default pass + expert committee info",
                        CommitteeComposition.EXPERT,
                        false
                )),
                new ScenarioEntry("default-pass-info-captured", defaultPassWithInformation(
                        "Default pass + captured committee info",
                        CommitteeComposition.CAPTURED,
                        false
                )),
                new ScenarioEntry("default-pass-guarded", defaultPassWithAccessAndCommitteeGate()),
                new ScenarioEntry("default-pass-informed-guarded", defaultPassWithInformation(
                        "Default pass + informed guarded committee",
                        CommitteeComposition.REPRESENTATIVE,
                        true
                )),
                new ScenarioEntry("bicameral-majority", bicameral("Bicameral simple majority", AffirmativeThresholdRule.simpleMajority())),
                new ScenarioEntry("presidential-veto", presidentialVeto())
        );
    }

    private static Scenario simpleMajorityWithMediation() {
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

    private static Scenario defaultPassWithMediation() {
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

    private static Scenario defaultPassWithLobbyFirewall() {
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

    private static Scenario defaultPassWithLobbyTransparency() {
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

    private static Scenario defaultPassWithPublicInterestScreen() {
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

    private static Scenario defaultPassWithLobbyAudit() {
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

    private static Scenario defaultPassWithAntiCaptureBundle() {
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

    private static Scenario defaultPassWithBudgetedLobbying(boolean includeTransparency, boolean includeAntiCaptureBundle) {
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

    private static Scenario defaultPassWithBudgetedLobbyingAndMediation() {
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

    private static Scenario defaultPassWithStrategicLobbying() {
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

    private static Scenario defaultPassWithAdaptiveProposers(boolean includeStrategicLobbying) {
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

    private static Scenario defaultPassWithDeepStrategyBundle() {
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

    private static Scenario defaultPassWithDeepLobbying(
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

    private static Scenario defaultPassWithCitizenPanel(String scenarioName, CitizenPanelMode mode) {
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

    private static Scenario defaultPassWithAgendaLottery(String scenarioName, boolean weighted) {
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

    private static Scenario defaultPassWithQuadraticAttentionBudget() {
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

    private static Scenario defaultPassWithPublicObjectionWindow(boolean repealMode) {
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

    private static Scenario defaultPassWithConstituentPublicWill(boolean includeCitizenPanel) {
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

    private static Scenario defaultPassWithProposalBonds(boolean includeChallengeVouchers) {
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

    private static Scenario defaultPassWithCoalitionSponsorship(
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

    private static Scenario defaultPassWithMultiRoundMediation(boolean includeChallengeVouchers) {
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

    private static Scenario defaultPassWithStrategicAlternatives() {
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
                        2,
                        2
                );
            }
        };
    }

    private static Scenario defaultPassWithHarmWeightedThreshold() {
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

    private static Scenario defaultPassWithDistributionalCompensation(boolean requireConsent) {
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

    private static Scenario simpleMajorityWithCompetingAlternatives(
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

    private static Scenario defaultPassWithCompetingAlternatives(
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

    private static LegislativeProcess mediationProcess(
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

    private static Scenario defaultPassWithProposalAccess() {
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

    private static Scenario defaultPassWithChallengeVouchers() {
        return defaultPassWithChallengeVouchers(
                "Default pass + challenge vouchers",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82
        );
    }

    private static Scenario defaultPassWithChallengeVouchers(
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

    private static Scenario defaultPassWithChallengePath(
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

    private static LegislativeProcess challengedProcess(
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

    private static Scenario defaultPassWithChallengeEscalation(
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

    private static Scenario defaultPassWithChallengeVouchersAndInformation() {
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

    private static Scenario defaultPassWithCrossBlocCosponsorship(
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

    private static Scenario defaultPassWithCrossBlocCosponsorshipAndChallenge() {
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

    private static Scenario defaultPassWithAdaptiveTrack(boolean useChallengeMiddleLane) {
        return defaultPassWithAdaptiveTrack(
                useChallengeMiddleLane,
                0.34,
                0.58,
                useChallengeMiddleLane
                        ? "Default pass + adaptive tracks + challenge"
                        : "Default pass + adaptive tracks"
        );
    }

    private static Scenario defaultPassWithAdaptiveTrack(
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

    private static Scenario defaultPassWithAdaptiveTrackCitizenHighRisk() {
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

    private static Scenario defaultPassWithAdaptiveTrackSupermajorityHighRisk() {
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

    private static Scenario defaultPassWithSunsetTrial(boolean includeChallengeVouchers) {
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

    private static Scenario defaultPassWithLawRegistry(boolean includeChallengeVouchers) {
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

    private static Scenario defaultPassWithLawRegistry(
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

    private static Scenario defaultPassWithProposalCredits(boolean includeChallengeVouchers) {
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

    private static LegislativeProcess defaultPassFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                new DefaultPassUnlessVetoedRule(2.0 / 3.0)
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess simpleMajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess supermajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy,
            double threshold
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.supermajority(threshold)
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess challengeMiddleLane(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber activeVoteChamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new ChallengeVoucherProcess(
                name,
                world.legislators(),
                strategy,
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                new UnicameralProcess(name, activeVoteChamber)
        );
    }

    private static LegislativeProcess informedGuardrailProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
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
        LegislativeProcess process = new UnicameralProcess(name, floorChamber);
        process = new CommitteeGatekeepingProcess(name, committee, process);
        process = new CommitteeInformationProcess(name, committeeMembers, 0.85, 0.45, process);
        return new ProposalAccessProcess(
                name,
                ProposalAccessRules.viabilityScreen(0.35, 0.85),
                process
        );
    }

    private static Scenario defaultPassWithProposalCost() {
        return defaultPassWithProposalCost("Default pass + proposal costs", 0.34, 0.22, 0.18);
    }

    private static Scenario defaultPassWithProposalCost(
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

    private static Scenario defaultPassWithLobbySurchargeCost() {
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

    private static Scenario defaultPassWithMemberQuota() {
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

    private static Scenario defaultPassWithCostAndGuardrails() {
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

    private static Scenario defaultPassWithCommitteeGate(String name, CommitteeComposition composition) {
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

    private static Scenario defaultPassWithInformation(
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

    private static Scenario defaultPassWithAccessAndCommitteeGate() {
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

    private static Scenario unicameral(String name, VotingRule rule) {
        return unicameral(name, rule, VotingStrategies.standard());
    }

    private static Scenario unicameral(String name, VotingRule rule, VotingStrategy strategy) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                Chamber chamber = new Chamber("Congress", world.legislators(), strategy, rule);
                return new UnicameralProcess(name, chamber);
            }
        };
    }

    private static Scenario bicameral(String name, VotingRule rule) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber("House", world.legislators(), strategy, rule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, rule);
                return new BicameralProcess(name, house, senate);
            }
        };
    }

    private static Scenario presidentialVeto() {
        return new Scenario() {
            @Override
            public String name() {
                return "Bicameral majority + presidential veto";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                VotingRule chamberRule = AffirmativeThresholdRule.simpleMajority();
                Chamber house = new Chamber("House", world.legislators(), strategy, chamberRule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, chamberRule);
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                Legislator president = presidentFromWorld(world);
                return new PresidentialVetoProcess(
                        bicameral,
                        president,
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
            }
        };
    }

    private static Scenario currentSystem() {
        return new Scenario() {
            @Override
            public String name() {
                return "Current U.S.-style system";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber(
                        "House",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                return new PresidentialVetoProcess(
                        bicameral,
                        presidentFromWorld(world),
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
            }
        };
    }

    private static List<Legislator> senateSubset(List<Legislator> legislators) {
        List<Legislator> senate = new ArrayList<>();
        int stride = Math.max(2, legislators.size() / Math.max(1, legislators.size() / 3));
        for (int i = 0; i < legislators.size(); i += stride) {
            senate.add(legislators.get(i));
        }
        if (senate.isEmpty()) {
            senate.add(legislators.getFirst());
        }
        return senate;
    }

    private static Legislator presidentFromWorld(SimulationWorld world) {
        double averageIdeology = world.legislators()
                .stream()
                .mapToDouble(Legislator::ideology)
                .average()
                .orElse(0.0);
        return new Legislator(
                "EXEC-1",
                "Executive",
                averageIdeology * 0.7,
                0.42,
                0.72,
                0.58,
                0.46,
                0.62
        );
    }

    private record ScenarioEntry(String key, Scenario scenario) {
    }

    private enum ChallengePath {
        SIMPLE_MAJORITY,
        SUPERMAJORITY,
        COMMITTEE_REVIEW,
        INFORMATION_PLUS_ACTIVE
    }
}
