# Simulation Campaign v18

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 35
- experiment cases: 4

## Case Weights

Scenario averages in this campaign are weighted by the case likelihood column below.

| Case | Weight | Description |
| --- | ---: | --- |
| Weighted Two-Party Baseline | 0.250 | Classic two-party legislature with ideological left/right sorting. |
| Weighted Two Major Plus Minors | 0.400 | Five-party legislature with two large ideological parties and smaller minor parties. |
| Weighted Fragmented Multiparty | 0.200 | Seven-party legislature with more even fragmentation across the ideological range. |
| Weighted Dominant-Party Legislature | 0.150 | Four-party legislature with one large center-weighted party and smaller opposition parties. |

## Headline Findings

- Open default-pass averaged 0.835 productivity, versus 0.279 for simple majority.
- Open default-pass also averaged 0.448 low-support passage and 0.657 policy shift.
- Proposal-cost screening reduced floor load by 29.748 bills/run and enactments by 21.757 bills/run, but raised proposer gain by 0.435.
- Challenge vouchers averaged 0.674 challenge use, changed productivity by -0.377, and changed low-support passage by -0.220 relative to open default-pass.
- Adaptive tracks changed productivity by -0.413, low-support passage by -0.222, and policy shift by -0.450 relative to open default-pass.
- Weighted agenda lotteries changed floor consideration by -0.533, productivity by -0.429, and welfare by 0.052 relative to open default-pass.
- Public objection windows triggered on 0.643 of potential bills and changed low-support passage by -0.192 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.003, policy shift by -0.652, and status-quo wins averaged 0.444 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.717.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.181 | 10.876 | 60.000 | 0.671 | 0.000 | 0.070 | 0.605 | 0.056 | 0.237 | 0.203 | 0.000 | 0.000 | 0.000 | 0.000 | 0.534 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.835 | 50.072 | 60.000 | 0.497 | 0.448 | 0.163 | 0.398 | 0.657 | 0.652 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.421 | 25.277 | 54.550 | 0.610 | 0.226 | 0.095 | 0.530 | 0.207 | 0.394 | 0.195 | 0.000 | 0.000 | 0.000 | 0.000 | 0.908 | 0.000 | 0.909 |
| Default pass + adaptive tracks + citizen high-risk | 0.419 | 25.115 | 60.000 | 0.610 | 0.219 | 0.095 | 0.531 | 0.204 | 0.390 | 0.196 | 0.000 | 0.000 | 0.000 | 0.000 | 0.910 | 0.000 | 1.000 |
| Default pass + adaptive tracks lenient | 0.553 | 33.204 | 58.925 | 0.574 | 0.324 | 0.114 | 0.488 | 0.314 | 0.457 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 | 0.978 | 0.000 | 0.982 |
| Default pass + adaptive tracks strict | 0.289 | 17.340 | 43.222 | 0.646 | 0.048 | 0.078 | 0.574 | 0.115 | 0.320 | 0.196 | 0.000 | 0.000 | 0.000 | 0.000 | 0.757 | 0.000 | 0.720 |
| Default pass + adaptive tracks + supermajority high-risk | 0.420 | 25.173 | 60.000 | 0.610 | 0.222 | 0.095 | 0.530 | 0.204 | 0.389 | 0.194 | 0.000 | 0.000 | 0.000 | 0.000 | 0.910 | 0.000 | 1.000 |
| Default pass + affected-group sponsor gate | 0.249 | 14.926 | 15.014 | 0.691 | 0.158 | 0.038 | 0.666 | 0.101 | 0.304 | 0.151 | 0.000 | 0.000 | 0.000 | 0.000 | 0.807 | 0.000 | 0.250 |
| Default pass + pairwise policy tournament | 0.556 | 33.349 | 33.349 | 0.639 | 0.011 | 0.045 | 0.650 | 0.005 | 0.005 | 0.194 | 0.000 | 0.000 | 0.556 | 0.000 | 0.956 | 0.000 | 0.556 |
| Default pass + strategic policy tournament | 0.556 | 33.349 | 33.353 | 0.639 | 0.012 | 0.045 | 0.650 | 0.005 | 0.005 | 0.194 | 0.000 | 0.000 | 0.556 | 0.000 | 0.956 | 0.000 | 0.556 |
| Default pass + challenge vouchers | 0.457 | 27.425 | 60.000 | 0.571 | 0.228 | 0.120 | 0.479 | 0.255 | 0.406 | 0.229 | 0.000 | 0.000 | 0.000 | 0.000 | 0.815 | 0.674 | 1.000 |
| Default pass + challenge to committee review | 0.410 | 24.620 | 28.192 | 0.573 | 0.254 | 0.119 | 0.481 | 0.226 | 0.380 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.730 | 0.678 | 0.470 |
| Default pass + challenge to info + active vote | 0.451 | 27.083 | 60.000 | 0.575 | 0.232 | 0.121 | 0.469 | 0.248 | 0.396 | 0.228 | 0.000 | 0.000 | 0.000 | 0.000 | 0.816 | 0.676 | 1.000 |
| Default pass + minority-bonus challenge vouchers | 0.437 | 26.229 | 60.000 | 0.580 | 0.202 | 0.114 | 0.490 | 0.238 | 0.394 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.810 | 0.706 | 1.000 |
| Default pass + proportional party challenge vouchers | 0.457 | 27.428 | 60.000 | 0.568 | 0.231 | 0.121 | 0.478 | 0.259 | 0.422 | 0.230 | 0.000 | 0.000 | 0.000 | 0.000 | 0.814 | 0.681 | 1.000 |
| Default pass + challenge to 60 percent vote | 0.352 | 21.142 | 60.000 | 0.575 | 0.302 | 0.120 | 0.479 | 0.193 | 0.334 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.597 | 0.681 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.399 | 23.923 | 60.000 | 0.630 | 0.234 | 0.102 | 0.521 | 0.210 | 0.431 | 0.199 | 0.000 | 0.000 | 0.000 | 0.000 | 0.968 | 0.000 | 1.000 |
| Default pass + constituent public will | 0.831 | 49.859 | 60.000 | 0.495 | 0.460 | 0.154 | 0.383 | 0.647 | 0.647 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + proposal costs | 0.472 | 28.315 | 30.252 | 0.472 | 0.491 | 0.180 | 0.371 | 0.568 | 1.087 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 | 0.431 | 0.000 | 0.504 |
| Default pass + lobby-surcharge proposal costs | 0.515 | 30.915 | 33.109 | 0.526 | 0.455 | 0.145 | 0.424 | 0.535 | 0.915 | 0.185 | 0.000 | 0.000 | 0.000 | 0.000 | 0.843 | 0.000 | 0.552 |
| Default pass + proposal costs + public waiver | 0.532 | 31.946 | 34.120 | 0.495 | 0.468 | 0.166 | 0.401 | 0.589 | 0.984 | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 0.644 | 0.000 | 0.569 |
| Default pass + cross-bloc credit discount | 0.347 | 20.801 | 21.109 | 0.653 | 0.223 | 0.062 | 0.610 | 0.146 | 0.316 | 0.168 | 0.000 | 0.000 | 0.000 | 0.000 | 0.904 | 0.000 | 0.352 |
| Default pass + law registry | 0.861 | 51.642 | 60.000 | 0.491 | 0.395 | 0.167 | 0.396 | 0.824 | 0.595 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + law registry fast review | 0.862 | 51.731 | 60.000 | 0.491 | 0.393 | 0.167 | 0.396 | 0.827 | 0.587 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.995 | 0.000 | 1.000 |
| Default pass + law registry slow partial review | 0.849 | 50.945 | 60.000 | 0.495 | 0.414 | 0.165 | 0.397 | 0.774 | 0.603 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.995 | 0.000 | 1.000 |
| Default pass + member proposal quota | 0.829 | 49.755 | 59.675 | 0.497 | 0.451 | 0.163 | 0.397 | 0.652 | 0.651 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.989 | 0.000 | 0.995 |
| Default pass + multi-round mediation | 0.965 | 57.915 | 60.000 | 0.448 | 0.385 | 0.116 | 0.428 | 0.397 | 0.369 | 0.259 | 0.000 | 0.000 | 0.719 | 0.233 | 0.992 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.685 | 41.126 | 60.000 | 0.475 | 0.195 | 0.109 | 0.460 | 0.256 | 0.335 | 0.268 | 0.000 | 0.000 | 0.714 | 0.234 | 0.814 | 0.608 | 1.000 |
| Default pass + proposal bonds | 0.833 | 49.951 | 59.832 | 0.498 | 0.448 | 0.162 | 0.398 | 0.654 | 0.651 | 0.252 | 0.000 | 0.000 | 0.000 | 0.000 | 0.995 | 0.000 | 0.997 |
| Default pass + proposal bonds + challenge | 0.456 | 27.384 | 59.856 | 0.571 | 0.228 | 0.119 | 0.480 | 0.254 | 0.407 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.819 | 0.674 | 0.998 |
| Default pass + public objection window | 0.450 | 26.997 | 60.000 | 0.590 | 0.256 | 0.100 | 0.512 | 0.218 | 0.389 | 0.206 | 0.000 | 0.000 | 0.000 | 0.000 | 0.906 | 0.000 | 1.000 |
| Default pass + weighted agenda lottery | 0.406 | 24.344 | 28.000 | 0.549 | 0.412 | 0.132 | 0.452 | 0.291 | 0.588 | 0.222 | 0.000 | 0.000 | 0.000 | 0.000 | 0.651 | 0.000 | 0.467 |
| Bicameral majority + presidential veto | 0.117 | 7.045 | 60.000 | 0.688 | 0.000 | 0.061 | 0.630 | 0.033 | 0.214 | 0.206 | 0.000 | 0.000 | 0.000 | 0.000 | 0.365 | 0.000 | 1.000 |
| Unicameral simple majority | 0.279 | 16.743 | 60.000 | 0.637 | 0.000 | 0.085 | 0.562 | 0.111 | 0.320 | 0.212 | 0.000 | 0.000 | 0.000 | 0.000 | 0.718 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.098 | 5.868 | 60.000 | 0.717 | 0.000 | 0.052 | 0.663 | 0.021 | 0.158 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.324 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted Two-Party Baseline | -6.717 | -0.112 | -0.004 | -0.027 | -0.154 | -0.087 | 0.333 |
| Weighted Two Major Plus Minors | -29.933 | -0.499 | 0.112 | -0.289 | -0.536 | -0.343 | 0.797 |
| Weighted Fragmented Multiparty | -29.783 | -0.496 | 0.120 | -0.375 | -0.495 | -0.312 | 0.861 |
| Weighted Dominant-Party Legislature | -20.250 | -0.337 | 0.043 | -0.153 | -0.336 | -0.160 | 0.667 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.413 | -0.091 | 0.090 | 0.001 | -0.222 | -0.450 | -0.258 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.510 | 5.119 | 0.589 | 0.039 | 0.167 |

