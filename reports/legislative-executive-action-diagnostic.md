# Legislative Executive-Action Diagnostic

Source-aligned diagnostic of presentment, presidential veto, successful override, enactment, and observed final chamber support in complete 108th-118th-Congress GovInfo decision panels and the frozen selected workflow panel.

## Denominator Alignment

- The bill panel parses 126,760 H.R./S. source records and retains 4,021 measures presented to the President. A separate panel parses 2,031 H.J.Res./S.J.Res. records and retains 187 presidential decisions.
- Bills and joint resolutions are reported separately before a combined 4,208-measure denominator is shown. Constitutional-amendment joint resolutions that are not presented to the President remain outside the population.
- The bill veto reference contains 21 vetoes and six successful overrides. The joint-resolution reference contains 26 vetoes and no overrides; the S.J.Res. 22 source-date discrepancy is preserved rather than forced into agreement.
- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. Every empirical subset uses the same identity, avoiding double-counting measures enacted over a veto.
- The final-vote panel contains one House and one Senate row for every presented measure. It retains 1,685 official final roll calls and 6,731 nonrecorded final approvals; earlier roll calls are never substituted for a later voice vote or unanimous-consent approval.
- These diagnostics do not participate in calendar-threshold selection or alter any frozen lifecycle tolerance.

## Measure-Class And Simulator Comparison

| Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 108-118 H.R./S. bills | 4021 | 21 | 0.005223 [0.003419, 0.007971] | 6 | 0.285714 [0.138139, 0.499564] |
| 108-118 joint resolutions | 187 | 26 | 0.139037 [0.096681, 0.195925] | 0 | 0.000000 [0.000000, 0.128729] |
| 108-118 all presented measures | 4208 | 47 | 0.011169 [0.008410, 0.014820] | 6 | 0.127660 [0.059846, 0.251739] |
| 117-selected 50-seed panel | 2621 | 647 | 0.246852 [0.230724, 0.263722] | 0 | 0.000000 [0.000000, 0.005902] |

## H.R./S. Congress Results

| Congress | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 108 | 476 | 0 | 0.000000 [0.000000, 0.008006] | 0 | NA |
| 109 | 466 | 1 | 0.002146 [0.000379, 0.012054] | 0 | 0.000000 [0.000000, 0.793451] |
| 110 | 449 | 11 | 0.024499 [0.013734, 0.043331] | 4 | 0.363636 [0.151665, 0.646199] |
| 111 | 367 | 1 | 0.002725 [0.000481, 0.015271] | 0 | 0.000000 [0.000000, 0.793451] |
| 112 | 272 | 0 | 0.000000 [0.000000, 0.013926] | 0 | NA |
| 113 | 282 | 0 | 0.000000 [0.000000, 0.013439] | 0 | NA |
| 114 | 330 | 5 | 0.015152 [0.006489, 0.034972] | 1 | 0.200000 [0.036224, 0.624465] |
| 115 | 417 | 0 | 0.000000 [0.000000, 0.009128] | 0 | NA |
| 116 | 334 | 2 | 0.005988 [0.001644, 0.021567] | 1 | 0.500000 [0.094531, 0.905469] |
| 117 | 358 | 0 | 0.000000 [0.000000, 0.010616] | 0 | NA |
| 118 | 270 | 1 | 0.003704 [0.000654, 0.020677] | 0 | 0.000000 [0.000000, 0.793451] |

## H.R./S. Descriptive Strata

| Stratum | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| George W. Bush | 1391 | 12 | 0.008627 [0.004942, 0.015019] | 4 | 0.333333 [0.138120, 0.609378] |
| Barack Obama | 1251 | 6 | 0.004796 [0.002200, 0.010424] | 1 | 0.166667 [0.030053, 0.563503] |
| Donald J. Trump | 751 | 2 | 0.002663 [0.000731, 0.009658] | 1 | 0.500000 [0.094531, 0.905469] |
| Joseph R. Biden Jr. | 628 | 1 | 0.001592 [0.000281, 0.008964] | 0 | 0.000000 [0.000000, 0.793451] |
| unified | 2084 | 2 | 0.000960 [0.000263, 0.003493] | 0 | 0.000000 [0.000000, 0.657620] |
| divided | 1937 | 19 | 0.009809 [0.006289, 0.015270] | 6 | 0.315789 [0.153644, 0.539896] |
| same-party sponsor | 2217 | 1 | 0.000451 [0.000080, 0.002551] | 0 | 0.000000 [0.000000, 0.793451] |
| opposition-party sponsor | 1790 | 20 | 0.011173 [0.007245, 0.017195] | 6 | 0.300000 [0.145477, 0.518973] |
| other/unknown sponsor | 14 | 0 | 0.000000 [0.000000, 0.215311] | 0 | NA |

