package congresssim.simulation;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
import congresssim.model.PolicyState;
import congresssim.model.SimulationWorld;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.Comparator;
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
    private static final List<String> AFFECTED_GROUPS = List.of(
            "rural",
            "urban",
            "workers",
            "small-business",
            "low-income",
            "future-generations",
            "regional-minority"
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
            double districtPreference = Values.clamp(
                    (0.78 * ideology) + (random.nextGaussian() * (0.18 + (0.10 * spec.polarization()))),
                    -1.0,
                    1.0
            );

            legislators.add(new Legislator(
                    "L-" + (i + 1),
                    party,
                    ideology,
                    Values.clamp(spec.compromiseCulture() + (moderation * 0.24) + random.nextGaussian() * 0.10, 0.0, 1.0),
                    Values.clamp(spec.partyLoyalty() + random.nextGaussian() * 0.12, 0.0, 1.0),
                    Values.clamp(spec.constituencySensitivity() + random.nextGaussian() * 0.12, 0.0, 1.0),
                    Values.clamp(spec.lobbyingSusceptibility() + random.nextGaussian() * 0.16, 0.0, 1.0),
                    Values.clamp(0.58 + random.nextGaussian() * 0.15, 0.0, 1.0),
                    districtPreference,
                    Values.clamp(spec.constituencySensitivity() + random.nextGaussian() * 0.16, 0.0, 1.0),
                    Values.clamp(0.34 + random.nextDouble() * 0.58, 0.0, 1.0)
            ));
        }
        return assignPartySystem(legislators, spec, random);
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
            String affectedGroup = AFFECTED_GROUPS.get(random.nextInt(AFFECTED_GROUPS.size()));
            double concentratedHarm;
            double affectedGroupSupport;
            double compensationCost;
            double publicBenefitUncertainty;

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
                concentratedHarm = Values.clamp(
                        0.08 + (Math.max(0.0, -lobbyPressure) * 0.08) + random.nextGaussian() * 0.06,
                        0.0,
                        0.35
                );
                publicBenefitUncertainty = Values.clamp(0.18 + random.nextGaussian() * 0.08, 0.0, 1.0);
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
                concentratedHarm = Values.clamp(
                        (Math.abs(ideology - proposer.ideology()) * 0.10)
                                + (Math.abs(ideology) * 0.22)
                                + (privateGain * 0.22)
                                + (salience * 0.12)
                                + random.nextGaussian() * 0.14,
                        0.0,
                        1.0
                );
                publicBenefitUncertainty = Values.clamp(
                        0.14
                                + (salience * 0.18)
                                + (Math.abs(publicSupport - publicBenefit) * 0.32)
                                + (Math.max(0.0, lobbyPressure) * 0.10)
                                + random.nextGaussian() * 0.08,
                        0.0,
                        1.0
                );
            }
            affectedGroupSupport = Values.clamp(
                    publicSupport
                            - (concentratedHarm * 0.48)
                            + (publicBenefit * 0.12)
                            - (Math.max(0.0, lobbyPressure) * 0.06)
                            + random.nextGaussian() * 0.12,
                    0.0,
                    1.0
            );
            compensationCost = Values.clamp(
                    concentratedHarm * (0.18 + random.nextDouble() * 0.34),
                    0.0,
                    0.55
            );

            Bill bill = new Bill(
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
                    0.0,
                    affectedGroup,
                    affectedGroupSupport,
                    concentratedHarm,
                    compensationCost
            ).withPublicBenefitUncertainty(publicBenefitUncertainty);
            bills.add(bill);
        }
        return bills;
    }

    private List<LobbyGroup> generateLobbyGroups(WorldSpec spec, Random random) {
        List<LobbyGroup> groups = new ArrayList<>();
        int count = Math.max(6, spec.partyCount() + 4);
        LobbyCaptureStrategy[] strategies = LobbyCaptureStrategy.values();
        for (int i = 0; i < count; i++) {
            String domain = ISSUE_DOMAINS.get(i % ISSUE_DOMAINS.size());
            Map<String, Double> issuePreferences = new HashMap<>();
            issuePreferences.put(domain, Values.clamp(0.72 + random.nextDouble() * 0.28, 0.0, 1.0));
            issuePreferences.put(ISSUE_DOMAINS.get(random.nextInt(ISSUE_DOMAINS.size())), Values.clamp(0.20 + random.nextDouble() * 0.40, 0.0, 1.0));
            double budget = Values.clamp(
                    0.40 + (spec.lobbyingSusceptibility() * 1.85) + random.nextDouble() * 1.20,
                    0.0,
                    4.0
            );
            groups.add(new LobbyGroup(
                    "G-" + (i + 1),
                    domain,
                    issuePreferences,
                    Values.clamp(random.nextGaussian() * 0.70, -1.0, 1.0),
                    budget,
                    Values.clamp(0.35 + (spec.lobbyingSusceptibility() * 0.45) + random.nextGaussian() * 0.10, 0.0, 1.0),
                    Values.clamp(0.70 + (spec.lobbyingSusceptibility() * 1.15) + random.nextGaussian() * 0.18, 0.0, 3.0),
                    Values.clamp(0.30 + random.nextDouble() * 0.55, 0.0, 1.0),
                    Values.clamp(0.28 + random.nextDouble() * 0.60, 0.0, 1.0),
                    strategies[Math.floorMod(i + random.nextInt(strategies.length), strategies.length)],
                    Values.clamp(0.18 + random.nextDouble() * 0.42, 0.0, 1.0)
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

    private static List<Legislator> assignPartySystem(List<Legislator> legislators, WorldSpec spec, Random random) {
        if (spec.partySystemProfile() == PartySystemProfile.IDEOLOGICAL_BINS) {
            return legislators;
        }

        int[] targets = partySeatTargets(spec, random);
        List<Legislator> ordered = new ArrayList<>(legislators);
        ordered.sort(Comparator.comparingDouble(Legislator::ideology));

        Map<String, String> partyByLegislatorId = new HashMap<>();
        int cursor = 0;
        for (int partyIndex = 0; partyIndex < targets.length; partyIndex++) {
            String party = partyLabel(spec.partySystemProfile(), partyIndex, targets.length);
            for (int seat = 0; seat < targets[partyIndex] && cursor < ordered.size(); seat++) {
                partyByLegislatorId.put(ordered.get(cursor).id(), party);
                cursor++;
            }
        }
        while (cursor < ordered.size()) {
            partyByLegislatorId.put(
                    ordered.get(cursor).id(),
                    partyLabel(spec.partySystemProfile(), targets.length - 1, targets.length)
            );
            cursor++;
        }

        List<Legislator> assigned = new ArrayList<>();
        for (Legislator legislator : legislators) {
            String party = partyByLegislatorId.getOrDefault(legislator.id(), legislator.party());
            assigned.add(new Legislator(
                    legislator.id(),
                    party,
                    legislator.ideology(),
                    legislator.compromisePreference(),
                    legislator.partyLoyalty(),
                    legislator.constituencySensitivity(),
                    legislator.lobbySensitivity(),
                    legislator.reputationSensitivity(),
                    legislator.districtPreference(),
                    legislator.districtIntensity(),
                    legislator.affectedGroupSensitivity()
            ));
        }
        return assigned;
    }

    private static int[] partySeatTargets(WorldSpec spec, Random random) {
        double[] shares = partyShares(spec.partySystemProfile(), spec.partyCount(), random);
        int[] seats = new int[shares.length];
        double[] remainders = new double[shares.length];
        int total = spec.legislatorCount();
        int assigned = 0;

        if (total >= shares.length) {
            for (int i = 0; i < seats.length; i++) {
                seats[i] = 1;
                assigned++;
            }
        }

        int remaining = total - assigned;
        for (int i = 0; i < shares.length; i++) {
            double raw = shares[i] * remaining;
            int additional = (int) Math.floor(raw);
            seats[i] += additional;
            assigned += additional;
            remainders[i] = raw - additional;
        }

        while (assigned < total) {
            int bestIndex = 0;
            for (int i = 1; i < remainders.length; i++) {
                if (remainders[i] > remainders[bestIndex]) {
                    bestIndex = i;
                }
            }
            seats[bestIndex]++;
            remainders[bestIndex] = -1.0;
            assigned++;
        }
        return seats;
    }

    private static double[] partyShares(PartySystemProfile profile, int partyCount, Random random) {
        double[] shares = new double[partyCount];
        if (partyCount == 1) {
            shares[0] = 1.0;
            return shares;
        }

        switch (profile) {
            case TWO_MAJOR_WITH_MINOR_PARTIES -> {
                if (partyCount == 2) {
                    shares[0] = Values.clamp(0.52 + random.nextGaussian() * 0.03, 0.45, 0.58);
                    shares[1] = 1.0 - shares[0];
                } else {
                    double leftMajor = Values.clamp(0.42 + random.nextGaussian() * 0.03, 0.34, 0.48);
                    double rightMajor = Values.clamp(0.39 + random.nextGaussian() * 0.03, 0.32, 0.46);
                    double majorTotal = leftMajor + rightMajor;
                    if (majorTotal > 0.86) {
                        leftMajor *= 0.86 / majorTotal;
                        rightMajor *= 0.86 / majorTotal;
                    }
                    shares[0] = leftMajor;
                    shares[partyCount - 1] = rightMajor;
                    distributeRemaining(shares, random, 1.0 - leftMajor - rightMajor, 1, partyCount - 1);
                }
            }
            case DOMINANT_PARTY -> {
                int dominantIndex = partyCount / 2;
                shares[dominantIndex] = Values.clamp(0.58 + random.nextGaussian() * 0.04, 0.48, 0.66);
                distributeRemaining(shares, random, 1.0 - shares[dominantIndex], 0, partyCount);
            }
            case FRAGMENTED_MULTIPARTY -> {
                double total = 0.0;
                for (int i = 0; i < partyCount; i++) {
                    shares[i] = Values.clamp(1.0 + random.nextGaussian() * 0.22, 0.45, 1.55);
                    total += shares[i];
                }
                for (int i = 0; i < partyCount; i++) {
                    shares[i] /= total;
                }
            }
            case IDEOLOGICAL_BINS -> {
                for (int i = 0; i < partyCount; i++) {
                    shares[i] = 1.0 / partyCount;
                }
            }
        }
        return shares;
    }

    private static void distributeRemaining(
            double[] shares,
            Random random,
            double remainingShare,
            int startInclusive,
            int endExclusive
    ) {
        double totalWeight = 0.0;
        double[] weights = new double[shares.length];
        for (int i = startInclusive; i < endExclusive; i++) {
            if (shares[i] == 0.0) {
                weights[i] = Values.clamp(1.0 + random.nextGaussian() * 0.18, 0.55, 1.45);
                totalWeight += weights[i];
            }
        }
        if (totalWeight == 0.0) {
            return;
        }
        for (int i = startInclusive; i < endExclusive; i++) {
            if (weights[i] > 0.0) {
                shares[i] = remainingShare * weights[i] / totalWeight;
            }
        }
    }

    private static String partyLabel(PartySystemProfile profile, int partyIndex, int partyCount) {
        if (partyCount == 1) {
            return "Unified";
        }
        if (partyCount == 2) {
            return partyIndex == 0 ? "Left" : "Right";
        }
        return switch (profile) {
            case TWO_MAJOR_WITH_MINOR_PARTIES -> {
                if (partyIndex == 0) {
                    yield "Major-Left";
                }
                if (partyIndex == partyCount - 1) {
                    yield "Major-Right";
                }
                if (partyIndex == partyCount / 2) {
                    yield "Center-Minor";
                }
                yield partyIndex < partyCount / 2 ? "Left-Minor-" + partyIndex : "Right-Minor-" + (partyCount - partyIndex);
            }
            case DOMINANT_PARTY -> partyIndex == partyCount / 2 ? "Dominant-Center" : "Minor-" + (partyIndex + 1);
            case FRAGMENTED_MULTIPARTY -> "Fragment-" + (partyIndex + 1);
            case IDEOLOGICAL_BINS -> "Party-" + (partyIndex + 1);
        };
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
