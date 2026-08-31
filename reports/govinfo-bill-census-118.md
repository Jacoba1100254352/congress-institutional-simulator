# GovInfo Bill Lifecycle Census: 118th Congress

This report summarizes the complete, provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 118th Congress. The full census is the temporal test cohort for the frozen 117th-Congress lifecycle calibration.

- Bills: 16213 (10564 H.R.; 5649 S.)
- Parsed direct bill actions: 75239
- Public/private law rows: 269 / 0
- Structurally invalid rows: 0
- Preserved source-date anomaly rows: 20
- Classification version: `govinfo-bill-lifecycle-v2`
- Committed CSV SHA-256: `b5d89515836e7209b6ef0d1d12b86627ebe2b2e6c8914a28a4994ae32278359b`

## Lifecycle Funnel

| Stage | Count | Rate |
| --- | ---: | ---: |
| Referred to committee | 16155 | 0.996423 |
| Committee hearing | 664 | 0.040955 |
| Committee markup | 1683 | 0.103806 |
| Committee ordered reported | 1677 | 0.103436 |
| Committee report | 1426 | 0.087954 |
| Committee discharge | 510 | 0.031456 |
| Committee advanced | 1843 | 0.113674 |
| Substantive floor consideration | 957 | 0.059027 |
| Passed origin chamber | 935 | 0.057670 |
| Completed congressional passage | 270 | 0.016653 |
| Presented to President | 270 | 0.016653 |
| Vetoed | 1 | 0.000062 |
| Enacted | 269 | 0.016592 |

## Bill-Type Strata

| Type | Bills | Committee advanced | Floor considered | Origin passage | Completed passage | Vetoed | Enacted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hr` | 10564 | 0.113783 | 0.063991 | 0.062476 | 0.016850 | 0.000000 | 0.016850 |
| `s` | 5649 | 0.113471 | 0.049743 | 0.048681 | 0.016286 | 0.000177 | 0.016109 |

## Classification And Integrity Audit

- The temporal audit found that GovInfo action code `E30000` is context-dependent: it labels signatures in most records but labels the presidential veto of `118-s-4199`. Classifier v2 therefore requires positive signature/enactment text or an unambiguous law record/code rather than treating `E30000` alone as enactment.
- `118-s-4199` completed passage and was presented, then vetoed; it is the only presented bill in this scope that was not enacted.
- Both chamber-passage flags are present for `118-s-1146`, `118-s-1258`, `118-s-2073`, but the conservative classifier does not mark completed passage because the records do not establish agreement on identical text.
- The 20 preserved source-date anomalies are hearing dates before introduction in official committee-activity metadata: `118-hr-4821`, `118-hr-6185`, `118-hr-6544`, `118-hr-8771`, `118-hr-8772`, `118-hr-9026`, `118-hr-9027`, `118-hr-9686`, `118-hr-9711`, `118-hr-9714`, `118-hr-9716`, `118-hr-9751`, `118-s-2226`, `118-s-2605`, `118-s-4678`, `118-s-4690`, `118-s-4795`, `118-s-4797`, `118-s-4802`, `118-s-4875`.

## Independent Source Cross-Check

The separate bounded 118th-Congress Congress.gov/GovInfo sample contains 180 rows; 180 retain GovInfo identifier matches, 180 align on the earlier coarse action flags, and 180 align on policy area. This bounded sample audits source translation; the full census supplies the temporal flow rates.

## Interpretation Boundary

- No 118th-Congress record participates in threshold selection or refitting.
- The census is complete for H.R. and S. measures, not resolutions or joint resolutions.
- Stage flags are conservative operational classifications of GovInfo records, not official legal-status determinations.
- The temporal comparison tests transport of three aggregate rates. It does not identify why Congresses differ or validate individual mechanisms.

Claim boundary: The census supports descriptive 118th-Congress H.R./S. legislative-flow benchmarks and an aggregate temporal transport check for the frozen 117th-Congress calibration. It does not establish causal mechanism validity, bill quality, public preferences, public benefit, welfare, or institutional rankings.