## Agenda-Scarcity Deltas

Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + weighted agenda lottery | -0.429 | -0.533 | 0.533 | 0.052 | -0.036 | 0.000 | 0.000 | 0.000 |
| Default pass + public objection window | -0.385 | 0.000 | 0.000 | 0.094 | -0.192 | 0.000 | 0.643 | 0.000 |
| Default pass + challenge vouchers | -0.377 | 0.000 | 0.000 | 0.074 | -0.220 | 0.000 | 0.000 | 0.000 |

## Roadmap-Completion Diagnostics

These scenarios cover the remaining planned gaps: constituent-grounded public signals, refundable proposal bonds, richer cosponsorship gates, multi-round mediation, strategic alternatives, challenge allocation/path variants, adaptive route sensitivity, and proposal-cost variants.

| Scenario | Productivity delta | Welfare delta | Low-support delta | False-negative pass | Public-will review | Public signal move | District alignment | Bond forfeiture | Cross-bloc admission | Cosponsors | Route fast/mid/high | Challenge exhaustion | Strategic decoys | Proposer access Gini | Welfare/submitted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Default pass + constituent public will | -0.004 | -0.002 | 0.012 | 0.000 | 1.000 | 0.283 | 0.427 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.411 |
| Default pass + constituent public will + citizen panel | -0.436 | 0.133 | -0.214 | 0.000 | 1.000 | 0.279 | 0.397 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.251 |
| Default pass + proposal bonds | -0.002 | 0.001 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.513 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.414 |
| Default pass + proposal bonds + challenge | -0.378 | 0.074 | -0.220 | 0.191 | 0.000 | 0.000 | 0.000 | 0.487 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.201 | 0.000 | 0.064 | 0.252 |
| Default pass + cross-bloc credit discount | -0.488 | 0.157 | -0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.352 | 7.999 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.117 | 0.224 |
| Default pass + affected-group sponsor gate | -0.586 | 0.194 | -0.290 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 6.339 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.134 | 0.170 |
| Default pass + multi-round mediation | 0.131 | -0.048 | -0.063 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.433 |
| Default pass + multi-round mediation + challenge | -0.149 | -0.021 | -0.253 | 0.240 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.210 | 0.000 | 0.064 | 0.325 |
| Default pass + strategic policy tournament | -0.279 | 0.142 | -0.436 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 4.000 | 0.090 | 0.355 |
| Default pass + proportional party challenge vouchers | -0.377 | 0.072 | -0.217 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.197 | 0.000 | 0.064 | 0.252 |
| Default pass + minority-bonus challenge vouchers | -0.397 | 0.084 | -0.245 | 0.170 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.173 | 0.000 | 0.064 | 0.245 |
| Default pass + challenge to 60 percent vote | -0.482 | 0.078 | -0.146 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.207 | 0.000 | 0.064 | 0.190 |
| Default pass + challenge to committee review | -0.424 | 0.077 | -0.194 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.204 | 0.000 | 0.103 | 0.225 |
| Default pass + challenge to info + active vote | -0.383 | 0.079 | -0.216 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.201 | 0.000 | 0.064 | 0.250 |
| Default pass + adaptive tracks lenient | -0.281 | 0.077 | -0.124 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.529/0.453/0.018 | 0.000 | 0.000 | 0.065 | 0.318 |
| Default pass + adaptive tracks strict | -0.546 | 0.149 | -0.400 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.091/0.623/0.287 | 0.000 | 0.000 | 0.078 | 0.187 |
| Default pass + adaptive tracks + citizen high-risk | -0.416 | 0.113 | -0.229 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.609/0.091 | 0.000 | 0.000 | 0.064 | 0.255 |
| Default pass + adaptive tracks + supermajority high-risk | -0.415 | 0.113 | -0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.609/0.090 | 0.000 | 0.000 | 0.064 | 0.256 |
| Default pass + law registry fast review | 0.028 | -0.006 | -0.055 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.423 |
| Default pass + law registry slow partial review | 0.015 | -0.002 | -0.034 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.420 |
| Default pass + proposal costs + public waiver | -0.302 | -0.001 | 0.020 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.085 | 0.264 |
| Default pass + lobby-surcharge proposal costs | -0.319 | 0.029 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.081 | 0.271 |
| Default pass + member proposal quota | -0.005 | 0.000 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.412 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.279 | 0.142 | -0.437 | -0.652 | -0.647 | 0.001 | 0.003 | 6.000 | 0.444 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted Two-Party Baseline | -20.950 | -28.508 | -0.349 | -0.022 | 0.038 | -0.084 | 0.428 |
| Weighted Two Major Plus Minors | -21.658 | -29.667 | -0.361 | -0.024 | 0.040 | -0.085 | 0.449 |
| Weighted Fragmented Multiparty | -23.067 | -30.992 | -0.384 | -0.027 | 0.050 | -0.108 | 0.415 |
| Weighted Dominant-Party Legislature | -21.617 | -30.375 | -0.360 | -0.025 | 0.053 | -0.079 | 0.436 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Weighted Two-Party Baseline | Default pass + affected-group sponsor gate (0.739) | Default pass + multi-round mediation (0.963) | Unicameral simple majority (0.000) |
| Weighted Two Major Plus Minors | Unicameral 60 percent passage (0.711) | Default pass + multi-round mediation (0.967) | Unicameral simple majority (0.000) |
| Weighted Fragmented Multiparty | Unicameral 60 percent passage (0.714) | Default pass + multi-round mediation (0.969) | Unicameral simple majority (0.000) |
| Weighted Dominant-Party Legislature | Unicameral 60 percent passage (0.727) | Default pass + multi-round mediation (0.961) | Unicameral simple majority (0.000) |

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
