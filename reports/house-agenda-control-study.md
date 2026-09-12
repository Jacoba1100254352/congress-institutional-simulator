# House Agenda-Control Source and Temporal Comparison

Frozen-artifact integrity status: **PASS**. Source attribution status: **CAVEAT**. Simulator fitting is reported separately.

Post-fit chamber review identifies one Senate action used as House suspension evidence in the frozen v1 panel (H.R. 4366, 118th Congress). The preserved counts below are not corrected census estimates. See [House procedure source audit](house-agenda-control-source-audit.md) for the full-archive review and the fixed-model sensitivity, which retains failure. The source mixed-route category spans a bill's history, not one scheduling decision.

This report implements the locked source specification in `papers/empirical-validation/house-agenda-control-panel-specification.md`. Specification SHA-256: `28c1b3874fb99a1987f1f8b146517dd4f2be14f74ea93b36bfadbb48591200ec`.

## Descriptive Result

The pooled 116th-117th development cohort has 1500 floor-considered H.R. measures among 18771 introduced measures (7.991%), compared with 676 of 10564 (6.399%) in the 118th-Congress test cohort. Among committee-advanced H.R. measures, the observed floor-consideration transition is 61.506% in development and 49.917% in the test cohort.

Adopted Table 1a special rules account for 10.333% of floor-considered measures in development and 18.787% in the test cohort. Suspension remains the largest observed route in every Congress, while mixed and other direct paths remain separately identified.

Among adopted Table 1a grant rows, the structured-or-closed share is 255/255 (100.000%) in development and 178/179 (99.441%) in the test cohort. This is a description of officially classified rules, not a causal estimate of agenda power.

## Lifecycle and Transitions

Rates in stage cells use all complete H.R. rows as the denominator. Transition rates use the preceding observed stage as the denominator.

| Cohort | H.R. rows | Referred | Committee advanced | Calendar placed | Floor considered | Passed House | Enacted | Referred to advanced | Advanced to floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 116th | 9062 | 9062 (100.000%) | 956 (10.550%) | 570 (6.290%) | 778 (8.585%) | 777 (8.574%) | 214 (2.362%) | 956/9062 (10.550%) | 614/956 (64.226%) |
| 117th | 9709 | 9698 (99.887%) | 956 (9.847%) | 497 (5.119%) | 722 (7.436%) | 719 (7.406%) | 198 (2.039%) | 956/9698 (9.858%) | 562/956 (58.787%) |
| 116th-117th development | 18771 | 18760 (99.941%) | 1912 (10.186%) | 1067 (5.684%) | 1500 (7.991%) | 1496 (7.970%) | 412 (2.195%) | 1912/18760 (10.192%) | 1176/1912 (61.506%) |
| 118th test | 10564 | 10555 (99.915%) | 1202 (11.378%) | 781 (7.393%) | 676 (6.399%) | 660 (6.248%) | 178 (1.685%) | 1202/10555 (11.388%) | 600/1202 (49.917%) |

## Floor Routes

Shares condition on substantive House floor consideration. The categories are mutually exclusive; an adopted Table 1a rule takes precedence, with concurrent suspension evidence retained as mixed.

| Cohort | Route | Count | Share of floor-considered |
| --- | --- | ---: | ---: |
| 116th | Adopted Table 1a special rule only | 69 | 8.869% |
| 116th | Suspension only | 644 | 82.776% |
| 116th | Mixed special rule and suspension | 17 | 2.185% |
| 116th | Other direct path | 48 | 6.170% |
| 117th | Adopted Table 1a special rule only | 86 | 11.911% |
| 117th | Suspension only | 604 | 83.657% |
| 117th | Mixed special rule and suspension | 21 | 2.909% |
| 117th | Other direct path | 11 | 1.524% |
| 116th-117th development | Adopted Table 1a special rule only | 155 | 10.333% |
| 116th-117th development | Suspension only | 1248 | 83.200% |
| 116th-117th development | Mixed special rule and suspension | 38 | 2.533% |
| 116th-117th development | Other direct path | 59 | 3.933% |
| 118th test | Adopted Table 1a special rule only | 127 | 18.787% |
| 118th test | Suspension only | 544 | 80.473% |
| 118th test | Mixed special rule and suspension | 4 | 0.592% |
| 118th test | Other direct path | 1 | 0.148% |

