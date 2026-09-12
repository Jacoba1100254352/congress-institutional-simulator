# House Agenda-Control Calibration and Temporal Test

Primary temporal gate: **FAIL**.

Source-attribution caveat: these are the preserved v1 results. A post-fit audit found one Senate action counted as House suspension evidence (118th-Congress H.R. 4366). [The separate source audit](house-agenda-control-source-audit.md) screens the chamber attribution without refitting; the discrepancy increases and the failure remains. Its history-wide source routes are also not equivalent to the simulator's single-decision score overlap.

## Locked Design

- Development source: all 18,771 H.R. measures in the 116th and 117th Congresses
- Primary test source: all 10,564 H.R. measures in the 118th Congress
- Candidate grid: 1,445 parameter triples
- Development simulation: 20 seeds, 12 runs per seed, 14,400 bills per candidate
- Test simulation: 30 independent seeds, 20 runs per seed, 36,000 bills
- The 118th-Congress route distribution was known before tolerances were locked, so the test is no-refit but not outcome blind

Protocol chronology is unverified: no separate pre-fit commit exists in the available Git history. The original specification records a pre-fit lock, but it was untracked alongside the fitted results at publication audit. See [Provenance and Numerical Amendment 1](../papers/empirical-validation/house-agenda-control-provenance-amendment.md). The fixed protocol and failed comparison are reproducible; their asserted pre-fit timing is not independently established by this artifact.

## Selected Development Candidate

- Minimum calendar priority: 0.680
- Special-rule threshold: 0.475
- Suspension threshold: 0.750
- Standardized squared selection loss: 4.248261
- Maximum absolute standardized fitted error: 1.712057
- Leave-one-seed-out stability: 16 / 20 panels reselected the full-panel triple
- Grid-boundary warning: yes

| Development metric | Source target | Simulator | Error |
| --- | ---: | ---: | ---: |
| Committee advancement | 0.101859 | 0.110556 | +0.008696 |
| Floor consideration | 0.079911 | 0.065278 | -0.014633 |
| Advance-to-floor ratio | 0.615063 | 0.590452 | -0.024611 |
| Special-rule-only route | 0.103333 | 0.081915 | -0.021418 |
| Suspension-only route | 0.832000 | 0.818085 | -0.013915 |
| Mixed route | 0.025333 | 0.059574 | +0.034241 |
| Other route | 0.039333 | 0.040426 | +0.001092 |
| Restrictive special-rule share | 1.000000 | 1.000000 | -0.000000 |
| Route total variation | 0.000000 | 0.035333 | +0.035333 |

Committee advancement and the restrictive share are reported development checks, not fitted terms. The advance-to-floor ratio is descriptive because real floor paths can bypass a recorded committee-advance stage while the simulator route layer follows its committee layer.

## No-Refit 118th-Congress Test

| Gate | Source target | Simulator | Error or distance | Tolerance | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Committee advancement | 0.113783 | 0.107528 | -0.006255 | 0.020 | pass |
| Floor consideration | 0.063991 | 0.062806 | -0.001185 | 0.020 | pass |
| Four-route total variation | 0.000000 | 0.110470 | +0.110470 | 0.100 | fail |
| Restrictive special-rule share | 0.992593 | 1.000000 | +0.007407 | 0.020 | pass |

The route-composition gate fails by 0.010470 total-variation units. The other three frozen conditions pass. This miss is retained; the candidate grid is not expanded and no route threshold is retuned against the 118th Congress.

### Test Route Composition

| Route | 118th source | Simulator | Error |
| --- | ---: | ---: | ---: |
| Special-rule-only route | 0.187870 | 0.077399 | -0.110470 |
| Suspension-only route | 0.804734 | 0.812915 | +0.008181 |
| Mixed route | 0.005917 | 0.057054 | +0.051137 |
| Other route | 0.001479 | 0.052632 | +0.051152 |

## Failure Diagnosis

The selected suspension threshold is the upper boundary of the locked grid, and the development candidate's mixed-route error is 1.712057 standardized tolerance units. In the later cohort, the source special-rule-only share rises to 0.187870, while the unchanged simulator remains at 0.077399 and allocates excess share to mixed and other routes. The current two-score overlap construction therefore does not transport the observed route shift. This is evidence against treating its route mechanism as calibrated Congress behavior.

## Monte Carlo Variation

The seed table retains all 20 selected-candidate development seeds and 30 independent test seeds. The summary reports means, sample standard deviations, standard errors of means, minima, and maxima computed from the serialized seed metrics. These describe simulation variability conditional on the fixed model and selected thresholds. Development variability is conditional on selection using the same seeds; it is not independent validation or an estimate of source-data uncertainty.

The acceptance gate continues to use pooled bill rates and pooled conditional route shares. A mean of per-seed shares or per-seed total-variation distances generally differs from its pooled counterpart and does not replace it. No new acceptance condition is introduced.

| Metric | Development seed SD | Test seed mean | Test seed SD | Test mean SE |
| --- | ---: | ---: | ---: | ---: |
| Committee advancement | 0.012938 | 0.107528 | 0.009193 | 0.001678 |
| Floor consideration | 0.009924 | 0.062806 | 0.006184 | 0.001129 |
| Advance-to-floor ratio | 0.058268 | 0.584556 | 0.037428 | 0.006833 |
| Enactment (descriptive) | 0.007238 | 0.027000 | 0.003430 | 0.000626 |
| Special-rule-only route | 0.032923 | 0.076418 | 0.035436 | 0.006470 |
| Suspension-only route | 0.060050 | 0.813354 | 0.045275 | 0.008266 |
| Mixed route | 0.035695 | 0.057476 | 0.022224 | 0.004058 |
| Other route | 0.025486 | 0.052752 | 0.028424 | 0.005190 |
| Restrictive special-rule share | 0.000000 | 1.000000 | 0.000000 | 0.000000 |
| Restrictive rule pressure | 0.009510 | 0.060861 | 0.007120 | 0.001300 |
| Open rule pressure | 0.009920 | 0.046667 | 0.005057 | 0.000923 |
| Calendar capacity denial | 0.007939 | 0.044722 | 0.005910 | 0.001079 |
| Route total variation | 0.037402 | 0.123601 | 0.027627 | 0.005044 |

## Preserved Lifecycle Baseline

The earlier lifecycle calibration remains unchanged at calendar threshold 0.68, committee advancement 0.106278, floor consideration 0.061097, and enactment 0.027417. The route study is a separately named calibration and does not overwrite that frozen result.

## Noncomparable Evidence

Official calendar-placement coverage, calendar-day stage durations, and amendment action counts are not fitted. The simulator has no official-calendar action record, defensible day scale, or route-specific amendment action log. House passage and enactment are also excluded from this gate because the source panel is H.R.-specific while the simulator continues through a stylized Senate, conference, President, and court.

## Claim Boundary

This study calibrates one aggregate synthetic route assignment against one pooled development cohort and applies an unchanged scenario to one later completed Congress. It does not validate bill-level agenda decisions, causal gatekeeping, leadership motives, amendment opportunities, calendar timing, downstream outcomes, welfare, representation, capture, or institutional rankings.
