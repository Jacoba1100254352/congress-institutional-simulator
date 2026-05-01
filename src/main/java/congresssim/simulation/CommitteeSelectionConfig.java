package congresssim.simulation;

import congresssim.util.Values;

public record CommitteeSelectionConfig(
        String issueDomain,
        long randomSeed,
        CommitteeQuotaRule partyQuotaRule,
        double expertiseWeight,
        double independenceWeight,
        double leadershipControlStrength,
        int rotationMemory,
        ChairAllocationRule chairAllocationRule,
        double quorumPartyBalance,
        double citizenMemberRatio,
        boolean topicReferralAuthority,
        int targetSize
) {
    public CommitteeSelectionConfig {
        if (issueDomain == null || issueDomain.isBlank()) {
            issueDomain = "general";
        }
        if (partyQuotaRule == null) {
            partyQuotaRule = CommitteeQuotaRule.REPRESENTATIVE;
        }
        if (chairAllocationRule == null) {
            chairAllocationRule = ChairAllocationRule.MAJORITY;
        }
        Values.requireRange("expertiseWeight", expertiseWeight, 0.0, 1.0);
        Values.requireRange("independenceWeight", independenceWeight, 0.0, 1.0);
        Values.requireRange("leadershipControlStrength", leadershipControlStrength, 0.0, 1.0);
        if (rotationMemory < 0) {
            throw new IllegalArgumentException("rotationMemory must be nonnegative.");
        }
        Values.requireRange("quorumPartyBalance", quorumPartyBalance, 0.0, 1.0);
        Values.requireRange("citizenMemberRatio", citizenMemberRatio, 0.0, 1.0);
        if (targetSize <= 0) {
            throw new IllegalArgumentException("targetSize must be positive.");
        }
    }

    public static CommitteeSelectionConfig standard(String issueDomain, int targetSize) {
        return new CommitteeSelectionConfig(
                issueDomain,
                404L,
                CommitteeQuotaRule.REPRESENTATIVE,
                0.35,
                0.25,
                0.20,
                0,
                ChairAllocationRule.MAJORITY,
                0.35,
                0.0,
                true,
                targetSize
        );
    }
}
