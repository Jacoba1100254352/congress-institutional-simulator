# Legislative Lifecycle Calibration

Deterministic calibration-only parameter sweep for the stylized current-Congress workflow.

## Selection Protocol

- Candidate calendar-priority thresholds: 0.60 through 0.74 in 0.01 steps
- Fixed simulator seed panel: 50 seeds defined by `117000001 + (104729 * index)` for indices 0 through 49
- Runs per seed: 24
- Simulated bills per candidate: 72000
- Selection data: calibration half of the 117th-Congress H.R./S. census only
- Selection criterion: sum of squared errors standardized by tolerances of 0.015 for floor consideration and 0.010 for enactment
- Committee advancement is reported as an upstream workflow check and does not enter calendar-threshold selection
- Held-out use: reported only after threshold selection; it does not participate in the fit criterion
- Leave-one-seed-out stability: 50 / 50 panels reselected 0.68

Selected and model-default threshold: **0.68**.

## Selected Fit

| Metric | Calibration target | Simulator mean | Calibration error | Held-out target | Held-out error |
| --- | ---: | ---: | ---: | ---: | ---: |
| committeeAdvanceRate | 0.099154 | 0.106278 | +0.007124 | 0.101440 | +0.004838 |
| floorConsiderationRate | 0.065442 | 0.061097 | -0.004345 | 0.067715 | -0.006618 |
| enactmentRate | 0.022607 | 0.027417 | +0.004810 | 0.024927 | +0.002490 |

## Executive-Action Diagnostic

- Enacted bills: 1974
- Veto events: 647
- Successful overrides: 0
- Executive decisions: 2621 (enactments plus vetoes minus overridden vetoes)
- Conditional veto rate: 0.246852
- Override rate among vetoes: 0.000000

These quantities are diagnostics only. They do not enter threshold selection, which remains frozen to floor consideration and enactment on the 117th calibration split.

## Candidate Grid

| Threshold | Committee advance | Floor | Enactment | Calendar denial | Standardized squared error | Selected |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0.60 | 0.104097 | 0.091986 | 0.035819 | 0.012111 | 4.877193 | no |
| 0.61 | 0.104125 | 0.089167 | 0.035222 | 0.014958 | 4.093041 | no |
| 0.62 | 0.104347 | 0.085931 | 0.034722 | 0.018417 | 3.333471 | no |
| 0.63 | 0.104722 | 0.082153 | 0.033583 | 0.022569 | 2.445899 | no |
| 0.64 | 0.105042 | 0.078083 | 0.032472 | 0.026958 | 1.683472 | no |
| 0.65 | 0.105472 | 0.073528 | 0.031083 | 0.031944 | 1.009066 | no |
| 0.66 | 0.105458 | 0.068944 | 0.029722 | 0.036514 | 0.560791 | no |
| 0.67 | 0.106236 | 0.065236 | 0.028667 | 0.041000 | 0.367383 | no |
| 0.68 | 0.106278 | 0.061097 | 0.027417 | 0.045181 | 0.315223 | yes |
| 0.69 | 0.106583 | 0.057292 | 0.026305 | 0.049292 | 0.432022 | no |
| 0.70 | 0.106694 | 0.053931 | 0.025222 | 0.052764 | 0.657339 | no |
| 0.71 | 0.106736 | 0.050833 | 0.023972 | 0.055903 | 0.967147 | no |
| 0.72 | 0.106819 | 0.048708 | 0.023056 | 0.058111 | 1.246534 | no |
| 0.73 | 0.106569 | 0.047208 | 0.022458 | 0.059361 | 1.477859 | no |
| 0.74 | 0.106597 | 0.046722 | 0.022319 | 0.059875 | 1.558304 | no |

## Claim Boundary

This procedure reports three aggregate flow rates for one stylized workflow and selects one downstream calendar threshold against two of them using a deterministic split of one Congress. It does not validate causal mechanisms, bill quality, public preferences, welfare, or institutional rankings, and the within-Congress held-out split is not temporal validation.
