# Adversary Catalog

Status: `schema_only_not_experiment_evidence`.

First-wave adversary specifications are simulator assumptions for bounded synthetic stress tests. They define actor objectives, budgets, information levels, and required outputs; they do not estimate real-world attack rates or validate institutional adoption claims.

- First-wave adversaries: 9
- Required trace fields: 19

| ID | Name | Information | Budget units | Success metric | Degradation metric |
| --- | --- | --- | --- | --- | --- |
| A1 | Clone/decoy proposer | medium; high | proposal_slots; amendment_slots | selected_bill_lower_than_best_available_support_or_benefit | selected_bill_support_or_benefit_loss; low_support_enactment_change |
| A2 | Poison-pill or sequencing actor | medium; high | amendment_slots; agenda_order_slots | high_benefit_bill_fails_or_passes_with_increased_harm_or_capture | high_benefit_blockage_rate; enacted_harm_or_capture_added |
| A3 | Public-input manipulator | low; medium | objections_filed; public_attention_units; panel_noise_intensity | review_path_diverges_from_generated_support_or_benefit | administrative_cost_added; false_positive_and_false_negative_public_input_errors |
| A4 | Bad-faith harm claimant | medium | harm_claims_filed; legal_attention_units | harm_review_blocks_non_harmful_bill_or_clears_harmful_bill | false_positive_burden; false_negative_concentrated_harm_passage |
| A5 | Proposal flooder | low; medium | proposal_slots; lobbying_support_units | high_benefit_bills_crowded_out_or_low_support_bills_enacted | floor_or_review_load_added; high_benefit_consideration_decline; low_support_enactment_change |
| A6 | Lobbying camouflage actor | medium; high | lobbying_money; proxy_sponsors; issue_framing_units | captured_bill_passes_anti_capture_or_access_screen | capture_among_enacted_bills_added; visible_spend_decline_with_capture_persistence |
| A7 | Administrative overload coalition | medium; high | proposals; objections; harm_claims; lobbying_camouflage; review_demand | routing_or_review_capacity_saturated | administrative_cost_added; queue_overflow; risk_control_degradation_after_overload |
| A8 | Public-support distortion actor | low; medium; high | public_campaign_spend; attention_capacity; salience_manipulation; proxy_endorsements | public_support_signal_moves_away_from_generated_benefit_or_burden | public_preference_distortion; low_support_enactment_change; popular_fail_change |
| A9 | Mixed adversary portfolio | medium; high | joint_budget_across_attack_actions | joint_attack_succeeds_where_strongest_single_attack_does_not | interaction_degradation; superadditive_loss; overload; recovery_failure |

## Required Trace Fields

- `seed`
- `caseKey`
- `scenarioKey`
- `mechanismFamily`
- `adversaryId`
- `actorType`
- `objective`
- `budgetUnit`
- `budgetValue`
- `informationLevel`
- `attackActionList`
- `preAttackFeatures`
- `postAttackFeatures`
- `institutionalPath`
- `baselineOutcome`
- `attackedOutcome`
- `successFlag`
- `metricDeltas`
- `administrativeBurden`
