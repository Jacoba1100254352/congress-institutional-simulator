# Simulation Campaign v17

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 80
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 35
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.843 productivity, versus 0.268 for simple majority.
- Open default-pass also averaged 0.448 low-support passage and 0.664 policy shift.
- Proposal-cost screening reduced floor load by 50.548 bills/run and enactments by 36.843 bills/run, but raised proposer gain by 0.437.
- Challenge vouchers averaged 0.397 challenge use, changed productivity by -0.172, and changed low-support passage by -0.054 relative to open default-pass.
- Adaptive tracks changed productivity by -0.424, low-support passage by -0.205, and policy shift by -0.463 relative to open default-pass.
- Weighted agenda lotteries changed floor consideration by -0.535, productivity by -0.435, and welfare by 0.052 relative to open default-pass.
- Public objection windows triggered on 0.646 of potential bills and changed low-support passage by -0.183 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.660, and status-quo wins averaged 0.449 relative to open default-pass.
- Best average welfare in this campaign came from Default pass + affected-group sponsor gate at 0.725.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.777 | 103.333 | 0.665 | 0.000 | 0.077 | 0.594 | 0.053 | 0.230 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.453 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.843 | 86.979 | 103.333 | 0.497 | 0.448 | 0.168 | 0.393 | 0.664 | 0.656 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.418 | 42.216 | 92.319 | 0.612 | 0.243 | 0.098 | 0.525 | 0.201 | 0.386 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 | 0.898 | 0.000 | 0.900 |
| Default pass + adaptive tracks + citizen high-risk | 0.418 | 42.164 | 103.333 | 0.612 | 0.241 | 0.098 | 0.525 | 0.200 | 0.386 | 0.202 | 0.000 | 0.000 | 0.000 | 0.000 | 0.897 | 0.000 | 1.000 |
| Default pass + adaptive tracks lenient | 0.557 | 56.527 | 100.729 | 0.574 | 0.338 | 0.117 | 0.481 | 0.315 | 0.461 | 0.213 | 0.000 | 0.000 | 0.000 | 0.000 | 0.971 | 0.000 | 0.977 |
| Default pass + adaptive tracks strict | 0.284 | 28.238 | 72.921 | 0.648 | 0.077 | 0.084 | 0.566 | 0.112 | 0.313 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.717 | 0.000 | 0.714 |
| Default pass + adaptive tracks + supermajority high-risk | 0.418 | 42.172 | 103.333 | 0.612 | 0.241 | 0.098 | 0.525 | 0.200 | 0.384 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 | 0.895 | 0.000 | 1.000 |
| Default pass + affected-group sponsor gate | 0.192 | 18.649 | 18.678 | 0.725 | 0.154 | 0.032 | 0.666 | 0.062 | 0.241 | 0.135 | 0.000 | 0.000 | 0.000 | 0.000 | 0.725 | 0.000 | 0.192 |
| Default pass + pairwise policy tournament | 0.551 | 56.412 | 56.423 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.201 | 0.000 | 0.000 | 0.551 | 0.000 | 0.944 | 0.000 | 0.551 |
| Default pass + strategic policy tournament | 0.551 | 56.416 | 56.423 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.201 | 0.000 | 0.000 | 0.551 | 0.000 | 0.945 | 0.000 | 0.551 |
| Default pass + challenge vouchers | 0.671 | 77.942 | 103.333 | 0.510 | 0.394 | 0.160 | 0.402 | 0.456 | 0.540 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.887 | 0.397 | 1.000 |
| Default pass + challenge to committee review | 0.649 | 76.322 | 79.015 | 0.508 | 0.410 | 0.161 | 0.399 | 0.443 | 0.540 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.849 | 0.397 | 0.685 |
| Default pass + challenge to info + active vote | 0.671 | 77.968 | 103.333 | 0.511 | 0.394 | 0.161 | 0.398 | 0.455 | 0.539 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.892 | 0.398 | 1.000 |
| Default pass + minority-bonus challenge vouchers | 0.634 | 75.042 | 103.333 | 0.520 | 0.372 | 0.155 | 0.412 | 0.420 | 0.524 | 0.252 | 0.000 | 0.000 | 0.000 | 0.000 | 0.881 | 0.442 | 1.000 |
| Default pass + proportional party challenge vouchers | 0.684 | 78.954 | 103.333 | 0.505 | 0.397 | 0.163 | 0.398 | 0.469 | 0.547 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.871 | 0.396 | 1.000 |
| Default pass + challenge to 60 percent vote | 0.618 | 74.042 | 103.333 | 0.504 | 0.434 | 0.164 | 0.393 | 0.427 | 0.541 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.782 | 0.398 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.407 | 41.312 | 103.333 | 0.629 | 0.250 | 0.106 | 0.516 | 0.213 | 0.435 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.964 | 0.000 | 1.000 |
| Default pass + constituent public will | 0.837 | 86.473 | 103.333 | 0.495 | 0.458 | 0.157 | 0.381 | 0.655 | 0.654 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + proposal costs | 0.477 | 50.136 | 52.785 | 0.474 | 0.489 | 0.184 | 0.368 | 0.580 | 1.093 | 0.286 | 0.000 | 0.000 | 0.000 | 0.000 | 0.452 | 0.000 | 0.503 |
| Default pass + lobby-surcharge proposal costs | 0.506 | 51.780 | 55.372 | 0.532 | 0.460 | 0.146 | 0.422 | 0.531 | 0.924 | 0.180 | 0.000 | 0.000 | 0.000 | 0.000 | 0.845 | 0.000 | 0.541 |
| Default pass + proposal costs + public waiver | 0.533 | 55.577 | 58.733 | 0.497 | 0.467 | 0.170 | 0.397 | 0.598 | 0.996 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.651 | 0.000 | 0.565 |
| Default pass + cross-bloc credit discount | 0.272 | 26.476 | 26.607 | 0.687 | 0.212 | 0.052 | 0.616 | 0.094 | 0.267 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 | 0.851 | 0.000 | 0.273 |
| Default pass + law registry | 0.868 | 89.730 | 103.333 | 0.492 | 0.398 | 0.171 | 0.392 | 0.836 | 0.598 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + law registry fast review | 0.868 | 89.698 | 103.333 | 0.492 | 0.394 | 0.171 | 0.392 | 0.840 | 0.593 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.994 | 0.000 | 1.000 |
| Default pass + law registry slow partial review | 0.857 | 88.476 | 103.333 | 0.494 | 0.424 | 0.169 | 0.392 | 0.777 | 0.603 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + member proposal quota | 0.810 | 80.566 | 95.806 | 0.497 | 0.449 | 0.168 | 0.393 | 0.639 | 0.658 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.956 | 0.000 | 0.963 |
| Default pass + multi-round mediation | 0.958 | 98.574 | 103.333 | 0.450 | 0.394 | 0.116 | 0.427 | 0.392 | 0.368 | 0.270 | 0.000 | 0.000 | 0.719 | 0.240 | 0.990 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.785 | 86.314 | 103.333 | 0.461 | 0.300 | 0.114 | 0.438 | 0.296 | 0.340 | 0.275 | 0.000 | 0.000 | 0.717 | 0.240 | 0.865 | 0.376 | 1.000 |
| Default pass + proposal bonds | 0.832 | 85.022 | 100.891 | 0.499 | 0.448 | 0.166 | 0.395 | 0.653 | 0.653 | 0.262 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.000 | 0.987 |
| Default pass + proposal bonds + challenge | 0.660 | 75.657 | 100.935 | 0.513 | 0.389 | 0.158 | 0.405 | 0.444 | 0.537 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.883 | 0.397 | 0.987 |
| Default pass + public objection window | 0.449 | 45.428 | 103.333 | 0.593 | 0.265 | 0.104 | 0.505 | 0.215 | 0.383 | 0.216 | 0.000 | 0.000 | 0.000 | 0.000 | 0.899 | 0.000 | 1.000 |
| Default pass + weighted agenda lottery | 0.408 | 41.833 | 47.833 | 0.549 | 0.420 | 0.137 | 0.445 | 0.294 | 0.599 | 0.231 | 0.000 | 0.000 | 0.000 | 0.000 | 0.648 | 0.000 | 0.465 |
| Bicameral majority + presidential veto | 0.113 | 10.863 | 103.333 | 0.682 | 0.000 | 0.070 | 0.616 | 0.032 | 0.214 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.301 | 0.000 | 1.000 |
| Unicameral simple majority | 0.268 | 26.267 | 103.333 | 0.636 | 0.000 | 0.092 | 0.553 | 0.104 | 0.310 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.651 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.090 | 8.542 | 103.333 | 0.707 | 0.000 | 0.061 | 0.652 | 0.020 | 0.147 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.662 | -0.261 | 0.023 | -0.066 | -0.300 | -0.138 | 0.500 |
| Low Polarization | -11.525 | -0.192 | 0.031 | -0.145 | -0.143 | -0.066 | 0.500 |
| High Polarization | -17.125 | -0.285 | 0.017 | -0.040 | -0.352 | -0.152 | 0.500 |
| Low Party Loyalty | -15.275 | -0.255 | 0.027 | -0.099 | -0.300 | -0.137 | 0.500 |
| High Party Loyalty | -15.375 | -0.256 | 0.021 | -0.058 | -0.300 | -0.142 | 0.500 |
| Low Compromise Culture | -15.563 | -0.259 | 0.021 | -0.054 | -0.299 | -0.142 | 0.500 |
| High Compromise Culture | -15.263 | -0.254 | 0.025 | -0.089 | -0.287 | -0.136 | 0.500 |
| Low Lobbying Pressure | -15.163 | -0.253 | 0.022 | -0.059 | -0.281 | -0.128 | 0.500 |
| High Lobbying Pressure | -15.113 | -0.252 | 0.018 | -0.053 | -0.297 | -0.143 | 0.500 |
| Weak Constituency Pressure | -18.213 | -0.304 | 0.024 | -0.067 | -0.325 | -0.137 | 0.498 |
| Two-Party System | -6.900 | -0.115 | -0.005 | -0.026 | -0.150 | -0.079 | 0.333 |
| Multi-Party System | -30.450 | -0.508 | 0.117 | -0.290 | -0.533 | -0.330 | 0.802 |
| High Proposal Pressure | 3.012 | 0.017 | -0.016 | 0.016 | -0.027 | -0.052 | 0.167 |
| Extreme Proposal Pressure | 21.738 | 0.072 | -0.022 | 0.020 | 0.020 | -0.049 | 0.100 |
| Lobby-Fueled Flooding | 2.662 | 0.015 | -0.016 | 0.012 | -0.030 | -0.053 | 0.167 |
| Low-Compromise Flooding | 2.612 | 0.015 | -0.017 | 0.027 | -0.048 | -0.076 | 0.167 |
| Capture Crisis | 1.738 | 0.010 | -0.013 | 0.018 | -0.042 | -0.061 | 0.167 |
| Popular Anti-Lobbying Push | -2.800 | -0.023 | -0.012 | -0.010 | -0.062 | -0.059 | 0.250 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.424 | -0.100 | 0.098 | 0.002 | -0.205 | -0.463 | -0.270 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.436 | 5.125 | 0.608 | 0.037 | 0.171 |

