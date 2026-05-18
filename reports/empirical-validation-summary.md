# Empirical Validation Summary

This report computes empirical comparison summaries when optional raw datasets are present under `data/validation/raw/`. Missing rows indicate absent local data, not a simulator failure. Adapter fixtures under `data/validation/fixtures/` are ignored because they test parser shape rather than empirical fit.

| Dataset | Metric | Value | Status | Note |
| --- | --- | ---: | --- | --- |
| `voteview_rollcalls.csv` | partyUnity | 0.946078 | computed | Mean within-party majority vote share by roll call. |
| `voteview_rollcalls.csv` | coalitionSize | 0.604453 | computed | Mean winning-side share by roll call. |
| `bill_progression.csv` | floorLoad | 0.122222 | computed | Share of introduced bills receiving floor action. |
| `bill_progression.csv` | committeeReportRate | 0.083333 | computed | Share of introduced bills reported by committee. |
| `bill_progression.csv` | enactmentRate | 0.016667 | computed | Share of introduced bills enacted. |
| `lobbying_disclosure.csv` | meanSpend | 308.219178 | computed | Mean disclosed spending row amount. |
| `lobbying_disclosure.csv` | clientSpendGini | 0.976526 | computed | Gini concentration of spending by client. |
| `lobbying_disclosure.csv` | issueEntropy | 0.891519 | computed | Normalized issue diversity in lobbying rows. |
| `topic_throughput.csv` | topicAgendaEntropy | 0.885219 | computed | Normalized diversity of introduced bills across topics. |
| `topic_throughput.csv` | topicFloorRate | 0.122222 | computed | Topic-weighted floor-consideration rate. |
| `topic_throughput.csv` | topicEnactmentRate | 0.016667 | computed | Topic-weighted enactment rate. |
| `sponsor_success.csv` | sponsorSuccessRate | 0.000000 | computed | Mean sponsor enactment rate. |
| `sponsor_success.csv` | sponsorIntroductionGini | 0.388636 | computed | Gini concentration of introduced bills by sponsor. |
| `sponsor_success.csv` | sponsorSuccessGini | 0.000000 | computed | Gini concentration of enacted bills by sponsor. |
| `district_public_opinion.csv` | missing | --- | missing | Add district opinion rows to compute public-will intensity and affected-group representation. |
| `committee_activity.csv` | committeeReportRate | 0.083333 | computed | Reported bills per referred bill. |
| `committee_activity.csv` | hearingPerReferral | 0.000000 | computed | Hearings per referred bill. |
| `committee_activity.csv` | amendmentPerReferral | 0.000000 | computed | Amendments per referred bill. |
| `committee_activity.csv` | dischargeRate | 0.000000 | computed | Discharge petitions or bypasses per referred bill. |
| `campaign_finance.csv` | missing | --- | missing | Add campaign-finance rows to compute private-spending concentration and outside-spending share. |
| `court_review.csv` | missing | --- | missing | Add constitutional-court review rows to compute emergency-order and invalidation rates. |
| `rulemaking_implementation.csv` | missing | --- | missing | Add Federal Register/Unified Agenda/Regulations.gov-style rows to compute implementation delay and failure risk. |
| `law_revision_history.csv` | missing | --- | missing | Add law-lineage rows to compute amendment, reauthorization, repeal, expiration, and invalidation rates. |
| `comparative_institutions.csv` | missing | --- | missing | Add comparative-institution rows to compute chamber, party-system, and productivity benchmarks. |
