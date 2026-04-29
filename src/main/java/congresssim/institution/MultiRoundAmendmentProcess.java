package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class MultiRoundAmendmentProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final int maxRounds;
    private final double roundCost;
    private final double proposerConcessionLimit;
    private final double poisonPillProbability;

    public MultiRoundAmendmentProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            int maxRounds,
            double roundCost,
            double proposerConcessionLimit,
            double poisonPillProbability
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (maxRounds < 1) {
            throw new IllegalArgumentException("maxRounds must be positive.");
        }
        Values.requireRange("roundCost", roundCost, 0.0, 1.0);
        Values.requireRange("proposerConcessionLimit", proposerConcessionLimit, 0.0, 2.0);
        Values.requireRange("poisonPillProbability", poisonPillProbability, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.maxRounds = maxRounds;
        this.roundCost = roundCost;
        this.proposerConcessionLimit = proposerConcessionLimit;
        this.poisonPillProbability = poisonPillProbability;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill current = bill;
        for (int round = 0; round < maxRounds; round++) {
            double need = amendmentNeed(current, context);
            if (need < 0.18) {
                break;
            }
            double target = targetPosition(current, context, round);
            double step = Math.min(0.42, 0.18 + (need * 0.34));
            double revisedPosition = Values.clamp(
                    current.ideologyPosition() + (step * (target - current.ideologyPosition())),
                    -1.0,
                    1.0
            );
            if (Math.abs(revisedPosition - bill.proposerIdeology()) > proposerConcessionLimit) {
                break;
            }
            boolean poisonPill = context.random().nextDouble() < poisonPillProbability * need;
            current = reviseBill(current, revisedPosition, round, poisonPill);
        }
        return innerProcess.consider(current, context);
    }

    private Bill reviseBill(Bill bill, double revisedPosition, int round, boolean poisonPill) {
        double movement = Math.abs(revisedPosition - bill.ideologyPosition());
        double supportGain = poisonPill ? -0.10 - (0.05 * round) : movement * (0.26 + (0.18 * bill.publicBenefit()));
        double benefitGain = poisonPill ? -roundCost : (movement * 0.12) - roundCost;
        Bill revised = bill.withAmendment(
                revisedPosition,
                Values.clamp(bill.publicSupport() + supportGain, 0.0, 1.0),
                Values.clamp(bill.publicBenefit() + benefitGain, 0.0, 1.0)
        );
        if (poisonPill) {
            return revised.withAffectedGroup(
                    revised.affectedGroup(),
                    Values.clamp(revised.affectedGroupSupport() - 0.08, 0.0, 1.0),
                    Values.clamp(revised.concentratedHarm() + 0.08, 0.0, 1.0),
                    revised.compensationCost()
            );
        }
        if (revised.concentratedHarm() < 0.38) {
            return revised;
        }
        double harmReduction = Values.clamp(0.16 + movement + (bill.compensationCost() * 0.30), 0.0, 0.70);
        double revisedHarm = Values.clamp(revised.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0);
        double affectedSupportGain = (revised.concentratedHarm() - revisedHarm) * 0.72;
        double compensationCost = revised.compensationCost() * (0.18 + (0.10 * round));
        return revised.withCompensation(
                Values.clamp(revised.publicBenefit() - compensationCost, 0.0, 1.0),
                Values.clamp(revised.affectedGroupSupport() + affectedSupportGain, 0.0, 1.0),
                revisedHarm
        );
    }

    private double targetPosition(Bill bill, VoteContext context, int round) {
        double chamberMedian = chamberMedian();
        double districtMedian = districtMedian();
        double harmPull = bill.concentratedHarm() > 0.45 ? context.currentPolicyPosition() : chamberMedian;
        double roundWeight = Math.min(0.28, round * 0.07);
        return ((0.42 - roundWeight) * chamberMedian)
                + (0.22 * districtMedian)
                + (0.22 * context.currentPolicyPosition())
                + (0.14 * harmPull)
                + (roundWeight * bill.proposerIdeology());
    }

    private static double amendmentNeed(Bill bill, VoteContext context) {
        double lowSupport = Math.max(0.0, 0.58 - bill.publicSupport()) / 0.58;
        double policyShift = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double uncertainty = bill.publicBenefitUncertainty();
        double harmRisk = AffectedGroupScoring.minorityHarm(bill);
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        return Values.clamp(
                (0.28 * lowSupport)
                        + (0.22 * policyShift)
                        + (0.18 * uncertainty)
                        + (0.20 * harmRisk)
                        + (0.12 * captureRisk),
                0.0,
                1.0
        );
    }

    private double chamberMedian() {
        List<Double> positions = legislators.stream().map(Legislator::ideology).sorted().toList();
        return median(positions);
    }

    private double districtMedian() {
        List<Double> positions = new ArrayList<>();
        for (Legislator legislator : legislators) {
            positions.add(legislator.districtPreference());
        }
        Collections.sort(positions);
        return median(positions);
    }

    private static double median(List<Double> sortedPositions) {
        int midpoint = sortedPositions.size() / 2;
        if (sortedPositions.size() % 2 == 1) {
            return sortedPositions.get(midpoint);
        }
        return (sortedPositions.get(midpoint - 1) + sortedPositions.get(midpoint)) / 2.0;
    }
}
