# Simulation Campaign v11

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 19
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.841 productivity, versus 0.264 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.663 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.233 and reduced policy shift by 0.590, while changing productivity by -0.619.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.171, and changed low-support passage by -0.058 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.588, floor consideration by -0.743, and low-support passage by -0.211 relative to open default-pass.
- Adaptive tracks changed productivity by -0.399, low-support passage by -0.186, and policy shift by -0.447 relative to open default-pass.
- Sunset trial review changed productivity by -0.372, welfare by 0.122, and policy shift by -0.398 relative to open default-pass.
- Earned proposal credits denied 0.202 of potential proposals, changed welfare by 0.016, and changed proposer gain by -0.031 relative to open default-pass.
- The anti-capture bundle changed lobby capture by -0.090, anti-lobbying reform passage by -0.034, and private-gain ratio by -0.193 relative to open default-pass.
- Budgeted lobbying spent 0.099 per potential bill, with 0.655 of spend aimed defensively at anti-lobbying reform bills.
- Mediated default-pass amended 0.827 of potential bills and changed compromise by 0.028 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.708.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.941 | 103.333 | 0.668 | 0.000 | 0.076 | 0.596 | 0.053 | 0.229 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.469 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.841 | 86.853 | 103.333 | 0.497 | 0.450 | 0.168 | 0.392 | 0.663 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.442 | 44.761 | 95.088 | 0.606 | 0.264 | 0.102 | 0.516 | 0.216 | 0.393 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.906 | 0.000 | 0.926 |
| Default pass + affected-group consent | 0.768 | 78.957 | 92.343 | 0.509 | 0.438 | 0.122 | 0.427 | 0.582 | 0.631 | 0.250 | 0.000 | 0.000 | 0.000 | 0.152 | 0.992 | 0.000 | 0.897 |
| Default pass + anti-capture bundle | 0.749 | 76.585 | 97.841 | 0.519 | 0.444 | 0.151 | 0.410 | 0.585 | 0.650 | 0.176 | 0.000 | 0.000 | 0.000 | 0.000 | 0.959 | 0.000 | 0.952 |
| Default pass + budgeted lobbying | 0.842 | 86.859 | 103.333 | 0.496 | 0.452 | 0.168 | 0.391 | 0.664 | 0.656 | 0.268 | 0.099 | 0.655 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Default pass + budgeted lobbying + mediation | 0.897 | 92.293 | 103.333 | 0.491 | 0.461 | 0.132 | 0.402 | 0.498 | 0.508 | 0.271 | 0.099 | 0.655 | 0.829 | 0.151 | 0.989 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.670 | 77.926 | 103.333 | 0.510 | 0.393 | 0.161 | 0.402 | 0.455 | 0.539 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.884 | 0.398 | 1.000 |
| Default pass + compensation amendments | 0.842 | 86.824 | 103.333 | 0.490 | 0.449 | 0.123 | 0.411 | 0.663 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.142 | 0.992 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.756 | 25.050 | 0.687 | 0.239 | 0.069 | 0.566 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.806 | 0.000 | 0.257 |
| Default pass + earned proposal credits | 0.676 | 64.683 | 76.317 | 0.512 | 0.442 | 0.157 | 0.408 | 0.510 | 0.625 | 0.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.856 | 0.000 | 0.798 |
| Default pass + harm-weighted threshold | 0.768 | 78.906 | 103.333 | 0.507 | 0.444 | 0.144 | 0.408 | 0.580 | 0.629 | 0.251 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.000 | 1.000 |
| Default pass + informed guarded committee | 0.223 | 22.114 | 22.265 | 0.651 | 0.217 | 0.087 | 0.551 | 0.073 | 0.249 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.578 | 0.000 | 0.224 |
| Default pass + mediated amendments | 0.896 | 92.230 | 103.333 | 0.492 | 0.458 | 0.132 | 0.404 | 0.498 | 0.508 | 0.269 | 0.000 | 0.000 | 0.827 | 0.151 | 0.993 | 0.000 | 1.000 |
| Default pass + sunset trial | 0.469 | 47.570 | 103.333 | 0.619 | 0.373 | 0.098 | 0.524 | 0.265 | 0.460 | 0.174 | 0.000 | 0.000 | 0.000 | 0.000 | 0.970 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.112 | 10.876 | 103.333 | 0.684 | 0.000 | 0.068 | 0.619 | 0.031 | 0.208 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.306 | 0.000 | 1.000 |
| Unicameral simple majority | 0.264 | 26.217 | 103.333 | 0.637 | 0.000 | 0.090 | 0.555 | 0.101 | 0.304 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 1.000 |
| Unicameral majority + mediation | 0.341 | 34.021 | 103.333 | 0.602 | 0.000 | 0.090 | 0.529 | 0.147 | 0.385 | 0.258 | 0.000 | 0.000 | 0.822 | 0.152 | 0.686 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.091 | 8.624 | 103.333 | 0.708 | 0.000 | 0.058 | 0.655 | 0.020 | 0.146 | 0.248 | 0.000 | 0.000 | 0.000 | 0.000 | 0.257 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.800 | -0.263 | 0.025 | -0.081 | -0.295 | -0.137 | 0.500 |
| Low Polarization | -11.160 | -0.186 | 0.030 | -0.139 | -0.145 | -0.066 | 0.499 |
| High Polarization | -16.867 | -0.281 | 0.018 | -0.037 | -0.363 | -0.177 | 0.500 |
| Low Party Loyalty | -15.140 | -0.252 | 0.024 | -0.088 | -0.296 | -0.139 | 0.499 |
| High Party Loyalty | -15.727 | -0.262 | 0.024 | -0.077 | -0.299 | -0.142 | 0.500 |
| Low Compromise Culture | -15.507 | -0.258 | 0.019 | -0.063 | -0.285 | -0.129 | 0.500 |
| High Compromise Culture | -15.160 | -0.253 | 0.022 | -0.083 | -0.289 | -0.137 | 0.500 |
| Low Lobbying Pressure | -15.813 | -0.264 | 0.023 | -0.079 | -0.311 | -0.152 | 0.500 |
| High Lobbying Pressure | -15.493 | -0.258 | 0.019 | -0.063 | -0.288 | -0.131 | 0.500 |
| Weak Constituency Pressure | -17.940 | -0.299 | 0.021 | -0.074 | -0.320 | -0.138 | 0.500 |
| Two-Party System | -6.407 | -0.107 | -0.005 | -0.024 | -0.142 | -0.080 | 0.333 |
| Multi-Party System | -31.020 | -0.517 | 0.122 | -0.303 | -0.545 | -0.335 | 0.810 |
| High Proposal Pressure | 3.513 | 0.020 | -0.017 | 0.010 | -0.031 | -0.058 | 0.167 |
| Extreme Proposal Pressure | 22.413 | 0.075 | -0.022 | 0.025 | 0.025 | -0.044 | 0.100 |
| Lobby-Fueled Flooding | 3.193 | 0.018 | -0.016 | 0.007 | -0.026 | -0.053 | 0.166 |
| Low-Compromise Flooding | 3.273 | 0.018 | -0.019 | 0.024 | -0.048 | -0.078 | 0.167 |
| Capture Crisis | 1.273 | 0.007 | -0.014 | 0.014 | -0.046 | -0.065 | 0.166 |
| Popular Anti-Lobbying Push | -2.313 | -0.019 | -0.013 | -0.003 | -0.053 | -0.051 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.588 | -0.743 | 0.743 | -0.211 | -0.583 | -0.421 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.399 | -0.074 | 0.073 | 0.001 | -0.186 | -0.447 | -0.263 | 0.000 |

