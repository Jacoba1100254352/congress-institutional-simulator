package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Bill;
import congresssim.model.Legislator;

import java.util.List;

public final class ChallengeEscalationProcess implements LegislativeProcess {
    private final String name;
    private final List<Legislator> legislators;
    private final Chamber supportProbe;
    private final LegislativeProcess challengedProcess;
    private final int minimumChallengers;
    private final double challengeThreshold;

    public ChallengeEscalationProcess(
            String name,
            List<Legislator> legislators,
            VotingStrategy votingStrategy,
            int minimumChallengers,
            double challengeThreshold,
            LegislativeProcess challengedProcess
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (minimumChallengers < 1) {
            throw new IllegalArgumentException("minimumChallengers must be positive.");
        }
        if (minimumChallengers > legislators.size()) {
            throw new IllegalArgumentException("minimumChallengers must not exceed the chamber size.");
        }
        if (challengeThreshold < 0.0) {
            throw new IllegalArgumentException("challengeThreshold must not be negative.");
        }
        this.name = name;
        this.legislators = List.copyOf(legislators);
        this.supportProbe = new Chamber(
                "Challenge support probe",
                legislators,
                votingStrategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        this.challengedProcess = challengedProcess;
        this.minimumChallengers = minimumChallengers;
        this.challengeThreshold = challengeThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        int challengers = 0;
        for (Legislator legislator : legislators) {
            if (ChallengeScoring.challengeUtility(legislator, bill, context) >= challengeThreshold) {
                challengers++;
            }
        }

        if (challengers >= minimumChallengers) {
            BillOutcome outcome = challengedProcess.consider(bill, context);
            return outcome.withChallenge("escalated by " + challengers + " challengers; " + outcome.finalReason());
        }

        ChamberVoteResult supportResult = supportProbe.voteOn(bill, context);
        double statusQuoBefore = context.currentPolicyPosition();
        return new BillOutcome(
                bill,
                statusQuoBefore,
                bill.ideologyPosition(),
                true,
                List.of(supportResult),
                PresidentialAction.none(),
                "unchallenged default enactment"
        );
    }
}
