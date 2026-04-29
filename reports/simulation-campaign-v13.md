# Simulation Campaign v13

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 21
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.841 productivity, versus 0.264 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.663 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.234 and reduced policy shift by 0.589, while changing productivity by -0.618.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.171, and changed low-support passage by -0.057 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.588, floor consideration by -0.744, and low-support passage by -0.210 relative to open default-pass.
- Adaptive tracks changed productivity by -0.399, low-support passage by -0.186, and policy shift by -0.447 relative to open default-pass.
- Earned proposal credits denied 0.202 of potential proposals, changed welfare by 0.016, and changed proposer gain by -0.031 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.659, and status-quo wins averaged 0.450 relative to open default-pass.
- Mediated default-pass amended 0.827 of potential bills and changed compromise by 0.028 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.708.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.888 | 103.333 | 0.667 | 0.000 | 0.076 | 0.595 | 0.052 | 0.224 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.841 | 86.853 | 103.333 | 0.497 | 0.450 | 0.168 | 0.392 | 0.663 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.442 | 44.807 | 95.078 | 0.606 | 0.264 | 0.102 | 0.516 | 0.216 | 0.394 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.904 | 0.000 | 0.926 |
| Default pass + affected-group consent | 0.768 | 78.957 | 92.343 | 0.509 | 0.438 | 0.122 | 0.427 | 0.582 | 0.631 | 0.250 | 0.000 | 0.000 | 0.000 | 0.152 | 0.992 | 0.000 | 0.897 |
| Default pass + public-benefit alternatives | 0.943 | 97.151 | 98.289 | 0.551 | 0.196 | 0.078 | 0.513 | 0.007 | 0.005 | 0.242 | 0.000 | 0.000 | 0.946 | 0.000 | 0.999 | 0.000 | 0.952 |
| Default pass + median-seeking alternatives | 0.943 | 97.161 | 98.294 | 0.551 | 0.195 | 0.078 | 0.513 | 0.004 | 0.002 | 0.242 | 0.000 | 0.000 | 0.953 | 0.000 | 0.999 | 0.000 | 0.953 |
| Default pass + pairwise policy tournament | 0.550 | 56.394 | 56.404 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.203 | 0.000 | 0.000 | 0.550 | 0.000 | 0.945 | 0.000 | 0.550 |
| Default pass + public-support alternatives | 0.854 | 87.869 | 98.105 | 0.489 | 0.346 | 0.082 | 0.528 | 0.462 | 0.160 | 0.251 | 0.000 | 0.000 | 0.918 | 0.000 | 0.965 | 0.000 | 0.950 |
| Default pass + challenge vouchers | 0.670 | 77.929 | 103.333 | 0.510 | 0.393 | 0.161 | 0.402 | 0.455 | 0.538 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.885 | 0.398 | 1.000 |
| Default pass + compensation amendments | 0.842 | 86.824 | 103.333 | 0.490 | 0.449 | 0.123 | 0.411 | 0.663 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.142 | 0.992 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.754 | 25.045 | 0.687 | 0.240 | 0.069 | 0.566 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.806 | 0.000 | 0.256 |
| Default pass + earned proposal credits | 0.676 | 64.694 | 76.341 | 0.513 | 0.441 | 0.157 | 0.408 | 0.510 | 0.625 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.857 | 0.000 | 0.798 |
| Default pass + harm-weighted threshold | 0.768 | 78.906 | 103.333 | 0.507 | 0.444 | 0.144 | 0.408 | 0.580 | 0.629 | 0.251 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.000 | 1.000 |
| Default pass + informed guarded committee | 0.223 | 22.198 | 22.334 | 0.651 | 0.216 | 0.088 | 0.551 | 0.074 | 0.251 | 0.228 | 0.000 | 0.000 | 0.000 | 0.000 | 0.580 | 0.000 | 0.225 |
| Default pass + law registry | 0.867 | 89.565 | 103.333 | 0.491 | 0.398 | 0.171 | 0.391 | 0.835 | 0.599 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + mediated amendments | 0.896 | 92.230 | 103.333 | 0.492 | 0.458 | 0.132 | 0.404 | 0.498 | 0.508 | 0.269 | 0.000 | 0.000 | 0.827 | 0.151 | 0.993 | 0.000 | 1.000 |
| Default pass + obstruction-with-substitute | 0.550 | 56.352 | 56.361 | 0.643 | 0.043 | 0.046 | 0.644 | 0.004 | 0.003 | 0.202 | 0.000 | 0.000 | 0.550 | 0.000 | 0.944 | 0.000 | 0.550 |
| Bicameral majority + presidential veto | 0.113 | 10.942 | 103.333 | 0.684 | 0.000 | 0.069 | 0.619 | 0.031 | 0.207 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.307 | 0.000 | 1.000 |
| Unicameral simple majority | 0.264 | 26.217 | 103.333 | 0.637 | 0.000 | 0.090 | 0.555 | 0.101 | 0.304 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.528 | 53.328 | 56.506 | 0.641 | 0.000 | 0.046 | 0.650 | 0.004 | 0.004 | 0.209 | 0.000 | 0.000 | 0.552 | 0.000 | 0.884 | 0.000 | 0.552 |
| Unicameral 60 percent passage | 0.091 | 8.624 | 103.333 | 0.708 | 0.000 | 0.058 | 0.655 | 0.020 | 0.146 | 0.248 | 0.000 | 0.000 | 0.000 | 0.000 | 0.257 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.833 | -0.264 | 0.025 | -0.087 | -0.296 | -0.138 | 0.500 |
| Low Polarization | -11.160 | -0.186 | 0.029 | -0.137 | -0.146 | -0.069 | 0.499 |
| High Polarization | -16.907 | -0.282 | 0.018 | -0.040 | -0.360 | -0.171 | 0.500 |
| Low Party Loyalty | -15.220 | -0.254 | 0.025 | -0.089 | -0.298 | -0.140 | 0.499 |
| High Party Loyalty | -15.853 | -0.264 | 0.024 | -0.070 | -0.301 | -0.140 | 0.500 |
| Low Compromise Culture | -15.360 | -0.256 | 0.020 | -0.069 | -0.283 | -0.128 | 0.500 |
| High Compromise Culture | -15.027 | -0.250 | 0.023 | -0.089 | -0.287 | -0.135 | 0.500 |
| Low Lobbying Pressure | -15.973 | -0.266 | 0.024 | -0.073 | -0.313 | -0.152 | 0.500 |
| High Lobbying Pressure | -15.380 | -0.256 | 0.020 | -0.062 | -0.287 | -0.132 | 0.500 |
| Weak Constituency Pressure | -17.707 | -0.295 | 0.022 | -0.071 | -0.316 | -0.135 | 0.500 |
| Two-Party System | -6.047 | -0.101 | -0.004 | -0.017 | -0.137 | -0.079 | 0.333 |
| Multi-Party System | -31.247 | -0.521 | 0.124 | -0.302 | -0.550 | -0.345 | 0.810 |
| High Proposal Pressure | 3.360 | 0.019 | -0.017 | 0.013 | -0.032 | -0.058 | 0.167 |
| Extreme Proposal Pressure | 22.620 | 0.075 | -0.022 | 0.023 | 0.025 | -0.045 | 0.100 |
| Lobby-Fueled Flooding | 2.953 | 0.016 | -0.016 | 0.009 | -0.027 | -0.052 | 0.166 |
| Low-Compromise Flooding | 3.253 | 0.018 | -0.019 | 0.023 | -0.047 | -0.077 | 0.167 |
| Capture Crisis | 1.220 | 0.007 | -0.014 | 0.014 | -0.046 | -0.065 | 0.166 |
| Popular Anti-Lobbying Push | -2.333 | -0.019 | -0.013 | -0.005 | -0.053 | -0.051 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.588 | -0.744 | 0.744 | -0.210 | -0.583 | -0.421 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.399 | -0.074 | 0.073 | 0.001 | -0.186 | -0.447 | -0.262 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.459 | 5.127 | 0.585 | 0.048 | 0.171 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.165 | -0.202 | 0.202 | 0.016 | -0.009 | -0.153 | -0.031 | 0.000 |

