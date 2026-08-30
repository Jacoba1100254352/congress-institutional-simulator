package congresssim.institution.adversary;


import java.util.List;


public record AdversarySpec(
		String id,
		String name,
		String actorType,
		String objective,
		List<InformationLevel> informationLevels,
		List<String> budgetUnits,
		List<String> strategySet,
		String successMetric,
		String degradationMetric
)
{
	public AdversarySpec {
		if (id == null || id.isBlank()) {
			throw new IllegalArgumentException("Adversary id is required.");
		}
		if (name == null || name.isBlank()) {
			throw new IllegalArgumentException("Adversary name is required.");
		}
		if (actorType == null || actorType.isBlank()) {
			throw new IllegalArgumentException("Actor type is required.");
		}
		if (objective == null || objective.isBlank()) {
			throw new IllegalArgumentException("Objective is required.");
		}
		if (successMetric == null || successMetric.isBlank()) {
			throw new IllegalArgumentException("Success metric is required.");
		}
		if (degradationMetric == null || degradationMetric.isBlank()) {
			throw new IllegalArgumentException("Degradation metric is required.");
		}
		informationLevels = List.copyOf(informationLevels);
		budgetUnits = List.copyOf(budgetUnits);
		strategySet = List.copyOf(strategySet);
		if (informationLevels.isEmpty()) {
			throw new IllegalArgumentException("At least one information level is required.");
		}
		if (budgetUnits.isEmpty()) {
			throw new IllegalArgumentException("At least one budget unit is required.");
		}
		if (strategySet.isEmpty()) {
			throw new IllegalArgumentException("At least one strategy action is required.");
		}
	}

	public String label() {
		return id + " " + name;
	}
}
