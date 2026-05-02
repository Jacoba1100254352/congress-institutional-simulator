package congresssim.simulation.catalog;
import congresssim.simulation.*;

import congresssim.institution.accountability.EligibilityDiagnosticsProcess;
import congresssim.institution.accountability.EligibilityRule;
import congresssim.institution.accountability.LawRegistryProcess;
import congresssim.institution.accountability.ProposalBondProcess;
import congresssim.institution.accountability.ProposalCreditProcess;
import congresssim.institution.accountability.QuadraticAttentionBudgetProcess;
import congresssim.institution.accountability.SunsetTrialProcess;
import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.agenda.AgendaLotteryProcess;
import congresssim.institution.agenda.ChallengeEscalationProcess;
import congresssim.institution.agenda.ChallengeTokenAllocation;
import congresssim.institution.agenda.ChallengeVoucherProcess;
import congresssim.institution.agenda.ProposalAccessProcess;
import congresssim.institution.agenda.ProposalAccessRules;
import congresssim.institution.bargaining.AlternativeSelectionRule;
import congresssim.institution.bargaining.AmendmentMediationProcess;
import congresssim.institution.bargaining.CoalitionCosponsorshipProcess;
import congresssim.institution.bargaining.CompetingAlternativesProcess;
import congresssim.institution.bargaining.MultiRoundAmendmentProcess;
import congresssim.institution.bargaining.MultidimensionalPackageBargainingProcess;
import congresssim.institution.bargaining.OmnibusBargainingProcess;
import congresssim.institution.bargaining.PackageBargainingProcess;
import congresssim.institution.chamber.BicameralConflictMode;
import congresssim.institution.chamber.BicameralOriginRule;
import congresssim.institution.chamber.BicameralProcess;
import congresssim.institution.chamber.BicameralRoutingProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberArchitectureSignalProcess;
import congresssim.institution.chamber.ConferenceCommitteeProcess;
import congresssim.institution.chamber.ConstitutionalCourtArchitectureProcess;
import congresssim.institution.chamber.DistrictPopulationProcess;
import congresssim.institution.chamber.PresidentialVetoProcess;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.committee.CommitteeGatekeepingProcess;
import congresssim.institution.committee.CommitteeInformationProcess;
import congresssim.institution.committee.CommitteePowerConfig;
import congresssim.institution.committee.CommitteePowerProcess;
import congresssim.institution.committee.CommitteeRoleMode;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.DistributionalHarmProcess;
import congresssim.institution.distribution.HarmWeightedThresholdProcess;
import congresssim.institution.lobbying.BudgetedLobbyingProcess;
import congresssim.institution.lobbying.InfluenceSystemProcess;
import congresssim.institution.lobbying.LobbyAuditProcess;
import congresssim.institution.lobbying.LobbyTransparencyProcess;
import congresssim.institution.publicinput.CitizenInitiativeProcess;
import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.publicinput.CitizenPanelReviewProcess;
import congresssim.institution.publicinput.ConstituentPublicWillProcess;
import congresssim.institution.publicinput.PublicObjectionWindowProcess;
import congresssim.institution.review.ExAnteReviewMode;
import congresssim.institution.review.ExAnteReviewProcess;
import congresssim.institution.review.IndependentInstitutionBundle;
import congresssim.institution.review.JudicialReviewProcess;
import congresssim.institution.strategy.DemocraticDeteriorationProcess;
import congresssim.institution.strategy.InstitutionalNormErosionProcess;
import congresssim.institution.strategy.LongHorizonStrategyProcess;
import congresssim.institution.strategy.ProposerStrategyProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.institution.voting.DefaultPassUnlessVetoedRule;
import congresssim.institution.voting.VotingRule;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

import static congresssim.simulation.catalog.BroadSystemScenarioBuilders.*;
import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.*;
import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.*;
import static congresssim.simulation.catalog.SharedScenarioBuilders.*;

/**
 * Core non-default and portfolio-style scenarios.
 */
final class BroadSystemScenarioFamily {
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
