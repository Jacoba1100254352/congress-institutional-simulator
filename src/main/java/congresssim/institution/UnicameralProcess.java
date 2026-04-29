package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

import java.util.List;

public final class UnicameralProcess implements LegislativeProcess {
    private final String name;
    private final Chamber chamber;

    public UnicameralProcess(String name, Chamber chamber) {
        this.name = name;
        this.chamber = chamber;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ChamberVoteResult result = chamber.voteOn(bill, context);
        double statusQuoBefore = context.currentPolicyPosition();
        return new BillOutcome(
                bill,
                statusQuoBefore,
                result.passed() ? bill.ideologyPosition() : statusQuoBefore,
                result.passed(),
                List.of(result),
                PresidentialAction.none(),
                result.passed() ? "passed chamber" : "failed chamber"
        );
    }
}
