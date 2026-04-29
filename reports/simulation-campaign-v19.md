# Simulation Campaign v19 Timeline

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 14
- experiment cases: 6

## Headline Findings

- Open default-pass averaged 0.837 productivity, versus 0.287 for simple majority.
- Open default-pass also averaged 0.431 low-support passage and 0.640 policy shift.
- Challenge vouchers averaged 0.494 challenge use, changed productivity by -0.218, and changed low-support passage by -0.129 relative to open default-pass.
- Public objection windows triggered on 0.631 of potential bills and changed low-support passage by -0.167 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.635, and status-quo wins averaged 0.446 relative to open default-pass.
- Best average welfare in this campaign came from Default pass + affected-group sponsor gate at 0.715.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.199 | 13.318 | 77.500 | 0.655 | 0.000 | 0.083 | 0.588 | 0.063 | 0.227 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.456 | 0.000 | 1.000 |
| Current U.S.-style system | 0.089 | 5.728 | 77.500 | 0.697 | 0.000 | 0.064 | 0.654 | 0.021 | 0.157 | 0.289 | 0.000 | 0.000 | 0.000 | 0.000 | 0.219 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.837 | 64.840 | 77.500 | 0.502 | 0.431 | 0.165 | 0.399 | 0.640 | 0.635 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.000 | 1.000 |
| Default pass + adaptive tracks strict | 0.304 | 21.487 | 53.724 | 0.649 | 0.093 | 0.082 | 0.569 | 0.116 | 0.295 | 0.215 | 0.000 | 0.000 | 0.000 | 0.000 | 0.698 | 0.000 | 0.712 |
| Default pass + affected-group sponsor gate | 0.240 | 15.819 | 15.862 | 0.715 | 0.205 | 0.033 | 0.666 | 0.089 | 0.242 | 0.142 | 0.000 | 0.000 | 0.000 | 0.000 | 0.679 | 0.000 | 0.241 |
| Default pass + pairwise policy tournament | 0.554 | 42.157 | 42.175 | 0.647 | 0.076 | 0.045 | 0.646 | 0.004 | 0.004 | 0.205 | 0.000 | 0.000 | 0.554 | 0.000 | 0.940 | 0.000 | 0.554 |
| Default pass + challenge vouchers | 0.620 | 51.410 | 77.500 | 0.538 | 0.302 | 0.145 | 0.438 | 0.397 | 0.483 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.869 | 0.494 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.425 | 31.703 | 77.500 | 0.627 | 0.244 | 0.105 | 0.517 | 0.214 | 0.421 | 0.214 | 0.000 | 0.000 | 0.000 | 0.000 | 0.959 | 0.000 | 1.000 |
| Default pass + law registry | 0.865 | 67.017 | 77.500 | 0.497 | 0.384 | 0.168 | 0.398 | 0.804 | 0.579 | 0.272 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.785 | 62.294 | 77.500 | 0.469 | 0.272 | 0.110 | 0.448 | 0.293 | 0.331 | 0.281 | 0.000 | 0.000 | 0.701 | 0.237 | 0.859 | 0.441 | 1.000 |
| Default pass + public objection window | 0.462 | 34.042 | 77.500 | 0.595 | 0.264 | 0.103 | 0.507 | 0.213 | 0.367 | 0.220 | 0.000 | 0.000 | 0.000 | 0.000 | 0.890 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.134 | 8.867 | 77.500 | 0.677 | 0.000 | 0.073 | 0.614 | 0.038 | 0.204 | 0.263 | 0.000 | 0.000 | 0.000 | 0.000 | 0.329 | 0.000 | 1.000 |
| Unicameral simple majority | 0.287 | 19.885 | 77.500 | 0.633 | 0.000 | 0.093 | 0.552 | 0.109 | 0.297 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.619 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.117 | 7.518 | 77.500 | 0.693 | 0.000 | 0.065 | 0.646 | 0.029 | 0.154 | 0.296 | 0.000 | 0.000 | 0.000 | 0.000 | 0.298 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`, so it rises when a system blocks more, compromises less, or passes more weak-support bills.

| Era | Scenario | Productivity | Compromise | Gridlock | Low-support | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Era 1 Low Contention | Current U.S.-style system | 0.220 | 0.342 | 0.780 | 0.000 | 0.588 |
| Era 1 Low Contention | Unicameral simple majority | 0.504 | 0.255 | 0.496 | 0.000 | 0.471 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.842 | 0.176 | 0.158 | 0.327 | 0.392 |
| Era 1 Low Contention | Default pass + challenge vouchers | 0.579 | 0.237 | 0.421 | 0.099 | 0.459 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.779 | 0.251 | 0.221 | 0.079 | 0.351 |
| Era 1 Low Contention | Default pass + pairwise policy tournament | 0.616 | 0.639 | 0.384 | 0.000 | 0.300 |
| Era 2 Normal Contention | Current U.S.-style system | 0.147 | 0.360 | 0.853 | 0.000 | 0.618 |
| Era 2 Normal Contention | Unicameral simple majority | 0.402 | 0.251 | 0.598 | 0.000 | 0.524 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.839 | 0.148 | 0.161 | 0.383 | 0.413 |
| Era 2 Normal Contention | Default pass + challenge vouchers | 0.457 | 0.239 | 0.543 | 0.103 | 0.521 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.739 | 0.245 | 0.261 | 0.118 | 0.381 |
| Era 2 Normal Contention | Default pass + pairwise policy tournament | 0.590 | 0.579 | 0.410 | 0.002 | 0.332 |
| Era 3 Polarizing | Current U.S.-style system | 0.084 | 0.361 | 0.916 | 0.000 | 0.650 |
| Era 3 Polarizing | Unicameral simple majority | 0.304 | 0.236 | 0.696 | 0.000 | 0.577 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.842 | 0.119 | 0.158 | 0.437 | 0.431 |
| Era 3 Polarizing | Default pass + challenge vouchers | 0.365 | 0.216 | 0.635 | 0.142 | 0.581 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.665 | 0.238 | 0.335 | 0.161 | 0.428 |
| Era 3 Polarizing | Default pass + pairwise policy tournament | 0.564 | 0.519 | 0.436 | 0.011 | 0.364 |
| Era 4 High Contention | Current U.S.-style system | 0.040 | 0.365 | 0.960 | 0.000 | 0.671 |
| Era 4 High Contention | Unicameral simple majority | 0.218 | 0.238 | 0.782 | 0.000 | 0.619 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.837 | 0.102 | 0.163 | 0.470 | 0.445 |
| Era 4 High Contention | Default pass + challenge vouchers | 0.659 | 0.112 | 0.341 | 0.446 | 0.526 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.767 | 0.209 | 0.233 | 0.344 | 0.423 |
| Era 4 High Contention | Default pass + pairwise policy tournament | 0.540 | 0.463 | 0.460 | 0.046 | 0.400 |
| Era 5 Capture Contention | Current U.S.-style system | 0.025 | 0.362 | 0.975 | 0.000 | 0.679 |
| Era 5 Capture Contention | Unicameral simple majority | 0.167 | 0.225 | 0.833 | 0.000 | 0.649 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.831 | 0.088 | 0.169 | 0.481 | 0.454 |
| Era 5 Capture Contention | Default pass + challenge vouchers | 0.807 | 0.085 | 0.193 | 0.499 | 0.471 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.865 | 0.196 | 0.135 | 0.442 | 0.397 |
| Era 5 Capture Contention | Default pass + pairwise policy tournament | 0.510 | 0.424 | 0.490 | 0.125 | 0.443 |
| Era 6 Crisis | Current U.S.-style system | 0.017 | 0.357 | 0.983 | 0.000 | 0.684 |
| Era 6 Crisis | Unicameral simple majority | 0.128 | 0.225 | 0.872 | 0.000 | 0.669 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.835 | 0.081 | 0.165 | 0.490 | 0.456 |
| Era 6 Crisis | Default pass + challenge vouchers | 0.853 | 0.076 | 0.147 | 0.522 | 0.455 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.895 | 0.189 | 0.105 | 0.488 | 0.393 |
| Era 6 Crisis | Default pass + pairwise policy tournament | 0.502 | 0.389 | 0.498 | 0.268 | 0.486 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Era 1 Low Contention | -15.783 | -0.263 | 0.049 | -0.228 | -0.227 | -0.112 | 0.657 |
| Era 2 Normal Contention | -22.908 | -0.382 | 0.089 | -0.280 | -0.368 | -0.221 | 0.730 |
| Era 3 Polarizing | -28.650 | -0.478 | 0.107 | -0.295 | -0.491 | -0.301 | 0.786 |
| Era 4 High Contention | -13.358 | -0.178 | 0.002 | -0.024 | -0.224 | -0.110 | 0.400 |
| Era 5 Capture Contention | -2.100 | -0.023 | -0.019 | 0.018 | -0.092 | -0.087 | 0.222 |
| Era 6 Crisis | 2.217 | 0.018 | -0.018 | 0.032 | -0.054 | -0.085 | 0.167 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.028 | -0.005 | 0.458 | 5.125 | 0.610 | 0.039 | 0.164 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.284 | 0.145 | -0.356 | -0.635 | -0.631 | 0.001 | 0.002 | 6.000 | 0.446 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Era 1 Low Contention | Current U.S.-style system (0.697) | Default pass + law registry (0.866) | Current U.S.-style system (0.000) |
| Era 2 Normal Contention | Current U.S.-style system (0.715) | Default pass + law registry (0.867) | Current U.S.-style system (0.000) |
| Era 3 Polarizing | Unicameral 60 percent passage (0.719) | Default pass + law registry (0.867) | Current U.S.-style system (0.000) |
| Era 4 High Contention | Current U.S.-style system (0.721) | Default pass + law registry (0.868) | Current U.S.-style system (0.000) |
| Era 5 Capture Contention | Default pass + affected-group sponsor gate (0.781) | Default pass + multi-round mediation + challenge (0.865) | Current U.S.-style system (0.000) |
| Era 6 Crisis | Default pass + affected-group sponsor gate (0.796) | Default pass + multi-round mediation + challenge (0.895) | Current U.S.-style system (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Timeline scenarios are stylized stress paths, not historical calibration. They increase polarization, party loyalty, lobbying pressure, and proposal pressure while reducing compromise culture and constituency responsiveness.
- The timeline comparison should be read as a degradation test: institutions that preserve compromise and productivity under later-era assumptions are more robust than systems that only work in low-contention settings.

## Reproduction

```sh
make campaign
```
