package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public interface ProposalAccessRule {
    String name();

    AccessDecision evaluate(Bill bill, VoteContext context);
}

