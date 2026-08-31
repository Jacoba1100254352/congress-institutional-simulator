# GovInfo Bill Lifecycle Census: 116th Congress

This report summarizes the complete, provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 116th Congress. It is the pre-calibration backcast cohort for the frozen 117th-Congress lifecycle design.

- Bills: 14148 (9062 H.R.; 5086 S.)
- Parsed direct bill actions: 68345
- Public/private law rows: 333 / 0
- Structurally invalid rows: 0
- Preserved source-date anomaly rows: 24
- Classification version: `govinfo-bill-lifecycle-v3`
- Committed CSV SHA-256: `422265c48bd344ebd132815f7d711bda9b76ffda7b2d2182d8682ef7fa05e374`

## Lifecycle Funnel

| Stage | Count | Rate |
| --- | ---: | ---: |
| Referred to committee | 14086 | 0.995618 |
| Committee hearing | 676 | 0.047781 |
| Committee markup | 1297 | 0.091674 |
| Committee ordered reported | 1264 | 0.089341 |
| Committee report | 1035 | 0.073155 |
| Committee discharge | 540 | 0.038168 |
| Committee advanced | 1488 | 0.105174 |
| Substantive floor consideration | 1048 | 0.074074 |
| Passed origin chamber | 1039 | 0.073438 |
| Completed congressional passage | 334 | 0.023608 |
| Presented to President | 334 | 0.023608 |
| Vetoed | 2 | 0.000141 |
| Veto overridden | 1 | 0.000071 |
| Enacted | 333 | 0.023537 |

## Bill-Type Strata

| Type | Bills | Committee advanced | Floor considered | Origin passage | Completed passage | Vetoed | Overridden | Enacted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hr` | 9062 | 0.105495 | 0.085853 | 0.085743 | 0.023615 | 0.000110 | 0.000110 | 0.023615 |
| `s` | 5086 | 0.104601 | 0.053087 | 0.051514 | 0.023594 | 0.000197 | 0.000000 | 0.023398 |

## Executive-Action Audit

- `116-hr-6395` was vetoed, overridden by both chambers, and enacted as Public Law 116-283. The successful-override date is the final Senate override action on 2021-01-01.
- `116-s-906` was vetoed without a successful override and is the only presented measure in scope that was not enacted.
- These two records make veto and override rates directly observable, but the event count is too small for a stable mechanism calibration by itself.

## Classification And Integrity Audit

- Classifier v3 requires affirmative House and Senate override evidence before labeling a veto successfully overridden. One chamber alone is insufficient.
- Both chamber-passage flags are present for `116-hr-1044`, `116-hr-2486`, `116-hr-2610`, `116-hr-4764`, `116-hr-550`, `116-hr-6172`, `116-hr-925`, `116-s-178`, `116-s-1811`, but the conservative classifier does not mark completed passage because the records do not establish agreement on identical text.
- The 24 preserved source-date anomalies are hearing dates before introduction in official committee-activity metadata: `116-hr-2665`, `116-hr-2779`, `116-hr-3432`, `116-hr-3630`, `116-hr-3631`, `116-hr-4618`, `116-hr-4650`, `116-hr-4665`, `116-hr-4671`, `116-hr-4995`, `116-hr-4996`, `116-hr-4997`, `116-hr-5000`, `116-hr-5035`, `116-hr-5552`, `116-s-1790`, `116-s-2470`, `116-s-2520`, `116-s-2524`, `116-s-2581`, `116-s-2582`, `116-s-2583`, `116-s-2584`, `116-s-4897`.

## Interpretation Boundary

- No 116th-Congress record participates in threshold selection, tolerance selection, or refitting.
- The census is complete for H.R. and S. measures, not resolutions or joint resolutions.
- Stage flags are conservative operational classifications of GovInfo records, not official legal-status determinations.
- The temporal comparison tests transport of aggregate rates and exposes an executive-action mechanism discrepancy. It does not identify why Congresses differ or validate individual causal mechanisms.

Claim boundary: The census supports descriptive 116th-Congress H.R./S. legislative-flow benchmarks and an aggregate backcast for the frozen 117th-Congress calibration. It does not establish causal mechanism validity, bill quality, public preferences, public benefit, welfare, or institutional rankings.
