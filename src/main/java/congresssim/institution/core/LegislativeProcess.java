package congresssim.institution.core;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

public interface LegislativeProcess {
    String name();

    BillOutcome consider(Bill bill, VoteContext context);
}

