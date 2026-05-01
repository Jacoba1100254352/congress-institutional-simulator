package congresssim.institution;

import congresssim.model.Legislator;
import congresssim.util.Values;

public record EligibilityRule(
        int minimumAge,
        int minimumResidencyYears,
        double languageRequirement,
        double expertiseThreshold,
        double conflictOfInterestThreshold,
        double attendanceThreshold,
        double captureRiskThreshold,
        boolean banDualOffice,
        boolean banPartyExecutiveRegulatorOverlap,
        boolean sectorRecusalRule,
        int preLobbyingCoolingOffYears,
        int postOfficeCoolingOffYears,
        int termLimitYears,
        boolean recallPossible,
        double publicSupportRetentionThreshold,
        boolean removalAfterSanctions,
        double selectorCaptureRisk,
        double turnoverRate
) {
    public EligibilityRule {
        if (minimumAge < 0 || minimumResidencyYears < 0) {
            throw new IllegalArgumentException("age and residency requirements must be nonnegative.");
        }
        Values.requireRange("languageRequirement", languageRequirement, 0.0, 1.0);
        Values.requireRange("expertiseThreshold", expertiseThreshold, 0.0, 1.0);
        Values.requireRange("conflictOfInterestThreshold", conflictOfInterestThreshold, 0.0, 1.0);
        Values.requireRange("attendanceThreshold", attendanceThreshold, 0.0, 1.0);
        Values.requireRange("captureRiskThreshold", captureRiskThreshold, 0.0, 1.0);
        if (preLobbyingCoolingOffYears < 0 || postOfficeCoolingOffYears < 0 || termLimitYears < 0) {
            throw new IllegalArgumentException("cooling-off and term-limit values must be nonnegative.");
        }
        Values.requireRange("publicSupportRetentionThreshold", publicSupportRetentionThreshold, 0.0, 1.0);
        Values.requireRange("selectorCaptureRisk", selectorCaptureRisk, 0.0, 1.0);
        Values.requireRange("turnoverRate", turnoverRate, 0.0, 1.0);
    }

    public static EligibilityRule expertiseMajority() {
        return new EligibilityRule(
                25,
                5,
                0.35,
                0.52,
                0.72,
                0.40,
                0.72,
                false,
                false,
                false,
                1,
                1,
                12,
                true,
                0.38,
                true,
                0.22,
                0.24
        );
    }

    public static EligibilityRule appointmentRetention() {
        return new EligibilityRule(
                35,
                8,
                0.48,
                0.60,
                0.66,
                0.52,
                0.68,
                true,
                true,
                false,
                2,
                2,
                14,
                false,
                0.45,
                true,
                0.46,
                0.16
        );
    }

    public static EligibilityRule recusalCoolingOff() {
        return new EligibilityRule(
                28,
                6,
                0.40,
                0.48,
                0.50,
                0.46,
                0.54,
                true,
                true,
                true,
                4,
                5,
                10,
                true,
                0.42,
                true,
                0.28,
                0.22
        );
    }

    public boolean eligible(Legislator legislator) {
        return ageProxy(legislator) >= minimumAge
                && residencyProxy(legislator) >= minimumResidencyYears
                && languageProxy(legislator) >= languageRequirement
                && expertiseProxy(legislator) >= expertiseThreshold
                && conflictProxy(legislator) <= conflictOfInterestThreshold
                && attendanceProxy(legislator) >= attendanceThreshold
                && captureProxy(legislator) <= captureRiskThreshold
                && (!banDualOffice || !dualOfficeProxy(legislator))
                && (!banPartyExecutiveRegulatorOverlap || !overlapProxy(legislator));
    }

    public static double expertiseProxy(Legislator legislator) {
        return Values.clamp(
                (0.34 * legislator.compromisePreference())
                        + (0.30 * legislator.reputationSensitivity())
                        + (0.22 * legislator.constituencySensitivity())
                        + (0.14 * (1.0 - legislator.lobbySensitivity())),
                0.0,
                1.0
        );
    }

    public static double conflictProxy(Legislator legislator) {
        return Values.clamp(
                (0.58 * legislator.lobbySensitivity())
                        + (0.24 * Math.abs(legislator.ideology()))
                        + (0.18 * stableUnit(legislator, "conflict")),
                0.0,
                1.0
        );
    }

    public static double captureProxy(Legislator legislator) {
        return Values.clamp(
                (0.52 * legislator.lobbySensitivity())
                        + (0.24 * legislator.partyLoyalty())
                        + (0.24 * stableUnit(legislator, "selector")),
                0.0,
                1.0
        );
    }

    public static double sectorAlignment(Legislator legislator, String issueDomain) {
        return stableUnit(legislator, "sector:" + issueDomain);
    }

    private static int ageProxy(Legislator legislator) {
        return 24 + (int) Math.round(42.0 * stableUnit(legislator, "age"));
    }

    private static int residencyProxy(Legislator legislator) {
        return 1 + (int) Math.round(18.0 * stableUnit(legislator, "residency"));
    }

    private static double languageProxy(Legislator legislator) {
        return 0.42 + (0.58 * legislator.reputationSensitivity());
    }

    private static double attendanceProxy(Legislator legislator) {
        return Values.clamp(
                (0.55 * legislator.reputationSensitivity())
                        + (0.25 * legislator.constituencySensitivity())
                        + (0.20 * (1.0 - Math.abs(legislator.ideology()))),
                0.0,
                1.0
        );
    }

    private static boolean dualOfficeProxy(Legislator legislator) {
        return stableUnit(legislator, "dual") > 0.82;
    }

    private static boolean overlapProxy(Legislator legislator) {
        return legislator.partyLoyalty() > 0.76 && stableUnit(legislator, "overlap") > 0.64;
    }

    private static double stableUnit(Legislator legislator, String salt) {
        int hash = Math.floorMod((legislator.id() + ":" + salt).hashCode(), 10_000);
        return hash / 10_000.0;
    }
}