## Sunset Trial Deltas

Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + sunset trial | -0.372 | 0.122 | -0.077 | -0.398 | -0.196 | 0.000 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.165 | -0.202 | 0.202 | 0.016 | -0.009 | -0.153 | -0.031 | 0.000 |

## Anti-Capture Deltas

Delta values compare anti-capture mechanisms against open `default-pass` across all cases. Negative capture and private-gain-ratio deltas are desirable; anti-lobby pass is the share of generated anti-lobbying reform bills enacted.

| Scenario | Productivity delta | Welfare delta | Capture delta | Public-alignment delta | Anti-lobby pass delta | Private-gain-ratio delta | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + anti-capture bundle | -0.092 | 0.022 | -0.090 | 0.010 | -0.034 | -0.193 | -0.006 |

## Budgeted Lobbying Deltas

Delta values compare explicit budgeted lobbying scenarios against open `default-pass` across all cases. Lobby spend is normalized per potential bill; defensive spend is the share of lobbying spend aimed at anti-lobbying reform bills.

| Scenario | Productivity delta | Welfare delta | Capture delta | Lobby spend/bill | Defensive spend share | Capture return/spend | Anti-lobby pass delta | Public-distortion delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + budgeted lobbying | 0.001 | -0.000 | 0.002 | 0.099 | 0.655 | 2.501 | -0.004 | -0.001 |

## Mediation Deltas

Delta values compare structured amendment mediation against the matching non-mediated scenario. Amendment rate is the share of potential bills whose policy position moved before final voting.

