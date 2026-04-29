# Simulation Campaign v7

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 28
- experiment cases: 16

## Headline Findings

- Open default-pass averaged 0.840 productivity, versus 0.245 for simple majority.
- Open default-pass also averaged 0.455 low-support passage and 0.688 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.238 and reduced policy shift by 0.624, while changing productivity by -0.644.
- Challenge vouchers averaged 0.422 challenge use, changed productivity by -0.196, and changed low-support passage by -0.057 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.632, floor consideration by -0.789, and low-support passage by -0.240 relative to open default-pass.
- Adaptive tracks changed productivity by -0.418, low-support passage by -0.192, and policy shift by -0.474 relative to open default-pass.
- Sunset trial review changed productivity by -0.394, welfare by 0.114, and policy shift by -0.427 relative to open default-pass.
- Earned proposal credits denied 0.200 of potential proposals, changed welfare by 0.015, and changed proposer gain by -0.032 relative to open default-pass.
- Best average welfare in this campaign came from Default pass + strong cross-bloc cosponsors at 0.740.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass unless 2/3 block | 0.840 | 81.818 | 97.500 | 0.469 | 0.455 | 0.688 | 0.686 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.423 | 40.321 | 89.799 | 0.565 | 0.264 | 0.214 | 0.408 | 0.000 | 0.925 |
| Default pass + adaptive tracks + challenge | 0.566 | 62.268 | 88.811 | 0.523 | 0.367 | 0.336 | 0.471 | 0.395 | 0.919 |
| Default pass + challenge vouchers | 0.645 | 71.626 | 97.500 | 0.480 | 0.398 | 0.451 | 0.561 | 0.422 | 1.000 |
| Default pass + member challenge vouchers t=1 s=.82 | 0.351 | 43.367 | 97.500 | 0.556 | 0.170 | 0.176 | 0.365 | 0.781 | 1.000 |
| Default pass + member challenge vouchers t=2 s=.82 | 0.280 | 28.530 | 97.500 | 0.576 | 0.104 | 0.111 | 0.310 | 0.870 | 1.000 |
| Default pass + member challenge vouchers t=3 s=.82 | 0.268 | 25.326 | 97.500 | 0.582 | 0.088 | 0.101 | 0.301 | 0.887 | 1.000 |
| Default pass + party challenge vouchers t=10 s=.50 | 0.653 | 72.237 | 97.500 | 0.477 | 0.398 | 0.468 | 0.577 | 0.423 | 1.000 |
| Default pass + party challenge vouchers t=10 s=.65 | 0.648 | 71.866 | 97.500 | 0.478 | 0.399 | 0.460 | 0.570 | 0.422 | 1.000 |
| Default pass + party challenge vouchers t=10 s=1.00 | 0.643 | 71.544 | 97.500 | 0.482 | 0.401 | 0.442 | 0.549 | 0.420 | 1.000 |
| Default pass + party challenge vouchers t=10 s=1.25 | 0.644 | 71.525 | 97.500 | 0.484 | 0.406 | 0.432 | 0.536 | 0.416 | 1.000 |
| Default pass + party challenge vouchers t=15 s=.82 | 0.493 | 60.259 | 97.500 | 0.516 | 0.306 | 0.304 | 0.469 | 0.603 | 1.000 |
| Default pass + party challenge vouchers t=25 s=.82 | 0.386 | 49.344 | 97.500 | 0.549 | 0.193 | 0.209 | 0.388 | 0.746 | 1.000 |
| Default pass + party challenge vouchers t=3 s=.82 | 0.893 | 89.717 | 97.500 | 0.451 | 0.474 | 0.690 | 0.635 | 0.127 | 1.000 |
| Default pass + party challenge vouchers t=6 s=.82 | 0.786 | 81.958 | 97.500 | 0.460 | 0.450 | 0.587 | 0.610 | 0.254 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.209 | 18.948 | 19.149 | 0.646 | 0.215 | 0.066 | 0.223 | 0.000 | 0.211 |
| Default pass + cross-bloc cosponsors + challenge | 0.169 | 15.700 | 19.248 | 0.653 | 0.071 | 0.047 | 0.198 | 0.131 | 0.212 |
| Default pass + strong cross-bloc cosponsors | 0.069 | 5.775 | 5.780 | 0.740 | 0.070 | 0.016 | 0.118 | 0.000 | 0.069 |
| Default pass + earned proposal credits | 0.674 | 60.434 | 71.631 | 0.483 | 0.445 | 0.529 | 0.654 | 0.000 | 0.800 |
| Default pass + earned proposal credits + challenge | 0.443 | 45.433 | 70.776 | 0.510 | 0.354 | 0.272 | 0.495 | 0.415 | 0.790 |
| Default pass + q=12 challenge escalation s=.82 | 0.271 | 25.526 | 97.500 | 0.580 | 0.100 | 0.101 | 0.295 | 0.876 | 1.000 |
| Default pass + q=20 challenge escalation s=.82 | 0.274 | 25.766 | 97.500 | 0.578 | 0.107 | 0.101 | 0.292 | 0.866 | 1.000 |
| Default pass + q=6 challenge escalation s=.82 | 0.270 | 25.341 | 97.500 | 0.581 | 0.092 | 0.100 | 0.295 | 0.883 | 1.000 |
| Default pass + informed guarded committee | 0.196 | 18.530 | 18.663 | 0.610 | 0.217 | 0.065 | 0.246 | 0.000 | 0.198 |
| Default pass + sunset trial + challenge | 0.368 | 38.350 | 97.500 | 0.584 | 0.322 | 0.188 | 0.407 | 0.422 | 1.000 |
| Default pass + sunset trial | 0.447 | 42.636 | 97.500 | 0.582 | 0.381 | 0.261 | 0.478 | 0.000 | 1.000 |
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
| Default pass + party challenge vouchers t=3 s=.82 | 0.053 | 0.019 | 0.002 | -0.051 | 0.127 |
| Default pass + party challenge vouchers t=6 s=.82 | -0.054 | -0.005 | -0.101 | -0.076 | 0.254 |
| Default pass + party challenge vouchers t=15 s=.82 | -0.348 | -0.149 | -0.384 | -0.217 | 0.603 |
| Default pass + party challenge vouchers t=25 s=.82 | -0.454 | -0.262 | -0.479 | -0.298 | 0.746 |
| Default pass + party challenge vouchers t=10 s=.50 | -0.187 | -0.057 | -0.220 | -0.109 | 0.423 |
| Default pass + party challenge vouchers t=10 s=.65 | -0.192 | -0.057 | -0.228 | -0.116 | 0.422 |
| Default pass + party challenge vouchers t=10 s=1.00 | -0.197 | -0.055 | -0.246 | -0.137 | 0.420 |
| Default pass + party challenge vouchers t=10 s=1.25 | -0.196 | -0.049 | -0.256 | -0.150 | 0.416 |
| Default pass + member challenge vouchers t=1 s=.82 | -0.489 | -0.286 | -0.512 | -0.321 | 0.781 |
| Default pass + member challenge vouchers t=2 s=.82 | -0.561 | -0.351 | -0.578 | -0.376 | 0.870 |
| Default pass + member challenge vouchers t=3 s=.82 | -0.572 | -0.367 | -0.587 | -0.385 | 0.887 |
| Default pass + q=6 challenge escalation s=.82 | -0.571 | -0.363 | -0.588 | -0.391 | 0.883 |
| Default pass + q=12 challenge escalation s=.82 | -0.569 | -0.355 | -0.588 | -0.391 | 0.876 |
| Default pass + q=20 challenge escalation s=.82 | -0.567 | -0.348 | -0.587 | -0.394 | 0.866 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.632 | -0.789 | 0.789 | -0.240 | -0.622 | -0.464 | 0.000 |
| Default pass + strong cross-bloc cosponsors | -0.771 | -0.931 | 0.931 | -0.386 | -0.673 | -0.568 | 0.000 |
| Default pass + cross-bloc cosponsors + challenge | -0.671 | -0.788 | 0.788 | -0.384 | -0.641 | -0.488 | 0.131 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.418 | -0.075 | 0.074 | 0.001 | -0.192 | -0.474 | -0.278 | 0.000 |
| Default pass + adaptive tracks + challenge | -0.274 | -0.081 | 0.080 | 0.001 | -0.089 | -0.352 | -0.215 | 0.395 |

