package congresssim.behavior;

import congresssim.model.Bill;
import congresssim.model.Legislator;

public interface VoteInfluence {
    String name();

    double score(Legislator legislator, Bill bill, VoteContext context);
}

