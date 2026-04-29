package congresssim.behavior;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

import java.util.List;

public final class WeightedVotingStrategy implements VotingStrategy {
    private final List<VoteInfluence> influences;
    private final double randomNoise;

    public WeightedVotingStrategy(List<VoteInfluence> influences, double randomNoise) {
        this.influences = List.copyOf(influences);
        this.randomNoise = randomNoise;
    }

    @Override
    public Vote vote(Legislator legislator, Bill bill, VoteContext context) {
        double score = 0.0;
        for (VoteInfluence influence : influences) {
            score += influence.score(legislator, bill, context);
        }
        score += context.random().nextGaussian() * randomNoise;

        double probability = logistic(score);
        return context.random().nextDouble() < probability ? Vote.YAY : Vote.NAY;
    }

    private static double logistic(double score) {
        double bounded = Math.max(-12.0, Math.min(12.0, score));
        return 1.0 / (1.0 + Math.exp(-bounded));
    }
}

