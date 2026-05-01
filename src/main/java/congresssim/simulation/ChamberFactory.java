package congresssim.simulation;

import congresssim.model.Legislator;
import congresssim.model.RepresentationProfile;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class ChamberFactory {
    private ChamberFactory() {
    }

    public static List<Legislator> select(List<Legislator> legislators, ChamberSpec spec, long seed) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        int size = Math.clamp(spec.targetSize(), 1, legislators.size());
        List<Legislator> selected = switch (spec.seatAllocationProfile()) {
            case EQUAL_POPULATION_SINGLE_MEMBER -> representative(legislators, size);
            case PROPORTIONAL_PARTY_LIST -> partyProportional(
                    legislators,
                    size,
                    effectiveThreshold(spec.legalThreshold(), spec.districtMagnitude())
            );
            case MIXED_MEMBER -> mixedMember(
                    legislators,
                    size,
                    effectiveThreshold(spec.legalThreshold(), spec.districtMagnitude())
            );
            case EQUAL_TERRITORIAL -> territorial(legislators, size, spec.territorialUnitCount(), 0.0);
            case BANDED_TERRITORIAL -> territorial(legislators, size, spec.territorialUnitCount(), 0.45);
            case MALAPPORTIONED_TERRITORIAL -> territorial(
                    legislators,
                    size,
                    spec.territorialUnitCount(),
                    Math.max(0.55, spec.malapportionmentStrength())
            );
            case APPOINTED -> appointed(legislators, size);
            case MIXED_ELECTED_APPOINTED -> mixedAppointed(legislators, size, spec.appointedShare(), seed);
        };
        return annotateSelection(selected, spec);
    }

    public static List<RepresentationUnit> representationUnits(ChamberSpec spec) {
        int units = Math.clamp(spec.territorialUnitCount(), 1, spec.targetSize());
        return switch (spec.seatAllocationProfile()) {
            case EQUAL_POPULATION_SINGLE_MEMBER, PROPORTIONAL_PARTY_LIST, MIXED_MEMBER -> equalPopulationUnits(spec, units);
            case EQUAL_TERRITORIAL -> territorialUnits(spec, units, 0.0);
            case BANDED_TERRITORIAL -> territorialUnits(spec, units, 0.45);
            case MALAPPORTIONED_TERRITORIAL -> territorialUnits(spec, units, Math.max(0.55, spec.malapportionmentStrength()));
            case APPOINTED -> appointedUnits(spec, units, 1.0);
            case MIXED_ELECTED_APPOINTED -> appointedUnits(spec, units, spec.appointedShare());
        };
    }

    private static List<Legislator> representative(List<Legislator> legislators, int size) {
        List<Legislator> sorted = new ArrayList<>(legislators);
        sorted.sort(Comparator.comparingDouble(Legislator::districtPreference));
        return evenlySpaced(sorted, size);
    }

    private static List<Legislator> partyProportional(List<Legislator> legislators, int size, double legalThreshold) {
        Map<String, List<Legislator>> byParty = byParty(legislators);
        List<String> parties = byParty.entrySet()
                .stream()
                .filter(entry -> (double) entry.getValue().size() / legislators.size() >= legalThreshold)
                .map(Map.Entry::getKey)
                .sorted()
                .toList();
        if (parties.isEmpty()) {
            parties = byParty.keySet().stream().sorted().toList();
        }

        Map<String, Integer> seatsByParty = allocateSeats(parties, byParty, legislators.size(), size);
        List<Legislator> selected = new ArrayList<>();
        for (String party : parties) {
            List<Legislator> partyMembers = new ArrayList<>(byParty.get(party));
            partyMembers.sort(Comparator.comparingDouble(Legislator::ideology));
            selected.addAll(evenlySpaced(partyMembers, seatsByParty.getOrDefault(party, 0)));
        }
        return trimOrFill(selected, legislators, size);
    }

    private static List<Legislator> mixedMember(List<Legislator> legislators, int size, double legalThreshold) {
        int districtSeats = size / 2;
        List<Legislator> selected = new ArrayList<>(representative(legislators, districtSeats));
        addUnique(selected, partyProportional(legislators, size - districtSeats, legalThreshold), size);
        return trimOrFill(selected, legislators, size);
    }

    private static List<Legislator> territorial(List<Legislator> legislators, int size, int unitCount, double strength) {
        int units = Math.clamp(unitCount, 1, Math.min(size, legislators.size()));
        List<List<Legislator>> buckets = districtBuckets(legislators, units);
        List<Integer> seats = territorialSeatTargets(size, units, strength);
        List<Legislator> selected = new ArrayList<>();
        for (int i = 0; i < buckets.size(); i++) {
            selected.addAll(evenlySpaced(buckets.get(i), seats.get(i)));
        }
        return trimOrFill(selected, legislators, size);
    }

    private static List<Legislator> appointed(List<Legislator> legislators, int size) {
        return legislators.stream()
                .sorted(Comparator.comparingDouble(ChamberFactory::appointmentScore).reversed())
                .limit(size)
                .toList();
    }

    private static List<Legislator> mixedAppointed(List<Legislator> legislators, int size, double appointedShare, long seed) {
        int appointedSeats = (int) Math.round(size * Math.clamp(appointedShare, 0.0, 1.0));
        List<Legislator> selected = new ArrayList<>(appointed(legislators, appointedSeats));
        List<Legislator> shuffled = new ArrayList<>(legislators);
        Collections.shuffle(shuffled, new Random(seed));
        addUnique(selected, evenlySpaced(shuffled, size - appointedSeats), size);
        return trimOrFill(selected, legislators, size);
    }

    private static List<RepresentationUnit> equalPopulationUnits(ChamberSpec spec, int unitCount) {
        List<RepresentationUnit> units = new ArrayList<>();
        for (int i = 0; i < unitCount; i++) {
            units.add(new RepresentationUnit(
                    spec.name() + "-U" + (i + 1),
                    1.0 / unitCount,
                    1.0 / unitCount,
                    spec.districtMagnitude(),
                    spec.selectionMode()
            ));
        }
        return units;
    }

    private static List<RepresentationUnit> territorialUnits(ChamberSpec spec, int unitCount, double strength) {
        double[] populations = weightedShares(unitCount, strength);
        double[] seats = equalShares(unitCount);
        List<RepresentationUnit> units = new ArrayList<>();
        for (int i = 0; i < unitCount; i++) {
            units.add(new RepresentationUnit(
                    spec.name() + "-T" + (i + 1),
                    populations[i],
                    seats[i],
                    spec.districtMagnitude(),
                    spec.selectionMode()
            ));
        }
        return units;
    }

    private static List<RepresentationUnit> appointedUnits(ChamberSpec spec, int unitCount, double appointedShare) {
        List<RepresentationUnit> units = new ArrayList<>();
        double appointedRemaining = appointedShare;
        for (int i = 0; i < unitCount; i++) {
            double seatShare = 1.0 / unitCount;
            boolean appointed = appointedRemaining > 0.000001;
            double appointedPortion = appointed ? Math.min(seatShare, appointedRemaining) : 0.0;
            appointedRemaining -= appointedPortion;
            units.add(new RepresentationUnit(
                    spec.name() + "-A" + (i + 1),
                    1.0 / unitCount,
                    seatShare,
                    spec.districtMagnitude(),
                    appointed ? SelectionMode.APPOINTED_COMMISSION : SelectionMode.ELECTED_SINGLE_MEMBER
            ));
        }
        return units;
    }

    private static List<Legislator> evenlySpaced(List<Legislator> sorted, int size) {
        if (sorted.isEmpty() || size <= 0) {
            return List.of();
        }
        if (size == 1) {
            return List.of(sorted.get(sorted.size() / 2));
        }
        List<Legislator> selected = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            int index = (int) Math.round(i * (sorted.size() - 1.0) / (size - 1.0));
            selected.add(sorted.get(index));
        }
        return selected;
    }

    private static List<Legislator> trimOrFill(List<Legislator> selected, List<Legislator> candidates, int size) {
        List<Legislator> result = new ArrayList<>();
        Set<String> ids = new HashSet<>();
        for (Legislator legislator : selected) {
            if (ids.add(legislator.id())) {
                result.add(legislator);
            }
            if (result.size() >= size) {
                return result;
            }
        }
        for (Legislator legislator : candidates) {
            if (ids.add(legislator.id())) {
                result.add(legislator);
            }
            if (result.size() >= size) {
                break;
            }
        }
        return result;
    }

    private static List<Legislator> annotateSelection(List<Legislator> selected, ChamberSpec spec) {
        if (selected.isEmpty()) {
            return selected;
        }
        List<RepresentationUnit> units = representationUnits(spec);
        Map<Integer, Integer> seatsByUnit = new HashMap<>();
        for (int i = 0; i < selected.size(); i++) {
            seatsByUnit.merge(unitIndexForSeat(i, selected.size(), units.size()), 1, Integer::sum);
        }

        List<Legislator> annotated = new ArrayList<>();
        for (int i = 0; i < selected.size(); i++) {
            int unitIndex = unitIndexForSeat(i, selected.size(), units.size());
            RepresentationUnit unit = units.get(unitIndex);
            int seatsInUnit = Math.max(1, seatsByUnit.getOrDefault(unitIndex, 1));
            int termLength = unit.appointed() ? spec.upperHouseTermLength() : spec.lowerHouseTermLength();
            int cohortCount = Math.max(1, spec.renewalCohortCount());
            int renewalCohort = unitIndex % cohortCount;
            int nextRenewalRound = renewalRound(termLength, cohortCount, renewalCohort);
            RepresentationProfile profile = new RepresentationProfile(
                    spec.name(),
                    Values.clamp(unit.populationShare() / seatsInUnit, 0.0, 1.0),
                    unit.districtMagnitude(),
                    unit.id(),
                    unit.selectionMode().name(),
                    unit.appointed(),
                    spec.lowerHouseTermLength(),
                    spec.upperHouseTermLength(),
                    renewalCohort,
                    termLength,
                    nextRenewalRound,
                    spec.selectorBody()
            );
            annotated.add(selected.get(i).withRepresentationProfile(profile));
        }
        return annotated;
    }

    private static int unitIndexForSeat(int seatIndex, int seatCount, int unitCount) {
        return Math.min(unitCount - 1, (int) Math.floor((double) seatIndex * unitCount / seatCount));
    }

    private static int renewalRound(int termLength, int cohortCount, int renewalCohort) {
        if (cohortCount <= 1) {
            return termLength;
        }
        double spacing = (double) termLength / cohortCount;
        return Math.max(1, (int) Math.round((renewalCohort + 1) * spacing));
    }

    private static void addUnique(List<Legislator> selected, List<Legislator> candidates, int size) {
        Set<String> ids = new HashSet<>();
        for (Legislator legislator : selected) {
            ids.add(legislator.id());
        }
        for (Legislator legislator : candidates) {
            if (selected.size() >= size) {
                return;
            }
            if (ids.add(legislator.id())) {
                selected.add(legislator);
            }
        }
    }

    private static Map<String, List<Legislator>> byParty(List<Legislator> legislators) {
        Map<String, List<Legislator>> byParty = new HashMap<>();
        for (Legislator legislator : legislators) {
            byParty.computeIfAbsent(legislator.party(), ignored -> new ArrayList<>()).add(legislator);
        }
        return byParty;
    }

    private static Map<String, Integer> allocateSeats(
            List<String> parties,
            Map<String, List<Legislator>> byParty,
            int totalMembers,
            int seatCount
    ) {
        Map<String, Integer> seats = new HashMap<>();
        Map<String, Double> remainders = new HashMap<>();
        int assigned = 0;
        for (String party : parties) {
            double exact = ((double) byParty.get(party).size() / totalMembers) * seatCount;
            int whole = (int) Math.floor(exact);
            seats.put(party, whole);
            remainders.put(party, exact - whole);
            assigned += whole;
        }
        while (assigned < seatCount) {
            String best = parties.stream()
                    .max(Comparator.comparingDouble(party -> remainders.getOrDefault(party, 0.0)))
                    .orElse(parties.getFirst());
            seats.merge(best, 1, Integer::sum);
            remainders.put(best, -1.0);
            assigned++;
        }
        return seats;
    }

    private static List<List<Legislator>> districtBuckets(List<Legislator> legislators, int unitCount) {
        List<Legislator> sorted = new ArrayList<>(legislators);
        sorted.sort(Comparator.comparingDouble(Legislator::districtPreference));
        List<List<Legislator>> buckets = new ArrayList<>();
        for (int i = 0; i < unitCount; i++) {
            buckets.add(new ArrayList<>());
        }
        for (int i = 0; i < sorted.size(); i++) {
            int index = Math.min(unitCount - 1, (int) Math.floor((double) i * unitCount / sorted.size()));
            buckets.get(index).add(sorted.get(i));
        }
        return buckets;
    }

    private static List<Integer> territorialSeatTargets(int seatCount, int unitCount, double strength) {
        double[] shares = strength <= 0.000001 ? equalShares(unitCount) : equalShares(unitCount);
        int base = seatCount / unitCount;
        int remainder = seatCount % unitCount;
        List<Integer> seats = new ArrayList<>();
        for (int i = 0; i < unitCount; i++) {
            seats.add(base + (i < remainder ? 1 : 0));
        }
        return seats;
    }

    private static double[] weightedShares(int unitCount, double strength) {
        double[] raw = new double[unitCount];
        double total = 0.0;
        for (int i = 0; i < unitCount; i++) {
            double rank = (double) (i + 1) / unitCount;
            raw[i] = Values.clamp(1.0 + (strength * (rank * 2.8 - 1.4)), 0.08, 4.0);
            total += raw[i];
        }
        for (int i = 0; i < unitCount; i++) {
            raw[i] /= total;
        }
        return raw;
    }

    private static double[] equalShares(int unitCount) {
        double[] shares = new double[unitCount];
        for (int i = 0; i < unitCount; i++) {
            shares[i] = 1.0 / unitCount;
        }
        return shares;
    }

    private static double appointmentScore(Legislator legislator) {
        return legislator.reputationSensitivity()
                + legislator.compromisePreference()
                + legislator.constituencySensitivity()
                - legislator.lobbySensitivity()
                - (0.20 * Math.abs(legislator.ideology()));
    }

    private static double effectiveThreshold(double legalThreshold, int districtMagnitude) {
        double magnitudeThreshold = 0.50 / (districtMagnitude + 1.0);
        return Values.clamp(Math.max(legalThreshold, magnitudeThreshold), 0.0, 1.0);
    }
}
