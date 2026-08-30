# Empirical Flow Sanity Checks

These checks make the empirical boundary explicit. They map each desired real-world signal to an optional raw-data summary and to the closest simulator flow-check proxy. Missing raw datasets are reported as work remaining, not as a failed simulator run.

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
| District public will | `district_public_opinion.csv` / intensityWeightedSupport = 0.515156 (computed) | `district-population-majority` / districtAlignment | 0.393 | 0.200--0.800 | raw summary available |
| District turnout skew | `district_public_opinion.csv` / turnoutGini = 0.051513 (computed) | `district-population-majority` / turnoutSkewIndex | 0.254 | 0.000--0.400 | raw summary available |
| Committee reporting | `committee_activity.csv` / committeeReportRate = 0.083333 (computed) | `current-system` / floor | 0.218 | 0.080--0.320 | raw summary available |
| Campaign finance concentration | `campaign_finance.csv` / recipientFinanceGini = 0.935526 (computed) | `influence-system-majority` / campaignFinanceCaptureIndex | 0.144 | 0.000--1.000 | raw summary available |
| Outside spending share | `campaign_finance.csv` / outsideSpendingShare = 0.982998 (computed) | `influence-system-majority` / campaignFinanceCaptureIndex | 0.144 | 0.000--1.000 | raw summary available |
| Court emergency posture | `court_review.csv` / emergencyOrderRate = 0.000000 (computed) | `constitutional-court-architecture-majority` / constitutionalInvalidationRate | 0.000 | 0.000--0.200 | raw summary available |
| Court invalidation | `court_review.csv` / invalidationRate = 0.071834 (computed) | `constitutional-court-architecture-majority` / constitutionalInvalidationRate | 0.000 | 0.000--0.200 | raw summary available |
| Rulemaking effective-date coverage | `rulemaking_implementation.csv` / effectiveDateCoverage = 0.884000 (computed) | `law-registry-majority` / implementationDelay | 0.486 | 0.000--100.000 | raw summary available |
| Rulemaking final-to-effective delay | `rulemaking_implementation.csv` / meanFinalToEffectiveDays = 31.696833 (computed) | `law-registry-majority` / implementationDelay | 0.486 | 0.000--100.000 | raw summary available |
| Rulemaking implementation-speed proxy | `rulemaking_implementation.csv` / meanEnforcementCapacity = 0.834500 (computed) | `law-registry-majority` / implementationCapacity | 0.184 | 0.000--1.000 | raw summary available |
| Law revision correction text | `law_revision_history.csv` / postEnactmentCorrectionRate = 0.375000 (computed) | `law-registry-majority` / reversalRate | 0.420 | 0.000--0.800 | raw summary available |
| Law revision repeal text | `law_revision_history.csv` / repealRate = 0.066667 (computed) | `law-registry-majority` / reversalRate | 0.420 | 0.000--0.800 | raw summary available |
| Comparative bicameralism | `comparative_institutions.csv` / bicameralShare = 0.238462 (computed) | `bicameral-majority` / interChamberConflictRate | 0.148 | 0.050--0.600 | raw summary available |
| Comparative legislative capacity | `comparative_institutions.csv` / meanLegislativeProductivity = 0.693985 (computed) | `simple-majority` / welfarePerSubmittedBill | 0.145 | 0.050--0.450 | raw summary available |
