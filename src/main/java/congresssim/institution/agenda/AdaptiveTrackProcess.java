package congresssim.institution.agenda;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public final class AdaptiveTrackProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess fastLaneProcess;
    private final LegislativeProcess middleLaneProcess;
    private final LegislativeProcess highRiskProcess;
    private final double fastLaneMaximumRisk;
    private final double highRiskMinimumRisk;

    public AdaptiveTrackProcess(
            String name,
            LegislativeProcess fastLaneProcess,
            LegislativeProcess middleLaneProcess,
            LegislativeProcess highRiskProcess,
            double fastLaneMaximumRisk,
            double highRiskMinimumRisk
    ) {
        if (fastLaneMaximumRisk < 0.0 || highRiskMinimumRisk < 0.0) {
            throw new IllegalArgumentException("risk thresholds must not be negative.");
        }
        if (fastLaneMaximumRisk >= highRiskMinimumRisk) {
            throw new IllegalArgumentException("fastLaneMaximumRisk must be lower than highRiskMinimumRisk.");
        }
        this.name = name;
        this.fastLaneProcess = fastLaneProcess;
        this.middleLaneProcess = middleLaneProcess;
        this.highRiskProcess = highRiskProcess;
        this.fastLaneMaximumRisk = fastLaneMaximumRisk;
        this.highRiskMinimumRisk = highRiskMinimumRisk;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double risk = riskScore(bill, context);
        if (risk <= fastLaneMaximumRisk) {
            return fastLaneProcess.consider(bill, context).withSignals(OutcomeSignals.route("fast"));
        }
        if (risk >= highRiskMinimumRisk) {
            return highRiskProcess.consider(bill, context).withSignals(OutcomeSignals.route("high"));
        }
        return middleLaneProcess.consider(bill, context).withSignals(OutcomeSignals.route("middle"));
    }

    public static double riskScore(Bill bill, VoteContext context) {
        double lowSupportRisk = 1.0 - bill.publicSupport();
        double shiftRisk = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double lobbyRisk = Math.max(0.0, bill.lobbyPressure());
        double salienceRisk = bill.salience();
        double signalUncertainty = Math.max(
                bill.publicBenefitUncertainty(),
                Math.abs(bill.publicSupport() - bill.publicBenefit()) * 0.65
        );
        double lowWelfareRisk = 1.0 - bill.publicBenefit();

        return (0.26 * lowSupportRisk)
                + (0.22 * shiftRisk)
                + (0.18 * lobbyRisk)
                + (0.14 * salienceRisk)
                + (0.12 * signalUncertainty)
                + (0.08 * lowWelfareRisk);
    }
}
