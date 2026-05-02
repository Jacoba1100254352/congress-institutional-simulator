package congresssim.institution.agenda;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

final class LobbySurchargeProposalAccessRule implements ProposalAccessRule {
    private final double baseCost;
    private final double publicCreditWeight;
    private final double lobbySurchargeWeight;

    LobbySurchargeProposalAccessRule(double baseCost, double publicCreditWeight, double lobbySurchargeWeight) {
        Values.requireRange("baseCost", baseCost, 0.0, 1.0);
        Values.requireRange("publicCreditWeight", publicCreditWeight, 0.0, 1.0);
        Values.requireRange("lobbySurchargeWeight", lobbySurchargeWeight, 0.0, 1.0);
        this.baseCost = baseCost;
        this.publicCreditWeight = publicCreditWeight;
        this.lobbySurchargeWeight = lobbySurchargeWeight;
    }

    @Override
    public String name() {
        return "lobby surcharge proposal cost";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        double policyGain = proposerPolicyGain(bill, context);
        double publicCredit = publicCreditWeight * ((0.55 * bill.publicSupport()) + (0.45 * bill.publicBenefit()));
        double lobbySurcharge = lobbySurchargeWeight * Math.max(0.0, bill.lobbyPressure()) * (1.0 + bill.privateGain());
        double requiredValue = baseCost + lobbySurcharge + (0.12 * bill.publicBenefitUncertainty());
        if (policyGain + publicCredit < requiredValue) {
            return AccessDecision.denied("proposal value below lobby-surcharged cost");
        }
        return AccessDecision.granted("lobby-surcharged proposal cost cleared");
    }

    private static double proposerPolicyGain(Bill bill, VoteContext context) {
        double statusQuoDistance = Math.abs(context.currentPolicyPosition() - bill.proposerIdeology());
        double billDistance = Math.abs(bill.ideologyPosition() - bill.proposerIdeology());
        return Math.max(0.0, statusQuoDistance - billDistance) / 2.0;
    }
}
