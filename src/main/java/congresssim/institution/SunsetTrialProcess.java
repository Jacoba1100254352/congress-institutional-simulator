package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public final class SunsetTrialProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double provisionalRiskThreshold;
    private final double renewalThreshold;

    public SunsetTrialProcess(
            String name,
            LegislativeProcess innerProcess,
            double provisionalRiskThreshold,
            double renewalThreshold
    ) {
        if (provisionalRiskThreshold < 0.0 || renewalThreshold < 0.0) {
            throw new IllegalArgumentException("sunset thresholds must not be negative.");
        }
        this.name = name;
        this.innerProcess = innerProcess;
        this.provisionalRiskThreshold = provisionalRiskThreshold;
        this.renewalThreshold = renewalThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        BillOutcome outcome = innerProcess.consider(bill, context);
        if (!outcome.enacted()) {
            return outcome;
        }

        double risk = AdaptiveTrackProcess.riskScore(bill, context);
        if (risk < provisionalRiskThreshold) {
            return outcome;
        }

        double reviewScore = reviewScore(bill, risk);
        if (reviewScore >= renewalThreshold) {
            return withOutcome(
                    outcome,
                    true,
                    outcome.statusQuoAfter(),
                    "sunset trial renewed; " + outcome.finalReason()
            );
        }
        return withOutcome(
                outcome,
                false,
                outcome.statusQuoBefore(),
                "sunset trial expired; " + outcome.finalReason()
        );
    }

    private static double reviewScore(Bill bill, double risk) {
        return (0.46 * bill.publicBenefit())
                + (0.34 * bill.publicSupport())
                + (0.12 * (1.0 - Math.max(0.0, bill.lobbyPressure())))
                + (0.08 * (1.0 - risk));
    }

    private static BillOutcome withOutcome(
            BillOutcome outcome,
            boolean enacted,
            double statusQuoAfter,
            String reason
    ) {
        return new BillOutcome(
                outcome.bill(),
                outcome.statusQuoBefore(),
                statusQuoAfter,
                enacted,
                outcome.agendaDisposition(),
                outcome.gateResults(),
                outcome.chamberResults(),
                outcome.presidentialAction(),
                outcome.challenged(),
                outcome.signals(),
                reason
        );
    }
}
