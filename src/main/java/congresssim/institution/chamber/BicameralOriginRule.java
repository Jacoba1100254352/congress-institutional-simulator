package congresssim.institution.chamber;

import congresssim.model.Bill;

public enum BicameralOriginRule {
    LOWER_FIRST,
    UPPER_FIRST,
    HOUSE_ORIGIN_ONLY,
    SENATE_ORIGIN_ONLY,
    REVENUE_LOWER,
    EMERGENCY_LOWER_FAST,
    PROPOSER_CHAMBER,
    LEADERSHIP_ROUTED,
    PRINCIPLES_RESOLUTION_FIRST,
    SECOND_CHAMBER_PRECLEARANCE,
    ISSUE_ROUTED,
    HIGH_RISK_UPPER_PRECLEARANCE,
    BILL_HASH_RANDOM;

    boolean startsInUpper(Bill bill) {
        return switch (this) {
            case LOWER_FIRST -> false;
            case UPPER_FIRST -> true;
            case HOUSE_ORIGIN_ONLY -> false;
            case SENATE_ORIGIN_ONLY -> true;
            case REVENUE_LOWER -> !isRevenueDomain(bill.issueDomain()) && isUpperDomain(bill.issueDomain());
            case EMERGENCY_LOWER_FAST -> bill.salience() < 0.88 && isUpperDomain(bill.issueDomain());
            case PROPOSER_CHAMBER -> bill.proposerIdeology() > 0.28 || Math.floorMod(bill.proposerId().hashCode(), 5) == 0;
            case LEADERSHIP_ROUTED -> bill.publicSupport() < 0.45 && bill.salience() >= 0.55;
            case PRINCIPLES_RESOLUTION_FIRST -> true;
            case SECOND_CHAMBER_PRECLEARANCE -> riskScore(bill) >= 0.42;
            case ISSUE_ROUTED -> isUpperDomain(bill.issueDomain());
            case HIGH_RISK_UPPER_PRECLEARANCE -> riskScore(bill) >= 0.58;
            case BILL_HASH_RANDOM -> Math.floorMod(bill.id().hashCode(), 2) == 1;
        };
    }

    private static boolean isRevenueDomain(String issueDomain) {
        String normalized = issueDomain == null ? "" : issueDomain.toLowerCase();
        return normalized.contains("tax")
                || normalized.contains("budget")
                || normalized.contains("revenue")
                || normalized.contains("finance")
                || normalized.contains("economy");
    }

    private static boolean isUpperDomain(String issueDomain) {
        String normalized = issueDomain == null ? "" : issueDomain.toLowerCase();
        return normalized.contains("defense")
                || normalized.contains("foreign")
                || normalized.contains("security")
                || normalized.contains("treaty")
                || normalized.contains("constitution");
    }

    private static double riskScore(Bill bill) {
        return Math.clamp(
                (0.30 * bill.salience())
                        + (0.28 * bill.publicBenefitUncertainty())
                        + (0.26 * bill.concentratedHarm())
                        + (0.16 * Math.max(0.0, bill.lobbyPressure())),
                0.0,
                1.0
        );
    }
}
