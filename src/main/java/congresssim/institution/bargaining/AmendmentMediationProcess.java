package congresssim.institution.bargaining;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class AmendmentMediationProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final double amendmentThreshold;
    private final double amendmentRate;
    private final double medianWeight;
    private final double statusQuoWeight;
    private final double proposerWeight;

    public AmendmentMediationProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            double amendmentThreshold,
            double amendmentRate,
            double medianWeight,
            double statusQuoWeight,
            double proposerWeight
    ) {
        Values.requireRange("amendmentThreshold", amendmentThreshold, 0.0, 1.0);
        Values.requireRange("amendmentRate", amendmentRate, 0.0, 1.0);
        Values.requireRange("medianWeight", medianWeight, 0.0, 1.0);
        Values.requireRange("statusQuoWeight", statusQuoWeight, 0.0, 1.0);
        Values.requireRange("proposerWeight", proposerWeight, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.amendmentThreshold = amendmentThreshold;
        this.amendmentRate = amendmentRate;
        this.medianWeight = medianWeight;
        this.statusQuoWeight = statusQuoWeight;
        this.proposerWeight = proposerWeight;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double need = amendmentNeed(bill, context);
        if (need < amendmentThreshold) {
            return innerProcess.consider(bill, context);
        }
        Bill amendedBill = mediate(bill, context, need);
        return innerProcess.consider(amendedBill, context);
    }

    private Bill mediate(Bill bill, VoteContext context, double need) {
        double target = targetPosition(bill, context);
        double movementRate = amendmentRate * Values.clamp(need, 0.0, 1.0);
        double revisedPosition = Values.clamp(
                bill.ideologyPosition() + (movementRate * (target - bill.ideologyPosition())),
                -1.0,
                1.0
        );
        double movement = Math.abs(revisedPosition - bill.ideologyPosition());
        double capturePenalty = LobbyCaptureScoring.captureRisk(bill) * 0.10;
        double supportGain = movement * (0.24 + (0.20 * bill.publicBenefit())) - capturePenalty;
        double benefitGain = movement * 0.10 * (1.0 - Math.max(0.0, bill.lobbyPressure()));
        Bill amended = bill.withAmendment(
                revisedPosition,
                Values.clamp(bill.publicSupport() + supportGain, 0.0, 1.0),
                Values.clamp(bill.publicBenefit() + benefitGain, 0.0, 1.0)
        );
        if (bill.concentratedHarm() < 0.42 || bill.affectedGroupSupport() >= 0.50) {
            return amended;
        }
        double harmReduction = Values.clamp(0.24 + (0.32 * movementRate), 0.0, 0.62);
        double revisedHarm = Values.clamp(amended.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0);
        double revisedAffectedSupport = Values.clamp(
                amended.affectedGroupSupport() + ((amended.concentratedHarm() - revisedHarm) * 0.70),
                0.0,
                1.0
        );
        double revisedBenefit = Values.clamp(
                amended.publicBenefit() - (amended.compensationCost() * 0.25),
                0.0,
                1.0
        );
        return amended.withCompensation(revisedBenefit, revisedAffectedSupport, revisedHarm);
    }

    private double targetPosition(Bill bill, VoteContext context) {
        double median = chamberMedian();
        double totalWeight = medianWeight + statusQuoWeight + proposerWeight;
        if (totalWeight <= 0.000001) {
            return median;
        }
        return ((medianWeight * median)
                + (statusQuoWeight * context.currentPolicyPosition())
                + (proposerWeight * bill.proposerIdeology())) / totalWeight;
    }

    private double amendmentNeed(Bill bill, VoteContext context) {
        double lowSupport = Math.max(0.0, 0.55 - bill.publicSupport()) / 0.55;
        double policyShift = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double proposerDistance = Math.abs(bill.ideologyPosition() - bill.proposerIdeology()) / 2.0;
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double harmRisk = AffectedGroupScoring.minorityHarm(bill);
        return Values.clamp(
                (0.34 * lowSupport)
                        + (0.28 * policyShift)
                        + (0.14 * (1.0 - proposerDistance))
                        + (0.16 * captureRisk)
                        + (0.08 * harmRisk),
                0.0,
                1.0
        );
    }

    private double chamberMedian() {
        List<Double> positions = new ArrayList<>();
        for (Legislator legislator : legislators) {
            positions.add(legislator.ideology());
        }
        Collections.sort(positions);
        int midpoint = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(midpoint);
        }
        return (positions.get(midpoint - 1) + positions.get(midpoint)) / 2.0;
    }
}
