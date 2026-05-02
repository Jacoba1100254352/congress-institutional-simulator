package congresssim.institution.agenda;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public final class ProposalAccessProcess implements LegislativeProcess {
    private final String name;
    private final ProposalAccessRule accessRule;
    private final LegislativeProcess innerProcess;

    public ProposalAccessProcess(String name, ProposalAccessRule accessRule, LegislativeProcess innerProcess) {
        this.name = name;
        this.accessRule = accessRule;
        this.innerProcess = innerProcess;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        AccessDecision decision = accessRule.evaluate(bill, context);
        if (!decision.granted()) {
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    decision.reason()
            );
        }
        return innerProcess.consider(bill, context);
    }
}

