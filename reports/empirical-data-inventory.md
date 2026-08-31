# Empirical Data Inventory

This registry-backed inventory lists each planned empirical source family, its local raw or cached support, and the boundary it can currently support. It is an evidence inventory, not a validation claim.

- Source families: 13
- Ready or cached source families: 13
- Fixture-only families: 0
- Missing or schema-gap families: 0

Boundary categories:
- calibration proxy: 2
- flow sanity check: 2
- held-out benchmark: 9

| Source family | Dataset | Inventory status | Boundary | Rows | Related cohort | Date range | Evidence |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| Congress.gov bill histories | `bill_progression.csv` | ready | calibration proxy | 180 | --- | 2023-01-03..2024-12-23 | raw summary available |
| govinfo bill and action records | `govinfo_bill_census.csv` | ready | held-out benchmark | 15066 | `data/validation/raw/govinfo_bill_census_116.csv` (14148 rows; 2019-01-03..2021-01-13); `data/validation/raw/govinfo_bill_census_118.csv` (16213 rows; 2023-01-03..2025-01-06); `data/validation/raw/govinfo_executive_action_panel.csv` (4021 rows; 2003-01-08..2025-01-06); `data/validation/raw/govinfo_joint_resolution_panel.csv` (187 rows; 2003-01-09..2024-05-31); `data/validation/raw/govinfo_final_chamber_vote_panel.csv` (8416 rows; 2003-01-07..2024-12-21) | 2021-01-03..2023-01-05 | held-out benchmark: pass; reported |
| Voteview roll-call data | `voteview_rollcalls.csv` | ready | held-out benchmark | 83636 | --- | --- | held-out benchmark: pass; reported |
| Comparative Agendas topic throughput | `topic_throughput.csv` | ready | flow sanity check | 28 | --- | --- | raw summary bridge: raw summary available |
| QoG and V-Dem comparative institutions | `comparative_institutions.csv` | ready | held-out benchmark | 130 | --- | 2011..2020 | held-out benchmark: pass; reported |
| Senate LDA lobbying disclosures | `lobbying_disclosure.csv` | ready | calibration proxy | 146 | --- | 2024-first..2024-first | raw summary bridge: raw summary available |
| OpenFEC campaign finance | `campaign_finance.csv` | ready | held-out benchmark | 194 | --- | 2024..2024 | held-out benchmark: pass |
| Center for Effective Lawmaking and sponsor histories | `sponsor_success.csv` | ready | held-out benchmark | 22 | --- | --- | held-out benchmark: pass; reported |
| District public opinion and affected groups | `district_public_opinion.csv` | ready | held-out benchmark | 1305 | --- | 2024..2024 | held-out benchmark: pass |
| Committee hearing markup referral and discharge records | `committee_activity.csv` | ready | flow sanity check | 28 | --- | --- | raw summary bridge: raw summary available; missing flow-check proxy |
| Court review and invalidation | `court_review.csv` | ready | held-out benchmark | 9341 | --- | --- | held-out benchmark: pass; reported |
| Rulemaking implementation and enforcement | `rulemaking_implementation.csv` | ready | held-out benchmark | 500 | --- | 2024-11-29..2028-09-30 | held-out benchmark: pass; reported |
| Statutory revision and law lineage | `law_revision_history.csv` | ready | held-out benchmark | 120 | --- | 2021-04-14..2025-01-06 | held-out benchmark: pass; reported |
