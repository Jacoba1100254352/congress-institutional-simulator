# Simulation Campaign v18

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 38
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
- Proposal-cost screening reduced floor load by 29.786 bills/run and enactments by 21.735 bills/run, but raised proposer gain by 0.436.
- Challenge vouchers averaged 0.676 challenge use, changed productivity by -0.379, and changed low-support passage by -0.221 relative to open default-pass.
- Adaptive tracks changed productivity by -0.414, low-support passage by -0.227, and policy shift by -0.453 relative to open default-pass.
- Weighted agenda lotteries changed floor consideration by -0.533, productivity by -0.430, and welfare by 0.052 relative to open default-pass.
- Public objection windows triggered on 0.645 of potential bills and changed low-support passage by -0.195 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.003, policy shift by -0.652, and status-quo wins averaged 0.444 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.717.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.186 | 11.160 | 60.000 | 0.668 | 0.000 | 0.070 | 0.604 | 0.059 | 0.246 | 0.206 | 0.000 | 0.000 | 0.000 | 0.000 | 0.536 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.835 | 50.072 | 60.000 | 0.497 | 0.448 | 0.163 | 0.398 | 0.657 | 0.652 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive proposers | 0.861 | 51.637 | 60.000 | 0.492 | 0.442 | 0.166 | 0.398 | 0.575 | 0.595 | 0.257 | 0.000 | 0.000 | 1.000 | 0.000 | 0.994 | 0.000 | 1.000 |
| Default pass + adaptive proposers + strategic lobbying | 0.862 | 51.726 | 60.000 | 0.491 | 0.443 | 0.166 | 0.398 | 0.577 | 0.596 | 0.258 | 0.145 | 0.593 | 1.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.420 | 25.228 | 54.606 | 0.609 | 0.221 | 0.095 | 0.530 | 0.204 | 0.389 | 0.195 | 0.000 | 0.000 | 0.000 | 0.000 | 0.910 | 0.000 | 0.910 |
| Default pass + adaptive tracks + citizen high-risk | 0.419 | 25.135 | 60.000 | 0.610 | 0.219 | 0.095 | 0.531 | 0.203 | 0.388 | 0.194 | 0.000 | 0.000 | 0.000 | 0.000 | 0.912 | 0.000 | 1.000 |
| Default pass + adaptive tracks lenient | 0.554 | 33.236 | 58.929 | 0.574 | 0.322 | 0.114 | 0.487 | 0.313 | 0.457 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 | 0.978 | 0.000 | 0.982 |
| Default pass + adaptive tracks strict | 0.290 | 17.397 | 43.269 | 0.645 | 0.055 | 0.080 | 0.573 | 0.117 | 0.322 | 0.197 | 0.000 | 0.000 | 0.000 | 0.000 | 0.757 | 0.000 | 0.721 |
| Default pass + adaptive tracks + supermajority high-risk | 0.417 | 25.016 | 60.000 | 0.610 | 0.222 | 0.094 | 0.531 | 0.202 | 0.387 | 0.195 | 0.000 | 0.000 | 0.000 | 0.000 | 0.911 | 0.000 | 1.000 |
| Default pass + affected-group sponsor gate | 0.249 | 14.926 | 15.014 | 0.691 | 0.158 | 0.038 | 0.666 | 0.101 | 0.304 | 0.151 | 0.000 | 0.000 | 0.000 | 0.000 | 0.807 | 0.000 | 0.250 |
| Default pass + pairwise policy tournament | 0.556 | 33.349 | 33.349 | 0.639 | 0.011 | 0.045 | 0.650 | 0.005 | 0.005 | 0.194 | 0.000 | 0.000 | 0.556 | 0.000 | 0.956 | 0.000 | 0.556 |
| Default pass + strategic policy tournament | 0.556 | 33.349 | 33.353 | 0.639 | 0.012 | 0.045 | 0.650 | 0.005 | 0.005 | 0.194 | 0.000 | 0.000 | 0.556 | 0.000 | 0.956 | 0.000 | 0.556 |
| Default pass + challenge vouchers | 0.455 | 27.315 | 60.000 | 0.571 | 0.226 | 0.119 | 0.479 | 0.254 | 0.407 | 0.227 | 0.000 | 0.000 | 0.000 | 0.000 | 0.816 | 0.676 | 1.000 |
| Default pass + challenge to committee review | 0.410 | 24.618 | 28.005 | 0.573 | 0.256 | 0.118 | 0.482 | 0.225 | 0.376 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.728 | 0.677 | 0.467 |
| Default pass + challenge to info + active vote | 0.450 | 27.012 | 60.000 | 0.576 | 0.232 | 0.122 | 0.470 | 0.249 | 0.399 | 0.228 | 0.000 | 0.000 | 0.000 | 0.000 | 0.810 | 0.677 | 1.000 |
| Default pass + minority-bonus challenge vouchers | 0.436 | 26.136 | 60.000 | 0.579 | 0.204 | 0.114 | 0.489 | 0.234 | 0.387 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.801 | 0.705 | 1.000 |
| Default pass + proportional party challenge vouchers | 0.460 | 27.600 | 60.000 | 0.568 | 0.229 | 0.122 | 0.476 | 0.261 | 0.420 | 0.230 | 0.000 | 0.000 | 0.000 | 0.000 | 0.819 | 0.681 | 1.000 |
| Default pass + challenge to 60 percent vote | 0.352 | 21.095 | 60.000 | 0.575 | 0.302 | 0.119 | 0.479 | 0.192 | 0.332 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.590 | 0.681 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.399 | 23.923 | 60.000 | 0.630 | 0.234 | 0.102 | 0.521 | 0.210 | 0.431 | 0.199 | 0.000 | 0.000 | 0.000 | 0.000 | 0.968 | 0.000 | 1.000 |
| Default pass + constituent public will | 0.831 | 49.859 | 60.000 | 0.495 | 0.460 | 0.154 | 0.383 | 0.647 | 0.647 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + proposal costs | 0.472 | 28.337 | 30.214 | 0.472 | 0.493 | 0.180 | 0.370 | 0.570 | 1.088 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 | 0.437 | 0.000 | 0.504 |
| Default pass + lobby-surcharge proposal costs | 0.513 | 30.801 | 33.071 | 0.527 | 0.453 | 0.146 | 0.424 | 0.532 | 0.916 | 0.185 | 0.000 | 0.000 | 0.000 | 0.000 | 0.843 | 0.000 | 0.551 |
| Default pass + proposal costs + public waiver | 0.532 | 31.917 | 34.114 | 0.495 | 0.465 | 0.166 | 0.401 | 0.588 | 0.985 | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 0.641 | 0.000 | 0.569 |
| Default pass + cross-bloc credit discount | 0.347 | 20.801 | 21.109 | 0.653 | 0.223 | 0.062 | 0.610 | 0.146 | 0.316 | 0.168 | 0.000 | 0.000 | 0.000 | 0.000 | 0.904 | 0.000 | 0.352 |
| Default pass + law registry | 0.862 | 51.718 | 60.000 | 0.491 | 0.392 | 0.167 | 0.396 | 0.826 | 0.595 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + law registry fast review | 0.861 | 51.633 | 60.000 | 0.491 | 0.391 | 0.167 | 0.396 | 0.827 | 0.587 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.994 | 0.000 | 1.000 |
| Default pass + law registry slow partial review | 0.849 | 50.914 | 60.000 | 0.495 | 0.416 | 0.165 | 0.398 | 0.771 | 0.601 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.994 | 0.000 | 1.000 |
| Default pass + member proposal quota | 0.832 | 49.899 | 59.675 | 0.497 | 0.444 | 0.163 | 0.397 | 0.652 | 0.650 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.988 | 0.000 | 0.995 |
| Default pass + multi-round mediation | 0.965 | 57.915 | 60.000 | 0.448 | 0.385 | 0.116 | 0.428 | 0.397 | 0.369 | 0.259 | 0.000 | 0.000 | 0.719 | 0.233 | 0.992 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.685 | 41.126 | 60.000 | 0.475 | 0.195 | 0.109 | 0.460 | 0.256 | 0.335 | 0.268 | 0.000 | 0.000 | 0.714 | 0.234 | 0.814 | 0.608 | 1.000 |
| Default pass + proposal bonds | 0.833 | 49.951 | 59.832 | 0.498 | 0.448 | 0.162 | 0.398 | 0.654 | 0.651 | 0.252 | 0.000 | 0.000 | 0.000 | 0.000 | 0.995 | 0.000 | 0.997 |
| Default pass + proposal bonds + challenge | 0.456 | 27.384 | 59.856 | 0.571 | 0.228 | 0.119 | 0.480 | 0.254 | 0.407 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.819 | 0.674 | 0.998 |
| Default pass + public objection window | 0.444 | 26.621 | 60.000 | 0.593 | 0.253 | 0.099 | 0.514 | 0.212 | 0.382 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 | 0.915 | 0.000 | 1.000 |
| Default pass + strategic lobbying | 0.834 | 50.054 | 60.000 | 0.496 | 0.448 | 0.163 | 0.397 | 0.654 | 0.650 | 0.256 | 0.142 | 0.604 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Default pass + weighted agenda lottery | 0.404 | 24.263 | 28.000 | 0.549 | 0.414 | 0.134 | 0.450 | 0.290 | 0.589 | 0.222 | 0.000 | 0.000 | 0.000 | 0.000 | 0.634 | 0.000 | 0.467 |
| Bicameral majority + presidential veto | 0.118 | 7.104 | 60.000 | 0.691 | 0.000 | 0.063 | 0.630 | 0.033 | 0.211 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.373 | 0.000 | 1.000 |
| Unicameral simple majority | 0.279 | 16.743 | 60.000 | 0.637 | 0.000 | 0.085 | 0.562 | 0.111 | 0.320 | 0.212 | 0.000 | 0.000 | 0.000 | 0.000 | 0.718 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.098 | 5.868 | 60.000 | 0.717 | 0.000 | 0.052 | 0.663 | 0.021 | 0.158 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.324 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted Two-Party Baseline | -6.842 | -0.114 | -0.005 | -0.030 | -0.156 | -0.086 | 0.333 |
| Weighted Two Major Plus Minors | -30.275 | -0.505 | 0.112 | -0.288 | -0.540 | -0.346 | 0.801 |
| Weighted Fragmented Multiparty | -29.575 | -0.493 | 0.122 | -0.376 | -0.490 | -0.303 | 0.863 |
| Weighted Dominant-Party Legislature | -20.142 | -0.336 | 0.042 | -0.157 | -0.335 | -0.164 | 0.667 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.414 | -0.090 | 0.089 | 0.001 | -0.227 | -0.453 | -0.262 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.027 | -0.005 | 0.513 | 5.126 | 0.587 | 0.038 | 0.169 |

