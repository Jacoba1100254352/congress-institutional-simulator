package congresssim.institution.agenda;

import congresssim.behavior.VoteContext;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;

public final class FloorRuleSchedulingProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double openRuleNorm;
    private final double leadershipClosurePressure;
    private final double queueDelayBase;
    private final double dischargeMandateThreshold;
    private final double fallbackBlockThreshold;

    public FloorRuleSchedulingProcess(
            String name,
            LegislativeProcess innerProcess,
            double openRuleNorm,
            double leadershipClosurePressure,
            double queueDelayBase,
            double dischargeMandateThreshold,
            double fallbackBlockThreshold
    ) {
        Values.requireRange("openRuleNorm", openRuleNorm, 0.0, 1.0);
        Values.requireRange("leadershipClosurePressure", leadershipClosurePressure, 0.0, 1.0);
        Values.requireRange("queueDelayBase", queueDelayBase, 0.0, 1.0);
        Values.requireRange("dischargeMandateThreshold", dischargeMandateThreshold, 0.0, 1.0);
        Values.requireRange("fallbackBlockThreshold", fallbackBlockThreshold, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.openRuleNorm = openRuleNorm;
        this.leadershipClosurePressure = leadershipClosurePressure;
        this.queueDelayBase = queueDelayBase;
        this.dischargeMandateThreshold = dischargeMandateThreshold;
        this.fallbackBlockThreshold = fallbackBlockThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double mandate = mandateScore(bill);
        double risk = schedulingRisk(bill, context);
        double capture = LobbyCaptureScoring.captureRisk(bill);
        double closureScore = Values.clamp(
                leadershipClosurePressure
                        + (0.20 * capture)
                        + (0.14 * risk)
                        + (0.12 * Math.max(0.0, Math.abs(bill.ideologyPosition()) - 0.35))
                        - (0.22 * mandate)
                        - (0.18 * openRuleNorm),
                0.0,
                1.0
        );
        boolean dischargeBackstop = mandate >= dischargeMandateThreshold
                && bill.salience() >= 0.52
                && capture < 0.72;
        boolean closedRule = !dischargeBackstop && closureScore >= Math.max(0.34, openRuleNorm);
        double statusQuoFallbackPressure = Values.clamp(
                closureScore
                        + (0.22 * (1.0 - mandate))
                        + (0.12 * risk)
                        - (dischargeBackstop ? 0.28 : 0.0),
                0.0,
                1.0
        );
        double delay = Values.clamp(
                queueDelayBase
                        + (0.24 * statusQuoFallbackPressure)
                        + (closedRule ? 0.12 : 0.0)
                        - (dischargeBackstop ? 0.16 : 0.0),
                0.0,
                1.0
        );
        OutcomeSignals signals = OutcomeSignals.diagnostics(Map.of(
                "floorSchedulingDelay",
                delay,
                "closedRuleRate",
                closedRule ? 1.0 : 0.0,
                "openRuleRate",
                closedRule ? 0.0 : 1.0,
                "dischargeBackstopUse",
                dischargeBackstop ? 1.0 : 0.0,
                "statusQuoFallbackPressure",
                statusQuoFallbackPressure,
                "leadershipSchedulingBias",
                Values.clamp(closureScore * leadershipClosurePressure, 0.0, 1.0),
                "rulesCommitteeCaptureIndex",
                Values.clamp(capture * leadershipClosurePressure * (closedRule ? 1.0 : 0.55), 0.0, 1.0)
        ));

        if (!dischargeBackstop && statusQuoFallbackPressure >= fallbackBlockThreshold && mandate < 0.36) {
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    "floor calendar fallback to status quo"
            ).withSignals(signals);
        }

        double opennessPenalty = closedRule ? 0.0 : 0.04 * (mandate - risk);
        Bill scheduled = bill.withAttentionSpend(delay + Math.max(0.0, -opennessPenalty));
        return innerProcess.consider(scheduled, context).withSignals(signals);
    }

    private static double mandateScore(Bill bill) {
        return Values.clamp(
                (0.46 * bill.publicSupport())
                        + (0.22 * bill.salience())
                        + (0.16 * bill.affectedGroupSupport())
                        + (0.10 * bill.publicBenefit())
                        + (0.06 * Math.clamp(bill.cosponsorCount() / 10.0, 0.0, 1.0))
                        - (0.16 * LobbyCaptureScoring.captureRisk(bill)),
                0.0,
                1.0
        );
    }

    private static double schedulingRisk(Bill bill, VoteContext context) {
        return Values.clamp(
                (0.26 * (1.0 - bill.publicSupport()))
                        + (0.20 * AffectedGroupScoring.minorityHarm(bill))
                        + (0.18 * bill.publicBenefitUncertainty())
                        + (0.14 * LobbyCaptureScoring.captureRisk(bill))
                        + (0.12 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
                        + (0.10 * bill.salience()),
                0.0,
                1.0
        );
    }
}
