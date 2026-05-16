package congresssim.simulation.catalog;


import congresssim.behavior.VotingStrategies;
import congresssim.institution.voting.AffirmativeThresholdRule;

import java.util.List;

import static congresssim.simulation.catalog.BroadSystemScenarioBuilders.*;
import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.currentSystem;
import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.stylizedCurrentCongressWorkflow;
import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.simpleMajorityWithMediation;
import static congresssim.simulation.catalog.SharedScenarioBuilders.unicameral;


/**
 * Core non-default and portfolio-style scenarios.
 */
final class BroadSystemScenarioFamily
{
	private BroadSystemScenarioFamily() {
	}
	
	static List<ScenarioEntry> entries() {
		return List.of(
				new ScenarioEntry("simple-majority", unicameral("Unicameral simple majority", AffirmativeThresholdRule.simpleMajority())),
				new ScenarioEntry("simple-majority-mediation", simpleMajorityWithMediation()),
				new ScenarioEntry("simple-majority-lobby-firewall", unicameral(
						"Unicameral majority + lobby firewall",
						AffirmativeThresholdRule.simpleMajority(),
						VotingStrategies.antiCapture()
				)),
				new ScenarioEntry("supermajority-60", unicameral("Unicameral 60 percent passage", AffirmativeThresholdRule.supermajority(0.60))),
				new ScenarioEntry("current-system", currentSystem()),
				new ScenarioEntry("current-congress-workflow", stylizedCurrentCongressWorkflow()),
				new ScenarioEntry("committee-regular-order", majorityWithCommitteeRegularOrder()),
				new ScenarioEntry("leadership-cartel-majority", leadershipCartelMajority()),
				new ScenarioEntry("cloture-conference-review", clotureConferenceAndJudicialReview()),
				new ScenarioEntry("constitutional-court-architecture-majority", majorityWithConstitutionalCourtArchitecture()),
				new ScenarioEntry("parliamentary-coalition-confidence", parliamentaryCoalitionConfidence()),
				new ScenarioEntry("citizen-initiative-referendum", citizenInitiativeReferendum()),
				new ScenarioEntry("district-population-majority", majorityWithDistrictPopulation()),
				new ScenarioEntry("public-interest-majority", majorityWithPublicInterestScreen()),
				new ScenarioEntry("citizen-assembly-threshold", majorityWithCitizenAssemblyThreshold()),
				new ScenarioEntry("random-public-review-panel-majority", majorityWithRandomPublicReviewPanel()),
				new ScenarioEntry("citizens-agenda-petition-majority", majorityWithCitizenAgendaPetitions()),
				new ScenarioEntry("open-rule-calendar-majority", majorityWithOpenRuleCalendar()),
				new ScenarioEntry("pairwise-amendment-tournament-majority", majorityWithPairwiseAmendmentTournament()),
				new ScenarioEntry("agenda-lottery-majority", majorityWithAgendaLottery(true)),
				new ScenarioEntry("quadratic-attention-majority", majorityWithQuadraticAttentionBudget()),
				new ScenarioEntry("proposal-bond-majority", majorityWithProposalBonds()),
				new ScenarioEntry("harm-weighted-majority", majorityWithHarmWeightedThreshold()),
				new ScenarioEntry("harm-weighted-loose-claims-majority", majorityWithLooseHarmClaims()),
				new ScenarioEntry("compensation-majority", majorityWithDistributionalCompensation(false)),
				new ScenarioEntry("affected-consent-majority", majorityWithDistributionalCompensation(true)),
				new ScenarioEntry("package-bargaining-majority", majorityWithPackageBargaining()),
				new ScenarioEntry("multidimensional-package-majority", majorityWithMultidimensionalPackageBargaining()),
				new ScenarioEntry("omnibus-bargaining-majority", majorityWithOmnibusBargaining()),
				new ScenarioEntry("law-registry-majority", majorityWithLawRegistry()),
				new ScenarioEntry("public-objection-majority", majorityWithPublicObjectionWindow()),
				new ScenarioEntry("public-objection-astroturf-majority", majorityWithAstroturfObjectionWindow()),
				new ScenarioEntry("anti-capture-majority-bundle", majorityWithAntiCaptureBundle()),
				new ScenarioEntry("anti-capture-access-majority", majorityWithAntiCaptureProposalAccess()),
				new ScenarioEntry("influence-system-majority", majorityWithInfluenceSystem()),
				new ScenarioEntry("risk-routed-majority", riskRoutedMajority()),
				new ScenarioEntry("portfolio-hybrid-legislature", portfolioHybridLegislature()),
				new ScenarioEntry("expanded-portfolio-hybrid-legislature", expandedPortfolioHybridLegislature()),
				new ScenarioEntry("risk-routed-no-citizen-majority", riskRoutedNoCitizenReviewMajority()),
				new ScenarioEntry("norm-erosion-majority", normErosionMajority()),
				new ScenarioEntry("long-horizon-learning-majority", longHorizonLearningMajority()),
				new ScenarioEntry("democratic-deterioration-majority", democraticDeteriorationMajority())
		);
	}
}
