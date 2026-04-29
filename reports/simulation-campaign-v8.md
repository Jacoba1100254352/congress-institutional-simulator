# Simulation Campaign v8

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 17
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.842 productivity, versus 0.264 for simple majority.
- Open default-pass also averaged 0.451 low-support passage and 0.664 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.233 and reduced policy shift by 0.591, while changing productivity by -0.622.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.171, and changed low-support passage by -0.056 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.590, floor consideration by -0.745, and low-support passage by -0.210 relative to open default-pass.
- Adaptive tracks changed productivity by -0.402, low-support passage by -0.187, and policy shift by -0.449 relative to open default-pass.
- Sunset trial review changed productivity by -0.373, welfare by 0.122, and policy shift by -0.400 relative to open default-pass.
- Earned proposal credits denied 0.203 of potential proposals, changed welfare by 0.017, and changed proposer gain by -0.033 relative to open default-pass.
- The anti-capture bundle changed lobby capture by -0.090, anti-lobbying reform passage by -0.037, and private-gain ratio by -0.193 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.709.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Capture | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.173 | 16.791 | 103.333 | 0.667 | 0.000 | 0.053 | 0.229 | 0.234 | 0.467 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.842 | 86.880 | 103.333 | 0.496 | 0.451 | 0.664 | 0.656 | 0.266 | 0.993 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.440 | 44.662 | 95.107 | 0.605 | 0.264 | 0.215 | 0.393 | 0.204 | 0.906 | 0.000 | 0.925 |
| Default pass + anti-capture bundle | 0.748 | 76.446 | 97.824 | 0.519 | 0.444 | 0.584 | 0.650 | 0.176 | 0.956 | 0.000 | 0.952 |
| Default pass + challenge vouchers | 0.671 | 78.007 | 103.333 | 0.510 | 0.394 | 0.456 | 0.541 | 0.257 | 0.891 | 0.398 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.252 | 24.573 | 24.871 | 0.687 | 0.241 | 0.080 | 0.235 | 0.158 | 0.809 | 0.000 | 0.255 |
| Default pass + earned proposal credits | 0.674 | 64.576 | 76.299 | 0.513 | 0.442 | 0.508 | 0.623 | 0.249 | 0.860 | 0.000 | 0.797 |
| Default pass + informed guarded committee | 0.220 | 21.886 | 22.037 | 0.651 | 0.218 | 0.073 | 0.251 | 0.226 | 0.572 | 0.000 | 0.221 |
| Default pass + anti-capture audit | 0.748 | 76.252 | 103.231 | 0.510 | 0.453 | 0.584 | 0.648 | 0.213 | 0.993 | 0.000 | 0.999 |
| Default pass + lobby firewall | 0.820 | 84.678 | 103.333 | 0.503 | 0.447 | 0.650 | 0.660 | 0.258 | 0.996 | 0.000 | 1.000 |
| Default pass + lobby transparency | 0.837 | 86.425 | 103.333 | 0.498 | 0.454 | 0.660 | 0.657 | 0.202 | 0.997 | 0.000 | 1.000 |
| Default pass + public-interest screen | 0.749 | 76.219 | 90.900 | 0.517 | 0.448 | 0.581 | 0.645 | 0.214 | 0.936 | 0.000 | 0.891 |
| Default pass + sunset trial | 0.469 | 47.476 | 103.333 | 0.618 | 0.374 | 0.265 | 0.459 | 0.173 | 0.969 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.111 | 10.740 | 103.333 | 0.682 | 0.000 | 0.031 | 0.212 | 0.237 | 0.300 | 0.000 | 1.000 |
| Unicameral simple majority | 0.264 | 26.111 | 103.333 | 0.637 | 0.000 | 0.102 | 0.309 | 0.233 | 0.650 | 0.000 | 1.000 |
| Unicameral majority + lobby firewall | 0.278 | 27.669 | 103.333 | 0.649 | 0.000 | 0.110 | 0.316 | 0.200 | 0.755 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.090 | 8.444 | 103.333 | 0.709 | 0.000 | 0.019 | 0.146 | 0.245 | 0.253 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.500 | -0.258 | 0.023 | -0.080 | -0.304 | -0.151 | 0.500 |
| Low Polarization | -11.027 | -0.184 | 0.029 | -0.136 | -0.139 | -0.064 | 0.499 |
| High Polarization | -17.440 | -0.291 | 0.020 | -0.057 | -0.366 | -0.165 | 0.500 |
| Low Party Loyalty | -15.347 | -0.256 | 0.024 | -0.079 | -0.295 | -0.139 | 0.499 |
| High Party Loyalty | -15.340 | -0.256 | 0.022 | -0.062 | -0.292 | -0.137 | 0.500 |
| Low Compromise Culture | -15.133 | -0.252 | 0.019 | -0.046 | -0.288 | -0.134 | 0.500 |
| High Compromise Culture | -14.887 | -0.248 | 0.024 | -0.091 | -0.287 | -0.132 | 0.500 |
| Low Lobbying Pressure | -15.587 | -0.260 | 0.021 | -0.063 | -0.290 | -0.125 | 0.500 |
| High Lobbying Pressure | -15.833 | -0.264 | 0.024 | -0.062 | -0.299 | -0.141 | 0.500 |
| Weak Constituency Pressure | -17.987 | -0.300 | 0.022 | -0.075 | -0.322 | -0.135 | 0.500 |
| Two-Party System | -6.627 | -0.110 | -0.004 | -0.015 | -0.142 | -0.077 | 0.333 |
| Multi-Party System | -30.713 | -0.512 | 0.117 | -0.312 | -0.541 | -0.337 | 0.812 |
| High Proposal Pressure | 3.447 | 0.019 | -0.017 | 0.013 | -0.030 | -0.056 | 0.167 |
| Extreme Proposal Pressure | 22.607 | 0.075 | -0.023 | 0.020 | 0.026 | -0.044 | 0.100 |
| Lobby-Fueled Flooding | 2.820 | 0.016 | -0.016 | 0.009 | -0.032 | -0.057 | 0.166 |
| Low-Compromise Flooding | 3.313 | 0.018 | -0.018 | 0.021 | -0.045 | -0.074 | 0.167 |
| Capture Crisis | 1.400 | 0.008 | -0.013 | 0.010 | -0.044 | -0.062 | 0.166 |
| Popular Anti-Lobbying Push | -1.873 | -0.016 | -0.012 | -0.007 | -0.053 | -0.053 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.590 | -0.745 | 0.745 | -0.210 | -0.584 | -0.422 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.402 | -0.075 | 0.074 | 0.001 | -0.187 | -0.449 | -0.263 | 0.000 |

