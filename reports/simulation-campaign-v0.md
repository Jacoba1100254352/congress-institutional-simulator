# Simulation Campaign v0

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- bills per run: 60
- base seed: 20260428
- scenarios per case: 9
- experiment cases: 12

## Headline Findings

- Open default-pass averaged 0.841 productivity, versus 0.255 for simple majority.
- Open default-pass also averaged 0.451 low-support passage and 0.680 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.234 and reduced policy shift by 0.613, while changing productivity by -0.637.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.673.

## Scenario Averages Across Cases

| Scenario | Productivity | Welfare | Low-support | Policy shift | Proposer gain | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.167 | 0.623 | 0.000 | 0.052 | 0.237 | 1.000 |
| Default pass unless 2/3 block | 0.841 | 0.472 | 0.451 | 0.680 | 0.676 | 1.000 |
| Default pass + proposal access screen | 0.348 | 0.559 | 0.342 | 0.120 | 0.239 | 0.395 |
| Default pass + representative committee gate | 0.305 | 0.558 | 0.290 | 0.150 | 0.404 | 0.308 |
| Default pass + access + committee | 0.212 | 0.604 | 0.207 | 0.070 | 0.248 | 0.213 |
| Default pass + informed guarded committee | 0.205 | 0.611 | 0.217 | 0.067 | 0.248 | 0.206 |
| Bicameral majority + presidential veto | 0.107 | 0.645 | 0.000 | 0.031 | 0.219 | 1.000 |
| Unicameral simple majority | 0.255 | 0.594 | 0.000 | 0.102 | 0.321 | 1.000 |
| Unicameral 60 percent passage | 0.088 | 0.673 | 0.000 | 0.020 | 0.158 | 1.000 |

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

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- The next model extension should target proposal flooding and proposal costs, because this campaign makes proposal access and agenda screening central to the default-pass tradeoff.

## Reproduction

```sh
make campaign
```
