package congresssim.simulation;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.BicameralProcess;
import congresssim.institution.Chamber;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.PresidentialVetoProcess;
import congresssim.institution.ProposalAccessProcess;
import congresssim.institution.ProposalAccessRules;
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
                new ScenarioEntry("supermajority-60", unicameral("Unicameral 60 percent passage", AffirmativeThresholdRule.supermajority(0.60))),
                new ScenarioEntry("default-pass", unicameral("Default pass unless 2/3 block", new DefaultPassUnlessVetoedRule(2.0 / 3.0))),
                new ScenarioEntry("default-pass-challenge", defaultPassWithChallengeVouchers()),
                new ScenarioEntry("default-pass-challenge-info", defaultPassWithChallengeVouchersAndInformation()),
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
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + challenge vouchers";
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
                        10,
                        0.82,
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
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
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
            senate.add(legislators.get(0));
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
