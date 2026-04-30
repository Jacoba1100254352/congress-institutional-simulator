# Empirical Bridge

This bridge makes the validation gap explicit. It maps each desired real-world signal to an optional raw-data summary and to the closest current simulator calibration target. Missing raw datasets are reported as work remaining, not as a failed simulator run.

| Signal | Raw input/status | Simulator proxy | Observed | Target range | Bridge status |
| --- | --- | --- | ---: | --- | --- |
| Bill attrition | `bill_progression.csv` / enactmentRate = --- (missing) | `current-system` / productivity | 0.038 | 0.010--0.120 | needs raw dataset |
| Floor consideration | `bill_progression.csv` / floorLoad = --- (missing) | `current-system` / floor | 0.218 | 0.050--0.450 | needs raw dataset |
| Roll-call coalition size | `voteview_rollcalls.csv` / coalitionSize = --- (missing) | `current-system` / averageEnactedSupport | 0.668 | 0.500--0.820 | needs raw dataset |
| Party unity | `voteview_rollcalls.csv` / partyUnity = --- (missing) | `current-system` / averageEnactedSupport | 0.668 | 0.500--0.820 | needs raw dataset |
| Sponsor success concentration | `sponsor_success.csv` / sponsorSuccessGini = --- (missing) | `current-system` / proposerAccessGini | 0.137 | 0.050--0.750 | needs raw dataset |
| Lobby spending observability | `lobbying_disclosure.csv` / meanSpend = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Lobby spending concentration | `lobbying_disclosure.csv` / clientSpendGini = --- (missing) | `default-pass-budgeted-lobbying` / lobbySpendPerBill | 0.092 | 0.010--1.500 | needs raw dataset |
| Topic throughput | `topic_throughput.csv` / topicEnactmentRate = --- (missing) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | needs raw dataset |