## Mediation Deltas

Delta values compare structured amendment mediation against the matching non-mediated scenario. Amendment rate is the share of potential bills whose policy position moved before final voting.

| Scenario | Baseline | Productivity delta | Welfare delta | Compromise delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Amendment rate | Amendment movement |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + mediated amendments | Default pass unless 2/3 block | 0.055 | -0.005 | 0.028 | 0.008 | -0.165 | -0.148 | 0.827 | 0.162 |

## Distributional-Harm Deltas

Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.

| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + harm-weighted threshold | -0.073 | 0.010 | -0.024 | 0.015 | 0.280 | 0.000 | -0.006 |
| Default pass + compensation amendments | 0.000 | -0.007 | -0.045 | 0.019 | 0.934 | 0.142 | -0.001 |
| Default pass + affected-group consent | -0.073 | 0.013 | -0.046 | 0.035 | 0.945 | 0.152 | -0.012 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Unicameral majority + pairwise alternatives | -0.314 | 0.145 | -0.450 | -0.659 | -0.652 | 0.001 | 0.003 | 6.000 | 0.448 |
| Default pass + public-benefit alternatives | 0.102 | 0.055 | -0.254 | -0.656 | -0.651 | 0.003 | 0.005 | 6.000 | 0.048 |
| Default pass + public-support alternatives | 0.013 | -0.007 | -0.105 | -0.201 | -0.496 | 0.409 | 0.138 | 6.000 | 0.050 |
| Default pass + median-seeking alternatives | 0.102 | 0.055 | -0.255 | -0.660 | -0.654 | 0.000 | 0.002 | 6.000 | 0.047 |
| Default pass + pairwise policy tournament | -0.291 | 0.144 | -0.409 | -0.659 | -0.652 | 0.001 | 0.002 | 6.000 | 0.450 |
| Default pass + obstruction-with-substitute | -0.291 | 0.147 | -0.408 | -0.660 | -0.652 | 0.000 | 0.002 | 5.000 | 0.450 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.619 | 0.160 | -0.262 | -0.592 | -0.405 |
| Low Polarization | -0.398 | 0.088 | -0.203 | -0.258 | -0.123 |
| High Polarization | -0.682 | 0.183 | -0.206 | -0.721 | -0.545 |
| Low Party Loyalty | -0.608 | 0.160 | -0.276 | -0.604 | -0.419 |
| High Party Loyalty | -0.624 | 0.167 | -0.255 | -0.607 | -0.425 |
| Low Compromise Culture | -0.623 | 0.160 | -0.224 | -0.592 | -0.417 |
| High Compromise Culture | -0.610 | 0.155 | -0.264 | -0.594 | -0.410 |
| Low Lobbying Pressure | -0.623 | 0.166 | -0.254 | -0.613 | -0.424 |
| High Lobbying Pressure | -0.628 | 0.139 | -0.219 | -0.583 | -0.389 |
| Weak Constituency Pressure | -0.668 | 0.152 | -0.217 | -0.612 | -0.397 |
| Two-Party System | -0.621 | 0.169 | -0.248 | -0.596 | -0.409 |
| Multi-Party System | -0.619 | 0.162 | -0.243 | -0.603 | -0.409 |
| High Proposal Pressure | -0.626 | 0.163 | -0.250 | -0.608 | -0.423 |
| Extreme Proposal Pressure | -0.621 | 0.159 | -0.250 | -0.601 | -0.417 |
| Lobby-Fueled Flooding | -0.641 | 0.137 | -0.208 | -0.590 | -0.393 |
| Low-Compromise Flooding | -0.674 | 0.175 | -0.188 | -0.674 | -0.496 |
| Capture Crisis | -0.679 | 0.145 | -0.178 | -0.650 | -0.444 |
| Popular Anti-Lobbying Push | -0.554 | 0.134 | -0.264 | -0.510 | -0.341 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.725) | Default pass + public-benefit alternatives (0.947) | Unicameral simple majority (0.000) |
| Low Polarization | Default pass + obstruction-with-substitute (0.709) | Default pass + public-benefit alternatives (0.976) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.738) | Default pass + public-benefit alternatives (0.935) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.721) | Default pass + public-benefit alternatives (0.950) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.713) | Default pass + median-seeking alternatives (0.946) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.731) | Default pass + median-seeking alternatives (0.939) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.696) | Default pass + public-benefit alternatives (0.954) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.724) | Default pass + public-benefit alternatives (0.954) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.705) | Default pass + median-seeking alternatives (0.926) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.699) | Default pass + public-benefit alternatives (0.954) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.725) | Default pass + median-seeking alternatives (0.947) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.721) | Default pass + public-benefit alternatives (0.947) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.721) | Default pass + public-benefit alternatives (0.947) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.714) | Default pass + median-seeking alternatives (0.950) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.711) | Default pass + public-benefit alternatives (0.929) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.737) | Default pass + median-seeking alternatives (0.930) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.740) | Default pass + median-seeking alternatives (0.918) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.692) | Default pass + public-benefit alternatives (0.931) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Policy-tournament scenarios test whether agenda-setter power falls when multiple alternatives compete before a final yes/no ratification vote.
- The next model extension should add deliberative citizen review or richer lobbying channels, because the simulator now has agenda competition, harm guardrails, law review, and mediation but still lacks an independent public legitimacy screen.

## Reproduction

```sh
make campaign
```
