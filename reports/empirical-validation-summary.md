# Empirical Validation Summary

This report computes validation summaries when optional raw datasets are present under `data/validation/raw/`. Missing rows indicate absent local data, not a simulator failure.

| Dataset | Metric | Value | Status | Note |
| --- | --- | ---: | --- | --- |
| `voteview_rollcalls.csv` | missing | --- | missing | Add Voteview-like member vote rows to compute party unity and coalition size. |
| `bill_progression.csv` | floorLoad | 0.480000 | computed | Share of introduced bills receiving floor action. |
| `bill_progression.csv` | committeeReportRate | 0.266667 | computed | Share of introduced bills reported by committee. |
| `bill_progression.csv` | enactmentRate | 0.333333 | computed | Share of introduced bills enacted. |
| `lobbying_disclosure.csv` | missing | --- | missing | Add LDA-style client issue spending rows to compute spend concentration. |
| `topic_throughput.csv` | topicAgendaEntropy | 0.890123 | computed | Normalized diversity of introduced bills across topics. |
| `topic_throughput.csv` | topicFloorRate | 0.480000 | computed | Topic-weighted floor-consideration rate. |
| `topic_throughput.csv` | topicEnactmentRate | 0.333333 | computed | Topic-weighted enactment rate. |
| `sponsor_success.csv` | sponsorSuccessRate | 0.523810 | computed | Mean sponsor enactment rate. |
| `sponsor_success.csv` | sponsorSuccessGini | 0.492381 | computed | Gini concentration of enacted bills by sponsor. |
| `district_public_opinion.csv` | missing | --- | missing | Add district opinion rows to compute public-will intensity and affected-group representation. |
| `committee_activity.csv` | missing | --- | missing | Add committee activity rows to compute referral, reporting, hearing, and discharge rates. |
| `campaign_finance.csv` | recipientFinanceGini | 0.980469 | computed | Gini concentration of campaign money by recipient. |
| `campaign_finance.csv` | industryFinanceEntropy | 0.019252 | computed | Issue/industry diversity of campaign money. |
| `campaign_finance.csv` | outsideSpendingShare | 0.995979 | computed | Share of campaign money marked independent expenditure. |
| `court_review.csv` | missing | --- | missing | Add constitutional-court review rows to compute emergency-order and invalidation rates. |
| `comparative_institutions.csv` | missing | --- | missing | Add comparative-institution rows to compute chamber, party-system, and productivity benchmarks. |
