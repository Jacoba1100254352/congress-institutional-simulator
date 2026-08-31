# Legislative Executive-Action Diagnostic

Source-aligned diagnostic of presentment, presidential veto, successful override, and enactment in complete 108th-118th-Congress H.R./S. GovInfo archives and the frozen selected workflow panel.

## Denominator Alignment

- The committed panel parses all 126,760 H.R./S. source records and retains the 4,021 measures classified as presented to the President.
- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. This avoids double-counting bills enacted over a veto.
- In every empirical cohort, presentments equal enactments plus vetoes minus overrides, so the two denominators describe the same decision point.
- The exact 21-bill veto set, veto dates, regular or disputed-return pocket-veto labels, and six successful overrides match an independently compiled official Senate reference.
- Joint resolutions are excluded because the lifecycle calibration is scoped to H.R. and S. measures. Their distinct recent veto incidence must be modeled as a separate measure class before broader presidential-veto claims are made.
- Veto and override diagnostics do not participate in calendar-threshold selection or alter any frozen tolerance.

## Pooled Comparison

| Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 108-118 pooled | 4021 | 21 | 0.005223 [0.003419, 0.007971] | 6 | 0.285714 [0.138139, 0.499564] |
| 117-selected 50-seed panel | 2621 | 647 | 0.246852 [0.230724, 0.263722] | 0 | 0.000000 [0.000000, 0.005902] |

## Congress Results

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

## Descriptive Strata

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

## Findings

The complete empirical panel contains 21 vetoes in 4021 H.R./S. presentments, a conditional rate of 0.005223. The frozen selected panel produces 647 vetoes in 2621 executive decisions, a rate of 0.246852. The absolute difference is 0.241630, and the simulator rate is 47.266 times the pooled empirical rate.
The difference and ratio are computed from the integer event counts before rates are rounded to six decimals for display.

The Wilson intervals do not overlap. That makes the mechanism discrepancy too large to hide behind the aggregate enactment fit. No veto-specific tolerance was prespecified, so this report preserves the result as a descriptive diagnostic rather than relabeling it as a formal held-out pass or failure.

Divided-government Congresses contain 19 vetoes in 1937 decisions versus 2 in 2084 under unified government, an unadjusted rate ratio of 10.221. Opposite-party sponsors account for 20 vetoes in 1790 decisions versus 1 in 2217 for same-party sponsors, an unadjusted rate ratio of 24.771.
These strata are selected after congressional passage, overlap with administration and issue mix, and omit final-vote support. They identify variables a future model must represent; they do not estimate causal party-control or sponsor-party effects.

The panel contains 21 vetoes and 6 successful overrides. That is materially stronger than the earlier three-veto diagnostic but remains sparse for a flexible presidential-choice model or stable override calibration.

## Model Boundary And Next Gate

The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can be produced while the internal executive-action pathway is wrong.

The next gate is a separately frozen presidential-choice study. It should add joint resolutions as a distinct measure class, link final House and Senate vote support, encode administration and party control without treating sponsor party as policy distance, specify a low-event estimator and calibration loss before fitting, and reserve whole Congresses for temporal testing. The current flow threshold and transport tolerances remain frozen.

Claim boundary: This is a descriptive mechanism diagnostic using complete H.R./S. presentment, veto, override, and enactment classifications for the 108th-118th Congresses. Party-control and sponsor-party strata are descriptive, selected post-passage comparisons. This is not a causal model, a presidential-choice calibration, or evidence about bill quality, welfare, public preferences, or institutional rankings.
