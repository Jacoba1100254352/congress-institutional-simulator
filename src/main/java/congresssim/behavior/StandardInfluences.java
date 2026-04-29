package congresssim.behavior;

import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

public final class StandardInfluences {
    private StandardInfluences() {
    }

    public static VoteInfluence ideology(double weight) {
        return new NamedVoteInfluence("ideology", (legislator, bill, context) -> {
            double billUtility = spatialUtility(bill.ideologyPosition(), legislator.ideology());
            double statusQuoUtility = spatialUtility(context.currentPolicyPosition(), legislator.ideology());
            return weight * (billUtility - statusQuoUtility) * (0.75 + bill.salience());
        });
    }

    public static VoteInfluence party(double weight) {
        return new NamedVoteInfluence("party", (legislator, bill, context) -> {
            double partyPosition = context.partyPosition(legislator.party());
            double billUtility = spatialUtility(bill.ideologyPosition(), partyPosition);
            double statusQuoUtility = spatialUtility(context.currentPolicyPosition(), partyPosition);
            return weight * legislator.partyLoyalty() * (billUtility - statusQuoUtility);
        });
    }

    public static VoteInfluence constituency(double weight) {
        return new NamedVoteInfluence("constituency", (legislator, bill, context) -> {
            double pressure = (bill.publicSupport() - 0.5) * 2.0;
            return weight * legislator.constituencySensitivity() * pressure;
        });
    }

    public static VoteInfluence lobbying(double weight) {
        return new NamedVoteInfluence("lobbying", (legislator, bill, context) ->
                weight * legislator.lobbySensitivity() * bill.lobbyPressure());
    }

    public static VoteInfluence compromise(double weight) {
        return new NamedVoteInfluence("compromise", (legislator, bill, context) -> {
            double moderation = 1.0 - Math.abs(bill.ideologyPosition());
            double policyShift = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
            double incrementalism = 1.0 - policyShift;
            double publicLegitimacy = Values.clamp((bill.publicSupport() - 0.35) / 0.65, 0.0, 1.0);
            double compromiseSignal = (0.45 * moderation) + (0.35 * publicLegitimacy) + (0.20 * incrementalism);
            return weight * legislator.compromisePreference() * compromiseSignal;
        });
    }

    public static VoteInfluence reputation(double weight) {
        return new NamedVoteInfluence("reputation", (legislator, bill, context) -> {
            double unpopularBillCost = Math.min(0.0, (bill.publicSupport() - 0.5) * 2.0);
            double lobbyCaptureCost = bill.lobbyPressure() > 0.55 && bill.publicSupport() < 0.45 ? -0.35 : 0.0;
            return weight * legislator.reputationSensitivity() * (unpopularBillCost + lobbyCaptureCost);
        });
    }

    private record NamedVoteInfluence(String name, InfluenceFunction function) implements VoteInfluence {
        @Override
        public double score(Legislator legislator, Bill bill, VoteContext context) {
            return function.score(legislator, bill, context);
        }
    }

    @FunctionalInterface
    private interface InfluenceFunction {
        double score(Legislator legislator, Bill bill, VoteContext context);
    }

    private static double spatialUtility(double policyPosition, double idealPoint) {
        double distance = policyPosition - idealPoint;
        return -(distance * distance);
    }
}
