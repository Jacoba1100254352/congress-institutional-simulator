# Simulation Campaign v17

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 80
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 38
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.843 productivity, versus 0.268 for simple majority.
- Open default-pass also averaged 0.448 low-support passage and 0.664 policy shift.
- Proposal-cost screening reduced floor load by 50.565 bills/run and enactments by 36.938 bills/run, but raised proposer gain by 0.438.
- Challenge vouchers averaged 0.397 challenge use, changed productivity by -0.172, and changed low-support passage by -0.055 relative to open default-pass.
- Adaptive tracks changed productivity by -0.425, low-support passage by -0.208, and policy shift by -0.464 relative to open default-pass.
- Weighted agenda lotteries changed floor consideration by -0.535, productivity by -0.436, and welfare by 0.052 relative to open default-pass.
- Public objection windows triggered on 0.647 of potential bills and changed low-support passage by -0.180 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.660, and status-quo wins averaged 0.449 relative to open default-pass.
- Best average welfare in this campaign came from Default pass + affected-group sponsor gate at 0.725.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.175 | 16.869 | 103.333 | 0.665 | 0.000 | 0.077 | 0.594 | 0.053 | 0.229 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.843 | 86.979 | 103.333 | 0.497 | 0.448 | 0.168 | 0.393 | 0.664 | 0.656 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive proposers | 0.863 | 88.983 | 103.310 | 0.493 | 0.446 | 0.171 | 0.395 | 0.577 | 0.597 | 0.268 | 0.000 | 0.000 | 1.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive proposers + strategic lobbying | 0.863 | 89.040 | 103.310 | 0.492 | 0.447 | 0.171 | 0.394 | 0.577 | 0.597 | 0.269 | 0.111 | 0.618 | 1.000 | 0.000 | 0.991 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.418 | 42.205 | 92.335 | 0.612 | 0.240 | 0.098 | 0.525 | 0.200 | 0.386 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 | 0.896 | 0.000 | 0.900 |
| Default pass + adaptive tracks + citizen high-risk | 0.417 | 42.133 | 103.333 | 0.612 | 0.244 | 0.098 | 0.525 | 0.199 | 0.384 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 | 0.895 | 0.000 | 1.000 |
| Default pass + adaptive tracks lenient | 0.556 | 56.472 | 100.747 | 0.574 | 0.337 | 0.118 | 0.481 | 0.314 | 0.460 | 0.213 | 0.000 | 0.000 | 0.000 | 0.000 | 0.972 | 0.000 | 0.978 |
| Default pass + adaptive tracks strict | 0.285 | 28.290 | 72.878 | 0.647 | 0.078 | 0.084 | 0.566 | 0.111 | 0.311 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.717 | 0.000 | 0.714 |
| Default pass + adaptive tracks + supermajority high-risk | 0.420 | 42.308 | 103.333 | 0.611 | 0.239 | 0.099 | 0.524 | 0.201 | 0.385 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 | 0.898 | 0.000 | 1.000 |
| Default pass + affected-group sponsor gate | 0.192 | 18.649 | 18.678 | 0.725 | 0.154 | 0.032 | 0.666 | 0.062 | 0.241 | 0.135 | 0.000 | 0.000 | 0.000 | 0.000 | 0.725 | 0.000 | 0.192 |
| Default pass + pairwise policy tournament | 0.551 | 56.412 | 56.423 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.201 | 0.000 | 0.000 | 0.551 | 0.000 | 0.944 | 0.000 | 0.551 |
| Default pass + strategic policy tournament | 0.551 | 56.416 | 56.423 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.201 | 0.000 | 0.000 | 0.551 | 0.000 | 0.945 | 0.000 | 0.551 |
| Default pass + challenge vouchers | 0.671 | 77.963 | 103.333 | 0.510 | 0.393 | 0.161 | 0.402 | 0.456 | 0.541 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.882 | 0.397 | 1.000 |
| Default pass + challenge to committee review | 0.648 | 76.270 | 78.967 | 0.508 | 0.410 | 0.162 | 0.399 | 0.442 | 0.540 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.845 | 0.397 | 0.683 |
| Default pass + challenge to info + active vote | 0.670 | 77.928 | 103.333 | 0.511 | 0.394 | 0.161 | 0.398 | 0.455 | 0.539 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.889 | 0.397 | 1.000 |
| Default pass + minority-bonus challenge vouchers | 0.635 | 75.106 | 103.333 | 0.519 | 0.372 | 0.155 | 0.412 | 0.421 | 0.524 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.884 | 0.442 | 1.000 |
| Default pass + proportional party challenge vouchers | 0.684 | 78.967 | 103.333 | 0.505 | 0.397 | 0.163 | 0.397 | 0.470 | 0.549 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.875 | 0.397 | 1.000 |
| Default pass + challenge to 60 percent vote | 0.619 | 74.059 | 103.333 | 0.503 | 0.435 | 0.164 | 0.393 | 0.427 | 0.542 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.784 | 0.398 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.407 | 41.312 | 103.333 | 0.629 | 0.250 | 0.106 | 0.516 | 0.213 | 0.435 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.964 | 0.000 | 1.000 |
| Default pass + constituent public will | 0.837 | 86.473 | 103.333 | 0.495 | 0.458 | 0.157 | 0.381 | 0.655 | 0.654 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + proposal costs | 0.475 | 50.041 | 52.768 | 0.474 | 0.488 | 0.184 | 0.368 | 0.579 | 1.094 | 0.286 | 0.000 | 0.000 | 0.000 | 0.000 | 0.450 | 0.000 | 0.503 |
| Default pass + lobby-surcharge proposal costs | 0.506 | 51.803 | 55.376 | 0.531 | 0.460 | 0.146 | 0.422 | 0.531 | 0.925 | 0.180 | 0.000 | 0.000 | 0.000 | 0.000 | 0.845 | 0.000 | 0.541 |
| Default pass + proposal costs + public waiver | 0.534 | 55.621 | 58.734 | 0.497 | 0.467 | 0.170 | 0.397 | 0.598 | 0.996 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.652 | 0.000 | 0.565 |
| Default pass + cross-bloc credit discount | 0.272 | 26.476 | 26.607 | 0.687 | 0.212 | 0.052 | 0.616 | 0.094 | 0.267 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 | 0.851 | 0.000 | 0.273 |
| Default pass + law registry | 0.867 | 89.653 | 103.333 | 0.492 | 0.396 | 0.170 | 0.392 | 0.836 | 0.598 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + law registry fast review | 0.869 | 89.735 | 103.333 | 0.491 | 0.396 | 0.171 | 0.392 | 0.839 | 0.592 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.994 | 0.000 | 1.000 |
| Default pass + law registry slow partial review | 0.857 | 88.486 | 103.333 | 0.494 | 0.424 | 0.169 | 0.392 | 0.778 | 0.603 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.000 | 1.000 |
| Default pass + member proposal quota | 0.811 | 80.633 | 95.806 | 0.497 | 0.449 | 0.168 | 0.392 | 0.640 | 0.658 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.955 | 0.000 | 0.963 |
| Default pass + multi-round mediation | 0.958 | 98.574 | 103.333 | 0.450 | 0.394 | 0.116 | 0.427 | 0.392 | 0.368 | 0.270 | 0.000 | 0.000 | 0.719 | 0.240 | 0.990 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.785 | 86.314 | 103.333 | 0.461 | 0.300 | 0.114 | 0.438 | 0.296 | 0.340 | 0.275 | 0.000 | 0.000 | 0.717 | 0.240 | 0.865 | 0.376 | 1.000 |
| Default pass + proposal bonds | 0.832 | 85.022 | 100.891 | 0.499 | 0.448 | 0.166 | 0.395 | 0.653 | 0.653 | 0.262 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.000 | 0.987 |
| Default pass + proposal bonds + challenge | 0.660 | 75.657 | 100.935 | 0.513 | 0.389 | 0.158 | 0.405 | 0.444 | 0.537 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.883 | 0.397 | 0.987 |
| Default pass + public objection window | 0.448 | 45.285 | 103.333 | 0.593 | 0.268 | 0.104 | 0.506 | 0.214 | 0.384 | 0.216 | 0.000 | 0.000 | 0.000 | 0.000 | 0.896 | 0.000 | 1.000 |
| Default pass + strategic lobbying | 0.842 | 86.907 | 103.333 | 0.496 | 0.448 | 0.168 | 0.392 | 0.665 | 0.657 | 0.266 | 0.110 | 0.629 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Default pass + weighted agenda lottery | 0.407 | 41.790 | 47.833 | 0.549 | 0.419 | 0.138 | 0.445 | 0.296 | 0.602 | 0.232 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 0.465 |
| Bicameral majority + presidential veto | 0.111 | 10.726 | 103.333 | 0.683 | 0.000 | 0.069 | 0.618 | 0.031 | 0.212 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.295 | 0.000 | 1.000 |
| Unicameral simple majority | 0.268 | 26.267 | 103.333 | 0.636 | 0.000 | 0.092 | 0.553 | 0.104 | 0.310 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.651 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.090 | 8.542 | 103.333 | 0.707 | 0.000 | 0.061 | 0.652 | 0.020 | 0.147 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.862 | -0.264 | 0.024 | -0.076 | -0.308 | -0.147 | 0.500 |
| Low Polarization | -11.550 | -0.193 | 0.028 | -0.136 | -0.143 | -0.063 | 0.499 |
| High Polarization | -17.313 | -0.289 | 0.014 | -0.042 | -0.350 | -0.145 | 0.500 |
| Low Party Loyalty | -15.300 | -0.255 | 0.026 | -0.095 | -0.297 | -0.135 | 0.500 |
| High Party Loyalty | -15.075 | -0.251 | 0.022 | -0.071 | -0.294 | -0.139 | 0.500 |
| Low Compromise Culture | -15.888 | -0.265 | 0.019 | -0.050 | -0.301 | -0.136 | 0.500 |
| High Compromise Culture | -14.925 | -0.249 | 0.026 | -0.097 | -0.278 | -0.128 | 0.500 |
| Low Lobbying Pressure | -15.150 | -0.253 | 0.022 | -0.069 | -0.285 | -0.135 | 0.500 |
| High Lobbying Pressure | -15.300 | -0.255 | 0.016 | -0.053 | -0.296 | -0.139 | 0.500 |
| Weak Constituency Pressure | -18.425 | -0.307 | 0.021 | -0.064 | -0.331 | -0.144 | 0.498 |
| Two-Party System | -6.813 | -0.114 | -0.005 | -0.029 | -0.148 | -0.078 | 0.333 |
| Multi-Party System | -30.375 | -0.506 | 0.116 | -0.296 | -0.529 | -0.319 | 0.804 |
| High Proposal Pressure | 3.412 | 0.019 | -0.016 | 0.014 | -0.027 | -0.055 | 0.167 |
| Extreme Proposal Pressure | 21.838 | 0.073 | -0.022 | 0.024 | 0.020 | -0.050 | 0.100 |
| Lobby-Fueled Flooding | 2.988 | 0.017 | -0.016 | 0.011 | -0.029 | -0.053 | 0.167 |
| Low-Compromise Flooding | 2.762 | 0.015 | -0.017 | 0.025 | -0.049 | -0.078 | 0.167 |
| Capture Crisis | 1.700 | 0.009 | -0.013 | 0.014 | -0.042 | -0.061 | 0.167 |
| Popular Anti-Lobbying Push | -3.013 | -0.025 | -0.012 | -0.009 | -0.063 | -0.059 | 0.250 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.425 | -0.100 | 0.097 | 0.002 | -0.208 | -0.464 | -0.270 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.025 | -0.005 | 0.436 | 5.125 | 0.608 | 0.037 | 0.172 |

