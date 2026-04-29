# Simulation Campaign v9

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 19
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.841 productivity, versus 0.265 for simple majority.
- Open default-pass also averaged 0.450 low-support passage and 0.662 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.233 and reduced policy shift by 0.589, while changing productivity by -0.620.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.171, and changed low-support passage by -0.056 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.588, floor consideration by -0.744, and low-support passage by -0.205 relative to open default-pass.
- Adaptive tracks changed productivity by -0.399, low-support passage by -0.186, and policy shift by -0.447 relative to open default-pass.
- Sunset trial review changed productivity by -0.372, welfare by 0.122, and policy shift by -0.398 relative to open default-pass.
- Earned proposal credits denied 0.203 of potential proposals, changed welfare by 0.016, and changed proposer gain by -0.031 relative to open default-pass.
- The anti-capture bundle changed lobby capture by -0.090, anti-lobbying reform passage by -0.035, and private-gain ratio by -0.194 relative to open default-pass.
- Budgeted lobbying spent 0.099 per potential bill, with 0.655 of spend aimed defensively at anti-lobbying reform bills.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.707.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.173 | 16.909 | 103.333 | 0.666 | 0.000 | 0.053 | 0.231 | 0.234 | 0.000 | 0.000 | 0.458 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.841 | 86.814 | 103.333 | 0.497 | 0.450 | 0.662 | 0.655 | 0.266 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.442 | 44.887 | 95.100 | 0.605 | 0.264 | 0.216 | 0.393 | 0.204 | 0.000 | 0.000 | 0.904 | 0.000 | 0.925 |
| Default pass + anti-capture bundle | 0.750 | 76.597 | 97.831 | 0.518 | 0.445 | 0.585 | 0.649 | 0.176 | 0.000 | 0.000 | 0.957 | 0.000 | 0.952 |
| Default pass + budgeted lobbying | 0.842 | 86.915 | 103.333 | 0.496 | 0.453 | 0.663 | 0.656 | 0.268 | 0.099 | 0.655 | 0.989 | 0.000 | 1.000 |
| Default pass + budgeted lobbying + anti-capture bundle | 0.748 | 76.501 | 97.787 | 0.519 | 0.444 | 0.584 | 0.649 | 0.176 | 0.099 | 0.655 | 0.957 | 0.000 | 0.951 |
| Default pass + budgeted lobbying + transparency | 0.836 | 86.310 | 103.333 | 0.498 | 0.454 | 0.659 | 0.657 | 0.201 | 0.099 | 0.655 | 0.997 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.670 | 77.968 | 103.333 | 0.509 | 0.394 | 0.455 | 0.539 | 0.257 | 0.000 | 0.000 | 0.889 | 0.398 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.696 | 25.001 | 0.687 | 0.245 | 0.080 | 0.236 | 0.157 | 0.000 | 0.000 | 0.811 | 0.000 | 0.256 |
| Default pass + earned proposal credits | 0.674 | 64.552 | 76.252 | 0.513 | 0.442 | 0.508 | 0.624 | 0.249 | 0.000 | 0.000 | 0.858 | 0.000 | 0.797 |
| Default pass + informed guarded committee | 0.221 | 22.067 | 22.201 | 0.651 | 0.217 | 0.073 | 0.250 | 0.227 | 0.000 | 0.000 | 0.574 | 0.000 | 0.222 |
| Default pass + anti-capture audit | 0.747 | 76.165 | 103.219 | 0.511 | 0.453 | 0.582 | 0.647 | 0.213 | 0.000 | 0.000 | 0.991 | 0.000 | 0.999 |
| Default pass + lobby transparency | 0.838 | 86.518 | 103.333 | 0.498 | 0.453 | 0.660 | 0.656 | 0.202 | 0.000 | 0.000 | 0.998 | 0.000 | 1.000 |
| Default pass + public-interest screen | 0.749 | 76.251 | 90.825 | 0.518 | 0.448 | 0.580 | 0.644 | 0.214 | 0.000 | 0.000 | 0.935 | 0.000 | 0.890 |
| Default pass + sunset trial | 0.469 | 47.595 | 103.333 | 0.618 | 0.374 | 0.265 | 0.460 | 0.173 | 0.000 | 0.000 | 0.968 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.112 | 10.838 | 103.333 | 0.685 | 0.000 | 0.031 | 0.209 | 0.236 | 0.000 | 0.000 | 0.304 | 0.000 | 1.000 |
| Unicameral simple majority | 0.265 | 26.189 | 103.333 | 0.637 | 0.000 | 0.102 | 0.307 | 0.234 | 0.000 | 0.000 | 0.646 | 0.000 | 1.000 |
| Unicameral majority + lobby firewall | 0.277 | 27.673 | 103.333 | 0.649 | 0.000 | 0.109 | 0.314 | 0.200 | 0.000 | 0.000 | 0.747 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.091 | 8.583 | 103.333 | 0.707 | 0.000 | 0.020 | 0.147 | 0.249 | 0.000 | 0.000 | 0.256 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.527 | -0.259 | 0.024 | -0.075 | -0.307 | -0.150 | 0.500 |
| Low Polarization | -11.393 | -0.190 | 0.029 | -0.143 | -0.148 | -0.067 | 0.499 |
| High Polarization | -17.333 | -0.289 | 0.016 | -0.030 | -0.356 | -0.165 | 0.500 |
| Low Party Loyalty | -15.400 | -0.257 | 0.022 | -0.086 | -0.291 | -0.135 | 0.499 |
| High Party Loyalty | -15.387 | -0.256 | 0.023 | -0.072 | -0.286 | -0.134 | 0.500 |
| Low Compromise Culture | -15.633 | -0.261 | 0.019 | -0.055 | -0.296 | -0.142 | 0.500 |
| High Compromise Culture | -14.880 | -0.248 | 0.021 | -0.087 | -0.292 | -0.135 | 0.500 |
| Low Lobbying Pressure | -15.520 | -0.259 | 0.020 | -0.077 | -0.298 | -0.143 | 0.500 |
| High Lobbying Pressure | -15.227 | -0.254 | 0.019 | -0.064 | -0.287 | -0.142 | 0.500 |
| Weak Constituency Pressure | -18.260 | -0.304 | 0.024 | -0.068 | -0.325 | -0.128 | 0.500 |
| Two-Party System | -6.660 | -0.111 | -0.004 | -0.016 | -0.151 | -0.083 | 0.333 |
| Multi-Party System | -30.560 | -0.509 | 0.119 | -0.302 | -0.534 | -0.321 | 0.811 |
| High Proposal Pressure | 3.580 | 0.020 | -0.017 | 0.013 | -0.028 | -0.055 | 0.167 |
| Extreme Proposal Pressure | 23.393 | 0.078 | -0.023 | 0.024 | 0.030 | -0.042 | 0.100 |
| Lobby-Fueled Flooding | 2.707 | 0.015 | -0.015 | 0.009 | -0.035 | -0.057 | 0.166 |
| Low-Compromise Flooding | 2.867 | 0.016 | -0.017 | 0.022 | -0.047 | -0.074 | 0.167 |
| Capture Crisis | 1.773 | 0.010 | -0.016 | 0.015 | -0.044 | -0.065 | 0.166 |
| Popular Anti-Lobbying Push | -1.773 | -0.015 | -0.013 | -0.010 | -0.046 | -0.047 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.588 | -0.744 | 0.744 | -0.205 | -0.582 | -0.419 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.399 | -0.075 | 0.074 | 0.001 | -0.186 | -0.447 | -0.262 | 0.000 |

