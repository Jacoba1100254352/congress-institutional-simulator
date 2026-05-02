package congresssim.institution.accountability;

import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.List;

public final class LawRegistryProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final int reviewDelayRounds;
    private final double provisionalRiskThreshold;
    private final double renewalThreshold;
    private final double rollbackRate;
    private final List<LawRecord> laws = new ArrayList<>();
    private int round;

    public LawRegistryProcess(
            String name,
            LegislativeProcess innerProcess,
            int reviewDelayRounds,
            double provisionalRiskThreshold,
            double renewalThreshold,
            double rollbackRate
    ) {
        if (reviewDelayRounds < 1) {
            throw new IllegalArgumentException("reviewDelayRounds must be positive.");
        }
        Values.requireRange("provisionalRiskThreshold", provisionalRiskThreshold, 0.0, 1.0);
        Values.requireRange("renewalThreshold", renewalThreshold, 0.0, 1.0);
        Values.requireRange("rollbackRate", rollbackRate, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.reviewDelayRounds = reviewDelayRounds;
        this.provisionalRiskThreshold = provisionalRiskThreshold;
        this.renewalThreshold = renewalThreshold;
        this.rollbackRate = rollbackRate;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        round++;
        BillOutcome outcome = innerProcess.consider(bill, context);
        if (outcome.enacted() && AdaptiveTrackProcess.riskScore(outcome.bill(), context) >= provisionalRiskThreshold) {
            laws.add(new LawRecord(
                    outcome.bill(),
                    outcome.statusQuoBefore(),
                    outcome.statusQuoAfter(),
                    round,
                    round + reviewDelayRounds,
                    true
            ));
        }
        return reviewDueLaws(outcome, context);
    }

    private BillOutcome reviewDueLaws(BillOutcome outcome, VoteContext context) {
        OutcomeSignals signals = OutcomeSignals.none();
        double adjustedStatusQuo = outcome.statusQuoAfter();
        boolean changedStatusQuo = false;
        List<LawRecord> updated = new ArrayList<>(laws.size());

        for (LawRecord law : laws) {
            if (!law.active() || law.reviewDueRound() > round) {
                updated.add(law);
                continue;
            }

            double reviewScore = reviewScore(law.sourceBill(), context);
            boolean renewed = reviewScore >= renewalThreshold;
            boolean reversed = !renewed;
            if (reversed) {
                adjustedStatusQuo = rollback(adjustedStatusQuo, law);
                changedStatusQuo = true;
                updated.add(law.deactivate());
            } else {
                updated.add(new LawRecord(
                        law.sourceBill(),
                        law.previousStatusQuo(),
                        law.enactedPosition(),
                        law.enactedRound(),
                        round + reviewDelayRounds,
                        true
                ));
            }
            signals = signals.plus(OutcomeSignals.lawReview(
                    reversed,
                    renewed,
                    activeLawWelfare(updated),
                    lowSupportActiveLawShare(updated),
                    round - law.enactedRound()
            ));
        }

        laws.clear();
        laws.addAll(updated);
        if (!changedStatusQuo) {
            return outcome.withSignals(signals);
        }
        return new BillOutcome(
                outcome.bill(),
                outcome.statusQuoBefore(),
                Values.clamp(adjustedStatusQuo, -1.0, 1.0),
                outcome.enacted(),
                outcome.agendaDisposition(),
                outcome.gateResults(),
                outcome.chamberResults(),
                outcome.presidentialAction(),
                outcome.challenged(),
                outcome.signals().plus(signals),
                "law-registry review adjusted active law; " + outcome.finalReason()
        );
    }

    private double rollback(double currentStatusQuo, LawRecord law) {
        double enactedShift = law.enactedPosition() - law.previousStatusQuo();
        return currentStatusQuo - (rollbackRate * enactedShift);
    }

    private static double reviewScore(Bill bill, VoteContext context) {
        double risk = AdaptiveTrackProcess.riskScore(bill, context);
        double harmPenalty = AffectedGroupScoring.minorityHarm(bill) * 0.18;
        return Values.clamp(
                (0.42 * bill.publicBenefit())
                        + (0.30 * bill.publicSupport())
                        + (0.16 * bill.affectedGroupSupport())
                        + (0.12 * (1.0 - risk))
                        - harmPenalty,
                0.0,
                1.0
        );
    }

    private static double activeLawWelfare(List<LawRecord> records) {
        double sum = 0.0;
        int count = 0;
        for (LawRecord law : records) {
            if (!law.active()) {
                continue;
            }
            sum += law.sourceBill().publicBenefit();
            count++;
        }
        return count == 0 ? 0.0 : sum / count;
    }

    private static double lowSupportActiveLawShare(List<LawRecord> records) {
        int lowSupport = 0;
        int count = 0;
        for (LawRecord law : records) {
            if (!law.active()) {
                continue;
            }
            count++;
            if (law.sourceBill().publicSupport() < 0.50) {
                lowSupport++;
            }
        }
        return count == 0 ? 0.0 : (double) lowSupport / count;
    }
}
