package congresssim.model;

import congresssim.util.Values;

public record LobbyGroup(
        String id,
        String issueDomain,
        double preferredPolicyPosition,
        double budget,
        double influenceIntensity,
        double defensiveMultiplier,
        double informationBias,
        double publicCampaignSkill
) {
    public LobbyGroup {
        Values.requireRange("preferredPolicyPosition", preferredPolicyPosition, -1.0, 1.0);
        Values.requireRange("budget", budget, 0.0, 10.0);
        Values.requireRange("influenceIntensity", influenceIntensity, 0.0, 1.0);
        Values.requireRange("defensiveMultiplier", defensiveMultiplier, 0.0, 3.0);
        Values.requireRange("informationBias", informationBias, 0.0, 1.0);
        Values.requireRange("publicCampaignSkill", publicCampaignSkill, 0.0, 1.0);
    }
}
