# Simulation Campaign v12

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 18
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.842 productivity, versus 0.264 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.664 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.232 and reduced policy shift by 0.591, while changing productivity by -0.619.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.172, and changed low-support passage by -0.057 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.588, floor consideration by -0.743, and low-support passage by -0.211 relative to open default-pass.
- Adaptive tracks changed productivity by -0.400, low-support passage by -0.185, and policy shift by -0.448 relative to open default-pass.
- Sunset trial review changed productivity by -0.372, welfare by 0.122, and policy shift by -0.399 relative to open default-pass.
- Earned proposal credits denied 0.202 of potential proposals, changed welfare by 0.016, and changed proposer gain by -0.030 relative to open default-pass.
- Mediated default-pass amended 0.827 of potential bills and changed compromise by 0.027 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.709.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.907 | 103.333 | 0.668 | 0.000 | 0.076 | 0.596 | 0.052 | 0.226 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.842 | 86.863 | 103.333 | 0.496 | 0.450 | 0.168 | 0.392 | 0.664 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.442 | 44.761 | 95.088 | 0.606 | 0.264 | 0.102 | 0.516 | 0.216 | 0.393 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.906 | 0.000 | 0.926 |
| Default pass + affected-group consent | 0.769 | 78.959 | 92.343 | 0.509 | 0.439 | 0.122 | 0.427 | 0.583 | 0.632 | 0.250 | 0.000 | 0.000 | 0.000 | 0.152 | 0.992 | 0.000 | 0.897 |
| Default pass + challenge vouchers | 0.670 | 77.926 | 103.333 | 0.510 | 0.393 | 0.161 | 0.402 | 0.455 | 0.539 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.884 | 0.398 | 1.000 |
| Default pass + compensation amendments | 0.841 | 86.786 | 103.333 | 0.490 | 0.451 | 0.123 | 0.411 | 0.663 | 0.655 | 0.267 | 0.000 | 0.000 | 0.000 | 0.142 | 0.992 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.756 | 25.050 | 0.687 | 0.239 | 0.069 | 0.566 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.806 | 0.000 | 0.257 |
| Default pass + earned proposal credits | 0.676 | 64.706 | 76.326 | 0.512 | 0.442 | 0.157 | 0.408 | 0.511 | 0.625 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.857 | 0.000 | 0.798 |
| Default pass + harm-weighted threshold | 0.768 | 78.956 | 103.333 | 0.507 | 0.442 | 0.144 | 0.408 | 0.580 | 0.629 | 0.251 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + informed guarded committee | 0.223 | 22.114 | 22.265 | 0.651 | 0.217 | 0.087 | 0.551 | 0.073 | 0.249 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.578 | 0.000 | 0.224 |
| Default pass + law registry | 0.868 | 89.680 | 103.333 | 0.491 | 0.397 | 0.171 | 0.391 | 0.835 | 0.599 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + law registry + challenge | 0.677 | 78.449 | 103.333 | 0.509 | 0.361 | 0.161 | 0.404 | 0.533 | 0.494 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.891 | 0.397 | 1.000 |
| Default pass + mediated amendments | 0.897 | 92.296 | 103.333 | 0.491 | 0.459 | 0.132 | 0.403 | 0.499 | 0.508 | 0.269 | 0.000 | 0.000 | 0.827 | 0.151 | 0.991 | 0.000 | 1.000 |
| Default pass + sunset trial + challenge | 0.398 | 43.528 | 103.333 | 0.622 | 0.317 | 0.096 | 0.524 | 0.198 | 0.394 | 0.172 | 0.000 | 0.000 | 0.000 | 0.000 | 0.871 | 0.398 | 1.000 |
| Default pass + sunset trial | 0.470 | 47.618 | 103.333 | 0.618 | 0.373 | 0.098 | 0.523 | 0.265 | 0.460 | 0.174 | 0.000 | 0.000 | 0.000 | 0.000 | 0.970 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.113 | 10.907 | 103.333 | 0.683 | 0.000 | 0.068 | 0.619 | 0.032 | 0.208 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.304 | 0.000 | 1.000 |
| Unicameral simple majority | 0.264 | 26.217 | 103.333 | 0.637 | 0.000 | 0.090 | 0.555 | 0.101 | 0.304 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.092 | 8.659 | 103.333 | 0.709 | 0.000 | 0.058 | 0.656 | 0.020 | 0.148 | 0.247 | 0.000 | 0.000 | 0.000 | 0.000 | 0.257 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.893 | -0.265 | 0.025 | -0.077 | -0.298 | -0.138 | 0.500 |
| Low Polarization | -11.207 | -0.187 | 0.030 | -0.143 | -0.143 | -0.064 | 0.499 |
| High Polarization | -17.113 | -0.285 | 0.019 | -0.039 | -0.365 | -0.175 | 0.500 |
| Low Party Loyalty | -15.240 | -0.254 | 0.025 | -0.087 | -0.298 | -0.139 | 0.499 |
| High Party Loyalty | -15.680 | -0.261 | 0.024 | -0.077 | -0.296 | -0.140 | 0.500 |
| Low Compromise Culture | -15.547 | -0.259 | 0.020 | -0.060 | -0.291 | -0.134 | 0.500 |
| High Compromise Culture | -15.387 | -0.256 | 0.023 | -0.086 | -0.293 | -0.136 | 0.500 |
| Low Lobbying Pressure | -15.760 | -0.263 | 0.023 | -0.076 | -0.312 | -0.154 | 0.500 |
| High Lobbying Pressure | -15.707 | -0.262 | 0.020 | -0.062 | -0.290 | -0.130 | 0.500 |
| Weak Constituency Pressure | -17.987 | -0.300 | 0.021 | -0.075 | -0.316 | -0.133 | 0.500 |
| Two-Party System | -6.273 | -0.105 | -0.005 | -0.025 | -0.142 | -0.082 | 0.333 |
| Multi-Party System | -31.267 | -0.521 | 0.123 | -0.303 | -0.548 | -0.335 | 0.810 |
| High Proposal Pressure | 3.233 | 0.018 | -0.017 | 0.008 | -0.032 | -0.057 | 0.167 |
| Extreme Proposal Pressure | 22.327 | 0.074 | -0.022 | 0.022 | 0.025 | -0.045 | 0.100 |
| Lobby-Fueled Flooding | 3.613 | 0.020 | -0.016 | 0.012 | -0.024 | -0.053 | 0.166 |
| Low-Compromise Flooding | 3.680 | 0.020 | -0.019 | 0.022 | -0.046 | -0.078 | 0.167 |
| Capture Crisis | 1.360 | 0.008 | -0.015 | 0.017 | -0.044 | -0.063 | 0.166 |
| Popular Anti-Lobbying Push | -2.013 | -0.017 | -0.014 | -0.000 | -0.051 | -0.051 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.588 | -0.743 | 0.743 | -0.211 | -0.584 | -0.421 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.400 | -0.074 | 0.073 | 0.001 | -0.185 | -0.448 | -0.263 | 0.000 |