## Sunset Trial Deltas

Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + sunset trial | -0.373 | 0.122 | -0.077 | -0.400 | -0.197 | 0.000 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.167 | -0.203 | 0.203 | 0.017 | -0.009 | -0.156 | -0.033 | 0.000 |

## Anti-Capture Deltas

Delta values compare anti-capture mechanisms against open `default-pass` across all cases. Negative capture and private-gain-ratio deltas are desirable; anti-lobby pass is the share of generated anti-lobbying reform bills enacted.

| Scenario | Productivity delta | Welfare delta | Capture delta | Public-alignment delta | Anti-lobby pass delta | Private-gain-ratio delta | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + lobby firewall | -0.022 | 0.007 | -0.008 | 0.011 | 0.003 | -0.033 | -0.003 |
| Default pass + lobby transparency | -0.004 | 0.002 | -0.063 | -0.005 | 0.005 | -0.027 | 0.003 |
| Default pass + public-interest screen | -0.093 | 0.021 | -0.052 | 0.002 | -0.057 | -0.202 | -0.002 |
| Default pass + anti-capture audit | -0.094 | 0.014 | -0.053 | 0.002 | 0.001 | -0.172 | 0.003 |
| Default pass + anti-capture bundle | -0.094 | 0.022 | -0.090 | 0.010 | -0.037 | -0.193 | -0.007 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.627 | 0.163 | -0.247 | -0.607 | -0.417 |
| Low Polarization | -0.421 | 0.089 | -0.216 | -0.263 | -0.119 |
| High Polarization | -0.696 | 0.195 | -0.218 | -0.736 | -0.558 |
| Low Party Loyalty | -0.618 | 0.168 | -0.269 | -0.600 | -0.412 |
| High Party Loyalty | -0.618 | 0.154 | -0.237 | -0.591 | -0.406 |
| Low Compromise Culture | -0.624 | 0.161 | -0.217 | -0.596 | -0.410 |
| High Compromise Culture | -0.612 | 0.161 | -0.273 | -0.600 | -0.412 |
| Low Lobbying Pressure | -0.631 | 0.159 | -0.243 | -0.606 | -0.419 |
| High Lobbying Pressure | -0.628 | 0.144 | -0.216 | -0.590 | -0.403 |
| Weak Constituency Pressure | -0.672 | 0.151 | -0.193 | -0.623 | -0.401 |
| Two-Party System | -0.618 | 0.156 | -0.249 | -0.596 | -0.416 |
| Multi-Party System | -0.618 | 0.162 | -0.268 | -0.605 | -0.423 |
| High Proposal Pressure | -0.624 | 0.165 | -0.252 | -0.603 | -0.417 |
| Extreme Proposal Pressure | -0.621 | 0.161 | -0.253 | -0.600 | -0.415 |
| Lobby-Fueled Flooding | -0.650 | 0.145 | -0.198 | -0.601 | -0.404 |
| Low-Compromise Flooding | -0.678 | 0.179 | -0.190 | -0.675 | -0.492 |
| Capture Crisis | -0.682 | 0.144 | -0.183 | -0.646 | -0.437 |
| Popular Anti-Lobbying Push | -0.553 | 0.134 | -0.270 | -0.506 | -0.334 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.712) | Default pass unless 2/3 block (0.840) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.702) | Default pass unless 2/3 block (0.841) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.745) | Default pass unless 2/3 block (0.846) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.726) | Default pass unless 2/3 block (0.843) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.718) | Default pass unless 2/3 block (0.841) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.745) | Default pass unless 2/3 block (0.820) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.716) | Default pass unless 2/3 block (0.851) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.720) | Default pass + anti-capture audit (0.842) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.701) | Default pass unless 2/3 block (0.844) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Unicameral 60 percent passage (0.696) | Default pass unless 2/3 block (0.870) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.729) | Default pass unless 2/3 block (0.840) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.723) | Default pass unless 2/3 block (0.845) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.723) | Default pass + challenge vouchers (0.861) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.715) | Default pass + challenge vouchers (0.916) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.715) | Default pass + challenge vouchers (0.858) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.731) | Default pass + challenge vouchers (0.852) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.742) | Default pass + challenge vouchers (0.854) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.695) | Default pass unless 2/3 block (0.823) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Anti-capture scenarios test whether lobbying pressure can be reduced through vote firewalls, transparency, public-interest screens, audit sanctions, or combined safeguards.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Anti-capture mechanisms test lobbying as institutional pressure: anti-lobbying bills now face organized opposition, while high-private-gain bills create measurable capture risk.
- The next model extension should make lobbying groups explicit actors with budgets, issue targets, defensive spending against anti-lobbying bills, and separate channels for money, information, litigation threat, and public campaigns.

## Reproduction

```sh
make campaign
```
