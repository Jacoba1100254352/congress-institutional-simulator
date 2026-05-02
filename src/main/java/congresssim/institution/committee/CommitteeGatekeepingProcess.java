package congresssim.institution.committee;

import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberVoteResult;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public final class CommitteeGatekeepingProcess implements LegislativeProcess {
    private final String name;
    private final Chamber committee;
    private final LegislativeProcess innerProcess;

    public CommitteeGatekeepingProcess(String name, Chamber committee, LegislativeProcess innerProcess) {
        this.name = name;
        this.committee = committee;
        this.innerProcess = innerProcess;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ChamberVoteResult committeeResult = committee.voteOn(bill, context);
        if (!committeeResult.passed()) {
            return BillOutcome.committeeRejected(
                    bill,
                    context.currentPolicyPosition(),
                    committeeResult,
                    "rejected by committee gate"
            );
        }

        return innerProcess.consider(bill, context).withGateResult(committeeResult);
    }
}

