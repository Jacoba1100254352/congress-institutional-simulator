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
 * Historical default-pass stress, challenge, cost, committee, and information variants.
 */
final class DefaultPassStressScenarioFamily {
    private DefaultPassStressScenarioFamily() {
    }

    static List<ScenarioEntry> entries() {
        return List.of(
                new ScenarioEntry("default-pass-challenge", defaultPassWithChallengeVouchers()),
                new ScenarioEntry("default-pass-challenge-info", defaultPassWithChallengeVouchersAndInformation()),
                new ScenarioEntry("default-pass-cross-bloc", defaultPassWithCrossBlocCosponsorship(
                "Default pass + cross-bloc cosponsors",
                2,
                1,
                0.12,
                0.52
                )),
                new ScenarioEntry("default-pass-cross-bloc-strong", defaultPassWithCrossBlocCosponsorship(
                "Default pass + strong cross-bloc cosponsors",
                6,
                1,
                0.20,
                0.58
                )),
                new ScenarioEntry("default-pass-cross-bloc-challenge", defaultPassWithCrossBlocCosponsorshipAndChallenge()),
                new ScenarioEntry("default-pass-adaptive-track", defaultPassWithAdaptiveTrack(false)),
                new ScenarioEntry("default-pass-adaptive-track-challenge", defaultPassWithAdaptiveTrack(true)),
                new ScenarioEntry("default-pass-sunset-trial", defaultPassWithSunsetTrial(false)),
                new ScenarioEntry("default-pass-sunset-challenge", defaultPassWithSunsetTrial(true)),
                new ScenarioEntry("default-pass-law-registry", defaultPassWithLawRegistry(false)),
                new ScenarioEntry("default-pass-law-registry-challenge", defaultPassWithLawRegistry(true)),
                new ScenarioEntry("default-pass-earned-credits", defaultPassWithProposalCredits(false)),
                new ScenarioEntry("default-pass-earned-credits-challenge", defaultPassWithProposalCredits(true)),
                new ScenarioEntry("default-pass-challenge-party-t3-s082", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=3 s=.82",
                ChallengeTokenAllocation.PARTY,
                3,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t6-s082", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=6 s=.82",
                ChallengeTokenAllocation.PARTY,
                6,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t15-s082", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=15 s=.82",
                ChallengeTokenAllocation.PARTY,
                15,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-t25-s082", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=25 s=.82",
                ChallengeTokenAllocation.PARTY,
                25,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-party-proportional", defaultPassWithChallengeVouchers(
                "Default pass + proportional party challenge vouchers",
                ChallengeTokenAllocation.PARTY_PROPORTIONAL,
                10,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-minority-bonus", defaultPassWithChallengeVouchers(
                "Default pass + minority-bonus challenge vouchers",
                ChallengeTokenAllocation.PARTY_MINORITY_BONUS,
                8,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-supermajority", defaultPassWithChallengePath(
                "Default pass + challenge to 60 percent vote",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                ChallengePath.SUPERMAJORITY
                )),
                new ScenarioEntry("default-pass-challenge-committee", defaultPassWithChallengePath(
                "Default pass + challenge to committee review",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                ChallengePath.COMMITTEE_REVIEW
                )),
                new ScenarioEntry("default-pass-challenge-info-active", defaultPassWithChallengePath(
                "Default pass + challenge to info + active vote",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                ChallengePath.INFORMATION_PLUS_ACTIVE
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s050", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=10 s=.50",
                ChallengeTokenAllocation.PARTY,
                10,
                0.50
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s065", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=10 s=.65",
                ChallengeTokenAllocation.PARTY,
                10,
                0.65
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s100", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=10 s=1.00",
                ChallengeTokenAllocation.PARTY,
                10,
                1.00
                )),
                new ScenarioEntry("default-pass-challenge-party-t10-s125", defaultPassWithChallengeVouchers(
                "Default pass + party challenge vouchers t=10 s=1.25",
                ChallengeTokenAllocation.PARTY,
                10,
                1.25
                )),
                new ScenarioEntry("default-pass-challenge-member-t1-s082", defaultPassWithChallengeVouchers(
                "Default pass + member challenge vouchers t=1 s=.82",
                ChallengeTokenAllocation.LEGISLATOR,
                1,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-member-t2-s082", defaultPassWithChallengeVouchers(
                "Default pass + member challenge vouchers t=2 s=.82",
                ChallengeTokenAllocation.LEGISLATOR,
                2,
                0.82
                )),
                new ScenarioEntry("default-pass-challenge-member-t3-s082", defaultPassWithChallengeVouchers(
                "Default pass + member challenge vouchers t=3 s=.82",
                ChallengeTokenAllocation.LEGISLATOR,
                3,
                0.82
                )),
                new ScenarioEntry("default-pass-escalation-q6-s082", defaultPassWithChallengeEscalation(
                "Default pass + q=6 challenge escalation s=.82",
                6,
                0.82
                )),
                new ScenarioEntry("default-pass-escalation-q12-s082", defaultPassWithChallengeEscalation(
                "Default pass + q=12 challenge escalation s=.82",
                12,
                0.82
                )),
                new ScenarioEntry("default-pass-escalation-q20-s082", defaultPassWithChallengeEscalation(
                "Default pass + q=20 challenge escalation s=.82",
                20,
                0.82
                )),
                new ScenarioEntry("default-pass-access", defaultPassWithProposalAccess()),
                new ScenarioEntry("default-pass-cost", defaultPassWithProposalCost()),
                new ScenarioEntry("default-pass-cost-guarded", defaultPassWithCostAndGuardrails()),
                new ScenarioEntry("default-pass-committee", defaultPassWithCommitteeGate(
                "Default pass + representative committee gate",
                CommitteeComposition.REPRESENTATIVE
                )),
                new ScenarioEntry("default-pass-committee-majority", defaultPassWithCommitteeGate(
                "Default pass + majority-controlled committee",
                CommitteeComposition.MAJORITY_CONTROLLED
                )),
                new ScenarioEntry("default-pass-committee-polarized", defaultPassWithCommitteeGate(
                "Default pass + polarized committee",
                CommitteeComposition.POLARIZED
                )),
                new ScenarioEntry("default-pass-committee-captured", defaultPassWithCommitteeGate(
                "Default pass + captured committee",
                CommitteeComposition.CAPTURED
                )),
                new ScenarioEntry("default-pass-info", defaultPassWithInformation(
                "Default pass + representative committee info",
                CommitteeComposition.REPRESENTATIVE,
                false
                )),
                new ScenarioEntry("default-pass-info-expert", defaultPassWithInformation(
                "Default pass + expert committee info",
                CommitteeComposition.EXPERT,
                false
                )),
                new ScenarioEntry("default-pass-info-captured", defaultPassWithInformation(
                "Default pass + captured committee info",
                CommitteeComposition.CAPTURED,
                false
                )),
                new ScenarioEntry("default-pass-guarded", defaultPassWithAccessAndCommitteeGate()),
                new ScenarioEntry("default-pass-informed-guarded", defaultPassWithInformation(
                "Default pass + informed guarded committee",
                CommitteeComposition.REPRESENTATIVE,
                true
                ))
        );
    }
}
