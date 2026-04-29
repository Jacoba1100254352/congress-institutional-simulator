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
    private final double challengeThreshold;

    public ChallengeVoucherProcess(
            String name,
            List<Legislator> legislators,
            VotingStrategy votingStrategy,
            int tokensPerParty,
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
        this.tokenBank = ChallengeTokenBank.byParty(legislators, tokensPerParty);
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
            tokenBank.spend(decision.party());
            BillOutcome outcome = challengedProcess.consider(bill, context);
            return outcome.withChallenge("challenged by " + decision.party() + "; " + outcome.finalReason());
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

    private ChallengeDecision challengeDecision(Bill bill, VoteContext context) {
        String strongestParty = "";
        double strongestChallenge = Double.NEGATIVE_INFINITY;
        for (Legislator legislator : legislators) {
            if (!tokenBank.hasToken(legislator.party())) {
                continue;
            }
            double score = challengeUtility(legislator, bill, context);
            if (score > strongestChallenge) {
                strongestChallenge = score;
                strongestParty = legislator.party();
            }
        }

        if (strongestChallenge >= challengeThreshold) {
            return new ChallengeDecision(true, strongestParty);
        }
        return new ChallengeDecision(false, "");
    }

    private static double challengeUtility(Legislator legislator, Bill bill, VoteContext context) {
        double billUtility = spatialUtility(bill.ideologyPosition(), legislator.ideology());
        double statusQuoUtility = spatialUtility(context.currentPolicyPosition(), legislator.ideology());
        double ideologyLoss = Math.max(0.0, statusQuoUtility - billUtility);

        double partyPosition = context.partyPosition(legislator.party());
        double partyBillUtility = spatialUtility(bill.ideologyPosition(), partyPosition);
        double partyStatusQuoUtility = spatialUtility(context.currentPolicyPosition(), partyPosition);
        double partyLoss = Math.max(0.0, partyStatusQuoUtility - partyBillUtility);

        double lowSupportRisk = Math.max(0.0, 0.50 - bill.publicSupport()) * 2.0;
        double policyShiftRisk = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double lobbyRisk = Math.max(0.0, bill.lobbyPressure()) * (1.0 - bill.publicSupport());

        double baseScore =
                (1.35 * ideologyLoss)
                        + (0.70 * legislator.partyLoyalty() * partyLoss)
                        + (0.80 * legislator.constituencySensitivity() * lowSupportRisk)
                        + (0.45 * legislator.compromisePreference() * policyShiftRisk)
                        + (0.45 * legislator.reputationSensitivity() * lobbyRisk);
        return baseScore * (0.70 + bill.salience());
    }

    private static double spatialUtility(double policyPosition, double idealPoint) {
        double distance = policyPosition - idealPoint;
        return -(distance * distance);
    }

    private record ChallengeDecision(boolean challenged, String party) {
    }
}
