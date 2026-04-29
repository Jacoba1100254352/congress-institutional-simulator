# Simulation Campaign v14

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 150
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 26
- experiment cases: 18

## Headline Findings

- Open default-pass averaged 0.843 productivity, versus 0.265 for simple majority.
- Open default-pass also averaged 0.451 low-support passage and 0.665 policy shift.
- Informed guarded default-pass reduced low-support passage by 0.233 and reduced policy shift by 0.592, while changing productivity by -0.620.
- Challenge vouchers averaged 0.398 challenge use, changed productivity by -0.172, and changed low-support passage by -0.058 relative to open default-pass.
- Cross-bloc cosponsorship changed productivity by -0.590, floor consideration by -0.744, and low-support passage by -0.209 relative to open default-pass.
- Adaptive tracks changed productivity by -0.400, low-support passage by -0.185, and policy shift by -0.449 relative to open default-pass.
- The anti-capture bundle changed lobby capture by -0.090, anti-lobbying reform passage by -0.035, and private-gain ratio by -0.193 relative to open default-pass.
- Budgeted lobbying spent 0.103 per potential bill, with 0.627 of spend aimed defensively at anti-lobbying reform bills.
- The channel anti-capture bundle changed public benefit per lobby dollar by 0.420 and anti-lobbying reform passage by 0.008 relative to budgeted lobbying.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.661, and status-quo wins averaged 0.451 relative to open default-pass.
- Mediated default-pass amended 0.828 of potential bills and changed compromise by 0.028 relative to open default-pass.
- Best average welfare in this campaign came from Unicameral 60 percent passage at 0.709.

## Scenario Averages Across Cases

| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Minority harm | Legitimacy | Policy shift | Proposer gain | Capture | Lobby spend | Defensive spend | Amend rate | Compensation | Anti-lobby pass | Challenge | Floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.174 | 16.940 | 103.333 | 0.665 | 0.000 | 0.077 | 0.593 | 0.053 | 0.230 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.460 | 0.000 | 1.000 |
| Default pass unless 2/3 block | 0.843 | 86.911 | 103.333 | 0.497 | 0.451 | 0.168 | 0.392 | 0.665 | 0.657 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks | 0.443 | 44.900 | 95.124 | 0.605 | 0.266 | 0.102 | 0.515 | 0.216 | 0.392 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.902 | 0.000 | 0.927 |
| Default pass + affected-group consent | 0.769 | 78.974 | 92.268 | 0.509 | 0.440 | 0.122 | 0.426 | 0.584 | 0.632 | 0.250 | 0.000 | 0.000 | 0.000 | 0.152 | 0.991 | 0.000 | 0.896 |
| Default pass + public-benefit alternatives | 0.943 | 97.150 | 98.288 | 0.552 | 0.196 | 0.079 | 0.513 | 0.008 | 0.005 | 0.242 | 0.000 | 0.000 | 0.946 | 0.000 | 0.999 | 0.000 | 0.953 |
| Default pass + median-seeking alternatives | 0.943 | 97.187 | 98.291 | 0.552 | 0.195 | 0.079 | 0.513 | 0.004 | 0.002 | 0.242 | 0.000 | 0.000 | 0.953 | 0.000 | 0.999 | 0.000 | 0.953 |
| Default pass + pairwise policy tournament | 0.549 | 56.344 | 56.349 | 0.641 | 0.042 | 0.046 | 0.645 | 0.004 | 0.004 | 0.202 | 0.000 | 0.000 | 0.549 | 0.000 | 0.941 | 0.000 | 0.549 |
| Default pass + anti-capture bundle | 0.750 | 76.584 | 97.869 | 0.518 | 0.444 | 0.151 | 0.409 | 0.586 | 0.650 | 0.176 | 0.000 | 0.000 | 0.000 | 0.000 | 0.957 | 0.000 | 0.953 |
| Default pass + blind sponsor/lobby review | 0.843 | 86.930 | 103.333 | 0.496 | 0.451 | 0.168 | 0.391 | 0.665 | 0.656 | 0.267 | 0.109 | 0.627 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Default pass + budgeted lobbying | 0.842 | 86.901 | 103.333 | 0.496 | 0.452 | 0.168 | 0.391 | 0.664 | 0.656 | 0.267 | 0.103 | 0.627 | 0.000 | 0.000 | 0.990 | 0.000 | 1.000 |
| Default pass + budgeted lobbying + anti-capture bundle | 0.749 | 76.556 | 97.777 | 0.518 | 0.443 | 0.151 | 0.409 | 0.585 | 0.650 | 0.176 | 0.103 | 0.627 | 0.000 | 0.000 | 0.955 | 0.000 | 0.952 |
| Default pass + budgeted lobbying + transparency | 0.838 | 86.448 | 103.333 | 0.498 | 0.453 | 0.166 | 0.385 | 0.662 | 0.658 | 0.201 | 0.103 | 0.627 | 0.000 | 0.000 | 0.998 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.671 | 77.976 | 103.333 | 0.510 | 0.393 | 0.161 | 0.401 | 0.456 | 0.540 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.886 | 0.398 | 1.000 |
| Default pass + compensation amendments | 0.843 | 86.967 | 103.333 | 0.490 | 0.450 | 0.123 | 0.411 | 0.665 | 0.656 | 0.266 | 0.000 | 0.000 | 0.000 | 0.143 | 0.991 | 0.000 | 1.000 |
| Default pass + cross-bloc cosponsors | 0.253 | 24.705 | 24.987 | 0.687 | 0.242 | 0.069 | 0.565 | 0.080 | 0.235 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 | 0.805 | 0.000 | 0.256 |
| Default pass + defensive lobbying cap | 0.842 | 86.893 | 103.333 | 0.496 | 0.450 | 0.168 | 0.391 | 0.665 | 0.657 | 0.267 | 0.074 | 0.381 | 0.000 | 0.000 | 0.989 | 0.000 | 1.000 |
| Default pass + democracy vouchers | 0.827 | 85.379 | 103.333 | 0.503 | 0.447 | 0.164 | 0.397 | 0.654 | 0.658 | 0.242 | 0.109 | 0.627 | 0.000 | 0.000 | 0.996 | 0.000 | 1.000 |
| Default pass + informed guarded committee | 0.222 | 22.113 | 22.254 | 0.651 | 0.218 | 0.087 | 0.551 | 0.074 | 0.249 | 0.227 | 0.000 | 0.000 | 0.000 | 0.000 | 0.576 | 0.000 | 0.223 |
| Default pass + law registry | 0.868 | 89.687 | 103.333 | 0.492 | 0.397 | 0.171 | 0.391 | 0.834 | 0.600 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + channel anti-capture bundle | 0.837 | 86.312 | 103.333 | 0.514 | 0.432 | 0.165 | 0.412 | 0.660 | 0.657 | 0.229 | 0.094 | 0.541 | 0.000 | 0.000 | 0.998 | 0.000 | 1.000 |
| Default pass + mediated amendments | 0.897 | 92.273 | 103.333 | 0.492 | 0.458 | 0.132 | 0.403 | 0.499 | 0.509 | 0.269 | 0.000 | 0.000 | 0.828 | 0.152 | 0.991 | 0.000 | 1.000 |
| Default pass + equal-access public advocate | 0.833 | 85.991 | 103.333 | 0.515 | 0.430 | 0.164 | 0.416 | 0.660 | 0.658 | 0.237 | 0.109 | 0.627 | 0.000 | 0.000 | 0.997 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.112 | 10.920 | 103.333 | 0.683 | 0.000 | 0.070 | 0.617 | 0.031 | 0.208 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.304 | 0.000 | 1.000 |
| Unicameral simple majority | 0.265 | 26.289 | 103.333 | 0.637 | 0.000 | 0.090 | 0.554 | 0.101 | 0.305 | 0.234 | 0.000 | 0.000 | 0.000 | 0.000 | 0.646 | 0.000 | 1.000 |
| Unicameral majority + lobby firewall | 0.279 | 27.774 | 103.333 | 0.647 | 0.000 | 0.082 | 0.568 | 0.110 | 0.316 | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 | 0.748 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.091 | 8.652 | 103.333 | 0.709 | 0.000 | 0.060 | 0.653 | 0.020 | 0.148 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 | 0.258 | 0.000 | 1.000 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.573 | -0.260 | 0.021 | -0.076 | -0.291 | -0.132 | 0.500 |
| Low Polarization | -11.527 | -0.192 | 0.029 | -0.149 | -0.144 | -0.064 | 0.499 |
| High Polarization | -17.027 | -0.284 | 0.016 | -0.039 | -0.357 | -0.165 | 0.500 |
| Low Party Loyalty | -15.593 | -0.260 | 0.026 | -0.089 | -0.299 | -0.131 | 0.499 |
| High Party Loyalty | -15.860 | -0.264 | 0.022 | -0.070 | -0.297 | -0.137 | 0.500 |
| Low Compromise Culture | -15.940 | -0.266 | 0.019 | -0.055 | -0.302 | -0.139 | 0.500 |
| High Compromise Culture | -14.767 | -0.246 | 0.024 | -0.093 | -0.296 | -0.147 | 0.500 |
| Low Lobbying Pressure | -16.247 | -0.271 | 0.024 | -0.081 | -0.320 | -0.148 | 0.500 |
| High Lobbying Pressure | -15.273 | -0.255 | 0.020 | -0.068 | -0.291 | -0.142 | 0.500 |
| Weak Constituency Pressure | -17.907 | -0.298 | 0.024 | -0.071 | -0.320 | -0.137 | 0.500 |
| Two-Party System | -6.447 | -0.107 | -0.002 | -0.027 | -0.148 | -0.086 | 0.333 |
| Multi-Party System | -31.033 | -0.517 | 0.117 | -0.307 | -0.542 | -0.338 | 0.811 |
| High Proposal Pressure | 3.047 | 0.017 | -0.017 | 0.014 | -0.032 | -0.057 | 0.167 |
| Extreme Proposal Pressure | 22.880 | 0.076 | -0.022 | 0.022 | 0.027 | -0.043 | 0.100 |
| Lobby-Fueled Flooding | 3.300 | 0.018 | -0.017 | 0.011 | -0.028 | -0.056 | 0.166 |
| Low-Compromise Flooding | 3.607 | 0.020 | -0.017 | 0.024 | -0.044 | -0.075 | 0.167 |
| Capture Crisis | 0.900 | 0.005 | -0.014 | 0.018 | -0.044 | -0.060 | 0.166 |
| Popular Anti-Lobbying Push | -1.367 | -0.011 | -0.015 | -0.006 | -0.047 | -0.051 | 0.250 |

