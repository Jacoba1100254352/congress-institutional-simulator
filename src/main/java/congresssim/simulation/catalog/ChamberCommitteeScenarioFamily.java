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
 * Chamber architecture, committee power, eligibility, and ex ante review scenarios.
 */
final class ChamberCommitteeScenarioFamily {
    private ChamberCommitteeScenarioFamily() {
    }

    static List<ScenarioEntry> entries() {
        return List.of(
                new ScenarioEntry("bicameral-majority", bicameral("Bicameral simple majority", AffirmativeThresholdRule.simpleMajority())),
                new ScenarioEntry("chamber-incongruence-pr-upper", chamberArchitecture(
                "Bicameral incongruence: district House + PR upper house",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.proportionalHouse(35, 7, 0.04),
                AffirmativeThresholdRule.simpleMajority(),
                false
                )),
                new ScenarioEntry("malapportioned-upper-chamber", chamberArchitecture(
                "Bicameral malapportioned territorial upper chamber",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.82),
                AffirmativeThresholdRule.simpleMajority(),
                false
                )),
                new ScenarioEntry("appointed-upper-chamber", chamberArchitecture(
                "Bicameral mixed appointed upper chamber",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.appointedUpperHouse(35, 0.55),
                AffirmativeThresholdRule.simpleMajority(),
                false
                )),
                new ScenarioEntry("asymmetric-senate-cloture", chamberArchitecture(
                "Bicameral House majority + upper cloture",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.50),
                AffirmativeThresholdRule.supermajority(0.60),
                false
                )),
                new ScenarioEntry("conference-malapportioned-upper", chamberArchitecture(
                "Bicameral malapportioned upper chamber + conference",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.72),
                AffirmativeThresholdRule.simpleMajority(),
                true
                )),
                new ScenarioEntry("revision-council-upper", chamberRouting(
                "Bicameral upper revision council",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.proportionalHouse(35, 7, 0.04),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.REVISION_COUNCIL
                )),
                new ScenarioEntry("suspensive-veto-upper", chamberRouting(
                "Bicameral upper suspensive veto",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.64),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.SUSPENSIVE_VETO
                )),
                new ScenarioEntry("limited-navette-upper", chamberRouting(
                "Bicameral limited navette",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.64),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.REVENUE_LOWER,
                BicameralConflictMode.LIMITED_NAVETTE
                )),
                new ScenarioEntry("joint-sitting-upper", chamberRouting(
                "Bicameral joint-sitting fallback",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.64),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.HIGH_RISK_UPPER_PRECLEARANCE,
                BicameralConflictMode.JOINT_SITTING
                )),
                new ScenarioEntry("balanced-committee-majority", majorityWithCommitteeComposition(
                "Majority + forced-balanced committee",
                CommitteeComposition.FORCED_PARTY_BALANCE
                )),
                new ScenarioEntry("lottery-committee-majority", majorityWithCommitteeComposition(
                "Majority + random-lottery committee",
                CommitteeComposition.RANDOM_LOTTERY
                )),
                new ScenarioEntry("expert-lottery-committee-majority", majorityWithCommitteeComposition(
                "Majority + expertise-qualified lottery committee",
                CommitteeComposition.EXPERTISE_QUALIFIED_LOTTERY
                )),
                new ScenarioEntry("opposition-chaired-committee-majority", majorityWithCommitteeComposition(
                "Majority + opposition-chaired scrutiny committee",
                CommitteeComposition.OPPOSITION_CHAIRED
                )),
                new ScenarioEntry("committee-deadline-discharge-majority", majorityWithCommitteePower(
                "Committee deadline + discharge petition",
                CommitteeComposition.MAJORITY_CONTROLLED,
                0.58,
                0.72,
                0.28,
                0.48
                )),
                new ScenarioEntry("committee-minority-hearing-majority", majorityWithCommitteePower(
                "Committee minority-hearing rights",
                CommitteeComposition.MINORITY_PROTECTED,
                0.64,
                0.62,
                0.36,
                0.34
                )),
                new ScenarioEntry("committee-amendment-majority", majorityWithCommitteePower(
                "Committee amendment and revision power",
                CommitteeComposition.ISSUE_EXPERT,
                0.66,
                0.54,
                0.68,
                0.42
                )),
                new ScenarioEntry("equal-population-unicameral", chamberUnicameral(
                "Equal-population unicameral chamber",
                ChamberSpec.lowerHouse(101),
                AffirmativeThresholdRule.simpleMajority()
                )),
                new ScenarioEntry("proportional-house-majority", chamberUnicameral(
                "Proportional lower-house majority",
                ChamberSpec.proportionalHouse(101, 9, 0.035),
                AffirmativeThresholdRule.simpleMajority()
                )),
                new ScenarioEntry("house-origin-routing", chamberRouting(
                "House-origin-only bicameral routing",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.52),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.HOUSE_ORIGIN_ONLY,
                BicameralConflictMode.REVISION_COUNCIL
                )),
                new ScenarioEntry("senate-origin-routing", chamberRouting(
                "Senate-origin-only bicameral routing",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.64),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.SENATE_ORIGIN_ONLY,
                BicameralConflictMode.REVISION_COUNCIL
                )),
                new ScenarioEntry("emergency-lower-fast-routing", chamberRouting(
                "Emergency lower-house fast path",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.46),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.EMERGENCY_LOWER_FAST,
                BicameralConflictMode.SUSPENSIVE_VETO
                )),
                new ScenarioEntry("proposer-chamber-origin-routing", chamberRouting(
                "Proposer-chamber origin routing",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.appointedUpperHouse(35, 0.40),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.PROPOSER_CHAMBER,
                BicameralConflictMode.LIMITED_NAVETTE
                )),
                new ScenarioEntry("leadership-routed-origin", chamberRouting(
                "Leadership-routed chamber origin",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.58),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LEADERSHIP_ROUTED,
                BicameralConflictMode.SECOND_CHAMBER_KILL
                )),
                new ScenarioEntry("principles-resolution-routing", chamberRouting(
                "Principles resolution before second-chamber drafting",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.proportionalHouse(35, 7, 0.04),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.PRINCIPLES_RESOLUTION_FIRST,
                BicameralConflictMode.MEDIATION_COMMITTEE
                )),
                new ScenarioEntry("second-chamber-preclearance", chamberRouting(
                "Second-chamber preclearance routing",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.70),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.SECOND_CHAMBER_PRECLEARANCE,
                BicameralConflictMode.JOINT_SITTING
                )),
                new ScenarioEntry("upper-amendment-only", chamberRouting(
                "Upper-house amendment-only power",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.48),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.SECOND_CHAMBER_AMENDMENT
                )),
                new ScenarioEntry("upper-absolute-veto", chamberRouting(
                "Upper-house absolute veto",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.72),
                AffirmativeThresholdRule.supermajority(0.60),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.SECOND_CHAMBER_KILL
                )),
                new ScenarioEntry("upper-territorial-veto", chamberRouting(
                "Upper-house territorial veto threshold",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.88),
                AffirmativeThresholdRule.supermajority(0.62),
                BicameralOriginRule.REVENUE_LOWER,
                BicameralConflictMode.SUSPENSIVE_VETO
                )),
                new ScenarioEntry("mediation-committee-upper", chamberRouting(
                "Mediation committee bicameral conflict",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.proportionalHouse(35, 7, 0.04),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.MEDIATION_COMMITTEE
                )),
                new ScenarioEntry("last-offer-bargaining-upper", chamberRouting(
                "Last-offer bicameral bargaining",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.62),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.REVENUE_LOWER,
                BicameralConflictMode.LAST_OFFER_BARGAINING
                )),
                new ScenarioEntry("lower-override-upper", chamberRouting(
                "Lower-house override after bicameral disagreement",
                ChamberSpec.lowerHouse(101),
                ChamberSpec.territorialUpperHouse(35, 0.68),
                AffirmativeThresholdRule.simpleMajority(),
                BicameralOriginRule.LOWER_FIRST,
                BicameralConflictMode.LOWER_OVERRIDE_AFTER_DISAGREEMENT
                )),
                new ScenarioEntry("minority-veto-committee-majority", majorityWithCommitteeComposition(
                "Majority + minority-veto committee seat",
                CommitteeComposition.MINORITY_VETO_HIGH_RISK
                )),
                new ScenarioEntry("mixed-citizen-committee-majority", majorityWithConfiguredCommittee(
                "Majority + mixed legislator-citizen committee",
                new CommitteeSelectionConfig(
                "general",
                818L,
                CommitteeQuotaRule.FORCED_BALANCE,
                0.28,
                0.26,
                0.10,
                2,
                ChairAllocationRule.ROTATING,
                0.50,
                0.35,
                true,
                19
                ),
                CommitteePowerConfig.standard()
                )),
                new ScenarioEntry("committee-priority-queue-majority", majorityWithCommitteeRole(
                "Committee priority queue",
                CommitteeRoleMode.PRIORITY_QUEUE,
                CommitteeComposition.PROPORTIONAL_PARTY,
                0.48,
                0.24,
                0.68,
                0.70,
                0.14,
                0.30
                )),
                new ScenarioEntry("committee-veto-player-majority", majorityWithCommitteeRole(
                "Committee veto player",
                CommitteeRoleMode.VETO_PLAYER,
                CommitteeComposition.MAJORITY_CONTROLLED,
                0.60,
                0.72,
                0.54,
                0.38,
                0.18,
                0.50
                )),
                new ScenarioEntry("committee-fast-track-certifier-majority", majorityWithCommitteeRole(
                "Committee fast-track certifier",
                CommitteeRoleMode.FAST_TRACK_CERTIFIER,
                CommitteeComposition.EXPERTISE_QUALIFIED_LOTTERY,
                0.50,
                0.20,
                0.76,
                0.82,
                0.16,
                0.28
                )),
                new ScenarioEntry("committee-scrutiny-audit-majority", majorityWithCommitteeRole(
                "Committee scrutiny and audit",
                CommitteeRoleMode.SCRUTINY_AUDIT,
                CommitteeComposition.OPPOSITION_CHAIRED,
                0.54,
                0.28,
                0.74,
                0.56,
                0.28,
                0.22
                )),
                new ScenarioEntry("committee-public-accounts-majority", majorityWithCommitteeRole(
                "Public-accounts committee",
                CommitteeRoleMode.PUBLIC_ACCOUNTS,
                CommitteeComposition.PUBLIC_ACCOUNTS_STYLE,
                0.52,
                0.18,
                0.72,
                0.60,
                0.22,
                0.20
                )),
                new ScenarioEntry("committee-legal-drafting-majority", majorityWithCommitteeRole(
                "Legal and drafting-quality committee",
                CommitteeRoleMode.LEGAL_DRAFTING_REVIEW,
                CommitteeComposition.INDEPENDENT_EXPERT,
                0.50,
                0.14,
                0.82,
                0.64,
                0.20,
                0.18
                )),
                new ScenarioEntry("committee-discharge-target-majority", majorityWithCommitteeRole(
                "Committee discharge-petition target",
                CommitteeRoleMode.DISCHARGE_TARGET,
                CommitteeComposition.MINORITY_PROTECTED,
                0.58,
                0.38,
                0.64,
                0.44,
                0.20,
                0.30
                )),
                new ScenarioEntry("eligibility-expertise-majority", eligibilityFilteredMajority(
                "Expertise eligibility filter",
                EligibilityRule.expertiseMajority(),
                false
                )),
                new ScenarioEntry("appointment-retention-majority", eligibilityFilteredMajority(
                "Appointment and retention eligibility filter",
                EligibilityRule.appointmentRetention(),
                true
                )),
                new ScenarioEntry("recusal-cooling-off-majority", eligibilityFilteredMajority(
                "Recusal and cooling-off eligibility filter",
                EligibilityRule.recusalCoolingOff(),
                false
                )),
                new ScenarioEntry("exante-advisory-majority", exAnteReviewMajority(
                "Ex ante advisory review",
                ExAnteReviewMode.ADVISORY_OPINION,
                IndependentInstitutionBundle.advisoryFiscalLegal(),
                0.52,
                0.62
                )),
                new ScenarioEntry("exante-clearance-majority", exAnteReviewMajority(
                "Mandatory ex ante legal clearance",
                ExAnteReviewMode.MANDATORY_CLEARANCE,
                IndependentInstitutionBundle.advisoryFiscalLegal(),
                0.54,
                0.68
                )),
                new ScenarioEntry("independent-insulation-majority", exAnteReviewMajority(
                "Independent fiscal/electoral/audit insulation bundle",
                ExAnteReviewMode.DEADLINE_LIMITED,
                IndependentInstitutionBundle.strongInsulation(),
                0.50,
                0.64
                )),
                new ScenarioEntry("presidential-veto", presidentialVeto())
        );
    }
}
