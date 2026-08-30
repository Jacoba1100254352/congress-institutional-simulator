# GovInfo Bill Lifecycle Census

This report summarizes the provenance-pinned GovInfo BILLSTATUS census for H.R. and S. measures in the completed 117th Congress. It is a descriptive legislative-flow benchmark, not a simulator-validation claim.

- Bills: 15066 (9709 H.R.; 5357 S.)
- Parsed direct bill actions: 72047
- Public/private law rows: 355 / 3
- Structurally invalid rows: 0
- Preserved source-date anomaly rows: 5
- Classification version: `govinfo-bill-lifecycle-v1`
- Committed CSV SHA-256: `8e43e521148f113e95a2040ec592d7c5470c6303676a534f3d272497cc7bea36`

## Lifecycle Funnel

The split is deterministic: `sha256(bill_id)` first 32 bits modulo 2 equals zero is held out. It is a within-Congress stability check, not a temporal or cross-Congress validation design.

| Stage | All count | All rate | Calibration rate | Held-out rate | Absolute split delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Referred to committee | 14959 | 0.992898 | 0.992861 | 0.992935 | 0.000074 |
| Committee hearing | 790 | 0.052436 | 0.053543 | 0.051320 | 0.002223 |
| Committee markup | 1347 | 0.089407 | 0.089238 | 0.089576 | 0.000338 |
| Committee ordered reported | 1347 | 0.089407 | 0.089238 | 0.089576 | 0.000338 |
| Committee report | 967 | 0.064184 | 0.063194 | 0.065183 | 0.001989 |
| Committee discharge | 573 | 0.038033 | 0.036885 | 0.039190 | 0.002305 |
| Committee advanced | 1511 | 0.100292 | 0.099154 | 0.101440 | 0.002286 |
| Substantive floor consideration | 1003 | 0.066574 | 0.065442 | 0.067715 | 0.002273 |
| Passed origin chamber | 991 | 0.065777 | 0.064384 | 0.067182 | 0.002798 |
| Completed congressional passage | 358 | 0.023762 | 0.022607 | 0.024927 | 0.002320 |
| Presented to President | 358 | 0.023762 | 0.022607 | 0.024927 | 0.002320 |
| Vetoed | 0 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| Enacted | 358 | 0.023762 | 0.022607 | 0.024927 | 0.002320 |

## Bill-Type Strata

| Type | Bills | Committee ordered reported | Committee report | Floor considered | Origin passage | Completed passage | Enacted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hr` | 9709 | 0.092697 | 0.057575 | 0.074364 | 0.074055 | 0.020393 | 0.020393 |
| `s` | 5357 | 0.083442 | 0.076162 | 0.052455 | 0.050775 | 0.029867 | 0.029867 |

## Independent Cross-Checks

- The existing 117th-Congress Congress.gov public-law linkage contributes 40 rows; 40 overlap the census by bill ID, with 40 enacted flags, 40 introduction dates, and 40 policy areas aligned.
- The separate bounded 118th-Congress Congress.gov/GovInfo sample contains 180 rows; 180 retain GovInfo identifier matches, 180 align on the earlier coarse action flags, and 180 align on policy area. It is a different-Congress source cross-check, not a validation sample for the 117th census.

## Interpretation Boundary

- The source archives contain both legacy v1 and current v3 XML records; both schemas are parsed, and no record is dropped for schema generation.
- Action codes are used only where their observed meaning is stable in this corpus. Special-rule actions, failed discharge requests, administrative messages, and sponsorship substitutions do not advance the bill lifecycle.
- Committee ordered-reported actions are separate from filed committee reports. Committee advancement is the union of ordered reported, reported, and discharged.
- Completed congressional passage requires presentment, enactment, or second-chamber passage without amendment. Passing nonidentical versions in each chamber is not enough.
- Five official committee-activity dates precede bill introduction. The source dates are retained and labeled rather than corrected locally.
- The calibration/held-out split is suitable for stability and tolerance checks only. A later Congress is still required for temporal replication.

Claim boundary: The census supports descriptive 117th-Congress H.R./S. legislative-flow benchmarks and deterministic within-Congress held-out checks. It does not establish causal mechanism validity, public support, public benefit, welfare, or institutional rankings.
