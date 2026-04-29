package congresssim.simulation;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyGroup;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class WorldGenerator {
    private static final List<String> ISSUE_DOMAINS = List.of(
            "tax",
            "health",
            "energy",
            "technology",
            "labor",
            "housing",
            "democracy"
    );

    public SimulationWorld generate(WorldSpec spec, long seed) {
        Random random = new Random(seed);
        List<Legislator> legislators = generateLegislators(spec, random);
        List<LobbyGroup> lobbyGroups = generateLobbyGroups(spec, random);
        PolicyState initialPolicy = new PolicyState(Values.clamp(random.nextGaussian() * 0.18, -1.0, 1.0));
        List<Bill> bills = generateBills(spec, legislators, random);
        return new SimulationWorld(legislators, bills, lobbyGroups, initialPolicy, partyPositions(legislators));
    }

    private List<Legislator> generateLegislators(WorldSpec spec, Random random) {
        List<Legislator> legislators = new ArrayList<>();
        double spread = 0.25 + (0.65 * spec.polarization());
        double standardDeviation = 0.24 - (0.10 * spec.polarization());

        for (int i = 0; i < spec.legislatorCount(); i++) {
            double faction = random.nextDouble();
            double center = faction < 0.46 ? -spread : faction < 0.92 ? spread : 0.0;
            double ideology = Values.clamp(center + (random.nextGaussian() * standardDeviation), -1.0, 1.0);
            String party = partyFor(ideology, spec.partyCount());
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
            boolean antiLobbyingReform = random.nextDouble() < 0.04 + (0.08 * spec.lobbyingSusceptibility());
            String issueDomain = antiLobbyingReform ? "democracy" : randomIssueDomain(random);
            double ideology = antiLobbyingReform
                    ? Values.clamp(proposer.ideology() * 0.45 + random.nextGaussian() * 0.16, -1.0, 1.0)
                    : Values.clamp(proposer.ideology() + random.nextGaussian() * 0.22, -1.0, 1.0);
            double moderation = 1.0 - Math.abs(ideology);
            double lobbyPressure;
            double privateGain;
            double publicBenefit;
            double publicSupport;
            double salience;

            if (antiLobbyingReform) {
                lobbyPressure = -Values.clamp(
                        0.28 + (0.58 * spec.lobbyingSusceptibility()) + random.nextGaussian() * 0.16,
                        0.10,
                        1.0
                );
                privateGain = 0.0;
                publicBenefit = Values.clamp(
                        0.58 + (moderation * 0.22) + (spec.constituencySensitivity() * 0.08) + random.nextGaussian() * 0.12,
                        0.0,
                        1.0
                );
                publicSupport = Values.clamp(
                        publicBenefit - (spec.lobbyingSusceptibility() * 0.10) + random.nextGaussian() * 0.16,
                        0.0,
                        1.0
                );
                salience = Values.clamp(0.50 + random.nextDouble() * 0.50, 0.0, 1.0);
            } else {
                lobbyPressure = Values.clamp(random.nextGaussian() * spec.lobbyingSusceptibility(), -1.0, 1.0);
                privateGain = Values.clamp(
                        (Math.max(0.0, lobbyPressure) * 0.72) + random.nextDouble() * 0.20,
                        0.0,
                        1.0
                );
                publicBenefit = Values.clamp(
                        0.34 + (moderation * 0.34) - (privateGain * 0.08) + random.nextGaussian() * 0.18,
                        0.0,
                        1.0
                );
                publicSupport = Values.clamp(
                        publicBenefit + (lobbyPressure * 0.08) - (privateGain * 0.05) + random.nextGaussian() * 0.22,
                        0.0,
                        1.0
                );
                salience = Values.clamp(0.20 + random.nextDouble() * 0.80, 0.0, 1.0);
            }

            bills.add(new Bill(
                    "B-" + (i + 1),
                    antiLobbyingReform ? "Anti-Lobbying Reform " + (i + 1) : "Bill " + (i + 1),
                    proposer.id(),
                    proposer.ideology(),
                    ideology,
                    publicSupport,
                    publicBenefit,
                    lobbyPressure,
                    salience,
                    privateGain,
                    antiLobbyingReform,
                    issueDomain,
                    0.0,
                    0.0
            ));
        }
        return bills;
    }

    private List<LobbyGroup> generateLobbyGroups(WorldSpec spec, Random random) {
        List<LobbyGroup> groups = new ArrayList<>();
        int count = Math.max(6, spec.partyCount() + 4);
        for (int i = 0; i < count; i++) {
            String domain = ISSUE_DOMAINS.get(i % ISSUE_DOMAINS.size());
            double budget = Values.clamp(
                    0.40 + (spec.lobbyingSusceptibility() * 1.85) + random.nextDouble() * 1.20,
                    0.0,
                    4.0
            );
            groups.add(new LobbyGroup(
                    "G-" + (i + 1),
                    domain,
                    Values.clamp(random.nextGaussian() * 0.70, -1.0, 1.0),
                    budget,
                    Values.clamp(0.35 + (spec.lobbyingSusceptibility() * 0.45) + random.nextGaussian() * 0.10, 0.0, 1.0),
                    Values.clamp(0.70 + (spec.lobbyingSusceptibility() * 1.15) + random.nextGaussian() * 0.18, 0.0, 3.0),
                    Values.clamp(0.30 + random.nextDouble() * 0.55, 0.0, 1.0),
                    Values.clamp(0.28 + random.nextDouble() * 0.60, 0.0, 1.0)
            ));
        }
        return groups;
    }

    private static String randomIssueDomain(Random random) {
        return ISSUE_DOMAINS.get(random.nextInt(ISSUE_DOMAINS.size() - 1));
    }

    private static String partyFor(double ideology, int partyCount) {
        if (partyCount == 1) {
            return "Unified";
        }
        if (partyCount == 2) {
            return ideology < 0.0 ? "Left" : "Right";
        }
        if (partyCount == 3) {
            if (ideology < -0.22) {
                return "Progressive";
            }
            if (ideology > 0.22) {
                return "Conservative";
            }
            return "Moderate";
        }

        double normalized = (ideology + 1.0) / 2.0;
        int partyIndex = Math.min(partyCount - 1, (int) Math.floor(normalized * partyCount));
        return "Party-" + (partyIndex + 1);
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