## Cross-Bloc Cosponsorship Deltas

Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.

| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + cross-bloc cosponsors | -0.590 | -0.744 | 0.744 | -0.209 | -0.585 | -0.422 | 0.000 |

## Adaptive Track Deltas

Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.

| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + adaptive tracks | -0.400 | -0.073 | 0.073 | 0.001 | -0.185 | -0.449 | -0.265 | 0.000 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.026 | -0.005 | 0.462 | 5.124 | 0.585 | 0.045 | 0.169 |

## Anti-Capture Deltas

Delta values compare anti-capture mechanisms against open `default-pass` across all cases. Negative capture and private-gain-ratio deltas are desirable; anti-lobby pass is the share of generated anti-lobbying reform bills enacted.

| Scenario | Productivity delta | Welfare delta | Capture delta | Public-alignment delta | Anti-lobby pass delta | Private-gain-ratio delta | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + anti-capture bundle | -0.093 | 0.022 | -0.090 | 0.010 | -0.035 | -0.193 | -0.007 |

## Budgeted Lobbying Deltas

Delta values compare explicit budgeted lobbying scenarios against open `default-pass` across all cases. Lobby spend is normalized per potential bill; defensive spend is the share of lobbying spend aimed at anti-lobbying reform bills.

| Scenario | Productivity delta | Welfare delta | Capture delta | Lobby spend/bill | Defensive spend share | Capture return/spend | Anti-lobby pass delta | Public-distortion delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + budgeted lobbying | -0.000 | -0.001 | 0.001 | 0.103 | 0.627 | 2.420 | -0.002 | -0.000 |
| Default pass + budgeted lobbying + transparency | -0.005 | 0.001 | -0.064 | 0.103 | 0.627 | 1.843 | 0.006 | 0.006 |
| Default pass + budgeted lobbying + anti-capture bundle | -0.093 | 0.021 | -0.089 | 0.103 | 0.627 | 1.477 | -0.037 | -0.010 |

