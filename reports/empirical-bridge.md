# Empirical Bridge

This bridge makes the validation gap explicit. It maps each desired real-world signal to an optional raw-data summary and to the closest current simulator calibration target. Missing raw datasets are reported as work remaining, not as a failed simulator run.

| Signal | Raw input/status | Simulator proxy | Observed | Target range | Bridge status |
| --- | --- | --- | ---: | --- | --- |
| Bill attrition | `bill_progression.csv` / enactmentRate = 0.016667 (computed) | `current-system` / productivity | 0.038 | 0.010--0.070 | raw summary available |
| Floor consideration | `bill_progression.csv` / floorLoad = 0.122222 (computed) | `current-system` / floor | 0.218 | 0.080--0.320 | raw summary available |
| Committee reporting from bill actions | `bill_progression.csv` / committeeReportRate = 0.083333 (computed) | `current-system` / floor | 0.218 | 0.080--0.320 | raw summary available |
| Roll-call coalition size | `voteview_rollcalls.csv` / coalitionSize = 0.604453 (computed) | `current-system` / averageEnactedSupport | 0.668 | 0.560--0.780 | raw summary available |
| Party unity | `voteview_rollcalls.csv` / partyUnity = 0.946078 (computed) | `current-system` / averageEnactedSupport | 0.668 | 0.560--0.780 | raw summary available |
| Sponsor proposal concentration | `sponsor_success.csv` / sponsorIntroductionGini = 0.388636 (computed) | `current-system` / proposerAccessGini | 0.137 | 0.050--0.550 | raw summary available |
| Sponsor enacted-success concentration | `sponsor_success.csv` / sponsorSuccessGini = 0.000000 (computed) | `current-system` / proposerAccessGini | 0.137 | 0.050--0.550 | raw summary available |
| Lobby spending observability | `lobbying_disclosure.csv` / meanSpend = 308.219178 (computed) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | raw summary available |
| Lobby spending concentration | `lobbying_disclosure.csv` / clientSpendGini = 0.976526 (computed) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | raw summary available |
| Topic throughput | `topic_throughput.csv` / topicEnactmentRate = 0.016667 (computed) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | raw summary available |
| District public will | `district_public_opinion.csv` / intensityWeightedSupport = --- (missing) | --- | --- | --- | missing calibration target |
| District turnout skew | `district_public_opinion.csv` / turnoutGini = --- (missing) | --- | --- | --- | missing calibration target |
| Committee reporting | `committee_activity.csv` / committeeReportRate = 0.083333 (computed) | `current-system` / floor | 0.218 | 0.080--0.320 | raw summary available |
| Campaign finance concentration | `campaign_finance.csv` / recipientFinanceGini = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Outside spending share | `campaign_finance.csv` / outsideSpendingShare = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Court emergency posture | `court_review.csv` / emergencyOrderRate = --- (missing) | --- | --- | --- | missing calibration target |
| Court invalidation | `court_review.csv` / invalidationRate = --- (missing) | --- | --- | --- | missing calibration target |
| Comparative bicameralism | `comparative_institutions.csv` / bicameralShare = --- (missing) | --- | --- | --- | missing calibration target |
| Comparative productivity | `comparative_institutions.csv` / meanLegislativeProductivity = --- (missing) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | needs raw dataset |