## Sunset Trial Deltas

Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + sunset trial | -0.372 | 0.122 | -0.076 | -0.398 | -0.196 | 0.000 |

## Earned Proposal-Credit Deltas

Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.

| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + earned proposal credits | -0.167 | -0.203 | 0.203 | 0.016 | -0.008 | -0.154 | -0.031 | 0.000 |

## Anti-Capture Deltas

Delta values compare anti-capture mechanisms against open `default-pass` across all cases. Negative capture and private-gain-ratio deltas are desirable; anti-lobby pass is the share of generated anti-lobbying reform bills enacted.

| Scenario | Productivity delta | Welfare delta | Capture delta | Public-alignment delta | Anti-lobby pass delta | Private-gain-ratio delta | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + lobby transparency | -0.003 | 0.001 | -0.063 | -0.005 | 0.006 | -0.026 | 0.003 |
| Default pass + public-interest screen | -0.092 | 0.021 | -0.052 | 0.002 | -0.057 | -0.203 | -0.002 |
| Default pass + anti-capture audit | -0.094 | 0.014 | -0.052 | 0.002 | -0.001 | -0.173 | 0.003 |
| Default pass + anti-capture bundle | -0.091 | 0.022 | -0.090 | 0.010 | -0.035 | -0.194 | -0.005 |

