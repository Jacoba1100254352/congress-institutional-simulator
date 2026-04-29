package congresssim.simulation;

import congresssim.util.Values;

public record WorldSpec(
        int legislatorCount,
        int billCount,
        int partyCount,
        double polarization,
        double partyLoyalty,
        double lobbyingSusceptibility,
        double constituencySensitivity,
        double compromiseCulture
) {
    public WorldSpec {
        if (legislatorCount <= 0 || billCount <= 0 || partyCount <= 0) {
            throw new IllegalArgumentException("legislatorCount, billCount, and partyCount must be positive.");
        }
        Values.requireRange("polarization", polarization, 0.0, 1.0);
        Values.requireRange("partyLoyalty", partyLoyalty, 0.0, 1.0);
        Values.requireRange("lobbyingSusceptibility", lobbyingSusceptibility, 0.0, 1.0);
        Values.requireRange("constituencySensitivity", constituencySensitivity, 0.0, 1.0);
        Values.requireRange("compromiseCulture", compromiseCulture, 0.0, 1.0);
    }
}
