# Empirical Bridge

This bridge makes the validation gap explicit. It maps each desired real-world signal to an optional raw-data summary and to the closest current simulator calibration target. Missing raw datasets are reported as work remaining, not as a failed simulator run.

| Signal | Raw input/status | Simulator proxy | Observed | Target range | Bridge status |
| --- | --- | --- | ---: | --- | --- |
| Bill attrition | `bill_progression.csv` / enactmentRate = 0.333333 (computed) | `current-system` / productivity | 0.038 | 0.010--0.120 | raw summary available |
| Floor consideration | `bill_progression.csv` / floorLoad = 0.480000 (computed) | `current-system` / floor | 0.218 | 0.050--0.450 | raw summary available |
| Roll-call coalition size | `voteview_rollcalls.csv` / coalitionSize = --- (missing) | `current-system` / averageEnactedSupport | 0.668 | 0.500--0.820 | needs raw dataset |
| Party unity | `voteview_rollcalls.csv` / partyUnity = --- (missing) | `current-system` / averageEnactedSupport | 0.668 | 0.500--0.820 | needs raw dataset |
| Sponsor success concentration | `sponsor_success.csv` / sponsorSuccessGini = 0.492381 (computed) | `current-system` / proposerAccessGini | 0.137 | 0.050--0.750 | raw summary available |
| Lobby spending observability | `lobbying_disclosure.csv` / meanSpend = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Lobby spending concentration | `lobbying_disclosure.csv` / clientSpendGini = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Topic throughput | `topic_throughput.csv` / topicEnactmentRate = 0.333333 (computed) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | raw summary available |
| District public will | `district_public_opinion.csv` / intensityWeightedSupport = --- (missing) | --- | --- | --- | missing calibration target |
| District turnout skew | `district_public_opinion.csv` / turnoutGini = --- (missing) | --- | --- | --- | missing calibration target |
| Committee reporting | `committee_activity.csv` / committeeReportRate = --- (missing) | `current-system` / floor | 0.218 | 0.050--0.450 | needs raw dataset |
| Campaign finance concentration | `campaign_finance.csv` / recipientFinanceGini = 0.980469 (computed) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | raw summary available |
| Outside spending share | `campaign_finance.csv` / outsideSpendingShare = 0.995979 (computed) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | raw summary available |
| Court emergency posture | `court_review.csv` / emergencyOrderRate = --- (missing) | --- | --- | --- | missing calibration target |
| Court invalidation | `court_review.csv` / invalidationRate = --- (missing) | --- | --- | --- | missing calibration target |
| Comparative bicameralism | `comparative_institutions.csv` / bicameralShare = --- (missing) | --- | --- | --- | missing calibration target |
| Comparative productivity | `comparative_institutions.csv` / meanLegislativeProductivity = --- (missing) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | needs raw dataset |
