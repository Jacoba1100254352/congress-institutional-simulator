package congresssim.simulation;

import congresssim.util.Values;

public record ChamberSpec(
        String name,
        int targetSize,
        SeatAllocationProfile seatAllocationProfile,
        SelectionMode selectionMode,
        int districtMagnitude,
        int territorialUnitCount,
        double legalThreshold,
        double malapportionmentStrength,
        double appointedShare,
        int lowerHouseTermLength,
        int upperHouseTermLength,
        int renewalCohortCount,
        String selectorBody
) {
    public ChamberSpec {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank.");
        }
        if (targetSize <= 0) {
            throw new IllegalArgumentException("targetSize must be positive.");
        }
        if (seatAllocationProfile == null) {
            throw new IllegalArgumentException("seatAllocationProfile must not be null.");
        }
        if (selectionMode == null) {
            throw new IllegalArgumentException("selectionMode must not be null.");
        }
        if (districtMagnitude <= 0) {
            throw new IllegalArgumentException("districtMagnitude must be positive.");
        }
        if (territorialUnitCount <= 0) {
            throw new IllegalArgumentException("territorialUnitCount must be positive.");
        }
        Values.requireRange("legalThreshold", legalThreshold, 0.0, 1.0);
        Values.requireRange("malapportionmentStrength", malapportionmentStrength, 0.0, 1.0);
        Values.requireRange("appointedShare", appointedShare, 0.0, 1.0);
        if (lowerHouseTermLength <= 0 || upperHouseTermLength <= 0) {
            throw new IllegalArgumentException("term lengths must be positive.");
        }
        if (renewalCohortCount <= 0) {
            throw new IllegalArgumentException("renewalCohortCount must be positive.");
        }
        if (selectorBody == null || selectorBody.isBlank()) {
            throw new IllegalArgumentException("selectorBody must not be blank.");
        }
    }

    public static ChamberSpec lowerHouse(int targetSize) {
        return new ChamberSpec(
                "Lower house",
                targetSize,
                SeatAllocationProfile.EQUAL_POPULATION_SINGLE_MEMBER,
                SelectionMode.ELECTED_SINGLE_MEMBER,
                1,
                Math.max(1, Math.min(targetSize, 12)),
                0.0,
                0.0,
                0.0,
                2,
                6,
                1,
                "general-electorate"
        );
    }

    public static ChamberSpec proportionalHouse(int targetSize, int districtMagnitude, double legalThreshold) {
        return new ChamberSpec(
                "Proportional lower house",
                targetSize,
                SeatAllocationProfile.PROPORTIONAL_PARTY_LIST,
                SelectionMode.ELECTED_PROPORTIONAL,
                districtMagnitude,
                Math.max(1, Math.min(targetSize, 12)),
                legalThreshold,
                0.0,
                0.0,
                2,
                6,
                1,
                "party-list-electorate"
        );
    }

    public static ChamberSpec territorialUpperHouse(int targetSize, double malapportionmentStrength) {
        return new ChamberSpec(
                "Territorial upper house",
                targetSize,
                SeatAllocationProfile.MALAPPORTIONED_TERRITORIAL,
                SelectionMode.INDIRECT_SUBNATIONAL,
                1,
                Math.max(2, Math.min(targetSize, 12)),
                0.0,
                malapportionmentStrength,
                0.0,
                2,
                6,
                3,
                "subnational-governments"
        );
    }

    public static ChamberSpec appointedUpperHouse(int targetSize, double appointedShare) {
        return new ChamberSpec(
                "Appointed upper house",
                targetSize,
                SeatAllocationProfile.MIXED_ELECTED_APPOINTED,
                SelectionMode.MIXED,
                1,
                Math.max(2, Math.min(targetSize, 12)),
                0.0,
                0.35,
                appointedShare,
                2,
                8,
                4,
                "mixed-election-and-appointment"
        );
    }
}
