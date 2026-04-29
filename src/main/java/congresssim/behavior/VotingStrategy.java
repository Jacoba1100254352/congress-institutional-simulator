package congresssim.behavior;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

public interface VotingStrategy {
    Vote vote(Legislator legislator, Bill bill, VoteContext context);
}

