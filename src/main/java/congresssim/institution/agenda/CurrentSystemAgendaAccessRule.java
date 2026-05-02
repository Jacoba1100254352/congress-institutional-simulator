package congresssim.institution.agenda;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.List;

final class CurrentSystemAgendaAccessRule implements ProposalAccessRule {
    private final double threshold;

    CurrentSystemAgendaAccessRule(double threshold) {
        this.threshold = threshold;
    }

    @Override
    public String name() {
        return "current-system agenda access";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        double policyStability = 1.0 - (Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0);
        double capturePenalty = Math.max(0.0, bill.lobbyPressure()) * (0.40 + (0.40 * bill.privateGain()));
        double harmPenalty = bill.concentratedHarm() * (1.0 - bill.affectedGroupSupport());
        double uncertaintyPenalty = bill.publicBenefitUncertainty() * (1.0 - bill.publicSupport());
        double sponsorPartyFit = sponsorPartyFit(bill, context);
        double chamberPartyMedian = chamberPartyMedian(context);
        double crossPartyConflict = Math.max(0.0, Math.abs(bill.ideologyPosition() - chamberPartyMedian) - 0.35);
        double partisanQueuePenalty = crossPartyConflict * (0.40 + (0.30 * bill.salience()));
        double observableValueSignal = Values.clamp(
                (0.52 * bill.publicSupport())
                        + (0.22 * bill.salience())
                        + (0.14 * (1.0 - bill.publicBenefitUncertainty()))
                        + (0.12 * (1.0 - harmPenalty)),
                0.0,
                1.0
        );
        double agendaScore =
                (0.24 * bill.publicSupport())
                        + (0.22 * observableValueSignal)
                        + (0.14 * bill.salience())
                        + (0.12 * policyStability)
                        + (0.13 * sponsorPartyFit)
                        + (bill.antiLobbyingReform() ? 0.05 : 0.0)
                        - (0.11 * capturePenalty)
                        - (0.10 * harmPenalty)
                        - (0.07 * uncertaintyPenalty)
                        - (0.10 * partisanQueuePenalty)
                        + deterministicPriorityJitter(bill);

        if (agendaScore < threshold) {
            return AccessDecision.denied("current-system agenda gate did not schedule proposal");
        }
        return AccessDecision.granted("current-system agenda gate scheduled proposal");
    }

    private static double deterministicPriorityJitter(Bill bill) {
        int bucket = Math.floorMod((bill.id() + ":" + bill.proposerId()).hashCode(), 1000);
        return ((bucket / 999.0) - 0.5) * 0.12;
    }

    private static double sponsorPartyFit(Bill bill, VoteContext context) {
        if (context.partyPositions().isEmpty()) {
            return 0.50;
        }
        double sponsorPartyPosition = context.partyPositions()
                .values()
                .stream()
                .min((left, right) -> Double.compare(
                        Math.abs(left - bill.proposerIdeology()),
                        Math.abs(right - bill.proposerIdeology())
                ))
                .orElse(0.0);
        return Values.clamp(1.0 - (Math.abs(bill.ideologyPosition() - sponsorPartyPosition) / 2.0), 0.0, 1.0);
    }

    private static double chamberPartyMedian(VoteContext context) {
        if (context.partyPositions().isEmpty()) {
            return 0.0;
        }
        List<Double> positions = context.partyPositions().values().stream().sorted().toList();
        int midpoint = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(midpoint);
        }
        return (positions.get(midpoint - 1) + positions.get(midpoint)) / 2.0;
    }
}
