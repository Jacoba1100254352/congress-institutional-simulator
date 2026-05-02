package congresssim.institution.review;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;

public final class ExAnteReviewProcess implements LegislativeProcess {
    private final String name;
    private final ExAnteReviewMode mode;
    private final IndependentInstitutionBundle bundle;
    private final double highRiskThreshold;
    private final double overrideThreshold;
    private final LegislativeProcess innerProcess;

    public ExAnteReviewProcess(
            String name,
            ExAnteReviewMode mode,
            IndependentInstitutionBundle bundle,
            double highRiskThreshold,
            double overrideThreshold,
            LegislativeProcess innerProcess
    ) {
        Values.requireRange("highRiskThreshold", highRiskThreshold, 0.0, 1.0);
        Values.requireRange("overrideThreshold", overrideThreshold, 0.0, 1.0);
        this.name = name;
        this.mode = mode == null ? ExAnteReviewMode.ADVISORY_OPINION : mode;
        this.bundle = bundle == null ? IndependentInstitutionBundle.advisoryFiscalLegal() : bundle;
        this.highRiskThreshold = highRiskThreshold;
        this.overrideThreshold = overrideThreshold;
        this.innerProcess = innerProcess;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double legalRisk = legalRisk(bill);
        boolean reviewed = reviewed(bill, legalRisk);
        double overrideSupport = overrideSupport(bill);
        boolean reviewBlocks = reviewed && blocks(legalRisk, overrideSupport);
        if (reviewBlocks) {
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    "ex ante review withheld clearance"
            ).withSignals(reviewSignals(bill, reviewed, legalRisk, overrideSupport, true));
        }

        Bill reviewedBill = reviewed ? improveDrafting(bill, legalRisk) : bill;
        return innerProcess.consider(reviewedBill, context)
                .withSignals(reviewSignals(bill, reviewed, legalRisk, overrideSupport, false));
    }

    private boolean reviewed(Bill bill, double legalRisk) {
        return switch (mode) {
            case OPTIONAL_REFERRAL -> bill.salience() > 0.62 || bill.concentratedHarm() > 0.48;
            case MANDATORY_HIGH_RISK -> legalRisk >= highRiskThreshold;
            case ADVISORY_OPINION -> bill.publicBenefitUncertainty() > 0.34 || bill.salience() > 0.45;
            case SUSPENSIVE_OBJECTION -> legalRisk >= highRiskThreshold * 0.82;
            case MANDATORY_CLEARANCE, QUALIFIED_OVERRIDE -> legalRisk >= highRiskThreshold * 0.70;
            case DEADLINE_LIMITED -> bill.salience() > 0.50 || legalRisk > 0.42;
        };
    }

    private boolean blocks(double legalRisk, double overrideSupport) {
        return switch (mode) {
            case MANDATORY_CLEARANCE -> legalRisk > highRiskThreshold
                    && overrideSupport < overrideThreshold + 0.10;
            case QUALIFIED_OVERRIDE -> legalRisk > highRiskThreshold
                    && overrideSupport < overrideThreshold;
            case SUSPENSIVE_OBJECTION -> legalRisk > highRiskThreshold + 0.12
                    && overrideSupport < overrideThreshold - 0.08;
            default -> false;
        };
    }

    private Bill improveDrafting(Bill bill, double legalRisk) {
        double informationGain = bundle.compulsoryInformationAccess() * (1.0 - bundle.quietCaptureRisk());
        double revisedUncertainty = Values.clamp(
                bill.publicBenefitUncertainty() * (1.0 - (0.38 * informationGain)),
                0.0,
                1.0
        );
        double draftingGain = (0.030 * bundle.staffingAutonomy())
                + (0.020 * bundle.publicationTimetable())
                - (0.030 * legalRisk);
        return bill.withAmendment(
                bill.ideologyPosition(),
                bill.publicSupport(),
                Values.clamp(bill.publicBenefit() + draftingGain, 0.0, 1.0)
        ).withPublicBenefitUncertainty(revisedUncertainty);
    }

    private OutcomeSignals reviewSignals(
            Bill bill,
            boolean reviewed,
            double legalRisk,
            double overrideSupport,
            boolean blocked
    ) {
        double informationFulfillment = bundle.compulsoryInformationAccess() * bundle.staffingAutonomy();
        double forecastError = Values.clamp(
                bill.publicBenefitUncertainty() * (1.0 - informationFulfillment)
                        + (0.20 * bundle.quietCaptureRisk()),
                0.0,
                1.0
        );
        double delay = reviewed ? switch (mode) {
            case SUSPENSIVE_OBJECTION -> 0.34;
            case MANDATORY_CLEARANCE, QUALIFIED_OVERRIDE -> 0.28;
            case DEADLINE_LIMITED -> 0.12;
            default -> 0.18;
        } : 0.0;
        double override = reviewed && !blocked && legalRisk >= highRiskThreshold && overrideSupport >= overrideThreshold ? 1.0 : 0.0;
        return OutcomeSignals.diagnostics(Map.ofEntries(
                Map.entry("exAnteReviewRate", reviewed ? 1.0 : 0.0),
                Map.entry("reviewDelay", Values.clamp(delay * (1.0 - (0.35 * bundle.publicationTimetable())), 0.0, 1.0)),
                Map.entry("exPostInvalidationRate", Values.clamp(legalRisk * (1.0 - (reviewed ? bundle.insulationScore() : 0.12)), 0.0, 1.0)),
                Map.entry("draftingErrorRate", Values.clamp(bill.publicBenefitUncertainty() * (1.0 - (reviewed ? bundle.staffingAutonomy() : 0.15)), 0.0, 1.0)),
                Map.entry("referralPartisanSkew", Values.clamp(Math.abs(bill.proposerIdeology()) * (mode == ExAnteReviewMode.OPTIONAL_REFERRAL ? 0.70 : 0.24), 0.0, 1.0)),
                Map.entry("forecastError", forecastError),
                Map.entry("publicationCompliance", Values.clamp(bundle.publicationTimetable(), 0.0, 1.0)),
                Map.entry("informationRequestFulfillment", Values.clamp(informationFulfillment, 0.0, 1.0)),
                Map.entry("institutionOverrideFrequency", override),
                Map.entry("oppositionTrustProxy", Values.clamp(bundle.insulationScore() * (1.0 - (0.45 * bundle.quietCaptureRisk())), 0.0, 1.0)),
                Map.entry("independenceInsulationScore", bundle.insulationScore()),
                Map.entry("quietCaptureRisk", bundle.quietCaptureRisk())
        ));
    }

    private double legalRisk(Bill bill) {
        return Values.clamp(
                (0.28 * bill.concentratedHarm())
                        + (0.18 * (1.0 - bill.affectedGroupSupport()))
                        + (0.18 * bill.publicBenefitUncertainty())
                        + (0.14 * Math.abs(bill.ideologyPosition()))
                        + (0.12 * Math.max(0.0, bill.lobbyPressure()))
                        + (0.10 * (bill.antiLobbyingReform() ? 1.0 : 0.0)),
                0.0,
                1.0
        );
    }

    private static double overrideSupport(Bill bill) {
        return Values.clamp(
                (0.52 * bill.publicSupport())
                        + (0.20 * bill.publicBenefit())
                        + (0.18 * Math.clamp(bill.cosponsorCount() / 10.0, 0.0, 1.0))
                        + (0.10 * bill.salience()),
                0.0,
                1.0
        );
    }
}
