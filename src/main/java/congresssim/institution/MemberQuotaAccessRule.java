package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

import java.util.HashMap;
import java.util.Map;

final class MemberQuotaAccessRule implements ProposalAccessRule {
    private final int quotaPerProposer;
    private final Map<String, Integer> usedSlots = new HashMap<>();

    MemberQuotaAccessRule(int quotaPerProposer) {
        if (quotaPerProposer < 1) {
            throw new IllegalArgumentException("quotaPerProposer must be positive.");
        }
        this.quotaPerProposer = quotaPerProposer;
    }

    @Override
    public String name() {
        return "member proposal quota";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        int used = usedSlots.getOrDefault(bill.proposerId(), 0);
        if (used >= quotaPerProposer) {
            return AccessDecision.denied("member proposal quota exhausted");
        }
        usedSlots.put(bill.proposerId(), used + 1);
        return AccessDecision.granted("member proposal quota available");
    }
}
