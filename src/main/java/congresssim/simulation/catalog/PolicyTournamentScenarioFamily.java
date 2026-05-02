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
 * Competing-alternative and policy-tournament scenarios.
 */
final class PolicyTournamentScenarioFamily {
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