## Sunset Trial Deltas

Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + sunset trial | -0.394 | 0.114 | -0.075 | -0.427 | -0.208 | 0.000 |
| Default pass + sunset trial + challenge | -0.472 | 0.116 | -0.133 | -0.500 | -0.279 | 0.422 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.166 | -0.200 | 0.200 | 0.015 | -0.010 | -0.159 | -0.032 | 0.000 |
| Default pass + earned proposal credits + challenge | -0.398 | -0.210 | 0.210 | 0.042 | -0.101 | -0.416 | -0.191 | 0.415 |

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
| Baseline | Default pass + strong cross-bloc cosponsors (0.728) | Default pass + party challenge vouchers t=3 s=.82 (0.870) | Unicameral simple majority (0.000) |
| Low Polarization | Default pass + strong cross-bloc cosponsors (0.671) | Default pass + party challenge vouchers t=3 s=.82 (0.892) | Unicameral simple majority (0.000) |
| High Polarization | Default pass + strong cross-bloc cosponsors (0.785) | Default pass + party challenge vouchers t=3 s=.82 (0.863) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Default pass + strong cross-bloc cosponsors (0.718) | Default pass + party challenge vouchers t=3 s=.82 (0.876) | Unicameral simple majority (0.000) |
| High Party Loyalty | Default pass + strong cross-bloc cosponsors (0.716) | Default pass + party challenge vouchers t=3 s=.82 (0.873) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Default pass + strong cross-bloc cosponsors (0.771) | Default pass + party challenge vouchers t=3 s=.82 (0.868) | Unicameral simple majority (0.000) |
| High Compromise Culture | Default pass + strong cross-bloc cosponsors (0.685) | Default pass + party challenge vouchers t=3 s=.82 (0.878) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Default pass + strong cross-bloc cosponsors (0.729) | Default pass + party challenge vouchers t=3 s=.82 (0.874) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + strong cross-bloc cosponsors (0.743) | Default pass + party challenge vouchers t=3 s=.82 (0.871) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + strong cross-bloc cosponsors (0.811) | Default pass + party challenge vouchers t=3 s=.82 (0.869) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + strong cross-bloc cosponsors (0.764) | Default pass + party challenge vouchers t=3 s=.82 (0.916) | Unicameral simple majority (0.000) |
| Multi-Party System | Default pass + strong cross-bloc cosponsors (0.692) | Default pass unless 2/3 block (0.849) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Default pass + strong cross-bloc cosponsors (0.726) | Default pass + party challenge vouchers t=3 s=.82 (0.957) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Default pass + strong cross-bloc cosponsors (0.727) | Default pass + party challenge vouchers t=3 s=.82 (0.974) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + strong cross-bloc cosponsors (0.773) | Default pass + party challenge vouchers t=3 s=.82 (0.957) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Default pass + strong cross-bloc cosponsors (0.808) | Default pass + party challenge vouchers t=3 s=.82 (0.955) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- The challenge sweep compares token budgets, challenge thresholds, party-held tokens, member-held tokens, and tokenless q-member escalation.
- Cross-bloc cosponsorship tests coalition breadth as a pre-floor agenda gate, before default-pass or challenge mechanics can operate.
- Adaptive procedural tracks test whether low-risk bills can stay in a fast lane while high-risk bills receive stronger review.
- Sunset trial rules test whether risky default enactments can be made reversible after automatic review.
- Earned proposal credits test whether agenda access can learn from proposer track records instead of using only fixed up-front costs.
- The next model extension should add structured amendment or mediation, because the current agenda systems screen and route bills but still rarely change bill content before final yes/no choice.

## Reproduction

```sh
make campaign
```
