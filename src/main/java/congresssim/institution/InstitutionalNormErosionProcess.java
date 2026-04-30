package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class InstitutionalNormErosionProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double learningRate;
    private final double recoveryRate;
    private double contention;

    public InstitutionalNormErosionProcess(
            String name,
            LegislativeProcess innerProcess,
            double initialContention,
            double learningRate,
            double recoveryRate
    ) {
        Values.requireRange("initialContention", initialContention, 0.0, 1.0);
        Values.requireRange("learningRate", learningRate, 0.0, 1.0);
        Values.requireRange("recoveryRate", recoveryRate, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.contention = initialContention;
        this.learningRate = learningRate;
        this.recoveryRate = recoveryRate;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill revisedBill = erodeSignals(bill);
        if (strategicDelay(revisedBill)) {
            contention = Values.clamp(contention + (learningRate * 0.08), 0.0, 1.0);
            return BillOutcome.accessDenied(revisedBill, context.currentPolicyPosition(), "norm erosion procedural delay");
        }

        BillOutcome outcome = innerProcess.consider(revisedBill, context);
        updateContention(revisedBill, outcome);
        return outcome;
    }

    private Bill erodeSignals(Bill bill) {
        if (contention <= 0.000001) {
            return bill;
        }
        double supportLoss = contention * (0.05 + (0.04 * bill.salience()));
        double lobbyAmplification = contention * Math.max(0.0, bill.privateGain() - bill.publicBenefit()) * 0.16;
        double revisedSupport = Values.clamp(bill.publicSupport() - supportLoss, 0.0, 1.0);
        double revisedLobbyPressure = Values.clamp(bill.lobbyPressure() + lobbyAmplification, -1.0, 1.0);
        double revisedPrivateGain = Values.clamp(bill.privateGain() + (lobbyAmplification * 0.20), 0.0, 1.0);
        return bill.withLobbyActivity(
                revisedLobbyPressure,
                revisedSupport,
                bill.publicBenefit(),
                revisedPrivateGain,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0
        );
    }

    private boolean strategicDelay(Bill bill) {
        double delayRisk = contention
                * (0.20 + (0.35 * bill.publicBenefitUncertainty()) + (0.25 * bill.salience()))
                * (1.0 - bill.publicSupport());
        int bucket = Math.floorMod(("norm:" + bill.id() + ":" + bill.proposerId()).hashCode(), 1000);
        double draw = bucket / 999.0;
        return draw < delayRisk * 0.35;
    }

    private void updateContention(Bill bill, BillOutcome outcome) {
        double lowSupportEnactment = outcome.enacted() && outcome.averageYayShare() < 0.55 ? 1.0 : 0.0;
        double popularFailure = !outcome.enacted() && bill.publicSupport() >= 0.62 ? 1.0 : 0.0;
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double minorityHarm = AffectedGroupScoring.minorityHarm(bill);
        double legitimacySignal = (0.35 * bill.publicSupport())
                + (0.30 * bill.publicBenefit())
                + (0.20 * bill.affectedGroupSupport())
                + (0.15 * outcome.averageYayShare());
        double stress = (0.28 * lowSupportEnactment)
                + (0.22 * popularFailure)
                + (0.22 * captureRisk)
                + (0.18 * minorityHarm)
                + (0.10 * (1.0 - legitimacySignal));
        contention = Values.clamp((contention * (1.0 - recoveryRate)) + (learningRate * stress), 0.0, 1.0);
    }
}
