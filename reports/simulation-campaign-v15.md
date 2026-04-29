# Simulation Campaign v15

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 18
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.842 productivity, versus 0.265 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.665 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.234 and reduced policy shift by 0.591, while changing productivity by -0.620.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.171, and changed low-support passage by -0.057 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.590, floor consideration by -0.744, and low-support passage by -0.211 relative to open default-pass.
- Adaptive tracks changed productivity by -0.400, low-support passage by -0.185, and policy shift by -0.449 relative to open default-pass.
- Citizen certificate review certified 0.330 of reviewed bills, changed low-support passage by -0.198, and changed legitimacy by 0.161 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.660, and status-quo wins averaged 0.451 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.707.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.173 | 16.893 | 103.333 | 0.666 | 0.000 | 0.077 | 0.594 | 0.052 | 0.226 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.842 | 86.886 | 103.333 | 0.497 | 0.450 | 0.168 | 0.392 | 0.665 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.442 | 44.839 | 95.131 | 0.605 | 0.265 | 0.102 | 0.516 | 0.215 | 0.391 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.901 | 0.000 | 0.926 |
| Default pass + pairwise policy tournament | 0.549 | 56.342 | 56.350 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.202 | 0.000 | 0.000 | 0.549 | 0.000 | 0.941 | 0.000 | 0.549 |
| Default pass + challenge vouchers | 0.671 | 78.000 | 103.333 | 0.510 | 0.394 | 0.161 | 0.401 | 0.456 | 0.541 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.886 | 0.398 | 1.000 |
| Default pass + citizen active-vote routing | 0.446 | 45.579 | 103.333 | 0.618 | 0.249 | 0.100 | 0.551 | 0.254 | 0.471 | 0.220 | 0.000 | 0.000 | 0.000 | 0.000 | 0.954 | 0.000 | 1.000 |
| Default pass + citizen agenda priority | 0.839 | 86.583 | 103.333 | 0.496 | 0.456 | 0.168 | 0.411 | 0.660 | 0.655 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + citizen certificate | 0.448 | 45.763 | 103.333 | 0.617 | 0.253 | 0.100 | 0.552 | 0.256 | 0.473 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.951 | 0.000 | 1.000 |
| Default pass + citizen threshold adjustment | 0.358 | 36.480 | 103.333 | 0.667 | 0.297 | 0.074 | 0.614 | 0.193 | 0.440 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.929 | 0.000 | 1.000 |
| Default pass + compensation amendments | 0.842 | 86.868 | 103.333 | 0.490 | 0.450 | 0.123 | 0.411 | 0.664 | 0.656 | 0.267 | 0.000 | 0.000 | 0.000 | 0.143 | 0.991 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.690 | 24.988 | 0.687 | 0.240 | 0.069 | 0.565 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.803 | 0.000 | 0.256 |
| Default pass + informed guarded committee | 0.222 | 22.173 | 22.310 | 0.651 | 0.216 | 0.087 | 0.551 | 0.074 | 0.250 | 0.227 | 0.000 | 0.000 | 0.000 | 0.000 | 0.574 | 0.000 | 0.223 |
| Default pass + law registry | 0.867 | 89.601 | 103.333 | 0.492 | 0.396 | 0.171 | 0.391 | 0.833 | 0.599 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + channel anti-capture bundle | 0.837 | 86.307 | 103.333 | 0.514 | 0.432 | 0.165 | 0.412 | 0.660 | 0.657 | 0.228 | 0.094 | 0.541 | 0.000 | 0.000 | 0.998 | 0.000 | 1.000 |
| Default pass + public-interest screen | 0.751 | 76.380 | 90.852 | 0.517 | 0.446 | 0.151 | 0.411 | 0.583 | 0.646 | 0.214 | 0.000 | 0.000 | 0.000 | 0.000 | 0.936 | 0.000 | 0.890 |
| Bicameral majority + presidential veto | 0.112 | 10.845 | 103.333 | 0.683 | 0.000 | 0.069 | 0.617 | 0.032 | 0.210 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.297 | 0.000 | 1.000 |
| Unicameral simple majority | 0.265 | 26.289 | 103.333 | 0.637 | 0.000 | 0.090 | 0.554 | 0.101 | 0.305 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.646 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.091 | 8.634 | 103.333 | 0.707 | 0.000 | 0.059 | 0.652 | 0.020 | 0.147 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.252 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.133 | -0.252 | 0.022 | -0.077 | -0.287 | -0.133 | 0.500 |
| Low Polarization | -11.227 | -0.187 | 0.028 | -0.146 | -0.140 | -0.061 | 0.499 |
| High Polarization | -16.927 | -0.282 | 0.018 | -0.039 | -0.355 | -0.164 | 0.500 |
| Low Party Loyalty | -15.587 | -0.260 | 0.026 | -0.090 | -0.302 | -0.136 | 0.499 |
| High Party Loyalty | -15.740 | -0.262 | 0.022 | -0.070 | -0.292 | -0.133 | 0.500 |
| Low Compromise Culture | -16.153 | -0.269 | 0.018 | -0.056 | -0.302 | -0.136 | 0.500 |
| High Compromise Culture | -15.000 | -0.250 | 0.023 | -0.086 | -0.297 | -0.143 | 0.500 |
| Low Lobbying Pressure | -15.873 | -0.265 | 0.024 | -0.070 | -0.317 | -0.151 | 0.500 |
| High Lobbying Pressure | -15.307 | -0.255 | 0.023 | -0.067 | -0.291 | -0.141 | 0.500 |
| Weak Constituency Pressure | -17.887 | -0.298 | 0.025 | -0.074 | -0.319 | -0.135 | 0.500 |
| Two-Party System | -6.600 | -0.110 | -0.002 | -0.030 | -0.145 | -0.081 | 0.333 |
| Multi-Party System | -30.847 | -0.514 | 0.117 | -0.306 | -0.540 | -0.327 | 0.809 |
| High Proposal Pressure | 2.847 | 0.016 | -0.017 | 0.010 | -0.034 | -0.059 | 0.167 |
| Extreme Proposal Pressure | 22.707 | 0.076 | -0.023 | 0.023 | 0.028 | -0.042 | 0.100 |
| Lobby-Fueled Flooding | 3.160 | 0.018 | -0.016 | 0.019 | -0.027 | -0.053 | 0.166 |
| Low-Compromise Flooding | 3.427 | 0.019 | -0.017 | 0.021 | -0.044 | -0.073 | 0.167 |
| Capture Crisis | 1.667 | 0.009 | -0.014 | 0.019 | -0.042 | -0.062 | 0.166 |
| Popular Anti-Lobbying Push | -1.480 | -0.012 | -0.015 | -0.003 | -0.047 | -0.050 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.590 | -0.744 | 0.744 | -0.211 | -0.584 | -0.421 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.400 | -0.074 | 0.073 | 0.001 | -0.185 | -0.449 | -0.265 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.025 | -0.005 | 0.463 | 5.128 | 0.585 | 0.046 | 0.168 |

