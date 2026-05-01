package congresssim.model;

import congresssim.util.Values;

public record RepresentationProfile(
        String chamberEligibility,
        double populationRepresented,
        int districtMagnitude,
        String regionLabel,
        String selectionMode,
        boolean appointed,
        int lowerHouseTermLength,
        int upperHouseTermLength,
        int renewalCohort,
        int renewalCycleLength,
        int nextRenewalRound,
        String selectorBody
) {
    public RepresentationProfile {
        if (chamberEligibility == null || chamberEligibility.isBlank()) {
            throw new IllegalArgumentException("chamberEligibility must not be blank.");
        }
        Values.requireRange("populationRepresented", populationRepresented, 0.0, 1.0);
        if (districtMagnitude <= 0) {
            throw new IllegalArgumentException("districtMagnitude must be positive.");
        }
        if (regionLabel == null || regionLabel.isBlank()) {
            throw new IllegalArgumentException("regionLabel must not be blank.");
        }
        if (selectionMode == null || selectionMode.isBlank()) {
            throw new IllegalArgumentException("selectionMode must not be blank.");
        }
        if (lowerHouseTermLength <= 0 || upperHouseTermLength <= 0) {
            throw new IllegalArgumentException("term lengths must be positive.");
        }
        if (renewalCohort < 0) {
            throw new IllegalArgumentException("renewalCohort must be nonnegative.");
        }
        if (renewalCycleLength <= 0) {
            throw new IllegalArgumentException("renewalCycleLength must be positive.");
        }
        if (nextRenewalRound <= 0) {
            throw new IllegalArgumentException("nextRenewalRound must be positive.");
        }
        if (selectorBody == null || selectorBody.isBlank()) {
            throw new IllegalArgumentException("selectorBody must not be blank.");
        }
    }

    public static RepresentationProfile standardElected() {
        return new RepresentationProfile(
                "lower-and-upper-eligible",
                0.0,
                1,
                "national",
                "ELECTED_SINGLE_MEMBER",
                false,
                2,
                6,
                0,
                2,
                2,
                "general-electorate"
        );
    }
}