## Agenda-Scarcity Deltas

Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + weighted agenda lottery | -0.436 | -0.535 | 0.535 | 0.052 | -0.028 | 0.000 | 0.000 | 0.000 |
| Default pass + public objection window | -0.395 | 0.000 | 0.000 | 0.096 | -0.180 | 0.000 | 0.647 | 0.000 |
| Default pass + challenge vouchers | -0.172 | 0.000 | 0.000 | 0.013 | -0.055 | 0.000 | 0.000 | 0.000 |

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
| Default pass + adaptive proposers | 0.020 | -0.004 | -0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.425 |
| Default pass + adaptive proposers + strategic lobbying | 0.020 | -0.005 | -0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.425 |
| Default pass + strategic lobbying | -0.001 | -0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.418 |
| Default pass + proportional party challenge vouchers | -0.159 | 0.008 | -0.051 | 0.415 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.445 | 0.000 | 0.070 | 0.342 |
| Default pass + minority-bonus challenge vouchers | -0.207 | 0.023 | -0.076 | 0.369 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.408 | 0.000 | 0.070 | 0.325 |
| Default pass + challenge to 60 percent vote | -0.224 | 0.006 | -0.013 | 0.409 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.455 | 0.000 | 0.070 | 0.307 |
| Default pass + challenge to committee review | -0.195 | 0.011 | -0.038 | 0.407 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.451 | 0.000 | 0.088 | 0.325 |
| Default pass + challenge to info + active vote | -0.172 | 0.014 | -0.054 | 0.407 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.449 | 0.000 | 0.070 | 0.338 |
| Default pass + adaptive tracks lenient | -0.286 | 0.077 | -0.111 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.523/0.455/0.022 | 0.000 | 0.000 | 0.071 | 0.320 |
| Default pass + adaptive tracks strict | -0.557 | 0.150 | -0.370 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.091/0.612/0.297 | 0.000 | 0.000 | 0.083 | 0.185 |
| Default pass + adaptive tracks + citizen high-risk | -0.425 | 0.115 | -0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.600/0.101 | 0.000 | 0.000 | 0.070 | 0.256 |
| Default pass + adaptive tracks + supermajority high-risk | -0.423 | 0.115 | -0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.599/0.101 | 0.000 | 0.000 | 0.070 | 0.257 |
| Default pass + law registry fast review | 0.026 | -0.005 | -0.052 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.427 |
| Default pass + law registry slow partial review | 0.015 | -0.003 | -0.024 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.070 | 0.423 |
| Default pass + proposal costs + public waiver | -0.309 | 0.000 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.095 | 0.264 |
| Default pass + lobby-surcharge proposal costs | -0.336 | 0.034 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.099 | 0.268 |
| Default pass + member proposal quota | -0.031 | -0.000 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.067 | 0.403 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.292 | 0.144 | -0.406 | -0.660 | -0.652 | 0.001 | 0.002 | 6.000 | 0.449 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -21.125 | -28.875 | -0.352 | -0.023 | 0.038 | -0.073 | 0.444 |
| Low Polarization | -35.925 | -42.538 | -0.599 | -0.020 | 0.041 | -0.194 | 0.380 |
| High Polarization | -19.550 | -27.913 | -0.326 | -0.022 | 0.032 | -0.063 | 0.483 |
| Low Party Loyalty | -21.237 | -28.638 | -0.354 | -0.022 | 0.037 | -0.080 | 0.446 |
| High Party Loyalty | -21.538 | -29.813 | -0.359 | -0.026 | 0.055 | -0.086 | 0.442 |
| Low Compromise Culture | -20.850 | -29.775 | -0.348 | -0.026 | 0.031 | -0.079 | 0.449 |
| High Compromise Culture | -22.913 | -30.138 | -0.382 | -0.022 | 0.064 | -0.087 | 0.458 |
| Low Lobbying Pressure | -23.263 | -31.375 | -0.388 | -0.023 | 0.058 | -0.101 | 0.469 |
| High Lobbying Pressure | -19.638 | -27.938 | -0.327 | -0.027 | 0.036 | -0.070 | 0.407 |
| Weak Constituency Pressure | -22.763 | -29.100 | -0.379 | -0.015 | 0.031 | -0.090 | 0.438 |
| Two-Party System | -21.887 | -29.250 | -0.365 | -0.025 | 0.042 | -0.082 | 0.449 |
| Multi-Party System | -21.862 | -29.525 | -0.364 | -0.022 | 0.051 | -0.085 | 0.445 |
| High Proposal Pressure | -64.300 | -88.200 | -0.357 | -0.022 | 0.041 | -0.081 | 0.441 |
| Extreme Proposal Pressure | -105.712 | -145.588 | -0.352 | -0.022 | 0.042 | -0.078 | 0.444 |
| Lobby-Fueled Flooding | -61.650 | -85.413 | -0.343 | -0.025 | 0.025 | -0.070 | 0.422 |
| Low-Compromise Flooding | -58.488 | -84.475 | -0.325 | -0.021 | 0.033 | -0.060 | 0.456 |
| Capture Crisis | -58.675 | -82.825 | -0.326 | -0.021 | 0.026 | -0.067 | 0.422 |
| Popular Anti-Lobbying Push | -43.513 | -58.800 | -0.363 | -0.030 | 0.038 | -0.087 | 0.391 |

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
- Roadmap-completion scenarios add district-grounded public signals, refundable proposal bonds, richer cosponsorship diagnostics, multi-round mediation, strategic alternatives, adaptive proposer behavior, strategic lobby-channel learning, challenge allocation/path variants, adaptive-route rates, and proposal-cost variants.
- The next model extension should deepen endogeneity: challengers, amendment coalitions, constituent publics, and alternative drafters should adapt to the institutional rules over repeated sessions.

## Reproduction

```sh
make campaign
```
