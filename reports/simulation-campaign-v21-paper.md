# Main Comparison Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 44
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

- The main comparison campaign compares 44 scenario families across the same synthetic worlds, including a small burden-shifting stress-test family.
- The scalar directional score is productivity-sensitive: its highest value came from Default pass unless 2/3 block at 0.727, which is why the report treats the score as a profile aid rather than a recommendation.
- Highest average welfare came from Committee amendment and revision power at 0.721; highest revision moderation came from Unicameral majority + pairwise alternatives at 0.505.
- Highest productivity came from Default pass unless 2/3 block at 0.866.
- Open burden-shifting passage averaged 0.866 productivity, 0.475 low-public-support enactment, and 0.629 policy shift, so it functions as a throughput/risk endpoint.
- The stylized U.S.-like conventional benchmark averaged 0.055 productivity and 0.677 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.
- The portfolio hybrid combines risk routing, pairwise alternatives, citizen/harm review, proposal bonds, anti-capture safeguards, and law review. It averaged 0.526 productivity, 0.421 revision moderation, 0.931 risk control, and 0.711 directional score, situating it between pairwise alternatives and risk routing rather than replacing the tradeoff frontier.
- The expanded portfolio hybrid adds district-public, long-horizon strategy, omnibus bargaining, influence-system, and constitutional-court architecture proxies. It averaged 0.789 productivity, 0.466 revision moderation, 0.902 risk control, and 0.684 directional score; its value is diagnostic because extra safeguards also increase complexity.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, revision moderation, public alignment, and legitimacy. Risk control inverts chamber low-support passage, low-public-support enactment, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Low-public-support enactment ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.647 | 0.571 | 0.878 | 0.967 | 0.171 | 13.684 | 39.882 | 0.636 | 0.000 | 0.182 | 0.033 | 0.114 | 0.543 | 0.061 | 0.296 | 0.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.380 | 0.000 | 0.465 |
| Anti-capture proposal access + majority | 0.668 | 0.576 | 0.884 | 0.938 | 0.275 | 22.374 | 76.296 | 0.642 | 0.000 | 0.191 | 0.062 | 0.109 | 0.542 | 0.102 | 0.297 | 0.138 | 0.000 | 0.000 | 0.000 | 0.000 | 0.653 | 0.000 | 0.890 |
| Majority + anti-capture bundle | 0.679 | 0.580 | 0.884 | 0.934 | 0.317 | 25.573 | 80.740 | 0.660 | 0.000 | 0.149 | 0.066 | 0.114 | 0.546 | 0.119 | 0.304 | 0.133 | 0.101 | 0.551 | 0.000 | 0.000 | 0.723 | 0.000 | 0.937 |
| Bicameral simple majority | 0.654 | 0.587 | 0.878 | 0.930 | 0.222 | 16.972 | 86.029 | 0.635 | 0.000 | 0.151 | 0.070 | 0.114 | 0.559 | 0.064 | 0.225 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.447 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.635 | 0.611 | 0.907 | 0.810 | 0.211 | 16.705 | 86.029 | 0.696 | 0.000 | 0.054 | 0.190 | 0.089 | 0.623 | 0.067 | 0.251 | 0.210 | 0.000 | 0.000 | 0.000 | 0.000 | 0.567 | 0.000 | 1.000 |
| Citizen initiative and referendum | 0.694 | 0.580 | 0.833 | 0.930 | 0.430 | 35.227 | 86.029 | 0.601 | 0.000 | 0.227 | 0.070 | 0.130 | 0.534 | 0.206 | 0.408 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.837 | 0.000 | 1.000 |
| Citizen agenda petitions + majority | 0.662 | 0.583 | 0.911 | 0.953 | 0.201 | 15.828 | 36.081 | 0.654 | 0.000 | 0.077 | 0.047 | 0.075 | 0.575 | 0.074 | 0.309 | 0.150 | 0.000 | 0.000 | 0.096 | 0.048 | 0.655 | 0.000 | 0.429 |
| Cloture, conference, and judicial review | 0.644 | 0.627 | 0.928 | 0.967 | 0.053 | 3.959 | 22.976 | 0.690 | 0.000 | 0.037 | 0.033 | 0.087 | 0.616 | 0.010 | 0.145 | 0.203 | 0.000 | 0.000 | 0.069 | 0.000 | 0.163 | 0.000 | 0.279 |
| Committee amendment and revision power | 0.651 | 0.620 | 0.932 | 0.929 | 0.121 | 9.813 | 12.275 | 0.721 | 0.000 | 0.014 | 0.071 | 0.072 | 0.605 | 0.032 | 0.209 | 0.156 | 0.000 | 0.000 | 0.130 | 0.031 | 0.450 | 0.000 | 0.148 |
| Committee discharge-petition target | 0.653 | 0.613 | 0.926 | 0.923 | 0.150 | 11.913 | 14.818 | 0.691 | 0.000 | 0.045 | 0.077 | 0.065 | 0.597 | 0.041 | 0.215 | 0.180 | 0.000 | 0.000 | 0.167 | 0.047 | 0.445 | 0.000 | 0.182 |
| Committee-first regular order | 0.665 | 0.592 | 0.892 | 0.968 | 0.209 | 16.004 | 20.727 | 0.652 | 0.000 | 0.093 | 0.032 | 0.114 | 0.550 | 0.057 | 0.210 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.444 | 0.000 | 0.264 |
| Compensation amendments + majority | 0.662 | 0.564 | 0.835 | 0.930 | 0.318 | 25.040 | 86.029 | 0.610 | 0.000 | 0.219 | 0.070 | 0.091 | 0.538 | 0.114 | 0.294 | 0.255 | 0.000 | 0.000 | 0.000 | 0.164 | 0.621 | 0.000 | 1.000 |
| Constitutional court architecture | 0.652 | 0.565 | 0.835 | 0.892 | 0.317 | 24.918 | 86.029 | 0.610 | 0.000 | 0.217 | 0.108 | 0.089 | 0.540 | 0.113 | 0.294 | 0.255 | 0.000 | 0.000 | 0.000 | 0.169 | 0.617 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.650 | 0.630 | 0.931 | 0.984 | 0.055 | 4.179 | 19.097 | 0.677 | 0.000 | 0.007 | 0.016 | 0.066 | 0.659 | 0.011 | 0.145 | 0.202 | 0.000 | 0.000 | 0.000 | 0.000 | 0.173 | 0.000 | 0.224 |
| Default pass unless 2/3 block | 0.727 | 0.479 | 0.630 | 0.930 | 0.866 | 73.849 | 86.029 | 0.515 | 0.418 | 0.475 | 0.070 | 0.185 | 0.392 | 0.629 | 0.603 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 | 0.986 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.682 | 0.494 | 0.704 | 0.892 | 0.636 | 60.620 | 86.029 | 0.532 | 0.334 | 0.438 | 0.108 | 0.175 | 0.410 | 0.378 | 0.470 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.834 | 0.471 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.708 | 0.513 | 0.725 | 0.793 | 0.799 | 71.369 | 86.029 | 0.478 | 0.244 | 0.370 | 0.207 | 0.114 | 0.451 | 0.279 | 0.316 | 0.282 | 0.000 | 0.000 | 0.738 | 0.273 | 0.864 | 0.424 | 1.000 |
| District-population public-will model | 0.657 | 0.565 | 0.859 | 0.930 | 0.273 | 21.202 | 86.029 | 0.628 | 0.000 | 0.325 | 0.070 | 0.127 | 0.456 | 0.083 | 0.249 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.549 | 0.000 | 1.000 |
| Expanded portfolio hybrid legislature | 0.684 | 0.628 | 0.902 | 0.416 | 0.789 | 65.126 | 78.546 | 0.571 | 0.000 | 0.002 | 0.584 | 0.047 | 0.585 | 0.046 | 0.033 | 0.227 | 0.460 | 0.385 | 1.000 | 0.653 | 0.809 | 0.000 | 0.915 |
| Harm-weighted double majority | 0.663 | 0.570 | 0.875 | 0.930 | 0.277 | 22.101 | 86.029 | 0.624 | 0.000 | 0.211 | 0.070 | 0.109 | 0.536 | 0.094 | 0.278 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 | 0.575 | 0.000 | 1.000 |
| Campaign-finance influence system | 0.676 | 0.573 | 0.871 | 0.937 | 0.322 | 26.022 | 77.045 | 0.631 | 0.000 | 0.144 | 0.063 | 0.116 | 0.553 | 0.123 | 0.308 | 0.207 | 0.460 | 0.382 | 0.000 | 0.000 | 0.658 | 0.000 | 0.899 |
| Active-law registry + majority review | 0.656 | 0.556 | 0.835 | 0.890 | 0.345 | 27.349 | 86.029 | 0.604 | 0.000 | 0.252 | 0.110 | 0.132 | 0.511 | 0.193 | 0.343 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.639 | 0.000 | 1.000 |
| Leadership agenda cartel + majority | 0.658 | 0.586 | 0.905 | 0.973 | 0.167 | 13.491 | 32.981 | 0.659 | 0.000 | 0.124 | 0.027 | 0.094 | 0.576 | 0.051 | 0.228 | 0.154 | 0.000 | 0.000 | 0.000 | 0.000 | 0.575 | 0.000 | 0.389 |
| Long-horizon strategic learning | 0.681 | 0.540 | 0.796 | 0.790 | 0.597 | 48.416 | 85.956 | 0.498 | 0.000 | 0.244 | 0.210 | 0.108 | 0.503 | 0.201 | 0.317 | 0.300 | 0.158 | 0.651 | 0.999 | 0.268 | 0.648 | 0.000 | 0.999 |
| Multidimensional package bargaining + majority | 0.640 | 0.558 | 0.835 | 0.826 | 0.339 | 26.583 | 86.029 | 0.591 | 0.000 | 0.223 | 0.174 | 0.100 | 0.529 | 0.125 | 0.313 | 0.261 | 0.000 | 0.000 | 0.373 | 0.373 | 0.633 | 0.000 | 1.000 |
| Endogenous norm erosion + majority | 0.632 | 0.558 | 0.843 | 0.800 | 0.325 | 25.608 | 81.302 | 0.612 | 0.000 | 0.252 | 0.200 | 0.126 | 0.510 | 0.116 | 0.321 | 0.258 | 0.000 | 0.000 | 0.951 | 0.020 | 0.595 | 0.000 | 0.951 |
| Omnibus bargaining + majority | 0.629 | 0.560 | 0.847 | 0.738 | 0.372 | 29.123 | 86.029 | 0.587 | 0.000 | 0.163 | 0.262 | 0.077 | 0.546 | 0.141 | 0.316 | 0.261 | 0.000 | 0.000 | 0.686 | 0.686 | 0.657 | 0.000 | 1.000 |
| Open-rule floor calendar + majority | 0.663 | 0.553 | 0.842 | 0.902 | 0.354 | 28.154 | 80.883 | 0.579 | 0.000 | 0.255 | 0.098 | 0.116 | 0.507 | 0.129 | 0.321 | 0.271 | 0.000 | 0.000 | 0.149 | 0.084 | 0.612 | 0.000 | 0.948 |
| Package bargaining + majority | 0.655 | 0.562 | 0.842 | 0.890 | 0.325 | 25.537 | 86.029 | 0.609 | 0.000 | 0.227 | 0.110 | 0.114 | 0.525 | 0.117 | 0.299 | 0.257 | 0.000 | 0.000 | 0.285 | 0.285 | 0.618 | 0.000 | 1.000 |
| Pairwise amendment tournament + majority | 0.713 | 0.658 | 0.937 | 0.714 | 0.544 | 45.234 | 47.884 | 0.639 | 0.000 | 0.002 | 0.286 | 0.056 | 0.640 | 0.005 | 0.004 | 0.227 | 0.000 | 0.000 | 0.567 | 0.000 | 0.789 | 0.000 | 0.567 |
| Parliamentary coalition confidence | 0.665 | 0.544 | 0.906 | 0.980 | 0.229 | 17.250 | 21.432 | 0.603 | 0.000 | 0.074 | 0.020 | 0.078 | 0.553 | 0.063 | 0.188 | 0.175 | 0.000 | 0.000 | 0.000 | 0.000 | 0.556 | 0.000 | 0.284 |
| Portfolio hybrid legislature | 0.711 | 0.627 | 0.931 | 0.761 | 0.526 | 43.369 | 54.483 | 0.630 | 0.000 | 0.030 | 0.239 | 0.064 | 0.599 | 0.075 | 0.087 | 0.146 | 0.105 | 0.598 | 0.427 | 0.016 | 0.771 | 0.000 | 0.640 |
| Bicameral majority + presidential veto | 0.642 | 0.600 | 0.891 | 0.930 | 0.147 | 11.125 | 86.029 | 0.647 | 0.000 | 0.126 | 0.070 | 0.106 | 0.580 | 0.039 | 0.208 | 0.259 | 0.000 | 0.000 | 0.000 | 0.000 | 0.307 | 0.000 | 1.000 |
| Majority + proportional committee assignment | 0.658 | 0.580 | 0.875 | 0.944 | 0.235 | 18.061 | 25.430 | 0.637 | 0.000 | 0.154 | 0.056 | 0.123 | 0.531 | 0.072 | 0.245 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.464 | 0.000 | 0.321 |
| Proposal bonds + majority | 0.666 | 0.563 | 0.853 | 0.931 | 0.317 | 24.835 | 84.833 | 0.616 | 0.000 | 0.218 | 0.069 | 0.125 | 0.524 | 0.113 | 0.294 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.614 | 0.000 | 0.993 |
| Majority + public-interest screen | 0.660 | 0.569 | 0.870 | 0.939 | 0.260 | 20.893 | 74.397 | 0.635 | 0.000 | 0.192 | 0.061 | 0.115 | 0.538 | 0.096 | 0.290 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.530 | 0.000 | 0.866 |
| Public objection window + majority | 0.644 | 0.588 | 0.893 | 0.866 | 0.229 | 17.950 | 86.029 | 0.649 | 0.000 | 0.127 | 0.134 | 0.097 | 0.573 | 0.063 | 0.215 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.555 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.621 | 0.575 | 0.877 | 0.779 | 0.251 | 18.965 | 48.500 | 0.633 | 0.000 | 0.185 | 0.221 | 0.110 | 0.545 | 0.078 | 0.243 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.550 | 0.000 | 0.609 |
| Random public review panel + majority | 0.636 | 0.604 | 0.898 | 0.810 | 0.232 | 18.422 | 86.029 | 0.681 | 0.000 | 0.074 | 0.190 | 0.095 | 0.618 | 0.077 | 0.266 | 0.218 | 0.000 | 0.000 | 0.000 | 0.000 | 0.576 | 0.000 | 1.000 |
| Risk-routed majority legislature | 0.688 | 0.546 | 0.840 | 0.830 | 0.536 | 42.728 | 86.029 | 0.522 | 0.000 | 0.234 | 0.170 | 0.102 | 0.512 | 0.184 | 0.320 | 0.286 | 0.000 | 0.000 | 0.648 | 0.226 | 0.676 | 0.000 | 1.000 |
| Unicameral simple majority | 0.666 | 0.562 | 0.852 | 0.930 | 0.318 | 24.990 | 86.029 | 0.615 | 0.000 | 0.218 | 0.070 | 0.125 | 0.524 | 0.114 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.617 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.714 | 0.658 | 0.937 | 0.712 | 0.549 | 45.676 | 48.323 | 0.638 | 0.000 | 0.002 | 0.288 | 0.056 | 0.641 | 0.005 | 0.004 | 0.227 | 0.000 | 0.000 | 0.572 | 0.000 | 0.792 | 0.000 | 0.573 |
| Unicameral majority + mediation | 0.639 | 0.547 | 0.800 | 0.815 | 0.395 | 31.495 | 86.029 | 0.587 | 0.000 | 0.279 | 0.185 | 0.107 | 0.508 | 0.156 | 0.379 | 0.275 | 0.000 | 0.000 | 0.824 | 0.176 | 0.655 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.647 | 0.625 | 0.903 | 0.930 | 0.130 | 9.578 | 86.029 | 0.661 | 0.000 | 0.068 | 0.070 | 0.097 | 0.611 | 0.027 | 0.164 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.267 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - revision moderation) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, produces less revision moderation, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Revision moderation | Gridlock | Low-public-support enactment | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.952 | 0.000 | 0.663 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.183 | 0.638 |
| Baseline | Committee-first regular order | 0.155 | 0.281 | 0.845 | 0.080 | 0.654 |
| Baseline | Parliamentary coalition confidence | 0.181 | 0.286 | 0.819 | 0.058 | 0.636 |
| Baseline | Unicameral majority + pairwise alternatives | 0.546 | 0.489 | 0.454 | 0.003 | 0.381 |
| Baseline | Citizen assembly threshold gate | 0.182 | 0.257 | 0.818 | 0.028 | 0.637 |
| Baseline | Risk-routed majority legislature | 0.473 | 0.237 | 0.528 | 0.243 | 0.541 |
| Baseline | Portfolio hybrid legislature | 0.512 | 0.398 | 0.488 | 0.038 | 0.432 |
| Baseline | Expanded portfolio hybrid legislature | 0.800 | 0.443 | 0.200 | 0.004 | 0.268 |
| Baseline | Default pass unless 2/3 block | 0.838 | 0.105 | 0.162 | 0.491 | 0.448 |
| Baseline | Default pass + multi-round mediation + challenge | 0.722 | 0.219 | 0.278 | 0.399 | 0.453 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.172 | 0.386 | 0.828 | 0.011 | 0.600 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.182 | 0.494 |
| Low Polarization | Committee-first regular order | 0.386 | 0.313 | 0.614 | 0.090 | 0.531 |
| Low Polarization | Parliamentary coalition confidence | 0.480 | 0.302 | 0.520 | 0.098 | 0.489 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.631 | 0.634 | 0.369 | 0.001 | 0.295 |
| Low Polarization | Citizen assembly threshold gate | 0.403 | 0.298 | 0.597 | 0.040 | 0.517 |
| Low Polarization | Risk-routed majority legislature | 0.675 | 0.276 | 0.325 | 0.247 | 0.429 |
| Low Polarization | Portfolio hybrid legislature | 0.653 | 0.432 | 0.347 | 0.049 | 0.354 |
| Low Polarization | Expanded portfolio hybrid legislature | 0.868 | 0.511 | 0.132 | 0.008 | 0.214 |
| Low Polarization | Default pass unless 2/3 block | 0.848 | 0.198 | 0.152 | 0.377 | 0.392 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.805 | 0.266 | 0.195 | 0.338 | 0.385 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.022 | 0.361 | 0.978 | 0.000 | 0.680 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.188 | 0.687 |
| High Polarization | Committee-first regular order | 0.091 | 0.270 | 0.909 | 0.069 | 0.687 |
| High Polarization | Parliamentary coalition confidence | 0.095 | 0.301 | 0.905 | 0.023 | 0.667 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.488 | 0.448 | 0.512 | 0.002 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.120 | 0.251 | 0.880 | 0.015 | 0.668 |
| High Polarization | Risk-routed majority legislature | 0.361 | 0.227 | 0.639 | 0.234 | 0.598 |
| High Polarization | Portfolio hybrid legislature | 0.438 | 0.392 | 0.562 | 0.028 | 0.469 |
| High Polarization | Expanded portfolio hybrid legislature | 0.729 | 0.425 | 0.271 | 0.002 | 0.309 |
| High Polarization | Default pass unless 2/3 block | 0.839 | 0.080 | 0.161 | 0.545 | 0.465 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.678 | 0.208 | 0.322 | 0.447 | 0.488 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.052 | 0.346 | 0.948 | 0.011 | 0.673 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.183 | 0.630 |
| Low Party Loyalty | Committee-first regular order | 0.165 | 0.269 | 0.835 | 0.097 | 0.656 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.187 | 0.280 | 0.813 | 0.052 | 0.633 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.536 | 0.503 | 0.464 | 0.003 | 0.382 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.205 | 0.243 | 0.795 | 0.030 | 0.631 |
| Low Party Loyalty | Risk-routed majority legislature | 0.511 | 0.230 | 0.489 | 0.247 | 0.525 |
| Low Party Loyalty | Portfolio hybrid legislature | 0.529 | 0.394 | 0.471 | 0.047 | 0.427 |
| Low Party Loyalty | Expanded portfolio hybrid legislature | 0.802 | 0.452 | 0.198 | 0.003 | 0.264 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.842 | 0.105 | 0.158 | 0.503 | 0.448 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.742 | 0.219 | 0.258 | 0.406 | 0.444 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.050 | 0.371 | 0.950 | 0.006 | 0.665 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.193 | 0.635 |
| High Party Loyalty | Committee-first regular order | 0.165 | 0.283 | 0.835 | 0.094 | 0.652 |
| High Party Loyalty | Parliamentary coalition confidence | 0.196 | 0.285 | 0.804 | 0.058 | 0.628 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.552 | 0.504 | 0.448 | 0.002 | 0.373 |
| High Party Loyalty | Citizen assembly threshold gate | 0.187 | 0.267 | 0.813 | 0.032 | 0.633 |
| High Party Loyalty | Risk-routed majority legislature | 0.481 | 0.239 | 0.519 | 0.247 | 0.537 |
| High Party Loyalty | Portfolio hybrid legislature | 0.518 | 0.404 | 0.482 | 0.042 | 0.428 |
| High Party Loyalty | Expanded portfolio hybrid legislature | 0.802 | 0.453 | 0.198 | 0.003 | 0.264 |
| High Party Loyalty | Default pass unless 2/3 block | 0.842 | 0.110 | 0.158 | 0.475 | 0.441 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.709 | 0.222 | 0.291 | 0.389 | 0.457 |
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.032 | 0.372 | 0.968 | 0.000 | 0.673 |
| Low Revision-Moderation Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.147 | 0.652 |
| Low Revision-Moderation Culture | Committee-first regular order | 0.125 | 0.285 | 0.875 | 0.078 | 0.668 |
| Low Revision-Moderation Culture | Parliamentary coalition confidence | 0.148 | 0.291 | 0.852 | 0.017 | 0.642 |
| Low Revision-Moderation Culture | Unicameral majority + pairwise alternatives | 0.527 | 0.470 | 0.473 | 0.002 | 0.396 |
| Low Revision-Moderation Culture | Citizen assembly threshold gate | 0.157 | 0.271 | 0.843 | 0.017 | 0.644 |
| Low Revision-Moderation Culture | Risk-routed majority legislature | 0.373 | 0.237 | 0.628 | 0.207 | 0.584 |
| Low Revision-Moderation Culture | Portfolio hybrid legislature | 0.483 | 0.392 | 0.517 | 0.031 | 0.447 |
| Low Revision-Moderation Culture | Expanded portfolio hybrid legislature | 0.746 | 0.429 | 0.254 | 0.001 | 0.298 |
| Low Revision-Moderation Culture | Default pass unless 2/3 block | 0.827 | 0.103 | 0.173 | 0.495 | 0.455 |
| Low Revision-Moderation Culture | Default pass + multi-round mediation + challenge | 0.678 | 0.213 | 0.322 | 0.407 | 0.479 |
| High Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.070 | 0.372 | 0.930 | 0.006 | 0.654 |
| High Revision-Moderation Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.222 | 0.617 |
| High Revision-Moderation Culture | Committee-first regular order | 0.192 | 0.277 | 0.808 | 0.111 | 0.643 |
| High Revision-Moderation Culture | Parliamentary coalition confidence | 0.234 | 0.274 | 0.766 | 0.086 | 0.618 |
| High Revision-Moderation Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.534 | 0.443 | 0.002 | 0.362 |
| High Revision-Moderation Culture | Citizen assembly threshold gate | 0.218 | 0.257 | 0.782 | 0.055 | 0.625 |
| High Revision-Moderation Culture | Risk-routed majority legislature | 0.572 | 0.235 | 0.428 | 0.287 | 0.501 |
| High Revision-Moderation Culture | Portfolio hybrid legislature | 0.557 | 0.417 | 0.443 | 0.052 | 0.407 |
| High Revision-Moderation Culture | Expanded portfolio hybrid legislature | 0.842 | 0.475 | 0.158 | 0.005 | 0.237 |
| High Revision-Moderation Culture | Default pass unless 2/3 block | 0.855 | 0.109 | 0.145 | 0.499 | 0.440 |
| High Revision-Moderation Culture | Default pass + multi-round mediation + challenge | 0.759 | 0.225 | 0.241 | 0.399 | 0.433 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.383 | 0.943 | 0.007 | 0.658 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.180 | 0.633 |
| Low Lobbying Pressure | Committee-first regular order | 0.163 | 0.290 | 0.837 | 0.095 | 0.651 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.200 | 0.282 | 0.800 | 0.078 | 0.631 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.570 | 0.515 | 0.430 | 0.003 | 0.361 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.192 | 0.255 | 0.808 | 0.038 | 0.635 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.488 | 0.219 | 0.512 | 0.290 | 0.549 |
| Low Lobbying Pressure | Portfolio hybrid legislature | 0.564 | 0.410 | 0.436 | 0.039 | 0.403 |
| Low Lobbying Pressure | Expanded portfolio hybrid legislature | 0.864 | 0.455 | 0.136 | 0.005 | 0.232 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.843 | 0.104 | 0.157 | 0.493 | 0.446 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.709 | 0.205 | 0.291 | 0.423 | 0.469 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.366 | 0.973 | 0.005 | 0.678 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.205 | 0.654 |
| High Lobbying Pressure | Committee-first regular order | 0.139 | 0.257 | 0.861 | 0.106 | 0.675 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.135 | 0.305 | 0.865 | 0.031 | 0.647 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.490 | 0.477 | 0.510 | 0.005 | 0.413 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.160 | 0.272 | 0.840 | 0.027 | 0.644 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.396 | 0.253 | 0.604 | 0.219 | 0.570 |
| High Lobbying Pressure | Portfolio hybrid legislature | 0.456 | 0.395 | 0.544 | 0.037 | 0.461 |
| High Lobbying Pressure | Expanded portfolio hybrid legislature | 0.651 | 0.443 | 0.349 | 0.002 | 0.342 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.831 | 0.106 | 0.169 | 0.502 | 0.453 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.712 | 0.230 | 0.288 | 0.418 | 0.459 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.387 | 0.973 | 0.016 | 0.674 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.231 | 0.658 |
| Weak Constituency Pressure | Committee-first regular order | 0.127 | 0.284 | 0.873 | 0.123 | 0.676 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.120 | 0.336 | 0.880 | 0.046 | 0.649 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.525 | 0.467 | 0.475 | 0.003 | 0.398 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.163 | 0.271 | 0.837 | 0.037 | 0.644 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.462 | 0.245 | 0.538 | 0.332 | 0.562 |
| Weak Constituency Pressure | Portfolio hybrid legislature | 0.481 | 0.400 | 0.519 | 0.043 | 0.448 |
| Weak Constituency Pressure | Expanded portfolio hybrid legislature | 0.764 | 0.439 | 0.236 | 0.005 | 0.287 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.877 | 0.102 | 0.123 | 0.521 | 0.435 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.742 | 0.225 | 0.258 | 0.464 | 0.454 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.011 | 0.666 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.189 | 0.633 |
| Two-Party System | Committee-first regular order | 0.162 | 0.282 | 0.838 | 0.081 | 0.650 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.486 | 0.458 | 0.002 | 0.383 |
| Two-Party System | Citizen assembly threshold gate | 0.188 | 0.257 | 0.812 | 0.029 | 0.635 |
| Two-Party System | Risk-routed majority legislature | 0.477 | 0.240 | 0.523 | 0.257 | 0.541 |
| Two-Party System | Portfolio hybrid legislature | 0.516 | 0.398 | 0.484 | 0.040 | 0.431 |
| Two-Party System | Expanded portfolio hybrid legislature | 0.803 | 0.440 | 0.197 | 0.002 | 0.267 |
| Two-Party System | Default pass unless 2/3 block | 0.846 | 0.108 | 0.154 | 0.503 | 0.445 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.828 | 0.206 | 0.172 | 0.410 | 0.406 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.054 | 0.360 | 0.946 | 0.005 | 0.666 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.191 | 0.628 |
| Multi-Party System | Committee-first regular order | 0.176 | 0.276 | 0.824 | 0.085 | 0.646 |
| Multi-Party System | Parliamentary coalition confidence | 0.266 | 0.252 | 0.734 | 0.072 | 0.606 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.510 | 0.457 | 0.003 | 0.376 |
| Multi-Party System | Citizen assembly threshold gate | 0.201 | 0.261 | 0.799 | 0.033 | 0.628 |
| Multi-Party System | Risk-routed majority legislature | 0.500 | 0.239 | 0.500 | 0.245 | 0.527 |
| Multi-Party System | Portfolio hybrid legislature | 0.528 | 0.403 | 0.472 | 0.044 | 0.423 |
| Multi-Party System | Expanded portfolio hybrid legislature | 0.811 | 0.460 | 0.189 | 0.003 | 0.257 |
| Multi-Party System | Default pass unless 2/3 block | 0.837 | 0.110 | 0.163 | 0.506 | 0.450 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.645 | 0.232 | 0.355 | 0.374 | 0.483 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.050 | 0.373 | 0.950 | 0.005 | 0.664 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.186 | 0.634 |
| High Proposal Pressure | Committee-first regular order | 0.162 | 0.286 | 0.838 | 0.085 | 0.650 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.187 | 0.292 | 0.813 | 0.056 | 0.630 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.496 | 0.460 | 0.001 | 0.382 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.265 | 0.813 | 0.034 | 0.634 |
| High Proposal Pressure | Risk-routed majority legislature | 0.480 | 0.240 | 0.520 | 0.251 | 0.538 |
| High Proposal Pressure | Portfolio hybrid legislature | 0.510 | 0.402 | 0.490 | 0.039 | 0.432 |
| High Proposal Pressure | Expanded portfolio hybrid legislature | 0.798 | 0.448 | 0.202 | 0.003 | 0.267 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.843 | 0.107 | 0.157 | 0.501 | 0.446 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.903 | 0.204 | 0.097 | 0.432 | 0.374 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.371 | 0.951 | 0.006 | 0.665 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.188 | 0.635 |
| Extreme Proposal Pressure | Committee-first regular order | 0.158 | 0.285 | 0.842 | 0.084 | 0.652 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.291 | 0.815 | 0.047 | 0.630 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.491 | 0.460 | 0.000 | 0.383 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.029 | 0.633 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.476 | 0.239 | 0.524 | 0.252 | 0.541 |
| Extreme Proposal Pressure | Portfolio hybrid legislature | 0.512 | 0.400 | 0.488 | 0.038 | 0.432 |
| Extreme Proposal Pressure | Expanded portfolio hybrid legislature | 0.796 | 0.445 | 0.204 | 0.003 | 0.269 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.844 | 0.105 | 0.156 | 0.500 | 0.446 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.941 | 0.199 | 0.059 | 0.435 | 0.357 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.023 | 0.353 | 0.977 | 0.002 | 0.683 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.216 | 0.661 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.127 | 0.268 | 0.873 | 0.099 | 0.676 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.114 | 0.320 | 0.886 | 0.031 | 0.654 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.459 | 0.455 | 0.541 | 0.001 | 0.434 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.145 | 0.277 | 0.855 | 0.037 | 0.652 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.376 | 0.258 | 0.624 | 0.239 | 0.582 |
| Lobby-Fueled Flooding | Portfolio hybrid legislature | 0.431 | 0.382 | 0.569 | 0.032 | 0.476 |
| Lobby-Fueled Flooding | Expanded portfolio hybrid legislature | 0.608 | 0.425 | 0.392 | 0.003 | 0.369 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.841 | 0.107 | 0.159 | 0.514 | 0.450 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.896 | 0.207 | 0.104 | 0.451 | 0.380 |
| Low-Revision-Moderation Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.380 | 0.980 | 0.011 | 0.678 |
| Low-Revision-Moderation Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.160 | 0.675 |
| Low-Revision-Moderation Flooding | Committee-first regular order | 0.092 | 0.285 | 0.908 | 0.072 | 0.683 |
| Low-Revision-Moderation Flooding | Parliamentary coalition confidence | 0.099 | 0.315 | 0.901 | 0.013 | 0.659 |
| Low-Revision-Moderation Flooding | Unicameral majority + pairwise alternatives | 0.496 | 0.461 | 0.504 | 0.001 | 0.414 |
| Low-Revision-Moderation Flooding | Citizen assembly threshold gate | 0.125 | 0.266 | 0.875 | 0.017 | 0.661 |
| Low-Revision-Moderation Flooding | Risk-routed majority legislature | 0.343 | 0.234 | 0.657 | 0.214 | 0.601 |
| Low-Revision-Moderation Flooding | Portfolio hybrid legislature | 0.433 | 0.399 | 0.568 | 0.026 | 0.469 |
| Low-Revision-Moderation Flooding | Expanded portfolio hybrid legislature | 0.692 | 0.433 | 0.308 | 0.001 | 0.324 |
| Low-Revision-Moderation Flooding | Default pass unless 2/3 block | 0.837 | 0.091 | 0.163 | 0.522 | 0.459 |
| Low-Revision-Moderation Flooding | Default pass + multi-round mediation + challenge | 0.884 | 0.189 | 0.116 | 0.444 | 0.390 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.015 | 0.366 | 0.985 | 0.006 | 0.684 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.231 | 0.687 |
| Capture Crisis | Committee-first regular order | 0.102 | 0.259 | 0.898 | 0.085 | 0.688 |
| Capture Crisis | Parliamentary coalition confidence | 0.070 | 0.334 | 0.930 | 0.028 | 0.670 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.406 | 0.456 | 0.594 | 0.001 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.112 | 0.271 | 0.888 | 0.046 | 0.672 |
| Capture Crisis | Risk-routed majority legislature | 0.325 | 0.257 | 0.675 | 0.233 | 0.607 |
| Capture Crisis | Portfolio hybrid legislature | 0.375 | 0.386 | 0.625 | 0.028 | 0.502 |
| Capture Crisis | Expanded portfolio hybrid legislature | 0.513 | 0.434 | 0.487 | 0.002 | 0.414 |
| Capture Crisis | Default pass unless 2/3 block | 0.841 | 0.099 | 0.159 | 0.519 | 0.453 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.889 | 0.206 | 0.111 | 0.448 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.074 | 0.375 | 0.926 | 0.003 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.195 | 0.593 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.224 | 0.280 | 0.776 | 0.086 | 0.621 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.271 | 0.283 | 0.729 | 0.066 | 0.592 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.545 | 0.544 | 0.455 | 0.001 | 0.364 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.250 | 0.277 | 0.750 | 0.046 | 0.601 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.505 | 0.267 | 0.495 | 0.219 | 0.511 |
| Popular Anti-Lobbying Push | Portfolio hybrid legislature | 0.524 | 0.411 | 0.476 | 0.053 | 0.425 |
| Popular Anti-Lobbying Push | Expanded portfolio hybrid legislature | 0.763 | 0.477 | 0.237 | 0.003 | 0.276 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.821 | 0.128 | 0.179 | 0.461 | 0.443 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.865 | 0.229 | 0.135 | 0.406 | 0.380 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.052 | 0.370 | 0.948 | 0.003 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.180 | 0.632 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.158 | 0.290 | 0.842 | 0.082 | 0.650 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.541 | 0.508 | 0.459 | 0.002 | 0.377 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.189 | 0.262 | 0.811 | 0.024 | 0.632 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.469 | 0.237 | 0.531 | 0.244 | 0.543 |
| Weighted Two-Party Baseline | Portfolio hybrid legislature | 0.521 | 0.408 | 0.479 | 0.035 | 0.424 |
| Weighted Two-Party Baseline | Expanded portfolio hybrid legislature | 0.794 | 0.455 | 0.206 | 0.003 | 0.267 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.835 | 0.108 | 0.165 | 0.498 | 0.450 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.826 | 0.205 | 0.174 | 0.416 | 0.409 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.393 | 0.950 | 0.000 | 0.657 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.193 | 0.637 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.161 | 0.277 | 0.839 | 0.098 | 0.656 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.253 | 0.256 | 0.747 | 0.087 | 0.614 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.544 | 0.510 | 0.456 | 0.002 | 0.376 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.193 | 0.263 | 0.807 | 0.035 | 0.632 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.489 | 0.235 | 0.511 | 0.266 | 0.538 |
| Weighted Two Major Plus Minors | Portfolio hybrid legislature | 0.519 | 0.408 | 0.481 | 0.043 | 0.427 |
| Weighted Two Major Plus Minors | Expanded portfolio hybrid legislature | 0.804 | 0.458 | 0.196 | 0.003 | 0.261 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.851 | 0.107 | 0.149 | 0.506 | 0.444 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.632 | 0.229 | 0.368 | 0.384 | 0.492 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.070 | 0.363 | 0.930 | 0.006 | 0.657 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.190 | 0.608 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.205 | 0.281 | 0.795 | 0.089 | 0.631 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.346 | 0.243 | 0.654 | 0.077 | 0.569 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.551 | 0.532 | 0.449 | 0.002 | 0.365 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.234 | 0.267 | 0.766 | 0.036 | 0.610 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.535 | 0.245 | 0.465 | 0.270 | 0.513 |
| Weighted Fragmented Multiparty | Portfolio hybrid legislature | 0.546 | 0.411 | 0.454 | 0.049 | 0.413 |
| Weighted Fragmented Multiparty | Expanded portfolio hybrid legislature | 0.821 | 0.469 | 0.179 | 0.004 | 0.250 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.837 | 0.122 | 0.163 | 0.481 | 0.441 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.635 | 0.244 | 0.365 | 0.361 | 0.482 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.048 | 0.384 | 0.952 | 0.003 | 0.661 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.181 | 0.628 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.174 | 0.290 | 0.826 | 0.092 | 0.644 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.204 | 0.283 | 0.796 | 0.047 | 0.622 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.552 | 0.522 | 0.448 | 0.002 | 0.368 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.200 | 0.271 | 0.800 | 0.029 | 0.625 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.481 | 0.241 | 0.519 | 0.252 | 0.538 |
| Weighted Dominant-Party Legislature | Portfolio hybrid legislature | 0.528 | 0.414 | 0.472 | 0.047 | 0.421 |
| Weighted Dominant-Party Legislature | Expanded portfolio hybrid legislature | 0.804 | 0.473 | 0.196 | 0.003 | 0.257 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.805 | 0.117 | 0.195 | 0.471 | 0.457 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.654 | 0.228 | 0.346 | 0.374 | 0.479 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.177 | 0.377 | 0.823 | 0.010 | 0.600 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.204 | 0.507 |
| Era 1 Low Contention | Committee-first regular order | 0.373 | 0.298 | 0.627 | 0.108 | 0.545 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.515 | 0.274 | 0.485 | 0.118 | 0.484 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.638 | 0.375 | 0.003 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.389 | 0.286 | 0.611 | 0.055 | 0.531 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.705 | 0.254 | 0.295 | 0.282 | 0.428 |
| Era 1 Low Contention | Portfolio hybrid legislature | 0.669 | 0.440 | 0.331 | 0.053 | 0.344 |
| Era 1 Low Contention | Expanded portfolio hybrid legislature | 0.891 | 0.518 | 0.109 | 0.007 | 0.201 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.853 | 0.178 | 0.147 | 0.405 | 0.401 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.782 | 0.252 | 0.218 | 0.335 | 0.400 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.111 | 0.377 | 0.889 | 0.008 | 0.633 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.219 | 0.564 |
| Era 2 Normal Contention | Committee-first regular order | 0.287 | 0.287 | 0.713 | 0.097 | 0.590 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.420 | 0.261 | 0.580 | 0.102 | 0.532 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.570 | 0.413 | 0.003 | 0.336 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.302 | 0.274 | 0.698 | 0.040 | 0.575 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.623 | 0.254 | 0.377 | 0.285 | 0.469 |
| Era 2 Normal Contention | Portfolio hybrid legislature | 0.613 | 0.417 | 0.387 | 0.056 | 0.379 |
| Era 2 Normal Contention | Expanded portfolio hybrid legislature | 0.864 | 0.483 | 0.136 | 0.005 | 0.224 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.845 | 0.149 | 0.155 | 0.454 | 0.424 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.736 | 0.246 | 0.264 | 0.372 | 0.433 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.061 | 0.380 | 0.939 | 0.005 | 0.656 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.184 | 0.612 |
| Era 3 Polarizing | Committee-first regular order | 0.196 | 0.287 | 0.804 | 0.092 | 0.634 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.301 | 0.259 | 0.699 | 0.072 | 0.587 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.553 | 0.510 | 0.447 | 0.002 | 0.371 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.224 | 0.269 | 0.776 | 0.027 | 0.613 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.507 | 0.250 | 0.493 | 0.254 | 0.522 |
| Era 3 Polarizing | Portfolio hybrid legislature | 0.537 | 0.398 | 0.463 | 0.045 | 0.421 |
| Era 3 Polarizing | Expanded portfolio hybrid legislature | 0.808 | 0.454 | 0.192 | 0.003 | 0.260 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.839 | 0.119 | 0.161 | 0.478 | 0.440 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.662 | 0.237 | 0.338 | 0.374 | 0.472 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.028 | 0.372 | 0.972 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.179 | 0.656 |
| Era 4 High Contention | Committee-first regular order | 0.126 | 0.280 | 0.874 | 0.080 | 0.669 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.122 | 0.308 | 0.878 | 0.025 | 0.652 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.517 | 0.475 | 0.483 | 0.001 | 0.399 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.153 | 0.262 | 0.847 | 0.027 | 0.650 |
| Era 4 High Contention | Risk-routed majority legislature | 0.401 | 0.246 | 0.599 | 0.232 | 0.572 |
| Era 4 High Contention | Portfolio hybrid legislature | 0.462 | 0.402 | 0.538 | 0.035 | 0.455 |
| Era 4 High Contention | Expanded portfolio hybrid legislature | 0.726 | 0.442 | 0.274 | 0.002 | 0.305 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.835 | 0.100 | 0.165 | 0.512 | 0.455 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.763 | 0.211 | 0.237 | 0.423 | 0.440 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.347 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.206 | 0.698 |
| Era 5 Capture Contention | Committee-first regular order | 0.083 | 0.264 | 0.918 | 0.066 | 0.693 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.436 | 0.428 | 0.564 | 0.002 | 0.454 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.106 | 0.259 | 0.894 | 0.031 | 0.675 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.320 | 0.242 | 0.680 | 0.216 | 0.611 |
| Era 5 Capture Contention | Portfolio hybrid legislature | 0.383 | 0.378 | 0.617 | 0.032 | 0.501 |
| Era 5 Capture Contention | Expanded portfolio hybrid legislature | 0.581 | 0.411 | 0.419 | 0.002 | 0.386 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.832 | 0.087 | 0.168 | 0.538 | 0.465 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.863 | 0.194 | 0.137 | 0.448 | 0.400 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.010 | 0.352 | 0.990 | 0.007 | 0.691 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.241 | 0.721 |
| Era 6 Crisis | Committee-first regular order | 0.062 | 0.258 | 0.938 | 0.099 | 0.711 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.355 | 0.413 | 0.645 | 0.003 | 0.499 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.080 | 0.267 | 0.920 | 0.030 | 0.686 |
| Era 6 Crisis | Risk-routed majority legislature | 0.275 | 0.238 | 0.725 | 0.229 | 0.637 |
| Era 6 Crisis | Portfolio hybrid legislature | 0.318 | 0.377 | 0.682 | 0.026 | 0.533 |
| Era 6 Crisis | Expanded portfolio hybrid legislature | 0.455 | 0.407 | 0.545 | 0.002 | 0.451 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.840 | 0.082 | 0.160 | 0.558 | 0.467 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.893 | 0.188 | 0.107 | 0.465 | 0.390 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.340 | 0.810 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.017 | 0.119 | 0.983 | 0.017 | 0.759 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.040 | 0.128 | 0.960 | 0.148 | 0.771 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.642 | 0.500 | 0.358 | 0.001 | 0.329 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.080 | 0.109 | 0.920 | 0.047 | 0.737 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.625 | 0.186 | 0.375 | 0.172 | 0.466 |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature | 0.794 | 0.507 | 0.206 | 0.000 | 0.251 |
| Adversarial High-Benefit Extreme Reform | Expanded portfolio hybrid legislature | 0.992 | 0.528 | 0.008 | 0.000 | 0.145 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.908 | 0.046 | 0.092 | 0.575 | 0.447 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.770 | 0.183 | 0.230 | 0.245 | 0.409 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.206 | 0.404 | 0.794 | 0.001 | 0.576 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.010 | 0.280 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.620 | 0.319 | 0.380 | 0.064 | 0.407 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.422 | 0.407 | 0.578 | 0.001 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.208 | 0.420 | 0.792 | 0.203 | 0.611 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.979 | 0.361 | 0.021 | 0.009 | 0.204 |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature | 0.367 | 0.505 | 0.633 | 0.000 | 0.465 |
| Adversarial Popular Harmful Bill | Expanded portfolio hybrid legislature | 0.898 | 0.519 | 0.102 | 0.000 | 0.195 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 1.000 | 0.262 | 0.000 | 0.013 | 0.224 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.989 | 0.359 | 0.011 | 0.010 | 0.200 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.059 | 0.552 | 0.941 | 0.002 | 0.605 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.290 | 0.226 |
| Adversarial Moderate Capture | Committee-first regular order | 0.837 | 0.497 | 0.163 | 0.273 | 0.287 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.849 | 0.533 | 0.151 | 0.106 | 0.237 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.568 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.421 | 0.532 | 0.579 | 0.477 | 0.525 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.987 | 0.525 | 0.013 | 0.243 | 0.198 |
| Adversarial Moderate Capture | Portfolio hybrid legislature | 0.190 | 0.488 | 0.810 | 0.015 | 0.562 |
| Adversarial Moderate Capture | Expanded portfolio hybrid legislature | 0.576 | 0.514 | 0.424 | 0.001 | 0.358 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.308 | 0.215 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.992 | 0.524 | 0.008 | 0.247 | 0.196 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.003 | 0.283 | 0.997 | 0.045 | 0.723 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.593 | 0.752 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.137 | 0.283 | 0.863 | 0.082 | 0.663 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.203 | 0.277 | 0.797 | 0.387 | 0.693 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.488 | 0.477 | 0.512 | 0.005 | 0.414 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.268 | 0.237 | 0.732 | 0.051 | 0.605 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.686 | 0.266 | 0.314 | 0.357 | 0.449 |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature | 0.708 | 0.473 | 0.293 | 0.005 | 0.305 |
| Adversarial Delayed-Benefit Reform | Expanded portfolio hybrid legislature | 0.985 | 0.495 | 0.015 | 0.000 | 0.159 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.856 | 0.113 | 0.144 | 0.751 | 0.488 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.838 | 0.260 | 0.162 | 0.429 | 0.388 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.048 | 0.373 | 0.952 | 0.003 | 0.665 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.117 | 0.495 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.273 | 0.302 | 0.727 | 0.121 | 0.597 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.384 | 0.306 | 0.616 | 0.027 | 0.522 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.476 | 0.519 | 0.524 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.073 | 0.387 | 0.927 | 0.059 | 0.659 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.772 | 0.287 | 0.228 | 0.083 | 0.344 |
| Adversarial Concentrated Rights Harm | Portfolio hybrid legislature | 0.438 | 0.462 | 0.562 | 0.001 | 0.443 |
| Adversarial Concentrated Rights Harm | Expanded portfolio hybrid legislature | 0.913 | 0.491 | 0.087 | 0.000 | 0.196 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.980 | 0.174 | 0.020 | 0.191 | 0.296 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.838 | 0.285 | 0.162 | 0.104 | 0.316 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.043 | 0.373 | 0.957 | 0.013 | 0.669 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.295 | 0.614 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.203 | 0.295 | 0.797 | 0.192 | 0.649 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.316 | 0.315 | 0.684 | 0.112 | 0.570 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.416 | 0.497 | 0.584 | 0.003 | 0.444 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.273 | 0.327 | 0.727 | 0.036 | 0.573 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.406 | 0.332 | 0.594 | 0.245 | 0.547 |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature | 0.591 | 0.444 | 0.409 | 0.007 | 0.373 |
| Adversarial Anti-Lobbying Backlash | Expanded portfolio hybrid legislature | 0.767 | 0.472 | 0.233 | 0.000 | 0.275 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.899 | 0.208 | 0.101 | 0.578 | 0.404 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.707 | 0.316 | 0.293 | 0.461 | 0.444 |
| Adversarial Revision Dilution | Stylized U.S.-like conventional benchmark | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Adversarial Revision Dilution | Unicameral simple majority | 0.051 | 0.129 | 0.949 | 0.422 | 0.820 |
| Adversarial Revision Dilution | Committee-first regular order | 0.017 | 0.159 | 0.983 | 0.016 | 0.747 |
| Adversarial Revision Dilution | Parliamentary coalition confidence | 0.036 | 0.156 | 0.964 | 0.230 | 0.781 |
| Adversarial Revision Dilution | Unicameral majority + pairwise alternatives | 0.560 | 0.487 | 0.440 | 0.002 | 0.374 |
| Adversarial Revision Dilution | Citizen assembly threshold gate | 0.113 | 0.124 | 0.887 | 0.033 | 0.713 |
| Adversarial Revision Dilution | Risk-routed majority legislature | 0.559 | 0.190 | 0.441 | 0.253 | 0.514 |
| Adversarial Revision Dilution | Portfolio hybrid legislature | 0.755 | 0.494 | 0.245 | 0.001 | 0.275 |
| Adversarial Revision Dilution | Expanded portfolio hybrid legislature | 0.981 | 0.517 | 0.019 | 0.000 | 0.154 |
| Adversarial Revision Dilution | Default pass unless 2/3 block | 0.897 | 0.055 | 0.103 | 0.668 | 0.468 |
| Adversarial Revision Dilution | Default pass + multi-round mediation + challenge | 0.738 | 0.186 | 0.262 | 0.346 | 0.444 |
| Adversarial Lobby Information | Stylized U.S.-like conventional benchmark | 0.117 | 0.391 | 0.883 | 0.012 | 0.627 |
| Adversarial Lobby Information | Unicameral simple majority | 0.772 | 0.271 | 0.228 | 0.225 | 0.378 |
| Adversarial Lobby Information | Committee-first regular order | 0.640 | 0.303 | 0.360 | 0.018 | 0.393 |
| Adversarial Lobby Information | Parliamentary coalition confidence | 0.579 | 0.329 | 0.421 | 0.086 | 0.429 |
| Adversarial Lobby Information | Unicameral majority + pairwise alternatives | 0.834 | 0.567 | 0.166 | 0.000 | 0.213 |
| Adversarial Lobby Information | Citizen assembly threshold gate | 0.745 | 0.279 | 0.255 | 0.030 | 0.350 |
| Adversarial Lobby Information | Risk-routed majority legislature | 0.884 | 0.286 | 0.116 | 0.202 | 0.312 |
| Adversarial Lobby Information | Portfolio hybrid legislature | 0.862 | 0.424 | 0.138 | 0.007 | 0.243 |
| Adversarial Lobby Information | Expanded portfolio hybrid legislature | 0.976 | 0.551 | 0.024 | 0.000 | 0.146 |
| Adversarial Lobby Information | Default pass unless 2/3 block | 0.996 | 0.232 | 0.004 | 0.281 | 0.288 |
| Adversarial Lobby Information | Default pass + multi-round mediation + challenge | 0.912 | 0.283 | 0.088 | 0.213 | 0.302 |
| Adversarial Public Opinion Error | Stylized U.S.-like conventional benchmark | 0.035 | 0.372 | 0.965 | 0.008 | 0.673 |
| Adversarial Public Opinion Error | Unicameral simple majority | 0.309 | 0.247 | 0.691 | 0.244 | 0.620 |
| Adversarial Public Opinion Error | Committee-first regular order | 0.152 | 0.292 | 0.848 | 0.136 | 0.664 |
| Adversarial Public Opinion Error | Parliamentary coalition confidence | 0.239 | 0.307 | 0.761 | 0.175 | 0.623 |
| Adversarial Public Opinion Error | Unicameral majority + pairwise alternatives | 0.654 | 0.513 | 0.346 | 0.001 | 0.319 |
| Adversarial Public Opinion Error | Citizen assembly threshold gate | 0.140 | 0.280 | 0.860 | 0.073 | 0.661 |
| Adversarial Public Opinion Error | Risk-routed majority legislature | 0.724 | 0.282 | 0.276 | 0.175 | 0.388 |
| Adversarial Public Opinion Error | Portfolio hybrid legislature | 0.644 | 0.490 | 0.356 | 0.003 | 0.332 |
| Adversarial Public Opinion Error | Expanded portfolio hybrid legislature | 0.939 | 0.500 | 0.061 | 0.000 | 0.180 |
| Adversarial Public Opinion Error | Default pass unless 2/3 block | 0.892 | 0.126 | 0.108 | 0.406 | 0.398 |
| Adversarial Public Opinion Error | Default pass + multi-round mediation + challenge | 0.881 | 0.274 | 0.119 | 0.244 | 0.326 |

