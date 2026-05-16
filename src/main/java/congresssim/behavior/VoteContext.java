package congresssim.behavior;


import java.util.Map;
import java.util.Random;


public record VoteContext(Map<String, Double> partyPositions, Random random, double currentPolicyPosition)
{
	public VoteContext(Map<String, Double> partyPositions, Random random, double currentPolicyPosition) {
		this.partyPositions = Map.copyOf(partyPositions);
		this.random = random;
		this.currentPolicyPosition = currentPolicyPosition;
	}
	
	public double partyPosition(String party) {
		return partyPositions.getOrDefault(party, 0.0);
	}
}
