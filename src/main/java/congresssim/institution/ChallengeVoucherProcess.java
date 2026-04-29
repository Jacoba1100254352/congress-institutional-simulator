package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Bill;
import congresssim.model.Legislator;

import java.util.List;

public final class ChallengeVoucherProcess implements LegislativeProcess {
    private final String name;
    private final List<Legislator> legislators;
    private final Chamber supportProbe;
    private final LegislativeProcess challengedProcess;
    private final ChallengeTokenBank tokenBank;
    private final ChallengeTokenAllocation allocation;
    private final double challengeThreshold;

    public ChallengeVoucherProcess(
            String name,
            List<Legislator> legislators,
            VotingStrategy votingStrategy,
            int tokensPerParty,
            double challengeThreshold,
            LegislativeProcess challengedProcess
    ) {
        this(
                name,
                legislators,
                votingStrategy,
                ChallengeTokenAllocation.PARTY,
                tokensPerParty,
                challengeThreshold,
                challengedProcess
        );
    }

    public ChallengeVoucherProcess(
            String name,
            List<Legislator> legislators,
            VotingStrategy votingStrategy,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner,
            double challengeThreshold,
            LegislativeProcess challengedProcess
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
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
        this.allocation = allocation;
        this.tokenBank = ChallengeTokenBank.create(legislators, allocation, tokensPerOwner);
        this.challengeThreshold = challengeThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ChallengeDecision decision = challengeDecision(bill, context);
        if (decision.challenged()) {
            tokenBank.spend(decision.owner());
            BillOutcome outcome = challengedProcess.consider(bill, context);
            return outcome.withChallenge("challenged by " + decision.label() + "; " + outcome.finalReason());
        }

        ChamberVoteResult supportResult = supportProbe.voteOn(bill, context);
        double statusQuoBefore = context.currentPolicyPosition();
        boolean falseNegativePass = badBillPassedUnchallenged(bill, supportResult);
        return new BillOutcome(
                bill,
                statusQuoBefore,
                bill.ideologyPosition(),
                true,
                List.of(supportResult),
                PresidentialAction.none(),
                "unchallenged default enactment"
        ).withSignals(OutcomeSignals.challengeDiagnostics(decision.tokenExhausted(), falseNegativePass));
    }

    private ChallengeDecision challengeDecision(Bill bill, VoteContext context) {
        String strongestOwner = "";
        String strongestLabel = "";
        double strongestChallenge = Double.NEGATIVE_INFINITY;
        double strongestAnyChallenge = Double.NEGATIVE_INFINITY;
        for (Legislator legislator : legislators) {
            double score = ChallengeScoring.challengeUtility(legislator, bill, context);
            if (score > strongestAnyChallenge) {
                strongestAnyChallenge = score;
            }
            String owner = allocation.ownerOf(legislator);
            if (!tokenBank.hasToken(owner)) {
                continue;
            }
            if (score > strongestChallenge) {
                strongestChallenge = score;
                strongestOwner = owner;
                strongestLabel = allocation.labelFor(legislator);
            }
        }

        if (strongestChallenge >= challengeThreshold) {
            return new ChallengeDecision(true, strongestOwner, strongestLabel, false);
        }
        return new ChallengeDecision(false, "", "", strongestAnyChallenge >= challengeThreshold);
    }

    private static boolean badBillPassedUnchallenged(Bill bill, ChamberVoteResult supportResult) {
        return supportResult.yayShare() < 0.50
                || bill.publicSupport() < 0.42
                || bill.publicBenefit() < 0.36
                || AffectedGroupScoring.minorityHarm(bill) > 0.18;
    }

    private record ChallengeDecision(boolean challenged, String owner, String label, boolean tokenExhausted) {
    }
}
