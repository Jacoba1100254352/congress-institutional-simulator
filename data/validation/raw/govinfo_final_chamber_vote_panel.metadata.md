# GovInfo Final Chamber-Vote Panel

- generated_at_utc: 2026-08-31T02:54:17+00:00
- selection_classifier_version: `govinfo-final-chamber-vote-v1`
- lifecycle_classification_version: `govinfo-bill-lifecycle-v3`
- configuration_sha256: `dcf503aeb2d808696d7e59451c42a70ccf2c7bef569f94cb6679e776798416d5`
- builder_sha256: `e2776719986fad1554097cc14733e593ce07dd19808022259e4b92b96181df24`
- lifecycle_builder_sha256: `75587c72a049635cea9c70d7cf48adda1e4f7d0a4e7bc468796ef23f199a0422`
- output_sha256: `539c497f8a6f0349fe284048228d652cb43cd9da42bec77da15ba72e63ed149c`
- official_source_manifest_sha256: `4a3e6ba5cd7235575422ac26222eee8a4b9d9a42ba4f1d38fa21a17e37e09ff2`
- decision_panel_sha256: `5ca526f1036d47bd8e5249e8f716063f493ee0060fb99604cccc01d265702795`
- presented_measures: 4208
- chamber_rows: 8416
- official_roll_call_rows: 1685
- nonrecorded_final_approval_rows: 6731
- measures_with_both_final_roll_calls: 310
- unique_official_vote_sources: 1685

## Coverage

| Measure class | Selection status | Chamber rows |
| --- | --- | ---: |
| bill | `final_approval_without_recorded_vote` | 6516 |
| bill | `official_roll_call_selected` | 1526 |
| joint resolution | `final_approval_without_recorded_vote` | 215 |
| joint resolution | `official_roll_call_selected` | 159 |

## Operational Definition

- The population is every H.R., S., H.J.Res., and S.J.Res. measure classified as presented to the President in the committed 108th-118th Congress decision panels.
- Each measure contributes one House row and one Senate row. The selected event is the latest successful final passage, concurrence, or conference-report approval action in that chamber on or before presentment.
- Motions to proceed, instruct, recommit, reconsider, table, invoke cloture, postpone, or decide consideration are excluded even when their text contains an affirmative result.
- A roll call is retained only when the selected final approval action itself carries a GovInfo recorded-vote reference. Earlier roll calls are not substituted for a later voice vote or unanimous-consent approval.
- Recorded votes are parsed from official House Clerk or Senate LIS XML. Overall and party support shares use yea divided by yea plus nay; present, absent, and not-voting members are excluded from that denominator.
- When one official Senate roll-call question expressly names several measures but the document field names only one, each named measure is labeled `matched_grouped_question`; the representative document identifier remains unchanged in the panel.
- H.R./S. bills and joint resolutions remain separately labeled. Constitutional-amendment joint resolutions never presented to the President are outside this decision population.

Claim boundary: final chamber-vote support is post-passage descriptive context for presidential decisions. The panel does not identify causal presidential preferences, legislator ideal points, public opinion, bill quality, welfare, or institutional rank. Missing roll calls are observed voice-vote or unanimous-consent pathways and are not imputed.
