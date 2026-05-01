package congresssim.simulation;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaLotteryProcess;
import congresssim.institution.AlternativeSelectionRule;
import congresssim.institution.AmendmentMediationProcess;
import congresssim.institution.BicameralProcess;
import congresssim.institution.BicameralConflictMode;
import congresssim.institution.BicameralOriginRule;
import congresssim.institution.BicameralRoutingProcess;
import congresssim.institution.BudgetedLobbyingProcess;
import congresssim.institution.Chamber;
import congresssim.institution.ChamberArchitectureSignalProcess;
import congresssim.institution.ChallengeEscalationProcess;
import congresssim.institution.ChallengeTokenAllocation;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CitizenPanelMode;
import congresssim.institution.CitizenPanelReviewProcess;
import congresssim.institution.CitizenInitiativeProcess;
import congresssim.institution.CoalitionCosponsorshipProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.CommitteePowerConfig;
import congresssim.institution.CommitteePowerProcess;
import congresssim.institution.CommitteeRoleMode;
import congresssim.institution.CompetingAlternativesProcess;
import congresssim.institution.ConferenceCommitteeProcess;
import congresssim.institution.ConstituentPublicWillProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.DemocraticDeteriorationProcess;
import congresssim.institution.DistributionalHarmProcess;
import congresssim.institution.EligibilityDiagnosticsProcess;
import congresssim.institution.EligibilityRule;
import congresssim.institution.ExAnteReviewMode;
import congresssim.institution.ExAnteReviewProcess;
import congresssim.institution.HarmWeightedThresholdProcess;
import congresssim.institution.IndependentInstitutionBundle;
import congresssim.institution.InstitutionalNormErosionProcess;
import congresssim.institution.JudicialReviewProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.MultiRoundAmendmentProcess;
import congresssim.institution.MultidimensionalPackageBargainingProcess;
import congresssim.institution.OutcomeSignals;
import congresssim.institution.PackageBargainingProcess;
import congresssim.institution.PresidentialVetoProcess;
import congresssim.institution.ProposalAccessProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalBondProcess;
import congresssim.institution.ProposalCreditProcess;
import congresssim.institution.ProposerStrategyProcess;
import congresssim.institution.PublicObjectionWindowProcess;
import congresssim.institution.QuadraticAttentionBudgetProcess;
import congresssim.institution.SunsetTrialProcess;
import congresssim.institution.UnicameralProcess;
import congresssim.institution.VotingRule;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

public final class ScenarioCatalog {
    private static final List<String> DEFAULT_SCENARIO_KEYS = List.of(
            "current-system",
            "simple-majority",
            "supermajority-60",
            "bicameral-majority",
            "presidential-veto",
            "leadership-cartel-majority",
            "committee-regular-order",
            "cloture-conference-review",
            "parliamentary-coalition-confidence",
            "citizen-initiative-referendum",
            "simple-majority-alternatives-pairwise",
            "citizen-assembly-threshold",
            "public-interest-majority",
            "agenda-lottery-majority",
            "quadratic-attention-majority",
            "proposal-bond-majority",
            "harm-weighted-majority",
            "compensation-majority",
            "package-bargaining-majority",
            "multidimensional-package-majority",
            "law-registry-majority",
            "public-objection-majority",
            "anti-capture-majority-bundle",
            "risk-routed-majority",
            "portfolio-hybrid-legislature",
            "norm-erosion-majority",
            "default-pass",
            "default-pass-challenge",
            "default-pass-multiround-mediation-challenge"
    );

    private ScenarioCatalog() {
    }

    public static List<Scenario> defaultScenarios() {
        return scenariosForKeys(DEFAULT_SCENARIO_KEYS);
    }

    public static List<String> defaultScenarioKeys() {
        return DEFAULT_SCENARIO_KEYS;
    }

    public static List<Scenario> allScenarios() {
        return entries().stream()
                .filter(entry -> isBreadthCatalogKey(entry.key()))
                .map(ScenarioEntry::scenario)
                .toList();
    }

    public static List<String> allScenarioKeys() {
        return entries().stream()
                .map(ScenarioEntry::key)
                .filter(ScenarioCatalog::isBreadthCatalogKey)
                .toList();
    }

    public static List<Scenario> historicalScenarios() {
        return entries().stream().map(ScenarioEntry::scenario).toList();
    }

    public static List<Scenario> scenariosForKeys(List<String> keys) {
        Map<String, Scenario> byKey = new LinkedHashMap<>();
        for (ScenarioEntry entry : entries()) {
            byKey.put(entry.key(), entry.scenario());
        }

        List<Scenario> scenarios = new ArrayList<>();
        for (String key : keys) {
            Scenario scenario = byKey.get(key);
            if (scenario == null) {
                throw new IllegalArgumentException("Unknown scenario key: " + key);
            }
            scenarios.add(scenario);
        }
        return scenarios;
    }

    public static List<String> scenarioKeys() {
        return entries().stream().map(ScenarioEntry::key).toList();
    }

    private static boolean isBreadthCatalogKey(String key) {
        return !key.startsWith("default-pass") || DEFAULT_SCENARIO_KEYS.contains(key);
    }

