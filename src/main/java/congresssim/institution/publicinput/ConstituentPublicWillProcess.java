package congresssim.institution.publicinput;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.List;

public final class ConstituentPublicWillProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final double updateStrength;
    private final double salienceAmplification;

    public ConstituentPublicWillProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            double updateStrength,
            double salienceAmplification
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        Values.requireRange("updateStrength", updateStrength, 0.0, 1.0);
        Values.requireRange("salienceAmplification", salienceAmplification, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.updateStrength = updateStrength;
        this.salienceAmplification = salienceAmplification;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        PublicWillEstimate estimate = estimatePublicWill(bill, context);
        double revisedSupport = blend(bill.publicSupport(), estimate.publicSupport(), updateStrength);
        double revisedAffectedSupport = blend(bill.affectedGroupSupport(), estimate.affectedGroupSupport(), updateStrength);
        double revisedSalience = Values.clamp(
                bill.salience() + (salienceAmplification * estimate.averageIntensity() * Math.abs(revisedSupport - bill.publicSupport())),
                0.0,
                1.0
        );
        double revisedUncertainty = Values.clamp(
                (bill.publicBenefitUncertainty() * (1.0 - (0.45 * updateStrength)))
                        + (estimate.disagreement() * 0.35),
                0.0,
                1.0
        );
        Bill revised = bill.withPublicWillSignal(
                revisedSupport,
                revisedAffectedSupport,
                revisedSalience,
                revisedUncertainty
        );
        double signalMovement = Math.abs(revisedSupport - bill.publicSupport())
                + Math.abs(revisedAffectedSupport - bill.affectedGroupSupport());
        return innerProcess.consider(revised, context)
                .withSignals(OutcomeSignals.publicWill(signalMovement, estimate.publicSupport()));
    }

    private PublicWillEstimate estimatePublicWill(Bill bill, VoteContext context) {
        double weightedSupport = 0.0;
        double weightSum = 0.0;
        double affectedSupport = 0.0;
        double affectedWeight = 0.0;
        double disagreement = 0.0;
        for (Legislator legislator : legislators) {
            double intensity = 0.35 + (0.65 * legislator.districtIntensity());
            double districtSupport = districtSupport(legislator, bill, context);
            weightedSupport += districtSupport * intensity;
            weightSum += intensity;
            disagreement += Math.abs(districtSupport - bill.publicSupport()) * intensity;

            double affectedWeightForLegislator = legislator.affectedGroupSensitivity()
                    * (0.35 + (0.65 * bill.concentratedHarm()));
            affectedSupport += districtSupport * affectedWeightForLegislator;
            affectedWeight += affectedWeightForLegislator;
        }
        double publicSupport = weightSum == 0.0 ? bill.publicSupport() : weightedSupport / weightSum;
        double affectedGroupSupport = affectedWeight == 0.0 ? bill.affectedGroupSupport() : affectedSupport / affectedWeight;
        double normalizedDisagreement = weightSum == 0.0 ? 0.0 : disagreement / weightSum;
        return new PublicWillEstimate(publicSupport, affectedGroupSupport, normalizedDisagreement, weightSum / legislators.size());
    }

    private static double districtSupport(Legislator legislator, Bill bill, VoteContext context) {
        double spatialFit = 1.0 - (Math.abs(bill.ideologyPosition() - legislator.districtPreference()) / 2.0);
        double statusQuoFit = 1.0 - (Math.abs(context.currentPolicyPosition() - legislator.districtPreference()) / 2.0);
        double changeBenefit = spatialFit - statusQuoFit;
        double benefitPull = bill.publicBenefit() - 0.5;
        double harmPenalty = AffectedGroupScoring.minorityHarm(bill) * legislator.affectedGroupSensitivity();
        double lobbySuspicion = Math.max(0.0, bill.lobbyPressure()) * (1.0 - bill.publicBenefit());
        double score = 0.50
                + (0.62 * changeBenefit)
                + (0.34 * benefitPull)
                - (0.28 * harmPenalty)
                - (0.18 * lobbySuspicion);
        return Values.clamp(score, 0.0, 1.0);
    }

    private static double blend(double original, double estimate, double strength) {
        return Values.clamp(original + (strength * (estimate - original)), 0.0, 1.0);
    }

    private record PublicWillEstimate(
            double publicSupport,
            double affectedGroupSupport,
            double disagreement,
            double averageIntensity
    ) {
    }
}
