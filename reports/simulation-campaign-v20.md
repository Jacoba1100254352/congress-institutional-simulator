# Simulation Campaign v20 Strategy and Calibration

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 17
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.841 productivity, versus 0.266 for simple majority.
- Open default-pass also averaged 0.449 low-support passage and 0.664 policy shift.
- Budgeted lobbying spent 0.103 per potential bill, with 0.629 of spend aimed defensively at anti-lobbying reform bills.
- Public objection windows triggered on 0.647 of potential bills and changed low-support passage by -0.180 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.659, and status-quo wins averaged 0.450 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.708.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.805 | 103.333 | 0.665 | 0.000 | 0.078 | 0.593 | 0.053 | 0.230 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.458 | 0.000 | 1.000 |
| Current U.S.-style system | 0.067 | 6.338 | 103.333 | 0.704 | 0.000 | 0.061 | 0.656 | 0.015 | 0.157 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.183 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.841 | 86.900 | 103.333 | 0.496 | 0.449 | 0.168 | 0.392 | 0.664 | 0.657 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.000 | 1.000 |
| Default pass + adaptive proposers | 0.861 | 88.603 | 102.607 | 0.495 | 0.444 | 0.163 | 0.399 | 0.568 | 0.590 | 0.256 | 0.000 | 0.000 | 0.995 | 0.019 | 0.993 | 0.000 | 0.995 |
| Default pass + adaptive proposers + strategic lobbying | 0.861 | 88.553 | 102.602 | 0.494 | 0.445 | 0.164 | 0.398 | 0.568 | 0.590 | 0.258 | 0.125 | 0.586 | 0.995 | 0.019 | 0.989 | 0.000 | 0.995 |
| Default pass + pairwise policy tournament | 0.550 | 56.361 | 56.369 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.202 | 0.000 | 0.000 | 0.550 | 0.000 | 0.944 | 0.000 | 0.550 |
| Default pass + budgeted lobbying | 0.843 | 86.975 | 103.333 | 0.495 | 0.450 | 0.168 | 0.391 | 0.665 | 0.656 | 0.267 | 0.103 | 0.629 | 0.000 | 0.000 | 0.990 | 0.000 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.404 | 41.193 | 103.333 | 0.629 | 0.248 | 0.106 | 0.516 | 0.211 | 0.434 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.963 | 0.000 | 1.000 |
| Default pass + adaptive strategy bundle | 0.965 | 99.159 | 102.662 | 0.456 | 0.377 | 0.120 | 0.433 | 0.370 | 0.346 | 0.239 | 0.123 | 0.555 | 0.996 | 0.230 | 0.990 | 0.000 | 0.996 |
| Default pass + law registry | 0.867 | 89.698 | 103.333 | 0.491 | 0.398 | 0.171 | 0.391 | 0.835 | 0.597 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + multi-round mediation | 0.957 | 98.540 | 103.333 | 0.449 | 0.394 | 0.117 | 0.426 | 0.391 | 0.368 | 0.270 | 0.000 | 0.000 | 0.720 | 0.240 | 0.989 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.784 | 86.294 | 103.333 | 0.460 | 0.301 | 0.114 | 0.438 | 0.296 | 0.340 | 0.275 | 0.000 | 0.000 | 0.718 | 0.241 | 0.867 | 0.376 | 1.000 |
| Default pass + public objection window | 0.447 | 45.377 | 103.333 | 0.592 | 0.268 | 0.104 | 0.505 | 0.214 | 0.383 | 0.216 | 0.000 | 0.000 | 0.000 | 0.000 | 0.901 | 0.000 | 1.000 |
| Default pass + strategic lobbying | 0.841 | 86.854 | 103.333 | 0.495 | 0.451 | 0.168 | 0.391 | 0.664 | 0.657 | 0.267 | 0.122 | 0.594 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.112 | 10.794 | 103.333 | 0.682 | 0.000 | 0.070 | 0.617 | 0.031 | 0.210 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.306 | 0.000 | 1.000 |
| Unicameral simple majority | 0.266 | 26.283 | 103.333 | 0.636 | 0.000 | 0.091 | 0.553 | 0.103 | 0.311 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.649 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.089 | 8.458 | 103.333 | 0.708 | 0.000 | 0.059 | 0.654 | 0.020 | 0.150 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 | 0.251 | 0.000 | 1.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.436 | 5.132 | 0.608 | 0.036 | 0.171 |

## Budgeted Lobbying Deltas

Delta values compare explicit budgeted lobbying scenarios against open `default-pass` across all cases. Lobby spend is normalized per potential bill; defensive spend is the share of lobbying spend aimed at anti-lobbying reform bills.

| Scenario | Productivity delta | Welfare delta | Capture delta | Lobby spend/bill | Defensive spend share | Capture return/spend | Anti-lobby pass delta | Public-distortion delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + budgeted lobbying | 0.001 | -0.001 | 0.002 | 0.103 | 0.629 | 2.403 | -0.001 | -0.000 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.292 | 0.144 | -0.407 | -0.659 | -0.653 | 0.001 | 0.002 | 6.000 | 0.450 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.732) | Default pass + adaptive strategy bundle (0.973) | Current U.S.-style system (0.000) |
| Low Polarization | Current U.S.-style system (0.704) | Default pass + adaptive strategy bundle (0.990) | Current U.S.-style system (0.000) |
| High Polarization | Unicameral 60 percent passage (0.727) | Default pass + adaptive strategy bundle (0.961) | Current U.S.-style system (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.714) | Default pass + adaptive strategy bundle (0.978) | Current U.S.-style system (0.000) |
| High Party Loyalty | Current U.S.-style system (0.729) | Default pass + adaptive strategy bundle (0.973) | Current U.S.-style system (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.734) | Default pass + adaptive strategy bundle (0.959) | Current U.S.-style system (0.000) |
| High Compromise Culture | Current U.S.-style system (0.710) | Default pass + adaptive strategy bundle (0.983) | Current U.S.-style system (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.730) | Default pass + adaptive strategy bundle (0.976) | Current U.S.-style system (0.000) |
| High Lobbying Pressure | Current U.S.-style system (0.692) | Default pass + adaptive strategy bundle (0.947) | Current U.S.-style system (0.000) |
| Weak Constituency Pressure | Unicameral 60 percent passage (0.714) | Default pass + adaptive strategy bundle (0.979) | Current U.S.-style system (0.000) |
| Two-Party System | Unicameral 60 percent passage (0.724) | Default pass + adaptive strategy bundle (0.974) | Current U.S.-style system (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.704) | Default pass + adaptive strategy bundle (0.977) | Current U.S.-style system (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.721) | Default pass + adaptive strategy bundle (0.970) | Current U.S.-style system (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.718) | Default pass + adaptive strategy bundle (0.965) | Current U.S.-style system (0.000) |
| Lobby-Fueled Flooding | Unicameral 60 percent passage (0.668) | Default pass + multi-round mediation (0.939) | Current U.S.-style system (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.720) | Default pass + adaptive strategy bundle (0.950) | Current U.S.-style system (0.000) |
| Capture Crisis | Current U.S.-style system (0.641) | Default pass + adaptive strategy bundle (0.925) | Current U.S.-style system (0.000) |
| Popular Anti-Lobbying Push | Current U.S.-style system (0.697) | Default pass + adaptive strategy bundle (0.954) | Current U.S.-style system (0.000) |

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