    private static List<ScenarioEntry> entries() {
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
                new ScenarioEntry("parliamentary-coalition-confidence", parliamentaryCoalitionConfidence()),
                new ScenarioEntry("citizen-initiative-referendum", citizenInitiativeReferendum()),
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
                new ScenarioEntry("law-registry-majority", majorityWithLawRegistry()),
                new ScenarioEntry("public-objection-majority", majorityWithPublicObjectionWindow()),
                new ScenarioEntry("public-objection-astroturf-majority", majorityWithAstroturfObjectionWindow()),
                new ScenarioEntry("anti-capture-majority-bundle", majorityWithAntiCaptureBundle()),
                new ScenarioEntry("risk-routed-majority", riskRoutedMajority()),
                new ScenarioEntry("portfolio-hybrid-legislature", portfolioHybridLegislature()),
                new ScenarioEntry("risk-routed-no-citizen-majority", riskRoutedNoCitizenReviewMajority()),
                new ScenarioEntry("norm-erosion-majority", normErosionMajority()),
                new ScenarioEntry("democratic-deterioration-majority", democraticDeteriorationMajority()),
                new ScenarioEntry("default-pass", unicameral("Default pass unless 2/3 block", new DefaultPassUnlessVetoedRule(2.0 / 3.0))),
                new ScenarioEntry("default-pass-mediation", defaultPassWithMediation()),
                new ScenarioEntry("default-pass-lobby-firewall", defaultPassWithLobbyFirewall()),
                new ScenarioEntry("default-pass-lobby-transparency", defaultPassWithLobbyTransparency()),
                new ScenarioEntry("default-pass-public-interest-screen", defaultPassWithPublicInterestScreen()),
                new ScenarioEntry("default-pass-lobby-audit", defaultPassWithLobbyAudit()),
                new ScenarioEntry("default-pass-anti-capture-bundle", defaultPassWithAntiCaptureBundle()),
                new ScenarioEntry("default-pass-budgeted-lobbying", defaultPassWithBudgetedLobbying(false, false)),
                new ScenarioEntry("default-pass-budgeted-lobbying-transparency", defaultPassWithBudgetedLobbying(true, false)),
                new ScenarioEntry("default-pass-budgeted-lobbying-bundle", defaultPassWithBudgetedLobbying(true, true)),
                new ScenarioEntry("default-pass-budgeted-lobbying-mediation", defaultPassWithBudgetedLobbyingAndMediation()),
                new ScenarioEntry("default-pass-democracy-vouchers", defaultPassWithDeepLobbying(
                        "Default pass + democracy vouchers",
                        0.72,
                        0.00,
                        0.00,
                        1.00
                )),
                new ScenarioEntry("default-pass-public-advocate", defaultPassWithDeepLobbying(
                        "Default pass + equal-access public advocate",
                        0.00,
                        0.74,
                        0.00,
                        1.00
                )),
                new ScenarioEntry("default-pass-blind-lobby-review", defaultPassWithDeepLobbying(
                        "Default pass + blind sponsor/lobby review",
                        0.00,
                        0.00,
                        0.78,
                        1.00
                )),
                new ScenarioEntry("default-pass-defensive-lobby-cap", defaultPassWithDeepLobbying(
                        "Default pass + defensive lobbying cap",
                        0.00,
                        0.00,
                        0.00,
                        0.025
                )),
                new ScenarioEntry("default-pass-lobby-channel-bundle", defaultPassWithDeepLobbying(
                        "Default pass + channel anti-capture bundle",
                        0.58,
                        0.62,
                        0.62,
                        0.05
                )),
                new ScenarioEntry("default-pass-citizen-certificate", defaultPassWithCitizenPanel(
                        "Default pass + citizen certificate",
                        CitizenPanelMode.DEFAULT_PASS_ELIGIBILITY
                )),
                new ScenarioEntry("default-pass-citizen-active-routing", defaultPassWithCitizenPanel(
                        "Default pass + citizen active-vote routing",
                        CitizenPanelMode.ACTIVE_VOTE_ROUTING
                )),
                new ScenarioEntry("default-pass-citizen-threshold", defaultPassWithCitizenPanel(
                        "Default pass + citizen threshold adjustment",
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT
                )),
                new ScenarioEntry("default-pass-citizen-agenda", defaultPassWithCitizenPanel(
                        "Default pass + citizen agenda priority",
                        CitizenPanelMode.AGENDA_PRIORITY
                )),
                new ScenarioEntry("default-pass-weighted-agenda-lottery", defaultPassWithAgendaLottery(
                        "Default pass + weighted agenda lottery",
                        true
                )),
                new ScenarioEntry("default-pass-random-agenda-lottery", defaultPassWithAgendaLottery(
                        "Default pass + random agenda lottery",
                        false
                )),
                new ScenarioEntry("default-pass-quadratic-attention", defaultPassWithQuadraticAttentionBudget()),
                new ScenarioEntry("default-pass-public-objection", defaultPassWithPublicObjectionWindow(false)),
                new ScenarioEntry("default-pass-repeal-window", defaultPassWithPublicObjectionWindow(true)),
                new ScenarioEntry("default-pass-constituent-public-will", defaultPassWithConstituentPublicWill(false)),
                new ScenarioEntry("default-pass-constituent-citizen-panel", defaultPassWithConstituentPublicWill(true)),
                new ScenarioEntry("default-pass-proposal-bonds", defaultPassWithProposalBonds(false)),
                new ScenarioEntry("default-pass-proposal-bonds-challenge", defaultPassWithProposalBonds(true)),
                new ScenarioEntry("default-pass-cross-bloc-credit-discount", defaultPassWithCoalitionSponsorship(
                        "Default pass + cross-bloc credit discount",
                        false,
                        true
                )),
                new ScenarioEntry("default-pass-affected-sponsor-gate", defaultPassWithCoalitionSponsorship(
                        "Default pass + affected-group sponsor gate",
                        true,
                        true
                )),
                new ScenarioEntry("default-pass-multiround-mediation", defaultPassWithMultiRoundMediation(false)),
                new ScenarioEntry("default-pass-multiround-mediation-challenge", defaultPassWithMultiRoundMediation(true)),
                new ScenarioEntry("default-pass-alternatives-strategic", defaultPassWithStrategicAlternatives()),
                new ScenarioEntry("default-pass-adaptive-proposers", defaultPassWithAdaptiveProposers(false)),
                new ScenarioEntry("default-pass-adaptive-proposers-lobbying", defaultPassWithAdaptiveProposers(true)),
                new ScenarioEntry("default-pass-strategic-lobbying", defaultPassWithStrategicLobbying()),
                new ScenarioEntry("default-pass-deep-strategy-bundle", defaultPassWithDeepStrategyBundle()),
                new ScenarioEntry("default-pass-adaptive-track-lenient", defaultPassWithAdaptiveTrack(false, 0.42, 0.68, "Default pass + adaptive tracks lenient")),
                new ScenarioEntry("default-pass-adaptive-track-strict", defaultPassWithAdaptiveTrack(false, 0.24, 0.48, "Default pass + adaptive tracks strict")),
                new ScenarioEntry("default-pass-adaptive-track-citizen-high-risk", defaultPassWithAdaptiveTrackCitizenHighRisk()),
                new ScenarioEntry("default-pass-adaptive-track-supermajority-high-risk", defaultPassWithAdaptiveTrackSupermajorityHighRisk()),
                new ScenarioEntry("default-pass-law-registry-fast-review", defaultPassWithLawRegistry(false, 2, 0.34, 0.58, 0.82, "Default pass + law registry fast review")),
                new ScenarioEntry("default-pass-law-registry-slow-review", defaultPassWithLawRegistry(false, 8, 0.34, 0.58, 0.62, "Default pass + law registry slow partial review")),
                new ScenarioEntry("default-pass-cost-public-waiver", defaultPassWithProposalCost(
                        "Default pass + proposal costs + public waiver",
                        0.34,
                        0.50,
                        0.00
                )),
                new ScenarioEntry("default-pass-cost-lobby-surcharge", defaultPassWithLobbySurchargeCost()),
                new ScenarioEntry("default-pass-member-quota", defaultPassWithMemberQuota()),
                new ScenarioEntry("default-pass-harm-threshold", defaultPassWithHarmWeightedThreshold()),
                new ScenarioEntry("default-pass-compensation", defaultPassWithDistributionalCompensation(false)),
                new ScenarioEntry("default-pass-affected-consent", defaultPassWithDistributionalCompensation(true)),
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
                )),
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
                )),
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

    private static Scenario majorityWithCommitteePower(
            String name,
            CommitteeComposition composition,
            double dischargeThreshold,
            double reportingDeadlinePressure,
            double amendmentStrength,
            double minorityHearingThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 19);
                Chamber committee = new Chamber(
                        "Committee power",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteePowerProcess(
                        name(),
                        committee,
                        process,
                        dischargeThreshold,
                        reportingDeadlinePressure,
                        amendmentStrength,
                        minorityHearingThreshold
                );
                return new CommitteeInformationProcess(name(), committeeMembers, 0.70, 0.40, process);
            }
        };
    }

    private static Scenario majorityWithCommitteeRole(
            String name,
            CommitteeRoleMode roleMode,
            CommitteeComposition composition,
            double gatekeepingThreshold,
            double chairNegativeAgendaPower,
            double informationAccuracy,
            double queueCapacity,
            double reviewCost,
            double captureSusceptibility
    ) {
        CommitteePowerConfig config = new CommitteePowerConfig(
                roleMode,
                gatekeepingThreshold,
                chairNegativeAgendaPower,
                informationAccuracy,
                queueCapacity,
                reviewCost,
                captureSusceptibility,
                Math.clamp(informationAccuracy - (0.30 * captureSusceptibility), 0.0, 1.0),
                Math.clamp(gatekeepingThreshold + 0.08, 0.0, 1.0),
                Math.clamp(0.42 + (0.40 * informationAccuracy), 0.0, 1.0),
                0.46,
                roleMode == CommitteeRoleMode.PUBLIC_ACCOUNTS ? 0.58 : 0.42,
                roleMode == CommitteeRoleMode.VETO_PLAYER,
                roleMode != CommitteeRoleMode.FAST_TRACK_CERTIFIER
        );
        return majorityWithConfiguredCommittee(
                name,
                CommitteeSelectionConfig.standard("general", 19),
                config,
                composition
        );
    }

    private static Scenario majorityWithConfiguredCommittee(
            String name,
            CommitteeSelectionConfig selectionConfig,
            CommitteePowerConfig powerConfig
    ) {
        return majorityWithConfiguredCommittee(
                name,
                selectionConfig,
                powerConfig,
                CommitteeComposition.MIXED_PARLIAMENTARIAN_CITIZEN
        );
    }

    private static Scenario majorityWithConfiguredCommittee(
            String name,
            CommitteeSelectionConfig selectionConfig,
            CommitteePowerConfig powerConfig,
            CommitteeComposition fallbackComposition
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                CommitteeSelectionResult selection = selectionConfig == null
                        ? new CommitteeSelectionResult(
                        CommitteeFactory.select(world.legislators(), fallbackComposition, 19),
                        null,
                        1.0,
                        0.0,
                        0.34,
                        true
                )
                        : CommitteeFactory.select(world.legislators(), selectionConfig);
                Chamber committee = new Chamber(
                        "Configured committee",
                        selection.members(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteePowerProcess(
                        name(),
                        committee,
                        process,
                        0.36,
                        powerConfig
                );
                return new CommitteeInformationProcess(
                        name(),
                        selection.members(),
                        Math.clamp(powerConfig.informationAccuracy() + (0.12 * selection.citizenAdvisoryWeight()), 0.0, 1.0),
                        Math.clamp(powerConfig.captureSusceptibility(), 0.0, 1.0),
                        process
                );
            }
        };
    }

    private static Scenario majorityWithCommitteeComposition(String name, CommitteeComposition composition) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 19);
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                return new CommitteeInformationProcess(name(), committeeMembers, 0.72, 0.44, process);
            }
        };
    }

    private static Scenario majorityWithCommitteeRegularOrder() {
        return new Scenario() {
            @Override
            public String name() {
                return "Committee-first regular order";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.86, 0.42, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.34, 0.82),
                        process
                );
            }
        };
    }

    private static Scenario leadershipCartelMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Leadership agenda cartel + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.54,
                                0.42,
                                0.34,
                                0.18,
                                0.22,
                                0.16
                        ),
                        simpleMajorityFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    private static Scenario clotureConferenceAndJudicialReview() {
        return new Scenario() {
            @Override
            public String name() {
                return "Cloture, conference, and judicial review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.MAJORITY_CONTROLLED,
                        17
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber house = new Chamber(
                        "House",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate cloture",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess process = new ConferenceCommitteeProcess(
                        name(),
                        house,
                        senate,
                        0.45,
                        chamberMedian(world.legislators()),
                        0.32,
                        0.30
                );
                process = new PresidentialVetoProcess(
                        process,
                        presidentFromWorld(world),
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                process = new JudicialReviewProcess(name(), process, 0.48, 0.66, 0.46);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.78, 0.48, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.56,
                                0.44,
                                0.30,
                                0.18,
                                0.18,
                                0.14
                        ),
                        process
                );
            }
        };
    }

    private static Scenario citizenInitiativeReferendum() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen initiative and referendum";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenInitiativeProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.58,
                        0.54,
                        0.42,
                        0.32
                );
            }
        };
    }

    private static Scenario parliamentaryCoalitionConfidence() {
        return new Scenario() {
            @Override
            public String name() {
                return "Parliamentary coalition confidence";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposalCreditProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        1.30,
                        0.34,
                        3.20,
                        0.48,
                        0.76,
                        0.36,
                        0.68,
                        0.50
                );
                return new CoalitionCosponsorshipProcess(
                        name(),
                        process,
                        world.legislators(),
                        3,
                        2,
                        0.14,
                        0.46,
                        false,
                        true
                );
            }
        };
    }

    private static Scenario majorityWithPublicInterestScreen() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority + public-interest screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.58, 2.35, 0.56),
                        simpleMajorityFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    private static Scenario majorityWithCitizenAssemblyThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen assembly threshold gate";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.62),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.14,
                        0.61
                );
            }
        };
    }

    private static Scenario majorityWithCitizenAssemblyManipulationStress() {
        return new Scenario() {
            @Override
            public String name() {
                return "Citizen assembly under manipulation stress";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        45,
                        0.24,
                        0.50,
                        0.86,
                        0.59
                );
            }
        };
    }

    private static Scenario majorityWithAgendaLottery(boolean weighted) {
        return new Scenario() {
            @Override
            public String name() {
                return weighted ? "Weighted agenda lottery + majority" : "Random agenda lottery + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AgendaLotteryProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.bills(),
                        weighted ? 0.46 : 0.42,
                        weighted
                );
            }
        };
    }

    private static Scenario majorityWithQuadraticAttentionBudget() {
        return new Scenario() {
            @Override
            public String name() {
                return "Quadratic attention budget + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new QuadraticAttentionBudgetProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        11.5,
                        4
                );
            }
        };
    }

    private static Scenario majorityWithProposalBonds() {
        return new Scenario() {
            @Override
            public String name() {
                return "Proposal bonds + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalBondProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        2.20,
                        0.20,
                        4.50,
                        0.40,
                        1.15,
                        0.38,
                        0.70
                );
            }
        };
    }

    private static Scenario majorityWithHarmWeightedThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Harm-weighted double majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber highHarm = new Chamber(
                        "Legislature harm review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.64)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.46);
            }
        };
    }

    private static Scenario majorityWithLooseHarmClaims() {
        return new Scenario() {
            @Override
            public String name() {
                return "Harm-weighted majority + loose harm claims";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber highHarm = new Chamber(
                        "Legislature loose-claim review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.64)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.22);
            }
        };
    }

    private static Scenario majorityWithDistributionalCompensation(boolean requireConsent) {
        return new Scenario() {
            @Override
            public String name() {
                return requireConsent
                        ? "Affected-group consent + majority"
                        : "Compensation amendments + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new DistributionalHarmProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.42,
                        requireConsent ? 0.48 : 0.42,
                        requireConsent ? 0.72 : 0.58,
                        requireConsent ? 0.42 : 0.30,
                        requireConsent
                );
            }
        };
    }

    private static Scenario majorityWithPackageBargaining() {
        return new Scenario() {
            @Override
            public String name() {
                return "Package bargaining + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PackageBargainingProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.32,
                        0.10,
                        0.08,
                        0.70
                );
            }
        };
    }

    private static Scenario majorityWithMultidimensionalPackageBargaining() {
        return new Scenario() {
            @Override
            public String name() {
                return "Multidimensional package bargaining + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new MultidimensionalPackageBargainingProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        0.28,
                        4,
                        0.66,
                        0.38,
                        0.54
                );
            }
        };
    }

    private static Scenario majorityWithLawRegistry() {
        return new Scenario() {
            @Override
            public String name() {
                return "Active-law registry + majority review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LawRegistryProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        5,
                        0.34,
                        0.58,
                        0.82
                );
            }
        };
    }

    private static Scenario majorityWithPublicObjectionWindow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Public objection window + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.62),
                        0.42,
                        0.06,
                        false
                );
            }
        };
    }

    private static Scenario majorityWithAstroturfObjectionWindow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Public objection window + astroturf stress";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        0.30,
                        0.18,
                        false
                );
            }
        };
    }

    private static Scenario majorityWithAntiCaptureBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority + anti-capture bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                LegislativeProcess process = simpleMajorityFloorProcess(name(), world, strategy);
                process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                        process
                );
                process = new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        0.58,
                        0.62,
                        0.62,
                        0.05,
                        true
                );
            }
        };
    }

    private static Scenario riskRoutedMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Risk-routed majority legislature";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.025,
                        1.15,
                        0.08
                );
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.64),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.12,
                        0.62
                );
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.30,
                        0.58
                );
            }
        };
    }

    private static Scenario portfolioHybridLegislature() {
        return new Scenario() {
            @Override
            public String name() {
                return "Portfolio hybrid legislature";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy standard = VotingStrategies.standard();
                VotingStrategy antiCapture = VotingStrategies.antiCapture();

                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, standard);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, standard),
                        world.legislators(),
                        3,
                        0.023,
                        1.18,
                        0.055
                );
                middleLane = new CompetingAlternativesProcess(
                        name(),
                        middleLane,
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        0,
                        0,
                        0.92,
                        0.012,
                        0.0
                );
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, antiCapture),
                        supermajorityFloorProcess(name(), world, antiCapture, 0.65),
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.84,
                        0.12,
                        0.62
                );
                highRiskLane = new DistributionalHarmProcess(
                        name(),
                        highRiskLane,
                        0.40,
                        0.43,
                        0.66,
                        0.31,
                        false
                );
                LegislativeProcess process = new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.28,
                        0.56
                );
                process = new LobbyAuditProcess(name(), process, 0.08, 0.70, 0.46, 0.50, true);
                process = new ProposalBondProcess(name(), process, 2.70, 0.22, 4.80, 0.24, 0.78, 0.30, 0.90);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.40, 0.70, 2.80, 0.52),
                        process
                );
                process = new LobbyTransparencyProcess(name(), 0.70, 0.30, process);
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.20,
                        0.40,
                        0.32,
                        0.48,
                        0.45,
                        0.40,
                        0.06,
                        true
                );
                return new LawRegistryProcess(name(), process, 4, 0.32, 0.58, 0.76);
            }
        };
    }

    private static Scenario riskRoutedNoCitizenReviewMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Risk-routed majority without citizen review";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = new MultiRoundAmendmentProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.025,
                        1.15,
                        0.08
                );
                LegislativeProcess highRiskLane = supermajorityFloorProcess(name(), world, strategy, 0.64);
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        0.30,
                        0.58
                );
            }
        };
    }

    private static Scenario normErosionMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Endogenous norm erosion + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposerStrategyProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        0.58,
                        0.58,
                        0.46
                );
                return new InstitutionalNormErosionProcess(
                        name(),
                        process,
                        0.18,
                        0.42,
                        0.16
                );
            }
        };
    }

    private static Scenario democraticDeteriorationMajority() {
        return new Scenario() {
            @Override
            public String name() {
                return "Democratic deterioration stress + majority";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new ProposerStrategyProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        0.62,
                        0.56,
                        0.44
                );
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.34,
                        true
                );
                return new DemocraticDeteriorationProcess(
                        name(),
                        process,
                        0.16,
                        0.38,
                        0.46,
                        0.34,
                        0.42,
                        0.10
                );
            }
        };
    }

    private static Scenario simpleMajorityWithMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Unicameral majority + mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return mediationProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world
                );
            }
        };
    }

    private static Scenario defaultPassWithMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + mediated amendments";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return mediationProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world
                );
            }
        };
    }

    private static Scenario defaultPassWithLobbyFirewall() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby firewall";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                return defaultPassFloorProcess(name(), world, strategy);
            }
        };
    }

    private static Scenario defaultPassWithLobbyTransparency() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby transparency";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LobbyTransparencyProcess(
                        name(),
                        0.72,
                        0.30,
                        defaultPassFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    private static Scenario defaultPassWithPublicInterestScreen() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + public-interest screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.54, 0.58, 2.40, 0.58),
                        defaultPassFloorProcess(name(), world, strategy)
                );
            }
        };
    }

    private static Scenario defaultPassWithLobbyAudit() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + anti-capture audit";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new LobbyAuditProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        0.08,
                        0.70,
                        0.48,
                        0.50,
                        true
                );
            }
        };
    }

    private static Scenario defaultPassWithAntiCaptureBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + anti-capture bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.antiCapture();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                        process
                );
                return new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
            }
        };
    }

    private static Scenario defaultPassWithBudgetedLobbying(boolean includeTransparency, boolean includeAntiCaptureBundle) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeAntiCaptureBundle) {
                    return "Default pass + budgeted lobbying + anti-capture bundle";
                }
                if (includeTransparency) {
                    return "Default pass + budgeted lobbying + transparency";
                }
                return "Default pass + budgeted lobbying";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = includeAntiCaptureBundle
                        ? VotingStrategies.antiCapture()
                        : VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                if (includeAntiCaptureBundle) {
                    process = new LobbyAuditProcess(name(), process, 0.10, 0.72, 0.45, 0.55, true);
                    process = new ProposalAccessProcess(
                            name(),
                            ProposalAccessRules.publicInterestScreen(0.52, 0.60, 2.50, 0.56),
                            process
                    );
                }
                if (includeTransparency) {
                    process = new LobbyTransparencyProcess(name(), 0.74, 0.34, process);
                }
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.35
                );
            }
        };
    }

    private static Scenario defaultPassWithBudgetedLobbyingAndMediation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + budgeted lobbying + mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = mediationProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world
                );
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.22,
                        0.44,
                        0.35
                );
            }
        };
    }

    private static Scenario defaultPassWithStrategicLobbying() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + strategic lobbying";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new BudgetedLobbyingProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        true
                );
            }
        };
    }

    private static Scenario defaultPassWithAdaptiveProposers(boolean includeStrategicLobbying) {
        return new Scenario() {
            @Override
            public String name() {
                return includeStrategicLobbying
                        ? "Default pass + adaptive proposers + strategic lobbying"
                        : "Default pass + adaptive proposers";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                if (includeStrategicLobbying) {
                    process = new BudgetedLobbyingProcess(
                            name(),
                            process,
                            world.lobbyGroups(),
                            0.24,
                            0.46,
                            0.38,
                            true
                    );
                }
                return new ProposerStrategyProcess(
                        name(),
                        process,
                        world.legislators(),
                        0.72,
                        0.56,
                        0.42
                );
            }
        };
    }

    private static Scenario defaultPassWithDeepStrategyBundle() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive strategy bundle";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = new MultiRoundAmendmentProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        3,
                        0.024,
                        1.18,
                        0.07
                );
                process = new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        0.42,
                        0.40,
                        0.30,
                        0.08,
                        true
                );
                return new ProposerStrategyProcess(
                        name(),
                        process,
                        world.legislators(),
                        0.80,
                        0.52,
                        0.36
                );
            }
        };
    }

    private static Scenario defaultPassWithDeepLobbying(
            String scenarioName,
            double publicFinancingStrength,
            double publicAdvocateStrength,
            double blindReviewStrength,
            double defensiveCapShare
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = publicAdvocateStrength > 0.0 || publicFinancingStrength > 0.0
                        ? VotingStrategies.antiCapture()
                        : VotingStrategies.standard();
                LegislativeProcess process = defaultPassFloorProcess(name(), world, strategy);
                return new BudgetedLobbyingProcess(
                        name(),
                        process,
                        world.lobbyGroups(),
                        0.24,
                        0.46,
                        0.38,
                        publicFinancingStrength,
                        publicAdvocateStrength,
                        blindReviewStrength,
                        defensiveCapShare
                );
            }
        };
    }

    private static Scenario defaultPassWithCitizenPanel(String scenarioName, CitizenPanelMode mode) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess certifiedProcess = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess uncertifiedProcess = switch (mode) {
                    case AGENDA_PRIORITY -> certifiedProcess;
                    case DEFAULT_PASS_ELIGIBILITY, ACTIVE_VOTE_ROUTING -> simpleMajorityFloorProcess(name(), world, strategy);
                    case THRESHOLD_ADJUSTMENT -> supermajorityFloorProcess(name(), world, strategy, 0.60);
                };
                return new CitizenPanelReviewProcess(
                        name(),
                        certifiedProcess,
                        uncertifiedProcess,
                        mode,
                        mode == CitizenPanelMode.AGENDA_PRIORITY ? 41 : 73,
                        0.18,
                        mode == CitizenPanelMode.ACTIVE_VOTE_ROUTING ? 0.78 : 0.68,
                        mode == CitizenPanelMode.THRESHOLD_ADJUSTMENT ? 0.18 : 0.24,
                        mode == CitizenPanelMode.AGENDA_PRIORITY ? 0.56 : 0.60
                );
            }
        };
    }

    private static Scenario defaultPassWithAgendaLottery(String scenarioName, boolean weighted) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AgendaLotteryProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.bills(),
                        weighted ? 0.46 : 0.42,
                        weighted
                );
            }
        };
    }

    private static Scenario defaultPassWithQuadraticAttentionBudget() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + quadratic attention budget";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new QuadraticAttentionBudgetProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        11.5,
                        4
                );
            }
        };
    }

    private static Scenario defaultPassWithPublicObjectionWindow(boolean repealMode) {
        return new Scenario() {
            @Override
            public String name() {
                return repealMode
                        ? "Default pass + public repeal window"
                        : "Default pass + public objection window";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new PublicObjectionWindowProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        repealMode ? 0.50 : 0.42,
                        0.06,
                        repealMode
                );
            }
        };
    }

    private static Scenario defaultPassWithConstituentPublicWill(boolean includeCitizenPanel) {
        return new Scenario() {
            @Override
            public String name() {
                return includeCitizenPanel
                        ? "Default pass + constituent public will + citizen panel"
                        : "Default pass + constituent public will";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process;
                if (includeCitizenPanel) {
                    LegislativeProcess certified = defaultPassFloorProcess(name(), world, strategy);
                    LegislativeProcess uncertified = simpleMajorityFloorProcess(name(), world, strategy);
                    process = new CitizenPanelReviewProcess(
                            name(),
                            certified,
                            uncertified,
                            CitizenPanelMode.ACTIVE_VOTE_ROUTING,
                            73,
                            0.14,
                            0.80,
                            0.16,
                            0.60
                    );
                } else {
                    process = defaultPassFloorProcess(name(), world, strategy);
                }
                return new ConstituentPublicWillProcess(name(), process, world.legislators(), 0.74, 0.45);
            }
        };
    }

    private static Scenario defaultPassWithProposalBonds(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                return includeChallengeVouchers
                        ? "Default pass + proposal bonds + challenge"
                        : "Default pass + proposal bonds";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new ProposalBondProcess(name(), process, 2.20, 0.20, 4.50, 0.40, 1.15, 0.38, 0.70);
            }
        };
    }

    private static Scenario defaultPassWithCoalitionSponsorship(
            String scenarioName,
            boolean requireAffectedGroupSponsor,
            boolean applyAgendaCreditDiscount
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CoalitionCosponsorshipProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        requireAffectedGroupSponsor ? 3 : 2,
                        1,
                        0.12,
                        requireAffectedGroupSponsor ? 0.50 : 0.48,
                        requireAffectedGroupSponsor,
                        applyAgendaCreditDiscount
                );
            }
        };
    }

    private static Scenario defaultPassWithMultiRoundMediation(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                return includeChallengeVouchers
                        ? "Default pass + multi-round mediation + challenge"
                        : "Default pass + multi-round mediation";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess process = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new MultiRoundAmendmentProcess(name(), process, world.legislators(), 3, 0.025, 1.15, 0.08);
            }
        };
    }

    private static Scenario defaultPassWithStrategicAlternatives() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + strategic policy tournament";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        4,
                        4,
                        0.45,
                        0.035,
                        0.10
                );
            }
        };
    }

    private static Scenario simpleMajorityWithStrategicAlternatives() {
        return new Scenario() {
            @Override
            public String name() {
                return "Majority ratification + strategic policy tournament";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        AlternativeSelectionRule.PAIRWISE_MAJORITY,
                        4,
                        true,
                        4,
                        4,
                        0.45,
                        0.035,
                        0.10
                );
            }
        };
    }

    private static Scenario defaultPassWithHarmWeightedThreshold() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + harm-weighted threshold";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber ordinary = new Chamber(
                        "Legislature",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber highHarm = new Chamber(
                        "Legislature harm review",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                return new HarmWeightedThresholdProcess(name(), ordinary, highHarm, 0.48);
            }
        };
    }

    private static Scenario defaultPassWithDistributionalCompensation(boolean requireConsent) {
        return new Scenario() {
            @Override
            public String name() {
                return requireConsent
                        ? "Default pass + affected-group consent"
                        : "Default pass + compensation amendments";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new DistributionalHarmProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        0.42,
                        requireConsent ? 0.48 : 0.42,
                        requireConsent ? 0.72 : 0.58,
                        requireConsent ? 0.42 : 0.30,
                        requireConsent
                );
            }
        };
    }

    private static Scenario simpleMajorityWithCompetingAlternatives(
            String scenarioName,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        world.legislators(),
                        selectionRule,
                        generatedAlternatives,
                        includeStatusQuo
                );
            }
        };
    }

    private static Scenario defaultPassWithCompetingAlternatives(
            String scenarioName,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new CompetingAlternativesProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        world.legislators(),
                        selectionRule,
                        generatedAlternatives,
                        includeStatusQuo
                );
            }
        };
    }

    private static LegislativeProcess mediationProcess(
            String name,
            LegislativeProcess innerProcess,
            SimulationWorld world
    ) {
        return new AmendmentMediationProcess(
                name,
                innerProcess,
                world.legislators(),
                0.22,
                0.72,
                0.58,
                0.28,
                0.14
        );
    }

    private static Scenario defaultPassWithProposalAccess() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + proposal access screen";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                LegislativeProcess floor = new UnicameralProcess(name(), chamber);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        floor
                );
            }
        };
    }

    private static Scenario defaultPassWithChallengeVouchers() {
        return defaultPassWithChallengeVouchers(
                "Default pass + challenge vouchers",
                ChallengeTokenAllocation.PARTY,
                10,
                0.82
        );
    }

    private static Scenario defaultPassWithChallengeVouchers(
            String scenarioName,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner,
            double challengeThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        allocation,
                        tokensPerOwner,
                        challengeThreshold,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithChallengePath(
            String scenarioName,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner,
            double challengeThreshold,
            ChallengePath challengePath
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess challengedProcess = challengedProcess(name(), world, strategy, challengePath);
                return new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        allocation,
                        tokensPerOwner,
                        challengeThreshold,
                        challengedProcess
                );
            }
        };
    }

    private static LegislativeProcess challengedProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy,
            ChallengePath challengePath
    ) {
        return switch (challengePath) {
            case SIMPLE_MAJORITY -> simpleMajorityFloorProcess(name, world, strategy);
            case SUPERMAJORITY -> supermajorityFloorProcess(name, world, strategy, 0.60);
            case COMMITTEE_REVIEW -> {
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                yield new CommitteeGatekeepingProcess(name, committee, simpleMajorityFloorProcess(name, world, strategy));
            }
            case INFORMATION_PLUS_ACTIVE -> {
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.EXPERT,
                        17
                );
                yield new CommitteeInformationProcess(
                        name,
                        committeeMembers,
                        0.90,
                        0.35,
                        simpleMajorityFloorProcess(name, world, strategy)
                );
            }
        };
    }

    private static Scenario defaultPassWithChallengeEscalation(
            String scenarioName,
            int minimumChallengers,
            double challengeThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new ChallengeEscalationProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        minimumChallengers,
                        challengeThreshold,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithChallengeVouchersAndInformation() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + challenge vouchers + info";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess challengeProcess = new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        10,
                        0.82,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
                return new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, challengeProcess);
            }
        };
    }

    private static Scenario defaultPassWithCrossBlocCosponsorship(
            String scenarioName,
            int minimumCosponsors,
            int minimumOutsideBlocs,
            double minimumIdeologicalDistance,
            double cosponsorThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.crossBlocCosponsorship(
                                world.legislators(),
                                minimumCosponsors,
                                minimumOutsideBlocs,
                                minimumIdeologicalDistance,
                                cosponsorThreshold
                        ),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithCrossBlocCosponsorshipAndChallenge() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + cross-bloc cosponsors + challenge";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber activeVoteChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess challengeProcess = new ChallengeVoucherProcess(
                        name(),
                        world.legislators(),
                        strategy,
                        ChallengeTokenAllocation.PARTY,
                        10,
                        0.82,
                        new UnicameralProcess(name(), activeVoteChamber)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.crossBlocCosponsorship(
                                world.legislators(),
                                2,
                                1,
                                0.12,
                                0.52
                        ),
                        challengeProcess
                );
            }
        };
    }

    private static Scenario defaultPassWithAdaptiveTrack(boolean useChallengeMiddleLane) {
        return defaultPassWithAdaptiveTrack(
                useChallengeMiddleLane,
                0.34,
                0.58,
                useChallengeMiddleLane
                        ? "Default pass + adaptive tracks + challenge"
                        : "Default pass + adaptive tracks"
        );
    }

    private static Scenario defaultPassWithAdaptiveTrack(
            boolean useChallengeMiddleLane,
            double fastLaneMaximumRisk,
            double highRiskMinimumRisk,
            String scenarioName
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess fastLane = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess middleLane = useChallengeMiddleLane
                        ? challengeMiddleLane(name(), world, strategy)
                        : simpleMajorityFloorProcess(name(), world, strategy);
                LegislativeProcess highRiskLane = informedGuardrailProcess(name(), world, strategy);
                return new AdaptiveTrackProcess(
                        name(),
                        fastLane,
                        middleLane,
                        highRiskLane,
                        fastLaneMaximumRisk,
                        highRiskMinimumRisk
                );
            }
        };
    }

    private static Scenario defaultPassWithAdaptiveTrackCitizenHighRisk() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive tracks + citizen high-risk";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess certified = defaultPassFloorProcess(name(), world, strategy);
                LegislativeProcess uncertified = supermajorityFloorProcess(name(), world, strategy, 0.60);
                LegislativeProcess highRiskLane = new CitizenPanelReviewProcess(
                        name(),
                        certified,
                        uncertified,
                        CitizenPanelMode.THRESHOLD_ADJUSTMENT,
                        91,
                        0.12,
                        0.82,
                        0.12,
                        0.62
                );
                return new AdaptiveTrackProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        highRiskLane,
                        0.34,
                        0.58
                );
            }
        };
    }

    private static Scenario defaultPassWithAdaptiveTrackSupermajorityHighRisk() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + adaptive tracks + supermajority high-risk";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                return new AdaptiveTrackProcess(
                        name(),
                        defaultPassFloorProcess(name(), world, strategy),
                        simpleMajorityFloorProcess(name(), world, strategy),
                        supermajorityFloorProcess(name(), world, strategy, 0.60),
                        0.34,
                        0.58
                );
            }
        };
    }

    private static Scenario defaultPassWithSunsetTrial(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeChallengeVouchers) {
                    return "Default pass + sunset trial + challenge";
                }
                return "Default pass + sunset trial";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new SunsetTrialProcess(
                        name(),
                        innerProcess,
                        0.38,
                        0.56
                );
            }
        };
    }

    private static Scenario defaultPassWithLawRegistry(boolean includeChallengeVouchers) {
        return defaultPassWithLawRegistry(
                includeChallengeVouchers,
                5,
                0.34,
                0.58,
                0.82,
                includeChallengeVouchers
                        ? "Default pass + law registry + challenge"
                        : "Default pass + law registry"
        );
    }

    private static Scenario defaultPassWithLawRegistry(
            boolean includeChallengeVouchers,
            int reviewDelayRounds,
            double provisionalRiskThreshold,
            double renewalThreshold,
            double rollbackRate,
            String scenarioName
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new LawRegistryProcess(
                        name(),
                        innerProcess,
                        reviewDelayRounds,
                        provisionalRiskThreshold,
                        renewalThreshold,
                        rollbackRate
                );
            }
        };
    }

    private static Scenario defaultPassWithProposalCredits(boolean includeChallengeVouchers) {
        return new Scenario() {
            @Override
            public String name() {
                if (includeChallengeVouchers) {
                    return "Default pass + earned proposal credits + challenge";
                }
                return "Default pass + earned proposal credits";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                LegislativeProcess innerProcess = includeChallengeVouchers
                        ? challengeMiddleLane(name(), world, strategy)
                        : defaultPassFloorProcess(name(), world, strategy);
                return new ProposalCreditProcess(
                        name(),
                        innerProcess,
                        1.15,
                        0.30,
                        3.00,
                        0.56,
                        1.00,
                        0.28,
                        0.75,
                        0.60
                );
            }
        };
    }

    private static LegislativeProcess defaultPassFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                new DefaultPassUnlessVetoedRule(2.0 / 3.0)
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess simpleMajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess supermajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy,
            double threshold
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.supermajority(threshold)
        );
        return new UnicameralProcess(name, chamber);
    }

    private static LegislativeProcess challengeMiddleLane(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber activeVoteChamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new ChallengeVoucherProcess(
                name,
                world.legislators(),
                strategy,
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                new UnicameralProcess(name, activeVoteChamber)
        );
    }

    private static LegislativeProcess informedGuardrailProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        List<Legislator> committeeMembers = CommitteeFactory.select(
                world.legislators(),
                CommitteeComposition.REPRESENTATIVE,
                17
        );
        Chamber floorChamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                new DefaultPassUnlessVetoedRule(2.0 / 3.0)
        );
        Chamber committee = new Chamber(
                "Committee",
                committeeMembers,
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        LegislativeProcess process = new UnicameralProcess(name, floorChamber);
        process = new CommitteeGatekeepingProcess(name, committee, process);
        process = new CommitteeInformationProcess(name, committeeMembers, 0.85, 0.45, process);
        return new ProposalAccessProcess(
                name,
                ProposalAccessRules.viabilityScreen(0.35, 0.85),
                process
        );
    }

    private static Scenario defaultPassWithProposalCost() {
        return defaultPassWithProposalCost("Default pass + proposal costs", 0.34, 0.22, 0.18);
    }

    private static Scenario defaultPassWithProposalCost(
            String scenarioName,
            double baseCost,
            double publicCreditWeight,
            double lobbyCreditWeight
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return scenarioName;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.proposalCost(baseCost, publicCreditWeight, lobbyCreditWeight),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithLobbySurchargeCost() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + lobby-surcharge proposal costs";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.lobbySurchargeCost(0.32, 0.48, 0.42),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithMemberQuota() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + member proposal quota";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.memberQuota(3),
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithCostAndGuardrails() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + costs + informed guardrails";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.REPRESENTATIVE,
                        17
                );
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );

                LegislativeProcess process = new UnicameralProcess(name(), floorChamber);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, process);
                process = new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        process
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.proposalCost(0.34, 0.22, 0.18),
                        process
                );
            }
        };
    }

    private static Scenario defaultPassWithCommitteeGate(String name, CommitteeComposition composition) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        CommitteeFactory.select(world.legislators(), composition, 17),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                return new CommitteeGatekeepingProcess(
                        name(),
                        committee,
                        new UnicameralProcess(name(), floorChamber)
                );
            }
        };
    }

    private static Scenario defaultPassWithInformation(
            String name,
            CommitteeComposition composition,
            boolean includeAccessAndGate
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 17);
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                LegislativeProcess process = new UnicameralProcess(name(), floorChamber);
                if (includeAccessAndGate) {
                    Chamber committee = new Chamber(
                            "Committee",
                            committeeMembers,
                            strategy,
                            AffirmativeThresholdRule.simpleMajority()
                    );
                    process = new CommitteeGatekeepingProcess(name(), committee, process);
                }
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.85, 0.45, process);
                if (includeAccessAndGate) {
                    process = new ProposalAccessProcess(
                            name(),
                            ProposalAccessRules.viabilityScreen(0.35, 0.85),
                            process
                    );
                }
                return process;
            }
        };
    }

    private static Scenario defaultPassWithAccessAndCommitteeGate() {
        return new Scenario() {
            @Override
            public String name() {
                return "Default pass + access + committee";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber floorChamber = new Chamber(
                        "Congress",
                        world.legislators(),
                        strategy,
                        new DefaultPassUnlessVetoedRule(2.0 / 3.0)
                );
                Chamber committee = new Chamber(
                        "Committee",
                        CommitteeFactory.select(world.legislators(), CommitteeComposition.REPRESENTATIVE, 17),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess committeeGate = new CommitteeGatekeepingProcess(
                        name(),
                        committee,
                        new UnicameralProcess(name(), floorChamber)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.viabilityScreen(0.35, 0.85),
                        committeeGate
                );
            }
        };
    }

    private static Scenario unicameral(String name, VotingRule rule) {
        return unicameral(name, rule, VotingStrategies.standard());
    }

    private static Scenario unicameral(String name, VotingRule rule, VotingStrategy strategy) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                Chamber chamber = new Chamber("Congress", world.legislators(), strategy, rule);
                return new UnicameralProcess(name, chamber);
            }
        };
    }

    private static Scenario bicameral(String name, VotingRule rule) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber("House", world.legislators(), strategy, rule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, rule);
                return new BicameralProcess(name, house, senate);
            }
        };
    }

    private static Scenario chamberUnicameral(String name, ChamberSpec chamberSpec, VotingRule rule) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> members = ChamberFactory.select(world.legislators(), chamberSpec, 15_151L);
                Chamber chamber = new Chamber(chamberSpec.name(), members, strategy, rule);
                OutcomeSignals architectureSignals = chamberArchitectureSignals(
                        world.legislators(),
                        chamberSpec,
                        chamberSpec,
                        members,
                        members
                );
                return new ChamberArchitectureSignalProcess(new UnicameralProcess(name(), chamber), architectureSignals);
            }
        };
    }

    private static Scenario eligibilityFilteredMajority(
            String name,
            EligibilityRule eligibilityRule,
            boolean appointmentPool
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> candidatePool = appointmentPool
                        ? ChamberFactory.select(world.legislators(), ChamberSpec.appointedUpperHouse(101, 0.62), 72_121L)
                        : world.legislators();
                List<Legislator> eligible = eligibleMembers(candidatePool, eligibilityRule, Math.min(31, candidatePool.size()));
                Chamber chamber = new Chamber("Eligibility-filtered chamber", eligible, strategy, AffirmativeThresholdRule.simpleMajority());
                LegislativeProcess process = new UnicameralProcess(name(), chamber);
                return new EligibilityDiagnosticsProcess(name(), world.legislators(), eligible, eligibilityRule, process);
            }
        };
    }

    private static Scenario exAnteReviewMajority(
            String name,
            ExAnteReviewMode mode,
            IndependentInstitutionBundle bundle,
            double highRiskThreshold,
            double overrideThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber("Congress", world.legislators(), strategy, AffirmativeThresholdRule.simpleMajority());
                return new ExAnteReviewProcess(
                        name(),
                        mode,
                        bundle,
                        highRiskThreshold,
                        overrideThreshold,
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    private static List<Legislator> eligibleMembers(
            List<Legislator> candidatePool,
            EligibilityRule eligibilityRule,
            int minimumSize
    ) {
        List<Legislator> eligible = candidatePool.stream()
                .filter(eligibilityRule::eligible)
                .toList();
        if (eligible.size() >= minimumSize) {
            return eligible;
        }
        List<Legislator> expanded = new ArrayList<>(eligible);
        candidatePool.stream()
                .sorted(Comparator.comparingDouble(EligibilityRule::expertiseProxy).reversed())
                .filter(legislator -> expanded.stream().noneMatch(existing -> existing.id().equals(legislator.id())))
                .forEach(legislator -> {
                    if (expanded.size() < minimumSize) {
                        expanded.add(legislator);
                    }
                });
        return expanded;
    }

    private static Scenario chamberArchitecture(
            String name,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            VotingRule upperRule,
            boolean useConference
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> lowerMembers = ChamberFactory.select(world.legislators(), lowerSpec, 10_101L);
                List<Legislator> upperMembers = ChamberFactory.select(world.legislators(), upperSpec, 20_202L);
                Chamber lower = new Chamber(
                        lowerSpec.name(),
                        lowerMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber upper = new Chamber(upperSpec.name(), upperMembers, strategy, upperRule);
                OutcomeSignals architectureSignals = chamberArchitectureSignals(
                        world.legislators(),
                        lowerSpec,
                        upperSpec,
                        lowerMembers,
                        upperMembers
                );
                LegislativeProcess process;
                if (useConference) {
                    process = new ConferenceCommitteeProcess(
                            name(),
                            lower,
                            upper,
                            0.46,
                            (chamberMedian(lowerMembers) + chamberMedian(upperMembers)) / 2.0,
                            0.34,
                            0.28
                    );
                } else {
                    process = new BicameralProcess(name(), lower, upper);
                }
                return new ChamberArchitectureSignalProcess(process, architectureSignals);
            }
        };
    }

    private static Scenario chamberRouting(
            String name,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            VotingRule upperRule,
            BicameralOriginRule originRule,
            BicameralConflictMode conflictMode
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> lowerMembers = ChamberFactory.select(world.legislators(), lowerSpec, 30_303L);
                List<Legislator> upperMembers = ChamberFactory.select(world.legislators(), upperSpec, 40_404L);
                Chamber lower = new Chamber(
                        lowerSpec.name(),
                        lowerMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber upper = new Chamber(upperSpec.name(), upperMembers, strategy, upperRule);
                LegislativeProcess process = new BicameralRoutingProcess(
                        name(),
                        lower,
                        upper,
                        strategy,
                        originRule,
                        conflictMode,
                        AffirmativeThresholdRule.simpleMajority(),
                        0.46,
                        (chamberMedian(lowerMembers) + chamberMedian(upperMembers)) / 2.0,
                        0.32,
                        0.22,
                        0.58,
                        3
                );
                return new ChamberArchitectureSignalProcess(
                        process,
                        chamberArchitectureSignals(world.legislators(), lowerSpec, upperSpec, lowerMembers, upperMembers)
                );
            }
        };
    }

    private static OutcomeSignals chamberArchitectureSignals(
            List<Legislator> electorate,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            List<Legislator> lowerMembers,
            List<Legislator> upperMembers
    ) {
        List<RepresentationUnit> lowerUnits = ChamberFactory.representationUnits(lowerSpec);
        List<RepresentationUnit> upperUnits = ChamberFactory.representationUnits(upperSpec);
        double populationSeatDistortion = average(
                ChamberArchitectureMetrics.populationSeatDistortion(lowerUnits),
                ChamberArchitectureMetrics.populationSeatDistortion(upperUnits)
        );
        double democraticResponsiveness = average(
                ChamberArchitectureMetrics.democraticResponsiveness(lowerUnits),
                ChamberArchitectureMetrics.democraticResponsiveness(upperUnits)
        );
        double seatVoteDistortion = average(
                ChamberArchitectureMetrics.seatVoteDistortion(electorate, lowerMembers),
                ChamberArchitectureMetrics.seatVoteDistortion(electorate, upperMembers)
        );
        double constituencyServiceConcentration = average(
                ChamberArchitectureMetrics.constituencyServiceConcentration(lowerUnits),
                ChamberArchitectureMetrics.constituencyServiceConcentration(upperUnits)
        );
        double regionalTransferBias = average(
                ChamberArchitectureMetrics.regionalTransferBias(lowerUnits),
                ChamberArchitectureMetrics.regionalTransferBias(upperUnits)
        );
        double malapportionmentIndex = average(
                ChamberArchitectureMetrics.malapportionmentIndex(lowerUnits),
                ChamberArchitectureMetrics.malapportionmentIndex(upperUnits)
        );
        return OutcomeSignals.chamberArchitecture(
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias
        ).plus(OutcomeSignals.diagnostic("malapportionmentIndex", malapportionmentIndex));
    }

    private static double average(double left, double right) {
        return (left + right) / 2.0;
    }

    private static Scenario presidentialVeto() {
        return new Scenario() {
            @Override
            public String name() {
                return "Bicameral majority + presidential veto";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                VotingRule chamberRule = AffirmativeThresholdRule.simpleMajority();
                Chamber house = new Chamber("House", world.legislators(), strategy, chamberRule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, chamberRule);
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                Legislator president = presidentFromWorld(world);
                return new PresidentialVetoProcess(
                        bicameral,
                        president,
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
            }
        };
    }

    private static Scenario currentSystem() {
        return new Scenario() {
            @Override
            public String name() {
                return "Stylized U.S.-like conventional benchmark";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber(
                        "House",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                LegislativeProcess finalPassage = new PresidentialVetoProcess(
                        bicameral,
                        presidentFromWorld(world),
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.currentSystemAgenda(0.58),
                        finalPassage
                );
            }
        };
    }

    private static Scenario stylizedCurrentCongressWorkflow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Stylized current-Congress workflow";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.MAJORITY_CONTROLLED,
                        19
                );
                Chamber committee = new Chamber(
                        "Committee queue",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber house = new Chamber(
                        "House floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate cloture/final passage",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess process = new ConferenceCommitteeProcess(
                        name(),
                        house,
                        senate,
                        0.50,
                        chamberMedian(world.legislators()),
                        0.30,
                        0.34
                );
                process = new PresidentialVetoProcess(
                        process,
                        presidentFromWorld(world),
                        strategy,
                        0.66,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                process = new JudicialReviewProcess(name(), process, 0.44, 0.68, 0.44);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.74, 0.50, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.58,
                                0.46,
                                0.34,
                                0.20,
                                0.20,
                                0.16
                        ),
                        process
                );
            }
        };
    }

    private static double chamberMedian(List<Legislator> legislators) {
        if (legislators.isEmpty()) {
            return 0.0;
        }
        List<Double> positions = legislators.stream()
                .map(Legislator::ideology)
                .sorted()
                .toList();
        int middle = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(middle);
        }
        return (positions.get(middle - 1) + positions.get(middle)) / 2.0;
    }

    private static List<Legislator> senateSubset(List<Legislator> legislators) {
        List<Legislator> senate = new ArrayList<>();
        int stride = Math.max(2, legislators.size() / Math.max(1, legislators.size() / 3));
        for (int i = 0; i < legislators.size(); i += stride) {
            senate.add(legislators.get(i));
        }
        if (senate.isEmpty()) {
            senate.add(legislators.getFirst());
        }
        return senate;
    }

    private static Legislator presidentFromWorld(SimulationWorld world) {
        double averageIdeology = world.legislators()
                .stream()
                .mapToDouble(Legislator::ideology)
                .average()
                .orElse(0.0);
        return new Legislator(
                "EXEC-1",
                "Executive",
                averageIdeology * 0.7,
                0.42,
                0.72,
                0.58,
                0.46,
                0.62
        );
    }

    private record ScenarioEntry(String key, Scenario scenario) {
    }

    private enum ChallengePath {
        SIMPLE_MAJORITY,
        SUPERMAJORITY,
        COMMITTEE_REVIEW,
        INFORMATION_PLUS_ACTIVE
    }
}
