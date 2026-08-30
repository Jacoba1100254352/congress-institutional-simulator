# Voteview Bill Linkage

This report derives a bounded vote-level bill-number crosswalk from cached Voteview roll-call rows and cached Voteview roll-call metadata. It is a linkage inventory, not bill-level roll-call validation.

- Voteview roll-call metadata rows represented: 320
- Roll-call member-vote rows represented: 83636
- Voteview roll-call rows with normalized bill IDs: 193
- Member-vote rows on roll calls with normalized bill IDs: 64894
- Voteview roll-call rows matching cached Congress.gov bill-progression rows: 8
- Member-vote rows matching cached Congress.gov bill-progression rows: 3075

Claim boundary: this context attaches Voteview roll-call metadata and parsed bill numbers to sampled roll-call IDs. It does not provide complete roll-call-to-bill coverage, district public-opinion support, sponsor-effectiveness evidence, public-law/statute lineage for most rows, implementation or court outcomes, public benefit, welfare, causal influence, or model validation.

Bill match statuses:
- bill_progression_metadata: 8
- missing_bill_number: 19
- nomination_or_nonbill_vote: 108
- voteview_bill_number_only: 185

Chambers:
- House: 160
- Senate: 160

| Vote | Bill | Status | Member-vote rows | Question | Missing links |
| --- | --- | --- | ---: | --- | --- |
| `118-House-29` | `118-hconres-3` | bill_progression_metadata | 429 | On Agreeing to the Resolution | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-137` | `118-hr-140` | bill_progression_metadata | 428 | On Agreeing to the Amendment | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-138` | `118-hr-140` | bill_progression_metadata | 428 | On Agreeing to the Amendment | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-102` | `118-hr-139` | bill_progression_metadata | 425 | On Passage | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-140` | `118-hr-140` | bill_progression_metadata | 423 | On Passage | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-31` | `118-hr-159` | bill_progression_metadata | 422 | On Motion to Suspend the Rules and Pass, as Amended | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-139` | `118-hr-140` | bill_progression_metadata | 420 | On Motion to Recommit | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-Senate-99` | `118-sjres-4` | bill_progression_metadata | 100 | On Cloture on the Motion to Proceed | district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-1` | `---` | missing_bill_number | 432 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-112` | `118-hr-185` | voteview_bill_number_only | 432 | On Agreeing to the Amendment | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-18` | `---` | missing_bill_number | 432 | On Motion to Adjourn | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-2` | `---` | missing_bill_number | 432 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-3` | `---` | missing_bill_number | 432 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-113` | `118-hr-185` | voteview_bill_number_only | 431 | On Agreeing to the Amendment | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-22` | `118-hres-5` | voteview_bill_number_only | 431 | On Agreeing to the Resolution | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-38` | `118-hr-21` | voteview_bill_number_only | 431 | On Agreeing to the Amendment | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-39` | `118-hr-21` | voteview_bill_number_only | 431 | On Agreeing to the Amendment | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-4` | `---` | missing_bill_number | 431 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-5` | `---` | missing_bill_number | 431 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
| `118-House-6` | `---` | missing_bill_number | 431 | Election of the Speaker | cached_bill_progression_overlap; district_public_opinion_issue; sponsor_success_or_member_effectiveness; public_law_or_statute_for_most_rows; implementation_or_court_outcome; model_validation |
