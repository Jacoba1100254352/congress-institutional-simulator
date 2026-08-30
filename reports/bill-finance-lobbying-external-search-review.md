# Bill Finance/Lobbying External-Search Review

This report reviews the 10 bill-finance/lobbying queue rows against a targeted official LDA current-bill activity-text search and records the FEC/OpenFEC source scope needed for later campaign-finance target review. It is source-search evidence, not influence or validation evidence.

- Queued public-law rows reviewed: 10
- Rows with exact external LDA current-bill activity-text mentions: 2
- Exact external LDA activity-text mention rows: 55
- Rows with complete external LDA search and no exact current-bill activity-text mention: 8
- Rows with partial/error LDA search status: 0
- Rows still requiring campaign-finance candidate/committee/outside-spending target-scope review: 4

Claim boundary: External source-search review only; exact LDA activity-text bill mentions show disclosed lobbying activity text that mentions the reviewed current bill, and FEC source-scope triage identifies public candidate/committee/outside-spending fields needed for later review. This does not show lobbying contacts, support, opposition, campaign spending for or against a bill, sponsor/member targeting, committee-action influence, roll-call influence, legislative-outcome causality, public benefit or welfare, causal capture, or model validation. Public FEC/OpenFEC source-scope triage only; public FEC records expose candidate, committee, receipt, and independent-expenditure target fields, not bill IDs or bill-specific campaign-finance influence.

Combined external review statuses:
- external_lda_bill_reference_found: 2
- external_lda_no_exact_match_campaign_target_scope_pending: 4
- external_search_review_no_exact_lda_match_campaign_not_scoped: 4

| Rank | Bill | Public law | LDA disposition | Exact LDA rows | Campaign scope | Combined status |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | `117-hr-6386` | `117-295` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | fec_public_records_need_candidate_committee_or_outside_spending_target_join | external_lda_no_exact_match_campaign_target_scope_pending |
| 2 | `117-hr-1842` | `117-163` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | campaign_finance_external_search_not_in_current_row_scope | external_search_review_no_exact_lda_match_campaign_not_scoped |
| 3 | `117-hr-3359` | `117-164` | official_lda_external_current_bill_activity_text_match | 46 | campaign_finance_external_search_not_in_current_row_scope | external_lda_bill_reference_found |
| 4 | `117-hr-4693` | `117-214` | official_lda_external_current_bill_activity_text_match | 9 | campaign_finance_external_search_not_in_current_row_scope | external_lda_bill_reference_found |
| 5 | `117-hr-6899` | `117-185` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | campaign_finance_external_search_not_in_current_row_scope | external_search_review_no_exact_lda_match_campaign_not_scoped |
| 6 | `117-hr-7334` | `117-165` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | campaign_finance_external_search_not_in_current_row_scope | external_search_review_no_exact_lda_match_campaign_not_scoped |
| 7 | `117-s-3470` | `117-211` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | fec_public_records_need_candidate_committee_or_outside_spending_target_join | external_lda_no_exact_match_campaign_target_scope_pending |
| 8 | `117-s-3969` | `117-182` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | fec_public_records_need_candidate_committee_or_outside_spending_target_join | external_lda_no_exact_match_campaign_target_scope_pending |
| 9 | `117-s-3294` | `117-111` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | fec_public_records_need_candidate_committee_or_outside_spending_target_join | external_lda_no_exact_match_campaign_target_scope_pending |
| 10 | `117-s-497` | `117-121` | official_lda_external_search_no_exact_current_bill_activity_text_match | 0 | campaign_finance_external_search_not_in_current_row_scope | external_search_review_no_exact_lda_match_campaign_not_scoped |
