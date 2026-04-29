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

    public static WeightedVotingStrategy antiCapture() {
        return new WeightedVotingStrategy(
                List.of(
                        StandardInfluences.ideology(1.45),
                        StandardInfluences.party(0.78),
                        StandardInfluences.constituency(1.12),
                        StandardInfluences.lobbying(0.14),
                        StandardInfluences.compromise(0.82),
                        StandardInfluences.reputation(0.92)
                ),
                0.25
        );
    }
}