## Citizen-Panel Deltas

Delta values compare deliberative mini-public review variants against open `default-pass`. Review rate is the share of potential bills reviewed by the synthetic panel; certification rate is the share of reviews receiving a positive certificate.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Legitimacy delta | Review rate | Certification | Citizen legitimacy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + citizen certificate | -0.395 | 0.120 | -0.198 | 0.161 | 1.000 | 0.330 | 0.500 |
| Default pass + citizen active-vote routing | -0.396 | 0.122 | -0.201 | 0.159 | 1.000 | 0.329 | 0.500 |
| Default pass + citizen threshold adjustment | -0.484 | 0.171 | -0.154 | 0.223 | 1.000 | 0.330 | 0.499 |
| Default pass + citizen agenda priority | -0.003 | -0.001 | 0.006 | 0.019 | 1.000 | 0.391 | 0.500 |

## Distributional-Harm Deltas

Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.

| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + compensation amendments | -0.000 | -0.006 | -0.045 | 0.019 | 0.934 | 0.143 | -0.000 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.293 | 0.144 | -0.408 | -0.660 | -0.652 | 0.001 | 0.002 | 6.000 | 0.451 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.626 | 0.166 | -0.257 | -0.598 | -0.415 |
| Low Polarization | -0.406 | 0.089 | -0.220 | -0.260 | -0.121 |
| High Polarization | -0.690 | 0.185 | -0.206 | -0.721 | -0.546 |
| Low Party Loyalty | -0.613 | 0.157 | -0.252 | -0.613 | -0.427 |
| High Party Loyalty | -0.622 | 0.161 | -0.244 | -0.590 | -0.404 |
| Low Compromise Culture | -0.633 | 0.161 | -0.210 | -0.599 | -0.407 |
| High Compromise Culture | -0.611 | 0.162 | -0.258 | -0.606 | -0.425 |
| Low Lobbying Pressure | -0.637 | 0.163 | -0.252 | -0.634 | -0.444 |
| High Lobbying Pressure | -0.625 | 0.141 | -0.239 | -0.589 | -0.403 |
| Weak Constituency Pressure | -0.668 | 0.151 | -0.195 | -0.616 | -0.405 |
| Two-Party System | -0.623 | 0.162 | -0.263 | -0.587 | -0.389 |
| Multi-Party System | -0.627 | 0.165 | -0.261 | -0.607 | -0.418 |
| High Proposal Pressure | -0.626 | 0.163 | -0.254 | -0.610 | -0.426 |
| Extreme Proposal Pressure | -0.618 | 0.158 | -0.255 | -0.597 | -0.413 |
| Lobby-Fueled Flooding | -0.647 | 0.140 | -0.213 | -0.594 | -0.396 |
| Low-Compromise Flooding | -0.669 | 0.179 | -0.191 | -0.673 | -0.496 |
| Capture Crisis | -0.674 | 0.143 | -0.171 | -0.643 | -0.444 |
| Popular Anti-Lobbying Push | -0.547 | 0.134 | -0.270 | -0.504 | -0.341 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.722) | Default pass + law registry (0.868) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.703) | Default pass + law registry (0.872) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.744) | Default pass + law registry (0.865) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass + law registry (0.868) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass + law registry (0.871) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.742) | Default pass + law registry (0.852) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.706) | Default pass + law registry (0.875) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.716) | Default pass + law registry (0.871) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.706) | Default pass + law registry (0.864) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.692) | Default pass + law registry (0.892) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.721) | Default pass + law registry (0.858) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.717) | Default pass + law registry (0.860) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.716) | Default pass + law registry (0.869) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.718) | Default pass + challenge vouchers (0.916) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.710) | Default pass + law registry (0.866) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.739) | Default pass + law registry (0.866) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.739) | Default pass + law registry (0.871) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.690) | Default pass + law registry (0.851) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Citizen-panel scenarios test whether an independent mini-public can add information and legitimacy without reproducing standing committee control.
- The next model extension should add agenda-scarcity variants, because the simulator now has independent review but still needs non-committee ways to ration floor attention and public objection capacity.

## Reproduction

```sh
make campaign
```
