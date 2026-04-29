package congresssim.simulation;

import congresssim.behavior.VoteContext;
import congresssim.institution.BillOutcome;
import congresssim.institution.LegislativeProcess;
import congresssim.model.Bill;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class Simulator {
    private final WorldGenerator worldGenerator = new WorldGenerator();

    public List<ScenarioReport> compare(List<Scenario> scenarios, WorldSpec worldSpec, int runs, long seed) {
        MetricsAccumulator[] accumulators = new MetricsAccumulator[scenarios.size()];
        for (int i = 0; i < accumulators.length; i++) {
            accumulators[i] = new MetricsAccumulator();
        }

        for (int run = 0; run < runs; run++) {
            long worldSeed = mix(seed, run, 17);
            SimulationWorld world = worldGenerator.generate(worldSpec, worldSeed);

            for (int scenarioIndex = 0; scenarioIndex < scenarios.size(); scenarioIndex++) {
                Scenario scenario = scenarios.get(scenarioIndex);
                LegislativeProcess process = scenario.buildProcess(world);
                Random scenarioRandom = new Random(mix(seed, run, scenarioIndex + 101));
                PolicyState policyState = world.initialPolicy();

                for (Bill bill : world.bills()) {
                    VoteContext context = new VoteContext(
                            world.partyPositions(),
                            scenarioRandom,
                            policyState.position()
                    );
                    BillOutcome outcome = process.consider(bill, context);
                    accumulators[scenarioIndex].add(outcome);
                    policyState = new PolicyState(outcome.statusQuoAfter());
                }
            }
        }

        List<ScenarioReport> reports = new ArrayList<>();
        for (int i = 0; i < scenarios.size(); i++) {
            reports.add(accumulators[i].toReport(scenarios.get(i).name()));
        }
        return reports;
    }

    private static long mix(long seed, int run, int stream) {
        long value = seed;
        value ^= 0x9E3779B97F4A7C15L + ((long) run << 6) + ((long) run >> 2);
        value ^= 0xBF58476D1CE4E5B9L * (stream + 31L);
        return value;
    }
}