## Special-Rule Structure

The first table reconciles the official narrative counts with identifiable literal Table 1a rows. The 117th-Congress table is short by two structured and two closed rule-to-measure rows. No identities or categories are imputed for those four rows.

| Congress | Category | Narrative | Literal Table 1a | Literal minus narrative |
| ---: | --- | ---: | ---: | ---: |
| 116 | open | 0 | 0 | 0 |
| 116 | modified open | 0 | 0 | 0 |
| 116 | structured | 55 | 55 | 0 |
| 116 | closed | 60 | 60 | 0 |
| 117 | open | 0 | 0 | 0 |
| 117 | modified open | 0 | 0 | 0 |
| 117 | structured | 59 | 57 | -2 |
| 117 | closed | 89 | 87 | -2 |
| 118 | open | 0 | 0 | 0 |
| 118 | modified open | 1 | 1 | 0 |
| 118 | structured | 83 | 83 | 0 |
| 118 | closed | 115 | 115 | 0 |

Category-presence counts at the resolution level can exceed the number of unique resolutions because a single rule may cover measures assigned to different categories. H.R.-measure counts preserve the category attached to each literal grant row.

| Cohort | Category | Adopted grant rows | Adopted resolution presence | Adopted H.R. measure presence |
| --- | --- | ---: | ---: | ---: |
| 116th | open | 0 | 0 | 0 |
| 116th | modified open | 0 | 0 | 0 |
| 116th | structured | 55 | 45 | 53 |
| 116th | closed | 60 | 37 | 35 |
| 117th | open | 0 | 0 | 0 |
| 117th | modified open | 0 | 0 | 0 |
| 117th | structured | 57 | 35 | 57 |
| 117th | closed | 83 | 51 | 53 |
| 116th-117th development | open | 0 | 0 | 0 |
| 116th-117th development | modified open | 0 | 0 | 0 |
| 116th-117th development | structured | 112 | 80 | 110 |
| 116th-117th development | closed | 143 | 88 | 88 |
| 118th test | open | 0 | 0 | 0 |
| 118th test | modified open | 1 | 1 | 1 |
| 118th test | structured | 73 | 45 | 71 |
| 118th test | closed | 105 | 47 | 63 |

## Stage Timing

Both summaries use the nearest-rank rule. Missing intervals are not imputed. Non-linear source stage sequences are excluded from the affected interval and reported below.

| Cohort | Interval | Observed n | P50 days | P90 days |
| --- | --- | ---: | ---: | ---: |
| 116th | Introduction to referral | 9041 | 0 | 0 |
| 116th | Referral to committee advance | 932 | 78 | 371 |
| 116th | Committee advance to floor | 547 | 60 | 208 |
| 116th | Introduction to floor | 778 | 126 | 419 |
| 117th | Introduction to referral | 9674 | 0 | 0 |
| 117th | Referral to committee advance | 929 | 70 | 337 |
| 117th | Committee advance to floor | 532 | 69 | 231 |
| 117th | Introduction to floor | 722 | 128 | 427 |
| 116th-117th development | Introduction to referral | 18715 | 0 | 0 |
| 116th-117th development | Referral to committee advance | 1861 | 75 | 355 |
| 116th-117th development | Committee advance to floor | 1079 | 63 | 218 |
| 116th-117th development | Introduction to floor | 1500 | 127 | 424 |
| 118th test | Introduction to referral | 10533 | 0 | 0 |
| 118th test | Referral to committee advance | 1180 | 49 | 309 |
| 118th test | Committee advance to floor | 585 | 105 | 292 |
| 118th test | Introduction to floor | 676 | 178 | 440 |

