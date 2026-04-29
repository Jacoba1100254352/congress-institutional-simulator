# Simulation Campaign v16

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 19
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.842 productivity, versus 0.265 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.665 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.236 and reduced policy shift by 0.592, while changing productivity by -0.621.
- Challenge vouchers averaged 0.397 challenge use, changed productivity by -0.171, and changed low-support passage by -0.058 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.590, floor consideration by -0.744, and low-support passage by -0.211 relative to open default-pass.
- Adaptive tracks changed productivity by -0.400, low-support passage by -0.185, and policy shift by -0.448 relative to open default-pass.
- Earned proposal credits denied 0.202 of potential proposals, changed welfare by 0.016, and changed proposer gain by -0.034 relative to open default-pass.
- Citizen certificate review certified 0.331 of reviewed bills, changed low-support passage by -0.199, and changed legitimacy by 0.160 relative to open default-pass.
- Weighted agenda lotteries changed floor consideration by -0.535, productivity by -0.436, and welfare by 0.051 relative to open default-pass.
- Quadratic attention budgets spent 3.402 credits per potential bill and changed low-support passage by -0.048 relative to open default-pass.
- Public objection windows triggered on 0.645 of potential bills and changed low-support passage by -0.181 relative to open default-pass.
- Public repeal windows triggered on 0.491 of potential bills; triggered windows reversed 0.558 of those enactments.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.660, and status-quo wins averaged 0.451 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.707.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.932 | 103.333 | 0.666 | 0.000 | 0.077 | 0.594 | 0.053 | 0.227 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.461 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.842 | 86.886 | 103.333 | 0.497 | 0.450 | 0.168 | 0.392 | 0.665 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.443 | 44.843 | 95.137 | 0.605 | 0.265 | 0.102 | 0.515 | 0.216 | 0.393 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.900 | 0.000 | 0.926 |
| Default pass + pairwise policy tournament | 0.549 | 56.338 | 56.349 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.202 | 0.000 | 0.000 | 0.549 | 0.000 | 0.941 | 0.000 | 0.549 |
| Default pass + challenge vouchers | 0.671 | 77.999 | 103.333 | 0.510 | 0.392 | 0.161 | 0.401 | 0.456 | 0.541 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.885 | 0.397 | 1.000 |
| Default pass + citizen certificate | 0.449 | 45.838 | 103.333 | 0.617 | 0.251 | 0.100 | 0.552 | 0.257 | 0.475 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.950 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.680 | 24.983 | 0.687 | 0.239 | 0.069 | 0.565 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.804 | 0.000 | 0.256 |
| Default pass + earned proposal credits | 0.675 | 64.621 | 76.286 | 0.513 | 0.441 | 0.157 | 0.408 | 0.509 | 0.623 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.857 | 0.000 | 0.798 |
| Default pass + informed guarded committee | 0.221 | 21.997 | 22.133 | 0.651 | 0.214 | 0.087 | 0.551 | 0.073 | 0.249 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.575 | 0.000 | 0.222 |
| Default pass + law registry | 0.869 | 89.729 | 103.333 | 0.492 | 0.396 | 0.171 | 0.391 | 0.834 | 0.599 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + public-interest screen | 0.750 | 76.342 | 90.852 | 0.517 | 0.448 | 0.151 | 0.411 | 0.583 | 0.646 | 0.214 | 0.000 | 0.000 | 0.000 | 0.000 | 0.936 | 0.000 | 0.890 |
| Default pass + public objection window | 0.447 | 45.360 | 103.333 | 0.593 | 0.269 | 0.104 | 0.505 | 0.211 | 0.378 | 0.216 | 0.000 | 0.000 | 0.000 | 0.000 | 0.900 | 0.000 | 1.000 |
| Default pass + quadratic attention budget | 0.443 | 41.819 | 52.177 | 0.575 | 0.402 | 0.110 | 0.479 | 0.197 | 0.344 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.840 | 0.000 | 0.552 |
| Default pass + random agenda lottery | 0.352 | 36.446 | 43.333 | 0.497 | 0.455 | 0.168 | 0.392 | 0.275 | 0.651 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.418 | 0.000 | 0.418 |
| Default pass + public repeal window | 0.535 | 54.382 | 103.333 | 0.572 | 0.370 | 0.115 | 0.479 | 0.279 | 0.420 | 0.222 | 0.000 | 0.000 | 0.000 | 0.000 | 0.950 | 0.000 | 1.000 |
| Default pass + weighted agenda lottery | 0.407 | 41.815 | 47.833 | 0.548 | 0.421 | 0.137 | 0.445 | 0.296 | 0.602 | 0.232 | 0.000 | 0.000 | 0.000 | 0.000 | 0.635 | 0.000 | 0.465 |
| Bicameral majority + presidential veto | 0.113 | 10.944 | 103.333 | 0.680 | 0.000 | 0.069 | 0.616 | 0.031 | 0.208 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.301 | 0.000 | 1.000 |
| Unicameral simple majority | 0.265 | 26.289 | 103.333 | 0.637 | 0.000 | 0.090 | 0.554 | 0.101 | 0.305 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.646 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.091 | 8.634 | 103.333 | 0.707 | 0.000 | 0.059 | 0.652 | 0.020 | 0.147 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.252 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.320 | -0.255 | 0.021 | -0.076 | -0.286 | -0.129 | 0.500 |
| Low Polarization | -11.260 | -0.188 | 0.028 | -0.146 | -0.142 | -0.064 | 0.499 |
| High Polarization | -16.927 | -0.282 | 0.017 | -0.042 | -0.354 | -0.161 | 0.500 |
| Low Party Loyalty | -15.547 | -0.259 | 0.026 | -0.092 | -0.304 | -0.139 | 0.499 |
| High Party Loyalty | -15.673 | -0.261 | 0.021 | -0.079 | -0.290 | -0.129 | 0.500 |
| Low Compromise Culture | -16.207 | -0.270 | 0.017 | -0.054 | -0.303 | -0.138 | 0.500 |
| High Compromise Culture | -14.987 | -0.250 | 0.024 | -0.088 | -0.297 | -0.143 | 0.500 |
| Low Lobbying Pressure | -16.060 | -0.268 | 0.023 | -0.071 | -0.318 | -0.149 | 0.500 |
| High Lobbying Pressure | -15.327 | -0.255 | 0.021 | -0.065 | -0.287 | -0.133 | 0.500 |
| Weak Constituency Pressure | -17.760 | -0.296 | 0.024 | -0.081 | -0.318 | -0.135 | 0.500 |
| Two-Party System | -6.620 | -0.110 | -0.003 | -0.035 | -0.145 | -0.080 | 0.333 |
| Multi-Party System | -30.800 | -0.513 | 0.114 | -0.304 | -0.542 | -0.335 | 0.807 |
| High Proposal Pressure | 3.007 | 0.017 | -0.016 | 0.010 | -0.034 | -0.060 | 0.167 |
| Extreme Proposal Pressure | 22.740 | 0.076 | -0.023 | 0.022 | 0.028 | -0.042 | 0.100 |
| Lobby-Fueled Flooding | 3.093 | 0.017 | -0.016 | 0.016 | -0.028 | -0.053 | 0.166 |
| Low-Compromise Flooding | 3.573 | 0.020 | -0.017 | 0.021 | -0.044 | -0.073 | 0.167 |
| Capture Crisis | 1.480 | 0.008 | -0.014 | 0.017 | -0.042 | -0.061 | 0.166 |
| Popular Anti-Lobbying Push | -1.380 | -0.011 | -0.015 | -0.003 | -0.047 | -0.050 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.590 | -0.744 | 0.744 | -0.211 | -0.584 | -0.421 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.400 | -0.074 | 0.073 | 0.001 | -0.185 | -0.448 | -0.263 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.463 | 5.127 | 0.585 | 0.045 | 0.170 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.167 | -0.202 | 0.202 | 0.016 | -0.009 | -0.156 | -0.034 | 0.000 |

