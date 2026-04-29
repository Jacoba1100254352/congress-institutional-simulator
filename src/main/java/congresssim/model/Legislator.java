package congresssim.model;

import congresssim.util.Values;

public record Legislator(
        String id,
        String party,
        double ideology,
        double compromisePreference,
        double partyLoyalty,
        double constituencySensitivity,
        double lobbySensitivity,
        double reputationSensitivity
) {
    public Legislator {
        Values.requireRange("ideology", ideology, -1.0, 1.0);
        Values.requireRange("compromisePreference", compromisePreference, 0.0, 1.0);
        Values.requireRange("partyLoyalty", partyLoyalty, 0.0, 1.0);
        Values.requireRange("constituencySensitivity", constituencySensitivity, 0.0, 1.0);
        Values.requireRange("lobbySensitivity", lobbySensitivity, 0.0, 1.0);
        Values.requireRange("reputationSensitivity", reputationSensitivity, 0.0, 1.0);
    }
}

