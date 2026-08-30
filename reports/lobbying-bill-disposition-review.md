# LDA Bill Disposition/Target Review

This report prioritizes exact LDA bill-text rows for manual disposition and target review. It is a source-review queue, not evidence that lobbying targeted or changed any legislative action or outcome.

- Exact LDA bill-text rows represented: 484
- Rows needing manual disposition or target review: 156
- High-priority review rows: 4
- Medium-priority review rows: 152
- Low-priority bill-reference-only rows: 328
- Support-only rows: 46
- Opposition-only rows: 3
- Mixed support/opposition rows: 2
- Position/activity rows: 104
- Bill-list/title-only rows: 329
- Possible member/committee reference rows: 2
- Rows with committee-reported metadata: 421
- Rows with floor-considered metadata: 484
- Rows with enacted public-law metadata: 484

Claim boundary: LDA disposition/target source-review queue only; deterministic text signals and possible target references are not manual disposition confirmation, sponsor/member targeting evidence, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, welfare, causal capture, or model validation.

Review priorities:
- high: 4
- low: 328
- medium: 152

Text review statuses:
- exact_bill_text_bill_list_or_title_only: 329
- exact_bill_text_with_explicit_opposition_signal: 3
- exact_bill_text_with_explicit_support_signal: 46
- exact_bill_text_with_mixed_support_opposition_signal: 2
- exact_bill_text_with_position_or_activity_signal: 104

Top priority rows:

| Rank | Priority | Bill | Public law | Client | Status | Target status | Reason | Next review |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | high | `117-hr-7776` | `117-263` | RAYMOND BASIN MANAGEMENT BOARD | exact_bill_text_with_explicit_support_signal | possible_member_or_committee_reference_needs_manual_target_review | support_signal; possible_member_or_committee_reference | Inspect filing text and linked Congress.gov bill/action metadata for manual disposition and target/outcome context. |
| 2 | high | `117-s-3373` | `117-168` | AFGE NATIONAL VA COUNCIL | exact_bill_text_with_mixed_support_opposition_signal | chamber_entity_context_only_no_specific_target_detected | mixed_support_opposition_signal | Inspect filing text and linked Congress.gov bill/action metadata for manual disposition and target/outcome context. |
| 3 | high | `117-s-3373` | `117-168` | AMERICAN FED OF GOVERNMENT EMPLOYEES AFL-CIO | exact_bill_text_with_mixed_support_opposition_signal | chamber_entity_context_only_no_specific_target_detected | mixed_support_opposition_signal | Inspect filing text and linked Congress.gov bill/action metadata for manual disposition and target/outcome context. |
| 4 | high | `117-s-4900` | `117-183` | THE INSTITUTE OF ELECTRICAL AND ELECTRONICS ENGINEERS | exact_bill_text_bill_list_or_title_only | possible_member_or_committee_reference_needs_manual_target_review | possible_member_or_committee_reference | Inspect filing text and linked Congress.gov bill/action metadata for manual disposition and target/outcome context. |
| 5 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 6 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 7 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 8 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 9 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 10 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 11 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 12 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 13 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 14 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 15 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 16 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 17 | medium | `117-hr-1437` | `117-229` | JACOBS SOLUTIONS, INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 18 | medium | `117-hr-1437` | `117-229` | AMERICAN SOCIETY OF CIVIL ENGINEERS | exact_bill_text_with_explicit_support_signal | chamber_entity_context_only_no_specific_target_detected | support_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 19 | medium | `117-hr-1437` | `117-229` | ASSURANT INC | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
| 20 | medium | `117-hr-1437` | `117-229` | EMERGENT BIOSOLUTIONS INC. | exact_bill_text_with_position_or_activity_signal | chamber_entity_context_only_no_specific_target_detected | position_or_activity_signal | Manually confirm direction/position and check whether the filing names a target, member, or committee rather than only a chamber/entity. |
