package congresssim.institution;

import congresssim.util.Values;

public record CommitteePowerConfig(
        CommitteeRoleMode roleMode,
        double gatekeepingThreshold,
        double chairNegativeAgendaPower,
        double informationAccuracy,
        double queueCapacity,
        double reviewCost,
        double captureSusceptibility,
        double transparencyLevel,
        double publicOverrideThreshold,
        double hearingTransparency,
        double publicReferralThreshold,
        double quorumPartyBalanceRequirement,
        boolean chairCastingVote,
        boolean minorityAmendmentRight
) {
    public CommitteePowerConfig {
        if (roleMode == null) {
            roleMode = CommitteeRoleMode.PRIORITY_QUEUE;
        }
        Values.requireRange("gatekeepingThreshold", gatekeepingThreshold, 0.0, 1.0);
        Values.requireRange("chairNegativeAgendaPower", chairNegativeAgendaPower, 0.0, 1.0);
        Values.requireRange("informationAccuracy", informationAccuracy, 0.0, 1.0);
        Values.requireRange("queueCapacity", queueCapacity, 0.0, 1.0);
        Values.requireRange("reviewCost", reviewCost, 0.0, 1.0);
        Values.requireRange("captureSusceptibility", captureSusceptibility, 0.0, 1.0);
        Values.requireRange("transparencyLevel", transparencyLevel, 0.0, 1.0);
        Values.requireRange("publicOverrideThreshold", publicOverrideThreshold, 0.0, 1.0);
        Values.requireRange("hearingTransparency", hearingTransparency, 0.0, 1.0);
        Values.requireRange("publicReferralThreshold", publicReferralThreshold, 0.0, 1.0);
        Values.requireRange("quorumPartyBalanceRequirement", quorumPartyBalanceRequirement, 0.0, 1.0);
    }

    public static CommitteePowerConfig standard() {
        return new CommitteePowerConfig(
                CommitteeRoleMode.PRIORITY_QUEUE,
                0.52,
                0.35,
                0.62,
                0.55,
                0.22,
                0.35,
                0.50,
                0.62,
                0.48,
                0.50,
                0.34,
                false,
                true
        );
    }
}
