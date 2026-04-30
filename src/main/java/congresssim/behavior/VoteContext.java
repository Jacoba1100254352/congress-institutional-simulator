package congresssim.behavior;

import java.util.Map;
import java.util.Random;

public final class VoteContext {
    private final Map<String, Double> partyPositions;
    private final Random random;
    private final double currentPolicyPosition;

    public VoteContext(Map<String, Double> partyPositions, Random random, double currentPolicyPosition) {
        this.partyPositions = Map.copyOf(partyPositions);
        this.random = random;
        this.currentPolicyPosition = currentPolicyPosition;
    }

    public double partyPosition(String party) {
        return partyPositions.getOrDefault(party, 0.0);
    }

    public Map<String, Double> partyPositions() {
        return partyPositions;
    }

    public Random random() {
        return random;
    }

    public double currentPolicyPosition() {
        return currentPolicyPosition;
    }
}
