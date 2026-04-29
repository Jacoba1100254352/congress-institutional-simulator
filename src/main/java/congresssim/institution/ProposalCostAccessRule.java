package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

final class ProposalCostAccessRule implements ProposalAccessRule {
    private final double baseCost;
    private final double publicCreditWeight;
    private final double lobbyCreditWeight;

    ProposalCostAccessRule(double baseCost, double publicCreditWeight, double lobbyCreditWeight) {
        Values.requireRange("baseCost", baseCost, 0.0, 1.0);
        Values.requireRange("publicCreditWeight", publicCreditWeight, 0.0, 1.0);
        Values.requireRange("lobbyCreditWeight", lobbyCreditWeight, 0.0, 1.0);
        this.baseCost = baseCost;
        this.publicCreditWeight = publicCreditWeight;
        this.lobbyCreditWeight = lobbyCreditWeight;
    }

    @Override
    public String name() {
        return "proposal cost";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        double policyGain = proposerPolicyGain(bill, context);
        double publicCredit = publicCreditWeight * bill.publicSupport() * bill.salience();
        double lobbyCredit = lobbyCreditWeight * Math.max(0.0, bill.lobbyPressure());
        double expectedValue = policyGain + publicCredit + lobbyCredit;

        if (expectedValue < baseCost) {
            return AccessDecision.denied("proposal value below cost threshold");
        }
        return AccessDecision.granted("proposal cost cleared");
    }

    private static double proposerPolicyGain(Bill bill, VoteContext context) {
        double statusQuoDistance = Math.abs(context.currentPolicyPosition() - bill.proposerIdeology());
        double billDistance = Math.abs(bill.ideologyPosition() - bill.proposerIdeology());
        return Math.max(0.0, statusQuoDistance - billDistance) / 2.0;
    }
}