## Agenda-Scarcity Deltas

Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + weighted agenda lottery | -0.435 | -0.535 | 0.535 | 0.052 | -0.028 | 0.000 | 0.000 | 0.000 |
| Default pass + public objection window | -0.393 | 0.000 | 0.000 | 0.096 | -0.183 | 0.000 | 0.646 | 0.000 |
| Default pass + challenge vouchers | -0.172 | 0.000 | 0.000 | 0.014 | -0.054 | 0.000 | 0.000 | 0.000 |

## Roadmap-Completion Diagnostics

These scenarios cover the remaining planned gaps: constituent-grounded public signals, refundable proposal bonds, richer cosponsorship gates, multi-round mediation, strategic alternatives, challenge allocation/path variants, adaptive route sensitivity, and proposal-cost variants.

| Scenario | Productivity delta | Welfare delta | Low-support delta | False-negative pass | Public-will review | Public signal move | District alignment | Bond forfeiture | Cross-bloc admission | Cosponsors | Route fast/mid/high | Challenge exhaustion | Strategic decoys | Proposer access Gini | Welfare/submitted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Default pass + constituent public will | -0.005 | -0.002 | 0.010 | 0.000 | 1.000 | 0.282 | 0.427 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.415 |
| Default pass + constituent public will + citizen panel | -0.436 | 0.132 | -0.198 | 0.000 | 1.000 | 0.278 | 0.398 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.256 |
| Default pass + proposal bonds | -0.011 | 0.002 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.517 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.069 | 0.415 |
| Default pass + proposal bonds + challenge | -0.183 | 0.016 | -0.059 | 0.394 | 0.000 | 0.000 | 0.000 | 0.504 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.437 | 0.000 | 0.069 | 0.335 |
| Default pass + cross-bloc credit discount | -0.571 | 0.190 | -0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.273 | 6.005 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.146 | 0.184 |
| Default pass + affected-group sponsor gate | -0.651 | 0.228 | -0.294 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.192 | 4.840 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.170 | 0.138 |
| Default pass + multi-round mediation | 0.115 | -0.047 | -0.054 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.431 |
| Default pass + multi-round mediation + challenge | -0.058 | -0.036 | -0.148 | 0.403 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.425 | 0.000 | 0.070 | 0.361 |
| Default pass + strategic policy tournament | -0.292 | 0.144 | -0.406 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 4.000 | 0.094 | 0.353 |
| Default pass + proportional party challenge vouchers | -0.159 | 0.008 | -0.051 | 0.415 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.445 | 0.000 | 0.070 | 0.342 |
| Default pass + minority-bonus challenge vouchers | -0.208 | 0.023 | -0.076 | 0.369 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.408 | 0.000 | 0.070 | 0.325 |
| Default pass + challenge to 60 percent vote | -0.224 | 0.007 | -0.014 | 0.408 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.455 | 0.000 | 0.070 | 0.307 |
| Default pass + challenge to committee review | -0.194 | 0.011 | -0.038 | 0.407 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.451 | 0.000 | 0.088 | 0.326 |
| Default pass + challenge to info + active vote | -0.172 | 0.014 | -0.054 | 0.406 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.448 | 0.000 | 0.070 | 0.339 |
| Default pass + adaptive tracks lenient | -0.286 | 0.077 | -0.110 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.523/0.455/0.023 | 0.000 | 0.000 | 0.071 | 0.320 |
| Default pass + adaptive tracks strict | -0.559 | 0.151 | -0.371 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.091/0.612/0.296 | 0.000 | 0.000 | 0.083 | 0.184 |
| Default pass + adaptive tracks + citizen high-risk | -0.425 | 0.115 | -0.207 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.299/0.600/0.101 | 0.000 | 0.000 | 0.070 | 0.256 |
| Default pass + adaptive tracks + supermajority high-risk | -0.424 | 0.115 | -0.207 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.599/0.101 | 0.000 | 0.000 | 0.070 | 0.256 |
| Default pass + law registry fast review | 0.026 | -0.005 | -0.054 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.427 |
| Default pass + law registry slow partial review | 0.014 | -0.003 | -0.024 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.423 |
| Default pass + proposal costs + public waiver | -0.309 | 0.000 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.096 | 0.264 |
| Default pass + lobby-surcharge proposal costs | -0.336 | 0.035 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.098 | 0.268 |
| Default pass + member proposal quota | -0.032 | 0.000 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.067 | 0.403 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.292 | 0.144 | -0.406 | -0.660 | -0.652 | 0.001 | 0.002 | 6.000 | 0.449 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -21.312 | -29.025 | -0.355 | -0.022 | 0.042 | -0.078 | 0.443 |
| Low Polarization | -35.662 | -42.475 | -0.594 | -0.022 | 0.048 | -0.190 | 0.376 |
| High Polarization | -19.513 | -27.888 | -0.325 | -0.023 | 0.027 | -0.061 | 0.484 |
| Low Party Loyalty | -21.275 | -28.563 | -0.355 | -0.022 | 0.036 | -0.083 | 0.441 |
| High Party Loyalty | -21.175 | -29.725 | -0.353 | -0.026 | 0.045 | -0.078 | 0.442 |
| Low Compromise Culture | -20.725 | -29.675 | -0.345 | -0.027 | 0.037 | -0.077 | 0.449 |
| High Compromise Culture | -22.888 | -30.100 | -0.381 | -0.022 | 0.067 | -0.086 | 0.458 |
| Low Lobbying Pressure | -23.162 | -31.338 | -0.386 | -0.024 | 0.044 | -0.101 | 0.467 |
| High Lobbying Pressure | -19.750 | -28.000 | -0.329 | -0.026 | 0.034 | -0.073 | 0.405 |
| Weak Constituency Pressure | -22.750 | -28.963 | -0.379 | -0.016 | 0.045 | -0.090 | 0.437 |
| Two-Party System | -21.525 | -28.975 | -0.359 | -0.025 | 0.037 | -0.076 | 0.447 |
| Multi-Party System | -21.713 | -29.588 | -0.362 | -0.023 | 0.052 | -0.080 | 0.447 |
| High Proposal Pressure | -64.400 | -88.575 | -0.358 | -0.022 | 0.041 | -0.081 | 0.444 |
| Extreme Proposal Pressure | -105.750 | -145.663 | -0.353 | -0.022 | 0.043 | -0.078 | 0.442 |
| Lobby-Fueled Flooding | -61.325 | -85.438 | -0.341 | -0.025 | 0.031 | -0.068 | 0.421 |
| Low-Compromise Flooding | -58.450 | -84.413 | -0.325 | -0.021 | 0.033 | -0.060 | 0.456 |
| Capture Crisis | -58.300 | -82.563 | -0.324 | -0.021 | 0.022 | -0.064 | 0.422 |
| Popular Anti-Lobbying Push | -43.500 | -58.900 | -0.363 | -0.029 | 0.046 | -0.088 | 0.390 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Default pass + affected-group sponsor gate (0.719) | Default pass + multi-round mediation (0.959) | Unicameral simple majority (0.000) |
| Low Polarization | Default pass + strategic policy tournament (0.700) | Default pass + multi-round mediation (0.982) | Unicameral simple majority (0.000) |
| High Polarization | Default pass + affected-group sponsor gate (0.750) | Default pass + multi-round mediation (0.956) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Default pass + affected-group sponsor gate (0.724) | Default pass + multi-round mediation (0.969) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.721) | Default pass + multi-round mediation (0.961) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Default pass + affected-group sponsor gate (0.737) | Default pass + multi-round mediation (0.942) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.701) | Default pass + multi-round mediation (0.978) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.733) | Default pass + multi-round mediation (0.972) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + affected-group sponsor gate (0.747) | Default pass + multi-round mediation (0.934) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + affected-group sponsor gate (0.737) | Default pass + multi-round mediation (0.975) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + affected-group sponsor gate (0.742) | Default pass + multi-round mediation (0.965) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.714) | Default pass + multi-round mediation (0.969) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.719) | Default pass + multi-round mediation (0.965) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Default pass + affected-group sponsor gate (0.715) | Default pass + multi-round mediation (0.962) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + affected-group sponsor gate (0.747) | Default pass + multi-round mediation (0.937) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Default pass + affected-group sponsor gate (0.752) | Default pass + multi-round mediation (0.944) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + affected-group sponsor gate (0.763) | Default pass + multi-round mediation (0.925) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Default pass + affected-group sponsor gate (0.712) | Default pass + multi-round mediation (0.944) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Proposal-cost screens are useful for measuring flooding as institutional load: floor/run and enacted/run expose costs hidden by percentage-only metrics.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- The current cost screen reduces volume, but it also selects for proposals with high proposer value or positive lobby pressure; that makes cost design an object of study, not a solved safeguard.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Roadmap-completion scenarios add district-grounded public signals, refundable proposal bonds, richer cosponsorship diagnostics, multi-round mediation, strategic alternatives, challenge allocation/path variants, adaptive-route rates, and proposal-cost variants.
- The next model extension should move from mechanism coverage to endogenous strategy: proposers, lobby groups, challengers, and amendment coalitions should adapt to the institutional rules over repeated sessions.

## Reproduction

```sh
make campaign
```
