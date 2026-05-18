# Chamber Structure Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 80
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 51
- experiment cases: 37

## Case Weights

Scenario averages in this campaign are weighted by the case likelihood column below.

| Case | Weight | Description |
| --- | ---: | --- |
| Baseline | 1.000 | Moderately polarized three-party legislature. |
| Low Polarization | 1.000 | Legislators are less ideologically clustered. |
| High Polarization | 1.000 | Legislators are tightly clustered into ideological camps. |
| Low Party Loyalty | 1.000 | Party pressure is weak and legislators act more independently. |
| High Party Loyalty | 1.000 | Party pressure is strong. |
| Low Revision-Moderation Culture | 1.000 | Members are less inclined toward moderate, incremental bills. |
| High Revision-Moderation Culture | 1.000 | Members are more inclined toward moderate, incremental bills. |
| Low Lobbying Pressure | 1.000 | Lobby pressure is weak. |
| High Lobbying Pressure | 1.000 | Lobby pressure is strong. |
| Weak Constituency Pressure | 1.000 | Members are less responsive to public support. |
| Two-Party System | 1.000 | Generated legislators sort into two broad parties. |
| Multi-Party System | 1.000 | Generated legislators sort into five parties. |
| High Proposal Pressure | 1.000 | Three times as many potential proposals reach the institutional system. |
| Extreme Proposal Pressure | 1.000 | Five times as many potential proposals reach the institutional system. |
| Lobby-Fueled Flooding | 1.000 | High proposal pressure with strong lobbying and weaker constituency pressure. |
| Low-Revision-Moderation Flooding | 1.000 | High proposal pressure in a low-revision-moderation legislature. |
| Capture Crisis | 1.000 | High lobbying, weak constituency pressure, low revision moderation, and high proposal pressure. |
| Popular Anti-Lobbying Push | 1.000 | High lobbying pressure with stronger public responsiveness and more appetite for reform. |
| Weighted Two-Party Baseline | 0.250 | Classic two-party legislature with ideological left/right sorting. |
| Weighted Two Major Plus Minors | 0.400 | Five-party legislature with two large ideological parties and smaller minor parties. |
| Weighted Fragmented Multiparty | 0.200 | Seven-party legislature with more even fragmentation across the ideological range. |
| Weighted Dominant-Party Legislature | 0.150 | Four-party legislature with one large center-weighted party and smaller opposition parties. |
| Era 1 Low Contention | 1.000 | Stylized low-contention legislature with several parties, high revision-moderation culture, lower lobbying, and stronger constituency responsiveness. |
| Era 2 Normal Contention | 1.000 | Stylized ordinary-contention legislature with two major parties plus minors and moderate party loyalty. |
| Era 3 Polarizing | 1.000 | Stylized rising-contention legislature with stronger ideological clustering, party loyalty, and lobbying pressure. |
| Era 4 High Contention | 1.000 | Stylized high-contention legislature with more proposal pressure, higher polarization, and weaker revision-moderation culture. |
| Era 5 Capture Contention | 1.000 | Stylized capture-contention legislature with two-party sorting, higher proposal pressure, strong lobbying, and lower public responsiveness. |
| Era 6 Crisis | 1.000 | Stylized crisis-contention legislature with severe polarization, high party loyalty, intense lobbying, weak constituency responsiveness, and doubled proposal pressure. |
| Adversarial High-Benefit Extreme Reform | 1.000 | Extreme proposals can have high generated public benefit but lower initial support and high uncertainty. |
| Adversarial Popular Harmful Bill | 1.000 | Popular proposals can have low generated public benefit, private upside, and concentrated harm. |
| Adversarial Moderate Capture | 1.000 | Moderate-looking proposals can have low public benefit and high organized-interest capture. |
| Adversarial Delayed-Benefit Reform | 1.000 | Beneficial reforms can have low immediate support because benefits are delayed and uncertain. |
| Adversarial Concentrated Rights Harm | 1.000 | Proposals can be broadly supported while imposing severe concentrated rights-like harm. |
| Adversarial Anti-Lobbying Backlash | 1.000 | Anti-lobbying reforms are more common, but face stronger defensive lobbying and lower observed support. |
| Adversarial Revision Dilution | 1.000 | Some high-distance reforms have high generated value, so moderation can dilute public benefit. |
| Adversarial Lobby Information | 1.000 | Organized lobbying sometimes supplies useful technical information rather than only capture pressure. |
| Adversarial Public Opinion Error | 1.000 | Observed public support can be noisy or systematically misaligned with generated public benefit. |