## Final-Vote Coverage

These four rows partition all 4,208 measures. A nonrecorded final approval is an observed legislative pathway, not missing data to be silently imputed.

| Coverage | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| both final roll calls | 310 | 40 | 0.129032 [0.096207, 0.170939] | 4 | 0.100000 [0.039580, 0.230518] |
| House final roll only | 1023 | 3 | 0.002933 [0.000998, 0.008586] | 1 | 0.333333 [0.061492, 0.792340] |
| Senate final roll only | 42 | 0 | 0.000000 [0.000000, 0.083799] | 0 | NA |
| no final roll calls | 2833 | 4 | 0.001412 [0.000549, 0.003625] | 1 | 0.250000 [0.045587, 0.699358] |

## Both-Recorded Support Strata

The next rows are restricted to the 310 measures with recorded final votes in both chambers. The two-thirds split uses yea divided by yea plus nay, matching the constitutional override benchmark. The opposition-party split uses the major party opposite the President. Neither split was used for model fitting or causal estimation.

| Minimum chamber support | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| both chambers at least two-thirds | 165 | 5 | 0.030303 [0.013012, 0.068967] | 4 | 0.800000 [0.375535, 0.963776] |
| one or both chambers below two-thirds | 145 | 35 | 0.241379 [0.178985, 0.317124] | 0 | 0.000000 [0.000000, 0.098901] |

| Opposition-party support | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| opposition majority in both chambers | 199 | 40 | 0.201005 [0.151228, 0.262107] | 4 | 0.100000 [0.039580, 0.230518] |
| opposition below majority in one or both chambers | 111 | 0 | 0.000000 [0.000000, 0.033450] | 0 | NA |

## Findings

The bill class contains 21 vetoes in 4021 decisions, a rate of 0.005223. Joint resolutions contain 26 vetoes in 187 decisions, a rate of 0.139037, or 26.620 times the bill-class rate. Pooling without a measure-class label would therefore conceal a large composition difference.

The combined empirical population contains 47 vetoes in 4208 presented measures, a rate of 0.011169. The frozen selected simulator panel produces 647 vetoes in 2621 executive decisions, a rate of 0.246852. The exact-count difference is 0.235683, and the simulator rate is 22.101 times the combined empirical rate.
The difference and ratio are computed from integer event counts before display rates are rounded.

The combined empirical and simulator Wilson intervals do not overlap. No veto-specific tolerance was prespecified, so this remains a descriptive mechanism discrepancy rather than a retroactive formal pass or failure.

Within the bill class, divided-government Congresses contain 19 vetoes in 1937 decisions versus 2 in 2084 under unified government, an unadjusted rate ratio of 10.221. Opposite-party sponsors account for 20 vetoes in 1790 decisions versus 1 in 2217 for same-party sponsors, an unadjusted rate ratio of 24.771.
These strata overlap with administration and issue mix and do not estimate causal party-control or sponsor-party effects.

Final-roll coverage is strongly selected: 40 of 47 vetoes occur among the 310 measures with recorded final votes in both chambers, while 4 occur among 2833 measures with neither final roll call. This pattern makes complete-case support analysis nonrepresentative of the full presentment population.

Within the both-recorded subset, 35 of 145 measures with one or both chambers below two-thirds were vetoed, compared with 5 of 165 measures at or above two-thirds in both chambers. All 40 both-recorded vetoes occur among the 199 measures with opposition-party majority support in both chambers; the other 111 measures contain 0 vetoes. These are descriptive associations conditioned on an informative recording process, measure class, and completed passage.

## Model Boundary And Next Gate

The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can coexist with a badly mis-scaled executive-action pathway.

The next gate is a separately frozen presidential-choice study using the now-committed measure-class and final-vote fields. It must specify the low-event estimator, predictor availability rules, treatment of nonrecorded approvals, calibration loss, and whole-Congress holdout before fitting. The current flow threshold and transport tolerances remain frozen.

Claim boundary: This is a descriptive mechanism diagnostic using complete H.R./S. and separately labeled H.J.Res./S.J.Res. presidential decisions for the 108th-118th Congresses. Final-vote support and party strata are observed after congressional passage, and missing roll calls are retained process outcomes rather than imputed support. This is not a causal model, a presidential-choice calibration, or evidence about bill quality, welfare, public preferences, or institutional rankings.