| Scenario | Baseline | Productivity delta | Welfare delta | Compromise delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Amendment rate | Amendment movement |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + mediated amendments | Default pass unless 2/3 block | 0.055 | -0.005 | 0.028 | 0.008 | -0.165 | -0.148 | 0.827 | 0.162 |
| Default pass + budgeted lobbying + mediation | Default pass + budgeted lobbying | 0.055 | -0.005 | 0.028 | 0.009 | -0.166 | -0.148 | 0.829 | 0.162 |
| Unicameral majority + mediation | Unicameral simple majority | 0.076 | -0.035 | -0.026 | 0.000 | 0.046 | 0.081 | 0.822 | 0.158 |

## Distributional-Harm Deltas

Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.

| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + harm-weighted threshold | -0.073 | 0.010 | -0.024 | 0.015 | 0.280 | 0.000 | -0.006 |
| Default pass + compensation amendments | 0.000 | -0.007 | -0.045 | 0.019 | 0.934 | 0.142 | -0.001 |
| Default pass + affected-group consent | -0.073 | 0.013 | -0.046 | 0.035 | 0.945 | 0.152 | -0.012 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.628 | 0.161 | -0.262 | -0.597 | -0.414 |
| Low Polarization | -0.407 | 0.089 | -0.213 | -0.262 | -0.128 |
| High Polarization | -0.684 | 0.188 | -0.207 | -0.722 | -0.552 |
| Low Party Loyalty | -0.605 | 0.157 | -0.267 | -0.603 | -0.419 |
| High Party Loyalty | -0.627 | 0.171 | -0.254 | -0.608 | -0.429 |
| Low Compromise Culture | -0.622 | 0.161 | -0.230 | -0.592 | -0.416 |
| High Compromise Culture | -0.604 | 0.154 | -0.250 | -0.593 | -0.410 |
| Low Lobbying Pressure | -0.622 | 0.161 | -0.259 | -0.615 | -0.434 |
| High Lobbying Pressure | -0.628 | 0.144 | -0.205 | -0.581 | -0.387 |
| Weak Constituency Pressure | -0.669 | 0.152 | -0.191 | -0.613 | -0.398 |
| Two-Party System | -0.619 | 0.164 | -0.263 | -0.594 | -0.407 |
| Multi-Party System | -0.620 | 0.167 | -0.240 | -0.604 | -0.408 |
| High Proposal Pressure | -0.628 | 0.162 | -0.249 | -0.608 | -0.422 |
| Extreme Proposal Pressure | -0.620 | 0.159 | -0.249 | -0.602 | -0.420 |
| Lobby-Fueled Flooding | -0.649 | 0.137 | -0.222 | -0.593 | -0.397 |
| Low-Compromise Flooding | -0.673 | 0.176 | -0.188 | -0.675 | -0.499 |
| Capture Crisis | -0.679 | 0.144 | -0.179 | -0.650 | -0.455 |
| Popular Anti-Lobbying Push | -0.550 | 0.134 | -0.263 | -0.508 | -0.338 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.725) | Default pass + mediated amendments (0.900) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.704) | Default pass + budgeted lobbying + mediation (0.934) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.738) | Default pass + budgeted lobbying + mediation (0.882) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.721) | Default pass + budgeted lobbying + mediation (0.911) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.713) | Default pass + budgeted lobbying + mediation (0.893) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.731) | Default pass + mediated amendments (0.869) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.696) | Default pass + mediated amendments (0.914) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.724) | Default pass + budgeted lobbying + mediation (0.899) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.705) | Default pass + mediated amendments (0.886) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.700) | Default pass + budgeted lobbying + mediation (0.939) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.726) | Default pass + budgeted lobbying + mediation (0.898) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.721) | Default pass + mediated amendments (0.907) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.721) | Default pass + budgeted lobbying + mediation (0.897) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.714) | Default pass + challenge vouchers (0.916) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.711) | Default pass + budgeted lobbying + mediation (0.888) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.737) | Default pass + budgeted lobbying + mediation (0.870) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.741) | Default pass + mediated amendments (0.885) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.692) | Default pass + budgeted lobbying + mediation (0.881) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Anti-capture scenarios test whether lobbying pressure can be reduced through vote firewalls, transparency, public-interest screens, audit sanctions, or combined safeguards.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Structured mediation scenarios let a bounded amendment stage move bills toward the chamber median/status quo before the final yes/no vote.
- The next model extension should add richer constituent and affected-group structure, because compromise quality should be judged against public will and concentrated harms rather than only chamber support.

## Reproduction

```sh
make campaign
```
