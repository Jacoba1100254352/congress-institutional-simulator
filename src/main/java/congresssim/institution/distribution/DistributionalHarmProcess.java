package congresssim.institution.distribution;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class DistributionalHarmProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double harmThreshold;
    private final double consentThreshold;
    private final double harmReductionRate;
    private final double compensationEfficiencyLoss;
    private final boolean requireAffectedConsent;

    public DistributionalHarmProcess(
            String name,
            LegislativeProcess innerProcess,
            double harmThreshold,
            double consentThreshold,
            double harmReductionRate,
            double compensationEfficiencyLoss,
            boolean requireAffectedConsent
    ) {
        Values.requireRange("harmThreshold", harmThreshold, 0.0, 1.0);
        Values.requireRange("consentThreshold", consentThreshold, 0.0, 1.0);
        Values.requireRange("harmReductionRate", harmReductionRate, 0.0, 1.0);
        Values.requireRange("compensationEfficiencyLoss", compensationEfficiencyLoss, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.harmThreshold = harmThreshold;
        this.consentThreshold = consentThreshold;
        this.harmReductionRate = harmReductionRate;
        this.compensationEfficiencyLoss = compensationEfficiencyLoss;
        this.requireAffectedConsent = requireAffectedConsent;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill reviewedBill = bill;
        if (bill.concentratedHarm() >= harmThreshold && bill.affectedGroupSupport() < consentThreshold) {
            reviewedBill = compensate(bill);
            if (requireAffectedConsent && reviewedBill.affectedGroupSupport() < consentThreshold) {
                return BillOutcome.accessDenied(
                        reviewedBill,
                        context.currentPolicyPosition(),
                        "affected-group consent withheld after compensation"
                );
            }
        }
        return innerProcess.consider(reviewedBill, context);
    }

    private Bill compensate(Bill bill) {
        double revisedHarm = Values.clamp(bill.concentratedHarm() * (1.0 - harmReductionRate), 0.0, 1.0);
        double supportGain = (bill.concentratedHarm() - revisedHarm) * 0.72;
        double revisedAffectedSupport = Values.clamp(bill.affectedGroupSupport() + supportGain, 0.0, 1.0);
        double revisedPublicBenefit = Values.clamp(
                bill.publicBenefit() - (bill.compensationCost() * compensationEfficiencyLoss),
                0.0,
                1.0
        );
        return bill.withCompensation(revisedPublicBenefit, revisedAffectedSupport, revisedHarm);
    }
}
