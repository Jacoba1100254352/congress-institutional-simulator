package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class DemocraticDeteriorationProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double electoralPressureWeight;
    private final double mediaAmplificationWeight;
    private final double courtShockWeight;
    private final double lobbyEscalationWeight;
    private final double normRecoveryRate;
    private double institutionalStress;

    public DemocraticDeteriorationProcess(
            String name,
            LegislativeProcess innerProcess,
            double initialStress,
            double electoralPressureWeight,
            double mediaAmplificationWeight,
            double courtShockWeight,
            double lobbyEscalationWeight,
            double normRecoveryRate
    ) {
        Values.requireRange("initialStress", initialStress, 0.0, 1.0);
        Values.requireRange("electoralPressureWeight", electoralPressureWeight, 0.0, 1.0);
        Values.requireRange("mediaAmplificationWeight", mediaAmplificationWeight, 0.0, 1.0);
        Values.requireRange("courtShockWeight", courtShockWeight, 0.0, 1.0);
        Values.requireRange("lobbyEscalationWeight", lobbyEscalationWeight, 0.0, 1.0);
        Values.requireRange("normRecoveryRate", normRecoveryRate, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.institutionalStress = initialStress;
        this.electoralPressureWeight = electoralPressureWeight;
        this.mediaAmplificationWeight = mediaAmplificationWeight;
        this.courtShockWeight = courtShockWeight;
        this.lobbyEscalationWeight = lobbyEscalationWeight;
        this.normRecoveryRate = normRecoveryRate;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill stressed = applyDeterioration(bill, context);
        if (courtOrDelayShock(stressed)) {
            updateStress(stressed, false, 0.0, true);
            return BillOutcome.accessDenied(stressed, context.currentPolicyPosition(), "democratic deterioration shock delay");
        }
        BillOutcome outcome = innerProcess.consider(stressed, context);
        updateStress(stressed, outcome.enacted(), outcome.averageYayShare(), false);
        return outcome;
    }

    private Bill applyDeterioration(Bill bill, VoteContext context) {
        double polarizationDistance = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double mediaHeat = institutionalStress
                * mediaAmplificationWeight
                * (0.35 + (0.45 * bill.salience()) + (0.20 * polarizationDistance));
        double electoralRetreat = institutionalStress
                * electoralPressureWeight
                * (0.20 + (0.50 * polarizationDistance))
                * (1.0 - bill.publicSupport());
        double lobbyEscalation = institutionalStress
                * lobbyEscalationWeight
                * (0.35 + (0.65 * Math.max(0.0, bill.privateGain() - bill.publicBenefit())));
        double revisedSupport = Values.clamp(
                bill.publicSupport() + (mediaHeat * 0.04) - electoralRetreat - (lobbyEscalation * 0.06),
                0.0,
                1.0
        );
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() - (institutionalStress * bill.publicBenefitUncertainty() * 0.08),
                0.0,
                1.0
        );
        double revisedLobbyPressure = Values.clamp(
                bill.lobbyPressure() + (lobbyEscalation * 0.20),
                -1.0,
                1.0
        );
        double revisedPrivateGain = Values.clamp(
                bill.privateGain() + (lobbyEscalation * 0.10),
                0.0,
                1.0
        );
        return bill.withLobbyActivity(
                revisedLobbyPressure,
                revisedSupport,
                revisedBenefit,
                revisedPrivateGain,
                lobbyEscalation,
                bill.antiLobbyingReform() ? lobbyEscalation * 0.50 : 0.0,
                lobbyEscalation * 0.35,
                lobbyEscalation * 0.18,
                lobbyEscalation * 0.16,
                mediaHeat * 0.20,
                institutionalStress * courtShockWeight * bill.publicBenefitUncertainty() * 0.18
        );
    }

    private boolean courtOrDelayShock(Bill bill) {
        double rightsLikeRisk = (0.55 * AffectedGroupScoring.minorityHarm(bill))
                + (0.25 * bill.publicBenefitUncertainty())
                + (0.20 * Math.max(0.0, bill.lobbyPressure()));
        double shockProbability = institutionalStress * courtShockWeight * rightsLikeRisk * 0.42;
        int bucket = Math.floorMod(("deterioration:" + bill.id() + ":" + bill.proposerId()).hashCode(), 1000);
        return (bucket / 999.0) < shockProbability;
    }

    private void updateStress(Bill bill, boolean enacted, double yayShare, boolean shockDelay) {
        double lowLegitimacyEnactment = enacted && (bill.publicSupport() < 0.54 || yayShare < 0.54) ? 1.0 : 0.0;
        double popularFrustration = !enacted && bill.publicSupport() > 0.62 ? 1.0 : 0.0;
        double capture = LobbyCaptureScoring.captureRisk(bill);
        double harm = AffectedGroupScoring.minorityHarm(bill);
        double shock = shockDelay ? 1.0 : 0.0;
        double pressure = (0.24 * lowLegitimacyEnactment)
                + (0.18 * popularFrustration)
                + (0.22 * capture)
                + (0.16 * harm)
                + (0.12 * bill.publicBenefitUncertainty())
                + (0.08 * shock);
        institutionalStress = Values.clamp(
                (institutionalStress * (1.0 - normRecoveryRate)) + pressure,
                0.0,
                1.0
        );
    }
}
