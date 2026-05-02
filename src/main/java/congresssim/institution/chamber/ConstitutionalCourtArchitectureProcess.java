package congresssim.institution.chamber;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;

public final class ConstitutionalCourtArchitectureProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final int courtSize;
    private final double panelReviewShare;
    private final double invalidationThreshold;
    private final double appointmentInsulation;
    private final double emergencyDocketConstraint;
    private final double opinionTransparency;
    private final boolean supermajorityInvalidation;

    public ConstitutionalCourtArchitectureProcess(
            String name,
            LegislativeProcess innerProcess,
            int courtSize,
            double panelReviewShare,
            double invalidationThreshold,
            double appointmentInsulation,
            double emergencyDocketConstraint,
            double opinionTransparency,
            boolean supermajorityInvalidation
    ) {
        if (courtSize < 3) {
            throw new IllegalArgumentException("courtSize must be at least 3.");
        }
        Values.requireRange("panelReviewShare", panelReviewShare, 0.0, 1.0);
        Values.requireRange("invalidationThreshold", invalidationThreshold, 0.0, 1.0);
        Values.requireRange("appointmentInsulation", appointmentInsulation, 0.0, 1.0);
        Values.requireRange("emergencyDocketConstraint", emergencyDocketConstraint, 0.0, 1.0);
        Values.requireRange("opinionTransparency", opinionTransparency, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.courtSize = courtSize;
        this.panelReviewShare = panelReviewShare;
        this.invalidationThreshold = invalidationThreshold;
        this.appointmentInsulation = appointmentInsulation;
        this.emergencyDocketConstraint = emergencyDocketConstraint;
        this.opinionTransparency = opinionTransparency;
        this.supermajorityInvalidation = supermajorityInvalidation;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        BillOutcome outcome = innerProcess.consider(bill, context);
        if (!outcome.enacted()) {
            return outcome.withSignals(OutcomeSignals.diagnostics(baseDiagnostics(bill, context, 0.0, false, false)));
        }

        double reviewRisk = reviewRisk(outcome.bill(), context);
        double shadowUse = shadowDocketUse(outcome.bill(), reviewRisk);
        double effectiveThreshold = Values.clamp(
                invalidationThreshold
                        + (supermajorityInvalidation ? 0.08 : 0.0)
                        + (0.08 * appointmentInsulation)
                        - (0.05 * shadowUse),
                0.0,
                1.0
        );
        double panelNoise = ((deterministic(outcome.bill(), "panel") - 0.5) * 0.10) * panelReviewShare;
        double reviewScore = Values.clamp(reviewRisk + panelNoise + (0.04 * (1.0 - opinionTransparency)), 0.0, 1.0);
        boolean invalidated = reviewScore >= effectiveThreshold;
        OutcomeSignals diagnostics = OutcomeSignals.diagnostics(baseDiagnostics(
                outcome.bill(),
                context,
                shadowUse,
                invalidated,
                reviewRisk >= 0.42
        ));
        if (!invalidated) {
            return outcome.withSignals(diagnostics.plus(OutcomeSignals.lawReview(
                    false,
                    true,
                    outcome.bill().publicBenefit(),
                    outcome.averageYayShare() < 0.50 ? 1.0 : 0.0,
                    1.0 + shadowUse
            )));
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
                outcome.signals().plus(diagnostics).plus(OutcomeSignals.lawReview(
                        true,
                        false,
                        outcome.bill().publicBenefit(),
                        outcome.averageYayShare() < 0.50 ? 1.0 : 0.0,
                        1.0 + shadowUse
                )),
                "constitutional court architecture invalidated enactment"
        );
    }

    private Map<String, Double> baseDiagnostics(
            Bill bill,
            VoteContext context,
            double shadowUse,
            boolean invalidated,
            boolean reviewed
    ) {
        double independence = Values.clamp(
                (0.44 * appointmentInsulation)
                        + (0.22 * opinionTransparency)
                        + (0.18 * (1.0 - panelReviewShare))
                        + (0.16 * Math.min(1.0, courtSize / 15.0)),
                0.0,
                1.0
        );
        double constraint = Values.clamp(
                (0.40 * emergencyDocketConstraint)
                        + (0.28 * opinionTransparency)
                        + (0.20 * (supermajorityInvalidation ? 1.0 : 0.0))
                        + (0.12 * appointmentInsulation),
                0.0,
                1.0
        );
        return Map.of(
                "courtIndependenceScore", independence,
                "courtConstraintIndex", constraint,
                "shadowDocketUseRate", shadowUse,
                "emergencyOrderExpirationRate", Values.clamp(emergencyDocketConstraint * shadowUse, 0.0, 1.0),
                "signedOpinionDisclosureRate", reviewed ? opinionTransparency : 0.0,
                "constitutionalInvalidationRate", invalidated ? 1.0 : 0.0,
                "courtReviewPressure", reviewRisk(bill, context)
        );
    }

    private double reviewRisk(Bill bill, VoteContext context) {
        double rightsRisk = bill.concentratedHarm() * (1.0 - bill.affectedGroupSupport());
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double policyShock = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        return Values.clamp(
                (0.34 * rightsRisk)
                        + (0.20 * captureRisk)
                        + (0.18 * policyShock)
                        + (0.12 * bill.publicBenefitUncertainty())
                        + (0.10 * bill.salience())
                        + (0.06 * (1.0 - appointmentInsulation)),
                0.0,
                1.0
        );
    }

    private double shadowDocketUse(Bill bill, double reviewRisk) {
        if (bill.salience() < 0.56 && reviewRisk < 0.48) {
            return 0.0;
        }
        return Values.clamp(
                (1.0 - emergencyDocketConstraint)
                        * (0.42 * bill.salience() + 0.40 * reviewRisk + 0.18 * bill.publicBenefitUncertainty()),
                0.0,
                1.0
        );
    }

    private static double deterministic(Bill bill, String salt) {
        return Math.floorMod((salt + ":" + bill.id() + ":" + bill.issueDomain()).hashCode(), 1000) / 999.0;
    }
}
