package congresssim.behavior;

import java.util.List;

public final class VotingStrategies {
    private VotingStrategies() {
    }

    public static WeightedVotingStrategy standard() {
        return new WeightedVotingStrategy(
                List.of(
                        StandardInfluences.ideology(1.45),
                        StandardInfluences.party(0.85),
                        StandardInfluences.constituency(0.95),
                        StandardInfluences.lobbying(0.55),
                        StandardInfluences.compromise(0.75),
                        StandardInfluences.reputation(0.55)
                ),
                0.25
        );
    }
}

