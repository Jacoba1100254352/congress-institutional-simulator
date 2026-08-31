# Legislative Executive-Action Diagnostic

Source-aligned diagnostic of presentment, presidential veto, successful override, and enactment in the complete 116th-118th H.R./S. censuses and the frozen selected workflow panel.

## Denominator Alignment

- Empirical executive decisions are measures classified as presented to the President.
- Simulator executive decisions equal enacted bills plus vetoes minus overridden vetoes. This avoids double-counting bills enacted over a veto.
- In every empirical cohort, presentments equal enactments plus vetoes minus overrides, so the two denominators describe the same decision point.
- Veto and override diagnostics do not participate in calendar-threshold selection or alter any frozen tolerance.

## Results

| Source | Cohort | Decisions | Vetoes | Conditional veto rate (95% Wilson interval) | Overrides | Override rate among vetoes (95% Wilson interval) | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| GovInfo census | 116 | 334 | 2 | 0.005988 [0.001644, 0.021567] | 1 | 0.500000 [0.094531, 0.905469] | empirical_reference |
| GovInfo census | 117 | 358 | 0 | 0.000000 [0.000000, 0.010616] | 0 | NA | empirical_reference |
| GovInfo census | 118 | 270 | 1 | 0.003704 [0.000654, 0.020677] | 0 | 0.000000 [0.000000, 0.793451] | empirical_reference |
| GovInfo census | 116-118 pooled | 962 | 3 | 0.003119 [0.001061, 0.009128] | 1 | 0.333333 [0.061492, 0.792340] | empirical_reference_pooled |
| frozen simulator | 117-selected 50-seed panel | 2621 | 647 | 0.246852 [0.230724, 0.263722] | 0 | 0.000000 [0.000000, 0.005902] | large_descriptive_mismatch_no_prespecified_tolerance |

## Finding

The complete empirical cohorts contain 3 vetoes in 962 presentments, a conditional rate of 0.003119. The frozen selected panel produces 647 vetoes in 2621 executive decisions, a rate of 0.246852. The absolute difference is 0.243734, and the simulator rate is 79.157 times the pooled empirical rate.
The difference and ratio are computed from the integer event counts before rates are rounded to six decimals for display.

The Wilson intervals do not overlap. That makes the mechanism discrepancy too large to hide behind the aggregate enactment fit. No veto-specific tolerance was prespecified, so this report preserves the result as a descriptive diagnostic rather than relabeling it as a formal held-out pass or failure.

Only three empirical vetoes are observed, including one successful override. The override estimate is therefore extremely sparse and should not be used for parameter fitting by itself.

## Model Boundary And Next Gate

The current presidential-veto parameterization should be interpreted as an elevated-propensity veto stress mechanism, not as an empirically calibrated representation of U.S. presidential action. Its aggregate enactment proximity can be produced while the internal executive-action pathway is wrong.

A future calibration should use a longer completed-Congress panel spanning multiple administrations, classify regular and pocket vetoes plus both-chamber overrides, condition presidential choice on policy distance, party control, and chamber support, and reserve complete Congresses for temporal testing. The current flow threshold and transport tolerances should remain frozen while that separate mechanism model is designed.

Claim boundary: This is a descriptive mechanism diagnostic using complete H.R./S. presentment, veto, override, and enactment classifications for three Congresses. It is not a causal model, a presidential-choice calibration, or evidence about bill quality, welfare, public preferences, or institutional rankings.
