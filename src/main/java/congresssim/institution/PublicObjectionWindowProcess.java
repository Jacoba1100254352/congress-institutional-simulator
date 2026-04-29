package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class PublicObjectionWindowProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess defaultProcess;
    private final LegislativeProcess reviewProcess;
    private final double objectionThreshold;
    private final double noise;
    private final boolean repealMode;

    public PublicObjectionWindowProcess(
            String name,
            LegislativeProcess defaultProcess,
            LegislativeProcess reviewProcess,
            double objectionThreshold,
            double noise,
            boolean repealMode
    ) {
        Values.requireRange("objectionThreshold", objectionThreshold, 0.0, 1.0);
        Values.requireRange("noise", noise, 0.0, 1.0);
        this.name = name;
        this.defaultProcess = defaultProcess;
        this.reviewProcess = reviewProcess;
        this.objectionThreshold = objectionThreshold;
        this.noise = noise;
        this.repealMode = repealMode;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double objectionScore = objectionScore(bill, context);
        boolean objectionTriggered = objectionScore >= objectionThreshold;
        if (!objectionTriggered) {
            return defaultProcess.consider(bill, context);
        }

        if (!repealMode) {
            return reviewProcess.consider(bill, context)
                    .withSignals(OutcomeSignals.objectionWindow(false));
        }

        BillOutcome defaultOutcome = defaultProcess.consider(bill, context);
        if (!defaultOutcome.enacted()) {
            return defaultOutcome.withSignals(OutcomeSignals.objectionWindow(false));
        }

        BillOutcome reviewOutcome = reviewProcess.consider(defaultOutcome.bill(), context);
        boolean reversed = !reviewOutcome.enacted();
        if (!reversed) {
            return defaultOutcome.withSignals(OutcomeSignals.objectionWindow(false));
        }

        return new BillOutcome(
                defaultOutcome.bill(),
                defaultOutcome.statusQuoBefore(),
                defaultOutcome.statusQuoBefore(),
                false,
                defaultOutcome.agendaDisposition(),
                defaultOutcome.gateResults(),
                defaultOutcome.chamberResults(),
                defaultOutcome.presidentialAction(),
                defaultOutcome.challenged(),
                defaultOutcome.signals()
                        .plus(reviewOutcome.signals())
                        .plus(OutcomeSignals.objectionWindow(true)),
                "repealed after public objection window"
        );
    }

    private double objectionScore(Bill bill, VoteContext context) {
        double authenticObjection = (0.30 * (1.0 - bill.publicSupport()))
                + (0.22 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()))
                + (0.16 * bill.salience())
                + (0.22 * AffectedGroupScoring.minorityHarm(bill))
                + (0.14 * LobbyCaptureScoring.captureRisk(bill));
        double amplifiedObjection = (0.08 * Math.max(0.0, bill.lobbyPressure()))
                + (0.04 * bill.publicCampaignSpend());
        double randomNoise = context.random().nextGaussian() * noise;
        return Values.clamp(authenticObjection + amplifiedObjection + randomNoise, 0.0, 1.0);
    }
}
