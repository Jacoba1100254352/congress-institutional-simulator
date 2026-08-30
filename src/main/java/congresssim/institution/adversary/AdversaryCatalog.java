package congresssim.institution.adversary;


import java.util.List;
import java.util.Optional;


public final class AdversaryCatalog
{
	public static final String CLAIM_BOUNDARY =
			"First-wave adversary specifications are simulator assumptions for bounded synthetic "
			+ "stress tests. They define actor objectives, budgets, information levels, and required "
			+ "outputs; they do not estimate real-world attack rates or validate institutional adoption claims.";

	private static final List<String> REQUIRED_TRACE_FIELDS = List.of(
			"seed",
			"caseKey",
			"scenarioKey",
			"mechanismFamily",
			"adversaryId",
			"actorType",
			"objective",
			"budgetUnit",
			"budgetValue",
			"informationLevel",
			"attackActionList",
			"preAttackFeatures",
			"postAttackFeatures",
			"institutionalPath",
			"baselineOutcome",
			"attackedOutcome",
			"successFlag",
			"metricDeltas",
			"administrativeBurden"
	);

	private static final List<AdversarySpec> FIRST_WAVE = List.of(
			new AdversarySpec(
					"A1",
					"Clone/decoy proposer",
					"Proposer, party, or lobby-aligned proposer",
					"Make content selection choose a worse alternative or dilute support for a good one.",
					List.of(InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("proposal_slots", "amendment_slots"),
					List.of("add_near_duplicate", "add_dominated_variant", "split_support_with_decoy"),
					"selected_bill_lower_than_best_available_support_or_benefit",
					"selected_bill_support_or_benefit_loss; low_support_enactment_change"
			),
			new AdversarySpec(
					"A2",
					"Poison-pill or sequencing actor",
					"Party, proposer, committee gatekeeper, or lobby group",
					"Block a high-benefit bill or pass it with a harmful rider.",
					List.of(InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("amendment_slots", "agenda_order_slots"),
					List.of("attach_harmful_rider", "add_private_gain_rider", "reorder_substitutes", "sequence_polarizing_amendment_first"),
					"high_benefit_bill_fails_or_passes_with_increased_harm_or_capture",
					"high_benefit_blockage_rate; enacted_harm_or_capture_added"
			),
			new AdversarySpec(
					"A3",
					"Public-input manipulator",
					"Outside campaign, lobby group, or panel manipulator",
					"Distort objection, petition, or panel signals.",
					List.of(InformationLevel.LOW, InformationLevel.MEDIUM),
					List.of("objections_filed", "public_attention_units", "panel_noise_intensity"),
					List.of("file_noisy_objections", "coordinate_repetitive_claims", "bias_panel_inputs", "increase_panel_noise"),
					"review_path_diverges_from_generated_support_or_benefit",
					"administrative_cost_added; false_positive_and_false_negative_public_input_errors"
			),
			new AdversarySpec(
					"A4",
					"Bad-faith harm claimant",
					"Outside campaign, party, affected-group proxy, or lobby group",
					"Trigger false-positive harm review or evade true harm review.",
					List.of(InformationLevel.MEDIUM),
					List.of("harm_claims_filed", "legal_attention_units"),
					List.of("exaggerate_harm", "duplicate_claims", "target_rivals", "understate_ally_harm"),
					"harm_review_blocks_non_harmful_bill_or_clears_harmful_bill",
					"false_positive_burden; false_negative_concentrated_harm_passage"
			),
			new AdversarySpec(
					"A5",
					"Proposal flooder",
					"Proposer, party, or lobby group",
					"Exhaust agenda, floor, or review capacity.",
					List.of(InformationLevel.LOW, InformationLevel.MEDIUM),
					List.of("proposal_slots", "lobbying_support_units"),
					List.of("submit_low_value_bills", "clone_bills", "submit_high_salience_noise", "submit_lobby_supported_low_support_bills"),
					"high_benefit_bills_crowded_out_or_low_support_bills_enacted",
					"floor_or_review_load_added; high_benefit_consideration_decline; low_support_enactment_change"
			),
			new AdversarySpec(
					"A6",
					"Lobbying camouflage actor",
					"Lobby group or proxy sponsor network",
					"Preserve private gain while evading anti-capture screens.",
					List.of(InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("lobbying_money", "proxy_sponsors", "issue_framing_units"),
					List.of("split_spend", "route_through_proxies", "mask_private_gain_as_technical_information"),
					"captured_bill_passes_anti_capture_or_access_screen",
					"capture_among_enacted_bills_added; visible_spend_decline_with_capture_persistence"
			),
			new AdversarySpec(
					"A7",
					"Administrative overload coalition",
					"Mixed coalition",
					"Saturate layered safeguards.",
					List.of(InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("proposals", "objections", "harm_claims", "lobbying_camouflage", "review_demand"),
					List.of("combine_flooding_claims_panel_noise_and_camouflage", "target_review_capacity", "force_queue_saturation"),
					"routing_or_review_capacity_saturated",
					"administrative_cost_added; queue_overflow; risk_control_degradation_after_overload"
			),
			new AdversarySpec(
					"A8",
					"Public-support distortion actor",
					"Outside campaign, lobby group, party, or proxy civic campaign",
					"Create false consensus, suppress support for a high-benefit bill, or inflate support for a private-gain bill.",
					List.of(InformationLevel.LOW, InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("public_campaign_spend", "attention_capacity", "salience_manipulation", "proxy_endorsements"),
					List.of("shift_cheap_public_signals", "amplify_distorted_salience", "target_generated_district_or_affected_group_support_proxies"),
					"public_support_signal_moves_away_from_generated_benefit_or_burden",
					"public_preference_distortion; low_support_enactment_change; popular_fail_change"
			),
			new AdversarySpec(
					"A9",
					"Mixed adversary portfolio",
					"Coordinated outside and inside actors",
					"Combine attacks so defenses that handle one stressor fail under interaction.",
					List.of(InformationLevel.MEDIUM, InformationLevel.HIGH),
					List.of("joint_budget_across_attack_actions"),
					List.of("allocate_budget_across_two_to_four_attack_types", "compare_to_strongest_same_budget_single_attack"),
					"joint_attack_succeeds_where_strongest_single_attack_does_not",
					"interaction_degradation; superadditive_loss; overload; recovery_failure"
			)
	);

	private AdversaryCatalog() {
	}

	public static List<AdversarySpec> firstWave() {
		return FIRST_WAVE;
	}

	public static List<String> requiredTraceFields() {
		return REQUIRED_TRACE_FIELDS;
	}

	public static Optional<AdversarySpec> find(String id) {
		return FIRST_WAVE.stream().filter(spec -> spec.id().equals(id)).findFirst();
	}
}
