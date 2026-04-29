package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

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
        double agendaScore =
                (0.30 * bill.publicSupport())
                        + (0.26 * bill.publicBenefit())
                        + (0.16 * bill.salience())
                        + (0.14 * policyStability)
                        + (bill.antiLobbyingReform() ? 0.05 : 0.0)
                        - (0.14 * capturePenalty)
                        - (0.12 * harmPenalty)
                        - (0.08 * uncertaintyPenalty)
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
}
