package congresssim.institution.distribution;

import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberVoteResult;
import congresssim.institution.chamber.PresidentialAction;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;

import java.util.List;

public final class HarmWeightedThresholdProcess implements LegislativeProcess {
    private final String name;
    private final Chamber ordinaryChamber;
    private final Chamber harmChamber;
    private final double harmThreshold;

    public HarmWeightedThresholdProcess(
            String name,
            Chamber ordinaryChamber,
            Chamber harmChamber,
            double harmThreshold
    ) {
        if (harmThreshold < 0.0 || harmThreshold > 1.0) {
            throw new IllegalArgumentException("harmThreshold must be in [0, 1].");
        }
        this.name = name;
        this.ordinaryChamber = ordinaryChamber;
        this.harmChamber = harmChamber;
        this.harmThreshold = harmThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Chamber selected = bill.concentratedHarm() >= harmThreshold ? harmChamber : ordinaryChamber;
        ChamberVoteResult result = selected.voteOn(bill, context);
        double statusQuoBefore = context.currentPolicyPosition();
        return new BillOutcome(
                bill,
                statusQuoBefore,
                result.passed() ? bill.ideologyPosition() : statusQuoBefore,
                result.passed(),
                List.of(result),
                PresidentialAction.none(),
                result.passed() ? "passed harm-weighted threshold" : "failed harm-weighted threshold"
        );
    }
}