## Sunset Trial Deltas

Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + sunset trial | -0.372 | 0.122 | -0.077 | -0.399 | -0.196 | 0.000 |
| Default pass + sunset trial + challenge | -0.444 | 0.125 | -0.133 | -0.466 | -0.262 | 0.398 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.027 | -0.005 | 0.459 | 5.129 | 0.585 | 0.048 | 0.171 |
| Default pass + law registry + challenge | -0.165 | 0.013 | 0.507 | 5.138 | 0.550 | 0.050 | -0.131 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.166 | -0.202 | 0.202 | 0.016 | -0.007 | -0.153 | -0.030 | 0.000 |

## Mediation Deltas

Delta values compare structured amendment mediation against the matching non-mediated scenario. Amendment rate is the share of potential bills whose policy position moved before final voting.

| Scenario | Baseline | Productivity delta | Welfare delta | Compromise delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Amendment rate | Amendment movement |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + mediated amendments | Default pass unless 2/3 block | 0.055 | -0.005 | 0.027 | 0.010 | -0.165 | -0.148 | 0.827 | 0.162 |

## Distributional-Harm Deltas

Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.

| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + harm-weighted threshold | -0.074 | 0.011 | -0.024 | 0.016 | 0.282 | 0.000 | -0.007 |
| Default pass + compensation amendments | -0.001 | -0.006 | -0.045 | 0.019 | 0.939 | 0.142 | 0.001 |
| Default pass + affected-group consent | -0.073 | 0.013 | -0.046 | 0.035 | 0.945 | 0.152 | -0.010 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.630 | 0.161 | -0.257 | -0.600 | -0.415 |
| Low Polarization | -0.407 | 0.089 | -0.218 | -0.261 | -0.126 |
| High Polarization | -0.688 | 0.188 | -0.209 | -0.723 | -0.550 |
| Low Party Loyalty | -0.607 | 0.158 | -0.266 | -0.605 | -0.419 |
| High Party Loyalty | -0.626 | 0.171 | -0.254 | -0.606 | -0.427 |
| Low Compromise Culture | -0.622 | 0.162 | -0.227 | -0.598 | -0.422 |
| High Compromise Culture | -0.608 | 0.155 | -0.253 | -0.597 | -0.409 |
| Low Lobbying Pressure | -0.621 | 0.161 | -0.256 | -0.615 | -0.436 |
| High Lobbying Pressure | -0.632 | 0.145 | -0.204 | -0.583 | -0.386 |
| Weak Constituency Pressure | -0.669 | 0.152 | -0.192 | -0.610 | -0.393 |
| Two-Party System | -0.616 | 0.164 | -0.263 | -0.593 | -0.409 |
| Multi-Party System | -0.624 | 0.168 | -0.240 | -0.607 | -0.408 |
| High Proposal Pressure | -0.629 | 0.162 | -0.250 | -0.609 | -0.421 |
| Extreme Proposal Pressure | -0.620 | 0.159 | -0.251 | -0.603 | -0.421 |
| Lobby-Fueled Flooding | -0.647 | 0.137 | -0.217 | -0.591 | -0.397 |
| Low-Compromise Flooding | -0.671 | 0.175 | -0.189 | -0.673 | -0.499 |
| Capture Crisis | -0.679 | 0.143 | -0.176 | -0.649 | -0.453 |
| Popular Anti-Lobbying Push | -0.548 | 0.134 | -0.261 | -0.507 | -0.338 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.720) | Default pass + mediated amendments (0.899) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.703) | Default pass + mediated amendments (0.938) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.736) | Default pass + mediated amendments (0.881) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.725) | Default pass + mediated amendments (0.908) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass + mediated amendments (0.895) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.730) | Default pass + mediated amendments (0.869) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.699) | Default pass + mediated amendments (0.921) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.727) | Default pass + mediated amendments (0.901) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.705) | Default pass + mediated amendments (0.884) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.700) | Default pass + mediated amendments (0.940) | Unicameral simple majority (0.000) |
| Two-Party System | Unicameral 60 percent passage (0.726) | Default pass + mediated amendments (0.895) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.722) | Default pass + mediated amendments (0.908) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.718) | Default pass + mediated amendments (0.895) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.714) | Default pass + law registry + challenge (0.918) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.711) | Default pass + mediated amendments (0.890) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.735) | Default pass + mediated amendments (0.867) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.741) | Default pass + mediated amendments (0.884) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.692) | Default pass + mediated amendments (0.881) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Structured mediation scenarios let a bounded amendment stage move bills toward the chamber median/status quo before the final yes/no vote.
- The next model extension should add richer constituent and affected-group structure, because compromise quality should be judged against public will and concentrated harms rather than only chamber support.

## Reproduction

```sh
make campaign
```
