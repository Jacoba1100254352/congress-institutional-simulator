# Simulation Campaign v3

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 19
- experiment cases: 16

## Headline Findings

- Open default-pass averaged 0.840 productivity, versus 0.245 for simple majority.
- Open default-pass also averaged 0.455 low-support passage and 0.688 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.238 and reduced policy shift by 0.624, while changing productivity by -0.644.
- Challenge vouchers averaged 0.422 challenge use, changed productivity by -0.196, and changed low-support passage by -0.057 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.671.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass unless 2/3 block | 0.840 | 81.818 | 97.500 | 0.469 | 0.455 | 0.688 | 0.686 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.645 | 71.626 | 97.500 | 0.480 | 0.398 | 0.451 | 0.561 | 0.422 | 1.000 |
| Default pass + member challenge vouchers t=1 s=.82 | 0.352 | 43.432 | 97.500 | 0.555 | 0.166 | 0.176 | 0.366 | 0.781 | 1.000 |
| Default pass + member challenge vouchers t=2 s=.82 | 0.280 | 28.560 | 97.500 | 0.576 | 0.104 | 0.111 | 0.309 | 0.870 | 1.000 |
| Default pass + member challenge vouchers t=3 s=.82 | 0.269 | 25.438 | 97.500 | 0.582 | 0.087 | 0.101 | 0.301 | 0.887 | 1.000 |
| Default pass + party challenge vouchers t=10 s=.50 | 0.654 | 72.254 | 97.500 | 0.477 | 0.398 | 0.469 | 0.578 | 0.423 | 1.000 |
| Default pass + party challenge vouchers t=10 s=.65 | 0.648 | 71.903 | 97.500 | 0.479 | 0.397 | 0.459 | 0.569 | 0.422 | 1.000 |
| Default pass + party challenge vouchers t=10 s=1.00 | 0.643 | 71.500 | 97.500 | 0.482 | 0.402 | 0.442 | 0.549 | 0.420 | 1.000 |
| Default pass + party challenge vouchers t=10 s=1.25 | 0.644 | 71.524 | 97.500 | 0.484 | 0.406 | 0.432 | 0.537 | 0.416 | 1.000 |
| Default pass + party challenge vouchers t=15 s=.82 | 0.493 | 60.285 | 97.500 | 0.516 | 0.304 | 0.305 | 0.469 | 0.603 | 1.000 |
| Default pass + party challenge vouchers t=25 s=.82 | 0.386 | 49.304 | 97.500 | 0.550 | 0.190 | 0.210 | 0.389 | 0.746 | 1.000 |
| Default pass + party challenge vouchers t=3 s=.82 | 0.893 | 89.721 | 97.500 | 0.451 | 0.475 | 0.690 | 0.635 | 0.127 | 1.000 |
| Default pass + party challenge vouchers t=6 s=.82 | 0.786 | 81.896 | 97.500 | 0.460 | 0.451 | 0.586 | 0.610 | 0.254 | 1.000 |
| Default pass + q=12 challenge escalation s=.82 | 0.273 | 25.690 | 97.500 | 0.580 | 0.100 | 0.102 | 0.297 | 0.875 | 1.000 |
| Default pass + q=20 challenge escalation s=.82 | 0.275 | 25.846 | 97.500 | 0.578 | 0.109 | 0.102 | 0.294 | 0.866 | 1.000 |
| Default pass + q=6 challenge escalation s=.82 | 0.270 | 25.417 | 97.500 | 0.581 | 0.093 | 0.100 | 0.296 | 0.883 | 1.000 |
| Default pass + informed guarded committee | 0.196 | 18.530 | 18.663 | 0.610 | 0.217 | 0.065 | 0.246 | 0.000 | 0.198 |
| Unicameral simple majority | 0.245 | 22.961 | 97.500 | 0.593 | 0.000 | 0.098 | 0.322 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.081 | 7.284 | 97.500 | 0.671 | 0.000 | 0.018 | 0.154 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.733 | -0.262 | 0.012 | -0.065 | -0.305 | -0.142 | 0.500 |
| Low Polarization | -10.907 | -0.182 | 0.024 | -0.136 | -0.142 | -0.063 | 0.499 |
| High Polarization | -17.620 | -0.294 | 0.009 | -0.025 | -0.361 | -0.153 | 0.500 |
| Low Party Loyalty | -15.267 | -0.254 | 0.015 | -0.078 | -0.301 | -0.141 | 0.499 |
| High Party Loyalty | -15.547 | -0.259 | 0.015 | -0.060 | -0.307 | -0.149 | 0.500 |
| Low Compromise Culture | -15.920 | -0.265 | 0.012 | -0.057 | -0.299 | -0.126 | 0.500 |
| High Compromise Culture | -15.993 | -0.267 | 0.020 | -0.087 | -0.311 | -0.138 | 0.500 |
| Low Lobbying Pressure | -16.100 | -0.268 | 0.021 | -0.065 | -0.305 | -0.133 | 0.500 |
| High Lobbying Pressure | -15.593 | -0.260 | 0.016 | -0.044 | -0.306 | -0.136 | 0.500 |
| Weak Constituency Pressure | -18.280 | -0.305 | 0.018 | -0.064 | -0.334 | -0.140 | 0.500 |
| Two-Party System | -6.867 | -0.114 | -0.005 | -0.016 | -0.159 | -0.083 | 0.333 |
| Multi-Party System | -31.667 | -0.528 | 0.094 | -0.290 | -0.559 | -0.330 | 0.815 |
| High Proposal Pressure | 3.327 | 0.018 | -0.016 | 0.014 | -0.037 | -0.063 | 0.167 |
| Extreme Proposal Pressure | 23.047 | 0.077 | -0.021 | 0.024 | 0.022 | -0.052 | 0.100 |
| Lobby-Fueled Flooding | 2.560 | 0.014 | -0.012 | 0.014 | -0.041 | -0.065 | 0.166 |
| Low-Compromise Flooding | 3.500 | 0.019 | -0.016 | 0.024 | -0.052 | -0.082 | 0.167 |