## Headline Findings

- This focused campaign does not include the open burden-shifting baseline, so relative headline deltas are reported in the diagnostic sections below.
- Highest average welfare in this campaign came from Committee amendment and revision power at 0.708.
- Highest productivity came from Bicameral malapportioned upper chamber + conference at 0.367, while highest revision moderation came from Stylized U.S.-like conventional benchmark at 0.353.
- Highest directional score, where lower-better risk metrics are inverted, came from Appointment and retention eligibility filter at 0.672.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, revision moderation, public alignment, and legitimacy. Risk control inverts chamber low-support passage, low-public-support enactment, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Low-public-support enactment ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral mixed appointed upper chamber | 0.660 | 0.578 | 0.864 | 0.930 | 0.267 | 19.237 | 80.581 | 0.617 | 0.000 | 0.173 | 0.070 | 0.136 | 0.535 | 0.078 | 0.238 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.484 | 0.000 | 1.000 |
| Appointment and retention eligibility filter | 0.672 | 0.558 | 0.832 | 0.930 | 0.366 | 27.198 | 80.581 | 0.595 | 0.000 | 0.262 | 0.070 | 0.151 | 0.499 | 0.135 | 0.312 | 0.263 | 0.000 | 0.000 | 0.000 | 0.000 | 0.616 | 0.000 | 1.000 |
| Bicameral House majority + upper cloture | 0.646 | 0.602 | 0.884 | 0.930 | 0.167 | 11.756 | 80.581 | 0.631 | 0.000 | 0.122 | 0.070 | 0.126 | 0.569 | 0.039 | 0.186 | 0.278 | 0.000 | 0.000 | 0.000 | 0.000 | 0.301 | 0.000 | 1.000 |
| Majority + forced-balanced committee | 0.661 | 0.578 | 0.868 | 0.943 | 0.256 | 18.416 | 25.770 | 0.626 | 0.000 | 0.153 | 0.057 | 0.143 | 0.515 | 0.074 | 0.231 | 0.282 | 0.000 | 0.000 | 0.000 | 0.000 | 0.445 | 0.000 | 0.348 |
| Bicameral simple majority | 0.656 | 0.581 | 0.866 | 0.930 | 0.246 | 17.610 | 80.581 | 0.618 | 0.000 | 0.172 | 0.070 | 0.136 | 0.538 | 0.069 | 0.221 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.439 | 0.000 | 1.000 |
| Bicameral incongruence: district House + PR upper house | 0.659 | 0.574 | 0.861 | 0.930 | 0.269 | 19.445 | 80.581 | 0.615 | 0.000 | 0.181 | 0.070 | 0.137 | 0.531 | 0.082 | 0.247 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.482 | 0.000 | 1.000 |
| Committee amendment and revision power | 0.648 | 0.617 | 0.928 | 0.930 | 0.116 | 8.974 | 11.274 | 0.708 | 0.000 | 0.016 | 0.070 | 0.089 | 0.585 | 0.031 | 0.209 | 0.175 | 0.000 | 0.000 | 0.124 | 0.034 | 0.395 | 0.000 | 0.143 |
| Committee deadline + discharge petition | 0.657 | 0.592 | 0.894 | 0.915 | 0.228 | 16.833 | 28.704 | 0.646 | 0.000 | 0.054 | 0.085 | 0.107 | 0.561 | 0.073 | 0.246 | 0.238 | 0.000 | 0.000 | 0.196 | 0.073 | 0.492 | 0.000 | 0.379 |
| Committee discharge-petition target | 0.650 | 0.609 | 0.921 | 0.923 | 0.149 | 11.226 | 13.933 | 0.675 | 0.000 | 0.051 | 0.077 | 0.081 | 0.578 | 0.040 | 0.214 | 0.202 | 0.000 | 0.000 | 0.166 | 0.053 | 0.401 | 0.000 | 0.182 |
| Committee fast-track certifier | 0.656 | 0.582 | 0.890 | 0.868 | 0.281 | 21.031 | 40.129 | 0.627 | 0.000 | 0.092 | 0.132 | 0.087 | 0.541 | 0.095 | 0.270 | 0.237 | 0.000 | 0.000 | 0.510 | 0.216 | 0.567 | 0.000 | 0.525 |
| Legal and drafting-quality committee | 0.660 | 0.601 | 0.916 | 0.910 | 0.211 | 15.965 | 20.768 | 0.653 | 0.000 | 0.049 | 0.090 | 0.082 | 0.567 | 0.060 | 0.231 | 0.229 | 0.000 | 0.000 | 0.246 | 0.091 | 0.487 | 0.000 | 0.270 |
| Committee minority-hearing rights | 0.649 | 0.607 | 0.915 | 0.928 | 0.144 | 10.914 | 14.771 | 0.686 | 0.000 | 0.031 | 0.072 | 0.098 | 0.578 | 0.042 | 0.226 | 0.206 | 0.000 | 0.000 | 0.131 | 0.039 | 0.406 | 0.000 | 0.191 |
| Committee priority queue | 0.656 | 0.595 | 0.904 | 0.914 | 0.210 | 15.684 | 22.499 | 0.644 | 0.000 | 0.070 | 0.086 | 0.092 | 0.560 | 0.063 | 0.239 | 0.235 | 0.000 | 0.000 | 0.215 | 0.075 | 0.461 | 0.000 | 0.294 |
| Public-accounts committee | 0.655 | 0.608 | 0.922 | 0.916 | 0.176 | 13.398 | 16.664 | 0.668 | 0.000 | 0.050 | 0.084 | 0.062 | 0.581 | 0.049 | 0.222 | 0.215 | 0.000 | 0.000 | 0.215 | 0.075 | 0.434 | 0.000 | 0.215 |
| Committee-first regular order | 0.667 | 0.587 | 0.883 | 0.966 | 0.233 | 16.708 | 21.218 | 0.635 | 0.000 | 0.097 | 0.034 | 0.136 | 0.530 | 0.062 | 0.206 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.435 | 0.000 | 0.290 |
| Committee scrutiny and audit | 0.653 | 0.609 | 0.923 | 0.920 | 0.162 | 12.238 | 15.019 | 0.674 | 0.000 | 0.042 | 0.080 | 0.076 | 0.580 | 0.044 | 0.220 | 0.209 | 0.000 | 0.000 | 0.189 | 0.062 | 0.423 | 0.000 | 0.195 |
| Committee veto player | 0.635 | 0.591 | 0.937 | 0.936 | 0.077 | 6.069 | 7.044 | 0.697 | 0.000 | 0.025 | 0.064 | 0.068 | 0.581 | 0.019 | 0.204 | 0.130 | 0.000 | 0.000 | 0.084 | 0.021 | 0.304 | 0.000 | 0.087 |
| Bicameral malapportioned upper chamber + conference | 0.668 | 0.559 | 0.839 | 0.906 | 0.367 | 26.993 | 80.581 | 0.592 | 0.024 | 0.193 | 0.094 | 0.146 | 0.514 | 0.120 | 0.292 | 0.271 | 0.000 | 0.000 | 0.172 | 0.000 | 0.615 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.646 | 0.622 | 0.924 | 0.985 | 0.055 | 4.012 | 17.452 | 0.651 | 0.000 | 0.009 | 0.015 | 0.089 | 0.644 | 0.011 | 0.162 | 0.215 | 0.000 | 0.000 | 0.000 | 0.000 | 0.162 | 0.000 | 0.216 |
| Expertise eligibility filter | 0.669 | 0.560 | 0.839 | 0.930 | 0.346 | 25.751 | 80.581 | 0.599 | 0.000 | 0.246 | 0.070 | 0.149 | 0.503 | 0.121 | 0.291 | 0.262 | 0.000 | 0.000 | 0.000 | 0.000 | 0.594 | 0.000 | 1.000 |
| Emergency lower-house fast path | 0.662 | 0.574 | 0.859 | 0.930 | 0.283 | 20.430 | 80.581 | 0.615 | 0.000 | 0.186 | 0.070 | 0.137 | 0.529 | 0.085 | 0.241 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.505 | 0.000 | 1.000 |
| Equal-population unicameral chamber | 0.669 | 0.559 | 0.842 | 0.930 | 0.345 | 25.365 | 80.581 | 0.604 | 0.000 | 0.231 | 0.070 | 0.145 | 0.506 | 0.119 | 0.289 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.602 | 0.000 | 1.000 |
| Ex ante advisory review | 0.670 | 0.562 | 0.841 | 0.930 | 0.345 | 25.307 | 80.581 | 0.622 | 0.000 | 0.231 | 0.070 | 0.145 | 0.506 | 0.119 | 0.288 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.596 | 0.000 | 1.000 |
| Mandatory ex ante legal clearance | 0.669 | 0.562 | 0.849 | 0.935 | 0.331 | 24.411 | 74.214 | 0.612 | 0.000 | 0.223 | 0.065 | 0.136 | 0.512 | 0.112 | 0.283 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.564 | 0.000 | 0.923 |
| Majority + expertise-qualified lottery committee | 0.661 | 0.580 | 0.871 | 0.943 | 0.252 | 18.123 | 26.983 | 0.629 | 0.000 | 0.146 | 0.057 | 0.142 | 0.515 | 0.071 | 0.222 | 0.277 | 0.000 | 0.000 | 0.000 | 0.000 | 0.452 | 0.000 | 0.362 |
| House-origin-only bicameral routing | 0.664 | 0.570 | 0.855 | 0.922 | 0.308 | 22.314 | 80.581 | 0.609 | 0.003 | 0.183 | 0.078 | 0.140 | 0.524 | 0.094 | 0.251 | 0.268 | 0.000 | 0.000 | 0.054 | 0.000 | 0.544 | 0.000 | 1.000 |
| Independent fiscal/electoral/audit insulation bundle | 0.670 | 0.563 | 0.842 | 0.930 | 0.345 | 25.388 | 80.581 | 0.627 | 0.000 | 0.230 | 0.070 | 0.145 | 0.506 | 0.119 | 0.287 | 0.262 | 0.000 | 0.000 | 0.000 | 0.000 | 0.600 | 0.000 | 1.000 |
| Bicameral joint-sitting fallback | 0.664 | 0.567 | 0.849 | 0.930 | 0.309 | 22.475 | 80.581 | 0.611 | 0.027 | 0.202 | 0.070 | 0.140 | 0.520 | 0.099 | 0.261 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.547 | 0.000 | 1.000 |
| Last-offer bicameral bargaining | 0.664 | 0.571 | 0.854 | 0.923 | 0.311 | 22.540 | 80.581 | 0.608 | 0.006 | 0.187 | 0.077 | 0.139 | 0.525 | 0.095 | 0.248 | 0.268 | 0.000 | 0.000 | 0.052 | 0.000 | 0.547 | 0.000 | 1.000 |
| Leadership-routed chamber origin | 0.659 | 0.575 | 0.861 | 0.930 | 0.271 | 19.562 | 80.581 | 0.616 | 0.000 | 0.182 | 0.070 | 0.137 | 0.531 | 0.082 | 0.245 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.484 | 0.000 | 1.000 |
| Bicameral limited navette | 0.665 | 0.568 | 0.851 | 0.922 | 0.320 | 23.273 | 80.581 | 0.605 | 0.013 | 0.192 | 0.078 | 0.141 | 0.522 | 0.098 | 0.254 | 0.268 | 0.000 | 0.000 | 0.054 | 0.000 | 0.563 | 0.000 | 1.000 |
| Majority + random-lottery committee | 0.660 | 0.579 | 0.870 | 0.943 | 0.250 | 17.880 | 27.052 | 0.625 | 0.000 | 0.150 | 0.057 | 0.143 | 0.516 | 0.070 | 0.217 | 0.283 | 0.000 | 0.000 | 0.000 | 0.000 | 0.438 | 0.000 | 0.362 |
| Lower-house override after bicameral disagreement | 0.661 | 0.573 | 0.858 | 0.930 | 0.284 | 20.509 | 80.581 | 0.614 | 0.000 | 0.185 | 0.070 | 0.138 | 0.528 | 0.086 | 0.249 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.507 | 0.000 | 1.000 |
| Bicameral malapportioned territorial upper chamber | 0.659 | 0.575 | 0.861 | 0.930 | 0.272 | 19.622 | 80.581 | 0.615 | 0.000 | 0.184 | 0.070 | 0.137 | 0.531 | 0.082 | 0.244 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.484 | 0.000 | 1.000 |
| Mediation committee bicameral conflict | 0.666 | 0.568 | 0.854 | 0.922 | 0.321 | 23.295 | 80.581 | 0.607 | 0.009 | 0.163 | 0.078 | 0.141 | 0.529 | 0.098 | 0.251 | 0.267 | 0.000 | 0.000 | 0.060 | 0.000 | 0.561 | 0.000 | 1.000 |
| Majority + minority-veto committee seat | 0.661 | 0.578 | 0.868 | 0.943 | 0.257 | 18.466 | 26.108 | 0.625 | 0.000 | 0.148 | 0.057 | 0.145 | 0.514 | 0.075 | 0.229 | 0.281 | 0.000 | 0.000 | 0.000 | 0.000 | 0.448 | 0.000 | 0.352 |
| Majority + mixed legislator-citizen committee | 0.650 | 0.605 | 0.919 | 0.921 | 0.156 | 11.795 | 15.178 | 0.665 | 0.000 | 0.058 | 0.079 | 0.080 | 0.576 | 0.043 | 0.216 | 0.208 | 0.000 | 0.000 | 0.180 | 0.058 | 0.394 | 0.000 | 0.197 |
| Majority + opposition-chaired scrutiny committee | 0.662 | 0.577 | 0.867 | 0.943 | 0.260 | 18.673 | 25.921 | 0.625 | 0.000 | 0.153 | 0.057 | 0.143 | 0.514 | 0.077 | 0.238 | 0.279 | 0.000 | 0.000 | 0.000 | 0.000 | 0.456 | 0.000 | 0.350 |
| Principles resolution before second-chamber drafting | 0.664 | 0.565 | 0.852 | 0.921 | 0.316 | 23.052 | 80.581 | 0.604 | 0.009 | 0.173 | 0.079 | 0.144 | 0.523 | 0.100 | 0.268 | 0.268 | 0.000 | 0.000 | 0.067 | 0.000 | 0.540 | 0.000 | 1.000 |
| Majority + proportional committee assignment | 0.662 | 0.577 | 0.867 | 0.943 | 0.260 | 18.724 | 25.658 | 0.625 | 0.000 | 0.154 | 0.057 | 0.144 | 0.514 | 0.077 | 0.239 | 0.282 | 0.000 | 0.000 | 0.000 | 0.000 | 0.454 | 0.000 | 0.347 |
| Proportional lower-house majority | 0.669 | 0.558 | 0.841 | 0.930 | 0.345 | 25.340 | 80.581 | 0.604 | 0.000 | 0.234 | 0.070 | 0.146 | 0.505 | 0.119 | 0.287 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.601 | 0.000 | 1.000 |
| Proposer-chamber origin routing | 0.664 | 0.566 | 0.850 | 0.921 | 0.321 | 23.476 | 80.581 | 0.601 | 0.019 | 0.190 | 0.079 | 0.142 | 0.520 | 0.100 | 0.263 | 0.267 | 0.000 | 0.000 | 0.065 | 0.000 | 0.561 | 0.000 | 1.000 |
| Recusal and cooling-off eligibility filter | 0.671 | 0.558 | 0.832 | 0.930 | 0.365 | 27.194 | 80.581 | 0.594 | 0.000 | 0.265 | 0.070 | 0.151 | 0.498 | 0.134 | 0.308 | 0.263 | 0.000 | 0.000 | 0.000 | 0.000 | 0.605 | 0.000 | 1.000 |
| Bicameral upper revision council | 0.664 | 0.570 | 0.855 | 0.922 | 0.309 | 22.423 | 80.581 | 0.609 | 0.003 | 0.181 | 0.078 | 0.138 | 0.526 | 0.094 | 0.249 | 0.268 | 0.000 | 0.000 | 0.054 | 0.000 | 0.544 | 0.000 | 1.000 |
| Second-chamber preclearance routing | 0.663 | 0.568 | 0.851 | 0.930 | 0.305 | 22.241 | 80.581 | 0.611 | 0.021 | 0.200 | 0.070 | 0.140 | 0.520 | 0.098 | 0.263 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 | 0.547 | 0.000 | 1.000 |
| Senate-origin-only bicameral routing | 0.662 | 0.568 | 0.853 | 0.921 | 0.304 | 22.098 | 80.581 | 0.607 | 0.006 | 0.188 | 0.079 | 0.142 | 0.523 | 0.095 | 0.263 | 0.270 | 0.000 | 0.000 | 0.062 | 0.000 | 0.528 | 0.000 | 1.000 |
| Unicameral simple majority | 0.669 | 0.558 | 0.841 | 0.930 | 0.345 | 25.339 | 80.581 | 0.603 | 0.000 | 0.232 | 0.070 | 0.146 | 0.506 | 0.119 | 0.288 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.598 | 0.000 | 1.000 |
| Bicameral upper suspensive veto | 0.662 | 0.574 | 0.860 | 0.930 | 0.283 | 20.441 | 80.581 | 0.615 | 0.000 | 0.182 | 0.070 | 0.137 | 0.529 | 0.085 | 0.242 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.506 | 0.000 | 1.000 |
| Upper-house absolute veto | 0.646 | 0.603 | 0.884 | 0.930 | 0.167 | 11.725 | 80.581 | 0.630 | 0.000 | 0.129 | 0.070 | 0.131 | 0.565 | 0.038 | 0.191 | 0.278 | 0.000 | 0.000 | 0.000 | 0.000 | 0.302 | 0.000 | 1.000 |
| Upper-house amendment-only power | 0.664 | 0.569 | 0.853 | 0.922 | 0.312 | 22.611 | 80.581 | 0.608 | 0.010 | 0.185 | 0.078 | 0.140 | 0.524 | 0.096 | 0.252 | 0.269 | 0.000 | 0.000 | 0.061 | 0.000 | 0.548 | 0.000 | 1.000 |
| Upper-house territorial veto threshold | 0.654 | 0.601 | 0.882 | 0.930 | 0.203 | 14.330 | 80.581 | 0.633 | 0.000 | 0.122 | 0.070 | 0.126 | 0.566 | 0.047 | 0.182 | 0.273 | 0.000 | 0.000 | 0.000 | 0.000 | 0.369 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - revision moderation) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, produces less revision moderation, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Revision moderation | Gridlock | Low-public-support enactment | Contention index |
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
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.033 | 0.388 | 0.967 | 0.006 | 0.668 |
| Low Revision-Moderation Culture | Unicameral simple majority | 0.213 | 0.242 | 0.788 | 0.140 | 0.649 |
| Low Revision-Moderation Culture | Committee-first regular order | 0.126 | 0.291 | 0.874 | 0.074 | 0.664 |
| High Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.073 | 0.382 | 0.927 | 0.011 | 0.651 |
| High Revision-Moderation Culture | Unicameral simple majority | 0.337 | 0.220 | 0.663 | 0.215 | 0.608 |
| High Revision-Moderation Culture | Committee-first regular order | 0.202 | 0.276 | 0.798 | 0.111 | 0.638 |
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
| Low-Revision-Moderation Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.373 | 0.980 | 0.011 | 0.680 |
| Low-Revision-Moderation Flooding | Unicameral simple majority | 0.161 | 0.250 | 0.839 | 0.148 | 0.674 |
| Low-Revision-Moderation Flooding | Committee-first regular order | 0.093 | 0.287 | 0.907 | 0.077 | 0.683 |
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
| Adversarial Revision Dilution | Stylized U.S.-like conventional benchmark | 0.000 | 0.180 | 1.000 | 0.000 | 0.746 |
| Adversarial Revision Dilution | Unicameral simple majority | 0.040 | 0.125 | 0.960 | 0.394 | 0.821 |
| Adversarial Revision Dilution | Committee-first regular order | 0.019 | 0.129 | 0.981 | 0.033 | 0.759 |
| Adversarial Lobby Information | Stylized U.S.-like conventional benchmark | 0.111 | 0.387 | 0.889 | 0.019 | 0.632 |
| Adversarial Lobby Information | Unicameral simple majority | 0.772 | 0.274 | 0.228 | 0.229 | 0.377 |
| Adversarial Lobby Information | Committee-first regular order | 0.648 | 0.306 | 0.352 | 0.018 | 0.388 |
| Adversarial Public Opinion Error | Stylized U.S.-like conventional benchmark | 0.032 | 0.379 | 0.968 | 0.000 | 0.671 |
| Adversarial Public Opinion Error | Unicameral simple majority | 0.305 | 0.244 | 0.695 | 0.227 | 0.620 |
| Adversarial Public Opinion Error | Committee-first regular order | 0.157 | 0.300 | 0.843 | 0.153 | 0.662 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-public-support enactment |
| --- | --- | --- | --- |
| Baseline | Committee veto player (0.763) | Bicameral malapportioned upper chamber + conference (0.289) | Committee veto player (0.007) |
| Low Polarization | Committee veto player (0.752) | Bicameral malapportioned upper chamber + conference (0.545) | Committee amendment and revision power (0.005) |
| High Polarization | Committee veto player (0.781) | Appointment and retention eligibility filter (0.218) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Committee veto player (0.766) | Bicameral malapportioned upper chamber + conference (0.311) | Committee amendment and revision power (0.003) |
| High Party Loyalty | Committee veto player (0.770) | Bicameral malapportioned upper chamber + conference (0.296) | Committee amendment and revision power (0.008) |
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark (0.773) | Recusal and cooling-off eligibility filter (0.244) | Committee minority-hearing rights (0.004) |
| High Revision-Moderation Culture | Committee veto player (0.756) | Bicameral malapportioned upper chamber + conference (0.370) | Committee veto player (0.007) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.758) | Appointment and retention eligibility filter (0.303) | Committee amendment and revision power (0.004) |
| High Lobbying Pressure | Committee veto player (0.779) | Appointment and retention eligibility filter (0.264) | Stylized U.S.-like conventional benchmark (0.000) |
| Weak Constituency Pressure | Committee veto player (0.751) | Recusal and cooling-off eligibility filter (0.270) | Committee amendment and revision power (0.008) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.761) | Recusal and cooling-off eligibility filter (0.306) | Committee amendment and revision power (0.005) |
| Multi-Party System | Committee veto player (0.764) | Bicameral malapportioned upper chamber + conference (0.302) | Committee veto player (0.004) |
| High Proposal Pressure | Committee veto player (0.766) | Bicameral malapportioned upper chamber + conference (0.292) | Committee amendment and revision power (0.007) |
| Extreme Proposal Pressure | Committee veto player (0.763) | Bicameral malapportioned upper chamber + conference (0.290) | Committee veto player (0.005) |
| Lobby-Fueled Flooding | Committee amendment and revision power (0.762) | Recusal and cooling-off eligibility filter (0.256) | Stylized U.S.-like conventional benchmark (0.000) |
| Low-Revision-Moderation Flooding | Committee veto player (0.771) | Expertise eligibility filter (0.207) | Committee veto player (0.005) |
| Capture Crisis | Committee veto player (0.747) | Recusal and cooling-off eligibility filter (0.224) | Stylized U.S.-like conventional benchmark (0.005) |
| Popular Anti-Lobbying Push | Committee veto player (0.783) | Bicameral malapportioned upper chamber + conference (0.378) | Stylized U.S.-like conventional benchmark (0.004) |
| Weighted Two-Party Baseline | Committee veto player (0.775) | Bicameral malapportioned upper chamber + conference (0.289) | Stylized U.S.-like conventional benchmark (0.004) |
| Weighted Two Major Plus Minors | Committee veto player (0.764) | Appointment and retention eligibility filter (0.295) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Committee veto player (0.760) | Bicameral malapportioned upper chamber + conference (0.345) | Stylized U.S.-like conventional benchmark (0.003) |
| Weighted Dominant-Party Legislature | Committee veto player (0.764) | Recusal and cooling-off eligibility filter (0.310) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 1 Low Contention | Committee veto player (0.737) | Bicameral malapportioned upper chamber + conference (0.543) | Committee amendment and revision power (0.007) |
| Era 2 Normal Contention | Committee veto player (0.760) | Bicameral malapportioned upper chamber + conference (0.441) | Committee veto player (0.005) |
| Era 3 Polarizing | Committee veto player (0.769) | Bicameral malapportioned upper chamber + conference (0.339) | Committee amendment and revision power (0.005) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.781) | Recusal and cooling-off eligibility filter (0.248) | Committee veto player (0.007) |
| Era 5 Capture Contention | Committee veto player (0.756) | Recusal and cooling-off eligibility filter (0.200) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Committee veto player (0.769) | Recusal and cooling-off eligibility filter (0.165) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial High-Benefit Extreme Reform | Committee veto player (0.852) | Committee fast-track certifier (0.207) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Public-accounts committee (0.416) | Bicameral malapportioned upper chamber + conference (0.930) | Committee amendment and revision power (0.000) |
| Adversarial Moderate Capture | Committee scrutiny and audit (0.526) | Bicameral malapportioned upper chamber + conference (0.978) | Committee minority-hearing rights (0.000) |
| Adversarial Delayed-Benefit Reform | Committee veto player (0.781) | Committee fast-track certifier (0.338) | Committee amendment and revision power (0.050) |
| Adversarial Concentrated Rights Harm | Committee veto player (0.541) | Bicameral malapportioned upper chamber + conference (0.552) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Anti-Lobbying Backlash | Committee veto player (0.726) | Expertise eligibility filter (0.374) | Stylized U.S.-like conventional benchmark (0.009) |
| Adversarial Revision Dilution | Committee veto player (0.828) | Committee fast-track certifier (0.186) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Lobby Information | Committee veto player (0.782) | Committee fast-track certifier (0.869) | Committee amendment and revision power (0.000) |
| Adversarial Public Opinion Error | Committee amendment and revision power (0.747) | Appointment and retention eligibility filter (0.346) | Stylized U.S.-like conventional benchmark (0.000) |

## Interpretation

- Timeline scenarios are stylized stress paths, not historical calibration. They increase polarization, party loyalty, lobbying pressure, and proposal pressure while reducing revision-moderation culture and constituency responsiveness.
- The timeline comparison should be read as a degradation test: institutions that preserve revision moderation and productivity under later-era assumptions are more robust than systems that only work in low-contention settings.

## Reproduction

```sh
make campaign
```
