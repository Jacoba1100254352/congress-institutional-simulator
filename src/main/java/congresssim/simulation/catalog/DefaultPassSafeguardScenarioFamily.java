package congresssim.simulation.catalog;


import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.voting.DefaultPassUnlessVetoedRule;

import java.util.List;

import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.*;
import static congresssim.simulation.catalog.SharedScenarioBuilders.unicameral;


/**
 * Default-pass safeguards, accountability, lobbying, and routing variants.
 */
final class DefaultPassSafeguardScenarioFamily
{
	private DefaultPassSafeguardScenarioFamily() {
	}
	
	static List<ScenarioEntry> entries() {
		return List.of(
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
				new ScenarioEntry("default-pass-affected-consent", defaultPassWithDistributionalCompensation(true))
		);
	}
}
