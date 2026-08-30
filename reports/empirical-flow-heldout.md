# Empirical Held-Out Benchmarks

This report runs deterministic held-out checks on committed raw empirical samples. These are source-family benchmarks for legislative flow, roll-call behavior, sponsor proposal access, campaign-finance concentration, district public-will proxies, court review, implementation delay, law revision, and comparative institutional context. They are not validation of public benefit, welfare, bill-specific public support, harm, capture, representation, or institutional rankings.

- Source families with held-out rows: 9
- Targeted held-out checks passing: 14 / 14

| Source family | Metric | Calibration slice | Held-out slice | All rows | Units | Simulator observed | Target range | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| govinfo bill and action records | enactmentRate | 0.022607 | 0.024927 | 0.023762 | 7564 / 7502 bills | 0.027 | 0.012--0.033 | pass |
| govinfo bill and action records | floorLoad | 0.065442 | 0.067715 | 0.066574 | 7564 / 7502 bills | 0.064 | 0.050--0.081 | pass |
| govinfo bill and action records | committeeReportRate | 0.063194 | 0.065183 | 0.064184 | 7564 / 7502 bills | --- | --- | reported |
| govinfo bill and action records | committeeAdvanceRate | 0.099154 | 0.101440 | 0.100292 | 7564 / 7502 bills | 0.107 | 0.079--0.120 | pass |
| govinfo bill and action records | originPassageRate | 0.064384 | 0.067182 | 0.065777 | 7564 / 7502 bills | --- | --- | reported |
| govinfo bill and action records | completedCongressionalPassageRate | 0.022607 | 0.024927 | 0.023762 | 7564 / 7502 bills | --- | --- | reported |
| Voteview roll-call data | coalitionSize | 0.619547 | 0.588782 | 0.604453 | 163 / 157 roll calls | 0.668 | 0.560--0.780 | pass |
| Voteview roll-call data | partyUnity | 0.939404 | 0.953025 | 0.946078 | 163 / 157 roll calls | --- | --- | reported |
| Center for Effective Lawmaking and sponsor histories | sponsorIntroductionGini | 0.313131 | 0.438017 | 0.388636 | 11 / 11 sponsors | 0.137 | 0.050--0.550 | pass |
| Center for Effective Lawmaking and sponsor histories | sponsorSuccessGini | 0.000000 | 0.000000 | 0.000000 | 11 / 11 sponsors | --- | --- | reported |
| OpenFEC campaign finance | recipientFinanceGini | 0.891986 | 0.912195 | 0.935526 | 91 / 103 transactions | 0.144 | 0.000--1.000 | pass |
| OpenFEC campaign finance | outsideSpendingShare | 0.994662 | 0.964491 | 0.982998 | 91 / 103 transactions | 0.144 | 0.000--1.000 | pass |
| District public opinion and affected groups | intensityWeightedSupport | 0.508576 | 0.522059 | 0.515156 | 223 / 213 districts | 0.394 | 0.200--0.800 | pass |
| District public opinion and affected groups | turnoutGini | 0.050825 | 0.052171 | 0.051513 | 223 / 213 districts | 0.254 | 0.000--0.400 | pass |
| Court review and invalidation | invalidationRate | 0.070282 | 0.073346 | 0.071834 | 4610 / 4731 cases | 0.000 | 0.000--0.200 | pass |
| Court review and invalidation | signedOpinionRate | 0.785900 | 0.782076 | 0.783963 | 4610 / 4731 cases | --- | --- | reported |
| Rulemaking implementation and enforcement | meanFinalToEffectiveDays | 37.102804 | 26.622807 | 31.696833 | 246 / 254 final rules | 0.505 | 0.000--100.000 | pass |
| Rulemaking implementation and enforcement | effectiveDateCoverage | 0.869919 | 0.897638 | 0.884000 | 246 / 254 final rules | --- | --- | reported |
| Rulemaking implementation and enforcement | meanEnforcementCapacity | 0.816057 | 0.852362 | 0.834500 | 246 / 254 final rules | 0.174 | 0.000--1.000 | pass |
| Statutory revision and law lineage | postEnactmentCorrectionRate | 0.368421 | 0.380952 | 0.375000 | 57 / 63 public laws | 0.469 | 0.000--0.800 | pass |
| Statutory revision and law lineage | repealRate | 0.052632 | 0.079365 | 0.066667 | 57 / 63 public laws | --- | --- | reported |
| QoG and V-Dem comparative institutions | bicameralShare | 0.227273 | 0.250000 | 0.238462 | 66 / 64 country-years | 0.148 | 0.050--0.600 | pass |
| QoG and V-Dem comparative institutions | meanJudicialReviewStrength | 0.694924 | 0.670250 | 0.682777 | 66 / 64 country-years | --- | --- | reported |

Boundary notes:

- The GovInfo bill census supports deterministic within-117th-Congress legislative-flow benchmarking only; a later Congress is still required for temporal replication.
- Voteview roll-call rows support held-out coalition-size and party-unity plausibility only; they do not validate district public opinion, representation, or generated public benefit.
- Sponsor rows support held-out proposal-access concentration benchmarking only; they do not validate full member effectiveness or bill-level sponsor success.
- Campaign-finance rows support held-out concentration and outside-spending observability only; they do not validate bill-level influence or capture.
- District public-opinion rows support held-out district proxy stability only; they do not validate bill-topic support, MRP estimates, or affected-group harm.
- Court-review rows support held-out merits-case invalidation plausibility only; they do not validate emergency-order behavior or lower-court review.
- Rulemaking rows support held-out final-to-effective-delay plausibility only; they do not validate comments, enforcement, underfunding, or proposed-rule linkage.
- Law-revision rows support held-out text-flag correction plausibility only; they do not validate full statutory lineage or codified-text diffs.
- Comparative-institution rows support held-out bicameral-context plausibility only; they do not validate cross-national productivity or institutional fit.
