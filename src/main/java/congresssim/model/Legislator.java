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
        double reputationSensitivity,
        double districtPreference,
        double districtIntensity,
        double affectedGroupSensitivity
) {
    public Legislator {
        Values.requireRange("ideology", ideology, -1.0, 1.0);
        Values.requireRange("compromisePreference", compromisePreference, 0.0, 1.0);
        Values.requireRange("partyLoyalty", partyLoyalty, 0.0, 1.0);
        Values.requireRange("constituencySensitivity", constituencySensitivity, 0.0, 1.0);
        Values.requireRange("lobbySensitivity", lobbySensitivity, 0.0, 1.0);
        Values.requireRange("reputationSensitivity", reputationSensitivity, 0.0, 1.0);
        Values.requireRange("districtPreference", districtPreference, -1.0, 1.0);
        Values.requireRange("districtIntensity", districtIntensity, 0.0, 1.0);
        Values.requireRange("affectedGroupSensitivity", affectedGroupSensitivity, 0.0, 1.0);
    }

    public Legislator(
            String id,
            String party,
            double ideology,
            double compromisePreference,
            double partyLoyalty,
            double constituencySensitivity,
            double lobbySensitivity,
            double reputationSensitivity
    ) {
        this(
                id,
                party,
                ideology,
                compromisePreference,
                partyLoyalty,
                constituencySensitivity,
                lobbySensitivity,
                reputationSensitivity,
                ideology,
                constituencySensitivity,
                reputationSensitivity
        );
    }
}