## Agenda-Scarcity Deltas

Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + weighted agenda lottery | -0.430 | -0.533 | 0.533 | 0.052 | -0.034 | 0.000 | 0.000 | 0.000 |
| Default pass + public objection window | -0.391 | 0.000 | 0.000 | 0.096 | -0.195 | 0.000 | 0.645 | 0.000 |
| Default pass + challenge vouchers | -0.379 | 0.000 | 0.000 | 0.074 | -0.221 | 0.000 | 0.000 | 0.000 |

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
| Default pass + adaptive proposers | 0.026 | -0.004 | -0.006 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.424 |
| Default pass + adaptive proposers + strategic lobbying | 0.028 | -0.005 | -0.005 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.424 |
| Default pass + strategic lobbying | -0.000 | -0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.414 |
| Default pass + proportional party challenge vouchers | -0.375 | 0.072 | -0.219 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.196 | 0.000 | 0.064 | 0.253 |
| Default pass + minority-bonus challenge vouchers | -0.399 | 0.082 | -0.244 | 0.171 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.174 | 0.000 | 0.064 | 0.243 |
| Default pass + challenge to 60 percent vote | -0.483 | 0.078 | -0.146 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.206 | 0.000 | 0.064 | 0.189 |
| Default pass + challenge to committee review | -0.424 | 0.077 | -0.192 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.204 | 0.000 | 0.102 | 0.225 |
| Default pass + challenge to info + active vote | -0.384 | 0.079 | -0.215 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.202 | 0.000 | 0.064 | 0.250 |
| Default pass + adaptive tracks lenient | -0.281 | 0.078 | -0.126 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.528/0.454/0.018 | 0.000 | 0.000 | 0.065 | 0.318 |
| Default pass + adaptive tracks strict | -0.545 | 0.148 | -0.393 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.090/0.623/0.287 | 0.000 | 0.000 | 0.079 | 0.187 |
| Default pass + adaptive tracks + citizen high-risk | -0.416 | 0.114 | -0.229 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.299/0.609/0.091 | 0.000 | 0.000 | 0.064 | 0.256 |
| Default pass + adaptive tracks + supermajority high-risk | -0.418 | 0.113 | -0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.300/0.609/0.091 | 0.000 | 0.000 | 0.064 | 0.254 |
| Default pass + law registry fast review | 0.026 | -0.005 | -0.056 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.423 |
| Default pass + law registry slow partial review | 0.014 | -0.002 | -0.032 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.420 |
| Default pass + proposal costs + public waiver | -0.303 | -0.001 | 0.017 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.085 | 0.263 |
| Default pass + lobby-surcharge proposal costs | -0.321 | 0.030 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.082 | 0.270 |
| Default pass + member proposal quota | -0.003 | 0.000 | -0.004 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000/0.000/0.000 | 0.000 | 0.000 | 0.064 | 0.413 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.279 | 0.142 | -0.437 | -0.652 | -0.647 | 0.001 | 0.003 | 6.000 | 0.444 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted Two-Party Baseline | -20.842 | -28.600 | -0.347 | -0.022 | 0.038 | -0.081 | 0.428 |
| Weighted Two Major Plus Minors | -21.617 | -29.683 | -0.360 | -0.026 | 0.042 | -0.084 | 0.449 |
| Weighted Fragmented Multiparty | -22.983 | -30.958 | -0.383 | -0.027 | 0.053 | -0.105 | 0.419 |
| Weighted Dominant-Party Legislature | -21.875 | -30.475 | -0.365 | -0.025 | 0.051 | -0.084 | 0.437 |

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
- Roadmap-completion scenarios add district-grounded public signals, refundable proposal bonds, richer cosponsorship diagnostics, multi-round mediation, strategic alternatives, adaptive proposer behavior, strategic lobby-channel learning, challenge allocation/path variants, adaptive-route rates, and proposal-cost variants.
- The next model extension should deepen endogeneity: challengers, amendment coalitions, constituent publics, and alternative drafters should adapt to the institutional rules over repeated sessions.

## Reproduction

```sh
make campaign
```
