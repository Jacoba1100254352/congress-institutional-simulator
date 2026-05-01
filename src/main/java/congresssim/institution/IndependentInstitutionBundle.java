package congresssim.institution;

import congresssim.util.Values;

import java.util.Set;

public record IndependentInstitutionBundle(
        Set<IndependentInstitutionType> institutionTypes,
        double appointmentInsulation,
        double removalForCauseProtection,
        double budgetAutonomy,
        double staffingAutonomy,
        double compulsoryInformationAccess,
        double publicationTimetable,
        double enforcementReferralPower,
        double judicialReviewExposure
) {
    public IndependentInstitutionBundle {
        institutionTypes = institutionTypes == null || institutionTypes.isEmpty()
                ? Set.of(IndependentInstitutionType.COST_ESTIMATOR)
                : Set.copyOf(institutionTypes);
        Values.requireRange("appointmentInsulation", appointmentInsulation, 0.0, 1.0);
        Values.requireRange("removalForCauseProtection", removalForCauseProtection, 0.0, 1.0);
        Values.requireRange("budgetAutonomy", budgetAutonomy, 0.0, 1.0);
        Values.requireRange("staffingAutonomy", staffingAutonomy, 0.0, 1.0);
        Values.requireRange("compulsoryInformationAccess", compulsoryInformationAccess, 0.0, 1.0);
        Values.requireRange("publicationTimetable", publicationTimetable, 0.0, 1.0);
        Values.requireRange("enforcementReferralPower", enforcementReferralPower, 0.0, 1.0);
        Values.requireRange("judicialReviewExposure", judicialReviewExposure, 0.0, 1.0);
    }

    public static IndependentInstitutionBundle advisoryFiscalLegal() {
        return new IndependentInstitutionBundle(
                Set.of(IndependentInstitutionType.FISCAL_COUNCIL, IndependentInstitutionType.COST_ESTIMATOR),
                0.54,
                0.48,
                0.56,
                0.58,
                0.66,
                0.72,
                0.32,
                0.42
        );
    }

    public static IndependentInstitutionBundle strongInsulation() {
        return new IndependentInstitutionBundle(
                Set.of(
                        IndependentInstitutionType.ELECTORAL_COMMISSION,
                        IndependentInstitutionType.BOUNDARY_COMMISSION,
                        IndependentInstitutionType.FISCAL_COUNCIL,
                        IndependentInstitutionType.AUDIT_BODY,
                        IndependentInstitutionType.ETHICS_BODY
                ),
                0.78,
                0.82,
                0.76,
                0.74,
                0.86,
                0.84,
                0.72,
                0.56
        );
    }

    public double insulationScore() {
        return Values.clamp(
                (appointmentInsulation
                        + removalForCauseProtection
                        + budgetAutonomy
                        + staffingAutonomy
                        + compulsoryInformationAccess
                        + publicationTimetable
                        + enforcementReferralPower) / 7.0,
                0.0,
                1.0
        );
    }

    public double quietCaptureRisk() {
        return Values.clamp(
                (1.0 - insulationScore())
                        + (0.22 * (1.0 - budgetAutonomy))
                        + (0.18 * (1.0 - compulsoryInformationAccess))
                        - (0.14 * publicationTimetable),
                0.0,
                1.0
        );
    }
}
