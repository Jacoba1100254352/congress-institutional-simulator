package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;

final class ChallengeScoring {
    private ChallengeScoring() {
    }

    static double challengeUtility(Legislator legislator, Bill bill, VoteContext context) {
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
}