## Citizen-Panel Deltas

Delta values compare deliberative mini-public review variants against open `default-pass`. Review rate is the share of potential bills reviewed by the synthetic panel; certification rate is the share of reviews receiving a positive certificate.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Legitimacy delta | Review rate | Certification | Citizen legitimacy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + citizen certificate | -0.394 | 0.120 | -0.199 | 0.160 | 1.000 | 0.331 | 0.500 |

## Agenda-Scarcity Deltas

Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + weighted agenda lottery | -0.436 | -0.535 | 0.535 | 0.051 | -0.029 | 0.000 | 0.000 | 0.000 |
| Default pass + random agenda lottery | -0.491 | -0.582 | 0.582 | 0.000 | 0.004 | 0.000 | 0.000 | 0.000 |
| Default pass + quadratic attention budget | -0.399 | -0.448 | 0.448 | 0.078 | -0.048 | 3.402 | 0.000 | 0.000 |
| Default pass + public objection window | -0.395 | 0.000 | 0.000 | 0.097 | -0.181 | 0.000 | 0.645 | 0.000 |
| Default pass + public repeal window | -0.308 | 0.000 | 0.000 | 0.075 | -0.081 | 0.000 | 0.491 | 0.558 |
| Default pass + earned proposal credits | -0.167 | -0.202 | 0.202 | 0.016 | -0.009 | 0.000 | 0.000 | 0.000 |
| Default pass + challenge vouchers | -0.171 | 0.000 | 0.000 | 0.013 | -0.058 | 0.000 | 0.000 | 0.000 |
| Default pass + informed guarded committee | -0.621 | -0.778 | 0.538 | 0.155 | -0.236 | 0.000 | 0.000 | 0.000 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.293 | 0.144 | -0.409 | -0.660 | -0.652 | 0.001 | 0.002 | 6.000 | 0.451 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.617 | 0.162 | -0.240 | -0.595 | -0.412 |
| Low Polarization | -0.409 | 0.088 | -0.228 | -0.261 | -0.122 |
| High Polarization | -0.689 | 0.194 | -0.202 | -0.720 | -0.552 |
| Low Party Loyalty | -0.624 | 0.159 | -0.250 | -0.617 | -0.429 |
| High Party Loyalty | -0.620 | 0.159 | -0.266 | -0.590 | -0.408 |
| Low Compromise Culture | -0.632 | 0.163 | -0.223 | -0.600 | -0.409 |
| High Compromise Culture | -0.608 | 0.157 | -0.275 | -0.606 | -0.428 |
| Low Lobbying Pressure | -0.635 | 0.161 | -0.257 | -0.632 | -0.443 |
| High Lobbying Pressure | -0.632 | 0.144 | -0.232 | -0.590 | -0.393 |
| Weak Constituency Pressure | -0.667 | 0.156 | -0.199 | -0.614 | -0.398 |
| Two-Party System | -0.623 | 0.160 | -0.255 | -0.589 | -0.403 |
| Multi-Party System | -0.627 | 0.169 | -0.265 | -0.606 | -0.412 |
| High Proposal Pressure | -0.628 | 0.166 | -0.264 | -0.611 | -0.425 |
| Extreme Proposal Pressure | -0.620 | 0.159 | -0.251 | -0.599 | -0.416 |
| Lobby-Fueled Flooding | -0.644 | 0.136 | -0.211 | -0.594 | -0.404 |
| Low-Compromise Flooding | -0.674 | 0.176 | -0.188 | -0.675 | -0.498 |
| Capture Crisis | -0.681 | 0.142 | -0.175 | -0.646 | -0.449 |
| Popular Anti-Lobbying Push | -0.552 | 0.134 | -0.275 | -0.504 | -0.330 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.722) | Default pass + law registry (0.870) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.703) | Default pass + law registry (0.872) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.744) | Default pass + law registry (0.866) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass + law registry (0.873) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass + law registry (0.869) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.742) | Default pass + law registry (0.852) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.706) | Default pass + law registry (0.876) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.716) | Default pass + law registry (0.873) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.706) | Default pass + law registry (0.863) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.692) | Default pass + law registry (0.899) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.721) | Default pass + law registry (0.862) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.717) | Default pass + law registry (0.864) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.716) | Default pass + law registry (0.869) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.718) | Default pass + challenge vouchers (0.917) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.711) | Default pass + law registry (0.867) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.739) | Default pass + law registry (0.863) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.739) | Default pass + law registry (0.875) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.690) | Default pass + law registry (0.852) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Agenda-scarcity variants test non-committee ways to ration floor attention, including weighted/random lotteries, quadratic credits, and public objection or repeal windows.
- The next model extension should add richer constituent and affected-group structure so public objection and citizen-panel signals are grounded in represented districts rather than generated bill fields.

## Reproduction

```sh
make campaign
```