## Challenge Sweep Summary

Delta values compare each challenge variant against open `default-pass` across all cases. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity deltas show the throughput cost or gain.

| Scenario | Productivity delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default pass + challenge vouchers | -0.196 | -0.057 | -0.237 | -0.125 | 0.422 |
| Default pass + party challenge vouchers t=3 s=.82 | 0.053 | 0.020 | 0.002 | -0.051 | 0.127 |
| Default pass + party challenge vouchers t=6 s=.82 | -0.055 | -0.004 | -0.102 | -0.076 | 0.254 |
| Default pass + party challenge vouchers t=15 s=.82 | -0.347 | -0.151 | -0.383 | -0.217 | 0.603 |
| Default pass + party challenge vouchers t=25 s=.82 | -0.455 | -0.265 | -0.479 | -0.297 | 0.746 |
| Default pass + party challenge vouchers t=10 s=.50 | -0.187 | -0.058 | -0.220 | -0.108 | 0.423 |
| Default pass + party challenge vouchers t=10 s=.65 | -0.192 | -0.058 | -0.229 | -0.117 | 0.422 |
| Default pass + party challenge vouchers t=10 s=1.00 | -0.197 | -0.054 | -0.246 | -0.137 | 0.420 |
| Default pass + party challenge vouchers t=10 s=1.25 | -0.197 | -0.049 | -0.256 | -0.149 | 0.416 |
| Default pass + member challenge vouchers t=1 s=.82 | -0.489 | -0.289 | -0.512 | -0.320 | 0.781 |
| Default pass + member challenge vouchers t=2 s=.82 | -0.560 | -0.351 | -0.578 | -0.377 | 0.870 |
| Default pass + member challenge vouchers t=3 s=.82 | -0.571 | -0.368 | -0.587 | -0.385 | 0.887 |
| Default pass + q=6 challenge escalation s=.82 | -0.571 | -0.362 | -0.588 | -0.390 | 0.883 |
| Default pass + q=12 challenge escalation s=.82 | -0.568 | -0.355 | -0.586 | -0.389 | 0.875 |
| Default pass + q=20 challenge escalation s=.82 | -0.566 | -0.347 | -0.586 | -0.392 | 0.866 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.657 | 0.149 | -0.253 | -0.637 | -0.450 |
| Low Polarization | -0.419 | 0.083 | -0.213 | -0.276 | -0.132 |
| High Polarization | -0.712 | 0.170 | -0.225 | -0.742 | -0.577 |
| Low Party Loyalty | -0.643 | 0.143 | -0.271 | -0.625 | -0.430 |
| High Party Loyalty | -0.645 | 0.141 | -0.247 | -0.631 | -0.458 |
| Low Compromise Culture | -0.659 | 0.151 | -0.217 | -0.631 | -0.449 |
| High Compromise Culture | -0.644 | 0.140 | -0.247 | -0.634 | -0.434 |
| Low Lobbying Pressure | -0.647 | 0.148 | -0.230 | -0.632 | -0.451 |
| High Lobbying Pressure | -0.646 | 0.124 | -0.247 | -0.635 | -0.448 |
| Weak Constituency Pressure | -0.682 | 0.148 | -0.209 | -0.641 | -0.437 |
| Two-Party System | -0.649 | 0.146 | -0.246 | -0.639 | -0.454 |
| Multi-Party System | -0.652 | 0.148 | -0.256 | -0.637 | -0.441 |
| High Proposal Pressure | -0.648 | 0.144 | -0.250 | -0.638 | -0.456 |
| Extreme Proposal Pressure | -0.642 | 0.144 | -0.244 | -0.633 | -0.448 |
| Lobby-Fueled Flooding | -0.663 | 0.126 | -0.247 | -0.647 | -0.453 |
| Low-Compromise Flooding | -0.694 | 0.158 | -0.203 | -0.700 | -0.527 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.667) | Default pass + party challenge vouchers t=3 s=.82 (0.873) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.670) | Default pass + party challenge vouchers t=3 s=.82 (0.892) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.694) | Default pass + party challenge vouchers t=3 s=.82 (0.865) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.666) | Default pass + party challenge vouchers t=3 s=.82 (0.876) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.675) | Default pass + party challenge vouchers t=3 s=.82 (0.874) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.697) | Default pass + party challenge vouchers t=3 s=.82 (0.868) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.666) | Default pass + party challenge vouchers t=3 s=.82 (0.877) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.691) | Default pass + party challenge vouchers t=3 s=.82 (0.875) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Unicameral 60 percent passage (0.632) | Default pass + party challenge vouchers t=3 s=.82 (0.873) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Unicameral 60 percent passage (0.679) | Default pass + party challenge vouchers t=3 s=.82 (0.868) | Unicameral simple majority (0.000) |
| Two-Party System | Unicameral 60 percent passage (0.667) | Default pass + party challenge vouchers t=3 s=.82 (0.916) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.673) | Default pass unless 2/3 block (0.849) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.674) | Default pass + party challenge vouchers t=3 s=.82 (0.957) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.673) | Default pass + party challenge vouchers t=3 s=.82 (0.975) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Unicameral 60 percent passage (0.630) | Default pass + party challenge vouchers t=3 s=.82 (0.957) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.687) | Default pass + party challenge vouchers t=3 s=.82 (0.954) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- The challenge sweep compares token budgets, challenge thresholds, party-held tokens, member-held tokens, and tokenless q-member escalation.
- The next model extension should add coalition-breadth proposal access, because challenge mechanics still operate after a bill enters the agenda.

## Reproduction

```sh
make campaign
```