## Burden-Shifting Side Note: Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from automatic passage into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.392 | -0.257 | 0.021 | -0.070 | -0.299 | -0.143 | 0.500 |
| Low Polarization | -11.392 | -0.190 | 0.029 | -0.136 | -0.146 | -0.066 | 0.500 |
| High Polarization | -17.008 | -0.283 | 0.012 | -0.030 | -0.358 | -0.160 | 0.500 |
| Low Party Loyalty | -15.133 | -0.252 | 0.029 | -0.087 | -0.295 | -0.136 | 0.500 |
| High Party Loyalty | -15.617 | -0.260 | 0.022 | -0.073 | -0.303 | -0.142 | 0.500 |
| Low Revision-Moderation Culture | -15.958 | -0.266 | 0.021 | -0.054 | -0.308 | -0.144 | 0.500 |
| High Revision-Moderation Culture | -14.850 | -0.248 | 0.026 | -0.102 | -0.284 | -0.135 | 0.500 |
| Low Lobbying Pressure | -15.742 | -0.262 | 0.023 | -0.073 | -0.300 | -0.139 | 0.500 |
| High Lobbying Pressure | -15.258 | -0.254 | 0.018 | -0.055 | -0.296 | -0.141 | 0.500 |
| Weak Constituency Pressure | -18.458 | -0.308 | 0.024 | -0.069 | -0.333 | -0.146 | 0.499 |
| Two-Party System | -6.600 | -0.110 | -0.007 | -0.018 | -0.142 | -0.075 | 0.333 |
| Multi-Party System | -30.292 | -0.505 | 0.116 | -0.295 | -0.529 | -0.328 | 0.802 |
| High Proposal Pressure | 3.158 | 0.018 | -0.016 | 0.010 | -0.028 | -0.054 | 0.167 |
| Extreme Proposal Pressure | 21.842 | 0.073 | -0.022 | 0.022 | 0.021 | -0.047 | 0.100 |
| Lobby-Fueled Flooding | 2.733 | 0.015 | -0.016 | 0.009 | -0.032 | -0.055 | 0.167 |
| Low-Revision-Moderation Flooding | 2.183 | 0.012 | -0.017 | 0.020 | -0.050 | -0.074 | 0.167 |
| Capture Crisis | 2.217 | 0.012 | -0.014 | 0.015 | -0.042 | -0.065 | 0.167 |
| Popular Anti-Lobbying Push | -1.550 | -0.013 | -0.014 | -0.006 | -0.052 | -0.057 | 0.250 |
| Weighted Two-Party Baseline | -6.183 | -0.103 | -0.005 | -0.018 | -0.149 | -0.087 | 0.333 |
| Weighted Two Major Plus Minors | -31.000 | -0.517 | 0.113 | -0.281 | -0.545 | -0.344 | 0.799 |
| Weighted Fragmented Multiparty | -29.558 | -0.493 | 0.117 | -0.363 | -0.488 | -0.308 | 0.854 |
| Weighted Dominant-Party Legislature | -20.000 | -0.333 | 0.041 | -0.155 | -0.345 | -0.177 | 0.667 |
| Era 1 Low Contention | -16.525 | -0.275 | 0.054 | -0.224 | -0.239 | -0.117 | 0.660 |
| Era 2 Normal Contention | -23.067 | -0.384 | 0.086 | -0.290 | -0.370 | -0.210 | 0.727 |
| Era 3 Polarizing | -28.250 | -0.471 | 0.104 | -0.295 | -0.496 | -0.324 | 0.779 |
| Era 4 High Contention | -13.508 | -0.180 | 0.001 | -0.023 | -0.219 | -0.099 | 0.400 |
| Era 5 Capture Contention | -2.383 | -0.026 | -0.015 | 0.024 | -0.096 | -0.090 | 0.222 |
| Era 6 Crisis | 1.508 | 0.013 | -0.016 | 0.030 | -0.061 | -0.085 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.250 | -0.554 | -0.002 | -0.005 | -0.591 | -0.184 | 0.665 |
| Adversarial Popular Harmful Bill | -6.267 | -0.104 | 0.000 | -0.092 | -0.092 | -0.050 | 0.461 |
| Adversarial Moderate Capture | -1.183 | -0.020 | -0.000 | -0.020 | -0.009 | -0.002 | 0.330 |
| Adversarial Delayed-Benefit Reform | -27.208 | -0.453 | 0.000 | -0.095 | -0.438 | -0.226 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.858 | -0.398 | 0.030 | -0.227 | -0.332 | -0.183 | 0.651 |
| Adversarial Anti-Lobbying Backlash | -22.825 | -0.380 | 0.044 | -0.168 | -0.259 | -0.154 | 0.648 |
| Adversarial Revision Dilution | -32.800 | -0.547 | -0.001 | 0.015 | -0.582 | -0.188 | 0.663 |
| Adversarial Lobby Information | -10.667 | -0.178 | -0.001 | -0.133 | -0.142 | -0.067 | 0.470 |
| Adversarial Public Opinion Error | -25.525 | -0.425 | -0.020 | -0.157 | -0.422 | -0.202 | 0.664 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-public-support enactment |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.763) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Cloture, conference, and judicial review (0.741) | Expanded portfolio hybrid legislature (0.868) | Unicameral majority + pairwise alternatives (0.001) |
| High Polarization | Committee amendment and revision power (0.766) | Default pass unless 2/3 block (0.839) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.759) | Default pass unless 2/3 block (0.842) | Unicameral majority + pairwise alternatives (0.003) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.755) | Default pass unless 2/3 block (0.842) | Unicameral majority + pairwise alternatives (0.002) |
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark (0.767) | Default pass unless 2/3 block (0.827) | Stylized U.S.-like conventional benchmark (0.000) |
| High Revision-Moderation Culture | Committee amendment and revision power (0.745) | Default pass unless 2/3 block (0.855) | Committee amendment and revision power (0.002) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Expanded portfolio hybrid legislature (0.864) | Pairwise amendment tournament + majority (0.003) |
| High Lobbying Pressure | Committee amendment and revision power (0.764) | Default pass unless 2/3 block (0.831) | Expanded portfolio hybrid legislature (0.002) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.877) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Committee amendment and revision power (0.755) | Default pass unless 2/3 block (0.846) | Parliamentary coalition confidence (0.000) |
| Multi-Party System | Committee amendment and revision power (0.746) | Default pass unless 2/3 block (0.837) | Unicameral majority + pairwise alternatives (0.003) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.756) | Default pass + multi-round mediation + challenge (0.903) | Unicameral majority + pairwise alternatives (0.001) |
| Extreme Proposal Pressure | Committee amendment and revision power (0.750) | Default pass + multi-round mediation + challenge (0.941) | Pairwise amendment tournament + majority (0.000) |
| Lobby-Fueled Flooding | Committee amendment and revision power (0.757) | Default pass + multi-round mediation + challenge (0.896) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Revision-Moderation Flooding | Committee amendment and revision power (0.763) | Default pass + multi-round mediation + challenge (0.884) | Unicameral majority + pairwise alternatives (0.001) |
| Capture Crisis | Parliamentary coalition confidence (0.751) | Default pass + multi-round mediation + challenge (0.889) | Pairwise amendment tournament + majority (0.001) |
| Popular Anti-Lobbying Push | Committee amendment and revision power (0.770) | Default pass + multi-round mediation + challenge (0.865) | Unicameral majority + pairwise alternatives (0.001) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.835) | Parliamentary coalition confidence (0.000) |
| Weighted Two Major Plus Minors | Committee amendment and revision power (0.754) | Default pass unless 2/3 block (0.851) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Cloture, conference, and judicial review (0.746) | Default pass unless 2/3 block (0.837) | Pairwise amendment tournament + majority (0.002) |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark (0.745) | Default pass unless 2/3 block (0.805) | Unicameral majority + pairwise alternatives (0.002) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.730) | Expanded portfolio hybrid legislature (0.891) | Pairwise amendment tournament + majority (0.002) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.753) | Expanded portfolio hybrid legislature (0.864) | Pairwise amendment tournament + majority (0.003) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.839) | Pairwise amendment tournament + majority (0.001) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.769) | Default pass unless 2/3 block (0.835) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Committee amendment and revision power (0.759) | Default pass + multi-round mediation + challenge (0.863) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Committee amendment and revision power (0.766) | Default pass + multi-round mediation + challenge (0.893) | Parliamentary coalition confidence (0.000) |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature (0.834) | Expanded portfolio hybrid legislature (0.992) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature (0.342) | Default pass unless 2/3 block (1.000) | Committee amendment and revision power (0.000) |
| Adversarial Moderate Capture | Committee discharge-petition target (0.470) | Default pass unless 2/3 block (1.000) | Committee amendment and revision power (0.000) |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature (0.819) | Expanded portfolio hybrid legislature (0.985) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.621) | Default pass unless 2/3 block (0.980) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature (0.730) | Default pass unless 2/3 block (0.899) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Revision Dilution | Portfolio hybrid legislature (0.882) | Expanded portfolio hybrid legislature (0.981) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Lobby Information | Unicameral majority + pairwise alternatives (0.781) | Default pass unless 2/3 block (0.996) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Public Opinion Error | Committee amendment and revision power (0.724) | Expanded portfolio hybrid legislature (0.939) | Expanded portfolio hybrid legislature (0.000) |

## Interpretation

- This paper campaign compares representative conventional, committee, coalition, tournament, citizen-review, agenda-scarcity, proposal-accountability, harm/compensation, anti-capture, adaptive-routing, law-registry, and burden-shifting mechanisms under shared synthetic worlds.
- Open burden-shifting passage remains the throughput extreme, but its high low-public-support enactment and policy movement make it a diagnostic endpoint.
- Policy tournaments and risk-routed majority systems occupy a promising revision-moderation/productivity middle ground in this synthetic campaign, but tournament variants remain sensitive to clone, decoy, and overload stress; committee-first, public-interest, citizen, and parliamentary-style gates control risk but give up substantial throughput.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality, and generated welfare remains conditional on model assumptions.
- Future model extensions should deepen multidimensional package bargaining, judicial/court intervention, executive emergency/delegated rulemaking, direct-democracy routes, electoral feedback, and media/information ecosystems.

## Reproduction

```sh
make campaign
```
