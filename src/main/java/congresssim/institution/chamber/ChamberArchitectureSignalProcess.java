package congresssim.institution.chamber;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public final class ChamberArchitectureSignalProcess implements LegislativeProcess {
    private final LegislativeProcess innerProcess;
    private final OutcomeSignals architectureSignals;

    public ChamberArchitectureSignalProcess(
            LegislativeProcess innerProcess,
            OutcomeSignals architectureSignals
    ) {
        this.innerProcess = innerProcess;
        this.architectureSignals = architectureSignals;
    }

    @Override
    public String name() {
        return innerProcess.name();
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        return innerProcess.consider(bill, context).withSignals(architectureSignals);
    }
}
