package congresssim.simulation.catalog;


import congresssim.institution.bargaining.AlternativeSelectionRule;

import java.util.List;

import static congresssim.simulation.catalog.BroadSystemScenarioBuilders.majorityWithCitizenAssemblyManipulationStress;
import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.*;


/**
 * Competing-alternative and policy-tournament scenarios.
 */
final class PolicyTournamentScenarioFamily
{
	private PolicyTournamentScenarioFamily() {
	}
	
	static List<ScenarioEntry> entries() {
		return List.of(
				new ScenarioEntry("simple-majority-alternatives-pairwise", simpleMajorityWithCompetingAlternatives(
						"Unicameral majority + pairwise alternatives",
						AlternativeSelectionRule.PAIRWISE_MAJORITY,
						4,
						true
				)),
				new ScenarioEntry("simple-majority-alternatives-benefit", simpleMajorityWithCompetingAlternatives(
						"Unicameral majority + public-benefit alternatives",
						AlternativeSelectionRule.HIGHEST_PUBLIC_BENEFIT,
						4,
						true
				)),
				new ScenarioEntry("simple-majority-alternatives-support", simpleMajorityWithCompetingAlternatives(
						"Unicameral majority + public-support alternatives",
						AlternativeSelectionRule.HIGHEST_PUBLIC_SUPPORT,
						4,
						true
				)),
				new ScenarioEntry("simple-majority-alternatives-median", simpleMajorityWithCompetingAlternatives(
						"Unicameral majority + median-seeking alternatives",
						AlternativeSelectionRule.CLOSEST_TO_CHAMBER_MEDIAN,
						4,
						true
				)),
				new ScenarioEntry("simple-majority-alternatives-strategic", simpleMajorityWithStrategicAlternatives()),
				new ScenarioEntry("citizen-assembly-manipulation-stress", majorityWithCitizenAssemblyManipulationStress()),
				new ScenarioEntry("default-pass-alternatives-benefit", defaultPassWithCompetingAlternatives(
						"Default pass + public-benefit alternatives",
						AlternativeSelectionRule.HIGHEST_PUBLIC_BENEFIT,
						4,
						true
				)),
				new ScenarioEntry("default-pass-alternatives-support", defaultPassWithCompetingAlternatives(
						"Default pass + public-support alternatives",
						AlternativeSelectionRule.HIGHEST_PUBLIC_SUPPORT,
						4,
						true
				)),
				new ScenarioEntry("default-pass-alternatives-median", defaultPassWithCompetingAlternatives(
						"Default pass + median-seeking alternatives",
						AlternativeSelectionRule.CLOSEST_TO_CHAMBER_MEDIAN,
						4,
						true
				)),
				new ScenarioEntry("default-pass-alternatives-pairwise", defaultPassWithCompetingAlternatives(
						"Default pass + pairwise policy tournament",
						AlternativeSelectionRule.PAIRWISE_MAJORITY,
						4,
						true
				)),
				new ScenarioEntry("default-pass-obstruction-substitute", defaultPassWithCompetingAlternatives(
						"Default pass + obstruction-with-substitute",
						AlternativeSelectionRule.PAIRWISE_MAJORITY,
						3,
						true
				))
		);
	}
}
