package congresssim.institution.chamber;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.List;
import java.util.Map;

public final class DistrictPopulationProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final int samplesPerDistrict;
    private final double turnoutSkew;
    private final double affectedGroupWeight;
    private final double signalStrength;

    public DistrictPopulationProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            int samplesPerDistrict,
            double turnoutSkew,
            double affectedGroupWeight,
            double signalStrength
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (samplesPerDistrict < 1) {
            throw new IllegalArgumentException("samplesPerDistrict must be positive.");
        }
        Values.requireRange("turnoutSkew", turnoutSkew, 0.0, 1.0);
        Values.requireRange("affectedGroupWeight", affectedGroupWeight, 0.0, 1.0);
        Values.requireRange("signalStrength", signalStrength, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.samplesPerDistrict = samplesPerDistrict;
        this.turnoutSkew = turnoutSkew;
        this.affectedGroupWeight = affectedGroupWeight;
        this.signalStrength = signalStrength;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        PopulationEstimate estimate = estimate(bill, context);
        Bill revised = bill.withPublicWillSignal(
                blend(bill.publicSupport(), estimate.publicSupport(), signalStrength),
                blend(bill.affectedGroupSupport(), estimate.affectedGroupSupport(), signalStrength),
                Values.clamp(bill.salience() + (signalStrength * estimate.attention() * 0.16), 0.0, 1.0),
                Values.clamp(
                        (bill.publicBenefitUncertainty() * (1.0 - (0.34 * signalStrength)))
                                + (estimate.preferenceVariance() * 0.22),
                        0.0,
                        1.0
                )
        );
        return innerProcess.consider(revised, context)
                .withSignals(OutcomeSignals.publicWill(
                        Math.abs(revised.publicSupport() - bill.publicSupport())
                                + Math.abs(revised.affectedGroupSupport() - bill.affectedGroupSupport()),
                        estimate.publicSupport()
                ))
                .withSignals(OutcomeSignals.diagnostics(Map.of(
                        "districtPreferenceVariance", estimate.preferenceVariance(),
                        "turnoutSkewIndex", estimate.turnoutSkewIndex(),
                        "affectedGroupRepresentationGap", estimate.affectedGroupRepresentationGap(),
                        "constituentAttentionIndex", estimate.attention(),
                        "publicWillPolarization", estimate.polarization()
                )));
    }

    private PopulationEstimate estimate(Bill bill, VoteContext context) {
        double weightedSupport = 0.0;
        double weightSum = 0.0;
        double affectedSupport = 0.0;
        double affectedWeightSum = 0.0;
        double preferenceSum = 0.0;
        double preferenceSquareSum = 0.0;
        double turnoutWeightSum = 0.0;
        double rawWeightSum = 0.0;
        double polarizationSum = 0.0;
        int samples = 0;

        for (Legislator legislator : legislators) {
            double representedPopulation = legislator.representationProfile().populationRepresented();
            double districtWeight = representedPopulation > 0.000001
                    ? representedPopulation
                    : 1.0 / legislators.size();
            for (int sample = 0; sample < samplesPerDistrict; sample++) {
                double preference = samplePreference(legislator, bill, sample);
                double support = constituentSupport(preference, legislator, bill, context);
                double attention = Values.clamp(
                        (0.30 + (0.70 * legislator.districtIntensity()))
                                * (0.55 + (0.45 * bill.salience()))
                                * (1.0 + turnoutSkew * Math.abs(preference)),
                        0.0,
                        2.0
                );
                double sampleWeight = districtWeight * attention / samplesPerDistrict;
                weightedSupport += support * sampleWeight;
                weightSum += sampleWeight;
                rawWeightSum += districtWeight / samplesPerDistrict;
                turnoutWeightSum += sampleWeight;
                preferenceSum += preference * sampleWeight;
                preferenceSquareSum += preference * preference * sampleWeight;
                polarizationSum += Math.abs(preference - bill.ideologyPosition()) * sampleWeight / 2.0;

                double affectedWeight = sampleWeight
                        * (0.20 + (affectedGroupWeight * legislator.affectedGroupSensitivity()))
                        * (0.35 + (0.65 * bill.concentratedHarm()));
                affectedSupport += support * affectedWeight;
                affectedWeightSum += affectedWeight;
                samples++;
            }
        }

        double publicSupport = weightSum == 0.0 ? bill.publicSupport() : weightedSupport / weightSum;
        double affected = affectedWeightSum == 0.0 ? bill.affectedGroupSupport() : affectedSupport / affectedWeightSum;
        double meanPreference = weightSum == 0.0 ? 0.0 : preferenceSum / weightSum;
        double variance = weightSum == 0.0
                ? 0.0
                : Values.clamp((preferenceSquareSum / weightSum) - (meanPreference * meanPreference), 0.0, 1.0);
        double expectedAffectedShare = Values.clamp(bill.concentratedHarm() * affectedGroupWeight, 0.0, 1.0);
        double representedAffectedShare = weightSum == 0.0 ? 0.0 : affectedWeightSum / Math.max(weightSum, 0.000001);
        return new PopulationEstimate(
                publicSupport,
                affected,
                variance,
                Values.clamp(Math.abs((turnoutWeightSum / Math.max(rawWeightSum, 0.000001)) - 1.0), 0.0, 1.0),
                Values.clamp(Math.abs(expectedAffectedShare - representedAffectedShare), 0.0, 1.0),
                Values.clamp(weightSum / Math.max(0.000001, samples * 0.01), 0.0, 1.0),
                weightSum == 0.0 ? 0.0 : Values.clamp(polarizationSum / weightSum, 0.0, 1.0)
        );
    }

    private static double samplePreference(Legislator legislator, Bill bill, int sample) {
        double offset = ((sample % 5) - 2) * 0.08;
        double issueTilt = Math.floorMod((legislator.id() + ":" + bill.issueDomain() + ":" + sample).hashCode(), 1000) / 999.0;
        double issueOffset = (issueTilt - 0.5) * 0.20;
        return Values.clamp(legislator.districtPreference() + offset + issueOffset, -1.0, 1.0);
    }

    private static double constituentSupport(
            double preference,
            Legislator legislator,
            Bill bill,
            VoteContext context
    ) {
        double proposedFit = 1.0 - Math.abs(preference - bill.ideologyPosition()) / 2.0;
        double statusQuoFit = 1.0 - Math.abs(preference - context.currentPolicyPosition()) / 2.0;
        double policyGain = proposedFit - statusQuoFit;
        double benefitPull = bill.publicBenefit() - 0.50;
        double affectedPenalty = bill.concentratedHarm() * (1.0 - bill.affectedGroupSupport())
                * legislator.affectedGroupSensitivity();
        double capturePenalty = Math.max(0.0, bill.lobbyPressure()) * Math.max(0.0, bill.privateGain() - bill.publicBenefit());
        return Values.clamp(
                0.50 + (0.66 * policyGain) + (0.34 * benefitPull) - (0.24 * affectedPenalty) - (0.20 * capturePenalty),
                0.0,
                1.0
        );
    }

    private static double blend(double original, double estimate, double strength) {
        return Values.clamp(original + (strength * (estimate - original)), 0.0, 1.0);
    }

    private record PopulationEstimate(
            double publicSupport,
            double affectedGroupSupport,
            double preferenceVariance,
            double turnoutSkewIndex,
            double affectedGroupRepresentationGap,
            double attention,
            double polarization
    ) {
    }
}
