package congresssim.institution.agenda;

import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

final class LeadershipAgendaAccessRule implements ProposalAccessRule {
    private final List<Legislator> legislators;
    private final double threshold;
    private final double majorityFitWeight;
    private final double publicSignalWeight;
    private final double salienceWeight;
    private final double capturePenaltyWeight;
    private final double minorityHarmPenaltyWeight;

    LeadershipAgendaAccessRule(
            List<Legislator> legislators,
            double threshold,
            double majorityFitWeight,
            double publicSignalWeight,
            double salienceWeight,
            double capturePenaltyWeight,
            double minorityHarmPenaltyWeight
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        Values.requireRange("threshold", threshold, 0.0, 1.0);
        this.legislators = List.copyOf(legislators);
        this.threshold = threshold;
        this.majorityFitWeight = majorityFitWeight;
        this.publicSignalWeight = publicSignalWeight;
        this.salienceWeight = salienceWeight;
        this.capturePenaltyWeight = capturePenaltyWeight;
        this.minorityHarmPenaltyWeight = minorityHarmPenaltyWeight;
    }

    @Override
    public String name() {
        return "leadership agenda cartel";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        double majorityMedian = majorityPartyMedian();
        double majorityFit = 1.0 - (Math.abs(bill.ideologyPosition() - majorityMedian) / 2.0);
        double publicSignal = (0.62 * bill.publicSupport())
                + (0.20 * (1.0 - bill.publicBenefitUncertainty()))
                + (0.18 * bill.salience());
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double minorityHarm = AffectedGroupScoring.minorityHarm(bill);
        double antiLobbyingBonus = bill.antiLobbyingReform() ? 0.04 : 0.0;
        double score = (majorityFitWeight * majorityFit)
                + (publicSignalWeight * publicSignal)
                + (salienceWeight * bill.salience())
                + antiLobbyingBonus
                - (capturePenaltyWeight * captureRisk)
                - (minorityHarmPenaltyWeight * minorityHarm)
                + deterministicSchedulingJitter(bill);

        if (score < threshold) {
            return AccessDecision.denied("leadership agenda did not schedule proposal");
        }
        return AccessDecision.granted("leadership agenda scheduled proposal");
    }

    private double majorityPartyMedian() {
        Map<String, Integer> counts = new HashMap<>();
        for (Legislator legislator : legislators) {
            counts.merge(legislator.party(), 1, Integer::sum);
        }
        String majorityParty = counts.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(legislators.getFirst().party());
        List<Double> positions = legislators.stream()
                .filter(legislator -> legislator.party().equals(majorityParty))
                .map(Legislator::ideology)
                .sorted()
                .toList();
        if (positions.isEmpty()) {
            return 0.0;
        }
        int middle = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(middle);
        }
        return (positions.get(middle - 1) + positions.get(middle)) / 2.0;
    }

    private static double deterministicSchedulingJitter(Bill bill) {
        int bucket = Math.floorMod(("leadership:" + bill.id() + ":" + bill.proposerId()).hashCode(), 1000);
        return ((bucket / 999.0) - 0.5) * 0.10;
    }
}
