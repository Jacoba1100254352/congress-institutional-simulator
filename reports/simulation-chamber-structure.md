# Chamber Structure Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 80
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 50
- experiment cases: 34

## Case Weights

Scenario averages in this campaign are weighted by the case likelihood column below.

| Case | Weight | Description |
| --- | ---: | --- |
| Baseline | 1.000 | Moderately polarized three-party legislature. |
| Low Polarization | 1.000 | Legislators are less ideologically clustered. |
| High Polarization | 1.000 | Legislators are tightly clustered into ideological camps. |
| Low Party Loyalty | 1.000 | Party pressure is weak and legislators act more independently. |
| High Party Loyalty | 1.000 | Party pressure is strong. |
| Low Compromise Culture | 1.000 | Members are less inclined toward moderate, incremental bills. |
| High Compromise Culture | 1.000 | Members are more inclined toward moderate, incremental bills. |
| Low Lobbying Pressure | 1.000 | Lobby pressure is weak. |
| High Lobbying Pressure | 1.000 | Lobby pressure is strong. |
| Weak Constituency Pressure | 1.000 | Members are less responsive to public support. |
| Two-Party System | 1.000 | Generated legislators sort into two broad parties. |
| Multi-Party System | 1.000 | Generated legislators sort into five parties. |
| High Proposal Pressure | 1.000 | Three times as many potential proposals reach the institutional system. |
| Extreme Proposal Pressure | 1.000 | Five times as many potential proposals reach the institutional system. |
| Lobby-Fueled Flooding | 1.000 | High proposal pressure with strong lobbying and weaker constituency pressure. |
| Low-Compromise Flooding | 1.000 | High proposal pressure in a low-compromise legislature. |
| Capture Crisis | 1.000 | High lobbying, weak constituency pressure, low compromise, and high proposal pressure. |
| Popular Anti-Lobbying Push | 1.000 | High lobbying pressure with stronger public responsiveness and more appetite for reform. |
| Weighted Two-Party Baseline | 0.250 | Classic two-party legislature with ideological left/right sorting. |
| Weighted Two Major Plus Minors | 0.400 | Five-party legislature with two large ideological parties and smaller minor parties. |
| Weighted Fragmented Multiparty | 0.200 | Seven-party legislature with more even fragmentation across the ideological range. |
| Weighted Dominant-Party Legislature | 0.150 | Four-party legislature with one large center-weighted party and smaller opposition parties. |
| Era 1 Low Contention | 1.000 | Stylized low-contention legislature with several parties, high compromise culture, lower lobbying, and stronger constituency responsiveness. |
| Era 2 Normal Contention | 1.000 | Stylized ordinary-contention legislature with two major parties plus minors and moderate party loyalty. |
| Era 3 Polarizing | 1.000 | Stylized rising-contention legislature with stronger ideological clustering, party loyalty, and lobbying pressure. |
| Era 4 High Contention | 1.000 | Stylized high-contention legislature with more proposal pressure, higher polarization, and weaker compromise culture. |
| Era 5 Capture Contention | 1.000 | Stylized capture-contention legislature with two-party sorting, higher proposal pressure, strong lobbying, and lower public responsiveness. |
| Era 6 Crisis | 1.000 | Stylized crisis-contention legislature with severe polarization, high party loyalty, intense lobbying, weak constituency responsiveness, and doubled proposal pressure. |
| Adversarial High-Benefit Extreme Reform | 1.000 | Extreme proposals can have high generated public benefit but lower initial support and high uncertainty. |
| Adversarial Popular Harmful Bill | 1.000 | Popular proposals can have low generated public benefit, private upside, and concentrated harm. |
| Adversarial Moderate Capture | 1.000 | Moderate-looking proposals can have low public benefit and high organized-interest capture. |
| Adversarial Delayed-Benefit Reform | 1.000 | Beneficial reforms can have low immediate support because benefits are delayed and uncertain. |
| Adversarial Concentrated Rights Harm | 1.000 | Proposals can be broadly supported while imposing severe concentrated rights-like harm. |
| Adversarial Anti-Lobbying Backlash | 1.000 | Anti-lobbying reforms are more common, but face stronger defensive lobbying and lower observed support. |

## Headline Findings

