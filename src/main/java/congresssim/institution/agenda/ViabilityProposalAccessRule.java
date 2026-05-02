package congresssim.institution.agenda;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

final class ViabilityProposalAccessRule implements ProposalAccessRule {
    private final double minimumPublicSupport;
    private final double maximumPolicyShift;

    ViabilityProposalAccessRule(double minimumPublicSupport, double maximumPolicyShift) {
        if (minimumPublicSupport < 0.0 || minimumPublicSupport > 1.0) {
            throw new IllegalArgumentException("minimumPublicSupport must be in [0, 1].");
        }
        if (maximumPolicyShift < 0.0 || maximumPolicyShift > 2.0) {
            throw new IllegalArgumentException("maximumPolicyShift must be in [0, 2].");
        }
        this.minimumPublicSupport = minimumPublicSupport;
        this.maximumPolicyShift = maximumPolicyShift;
    }

    @Override
    public String name() {
        return "viability screen";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        if (bill.publicSupport() < minimumPublicSupport) {
            return AccessDecision.denied("public support below proposal-access threshold");
        }

        double policyShift = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition());
        if (policyShift > maximumPolicyShift) {
            return AccessDecision.denied("proposal too distant from current status quo");
        }

        return AccessDecision.granted("proposal cleared viability screen");
    }
}

