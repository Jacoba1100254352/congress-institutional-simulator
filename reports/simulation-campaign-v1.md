# Simulation Campaign v1

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 11
- experiment cases: 16

## Headline Findings

- Open default-pass averaged 0.840 productivity, versus 0.245 for simple majority.
- Open default-pass also averaged 0.455 low-support passage and 0.688 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.236 and reduced policy shift by 0.623, while changing productivity by -0.643.
- Proposal-cost screening reduced floor load by 47.296 bills/run and enactments by 34.043 bills/run, but raised proposer gain by 0.437.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.671.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.158 | 14.576 | 97.500 | 0.624 | 0.000 | 0.050 | 0.238 | 1.000 |
| Default pass unless 2/3 block | 0.840 | 81.818 | 97.500 | 0.469 | 0.455 | 0.688 | 0.686 | 1.000 |
| Default pass + proposal access screen | 0.340 | 32.382 | 37.157 | 0.557 | 0.346 | 0.117 | 0.238 | 0.387 |
| Default pass + representative committee gate | 0.297 | 28.132 | 28.457 | 0.556 | 0.296 | 0.150 | 0.415 | 0.300 |
| Default pass + proposal costs | 0.483 | 47.774 | 50.204 | 0.453 | 0.492 | 0.607 | 1.124 | 0.509 |
| Default pass + costs + informed guardrails | 0.053 | 5.067 | 5.090 | 0.610 | 0.288 | 0.031 | 0.565 | 0.053 |
| Default pass + access + committee | 0.204 | 19.168 | 19.290 | 0.601 | 0.212 | 0.067 | 0.247 | 0.205 |
| Default pass + informed guarded committee | 0.198 | 18.643 | 18.771 | 0.610 | 0.220 | 0.065 | 0.247 | 0.199 |
| Bicameral majority + presidential veto | 0.101 | 9.280 | 97.500 | 0.643 | 0.000 | 0.029 | 0.215 | 1.000 |
| Unicameral simple majority | 0.245 | 22.961 | 97.500 | 0.593 | 0.000 | 0.098 | 0.322 | 1.000 |
| Unicameral 60 percent passage | 0.081 | 7.284 | 97.500 | 0.671 | 0.000 | 0.018 | 0.154 | 1.000 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -21.053 | -29.287 | -0.351 | -0.018 | 0.037 | -0.080 | 0.445 |
| Low Polarization | -33.840 | -41.067 | -0.564 | -0.016 | 0.040 | -0.181 | 0.369 |
| High Polarization | -19.147 | -27.467 | -0.319 | -0.015 | 0.032 | -0.051 | 0.492 |
| Low Party Loyalty | -20.753 | -28.567 | -0.346 | -0.017 | 0.036 | -0.081 | 0.427 |
| High Party Loyalty | -20.753 | -29.280 | -0.346 | -0.018 | 0.043 | -0.080 | 0.435 |
| Low Compromise Culture | -19.667 | -28.273 | -0.328 | -0.015 | 0.022 | -0.072 | 0.413 |
| High Compromise Culture | -22.300 | -29.460 | -0.372 | -0.015 | 0.048 | -0.088 | 0.458 |
| Low Lobbying Pressure | -22.200 | -30.260 | -0.370 | -0.019 | 0.041 | -0.092 | 0.463 |
| High Lobbying Pressure | -19.133 | -27.553 | -0.319 | -0.017 | 0.039 | -0.064 | 0.402 |
| Weak Constituency Pressure | -22.460 | -29.427 | -0.374 | -0.015 | 0.044 | -0.082 | 0.457 |
| Two-Party System | -20.553 | -28.680 | -0.343 | -0.015 | 0.050 | -0.076 | 0.428 |
| Multi-Party System | -21.393 | -28.640 | -0.357 | -0.012 | 0.034 | -0.084 | 0.440 |
| High Proposal Pressure | -61.913 | -86.693 | -0.344 | -0.020 | 0.038 | -0.069 | 0.449 |
| Extreme Proposal Pressure | -102.633 | -143.667 | -0.342 | -0.015 | 0.039 | -0.072 | 0.438 |
| Lobby-Fueled Flooding | -58.853 | -83.313 | -0.327 | -0.014 | 0.021 | -0.066 | 0.415 |
| Low-Compromise Flooding | -58.040 | -85.107 | -0.322 | -0.014 | 0.023 | -0.057 | 0.468 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.653 | 0.148 | -0.251 | -0.635 | -0.446 |
| Low Polarization | -0.422 | 0.085 | -0.220 | -0.278 | -0.135 |
| High Polarization | -0.711 | 0.177 | -0.217 | -0.742 | -0.573 |
| Low Party Loyalty | -0.636 | 0.141 | -0.257 | -0.624 | -0.433 |
| High Party Loyalty | -0.649 | 0.142 | -0.244 | -0.635 | -0.466 |
| Low Compromise Culture | -0.658 | 0.150 | -0.209 | -0.631 | -0.443 |
| High Compromise Culture | -0.644 | 0.144 | -0.264 | -0.634 | -0.436 |
| Low Lobbying Pressure | -0.649 | 0.146 | -0.233 | -0.632 | -0.444 |
| High Lobbying Pressure | -0.644 | 0.129 | -0.242 | -0.636 | -0.453 |
| Weak Constituency Pressure | -0.682 | 0.141 | -0.207 | -0.639 | -0.424 |
| Two-Party System | -0.645 | 0.144 | -0.241 | -0.638 | -0.454 |
| Multi-Party System | -0.651 | 0.150 | -0.259 | -0.638 | -0.445 |
| High Proposal Pressure | -0.648 | 0.146 | -0.245 | -0.638 | -0.456 |
| Extreme Proposal Pressure | -0.640 | 0.142 | -0.244 | -0.633 | -0.448 |
| Lobby-Fueled Flooding | -0.662 | 0.127 | -0.245 | -0.645 | -0.447 |
| Low-Compromise Flooding | -0.691 | 0.156 | -0.192 | -0.699 | -0.525 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.667) | Default pass unless 2/3 block (0.836) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.670) | Default pass unless 2/3 block (0.835) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.694) | Default pass unless 2/3 block (0.839) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.666) | Default pass unless 2/3 block (0.836) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.675) | Default pass unless 2/3 block (0.833) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.697) | Default pass unless 2/3 block (0.827) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.666) | Default pass unless 2/3 block (0.858) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.691) | Default pass unless 2/3 block (0.842) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Unicameral 60 percent passage (0.632) | Default pass unless 2/3 block (0.834) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Unicameral 60 percent passage (0.679) | Default pass unless 2/3 block (0.866) | Unicameral simple majority (0.000) |
| Two-Party System | Unicameral 60 percent passage (0.667) | Default pass unless 2/3 block (0.840) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.673) | Default pass unless 2/3 block (0.849) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.674) | Default pass unless 2/3 block (0.840) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.673) | Default pass unless 2/3 block (0.838) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Unicameral 60 percent passage (0.630) | Default pass unless 2/3 block (0.841) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.687) | Default pass unless 2/3 block (0.830) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Proposal-cost screens are useful for measuring flooding as institutional load: floor/run and enacted/run expose costs hidden by percentage-only metrics.
- The current cost screen reduces volume, but it also selects for proposals with high proposer value or positive lobby pressure; that makes cost design an object of study, not a solved safeguard.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- The next model extension should run proposal-cost parameter sweeps and compare alternative cost mechanisms, because agenda screening is now the central default-pass tradeoff.

## Reproduction

```sh
make campaign
```
