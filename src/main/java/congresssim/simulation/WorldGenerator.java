package congresssim.simulation;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class WorldGenerator {
    public SimulationWorld generate(WorldSpec spec, long seed) {
        Random random = new Random(seed);
        List<Legislator> legislators = generateLegislators(spec, random);
        PolicyState initialPolicy = new PolicyState(Values.clamp(random.nextGaussian() * 0.18, -1.0, 1.0));
        List<Bill> bills = generateBills(spec, legislators, random);
        return new SimulationWorld(legislators, bills, initialPolicy, partyPositions(legislators));
    }

    private List<Legislator> generateLegislators(WorldSpec spec, Random random) {
        List<Legislator> legislators = new ArrayList<>();
        double spread = 0.25 + (0.65 * spec.polarization());
        double standardDeviation = 0.24 - (0.10 * spec.polarization());

        for (int i = 0; i < spec.legislatorCount(); i++) {
            double faction = random.nextDouble();
            double center = faction < 0.46 ? -spread : faction < 0.92 ? spread : 0.0;
            double ideology = Values.clamp(center + (random.nextGaussian() * standardDeviation), -1.0, 1.0);
            String party = partyFor(ideology);
            double moderation = 1.0 - Math.abs(ideology);

            legislators.add(new Legislator(
                    "L-" + (i + 1),
                    party,
                    ideology,
                    Values.clamp(spec.compromiseCulture() + (moderation * 0.24) + random.nextGaussian() * 0.10, 0.0, 1.0),
                    Values.clamp(spec.partyLoyalty() + random.nextGaussian() * 0.12, 0.0, 1.0),
                    Values.clamp(spec.constituencySensitivity() + random.nextGaussian() * 0.12, 0.0, 1.0),
                    Values.clamp(spec.lobbyingSusceptibility() + random.nextGaussian() * 0.16, 0.0, 1.0),
                    Values.clamp(0.58 + random.nextGaussian() * 0.15, 0.0, 1.0)
            ));
        }
        return legislators;
    }

    private List<Bill> generateBills(WorldSpec spec, List<Legislator> legislators, Random random) {
        List<Bill> bills = new ArrayList<>();
        for (int i = 0; i < spec.billCount(); i++) {
            Legislator proposer = legislators.get(random.nextInt(legislators.size()));
            double ideology = Values.clamp(proposer.ideology() + random.nextGaussian() * 0.22, -1.0, 1.0);
            double moderation = 1.0 - Math.abs(ideology);
            double publicSupport = Values.clamp(0.42 + (moderation * 0.20) + random.nextGaussian() * 0.20, 0.0, 1.0);
            double lobbyPressure = Values.clamp(random.nextGaussian() * spec.lobbyingSusceptibility(), -1.0, 1.0);
            double salience = Values.clamp(0.20 + random.nextDouble() * 0.80, 0.0, 1.0);

            bills.add(new Bill(
                    "B-" + (i + 1),
                    "Bill " + (i + 1),
                    proposer.id(),
                    proposer.ideology(),
                    ideology,
                    publicSupport,
                    lobbyPressure,
                    salience
            ));
        }
        return bills;
    }

    private static String partyFor(double ideology) {
        if (ideology < -0.22) {
            return "Progressive";
        }
        if (ideology > 0.22) {
            return "Conservative";
        }
        return "Moderate";
    }

    private static Map<String, Double> partyPositions(List<Legislator> legislators) {
        Map<String, Double> sums = new HashMap<>();
        Map<String, Integer> counts = new HashMap<>();

        for (Legislator legislator : legislators) {
            sums.merge(legislator.party(), legislator.ideology(), Double::sum);
            counts.merge(legislator.party(), 1, Integer::sum);
        }

        Map<String, Double> positions = new HashMap<>();
        for (Map.Entry<String, Double> entry : sums.entrySet()) {
            positions.put(entry.getKey(), entry.getValue() / counts.get(entry.getKey()));
        }
        return positions;
    }
}