## Amendment-Action Coverage

These are matched GovInfo direct-action records, not counts of amendments permitted by a rule. Offer-action recording is sparse, so the disposition evidence is reported separately and neither field is treated as complete amendment opportunity data.

| Cohort | Route | Bills | Bills with offer action | Bills with disposition action | Offer actions | Disposition actions |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 116th | Adopted Table 1a special rule only | 69 | 0 | 33 | 0 | 187 |
| 116th | Suspension only | 644 | 1 | 2 | 1 | 2 |
| 116th | Mixed special rule and suspension | 17 | 1 | 9 | 1 | 66 |
| 116th | Other direct path | 48 | 0 | 1 | 0 | 1 |
| 117th | Adopted Table 1a special rule only | 86 | 0 | 13 | 0 | 57 |
| 117th | Suspension only | 604 | 0 | 14 | 0 | 15 |
| 117th | Mixed special rule and suspension | 21 | 1 | 2 | 1 | 13 |
| 117th | Other direct path | 11 | 0 | 2 | 0 | 2 |
| 116th-117th development | Adopted Table 1a special rule only | 155 | 0 | 46 | 0 | 244 |
| 116th-117th development | Suspension only | 1248 | 1 | 16 | 1 | 17 |
| 116th-117th development | Mixed special rule and suspension | 38 | 2 | 11 | 2 | 79 |
| 116th-117th development | Other direct path | 59 | 0 | 3 | 0 | 3 |
| 118th test | Adopted Table 1a special rule only | 127 | 0 | 60 | 0 | 452 |
| 118th test | Suspension only | 544 | 0 | 3 | 0 | 3 |
| 118th test | Mixed special rule and suspension | 4 | 0 | 3 | 0 | 68 |
| 118th test | Other direct path | 1 | 0 | 0 | 0 | 0 |

## Integrity and Source Limits

| Cohort | Non-linear stage rows | Lifecycle source-date anomalies | Unidentified floor paths | Mixed paths | Direct rule use without adopted Table 1a link | Adopted Table 1a link without direct rule-use ID |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 116th | 70 | 15 | 0 | 17 | 8 | 2 |
| 117th | 32 | 2 | 0 | 21 | 182 | 3 |
| 116th-117th development | 102 | 17 | 0 | 38 | 190 | 5 |
| 118th test | 15 | 12 | 0 | 4 | 3 | 4 |

Direct rule-use differences are not automatically errors. Some H. Res. actions govern suspension batches, resolving-differences proceedings, or other House orders outside literal Table 1a. Conversely, a granted rule can cover a measure that is not ultimately floor-considered. In the 117th Congress, direct action records show H. Res. 1119 used for H.R. 6531 and H.R. 7309 even though literal Table 1a omits those measure rows; their amendment structures remain unassigned in this panel.

The 117 total preserved non-linear stage rows across the three Congresses arise when a later committee-stage date follows an earlier floor event or, less often, when the first extracted referral follows the first extracted advance event. Their affected elapsed intervals are blank rather than negative.

## Simulator Implication and Boundary

The source evidence supports representing suspension, adopted special-rule, mixed, and other detected floor paths separately. It also shows that the official special-rule categories in these completed Congresses are overwhelmingly structured or closed. Those observations identify a structural comparison target, but they do not authorize parameter fitting by themselves.

Official-source descriptive House procedure and timing evidence only; not causal agenda-control, unobserved floor-demand, public-benefit, welfare, capture, or simulator-validation evidence.

A separate pre-fit specification must freeze comparable simulator metrics, development-only fitting, seeds, candidate grid, loss, tie-breaking, and 118th-Congress no-refit tolerances before simulator behavior changes.

## Reproduction

Run `make house-agenda-control-study`. The study uses the committed source panels and Python's standard library. Source, specification, implementation, and output hashes are recorded in `reports/house-agenda-control-study-metadata.json`.
