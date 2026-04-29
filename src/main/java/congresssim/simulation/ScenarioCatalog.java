package congresssim.simulation;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.BicameralProcess;
import congresssim.institution.Chamber;
import congresssim.institution.CommitteeGatekeepingProcess;
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

public final class ScenarioCatalog {
    private ScenarioCatalog() {
    }

    public static List<Scenario> defaultScenarios() {
        return List.of(
                unicameral("Unicameral simple majority", AffirmativeThresholdRule.simpleMajority()),
                unicameral("Unicameral 60 percent passage", AffirmativeThresholdRule.supermajority(0.60)),
                unicameral("Default pass unless 2/3 block", new DefaultPassUnlessVetoedRule(2.0 / 3.0)),
                defaultPassWithProposalAccess(),
                defaultPassWithCommitteeGate(),
                defaultPassWithAccessAndCommitteeGate(),
                bicameral("Bicameral simple majority", AffirmativeThresholdRule.simpleMajority()),
                presidentialVeto()
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

    private static Scenario defaultPassWithCommitteeGate() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + committee gate";
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
                        representativeSubset(world.legislators(), 17),
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
                        representativeSubset(world.legislators(), 17),
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

    private static List<Legislator> representativeSubset(List<Legislator> legislators, int targetSize) {
        List<Legislator> sorted = new ArrayList<>(legislators);
        sorted.sort((left, right) -> Double.compare(left.ideology(), right.ideology()));

        int size = Math.min(targetSize, sorted.size());
        if (size <= 1) {
            return List.of(sorted.get(0));
        }

        List<Legislator> subset = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            int index = (int) Math.round(i * (sorted.size() - 1.0) / (size - 1.0));
            subset.add(sorted.get(index));
        }
        return subset;
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
}
