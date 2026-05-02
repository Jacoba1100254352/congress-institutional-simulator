package congresssim.institution.chamber;

import congresssim.institution.voting.VotingRule;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

import java.util.List;

public final class Chamber {
    private final String name;
    private final List<Legislator> legislators;
    private final VotingStrategy votingStrategy;
    private final VotingRule votingRule;

    public Chamber(String name, List<Legislator> legislators, VotingStrategy votingStrategy, VotingRule votingRule) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("A chamber must have at least one legislator.");
        }
        this.name = name;
        this.legislators = List.copyOf(legislators);
        this.votingStrategy = votingStrategy;
        this.votingRule = votingRule;
    }

    public String name() {
        return name;
    }

    public List<Legislator> legislators() {
        return legislators;
    }

    public ChamberVoteResult voteOn(Bill bill, VoteContext context) {
        int yay = 0;
        int nay = 0;

        for (Legislator legislator : legislators) {
            Vote vote = votingStrategy.vote(legislator, bill, context);
            if (vote == Vote.YAY) {
                yay++;
            } else {
                nay++;
            }
        }

        boolean passed = votingRule.passes(yay, nay);
        return new ChamberVoteResult(name, votingRule.name(), yay, nay, passed);
    }
}
