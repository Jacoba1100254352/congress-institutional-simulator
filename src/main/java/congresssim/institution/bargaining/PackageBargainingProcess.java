package congresssim.institution.bargaining;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.distribution.AffectedGroupScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class PackageBargainingProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double bargainingThreshold;
    private final double sidePaymentCost;
    private final double implementationDelayCost;
    private final double tradeEffectiveness;

    public PackageBargainingProcess(
            String name,
            LegislativeProcess innerProcess,
            double bargainingThreshold,
            double sidePaymentCost,
            double implementationDelayCost,
            double tradeEffectiveness
    ) {
        Values.requireRange("bargainingThreshold", bargainingThreshold, 0.0, 1.0);
        Values.requireRange("sidePaymentCost", sidePaymentCost, 0.0, 1.0);
        Values.requireRange("implementationDelayCost", implementationDelayCost, 0.0, 1.0);
        Values.requireRange("tradeEffectiveness", tradeEffectiveness, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.bargainingThreshold = bargainingThreshold;
        this.sidePaymentCost = sidePaymentCost;
        this.implementationDelayCost = implementationDelayCost;
        this.tradeEffectiveness = tradeEffectiveness;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double need = bargainingNeed(bill, context);
        if (need < bargainingThreshold) {
            return innerProcess.consider(bill, context);
        }
        return innerProcess.consider(packageDeal(bill, context, need), context);
    }

    private Bill packageDeal(Bill bill, VoteContext context, double need) {
        double policyDelay = implementationDelayCost * bill.publicBenefitUncertainty() * need;
        double sidePayment = sidePaymentCost * (0.30 + (0.70 * bill.concentratedHarm())) * need;
        double supportGain = tradeEffectiveness
                * ((0.16 * need) + (0.18 * bill.concentratedHarm()) + (0.06 * bill.salience()));
        double harmReduction = tradeEffectiveness * (0.22 + (0.42 * need));
        double revisedPosition = Values.clamp(
                bill.ideologyPosition()
                        + (0.05 * need * (context.currentPolicyPosition() - bill.ideologyPosition())),
                -1.0,
                1.0
        );
        Bill revised = bill.withAmendment(
                revisedPosition,
                Values.clamp(bill.publicSupport() + supportGain, 0.0, 1.0),
                Values.clamp(bill.publicBenefit() - sidePayment - policyDelay, 0.0, 1.0)
        );
        double revisedHarm = Values.clamp(revised.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0);
        double affectedSupport = Values.clamp(
                revised.affectedGroupSupport()
                        + ((revised.concentratedHarm() - revisedHarm) * 0.76)
                        + (supportGain * 0.24),
                0.0,
                1.0
        );
        return revised.withCompensation(revised.publicBenefit(), affectedSupport, revisedHarm);
    }

    private static double bargainingNeed(Bill bill, VoteContext context) {
        double lowSupport = Math.max(0.0, 0.58 - bill.publicSupport()) / 0.58;
        double policyDistance = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double harm = AffectedGroupScoring.minorityHarm(bill);
        double uncertainty = bill.publicBenefitUncertainty();
        double upside = Math.max(0.0, bill.publicBenefit() - bill.publicSupport());
        return Values.clamp(
                (0.24 * lowSupport)
                        + (0.18 * policyDistance)
                        + (0.24 * harm)
                        + (0.16 * uncertainty)
                        + (0.18 * upside),
                0.0,
                1.0
        );
    }
}