## Lobbying-Channel Deltas

Delta values compare channel-specific lobbying safeguards against explicit budgeted lobbying. Spend-share columns show where lobby budgets are going after each scenario's constraints.

| Scenario | Productivity delta | Welfare delta | Capture delta | Public-benefit/lobby dollar | Anti-lobby pass delta | Direct | Agenda | Info | Public | Litigation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + democracy vouchers | -0.015 | 0.007 | -0.025 | 4.387 | 0.007 | 0.209 | 0.202 | 0.197 | 0.201 | 0.191 |
| Default pass + equal-access public advocate | -0.009 | 0.020 | -0.030 | 4.534 | 0.007 | 0.209 | 0.202 | 0.197 | 0.201 | 0.191 |
| Default pass + blind sponsor/lobby review | 0.000 | -0.000 | -0.000 | 4.409 | -0.001 | 0.209 | 0.202 | 0.197 | 0.201 | 0.191 |
| Default pass + defensive lobbying cap | -0.000 | 0.000 | 0.000 | 6.083 | -0.000 | 0.210 | 0.202 | 0.197 | 0.202 | 0.190 |
| Default pass + channel anti-capture bundle | -0.006 | 0.018 | -0.038 | 5.065 | 0.008 | 0.209 | 0.202 | 0.197 | 0.201 | 0.191 |

## Mediation Deltas

Delta values compare structured amendment mediation against the matching non-mediated scenario. Amendment rate is the share of potential bills whose policy position moved before final voting.

| Scenario | Baseline | Productivity delta | Welfare delta | Compromise delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Amendment rate | Amendment movement |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + mediated amendments | Default pass unless 2/3 block | 0.054 | -0.005 | 0.028 | 0.007 | -0.167 | -0.148 | 0.828 | 0.162 |

## Distributional-Harm Deltas

Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.

| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + compensation amendments | 0.001 | -0.007 | -0.045 | 0.019 | 0.935 | 0.143 | -0.001 |
| Default pass + affected-group consent | -0.074 | 0.013 | -0.046 | 0.035 | 0.936 | 0.152 | -0.010 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + public-benefit alternatives | 0.100 | 0.055 | -0.254 | -0.658 | -0.652 | 0.003 | 0.005 | 6.000 | 0.047 |
| Default pass + median-seeking alternatives | 0.101 | 0.055 | -0.256 | -0.662 | -0.655 | 0.000 | 0.002 | 6.000 | 0.047 |
| Default pass + pairwise policy tournament | -0.293 | 0.144 | -0.409 | -0.661 | -0.653 | 0.001 | 0.002 | 6.000 | 0.451 |

## Default-Pass Guardrail Deltas

Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.

| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | -0.620 | 0.162 | -0.248 | -0.598 | -0.413 |
| Low Polarization | -0.410 | 0.089 | -0.219 | -0.260 | -0.118 |
| High Polarization | -0.692 | 0.187 | -0.207 | -0.722 | -0.550 |
| Low Party Loyalty | -0.610 | 0.157 | -0.261 | -0.610 | -0.423 |
| High Party Loyalty | -0.623 | 0.162 | -0.257 | -0.595 | -0.407 |
| Low Compromise Culture | -0.638 | 0.162 | -0.222 | -0.603 | -0.410 |
| High Compromise Culture | -0.614 | 0.161 | -0.254 | -0.606 | -0.420 |
| Low Lobbying Pressure | -0.634 | 0.159 | -0.240 | -0.632 | -0.444 |
| High Lobbying Pressure | -0.628 | 0.141 | -0.225 | -0.588 | -0.404 |
| Weak Constituency Pressure | -0.673 | 0.155 | -0.191 | -0.617 | -0.403 |
| Two-Party System | -0.622 | 0.163 | -0.255 | -0.593 | -0.405 |
| Multi-Party System | -0.615 | 0.162 | -0.261 | -0.600 | -0.418 |
| High Proposal Pressure | -0.629 | 0.163 | -0.245 | -0.608 | -0.421 |
| Extreme Proposal Pressure | -0.618 | 0.158 | -0.249 | -0.599 | -0.418 |
| Lobby-Fueled Flooding | -0.644 | 0.137 | -0.209 | -0.592 | -0.403 |
| Low-Compromise Flooding | -0.671 | 0.178 | -0.195 | -0.675 | -0.500 |
| Capture Crisis | -0.681 | 0.144 | -0.181 | -0.647 | -0.444 |
| Popular Anti-Lobbying Push | -0.549 | 0.134 | -0.275 | -0.504 | -0.339 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Unicameral 60 percent passage (0.729) | Default pass + public-benefit alternatives (0.947) | Unicameral simple majority (0.000) |
| Low Polarization | Default pass + pairwise policy tournament (0.702) | Default pass + median-seeking alternatives (0.973) | Unicameral simple majority (0.000) |
| High Polarization | Unicameral 60 percent passage (0.739) | Default pass + median-seeking alternatives (0.934) | Unicameral simple majority (0.000) |
| Low Party Loyalty | Unicameral 60 percent passage (0.720) | Default pass + public-benefit alternatives (0.951) | Unicameral simple majority (0.000) |
| High Party Loyalty | Unicameral 60 percent passage (0.717) | Default pass + median-seeking alternatives (0.949) | Unicameral simple majority (0.000) |
| Low Compromise Culture | Unicameral 60 percent passage (0.746) | Default pass + median-seeking alternatives (0.938) | Unicameral simple majority (0.000) |
| High Compromise Culture | Unicameral 60 percent passage (0.702) | Default pass + public-benefit alternatives (0.953) | Unicameral simple majority (0.000) |
| Low Lobbying Pressure | Unicameral 60 percent passage (0.722) | Default pass + median-seeking alternatives (0.956) | Unicameral simple majority (0.000) |
| High Lobbying Pressure | Default pass + cross-bloc cosponsors (0.707) | Default pass + median-seeking alternatives (0.929) | Unicameral simple majority (0.000) |
| Weak Constituency Pressure | Unicameral 60 percent passage (0.695) | Default pass + median-seeking alternatives (0.954) | Unicameral simple majority (0.000) |
| Two-Party System | Default pass + cross-bloc cosponsors (0.721) | Default pass + public-benefit alternatives (0.947) | Unicameral simple majority (0.000) |
| Multi-Party System | Unicameral 60 percent passage (0.720) | Default pass + public-benefit alternatives (0.946) | Unicameral simple majority (0.000) |
| High Proposal Pressure | Unicameral 60 percent passage (0.720) | Default pass + median-seeking alternatives (0.948) | Unicameral simple majority (0.000) |
| Extreme Proposal Pressure | Unicameral 60 percent passage (0.718) | Default pass + median-seeking alternatives (0.949) | Unicameral simple majority (0.000) |
| Lobby-Fueled Flooding | Default pass + cross-bloc cosponsors (0.711) | Default pass + median-seeking alternatives (0.927) | Unicameral simple majority (0.000) |
| Low-Compromise Flooding | Unicameral 60 percent passage (0.736) | Default pass + public-benefit alternatives (0.929) | Unicameral simple majority (0.000) |
| Capture Crisis | Default pass + cross-bloc cosponsors (0.739) | Default pass + median-seeking alternatives (0.920) | Unicameral simple majority (0.000) |
| Popular Anti-Lobbying Push | Unicameral 60 percent passage (0.693) | Default pass + public-benefit alternatives (0.933) | Unicameral simple majority (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Anti-capture scenarios test whether lobbying pressure can be reduced through vote firewalls, transparency, public-interest screens, audit sanctions, or combined safeguards.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Lobbying-depth scenarios split organized-interest influence into direct pressure, agenda access, information distortion, public campaigns, litigation threats, and defensive spending against reform.
- The next model extension should add deliberative citizen review, because the simulator now has richer organized-interest pressure but still lacks an independent public legitimacy screen.

## Reproduction

```sh
make campaign
```
