package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

final class OpenProposalAccessRule implements ProposalAccessRule {
    @Override
    public String name() {
        return "open proposal access";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        return AccessDecision.granted("open access");
    }
}

