package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

import java.util.List;

public final class BicameralProcess implements LegislativeProcess {
    private final String name;
    private final Chamber firstChamber;
    private final Chamber secondChamber;

    public BicameralProcess(String name, Chamber firstChamber, Chamber secondChamber) {
        this.name = name;
        this.firstChamber = firstChamber;
        this.secondChamber = secondChamber;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ChamberVoteResult firstResult = firstChamber.voteOn(bill, context);
        ChamberVoteResult secondResult = secondChamber.voteOn(bill, context);
        boolean enacted = firstResult.passed() && secondResult.passed();
        double statusQuoBefore = context.currentPolicyPosition();
        String reason = enacted ? "passed both chambers" : "failed chamber passage";
        return new BillOutcome(
                bill,
                statusQuoBefore,
                enacted ? bill.ideologyPosition() : statusQuoBefore,
                enacted,
                List.of(firstResult, secondResult),
                PresidentialAction.none(),
                reason
        );
    }
}
