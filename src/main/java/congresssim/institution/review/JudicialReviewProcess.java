package congresssim.institution.review;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class JudicialReviewProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double reviewThreshold;
    private final double invalidationThreshold;
    private final double courtActivism;

    public JudicialReviewProcess(
            String name,
            LegislativeProcess innerProcess,
            double reviewThreshold,
            double invalidationThreshold,
            double courtActivism
    ) {
        Values.requireRange("reviewThreshold", reviewThreshold, 0.0, 1.0);
        Values.requireRange("invalidationThreshold", invalidationThreshold, 0.0, 1.0);
        Values.requireRange("courtActivism", courtActivism, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.reviewThreshold = reviewThreshold;
        this.invalidationThreshold = invalidationThreshold;
        this.courtActivism = courtActivism;
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

        double reviewRisk = reviewRisk(outcome.bill(), context);
        if (reviewRisk < reviewThreshold) {
            return outcome;
        }

        double invalidationRisk = Values.clamp(reviewRisk + deterministicCourtJitter(outcome.bill()), 0.0, 1.0);
        if (invalidationRisk < invalidationThreshold) {
            return outcome.withSignals(OutcomeSignals.lawReview(
                    false,
                    true,
                    outcome.bill().publicBenefit(),
                    lowSupportShare(outcome),
                    1.0
            ));
        }

        return new BillOutcome(
                outcome.bill(),
                outcome.statusQuoBefore(),
                outcome.statusQuoBefore(),
                false,
                outcome.agendaDisposition(),
                outcome.gateResults(),
                outcome.chamberResults(),
                outcome.presidentialAction(),
                outcome.challenged(),
                outcome.signals().plus(OutcomeSignals.lawReview(
                        true,
                        false,
                        outcome.bill().publicBenefit(),
                        lowSupportShare(outcome),
                        1.0
                )),
                "judicial review invalidated enactment"
        );
    }

    private double reviewRisk(Bill bill, VoteContext context) {
        double rightsLikeHarm = bill.concentratedHarm() * (1.0 - bill.affectedGroupSupport());
        double policyShock = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        return Values.clamp(
                (0.40 * rightsLikeHarm)
                        + (0.20 * policyShock)
                        + (0.16 * captureRisk)
                        + (0.12 * bill.publicBenefitUncertainty())
                        + (0.12 * bill.salience())
                        + (0.10 * courtActivism),
                0.0,
                1.0
        );
    }

    private static double lowSupportShare(BillOutcome outcome) {
        return outcome.averageYayShare() < 0.50 ? 1.0 : 0.0;
    }

    private double deterministicCourtJitter(Bill bill) {
        int bucket = Math.floorMod(("court:" + bill.id() + ":" + bill.issueDomain()).hashCode(), 1000);
        return ((bucket / 999.0) - 0.5) * 0.12 * courtActivism;
    }
}
