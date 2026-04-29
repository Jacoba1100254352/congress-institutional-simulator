# Simulation Campaign v2

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 9
- experiment cases: 16

## Headline Findings

- Open default-pass averaged 0.840 productivity, versus 0.245 for simple majority.
- Open default-pass also averaged 0.455 low-support passage and 0.688 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.234 and reduced policy shift by 0.623, while changing productivity by -0.643.
- Proposal-cost screening reduced floor load by 47.305 bills/run and enactments by 34.034 bills/run, but raised proposer gain by 0.438.
- Challenge vouchers averaged 0.422 challenge use, changed productivity by -0.196, and changed low-support passage by -0.058 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.671.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.158 | 14.509 | 97.500 | 0.623 | 0.000 | 0.049 | 0.236 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.840 | 81.818 | 97.500 | 0.469 | 0.455 | 0.688 | 0.686 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.644 | 71.596 | 97.500 | 0.481 | 0.398 | 0.451 | 0.561 | 0.422 | 1.000 |
| Default pass + challenge vouchers + info | 0.642 | 71.423 | 97.500 | 0.482 | 0.398 | 0.447 | 0.558 | 0.421 | 1.000 |
| Default pass + proposal costs | 0.482 | 47.784 | 50.195 | 0.453 | 0.491 | 0.607 | 1.124 | 0.000 | 0.508 |
| Default pass + informed guarded committee | 0.197 | 18.569 | 18.714 | 0.609 | 0.221 | 0.065 | 0.248 | 0.000 | 0.199 |
| Bicameral majority + presidential veto | 0.101 | 9.253 | 97.500 | 0.643 | 0.000 | 0.029 | 0.218 | 0.000 | 1.000 |
| Unicameral simple majority | 0.245 | 22.961 | 97.500 | 0.593 | 0.000 | 0.098 | 0.322 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.081 | 7.284 | 97.500 | 0.671 | 0.000 | 0.018 | 0.154 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.927 | -0.265 | 0.012 | -0.061 | -0.306 | -0.139 | 0.500 |
| Low Polarization | -11.147 | -0.186 | 0.024 | -0.138 | -0.145 | -0.063 | 0.500 |
| High Polarization | -17.567 | -0.293 | 0.008 | -0.026 | -0.359 | -0.150 | 0.500 |
| Low Party Loyalty | -15.253 | -0.254 | 0.015 | -0.084 | -0.302 | -0.146 | 0.499 |
| High Party Loyalty | -15.473 | -0.258 | 0.014 | -0.061 | -0.304 | -0.149 | 0.500 |
| Low Compromise Culture | -15.907 | -0.265 | 0.012 | -0.050 | -0.300 | -0.128 | 0.500 |
| High Compromise Culture | -16.067 | -0.268 | 0.020 | -0.087 | -0.312 | -0.139 | 0.500 |
| Low Lobbying Pressure | -15.993 | -0.267 | 0.020 | -0.068 | -0.303 | -0.131 | 0.500 |
| High Lobbying Pressure | -15.733 | -0.262 | 0.016 | -0.043 | -0.306 | -0.132 | 0.500 |
| Weak Constituency Pressure | -18.187 | -0.303 | 0.019 | -0.070 | -0.332 | -0.139 | 0.500 |
| Two-Party System | -6.860 | -0.114 | -0.004 | -0.016 | -0.159 | -0.084 | 0.333 |
| Multi-Party System | -31.813 | -0.530 | 0.098 | -0.294 | -0.565 | -0.343 | 0.814 |
| High Proposal Pressure | 3.307 | 0.018 | -0.016 | 0.015 | -0.037 | -0.063 | 0.167 |
| Extreme Proposal Pressure | 23.247 | 0.077 | -0.020 | 0.023 | 0.022 | -0.052 | 0.100 |
| Lobby-Fueled Flooding | 2.513 | 0.014 | -0.012 | 0.016 | -0.040 | -0.064 | 0.166 |
| Low-Compromise Flooding | 3.313 | 0.018 | -0.016 | 0.022 | -0.050 | -0.080 | 0.167 |

## Proposal-Cost Deltas

Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.

| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -21.167 | -29.420 | -0.353 | -0.017 | 0.039 | -0.081 | 0.447 |
| Low Polarization | -33.767 | -41.040 | -0.563 | -0.015 | 0.041 | -0.182 | 0.369 |
| High Polarization | -19.047 | -27.493 | -0.317 | -0.015 | 0.031 | -0.049 | 0.491 |
| Low Party Loyalty | -20.920 | -28.660 | -0.349 | -0.018 | 0.035 | -0.085 | 0.426 |
| High Party Loyalty | -20.740 | -29.360 | -0.346 | -0.018 | 0.039 | -0.080 | 0.436 |
| Low Compromise Culture | -19.580 | -28.280 | -0.326 | -0.016 | 0.025 | -0.068 | 0.417 |
| High Compromise Culture | -22.327 | -29.440 | -0.372 | -0.015 | 0.047 | -0.089 | 0.458 |
| Low Lobbying Pressure | -22.093 | -30.233 | -0.368 | -0.019 | 0.044 | -0.089 | 0.463 |
| High Lobbying Pressure | -19.127 | -27.580 | -0.319 | -0.017 | 0.039 | -0.064 | 0.403 |
| Weak Constituency Pressure | -22.567 | -29.487 | -0.376 | -0.016 | 0.034 | -0.083 | 0.458 |
| Two-Party System | -20.653 | -28.793 | -0.344 | -0.015 | 0.040 | -0.078 | 0.430 |
| Multi-Party System | -21.393 | -28.660 | -0.357 | -0.012 | 0.039 | -0.084 | 0.441 |
| High Proposal Pressure | -61.700 | -86.567 | -0.343 | -0.019 | 0.040 | -0.068 | 0.448 |
| Extreme Proposal Pressure | -102.393 | -143.547 | -0.341 | -0.015 | 0.038 | -0.071 | 0.437 |
| Lobby-Fueled Flooding | -58.960 | -83.287 | -0.328 | -0.013 | 0.021 | -0.068 | 0.413 |
| Low-Compromise Flooding | -58.107 | -85.040 | -0.323 | -0.014 | 0.025 | -0.059 | 0.467 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.651 | 0.151 | -0.246 | -0.634 | -0.447 |
| Low Polarization | -0.420 | 0.083 | -0.222 | -0.278 | -0.136 |
| High Polarization | -0.713 | 0.168 | -0.216 | -0.742 | -0.573 |
| Low Party Loyalty | -0.639 | 0.141 | -0.246 | -0.625 | -0.442 |
| High Party Loyalty | -0.648 | 0.143 | -0.237 | -0.631 | -0.447 |
| Low Compromise Culture | -0.650 | 0.146 | -0.208 | -0.627 | -0.441 |
| High Compromise Culture | -0.647 | 0.139 | -0.255 | -0.636 | -0.435 |
| Low Lobbying Pressure | -0.648 | 0.147 | -0.245 | -0.634 | -0.453 |
| High Lobbying Pressure | -0.645 | 0.126 | -0.248 | -0.634 | -0.437 |
| Weak Constituency Pressure | -0.677 | 0.135 | -0.191 | -0.638 | -0.429 |
| Two-Party System | -0.649 | 0.142 | -0.243 | -0.639 | -0.450 |
| Multi-Party System | -0.652 | 0.152 | -0.252 | -0.638 | -0.442 |
| High Proposal Pressure | -0.649 | 0.145 | -0.239 | -0.638 | -0.448 |
| Extreme Proposal Pressure | -0.641 | 0.144 | -0.242 | -0.632 | -0.444 |
| Lobby-Fueled Flooding | -0.665 | 0.130 | -0.259 | -0.648 | -0.456 |
| Low-Compromise Flooding | -0.694 | 0.154 | -0.196 | -0.700 | -0.526 |

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
| High Proposal Pressure | Unicameral 60 percent passage (0.674) | Default pass + challenge vouchers (0.858) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.673) | Default pass + challenge vouchers (0.916) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Unicameral 60 percent passage (0.630) | Default pass + challenge vouchers + info (0.857) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.687) | Default pass + challenge vouchers + info (0.849) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Proposal-cost screens are useful for measuring flooding as institutional load: floor/run and enacted/run expose costs hidden by percentage-only metrics.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- The current cost screen reduces volume, but it also selects for proposals with high proposer value or positive lobby pressure; that makes cost design an object of study, not a solved safeguard.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- The next model extension should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms, because agenda screening is now the central default-pass tradeoff.

## Reproduction

```sh
make campaign
```