## Budgeted Lobbying Deltas

Delta values compare explicit budgeted lobbying scenarios against open `default-pass` across all cases. Lobby spend is normalized per potential bill; defensive spend is the share of lobbying spend aimed at anti-lobbying reform bills.

| Scenario | Productivity delta | Welfare delta | Capture delta | Lobby spend/bill | Defensive spend share | Capture return/spend | Anti-lobby pass delta | Public-distortion delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + budgeted lobbying | 0.001 | -0.000 | 0.003 | 0.099 | 0.655 | 2.501 | -0.003 | -0.001 |
| Default pass + budgeted lobbying + transparency | -0.005 | 0.002 | -0.064 | 0.099 | 0.655 | 1.896 | 0.005 | 0.005 |
| Default pass + budgeted lobbying + anti-capture bundle | -0.093 | 0.022 | -0.089 | 0.099 | 0.655 | 1.522 | -0.035 | -0.011 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.623 | 0.164 | -0.237 | -0.606 | -0.417 |
| Low Polarization | -0.417 | 0.089 | -0.218 | -0.269 | -0.125 |
| High Polarization | -0.687 | 0.195 | -0.216 | -0.713 | -0.556 |
| Low Party Loyalty | -0.608 | 0.160 | -0.282 | -0.589 | -0.408 |
| High Party Loyalty | -0.624 | 0.161 | -0.249 | -0.588 | -0.410 |
| Low Compromise Culture | -0.631 | 0.158 | -0.214 | -0.594 | -0.408 |
| High Compromise Culture | -0.612 | 0.160 | -0.260 | -0.606 | -0.415 |
| Low Lobbying Pressure | -0.621 | 0.157 | -0.255 | -0.605 | -0.427 |
| High Lobbying Pressure | -0.629 | 0.141 | -0.222 | -0.582 | -0.397 |
| Weak Constituency Pressure | -0.678 | 0.155 | -0.201 | -0.629 | -0.401 |
| Two-Party System | -0.628 | 0.164 | -0.259 | -0.604 | -0.415 |
| Multi-Party System | -0.621 | 0.165 | -0.253 | -0.601 | -0.410 |
| High Proposal Pressure | -0.617 | 0.163 | -0.252 | -0.604 | -0.419 |
| Extreme Proposal Pressure | -0.616 | 0.159 | -0.248 | -0.592 | -0.408 |
| Lobby-Fueled Flooding | -0.651 | 0.143 | -0.200 | -0.602 | -0.401 |
| Low-Compromise Flooding | -0.673 | 0.172 | -0.183 | -0.673 | -0.498 |
| Capture Crisis | -0.682 | 0.148 | -0.182 | -0.646 | -0.440 |
| Popular Anti-Lobbying Push | -0.549 | 0.134 | -0.267 | -0.506 | -0.341 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.722) | Default pass + budgeted lobbying (0.848) | Unicameral simple majority (0.000) |
| Low Polarization | Unicameral 60 percent passage (0.701) | Default pass unless 2/3 block (0.847) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.731) | Default pass unless 2/3 block (0.841) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.715) | Default pass unless 2/3 block (0.840) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.711) | Default pass unless 2/3 block (0.839) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.731) | Default pass + budgeted lobbying (0.829) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.711) | Default pass + budgeted lobbying (0.851) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.719) | Default pass + budgeted lobbying (0.842) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.704) | Default pass unless 2/3 block (0.835) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Default pass + cross-bloc cosponsors (0.697) | Default pass unless 2/3 block (0.875) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.723) | Default pass unless 2/3 block (0.848) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.713) | Default pass + budgeted lobbying (0.841) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.727) | Default pass + challenge vouchers (0.861) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.717) | Default pass + challenge vouchers (0.917) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.719) | Default pass + challenge vouchers (0.858) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Default pass + cross-bloc cosponsors (0.730) | Default pass + challenge vouchers (0.850) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.745) | Default pass + challenge vouchers (0.854) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.691) | Default pass unless 2/3 block (0.825) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Anti-capture scenarios test whether lobbying pressure can be reduced through vote firewalls, transparency, public-interest screens, audit sanctions, or combined safeguards.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Budgeted lobbying scenarios make organized interests explicit actors with budgets, issue targets, and defensive spending against anti-lobbying reform.
- The next model extension should add structured amendment or mediation, because capture controls and agenda screens still rarely turn narrow bills into better compromises before the final yes/no choice.

## Reproduction

```sh
make campaign
```
