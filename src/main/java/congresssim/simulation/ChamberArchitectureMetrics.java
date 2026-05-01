package congresssim.simulation;

import congresssim.model.Legislator;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ChamberArchitectureMetrics {
    private ChamberArchitectureMetrics() {
    }

    public static double malapportionmentIndex(List<RepresentationUnit> units) {
        if (units.isEmpty()) {
            return 0.0;
        }
        double total = 0.0;
        for (RepresentationUnit unit : units) {
            total += Math.abs(unit.seatShare() - unit.populationShare());
        }
        return Math.clamp(total / 2.0, 0.0, 1.0);
    }

    public static double populationSeatDistortion(List<RepresentationUnit> units) {
        return malapportionmentIndex(units);
    }

    public static double appointedSeatShare(List<RepresentationUnit> units) {
        double total = 0.0;
        for (RepresentationUnit unit : units) {
            if (unit.appointed()) {
                total += unit.seatShare();
            }
        }
        return Math.clamp(total, 0.0, 1.0);
    }

    public static double perCitizenVotingPowerVariance(List<RepresentationUnit> units) {
        if (units.isEmpty()) {
            return 0.0;
        }
        double mean = 0.0;
        double[] powers = new double[units.size()];
        for (int i = 0; i < units.size(); i++) {
            RepresentationUnit unit = units.get(i);
            powers[i] = unit.populationShare() == 0.0 ? 0.0 : unit.seatShare() / unit.populationShare();
            mean += powers[i];
        }
        mean /= powers.length;
        double variance = 0.0;
        for (double power : powers) {
            double delta = power - mean;
            variance += delta * delta;
        }
        return Math.clamp(variance / powers.length, 0.0, 1.0);
    }

    public static double democraticResponsiveness(List<RepresentationUnit> units) {
        if (units.isEmpty()) {
            return 0.0;
        }
        double electedShare = 1.0 - appointedSeatShare(units);
        double averageMagnitude = units.stream()
                .mapToInt(RepresentationUnit::districtMagnitude)
                .average()
                .orElse(1.0);
        double magnitudeScore = Math.clamp(averageMagnitude / (averageMagnitude + 4.0), 0.0, 1.0);
        return Math.clamp(
                (0.45 * electedShare)
                        + (0.25 * (1.0 - populationSeatDistortion(units)))
                        + (0.20 * (1.0 - perCitizenVotingPowerVariance(units)))
                        + (0.10 * magnitudeScore),
                0.0,
                1.0
        );
    }

    public static double constituencyServiceConcentration(List<RepresentationUnit> units) {
        if (units.isEmpty()) {
            return 0.0;
        }
        double averageMagnitude = units.stream()
                .mapToInt(RepresentationUnit::districtMagnitude)
                .average()
                .orElse(1.0);
        double singleMemberConcentration = 1.0 / Math.sqrt(Math.max(1.0, averageMagnitude));
        return Math.clamp(
                (0.70 * singleMemberConcentration)
                        + (0.30 * perCitizenVotingPowerVariance(units)),
                0.0,
                1.0
        );
    }

    public static double regionalTransferBias(List<RepresentationUnit> units) {
        if (units.isEmpty()) {
            return 0.0;
        }
        double meanPopulationShare = 1.0 / units.size();
        double overrepresentationOfSmallUnits = 0.0;
        for (RepresentationUnit unit : units) {
            if (unit.populationShare() < meanPopulationShare) {
                overrepresentationOfSmallUnits += Math.max(0.0, unit.seatShare() - unit.populationShare());
            }
        }
        return Math.clamp(overrepresentationOfSmallUnits, 0.0, 1.0);
    }

    public static double chamberMedianGap(List<Legislator> firstChamber, List<Legislator> secondChamber) {
        return Math.abs(medianIdeology(firstChamber) - medianIdeology(secondChamber)) / 2.0;
    }

    public static double chamberIncongruenceIndex(List<Legislator> firstChamber, List<Legislator> secondChamber) {
        Map<String, Double> firstShares = partyShares(firstChamber);
        Map<String, Double> secondShares = partyShares(secondChamber);
        double total = 0.0;
        for (String party : unionKeys(firstShares, secondShares)) {
            total += Math.abs(firstShares.getOrDefault(party, 0.0) - secondShares.getOrDefault(party, 0.0));
        }
        return Math.clamp(total / 2.0, 0.0, 1.0);
    }

    public static double seatVoteDistortion(List<Legislator> electorate, List<Legislator> chamber) {
        Map<String, Double> electorateShares = partyShares(electorate);
        Map<String, Double> chamberShares = partyShares(chamber);
        double total = 0.0;
        for (String party : unionKeys(electorateShares, chamberShares)) {
            total += Math.abs(electorateShares.getOrDefault(party, 0.0) - chamberShares.getOrDefault(party, 0.0));
        }
        return Math.clamp(total / 2.0, 0.0, 1.0);
    }

    public static double effectivePartyCount(List<Legislator> members) {
        Map<String, Double> shares = partyShares(members);
        double sumSquares = 0.0;
        for (double share : shares.values()) {
            sumSquares += share * share;
        }
        return sumSquares == 0.0 ? 0.0 : 1.0 / sumSquares;
    }

    private static List<String> unionKeys(Map<String, Double> first, Map<String, Double> second) {
        return java.util.stream.Stream.concat(first.keySet().stream(), second.keySet().stream())
                .distinct()
                .toList();
    }

    private static Map<String, Double> partyShares(List<Legislator> members) {
        Map<String, Integer> counts = new HashMap<>();
        for (Legislator member : members) {
            counts.merge(member.party(), 1, Integer::sum);
        }
        Map<String, Double> shares = new HashMap<>();
        for (Map.Entry<String, Integer> entry : counts.entrySet()) {
            shares.put(entry.getKey(), members.isEmpty() ? 0.0 : (double) entry.getValue() / members.size());
        }
        return shares;
    }

    private static double medianIdeology(List<Legislator> members) {
        if (members.isEmpty()) {
            return 0.0;
        }
        List<Double> positions = members.stream()
                .map(Legislator::ideology)
                .sorted()
                .toList();
        int middle = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(middle);
        }
        return (positions.get(middle - 1) + positions.get(middle)) / 2.0;
    }
}
