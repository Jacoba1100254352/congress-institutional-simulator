package congresssim.simulation;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AlternativeSelectionRule;
import congresssim.institution.AmendmentMediationProcess;
import congresssim.institution.BicameralProcess;
import congresssim.institution.BudgetedLobbyingProcess;
import congresssim.institution.Chamber;
import congresssim.institution.ChallengeEscalationProcess;
import congresssim.institution.ChallengeTokenAllocation;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.CompetingAlternativesProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.DistributionalHarmProcess;
import congresssim.institution.HarmWeightedThresholdProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.PresidentialVetoProcess;
import congresssim.institution.ProposalAccessProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalCreditProcess;
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
        return new Scenario() {
            @Override
            public String name() {
                if (useChallengeMiddleLane) {
                    return "Default pass + adaptive tracks + challenge";
                }
                return "Default pass + adaptive tracks";
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
        return new Scenario() {
            @Override
            public String name() {
                if (includeChallengeVouchers) {
                    return "Default pass + law registry + challenge";
                }
                return "Default pass + law registry";
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
                        5,
                        0.34,
                        0.58,
                        0.82
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
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + proposal costs";
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
                        ProposalAccessRules.proposalCost(0.34, 0.22, 0.18),
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
}
