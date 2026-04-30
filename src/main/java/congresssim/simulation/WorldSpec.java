package congresssim.simulation;

import congresssim.util.Values;

import java.util.Objects;

public record WorldSpec(
        int legislatorCount,
        int billCount,
        int partyCount,
        double polarization,
        double partyLoyalty,
        double lobbyingSusceptibility,
        double constituencySensitivity,
        double compromiseCulture,
        PartySystemProfile partySystemProfile,
        double partySystemWeight,
        ProposalShockProfile proposalShockProfile
) {
    public WorldSpec(
            int legislatorCount,
            int billCount,
            int partyCount,
            double polarization,
            double partyLoyalty,
            double lobbyingSusceptibility,
            double constituencySensitivity,
            double compromiseCulture
    ) {
        this(
                legislatorCount,
                billCount,
                partyCount,
                polarization,
                partyLoyalty,
                lobbyingSusceptibility,
                constituencySensitivity,
                compromiseCulture,
                PartySystemProfile.IDEOLOGICAL_BINS,
                1.0,
                ProposalShockProfile.BASELINE
        );
    }

    public WorldSpec(
            int legislatorCount,
            int billCount,
            int partyCount,
            double polarization,
            double partyLoyalty,
            double lobbyingSusceptibility,
            double constituencySensitivity,
            double compromiseCulture,
            PartySystemProfile partySystemProfile,
            double partySystemWeight
    ) {
        this(
                legislatorCount,
                billCount,
                partyCount,
                polarization,
                partyLoyalty,
                lobbyingSusceptibility,
                constituencySensitivity,
                compromiseCulture,
                partySystemProfile,
                partySystemWeight,
                ProposalShockProfile.BASELINE
        );
    }

    public WorldSpec {
        if (legislatorCount <= 0 || billCount <= 0 || partyCount <= 0) {
            throw new IllegalArgumentException("legislatorCount, billCount, and partyCount must be positive.");
        }
        partySystemProfile = Objects.requireNonNull(partySystemProfile, "partySystemProfile");
        proposalShockProfile = Objects.requireNonNull(proposalShockProfile, "proposalShockProfile");
        if (!Double.isFinite(partySystemWeight) || partySystemWeight <= 0.0) {
            throw new IllegalArgumentException("partySystemWeight must be finite and positive.");
        }
        Values.requireRange("polarization", polarization, 0.0, 1.0);
        Values.requireRange("partyLoyalty", partyLoyalty, 0.0, 1.0);
        Values.requireRange("lobbyingSusceptibility", lobbyingSusceptibility, 0.0, 1.0);
        Values.requireRange("constituencySensitivity", constituencySensitivity, 0.0, 1.0);
        Values.requireRange("compromiseCulture", compromiseCulture, 0.0, 1.0);
    }
}