- This focused campaign does not include the open default-pass baseline, so relative headline deltas are reported in the diagnostic sections below.
- Highest average welfare in this campaign came from Committee amendment and revision power at 0.695.
- Highest productivity came from Appointment and retention eligibility filter at 0.362, while highest compromise came from Stylized U.S.-like conventional benchmark at 0.364.
- Highest directional score, where lower-better risk metrics are inverted, came from Appointment and retention eligibility filter at 0.671.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral mixed appointed upper chamber | 0.660 | 0.580 | 0.867 | 0.930 | 0.264 | 19.572 | 83.919 | 0.616 | 0.000 | 0.162 | 0.070 | 0.134 | 0.543 | 0.077 | 0.238 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.498 | 0.000 | 1.000 |
| Appointment and retention eligibility filter | 0.671 | 0.558 | 0.836 | 0.930 | 0.362 | 27.778 | 83.919 | 0.586 | 0.000 | 0.250 | 0.070 | 0.150 | 0.505 | 0.132 | 0.308 | 0.263 | 0.000 | 0.000 | 0.000 | 0.000 | 0.630 | 0.000 | 1.000 |
| Bicameral House majority + upper cloture | 0.647 | 0.606 | 0.886 | 0.930 | 0.166 | 11.972 | 83.919 | 0.634 | 0.000 | 0.120 | 0.070 | 0.125 | 0.577 | 0.038 | 0.183 | 0.280 | 0.000 | 0.000 | 0.000 | 0.000 | 0.310 | 0.000 | 1.000 |
| Majority + forced-balanced committee | 0.660 | 0.579 | 0.870 | 0.943 | 0.248 | 18.398 | 26.052 | 0.621 | 0.000 | 0.152 | 0.057 | 0.141 | 0.522 | 0.070 | 0.230 | 0.284 | 0.000 | 0.000 | 0.000 | 0.000 | 0.456 | 0.000 | 0.340 |
| Bicameral simple majority | 0.656 | 0.583 | 0.870 | 0.930 | 0.243 | 17.878 | 83.919 | 0.617 | 0.000 | 0.159 | 0.070 | 0.133 | 0.547 | 0.067 | 0.219 | 0.272 | 0.000 | 0.000 | 0.000 | 0.000 | 0.451 | 0.000 | 1.000 |
| Bicameral incongruence: district House + PR upper house | 0.659 | 0.576 | 0.864 | 0.930 | 0.266 | 19.782 | 83.919 | 0.613 | 0.000 | 0.169 | 0.070 | 0.135 | 0.539 | 0.080 | 0.245 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.496 | 0.000 | 1.000 |
| Committee amendment and revision power | 0.647 | 0.614 | 0.927 | 0.929 | 0.118 | 9.397 | 11.913 | 0.695 | 0.000 | 0.013 | 0.071 | 0.094 | 0.591 | 0.032 | 0.209 | 0.177 | 0.000 | 0.000 | 0.126 | 0.033 | 0.433 | 0.000 | 0.147 |
| Committee deadline + discharge petition | 0.656 | 0.592 | 0.895 | 0.918 | 0.219 | 16.808 | 28.873 | 0.641 | 0.000 | 0.051 | 0.082 | 0.106 | 0.568 | 0.071 | 0.249 | 0.238 | 0.000 | 0.000 | 0.176 | 0.065 | 0.521 | 0.000 | 0.366 |
| Committee discharge-petition target | 0.648 | 0.609 | 0.922 | 0.925 | 0.139 | 10.979 | 13.887 | 0.669 | 0.000 | 0.044 | 0.075 | 0.082 | 0.588 | 0.038 | 0.212 | 0.200 | 0.000 | 0.000 | 0.155 | 0.048 | 0.416 | 0.000 | 0.173 |
| Committee fast-track certifier | 0.653 | 0.582 | 0.895 | 0.875 | 0.259 | 20.356 | 39.102 | 0.621 | 0.000 | 0.090 | 0.125 | 0.086 | 0.548 | 0.087 | 0.269 | 0.236 | 0.000 | 0.000 | 0.468 | 0.200 | 0.579 | 0.000 | 0.485 |
| Legal and drafting-quality committee | 0.656 | 0.600 | 0.915 | 0.913 | 0.196 | 15.587 | 20.567 | 0.645 | 0.000 | 0.046 | 0.087 | 0.082 | 0.574 | 0.057 | 0.234 | 0.229 | 0.000 | 0.000 | 0.228 | 0.086 | 0.502 | 0.000 | 0.255 |
| Committee minority-hearing rights | 0.649 | 0.606 | 0.915 | 0.928 | 0.145 | 11.342 | 15.528 | 0.677 | 0.000 | 0.024 | 0.072 | 0.100 | 0.586 | 0.043 | 0.228 | 0.209 | 0.000 | 0.000 | 0.129 | 0.037 | 0.441 | 0.000 | 0.194 |
| Committee priority queue | 0.653 | 0.595 | 0.905 | 0.917 | 0.194 | 15.270 | 22.368 | 0.641 | 0.000 | 0.067 | 0.083 | 0.092 | 0.569 | 0.060 | 0.240 | 0.233 | 0.000 | 0.000 | 0.194 | 0.068 | 0.479 | 0.000 | 0.279 |
| Public-accounts committee | 0.652 | 0.608 | 0.923 | 0.918 | 0.159 | 12.843 | 16.266 | 0.662 | 0.000 | 0.046 | 0.082 | 0.060 | 0.592 | 0.045 | 0.221 | 0.211 | 0.000 | 0.000 | 0.199 | 0.071 | 0.450 | 0.000 | 0.199 |
| Committee-first regular order | 0.666 | 0.588 | 0.884 | 0.967 | 0.227 | 16.781 | 21.469 | 0.633 | 0.000 | 0.101 | 0.033 | 0.133 | 0.536 | 0.059 | 0.208 | 0.272 | 0.000 | 0.000 | 0.000 | 0.000 | 0.449 | 0.000 | 0.283 |
| Committee scrutiny and audit | 0.650 | 0.609 | 0.923 | 0.922 | 0.148 | 11.810 | 14.733 | 0.667 | 0.000 | 0.037 | 0.078 | 0.077 | 0.590 | 0.040 | 0.217 | 0.207 | 0.000 | 0.000 | 0.174 | 0.058 | 0.438 | 0.000 | 0.182 |
| Committee veto player | 0.636 | 0.588 | 0.938 | 0.935 | 0.084 | 6.749 | 7.800 | 0.685 | 0.000 | 0.017 | 0.065 | 0.068 | 0.586 | 0.021 | 0.197 | 0.128 | 0.000 | 0.000 | 0.092 | 0.022 | 0.342 | 0.000 | 0.096 |
| Bicameral malapportioned upper chamber + conference | 0.667 | 0.560 | 0.842 | 0.906 | 0.361 | 27.459 | 83.919 | 0.587 | 0.024 | 0.187 | 0.094 | 0.144 | 0.519 | 0.118 | 0.289 | 0.273 | 0.000 | 0.000 | 0.172 | 0.000 | 0.634 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.652 | 0.642 | 0.924 | 0.984 | 0.056 | 4.195 | 18.516 | 0.682 | 0.000 | 0.009 | 0.016 | 0.087 | 0.663 | 0.012 | 0.162 | 0.217 | 0.000 | 0.000 | 0.000 | 0.000 | 0.170 | 0.000 | 0.222 |
| Expertise eligibility filter | 0.669 | 0.560 | 0.842 | 0.930 | 0.343 | 26.416 | 83.919 | 0.592 | 0.000 | 0.236 | 0.070 | 0.147 | 0.509 | 0.120 | 0.293 | 0.263 | 0.000 | 0.000 | 0.000 | 0.000 | 0.620 | 0.000 | 1.000 |
| Emergency lower-house fast path | 0.662 | 0.576 | 0.863 | 0.930 | 0.279 | 20.734 | 83.919 | 0.614 | 0.000 | 0.173 | 0.070 | 0.135 | 0.537 | 0.083 | 0.240 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.518 | 0.000 | 1.000 |
| Equal-population unicameral chamber | 0.669 | 0.560 | 0.845 | 0.930 | 0.340 | 25.776 | 83.919 | 0.599 | 0.000 | 0.219 | 0.070 | 0.143 | 0.513 | 0.116 | 0.288 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.620 | 0.000 | 1.000 |
| Ex ante advisory review | 0.670 | 0.563 | 0.845 | 0.930 | 0.341 | 25.825 | 83.919 | 0.616 | 0.000 | 0.220 | 0.070 | 0.143 | 0.512 | 0.117 | 0.289 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.618 | 0.000 | 1.000 |
| Mandatory ex ante legal clearance | 0.669 | 0.563 | 0.853 | 0.936 | 0.326 | 24.839 | 77.090 | 0.607 | 0.000 | 0.213 | 0.064 | 0.134 | 0.519 | 0.110 | 0.281 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.584 | 0.000 | 0.920 |
| Majority + expertise-qualified lottery committee | 0.660 | 0.580 | 0.872 | 0.943 | 0.244 | 18.117 | 27.211 | 0.623 | 0.000 | 0.147 | 0.057 | 0.141 | 0.522 | 0.067 | 0.220 | 0.280 | 0.000 | 0.000 | 0.000 | 0.000 | 0.460 | 0.000 | 0.352 |
| House-origin-only bicameral routing | 0.664 | 0.572 | 0.858 | 0.922 | 0.302 | 22.613 | 83.919 | 0.606 | 0.003 | 0.174 | 0.078 | 0.137 | 0.533 | 0.091 | 0.249 | 0.271 | 0.000 | 0.000 | 0.054 | 0.000 | 0.560 | 0.000 | 1.000 |
| Independent fiscal/electoral/audit insulation bundle | 0.670 | 0.564 | 0.845 | 0.930 | 0.340 | 25.814 | 83.919 | 0.620 | 0.000 | 0.222 | 0.070 | 0.144 | 0.512 | 0.116 | 0.282 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.616 | 0.000 | 1.000 |
| Bicameral joint-sitting fallback | 0.664 | 0.569 | 0.853 | 0.930 | 0.304 | 22.853 | 83.919 | 0.608 | 0.026 | 0.189 | 0.070 | 0.138 | 0.527 | 0.096 | 0.260 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.564 | 0.000 | 1.000 |
| Last-offer bicameral bargaining | 0.665 | 0.572 | 0.857 | 0.923 | 0.306 | 22.891 | 83.919 | 0.606 | 0.006 | 0.175 | 0.077 | 0.138 | 0.533 | 0.092 | 0.248 | 0.270 | 0.000 | 0.000 | 0.051 | 0.000 | 0.562 | 0.000 | 1.000 |
| Leadership-routed chamber origin | 0.659 | 0.577 | 0.864 | 0.930 | 0.267 | 19.836 | 83.919 | 0.614 | 0.000 | 0.171 | 0.070 | 0.135 | 0.539 | 0.080 | 0.242 | 0.270 | 0.000 | 0.000 | 0.000 | 0.000 | 0.499 | 0.000 | 1.000 |
| Bicameral limited navette | 0.665 | 0.569 | 0.855 | 0.923 | 0.315 | 23.634 | 83.919 | 0.602 | 0.011 | 0.179 | 0.077 | 0.138 | 0.529 | 0.095 | 0.251 | 0.269 | 0.000 | 0.000 | 0.053 | 0.000 | 0.580 | 0.000 | 1.000 |
| Majority + random-lottery committee | 0.659 | 0.580 | 0.872 | 0.943 | 0.241 | 17.820 | 27.335 | 0.619 | 0.000 | 0.149 | 0.057 | 0.141 | 0.523 | 0.065 | 0.218 | 0.286 | 0.000 | 0.000 | 0.000 | 0.000 | 0.446 | 0.000 | 0.352 |
| Lower-house override after bicameral disagreement | 0.662 | 0.575 | 0.862 | 0.930 | 0.279 | 20.799 | 83.919 | 0.613 | 0.000 | 0.175 | 0.070 | 0.136 | 0.536 | 0.084 | 0.245 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.521 | 0.000 | 1.000 |
| Bicameral malapportioned territorial upper chamber | 0.660 | 0.577 | 0.864 | 0.930 | 0.269 | 19.942 | 83.919 | 0.613 | 0.000 | 0.171 | 0.070 | 0.135 | 0.539 | 0.080 | 0.243 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.499 | 0.000 | 1.000 |
| Mediation committee bicameral conflict | 0.666 | 0.569 | 0.857 | 0.922 | 0.315 | 23.590 | 83.919 | 0.603 | 0.008 | 0.157 | 0.078 | 0.139 | 0.535 | 0.095 | 0.252 | 0.269 | 0.000 | 0.000 | 0.059 | 0.000 | 0.577 | 0.000 | 1.000 |
| Majority + minority-veto committee seat | 0.660 | 0.578 | 0.869 | 0.943 | 0.249 | 18.486 | 26.341 | 0.620 | 0.000 | 0.150 | 0.057 | 0.143 | 0.521 | 0.071 | 0.231 | 0.284 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 0.343 |
| Majority + mixed legislator-citizen committee | 0.648 | 0.605 | 0.919 | 0.923 | 0.145 | 11.517 | 15.061 | 0.661 | 0.000 | 0.052 | 0.077 | 0.079 | 0.586 | 0.040 | 0.219 | 0.209 | 0.000 | 0.000 | 0.167 | 0.053 | 0.414 | 0.000 | 0.186 |
| Majority + opposition-chaired scrutiny committee | 0.660 | 0.578 | 0.869 | 0.943 | 0.252 | 18.684 | 26.216 | 0.620 | 0.000 | 0.152 | 0.057 | 0.142 | 0.521 | 0.073 | 0.237 | 0.282 | 0.000 | 0.000 | 0.000 | 0.000 | 0.466 | 0.000 | 0.342 |
| Principles resolution before second-chamber drafting | 0.664 | 0.566 | 0.855 | 0.921 | 0.312 | 23.417 | 83.919 | 0.599 | 0.008 | 0.163 | 0.079 | 0.142 | 0.530 | 0.097 | 0.266 | 0.270 | 0.000 | 0.000 | 0.066 | 0.000 | 0.558 | 0.000 | 1.000 |
| Proportional lower-house majority | 0.668 | 0.559 | 0.845 | 0.930 | 0.340 | 25.773 | 83.919 | 0.598 | 0.000 | 0.222 | 0.070 | 0.144 | 0.512 | 0.116 | 0.287 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.616 | 0.000 | 1.000 |
| Proposer-chamber origin routing | 0.665 | 0.568 | 0.854 | 0.921 | 0.317 | 23.892 | 83.919 | 0.598 | 0.017 | 0.180 | 0.079 | 0.140 | 0.527 | 0.097 | 0.259 | 0.269 | 0.000 | 0.000 | 0.065 | 0.000 | 0.579 | 0.000 | 1.000 |
| Recusal and cooling-off eligibility filter | 0.671 | 0.559 | 0.837 | 0.930 | 0.357 | 27.479 | 83.919 | 0.587 | 0.000 | 0.250 | 0.070 | 0.150 | 0.506 | 0.130 | 0.307 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.626 | 0.000 | 1.000 |
| Bicameral upper revision council | 0.664 | 0.571 | 0.858 | 0.923 | 0.304 | 22.749 | 83.919 | 0.606 | 0.003 | 0.173 | 0.077 | 0.137 | 0.532 | 0.092 | 0.248 | 0.270 | 0.000 | 0.000 | 0.053 | 0.000 | 0.561 | 0.000 | 1.000 |
| Second-chamber preclearance routing | 0.664 | 0.569 | 0.855 | 0.930 | 0.301 | 22.589 | 83.919 | 0.608 | 0.021 | 0.188 | 0.070 | 0.138 | 0.528 | 0.095 | 0.259 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.565 | 0.000 | 1.000 |
| Senate-origin-only bicameral routing | 0.662 | 0.570 | 0.856 | 0.921 | 0.299 | 22.425 | 83.919 | 0.604 | 0.005 | 0.179 | 0.079 | 0.139 | 0.530 | 0.093 | 0.260 | 0.272 | 0.000 | 0.000 | 0.062 | 0.000 | 0.543 | 0.000 | 1.000 |
| Unicameral simple majority | 0.669 | 0.559 | 0.845 | 0.930 | 0.340 | 25.774 | 83.919 | 0.598 | 0.000 | 0.219 | 0.070 | 0.144 | 0.513 | 0.116 | 0.287 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.616 | 0.000 | 1.000 |
| Bicameral upper suspensive veto | 0.662 | 0.576 | 0.864 | 0.930 | 0.279 | 20.733 | 83.919 | 0.613 | 0.000 | 0.167 | 0.070 | 0.135 | 0.537 | 0.083 | 0.243 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.521 | 0.000 | 1.000 |
| Upper-house absolute veto | 0.648 | 0.607 | 0.887 | 0.930 | 0.166 | 11.962 | 83.919 | 0.633 | 0.000 | 0.116 | 0.070 | 0.126 | 0.575 | 0.038 | 0.182 | 0.282 | 0.000 | 0.000 | 0.000 | 0.000 | 0.307 | 0.000 | 1.000 |
| Upper-house amendment-only power | 0.664 | 0.570 | 0.857 | 0.922 | 0.307 | 22.932 | 83.919 | 0.606 | 0.009 | 0.177 | 0.078 | 0.138 | 0.531 | 0.094 | 0.252 | 0.269 | 0.000 | 0.000 | 0.060 | 0.000 | 0.564 | 0.000 | 1.000 |
| Upper-house territorial veto threshold | 0.655 | 0.604 | 0.885 | 0.930 | 0.200 | 14.484 | 83.919 | 0.635 | 0.000 | 0.110 | 0.070 | 0.124 | 0.572 | 0.046 | 0.177 | 0.276 | 0.000 | 0.000 | 0.000 | 0.000 | 0.376 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, compromises less, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Compromise | Gridlock | Weak public mandate | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.050 | 0.363 | 0.950 | 0.008 | 0.668 |
| Baseline | Unicameral simple majority | 0.272 | 0.219 | 0.728 | 0.192 | 0.637 |
| Baseline | Committee-first regular order | 0.149 | 0.285 | 0.851 | 0.076 | 0.655 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.166 | 0.379 | 0.834 | 0.010 | 0.605 |
| Low Polarization | Unicameral simple majority | 0.520 | 0.279 | 0.480 | 0.185 | 0.493 |
| Low Polarization | Committee-first regular order | 0.391 | 0.310 | 0.609 | 0.091 | 0.530 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.024 | 0.346 | 0.976 | 0.000 | 0.684 |
| High Polarization | Unicameral simple majority | 0.179 | 0.222 | 0.821 | 0.169 | 0.678 |
| High Polarization | Committee-first regular order | 0.094 | 0.277 | 0.906 | 0.062 | 0.682 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.048 | 0.352 | 0.952 | 0.004 | 0.671 |
| Low Party Loyalty | Unicameral simple majority | 0.292 | 0.212 | 0.708 | 0.186 | 0.628 |
| Low Party Loyalty | Committee-first regular order | 0.170 | 0.269 | 0.830 | 0.100 | 0.654 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.051 | 0.378 | 0.949 | 0.008 | 0.663 |
| High Party Loyalty | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.193 | 0.635 |
| High Party Loyalty | Committee-first regular order | 0.164 | 0.281 | 0.836 | 0.093 | 0.652 |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark | 0.033 | 0.388 | 0.967 | 0.006 | 0.668 |
| Low Compromise Culture | Unicameral simple majority | 0.213 | 0.242 | 0.788 | 0.140 | 0.649 |
| Low Compromise Culture | Committee-first regular order | 0.126 | 0.291 | 0.874 | 0.074 | 0.664 |
| High Compromise Culture | Stylized U.S.-like conventional benchmark | 0.073 | 0.382 | 0.927 | 0.011 | 0.651 |
| High Compromise Culture | Unicameral simple majority | 0.337 | 0.220 | 0.663 | 0.215 | 0.608 |
| High Compromise Culture | Committee-first regular order | 0.202 | 0.276 | 0.798 | 0.111 | 0.638 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.063 | 0.380 | 0.937 | 0.007 | 0.656 |
| Low Lobbying Pressure | Unicameral simple majority | 0.279 | 0.230 | 0.721 | 0.191 | 0.630 |
| Low Lobbying Pressure | Committee-first regular order | 0.180 | 0.284 | 0.820 | 0.096 | 0.644 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.030 | 0.368 | 0.970 | 0.000 | 0.675 |
| High Lobbying Pressure | Unicameral simple majority | 0.236 | 0.234 | 0.764 | 0.208 | 0.653 |
| High Lobbying Pressure | Committee-first regular order | 0.138 | 0.268 | 0.862 | 0.102 | 0.671 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.026 | 0.386 | 0.974 | 0.008 | 0.673 |
| Weak Constituency Pressure | Unicameral simple majority | 0.238 | 0.233 | 0.762 | 0.253 | 0.662 |
| Weak Constituency Pressure | Committee-first regular order | 0.127 | 0.284 | 0.873 | 0.133 | 0.678 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.051 | 0.366 | 0.949 | 0.008 | 0.666 |
| Two-Party System | Unicameral simple majority | 0.270 | 0.229 | 0.730 | 0.182 | 0.633 |
| Two-Party System | Committee-first regular order | 0.163 | 0.284 | 0.837 | 0.077 | 0.648 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.056 | 0.352 | 0.944 | 0.011 | 0.668 |
| Multi-Party System | Unicameral simple majority | 0.284 | 0.223 | 0.716 | 0.191 | 0.629 |
| Multi-Party System | Committee-first regular order | 0.177 | 0.276 | 0.823 | 0.084 | 0.645 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.047 | 0.373 | 0.953 | 0.007 | 0.666 |
| High Proposal Pressure | Unicameral simple majority | 0.263 | 0.236 | 0.737 | 0.190 | 0.636 |
| High Proposal Pressure | Committee-first regular order | 0.163 | 0.288 | 0.837 | 0.089 | 0.650 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.373 | 0.951 | 0.008 | 0.665 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.263 | 0.233 | 0.737 | 0.184 | 0.635 |
| Extreme Proposal Pressure | Committee-first regular order | 0.156 | 0.283 | 0.844 | 0.084 | 0.654 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.023 | 0.371 | 0.977 | 0.000 | 0.677 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.236 | 0.777 | 0.220 | 0.662 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.130 | 0.262 | 0.870 | 0.087 | 0.674 |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.373 | 0.980 | 0.011 | 0.680 |
| Low-Compromise Flooding | Unicameral simple majority | 0.161 | 0.250 | 0.839 | 0.148 | 0.674 |
| Low-Compromise Flooding | Committee-first regular order | 0.093 | 0.287 | 0.907 | 0.077 | 0.683 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.015 | 0.368 | 0.985 | 0.005 | 0.683 |
| Capture Crisis | Unicameral simple majority | 0.180 | 0.226 | 0.820 | 0.232 | 0.688 |
| Capture Crisis | Committee-first regular order | 0.100 | 0.259 | 0.900 | 0.091 | 0.690 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.072 | 0.378 | 0.928 | 0.004 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.347 | 0.238 | 0.653 | 0.196 | 0.595 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.223 | 0.286 | 0.777 | 0.081 | 0.619 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.052 | 0.380 | 0.948 | 0.004 | 0.661 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.254 | 0.240 | 0.746 | 0.162 | 0.633 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.157 | 0.289 | 0.843 | 0.080 | 0.651 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.048 | 0.369 | 0.953 | 0.000 | 0.665 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.273 | 0.221 | 0.728 | 0.205 | 0.638 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.160 | 0.280 | 0.840 | 0.110 | 0.658 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.074 | 0.356 | 0.926 | 0.003 | 0.657 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.312 | 0.238 | 0.688 | 0.194 | 0.611 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.208 | 0.289 | 0.792 | 0.080 | 0.625 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.051 | 0.382 | 0.949 | 0.000 | 0.660 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.282 | 0.244 | 0.718 | 0.174 | 0.621 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.177 | 0.283 | 0.823 | 0.076 | 0.642 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.182 | 0.382 | 0.818 | 0.010 | 0.597 |
| Era 1 Low Contention | Unicameral simple majority | 0.515 | 0.259 | 0.485 | 0.203 | 0.505 |
| Era 1 Low Contention | Committee-first regular order | 0.382 | 0.301 | 0.618 | 0.105 | 0.540 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.114 | 0.384 | 0.886 | 0.011 | 0.630 |
| Era 2 Normal Contention | Unicameral simple majority | 0.405 | 0.251 | 0.595 | 0.220 | 0.566 |
| Era 2 Normal Contention | Committee-first regular order | 0.278 | 0.300 | 0.722 | 0.088 | 0.589 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.061 | 0.376 | 0.939 | 0.010 | 0.659 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.234 | 0.693 | 0.178 | 0.612 |
| Era 3 Polarizing | Committee-first regular order | 0.199 | 0.275 | 0.801 | 0.107 | 0.640 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.030 | 0.371 | 0.970 | 0.017 | 0.677 |
| Era 4 High Contention | Unicameral simple majority | 0.217 | 0.236 | 0.783 | 0.176 | 0.656 |
| Era 4 High Contention | Committee-first regular order | 0.124 | 0.284 | 0.876 | 0.077 | 0.668 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.357 | 0.984 | 0.000 | 0.685 |
| Era 5 Capture Contention | Unicameral simple majority | 0.162 | 0.224 | 0.838 | 0.209 | 0.694 |
| Era 5 Capture Contention | Committee-first regular order | 0.087 | 0.264 | 0.913 | 0.091 | 0.696 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.009 | 0.318 | 0.991 | 0.000 | 0.700 |
| Era 6 Crisis | Unicameral simple majority | 0.119 | 0.226 | 0.881 | 0.241 | 0.721 |
| Era 6 Crisis | Committee-first regular order | 0.060 | 0.256 | 0.940 | 0.089 | 0.711 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.042 | 1.000 | 0.000 | 0.787 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.054 | 0.100 | 0.946 | 0.326 | 0.808 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.013 | 0.127 | 0.987 | 0.032 | 0.762 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.205 | 0.402 | 0.795 | 0.002 | 0.577 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.870 | 0.292 | 0.130 | 0.010 | 0.280 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.622 | 0.323 | 0.378 | 0.062 | 0.404 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.060 | 0.546 | 0.940 | 0.003 | 0.607 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.974 | 0.495 | 0.026 | 0.286 | 0.222 |
| Adversarial Moderate Capture | Committee-first regular order | 0.830 | 0.499 | 0.170 | 0.274 | 0.290 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.003 | 0.311 | 0.997 | 0.067 | 0.718 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.184 | 0.258 | 0.816 | 0.608 | 0.752 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.140 | 0.277 | 0.860 | 0.077 | 0.662 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.047 | 0.385 | 0.953 | 0.013 | 0.664 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.495 | 0.256 | 0.505 | 0.121 | 0.500 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.259 | 0.298 | 0.741 | 0.122 | 0.606 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.044 | 0.362 | 0.956 | 0.029 | 0.675 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.327 | 0.278 | 0.673 | 0.290 | 0.611 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.191 | 0.295 | 0.809 | 0.190 | 0.654 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest weak public-mandate passage |
| --- | --- | --- | --- |
| Baseline | Committee veto player (0.762) | Bicameral malapportioned upper chamber + conference (0.289) | Committee veto player (0.004) |
| Low Polarization | Committee veto player (0.751) | Bicameral malapportioned upper chamber + conference (0.545) | Committee amendment and revision power (0.005) |
| High Polarization | Committee veto player (0.784) | Recusal and cooling-off eligibility filter (0.209) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Committee veto player (0.772) | Bicameral malapportioned upper chamber + conference (0.311) | Committee veto player (0.002) |
| High Party Loyalty | Committee veto player (0.769) | Bicameral malapportioned upper chamber + conference (0.296) | Committee amendment and revision power (0.008) |
| Low Compromise Culture | Committee veto player (0.774) | Appointment and retention eligibility filter (0.248) | Committee minority-hearing rights (0.004) |
| High Compromise Culture | Committee veto player (0.755) | Bicameral malapportioned upper chamber + conference (0.370) | Committee veto player (0.004) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.758) | Bicameral malapportioned upper chamber + conference (0.301) | Committee amendment and revision power (0.004) |
| High Lobbying Pressure | Committee veto player (0.777) | Recusal and cooling-off eligibility filter (0.262) | Stylized U.S.-like conventional benchmark (0.000) |
| Weak Constituency Pressure | Committee veto player (0.753) | Expertise eligibility filter (0.271) | Committee amendment and revision power (0.008) |
| Two-Party System | Committee veto player (0.762) | Bicameral malapportioned upper chamber + conference (0.304) | Committee amendment and revision power (0.005) |
| Multi-Party System | Committee veto player (0.756) | Bicameral malapportioned upper chamber + conference (0.302) | Committee amendment and revision power (0.008) |
| High Proposal Pressure | Committee veto player (0.768) | Bicameral malapportioned upper chamber + conference (0.292) | Committee veto player (0.006) |
| Extreme Proposal Pressure | Committee veto player (0.764) | Bicameral malapportioned upper chamber + conference (0.290) | Committee amendment and revision power (0.006) |
| Lobby-Fueled Flooding | Committee veto player (0.766) | Appointment and retention eligibility filter (0.256) | Stylized U.S.-like conventional benchmark (0.000) |
| Low-Compromise Flooding | Committee veto player (0.773) | Recusal and cooling-off eligibility filter (0.209) | Committee amendment and revision power (0.007) |
| Capture Crisis | Committee veto player (0.744) | Expertise eligibility filter (0.223) | Stylized U.S.-like conventional benchmark (0.005) |
| Popular Anti-Lobbying Push | Committee veto player (0.787) | Bicameral malapportioned upper chamber + conference (0.378) | Stylized U.S.-like conventional benchmark (0.004) |
| Weighted Two-Party Baseline | Committee veto player (0.770) | Bicameral malapportioned upper chamber + conference (0.289) | Stylized U.S.-like conventional benchmark (0.004) |
| Weighted Two Major Plus Minors | Committee veto player (0.764) | Recusal and cooling-off eligibility filter (0.293) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Committee veto player (0.757) | Bicameral malapportioned upper chamber + conference (0.345) | Stylized U.S.-like conventional benchmark (0.003) |
| Weighted Dominant-Party Legislature | Committee veto player (0.768) | Appointment and retention eligibility filter (0.312) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 1 Low Contention | Committee veto player (0.737) | Bicameral malapportioned upper chamber + conference (0.543) | Committee veto player (0.005) |
| Era 2 Normal Contention | Committee veto player (0.760) | Bicameral malapportioned upper chamber + conference (0.441) | Committee veto player (0.005) |
| Era 3 Polarizing | Committee veto player (0.769) | Bicameral malapportioned upper chamber + conference (0.339) | Committee amendment and revision power (0.005) |
| Era 4 High Contention | Committee veto player (0.783) | Recusal and cooling-off eligibility filter (0.258) | Committee veto player (0.007) |
| Era 5 Capture Contention | Committee veto player (0.759) | Appointment and retention eligibility filter (0.199) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Committee veto player (0.762) | Expertise eligibility filter (0.166) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial High-Benefit Extreme Reform | Upper-house territorial veto threshold (0.807) | Committee fast-track certifier (0.188) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Public-accounts committee (0.408) | Bicameral malapportioned upper chamber + conference (0.931) | Committee amendment and revision power (0.000) |
| Adversarial Moderate Capture | Committee scrutiny and audit (0.529) | Bicameral malapportioned upper chamber + conference (0.983) | Committee minority-hearing rights (0.000) |
| Adversarial Delayed-Benefit Reform | Committee veto player (0.774) | Committee fast-track certifier (0.344) | Committee amendment and revision power (0.055) |
| Adversarial Concentrated Rights Harm | Committee amendment and revision power (0.546) | Bicameral malapportioned upper chamber + conference (0.541) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Anti-Lobbying Backlash | Committee veto player (0.725) | Appointment and retention eligibility filter (0.365) | Stylized U.S.-like conventional benchmark (0.009) |

## Interpretation

- Timeline scenarios are stylized stress paths, not historical calibration. They increase polarization, party loyalty, lobbying pressure, and proposal pressure while reducing compromise culture and constituency responsiveness.
- The timeline comparison should be read as a degradation test: institutions that preserve compromise and productivity under later-era assumptions are more robust than systems that only work in low-contention settings.

## Reproduction

```sh
make campaign
```
