package congresssim.model;

import congresssim.util.Values;

import java.util.LinkedHashMap;
import java.util.Map;

public record LobbyGroup(
        String id,
        String issueDomain,
        Map<String, Double> issuePreferences,
        double preferredPolicyPosition,
        double budget,
        double influenceIntensity,
        double defensiveMultiplier,
        double informationBias,
        double publicCampaignSkill,
        LobbyCaptureStrategy captureStrategy,
        double publicSupportMismatchTolerance
) {
    public LobbyGroup {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("id must not be blank.");
        }
        if (issueDomain == null || issueDomain.isBlank()) {
            throw new IllegalArgumentException("issueDomain must not be blank.");
        }
        if (captureStrategy == null) {
            throw new IllegalArgumentException("captureStrategy must not be null.");
        }
        Values.requireRange("preferredPolicyPosition", preferredPolicyPosition, -1.0, 1.0);
        Values.requireRange("budget", budget, 0.0, 10.0);
        Values.requireRange("influenceIntensity", influenceIntensity, 0.0, 1.0);
        Values.requireRange("defensiveMultiplier", defensiveMultiplier, 0.0, 3.0);
        Values.requireRange("informationBias", informationBias, 0.0, 1.0);
        Values.requireRange("publicCampaignSkill", publicCampaignSkill, 0.0, 1.0);
        Values.requireRange("publicSupportMismatchTolerance", publicSupportMismatchTolerance, 0.0, 1.0);
        issuePreferences = normalizeIssuePreferences(issueDomain, issuePreferences);
    }

    public LobbyGroup(
            String id,
            String issueDomain,
            double preferredPolicyPosition,
            double budget,
            double influenceIntensity,
            double defensiveMultiplier,
            double informationBias,
            double publicCampaignSkill
    ) {
        this(
                id,
                issueDomain,
                Map.of(issueDomain, 1.0),
                preferredPolicyPosition,
                budget,
                influenceIntensity,
                defensiveMultiplier,
                informationBias,
                publicCampaignSkill,
                LobbyCaptureStrategy.BALANCED,
                0.35
        );
    }

    public double preferenceFor(String domain) {
        return issuePreferences.getOrDefault(domain, 0.0);
    }

    private static Map<String, Double> normalizeIssuePreferences(String primaryDomain, Map<String, Double> preferences) {
        Map<String, Double> normalized = new LinkedHashMap<>();
        if (preferences != null) {
            for (Map.Entry<String, Double> entry : preferences.entrySet()) {
                if (entry.getKey() == null || entry.getKey().isBlank()) {
                    continue;
                }
                Values.requireRange("issuePreference", entry.getValue(), 0.0, 1.0);
                if (entry.getValue() > 0.0) {
                    normalized.put(entry.getKey(), entry.getValue());
                }
            }
        }
        normalized.putIfAbsent(primaryDomain, 1.0);
        return Map.copyOf(normalized);
    }
}
