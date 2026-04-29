package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.Vote;

public final class PresidentialVetoProcess implements LegislativeProcess {
    private final LegislativeProcess innerProcess;
    private final Legislator president;
    private final VotingStrategy votingStrategy;
    private final double consensusSafeHarbor;
    private final VotingRule overrideRule;

    public PresidentialVetoProcess(
            LegislativeProcess innerProcess,
            Legislator president,
            VotingStrategy votingStrategy,
            double consensusSafeHarbor,
            VotingRule overrideRule
    ) {
        this.innerProcess = innerProcess;
        this.president = president;
        this.votingStrategy = votingStrategy;
        this.consensusSafeHarbor = consensusSafeHarbor;
        this.overrideRule = overrideRule;
    }

    @Override
    public String name() {
        return innerProcess.name() + " + presidential veto";
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        BillOutcome preliminary = innerProcess.consider(bill, context);
        if (!preliminary.enacted()) {
            return preliminary;
        }

        Vote presidentVote = votingStrategy.vote(president, bill, context);
        boolean safeHarbor = preliminary.averageYayShare() >= consensusSafeHarbor;
        if (presidentVote == Vote.YAY || safeHarbor) {
            return new BillOutcome(
                    bill,
                    preliminary.statusQuoBefore(),
                    bill.ideologyPosition(),
                    true,
                    preliminary.agendaDisposition(),
                    preliminary.gateResults(),
                    preliminary.chamberResults(),
                    PresidentialAction.none(),
                    preliminary.challenged(),
                    preliminary.signals(),
                    "enacted without veto"
            );
        }

        boolean overridden = preliminary.chamberResults()
                .stream()
                .allMatch(result -> overrideRule.passes(result.yayCount(), result.nayCount()));
        return new BillOutcome(
                bill,
                preliminary.statusQuoBefore(),
                overridden ? bill.ideologyPosition() : preliminary.statusQuoBefore(),
                overridden,
                preliminary.agendaDisposition(),
                preliminary.gateResults(),
                preliminary.chamberResults(),
                new PresidentialAction(true, true, overridden),
                preliminary.challenged(),
                preliminary.signals(),
                overridden ? "veto overridden" : "presidential veto sustained"
        );
    }
}
