# Main Comparison Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 46
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

- The main comparison campaign compares 46 scenario families across the same synthetic worlds, including a small burden-shifting stress-test family.
- The scalar directional score is productivity-sensitive: its highest value came from Default pass unless 2/3 block at 0.726, which is why the report treats the score as a profile aid rather than a recommendation.
- Highest average welfare came from Committee amendment and revision power at 0.721; highest revision moderation came from Unicameral majority + pairwise alternatives at 0.505.
- Highest productivity came from Default pass unless 2/3 block at 0.866.
- Open burden-shifting passage averaged 0.866 productivity, 0.474 low-public-support enactment, and 0.629 policy shift, so it functions as a throughput/risk endpoint.
- The stylized U.S.-like conventional benchmark averaged 0.055 productivity and 0.677 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.
- The portfolio hybrid combines risk routing, pairwise alternatives, citizen/harm review, proposal bonds, anti-capture safeguards, and law review. It averaged 0.526 productivity, 0.421 revision moderation, 0.931 risk control, and 0.711 directional score, situating it between pairwise alternatives and risk routing rather than replacing the tradeoff frontier.
- The expanded portfolio hybrid adds district-public, long-horizon strategy, omnibus bargaining, influence-system, and constitutional-court architecture proxies. It averaged 0.788 productivity, 0.466 revision moderation, 0.903 risk control, and 0.684 directional score; its value is diagnostic because extra safeguards also increase complexity.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, revision moderation, public alignment, and legitimacy. Risk control inverts chamber low-support passage, low-public-support enactment, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Low-public-support enactment ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.647 | 0.571 | 0.877 | 0.967 | 0.171 | 13.689 | 39.882 | 0.636 | 0.000 | 0.188 | 0.033 | 0.114 | 0.543 | 0.061 | 0.288 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.375 | 0.000 | 0.465 |
| Anti-capture proposal access + majority | 0.668 | 0.576 | 0.884 | 0.938 | 0.276 | 22.457 | 76.296 | 0.643 | 0.000 | 0.193 | 0.062 | 0.108 | 0.541 | 0.103 | 0.300 | 0.138 | 0.000 | 0.000 | 0.000 | 0.000 | 0.654 | 0.000 | 0.890 |
| Majority + anti-capture bundle | 0.679 | 0.580 | 0.884 | 0.934 | 0.316 | 25.548 | 80.738 | 0.659 | 0.000 | 0.148 | 0.066 | 0.115 | 0.546 | 0.119 | 0.303 | 0.133 | 0.101 | 0.552 | 0.000 | 0.000 | 0.720 | 0.000 | 0.937 |
| Bicameral simple majority | 0.654 | 0.587 | 0.878 | 0.930 | 0.222 | 16.933 | 86.029 | 0.636 | 0.000 | 0.155 | 0.070 | 0.113 | 0.559 | 0.064 | 0.223 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.451 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.635 | 0.611 | 0.906 | 0.810 | 0.211 | 16.707 | 86.029 | 0.696 | 0.000 | 0.055 | 0.190 | 0.089 | 0.623 | 0.068 | 0.252 | 0.211 | 0.000 | 0.000 | 0.000 | 0.000 | 0.564 | 0.000 | 1.000 |
| Citizen initiative and referendum | 0.693 | 0.580 | 0.833 | 0.930 | 0.431 | 35.285 | 86.029 | 0.601 | 0.000 | 0.229 | 0.070 | 0.131 | 0.533 | 0.206 | 0.406 | 0.239 | 0.000 | 0.000 | 0.000 | 0.000 | 0.836 | 0.000 | 1.000 |
| Citizen agenda petitions + majority | 0.662 | 0.583 | 0.910 | 0.953 | 0.201 | 15.850 | 36.085 | 0.654 | 0.000 | 0.080 | 0.047 | 0.075 | 0.575 | 0.073 | 0.308 | 0.150 | 0.000 | 0.000 | 0.095 | 0.048 | 0.653 | 0.000 | 0.429 |
| Cloture, conference, and judicial review | 0.644 | 0.626 | 0.929 | 0.967 | 0.053 | 3.968 | 22.929 | 0.691 | 0.000 | 0.035 | 0.033 | 0.088 | 0.613 | 0.010 | 0.150 | 0.201 | 0.000 | 0.000 | 0.069 | 0.000 | 0.162 | 0.000 | 0.278 |
| Committee amendment and revision power | 0.651 | 0.620 | 0.932 | 0.929 | 0.121 | 9.795 | 12.264 | 0.721 | 0.000 | 0.014 | 0.071 | 0.072 | 0.605 | 0.032 | 0.211 | 0.156 | 0.000 | 0.000 | 0.130 | 0.031 | 0.449 | 0.000 | 0.148 |
| Committee discharge-petition target | 0.653 | 0.613 | 0.926 | 0.923 | 0.149 | 11.896 | 14.778 | 0.692 | 0.000 | 0.045 | 0.077 | 0.065 | 0.598 | 0.041 | 0.219 | 0.183 | 0.000 | 0.000 | 0.167 | 0.047 | 0.448 | 0.000 | 0.182 |
| Committee-first regular order | 0.665 | 0.593 | 0.892 | 0.968 | 0.209 | 15.989 | 20.749 | 0.653 | 0.000 | 0.092 | 0.032 | 0.114 | 0.550 | 0.057 | 0.209 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.447 | 0.000 | 0.265 |
| Compensation amendments + majority | 0.662 | 0.564 | 0.835 | 0.930 | 0.318 | 24.961 | 86.029 | 0.610 | 0.000 | 0.217 | 0.070 | 0.091 | 0.539 | 0.114 | 0.296 | 0.255 | 0.000 | 0.000 | 0.000 | 0.164 | 0.616 | 0.000 | 1.000 |
| Constitutional court architecture | 0.652 | 0.565 | 0.836 | 0.892 | 0.318 | 24.945 | 86.029 | 0.610 | 0.000 | 0.217 | 0.108 | 0.089 | 0.540 | 0.113 | 0.295 | 0.255 | 0.000 | 0.000 | 0.000 | 0.169 | 0.616 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.650 | 0.630 | 0.931 | 0.984 | 0.055 | 4.179 | 19.097 | 0.677 | 0.000 | 0.007 | 0.016 | 0.066 | 0.659 | 0.011 | 0.145 | 0.202 | 0.000 | 0.000 | 0.000 | 0.000 | 0.173 | 0.000 | 0.224 |
| Default pass unless 2/3 block | 0.726 | 0.479 | 0.630 | 0.930 | 0.866 | 73.834 | 86.029 | 0.515 | 0.417 | 0.474 | 0.070 | 0.185 | 0.392 | 0.629 | 0.603 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 | 0.986 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.682 | 0.495 | 0.705 | 0.892 | 0.635 | 60.596 | 86.029 | 0.532 | 0.332 | 0.438 | 0.108 | 0.175 | 0.410 | 0.377 | 0.468 | 0.264 | 0.000 | 0.000 | 0.000 | 0.000 | 0.835 | 0.470 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.708 | 0.513 | 0.727 | 0.793 | 0.799 | 71.391 | 86.029 | 0.478 | 0.244 | 0.370 | 0.207 | 0.114 | 0.451 | 0.279 | 0.316 | 0.283 | 0.000 | 0.000 | 0.738 | 0.274 | 0.862 | 0.424 | 1.000 |
| District-population public-will model | 0.657 | 0.565 | 0.859 | 0.930 | 0.273 | 21.237 | 86.029 | 0.627 | 0.000 | 0.329 | 0.070 | 0.127 | 0.456 | 0.083 | 0.252 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.551 | 0.000 | 1.000 |
| Expanded portfolio hybrid legislature | 0.684 | 0.628 | 0.903 | 0.416 | 0.788 | 65.097 | 78.528 | 0.571 | 0.000 | 0.002 | 0.584 | 0.047 | 0.585 | 0.045 | 0.033 | 0.227 | 0.460 | 0.385 | 1.000 | 0.652 | 0.806 | 0.000 | 0.915 |
| Harm-weighted double majority | 0.663 | 0.571 | 0.876 | 0.930 | 0.275 | 21.955 | 86.029 | 0.624 | 0.000 | 0.211 | 0.070 | 0.108 | 0.536 | 0.093 | 0.276 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 | 0.572 | 0.000 | 1.000 |
| Campaign-finance influence system | 0.676 | 0.573 | 0.871 | 0.937 | 0.321 | 25.925 | 77.045 | 0.631 | 0.000 | 0.145 | 0.063 | 0.116 | 0.552 | 0.123 | 0.309 | 0.207 | 0.460 | 0.382 | 0.000 | 0.000 | 0.660 | 0.000 | 0.899 |
| Active-law registry + majority review | 0.656 | 0.556 | 0.835 | 0.890 | 0.345 | 27.398 | 86.029 | 0.603 | 0.000 | 0.253 | 0.110 | 0.132 | 0.510 | 0.193 | 0.340 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.637 | 0.000 | 1.000 |
| Leadership agenda cartel + majority | 0.658 | 0.587 | 0.905 | 0.973 | 0.167 | 13.488 | 32.981 | 0.660 | 0.000 | 0.121 | 0.027 | 0.094 | 0.576 | 0.051 | 0.227 | 0.154 | 0.000 | 0.000 | 0.000 | 0.000 | 0.576 | 0.000 | 0.389 |
| Long-horizon strategic learning | 0.681 | 0.540 | 0.797 | 0.790 | 0.597 | 48.425 | 85.956 | 0.498 | 0.000 | 0.245 | 0.210 | 0.109 | 0.502 | 0.201 | 0.316 | 0.301 | 0.158 | 0.650 | 0.999 | 0.268 | 0.649 | 0.000 | 0.999 |
| Multidimensional package bargaining + majority | 0.640 | 0.558 | 0.835 | 0.826 | 0.339 | 26.586 | 86.029 | 0.591 | 0.000 | 0.224 | 0.174 | 0.100 | 0.529 | 0.124 | 0.311 | 0.261 | 0.000 | 0.000 | 0.373 | 0.373 | 0.636 | 0.000 | 1.000 |
| Endogenous norm erosion + majority | 0.632 | 0.558 | 0.844 | 0.800 | 0.324 | 25.537 | 81.289 | 0.612 | 0.000 | 0.252 | 0.200 | 0.125 | 0.510 | 0.116 | 0.321 | 0.257 | 0.000 | 0.000 | 0.951 | 0.020 | 0.598 | 0.000 | 0.951 |
| Omnibus bargaining + majority | 0.629 | 0.560 | 0.847 | 0.738 | 0.372 | 29.161 | 86.029 | 0.586 | 0.000 | 0.162 | 0.262 | 0.077 | 0.546 | 0.141 | 0.317 | 0.261 | 0.000 | 0.000 | 0.686 | 0.686 | 0.662 | 0.000 | 1.000 |
| Open-rule floor calendar + majority | 0.663 | 0.553 | 0.842 | 0.902 | 0.353 | 28.102 | 80.883 | 0.579 | 0.000 | 0.255 | 0.098 | 0.117 | 0.506 | 0.128 | 0.321 | 0.271 | 0.000 | 0.000 | 0.149 | 0.083 | 0.610 | 0.000 | 0.948 |
| Package bargaining + majority | 0.655 | 0.561 | 0.842 | 0.890 | 0.326 | 25.616 | 86.029 | 0.610 | 0.000 | 0.226 | 0.110 | 0.114 | 0.525 | 0.118 | 0.302 | 0.258 | 0.000 | 0.000 | 0.285 | 0.285 | 0.619 | 0.000 | 1.000 |
| Pairwise amendment tournament + majority | 0.713 | 0.658 | 0.937 | 0.714 | 0.544 | 45.246 | 47.890 | 0.639 | 0.000 | 0.002 | 0.286 | 0.056 | 0.640 | 0.005 | 0.004 | 0.227 | 0.000 | 0.000 | 0.567 | 0.000 | 0.789 | 0.000 | 0.567 |
| Parliamentary coalition confidence | 0.665 | 0.544 | 0.906 | 0.980 | 0.230 | 17.269 | 21.442 | 0.603 | 0.000 | 0.073 | 0.020 | 0.078 | 0.553 | 0.063 | 0.188 | 0.175 | 0.000 | 0.000 | 0.000 | 0.000 | 0.558 | 0.000 | 0.284 |
| Portfolio hybrid legislature | 0.711 | 0.627 | 0.931 | 0.761 | 0.526 | 43.418 | 54.481 | 0.630 | 0.000 | 0.030 | 0.239 | 0.064 | 0.599 | 0.074 | 0.086 | 0.146 | 0.105 | 0.598 | 0.427 | 0.016 | 0.771 | 0.000 | 0.640 |
| Bicameral majority + presidential veto | 0.642 | 0.600 | 0.891 | 0.930 | 0.149 | 11.272 | 86.029 | 0.648 | 0.000 | 0.124 | 0.070 | 0.106 | 0.580 | 0.039 | 0.210 | 0.259 | 0.000 | 0.000 | 0.000 | 0.000 | 0.309 | 0.000 | 1.000 |
| Majority + proportional committee assignment | 0.659 | 0.580 | 0.875 | 0.944 | 0.237 | 18.197 | 25.563 | 0.636 | 0.000 | 0.151 | 0.056 | 0.124 | 0.531 | 0.073 | 0.249 | 0.270 | 0.000 | 0.000 | 0.000 | 0.000 | 0.465 | 0.000 | 0.322 |
| Proposal bonds + majority | 0.666 | 0.563 | 0.852 | 0.931 | 0.317 | 24.899 | 84.831 | 0.616 | 0.000 | 0.218 | 0.069 | 0.125 | 0.524 | 0.113 | 0.293 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.619 | 0.000 | 0.993 |
| Majority + public-interest screen | 0.660 | 0.569 | 0.870 | 0.939 | 0.260 | 20.872 | 74.397 | 0.635 | 0.000 | 0.193 | 0.061 | 0.115 | 0.537 | 0.096 | 0.291 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.529 | 0.000 | 0.866 |
| Public objection window + majority | 0.644 | 0.588 | 0.892 | 0.866 | 0.229 | 17.960 | 86.029 | 0.648 | 0.000 | 0.128 | 0.134 | 0.098 | 0.572 | 0.063 | 0.213 | 0.210 | 0.000 | 0.000 | 0.000 | 0.000 | 0.555 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.621 | 0.575 | 0.878 | 0.779 | 0.251 | 18.997 | 48.519 | 0.633 | 0.000 | 0.184 | 0.221 | 0.109 | 0.545 | 0.077 | 0.243 | 0.224 | 0.000 | 0.000 | 0.000 | 0.000 | 0.548 | 0.000 | 0.609 |
| Random public review panel + majority | 0.636 | 0.604 | 0.898 | 0.810 | 0.232 | 18.403 | 86.029 | 0.681 | 0.000 | 0.076 | 0.190 | 0.095 | 0.619 | 0.077 | 0.263 | 0.218 | 0.000 | 0.000 | 0.000 | 0.000 | 0.576 | 0.000 | 1.000 |
| Risk-routed majority legislature | 0.688 | 0.546 | 0.839 | 0.830 | 0.537 | 42.825 | 86.029 | 0.522 | 0.000 | 0.235 | 0.170 | 0.102 | 0.511 | 0.185 | 0.319 | 0.286 | 0.000 | 0.000 | 0.649 | 0.226 | 0.679 | 0.000 | 1.000 |
| Unicameral simple majority | 0.666 | 0.562 | 0.852 | 0.930 | 0.318 | 24.990 | 86.029 | 0.615 | 0.000 | 0.218 | 0.070 | 0.125 | 0.524 | 0.114 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.617 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.714 | 0.657 | 0.937 | 0.712 | 0.549 | 45.664 | 48.312 | 0.639 | 0.000 | 0.002 | 0.288 | 0.056 | 0.641 | 0.005 | 0.004 | 0.227 | 0.000 | 0.000 | 0.572 | 0.000 | 0.793 | 0.000 | 0.572 |
| Pairwise alternatives + no support/revision vote kernel | 0.624 | 0.585 | 0.914 | 0.711 | 0.286 | 23.288 | 48.705 | 0.614 | 0.000 | 0.007 | 0.289 | 0.062 | 0.602 | 0.004 | 0.008 | 0.312 | 0.000 | 0.000 | 0.578 | 0.000 | 0.223 | 0.000 | 0.578 |
| Unicameral majority + mediation | 0.639 | 0.548 | 0.801 | 0.815 | 0.393 | 31.374 | 86.029 | 0.589 | 0.000 | 0.278 | 0.185 | 0.106 | 0.509 | 0.155 | 0.377 | 0.274 | 0.000 | 0.000 | 0.824 | 0.176 | 0.653 | 0.000 | 1.000 |
| Simple majority + no support/revision vote kernel | 0.611 | 0.520 | 0.830 | 0.930 | 0.165 | 12.835 | 86.029 | 0.576 | 0.000 | 0.399 | 0.070 | 0.155 | 0.437 | 0.047 | 0.246 | 0.324 | 0.000 | 0.000 | 0.000 | 0.000 | 0.218 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.648 | 0.627 | 0.904 | 0.930 | 0.131 | 9.601 | 86.029 | 0.667 | 0.000 | 0.061 | 0.070 | 0.099 | 0.615 | 0.027 | 0.151 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.270 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - revision moderation) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, produces less revision moderation, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Revision moderation | Gridlock | Low-public-support enactment | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.952 | 0.000 | 0.663 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.183 | 0.638 |
| Baseline | Committee-first regular order | 0.149 | 0.283 | 0.851 | 0.076 | 0.656 |
| Baseline | Parliamentary coalition confidence | 0.181 | 0.286 | 0.819 | 0.048 | 0.633 |
| Baseline | Unicameral majority + pairwise alternatives | 0.547 | 0.489 | 0.453 | 0.003 | 0.381 |
| Baseline | Citizen assembly threshold gate | 0.176 | 0.261 | 0.824 | 0.032 | 0.640 |
| Baseline | Risk-routed majority legislature | 0.478 | 0.237 | 0.522 | 0.248 | 0.539 |
| Baseline | Portfolio hybrid legislature | 0.513 | 0.400 | 0.487 | 0.040 | 0.432 |
| Baseline | Expanded portfolio hybrid legislature | 0.800 | 0.443 | 0.200 | 0.005 | 0.268 |
| Baseline | Default pass unless 2/3 block | 0.840 | 0.105 | 0.160 | 0.492 | 0.447 |
| Baseline | Default pass + multi-round mediation + challenge | 0.722 | 0.219 | 0.278 | 0.401 | 0.454 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.172 | 0.386 | 0.828 | 0.011 | 0.600 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.182 | 0.494 |
| Low Polarization | Committee-first regular order | 0.387 | 0.306 | 0.613 | 0.089 | 0.533 |
| Low Polarization | Parliamentary coalition confidence | 0.482 | 0.301 | 0.518 | 0.102 | 0.489 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.631 | 0.633 | 0.369 | 0.002 | 0.295 |
| Low Polarization | Citizen assembly threshold gate | 0.413 | 0.295 | 0.587 | 0.040 | 0.513 |
| Low Polarization | Risk-routed majority legislature | 0.686 | 0.272 | 0.314 | 0.249 | 0.425 |
| Low Polarization | Portfolio hybrid legislature | 0.650 | 0.432 | 0.350 | 0.050 | 0.355 |
| Low Polarization | Expanded portfolio hybrid legislature | 0.865 | 0.512 | 0.135 | 0.007 | 0.215 |
| Low Polarization | Default pass unless 2/3 block | 0.843 | 0.200 | 0.157 | 0.374 | 0.394 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.808 | 0.265 | 0.192 | 0.338 | 0.384 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.022 | 0.361 | 0.978 | 0.000 | 0.680 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.188 | 0.687 |
| High Polarization | Committee-first regular order | 0.093 | 0.282 | 0.907 | 0.053 | 0.679 |
| High Polarization | Parliamentary coalition confidence | 0.097 | 0.293 | 0.903 | 0.026 | 0.669 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.488 | 0.446 | 0.512 | 0.002 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.123 | 0.248 | 0.877 | 0.018 | 0.668 |
| High Polarization | Risk-routed majority legislature | 0.367 | 0.226 | 0.633 | 0.239 | 0.597 |
| High Polarization | Portfolio hybrid legislature | 0.435 | 0.392 | 0.565 | 0.028 | 0.471 |
| High Polarization | Expanded portfolio hybrid legislature | 0.723 | 0.426 | 0.277 | 0.002 | 0.311 |
| High Polarization | Default pass unless 2/3 block | 0.836 | 0.081 | 0.164 | 0.545 | 0.467 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.685 | 0.206 | 0.315 | 0.443 | 0.484 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.052 | 0.346 | 0.948 | 0.011 | 0.673 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.183 | 0.630 |
| Low Party Loyalty | Committee-first regular order | 0.168 | 0.265 | 0.832 | 0.087 | 0.654 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.187 | 0.278 | 0.813 | 0.053 | 0.634 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.537 | 0.502 | 0.463 | 0.004 | 0.382 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.200 | 0.246 | 0.800 | 0.038 | 0.634 |
| Low Party Loyalty | Risk-routed majority legislature | 0.510 | 0.233 | 0.490 | 0.259 | 0.527 |
| Low Party Loyalty | Portfolio hybrid legislature | 0.526 | 0.394 | 0.474 | 0.042 | 0.427 |
| Low Party Loyalty | Expanded portfolio hybrid legislature | 0.806 | 0.452 | 0.194 | 0.003 | 0.262 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.839 | 0.105 | 0.161 | 0.500 | 0.449 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.743 | 0.218 | 0.257 | 0.403 | 0.444 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.050 | 0.371 | 0.950 | 0.006 | 0.665 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.193 | 0.635 |
| High Party Loyalty | Committee-first regular order | 0.164 | 0.287 | 0.836 | 0.107 | 0.653 |
| High Party Loyalty | Parliamentary coalition confidence | 0.196 | 0.287 | 0.804 | 0.055 | 0.627 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.553 | 0.503 | 0.447 | 0.002 | 0.373 |
| High Party Loyalty | Citizen assembly threshold gate | 0.193 | 0.263 | 0.807 | 0.030 | 0.631 |
| High Party Loyalty | Risk-routed majority legislature | 0.471 | 0.238 | 0.529 | 0.238 | 0.541 |
| High Party Loyalty | Portfolio hybrid legislature | 0.518 | 0.405 | 0.482 | 0.039 | 0.427 |
| High Party Loyalty | Expanded portfolio hybrid legislature | 0.800 | 0.452 | 0.200 | 0.003 | 0.265 |
| High Party Loyalty | Default pass unless 2/3 block | 0.848 | 0.109 | 0.152 | 0.476 | 0.439 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.716 | 0.221 | 0.284 | 0.391 | 0.454 |
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.032 | 0.372 | 0.968 | 0.000 | 0.673 |
| Low Revision-Moderation Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.147 | 0.652 |
| Low Revision-Moderation Culture | Committee-first regular order | 0.115 | 0.288 | 0.885 | 0.072 | 0.670 |
| Low Revision-Moderation Culture | Parliamentary coalition confidence | 0.151 | 0.297 | 0.849 | 0.017 | 0.639 |
| Low Revision-Moderation Culture | Unicameral majority + pairwise alternatives | 0.527 | 0.471 | 0.473 | 0.003 | 0.396 |
| Low Revision-Moderation Culture | Citizen assembly threshold gate | 0.154 | 0.275 | 0.846 | 0.012 | 0.643 |
| Low Revision-Moderation Culture | Risk-routed majority legislature | 0.382 | 0.237 | 0.618 | 0.204 | 0.579 |
| Low Revision-Moderation Culture | Portfolio hybrid legislature | 0.492 | 0.393 | 0.508 | 0.032 | 0.442 |
| Low Revision-Moderation Culture | Expanded portfolio hybrid legislature | 0.747 | 0.429 | 0.253 | 0.001 | 0.298 |
| Low Revision-Moderation Culture | Default pass unless 2/3 block | 0.834 | 0.102 | 0.166 | 0.495 | 0.452 |
| Low Revision-Moderation Culture | Default pass + multi-round mediation + challenge | 0.684 | 0.212 | 0.316 | 0.402 | 0.475 |
| High Revision-Moderation Culture | Stylized U.S.-like conventional benchmark | 0.070 | 0.372 | 0.930 | 0.006 | 0.654 |
| High Revision-Moderation Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.222 | 0.617 |
| High Revision-Moderation Culture | Committee-first regular order | 0.191 | 0.286 | 0.809 | 0.110 | 0.641 |
| High Revision-Moderation Culture | Parliamentary coalition confidence | 0.236 | 0.275 | 0.764 | 0.090 | 0.618 |
| High Revision-Moderation Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.533 | 0.443 | 0.002 | 0.362 |
| High Revision-Moderation Culture | Citizen assembly threshold gate | 0.221 | 0.254 | 0.779 | 0.045 | 0.622 |
| High Revision-Moderation Culture | Risk-routed majority legislature | 0.584 | 0.236 | 0.416 | 0.294 | 0.496 |
| High Revision-Moderation Culture | Portfolio hybrid legislature | 0.553 | 0.419 | 0.447 | 0.049 | 0.408 |
| High Revision-Moderation Culture | Expanded portfolio hybrid legislature | 0.841 | 0.474 | 0.159 | 0.004 | 0.238 |
| High Revision-Moderation Culture | Default pass unless 2/3 block | 0.858 | 0.109 | 0.142 | 0.499 | 0.438 |
| High Revision-Moderation Culture | Default pass + multi-round mediation + challenge | 0.764 | 0.224 | 0.236 | 0.399 | 0.431 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.383 | 0.943 | 0.007 | 0.658 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.180 | 0.633 |
| Low Lobbying Pressure | Committee-first regular order | 0.166 | 0.283 | 0.834 | 0.073 | 0.647 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.200 | 0.284 | 0.800 | 0.074 | 0.629 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.569 | 0.514 | 0.431 | 0.003 | 0.362 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.192 | 0.258 | 0.808 | 0.033 | 0.633 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.482 | 0.222 | 0.518 | 0.293 | 0.551 |
| Low Lobbying Pressure | Portfolio hybrid legislature | 0.564 | 0.411 | 0.436 | 0.040 | 0.402 |
| Low Lobbying Pressure | Expanded portfolio hybrid legislature | 0.862 | 0.455 | 0.138 | 0.005 | 0.234 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.846 | 0.103 | 0.154 | 0.494 | 0.445 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.712 | 0.207 | 0.288 | 0.423 | 0.467 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.366 | 0.973 | 0.005 | 0.678 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.205 | 0.654 |
| High Lobbying Pressure | Committee-first regular order | 0.134 | 0.273 | 0.866 | 0.078 | 0.667 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.137 | 0.303 | 0.863 | 0.024 | 0.645 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.485 | 0.475 | 0.515 | 0.005 | 0.416 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.158 | 0.270 | 0.842 | 0.029 | 0.645 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.396 | 0.252 | 0.604 | 0.227 | 0.572 |
| High Lobbying Pressure | Portfolio hybrid legislature | 0.451 | 0.398 | 0.549 | 0.035 | 0.462 |
| High Lobbying Pressure | Expanded portfolio hybrid legislature | 0.654 | 0.445 | 0.346 | 0.003 | 0.340 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.830 | 0.106 | 0.170 | 0.501 | 0.453 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.706 | 0.231 | 0.294 | 0.423 | 0.462 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.387 | 0.973 | 0.016 | 0.674 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.231 | 0.658 |
| Weak Constituency Pressure | Committee-first regular order | 0.130 | 0.289 | 0.870 | 0.113 | 0.671 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.119 | 0.337 | 0.881 | 0.057 | 0.651 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.526 | 0.467 | 0.474 | 0.003 | 0.398 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.154 | 0.274 | 0.846 | 0.035 | 0.648 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.462 | 0.246 | 0.538 | 0.334 | 0.562 |
| Weak Constituency Pressure | Portfolio hybrid legislature | 0.478 | 0.402 | 0.523 | 0.044 | 0.449 |
| Weak Constituency Pressure | Expanded portfolio hybrid legislature | 0.759 | 0.440 | 0.241 | 0.004 | 0.289 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.875 | 0.102 | 0.125 | 0.520 | 0.436 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.737 | 0.225 | 0.263 | 0.462 | 0.457 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.011 | 0.666 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.189 | 0.633 |
| Two-Party System | Committee-first regular order | 0.162 | 0.280 | 0.838 | 0.087 | 0.652 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.486 | 0.457 | 0.002 | 0.383 |
| Two-Party System | Citizen assembly threshold gate | 0.189 | 0.263 | 0.811 | 0.039 | 0.634 |
| Two-Party System | Risk-routed majority legislature | 0.478 | 0.237 | 0.522 | 0.250 | 0.540 |
| Two-Party System | Portfolio hybrid legislature | 0.514 | 0.397 | 0.486 | 0.037 | 0.432 |
| Two-Party System | Expanded portfolio hybrid legislature | 0.801 | 0.441 | 0.199 | 0.002 | 0.267 |
| Two-Party System | Default pass unless 2/3 block | 0.843 | 0.107 | 0.157 | 0.503 | 0.447 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.826 | 0.207 | 0.174 | 0.415 | 0.408 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.054 | 0.360 | 0.946 | 0.005 | 0.666 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.191 | 0.628 |
| Multi-Party System | Committee-first regular order | 0.173 | 0.279 | 0.827 | 0.100 | 0.650 |
| Multi-Party System | Parliamentary coalition confidence | 0.265 | 0.253 | 0.735 | 0.070 | 0.606 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.541 | 0.510 | 0.459 | 0.003 | 0.377 |
| Multi-Party System | Citizen assembly threshold gate | 0.203 | 0.260 | 0.797 | 0.038 | 0.628 |
| Multi-Party System | Risk-routed majority legislature | 0.500 | 0.240 | 0.500 | 0.258 | 0.530 |
| Multi-Party System | Portfolio hybrid legislature | 0.524 | 0.405 | 0.476 | 0.045 | 0.426 |
| Multi-Party System | Expanded portfolio hybrid legislature | 0.812 | 0.458 | 0.188 | 0.004 | 0.257 |
| Multi-Party System | Default pass unless 2/3 block | 0.839 | 0.109 | 0.161 | 0.507 | 0.449 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.645 | 0.233 | 0.355 | 0.374 | 0.483 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.050 | 0.373 | 0.950 | 0.005 | 0.664 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.186 | 0.634 |
| High Proposal Pressure | Committee-first regular order | 0.162 | 0.286 | 0.838 | 0.086 | 0.650 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.187 | 0.290 | 0.813 | 0.057 | 0.631 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.496 | 0.460 | 0.001 | 0.381 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.186 | 0.265 | 0.814 | 0.034 | 0.634 |
| High Proposal Pressure | Risk-routed majority legislature | 0.481 | 0.239 | 0.519 | 0.253 | 0.538 |
| High Proposal Pressure | Portfolio hybrid legislature | 0.512 | 0.402 | 0.488 | 0.039 | 0.431 |
| High Proposal Pressure | Expanded portfolio hybrid legislature | 0.797 | 0.448 | 0.203 | 0.003 | 0.268 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.845 | 0.107 | 0.155 | 0.501 | 0.446 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.904 | 0.203 | 0.096 | 0.433 | 0.374 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.371 | 0.951 | 0.006 | 0.665 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.188 | 0.635 |
| Extreme Proposal Pressure | Committee-first regular order | 0.161 | 0.287 | 0.839 | 0.083 | 0.650 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.290 | 0.815 | 0.050 | 0.631 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.382 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.185 | 0.263 | 0.815 | 0.028 | 0.634 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.480 | 0.237 | 0.520 | 0.252 | 0.539 |
| Extreme Proposal Pressure | Portfolio hybrid legislature | 0.514 | 0.399 | 0.486 | 0.040 | 0.432 |
| Extreme Proposal Pressure | Expanded portfolio hybrid legislature | 0.796 | 0.445 | 0.204 | 0.003 | 0.269 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.842 | 0.106 | 0.158 | 0.500 | 0.447 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.940 | 0.199 | 0.060 | 0.435 | 0.358 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.023 | 0.353 | 0.977 | 0.002 | 0.683 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.216 | 0.661 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.127 | 0.269 | 0.873 | 0.091 | 0.674 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.115 | 0.319 | 0.885 | 0.031 | 0.653 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.458 | 0.455 | 0.542 | 0.001 | 0.435 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.147 | 0.274 | 0.853 | 0.044 | 0.653 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.377 | 0.259 | 0.623 | 0.242 | 0.582 |
| Lobby-Fueled Flooding | Portfolio hybrid legislature | 0.433 | 0.380 | 0.567 | 0.033 | 0.476 |
| Lobby-Fueled Flooding | Expanded portfolio hybrid legislature | 0.604 | 0.428 | 0.396 | 0.003 | 0.370 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.843 | 0.106 | 0.157 | 0.515 | 0.450 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.896 | 0.208 | 0.104 | 0.451 | 0.380 |
| Low-Revision-Moderation Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.380 | 0.980 | 0.011 | 0.678 |
| Low-Revision-Moderation Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.160 | 0.675 |
| Low-Revision-Moderation Flooding | Committee-first regular order | 0.090 | 0.292 | 0.910 | 0.080 | 0.683 |
| Low-Revision-Moderation Flooding | Parliamentary coalition confidence | 0.100 | 0.313 | 0.900 | 0.014 | 0.659 |
| Low-Revision-Moderation Flooding | Unicameral majority + pairwise alternatives | 0.495 | 0.461 | 0.505 | 0.001 | 0.414 |
| Low-Revision-Moderation Flooding | Citizen assembly threshold gate | 0.123 | 0.268 | 0.877 | 0.016 | 0.661 |
| Low-Revision-Moderation Flooding | Risk-routed majority legislature | 0.338 | 0.234 | 0.662 | 0.214 | 0.604 |
| Low-Revision-Moderation Flooding | Portfolio hybrid legislature | 0.434 | 0.398 | 0.566 | 0.027 | 0.469 |
| Low-Revision-Moderation Flooding | Expanded portfolio hybrid legislature | 0.693 | 0.433 | 0.307 | 0.001 | 0.324 |
| Low-Revision-Moderation Flooding | Default pass unless 2/3 block | 0.836 | 0.091 | 0.164 | 0.522 | 0.459 |
| Low-Revision-Moderation Flooding | Default pass + multi-round mediation + challenge | 0.885 | 0.188 | 0.115 | 0.442 | 0.390 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.015 | 0.366 | 0.985 | 0.006 | 0.684 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.231 | 0.687 |
| Capture Crisis | Committee-first regular order | 0.098 | 0.259 | 0.902 | 0.088 | 0.691 |
| Capture Crisis | Parliamentary coalition confidence | 0.067 | 0.338 | 0.933 | 0.020 | 0.669 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.405 | 0.454 | 0.595 | 0.001 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.113 | 0.267 | 0.887 | 0.046 | 0.672 |
| Capture Crisis | Risk-routed majority legislature | 0.327 | 0.258 | 0.673 | 0.233 | 0.606 |
| Capture Crisis | Portfolio hybrid legislature | 0.379 | 0.385 | 0.621 | 0.028 | 0.501 |
| Capture Crisis | Expanded portfolio hybrid legislature | 0.516 | 0.434 | 0.484 | 0.002 | 0.412 |
| Capture Crisis | Default pass unless 2/3 block | 0.841 | 0.099 | 0.159 | 0.519 | 0.454 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.889 | 0.205 | 0.111 | 0.446 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.074 | 0.375 | 0.926 | 0.003 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.195 | 0.593 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.226 | 0.281 | 0.774 | 0.083 | 0.619 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.273 | 0.282 | 0.727 | 0.067 | 0.592 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.545 | 0.543 | 0.455 | 0.001 | 0.365 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.253 | 0.274 | 0.747 | 0.046 | 0.601 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.506 | 0.268 | 0.494 | 0.218 | 0.510 |
| Popular Anti-Lobbying Push | Portfolio hybrid legislature | 0.523 | 0.412 | 0.477 | 0.051 | 0.425 |
| Popular Anti-Lobbying Push | Expanded portfolio hybrid legislature | 0.762 | 0.476 | 0.238 | 0.003 | 0.276 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.823 | 0.129 | 0.177 | 0.463 | 0.442 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.862 | 0.230 | 0.138 | 0.407 | 0.381 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.052 | 0.370 | 0.948 | 0.003 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.180 | 0.632 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.157 | 0.287 | 0.843 | 0.081 | 0.652 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.542 | 0.506 | 0.458 | 0.002 | 0.377 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.190 | 0.268 | 0.810 | 0.031 | 0.630 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.470 | 0.241 | 0.530 | 0.246 | 0.542 |
| Weighted Two-Party Baseline | Portfolio hybrid legislature | 0.517 | 0.411 | 0.483 | 0.039 | 0.426 |
| Weighted Two-Party Baseline | Expanded portfolio hybrid legislature | 0.791 | 0.456 | 0.209 | 0.002 | 0.268 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.834 | 0.108 | 0.166 | 0.497 | 0.450 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.827 | 0.206 | 0.173 | 0.414 | 0.408 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.393 | 0.950 | 0.000 | 0.657 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.193 | 0.637 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.159 | 0.286 | 0.841 | 0.086 | 0.652 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.255 | 0.255 | 0.745 | 0.083 | 0.613 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.545 | 0.509 | 0.455 | 0.001 | 0.375 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.186 | 0.264 | 0.814 | 0.025 | 0.633 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.485 | 0.235 | 0.515 | 0.259 | 0.539 |
| Weighted Two Major Plus Minors | Portfolio hybrid legislature | 0.522 | 0.406 | 0.478 | 0.044 | 0.426 |
| Weighted Two Major Plus Minors | Expanded portfolio hybrid legislature | 0.802 | 0.455 | 0.198 | 0.003 | 0.263 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.846 | 0.108 | 0.154 | 0.504 | 0.445 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.643 | 0.228 | 0.357 | 0.384 | 0.487 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.070 | 0.363 | 0.930 | 0.006 | 0.657 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.190 | 0.608 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.207 | 0.289 | 0.793 | 0.085 | 0.627 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.342 | 0.243 | 0.658 | 0.073 | 0.570 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.550 | 0.532 | 0.450 | 0.002 | 0.366 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.235 | 0.266 | 0.765 | 0.034 | 0.609 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.544 | 0.245 | 0.456 | 0.272 | 0.509 |
| Weighted Fragmented Multiparty | Portfolio hybrid legislature | 0.550 | 0.411 | 0.450 | 0.051 | 0.412 |
| Weighted Fragmented Multiparty | Expanded portfolio hybrid legislature | 0.819 | 0.470 | 0.181 | 0.004 | 0.250 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.833 | 0.122 | 0.167 | 0.479 | 0.443 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.636 | 0.243 | 0.364 | 0.350 | 0.479 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.048 | 0.384 | 0.952 | 0.003 | 0.661 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.181 | 0.628 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.170 | 0.291 | 0.830 | 0.080 | 0.644 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.204 | 0.286 | 0.796 | 0.042 | 0.621 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.552 | 0.524 | 0.448 | 0.003 | 0.368 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.201 | 0.267 | 0.799 | 0.026 | 0.625 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.473 | 0.238 | 0.527 | 0.241 | 0.540 |
| Weighted Dominant-Party Legislature | Portfolio hybrid legislature | 0.529 | 0.413 | 0.471 | 0.045 | 0.421 |
| Weighted Dominant-Party Legislature | Expanded portfolio hybrid legislature | 0.805 | 0.472 | 0.195 | 0.003 | 0.256 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.806 | 0.117 | 0.194 | 0.472 | 0.456 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.650 | 0.229 | 0.350 | 0.374 | 0.481 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.177 | 0.377 | 0.823 | 0.010 | 0.600 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.204 | 0.507 |
| Era 1 Low Contention | Committee-first regular order | 0.373 | 0.301 | 0.627 | 0.104 | 0.544 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.516 | 0.273 | 0.484 | 0.115 | 0.483 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.639 | 0.375 | 0.003 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.389 | 0.283 | 0.611 | 0.050 | 0.530 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.710 | 0.255 | 0.290 | 0.277 | 0.424 |
| Era 1 Low Contention | Portfolio hybrid legislature | 0.666 | 0.440 | 0.334 | 0.051 | 0.345 |
| Era 1 Low Contention | Expanded portfolio hybrid legislature | 0.889 | 0.520 | 0.111 | 0.007 | 0.201 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.848 | 0.179 | 0.152 | 0.403 | 0.403 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.779 | 0.253 | 0.221 | 0.333 | 0.401 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.111 | 0.377 | 0.889 | 0.008 | 0.633 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.219 | 0.564 |
| Era 2 Normal Contention | Committee-first regular order | 0.283 | 0.294 | 0.717 | 0.095 | 0.589 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.422 | 0.263 | 0.578 | 0.104 | 0.531 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.569 | 0.413 | 0.003 | 0.337 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.303 | 0.277 | 0.697 | 0.045 | 0.575 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.618 | 0.253 | 0.382 | 0.283 | 0.472 |
| Era 2 Normal Contention | Portfolio hybrid legislature | 0.613 | 0.418 | 0.387 | 0.058 | 0.380 |
| Era 2 Normal Contention | Expanded portfolio hybrid legislature | 0.864 | 0.484 | 0.136 | 0.005 | 0.224 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.841 | 0.149 | 0.159 | 0.452 | 0.425 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.735 | 0.245 | 0.265 | 0.366 | 0.432 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.061 | 0.380 | 0.939 | 0.005 | 0.656 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.184 | 0.612 |
| Era 3 Polarizing | Committee-first regular order | 0.199 | 0.286 | 0.801 | 0.095 | 0.634 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.296 | 0.263 | 0.704 | 0.076 | 0.588 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.554 | 0.510 | 0.446 | 0.001 | 0.370 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.220 | 0.265 | 0.780 | 0.033 | 0.617 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.513 | 0.246 | 0.487 | 0.253 | 0.520 |
| Era 3 Polarizing | Portfolio hybrid legislature | 0.536 | 0.399 | 0.464 | 0.044 | 0.421 |
| Era 3 Polarizing | Expanded portfolio hybrid legislature | 0.810 | 0.454 | 0.190 | 0.003 | 0.259 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.845 | 0.118 | 0.155 | 0.482 | 0.438 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.662 | 0.238 | 0.338 | 0.372 | 0.472 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.028 | 0.372 | 0.972 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.179 | 0.656 |
| Era 4 High Contention | Committee-first regular order | 0.128 | 0.281 | 0.872 | 0.081 | 0.668 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.125 | 0.309 | 0.875 | 0.026 | 0.650 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.519 | 0.477 | 0.481 | 0.001 | 0.398 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.150 | 0.265 | 0.850 | 0.022 | 0.650 |
| Era 4 High Contention | Risk-routed majority legislature | 0.400 | 0.244 | 0.600 | 0.230 | 0.573 |
| Era 4 High Contention | Portfolio hybrid legislature | 0.468 | 0.400 | 0.532 | 0.033 | 0.453 |
| Era 4 High Contention | Expanded portfolio hybrid legislature | 0.726 | 0.440 | 0.274 | 0.003 | 0.305 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.833 | 0.100 | 0.167 | 0.509 | 0.455 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.762 | 0.212 | 0.238 | 0.424 | 0.440 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.347 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.206 | 0.698 |
| Era 5 Capture Contention | Committee-first regular order | 0.088 | 0.258 | 0.912 | 0.092 | 0.697 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.437 | 0.428 | 0.563 | 0.002 | 0.454 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.106 | 0.257 | 0.894 | 0.031 | 0.676 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.326 | 0.241 | 0.674 | 0.225 | 0.610 |
| Era 5 Capture Contention | Portfolio hybrid legislature | 0.388 | 0.376 | 0.612 | 0.037 | 0.500 |
| Era 5 Capture Contention | Expanded portfolio hybrid legislature | 0.579 | 0.412 | 0.421 | 0.002 | 0.387 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.833 | 0.087 | 0.167 | 0.540 | 0.465 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.863 | 0.195 | 0.137 | 0.449 | 0.400 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.010 | 0.352 | 0.990 | 0.007 | 0.691 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.241 | 0.721 |
| Era 6 Crisis | Committee-first regular order | 0.065 | 0.255 | 0.935 | 0.106 | 0.712 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.356 | 0.413 | 0.644 | 0.002 | 0.498 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.075 | 0.269 | 0.925 | 0.031 | 0.688 |
| Era 6 Crisis | Risk-routed majority legislature | 0.272 | 0.236 | 0.728 | 0.238 | 0.641 |
| Era 6 Crisis | Portfolio hybrid legislature | 0.318 | 0.376 | 0.682 | 0.026 | 0.533 |
| Era 6 Crisis | Expanded portfolio hybrid legislature | 0.456 | 0.404 | 0.544 | 0.002 | 0.451 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.840 | 0.082 | 0.160 | 0.558 | 0.467 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.894 | 0.188 | 0.106 | 0.466 | 0.390 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.340 | 0.810 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.013 | 0.122 | 0.987 | 0.021 | 0.761 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.038 | 0.126 | 0.962 | 0.167 | 0.776 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.641 | 0.499 | 0.359 | 0.001 | 0.330 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.098 | 0.102 | 0.902 | 0.047 | 0.730 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.611 | 0.186 | 0.389 | 0.168 | 0.472 |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature | 0.794 | 0.507 | 0.206 | 0.000 | 0.251 |
| Adversarial High-Benefit Extreme Reform | Expanded portfolio hybrid legislature | 0.993 | 0.529 | 0.007 | 0.000 | 0.145 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.910 | 0.046 | 0.090 | 0.575 | 0.446 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.767 | 0.182 | 0.233 | 0.244 | 0.411 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.206 | 0.404 | 0.794 | 0.001 | 0.576 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.010 | 0.280 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.627 | 0.316 | 0.373 | 0.062 | 0.404 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.422 | 0.408 | 0.578 | 0.001 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.204 | 0.422 | 0.796 | 0.211 | 0.614 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.983 | 0.360 | 0.017 | 0.010 | 0.203 |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature | 0.370 | 0.507 | 0.630 | 0.000 | 0.463 |
| Adversarial Popular Harmful Bill | Expanded portfolio hybrid legislature | 0.899 | 0.518 | 0.101 | 0.000 | 0.195 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 1.000 | 0.261 | 0.000 | 0.013 | 0.224 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.990 | 0.359 | 0.010 | 0.010 | 0.199 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.059 | 0.552 | 0.941 | 0.002 | 0.605 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.290 | 0.226 |
| Adversarial Moderate Capture | Committee-first regular order | 0.833 | 0.497 | 0.167 | 0.279 | 0.290 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.848 | 0.533 | 0.152 | 0.106 | 0.237 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.568 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.427 | 0.536 | 0.573 | 0.490 | 0.524 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.984 | 0.525 | 0.016 | 0.239 | 0.198 |
| Adversarial Moderate Capture | Portfolio hybrid legislature | 0.192 | 0.485 | 0.808 | 0.017 | 0.562 |
| Adversarial Moderate Capture | Expanded portfolio hybrid legislature | 0.578 | 0.513 | 0.422 | 0.001 | 0.357 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.308 | 0.215 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.991 | 0.524 | 0.009 | 0.245 | 0.196 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.003 | 0.283 | 0.997 | 0.045 | 0.723 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.593 | 0.752 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.146 | 0.276 | 0.854 | 0.086 | 0.661 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.204 | 0.279 | 0.796 | 0.375 | 0.690 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.485 | 0.477 | 0.515 | 0.004 | 0.415 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.264 | 0.238 | 0.736 | 0.051 | 0.607 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.700 | 0.267 | 0.300 | 0.353 | 0.440 |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature | 0.710 | 0.472 | 0.290 | 0.004 | 0.304 |
| Adversarial Delayed-Benefit Reform | Expanded portfolio hybrid legislature | 0.985 | 0.496 | 0.015 | 0.000 | 0.159 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.858 | 0.114 | 0.142 | 0.751 | 0.487 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.847 | 0.261 | 0.153 | 0.426 | 0.384 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.048 | 0.373 | 0.952 | 0.003 | 0.665 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.117 | 0.495 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.270 | 0.294 | 0.730 | 0.131 | 0.603 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.385 | 0.304 | 0.615 | 0.028 | 0.522 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.475 | 0.519 | 0.525 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.076 | 0.370 | 0.924 | 0.073 | 0.666 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.768 | 0.286 | 0.232 | 0.082 | 0.347 |
| Adversarial Concentrated Rights Harm | Portfolio hybrid legislature | 0.435 | 0.461 | 0.565 | 0.002 | 0.445 |
| Adversarial Concentrated Rights Harm | Expanded portfolio hybrid legislature | 0.911 | 0.493 | 0.089 | 0.000 | 0.197 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.977 | 0.175 | 0.023 | 0.190 | 0.297 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.843 | 0.287 | 0.157 | 0.109 | 0.314 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.043 | 0.373 | 0.957 | 0.013 | 0.669 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.295 | 0.614 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.189 | 0.299 | 0.811 | 0.165 | 0.649 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.320 | 0.319 | 0.680 | 0.113 | 0.567 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.413 | 0.497 | 0.587 | 0.003 | 0.445 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.273 | 0.329 | 0.727 | 0.033 | 0.571 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.405 | 0.334 | 0.595 | 0.253 | 0.548 |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature | 0.587 | 0.445 | 0.413 | 0.007 | 0.375 |
| Adversarial Anti-Lobbying Backlash | Expanded portfolio hybrid legislature | 0.767 | 0.472 | 0.233 | 0.000 | 0.275 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.890 | 0.208 | 0.110 | 0.575 | 0.408 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.698 | 0.318 | 0.303 | 0.465 | 0.449 |
| Adversarial Revision Dilution | Stylized U.S.-like conventional benchmark | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Adversarial Revision Dilution | Unicameral simple majority | 0.051 | 0.129 | 0.949 | 0.422 | 0.820 |
| Adversarial Revision Dilution | Committee-first regular order | 0.017 | 0.154 | 0.983 | 0.033 | 0.752 |
| Adversarial Revision Dilution | Parliamentary coalition confidence | 0.035 | 0.153 | 0.965 | 0.216 | 0.780 |
| Adversarial Revision Dilution | Unicameral majority + pairwise alternatives | 0.559 | 0.486 | 0.441 | 0.002 | 0.375 |
| Adversarial Revision Dilution | Citizen assembly threshold gate | 0.113 | 0.123 | 0.888 | 0.042 | 0.715 |
| Adversarial Revision Dilution | Risk-routed majority legislature | 0.563 | 0.189 | 0.438 | 0.250 | 0.512 |
| Adversarial Revision Dilution | Portfolio hybrid legislature | 0.755 | 0.494 | 0.245 | 0.001 | 0.274 |
| Adversarial Revision Dilution | Expanded portfolio hybrid legislature | 0.980 | 0.518 | 0.020 | 0.000 | 0.155 |
| Adversarial Revision Dilution | Default pass unless 2/3 block | 0.896 | 0.056 | 0.104 | 0.668 | 0.469 |
| Adversarial Revision Dilution | Default pass + multi-round mediation + challenge | 0.741 | 0.186 | 0.259 | 0.336 | 0.441 |
| Adversarial Lobby Information | Stylized U.S.-like conventional benchmark | 0.117 | 0.391 | 0.883 | 0.012 | 0.627 |
| Adversarial Lobby Information | Unicameral simple majority | 0.772 | 0.271 | 0.228 | 0.225 | 0.378 |
| Adversarial Lobby Information | Committee-first regular order | 0.643 | 0.302 | 0.358 | 0.018 | 0.392 |
| Adversarial Lobby Information | Parliamentary coalition confidence | 0.577 | 0.330 | 0.423 | 0.086 | 0.430 |
| Adversarial Lobby Information | Unicameral majority + pairwise alternatives | 0.835 | 0.566 | 0.165 | 0.000 | 0.213 |
| Adversarial Lobby Information | Citizen assembly threshold gate | 0.746 | 0.278 | 0.254 | 0.028 | 0.349 |
| Adversarial Lobby Information | Risk-routed majority legislature | 0.880 | 0.288 | 0.120 | 0.202 | 0.314 |
| Adversarial Lobby Information | Portfolio hybrid legislature | 0.866 | 0.424 | 0.134 | 0.008 | 0.241 |
| Adversarial Lobby Information | Expanded portfolio hybrid legislature | 0.978 | 0.550 | 0.022 | 0.000 | 0.146 |
| Adversarial Lobby Information | Default pass unless 2/3 block | 0.995 | 0.233 | 0.005 | 0.281 | 0.289 |
| Adversarial Lobby Information | Default pass + multi-round mediation + challenge | 0.912 | 0.284 | 0.088 | 0.213 | 0.301 |
| Adversarial Public Opinion Error | Stylized U.S.-like conventional benchmark | 0.035 | 0.372 | 0.965 | 0.008 | 0.673 |
| Adversarial Public Opinion Error | Unicameral simple majority | 0.309 | 0.247 | 0.691 | 0.244 | 0.620 |
| Adversarial Public Opinion Error | Committee-first regular order | 0.152 | 0.290 | 0.848 | 0.128 | 0.663 |
| Adversarial Public Opinion Error | Parliamentary coalition confidence | 0.241 | 0.308 | 0.759 | 0.165 | 0.620 |
| Adversarial Public Opinion Error | Unicameral majority + pairwise alternatives | 0.655 | 0.513 | 0.345 | 0.001 | 0.319 |
| Adversarial Public Opinion Error | Citizen assembly threshold gate | 0.142 | 0.284 | 0.858 | 0.065 | 0.657 |
| Adversarial Public Opinion Error | Risk-routed majority legislature | 0.731 | 0.281 | 0.269 | 0.177 | 0.386 |
| Adversarial Public Opinion Error | Portfolio hybrid legislature | 0.646 | 0.490 | 0.354 | 0.001 | 0.330 |
| Adversarial Public Opinion Error | Expanded portfolio hybrid legislature | 0.938 | 0.501 | 0.062 | 0.000 | 0.181 |
| Adversarial Public Opinion Error | Default pass unless 2/3 block | 0.892 | 0.126 | 0.108 | 0.406 | 0.397 |
| Adversarial Public Opinion Error | Default pass + multi-round mediation + challenge | 0.878 | 0.275 | 0.122 | 0.248 | 0.328 |

## Burden-Shifting Side Note: Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from automatic passage into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.283 | -0.255 | 0.022 | -0.077 | -0.294 | -0.137 | 0.500 |
| Low Polarization | -11.125 | -0.185 | 0.029 | -0.141 | -0.141 | -0.064 | 0.499 |
| High Polarization | -16.917 | -0.282 | 0.012 | -0.036 | -0.357 | -0.163 | 0.500 |
| Low Party Loyalty | -15.325 | -0.255 | 0.028 | -0.089 | -0.303 | -0.145 | 0.500 |
| High Party Loyalty | -16.150 | -0.269 | 0.023 | -0.073 | -0.307 | -0.140 | 0.500 |
| Low Revision-Moderation Culture | -16.283 | -0.271 | 0.021 | -0.058 | -0.308 | -0.139 | 0.500 |
| High Revision-Moderation Culture | -15.150 | -0.253 | 0.027 | -0.094 | -0.289 | -0.134 | 0.500 |
| Low Lobbying Pressure | -15.858 | -0.264 | 0.025 | -0.081 | -0.302 | -0.142 | 0.500 |
| High Lobbying Pressure | -14.983 | -0.250 | 0.017 | -0.057 | -0.293 | -0.140 | 0.500 |
| Weak Constituency Pressure | -18.250 | -0.304 | 0.024 | -0.073 | -0.332 | -0.150 | 0.499 |
| Two-Party System | -6.608 | -0.110 | -0.009 | -0.006 | -0.145 | -0.079 | 0.333 |
| Multi-Party System | -30.150 | -0.503 | 0.114 | -0.297 | -0.530 | -0.336 | 0.800 |
| High Proposal Pressure | 3.025 | 0.017 | -0.016 | 0.007 | -0.029 | -0.054 | 0.167 |
| Extreme Proposal Pressure | 22.458 | 0.075 | -0.022 | 0.023 | 0.022 | -0.048 | 0.100 |
| Lobby-Fueled Flooding | 2.317 | 0.013 | -0.015 | 0.005 | -0.032 | -0.054 | 0.167 |
| Low-Revision-Moderation Flooding | 2.517 | 0.014 | -0.017 | 0.017 | -0.048 | -0.073 | 0.167 |
| Capture Crisis | 2.325 | 0.013 | -0.014 | 0.016 | -0.042 | -0.065 | 0.167 |
| Popular Anti-Lobbying Push | -2.117 | -0.018 | -0.014 | -0.005 | -0.053 | -0.054 | 0.250 |
| Weighted Two-Party Baseline | -6.067 | -0.101 | -0.006 | -0.027 | -0.144 | -0.083 | 0.333 |
| Weighted Two Major Plus Minors | -30.733 | -0.512 | 0.111 | -0.277 | -0.539 | -0.330 | 0.802 |
| Weighted Fragmented Multiparty | -29.075 | -0.485 | 0.114 | -0.376 | -0.478 | -0.298 | 0.855 |
| Weighted Dominant-Party Legislature | -20.058 | -0.334 | 0.041 | -0.155 | -0.343 | -0.170 | 0.667 |
| Era 1 Low Contention | -15.908 | -0.265 | 0.052 | -0.214 | -0.230 | -0.115 | 0.660 |
| Era 2 Normal Contention | -22.492 | -0.375 | 0.084 | -0.283 | -0.365 | -0.213 | 0.725 |
| Era 3 Polarizing | -29.508 | -0.492 | 0.108 | -0.294 | -0.510 | -0.330 | 0.781 |
| Era 4 High Contention | -13.350 | -0.178 | -0.000 | -0.024 | -0.218 | -0.102 | 0.400 |
| Era 5 Capture Contention | -2.708 | -0.030 | -0.014 | 0.023 | -0.094 | -0.086 | 0.222 |
| Era 6 Crisis | 1.400 | 0.012 | -0.016 | 0.024 | -0.061 | -0.085 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.475 | -0.558 | 0.000 | -0.008 | -0.603 | -0.203 | 0.665 |
| Adversarial Popular Harmful Bill | -6.550 | -0.109 | 0.000 | -0.094 | -0.095 | -0.050 | 0.462 |
| Adversarial Moderate Capture | -1.042 | -0.017 | 0.000 | -0.016 | -0.008 | -0.002 | 0.329 |
| Adversarial Delayed-Benefit Reform | -27.242 | -0.454 | 0.002 | -0.102 | -0.439 | -0.225 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.642 | -0.394 | 0.029 | -0.220 | -0.326 | -0.175 | 0.651 |
| Adversarial Anti-Lobbying Backlash | -22.433 | -0.374 | 0.045 | -0.159 | -0.257 | -0.156 | 0.648 |
| Adversarial Revision Dilution | -32.617 | -0.544 | -0.000 | 0.005 | -0.586 | -0.206 | 0.664 |
| Adversarial Lobby Information | -10.667 | -0.178 | -0.000 | -0.131 | -0.143 | -0.069 | 0.469 |
| Adversarial Public Opinion Error | -25.658 | -0.428 | -0.019 | -0.167 | -0.427 | -0.205 | 0.664 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-public-support enactment |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.763) | Default pass unless 2/3 block (0.840) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Committee amendment and revision power (0.740) | Expanded portfolio hybrid legislature (0.865) | Unicameral majority + pairwise alternatives (0.002) |
| High Polarization | Committee amendment and revision power (0.761) | Default pass unless 2/3 block (0.836) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.759) | Default pass unless 2/3 block (0.839) | Expanded portfolio hybrid legislature (0.003) |
| High Party Loyalty | Cloture, conference, and judicial review (0.757) | Default pass unless 2/3 block (0.848) | Unicameral majority + pairwise alternatives (0.002) |
| Low Revision-Moderation Culture | Cloture, conference, and judicial review (0.769) | Default pass unless 2/3 block (0.834) | Stylized U.S.-like conventional benchmark (0.000) |
| High Revision-Moderation Culture | Stylized U.S.-like conventional benchmark (0.744) | Default pass unless 2/3 block (0.858) | Unicameral majority + pairwise alternatives (0.002) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Expanded portfolio hybrid legislature (0.862) | Unicameral majority + pairwise alternatives (0.003) |
| High Lobbying Pressure | Committee amendment and revision power (0.760) | Default pass unless 2/3 block (0.830) | Expanded portfolio hybrid legislature (0.003) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.875) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Committee amendment and revision power (0.752) | Default pass unless 2/3 block (0.843) | Parliamentary coalition confidence (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.839) | Pairwise amendment tournament + majority (0.003) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.756) | Default pass + multi-round mediation + challenge (0.904) | Pairwise amendment tournament + majority (0.001) |
| Extreme Proposal Pressure | Committee amendment and revision power (0.752) | Default pass + multi-round mediation + challenge (0.940) | Unicameral majority + pairwise alternatives (0.000) |
| Lobby-Fueled Flooding | Committee amendment and revision power (0.757) | Default pass + multi-round mediation + challenge (0.896) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Revision-Moderation Flooding | Committee amendment and revision power (0.759) | Default pass + multi-round mediation + challenge (0.885) | Pairwise amendment tournament + majority (0.001) |
| Capture Crisis | Parliamentary coalition confidence (0.747) | Default pass + multi-round mediation + challenge (0.889) | Unicameral majority + pairwise alternatives (0.001) |
| Popular Anti-Lobbying Push | Committee amendment and revision power (0.767) | Default pass + multi-round mediation + challenge (0.862) | Pairwise amendment tournament + majority (0.001) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.834) | Parliamentary coalition confidence (0.000) |
| Weighted Two Major Plus Minors | Committee amendment and revision power (0.753) | Default pass unless 2/3 block (0.846) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Committee amendment and revision power (0.746) | Default pass unless 2/3 block (0.833) | Unicameral majority + pairwise alternatives (0.002) |
| Weighted Dominant-Party Legislature | Committee amendment and revision power (0.745) | Default pass unless 2/3 block (0.806) | Pairwise amendment tournament + majority (0.002) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.730) | Expanded portfolio hybrid legislature (0.889) | Pairwise amendment tournament + majority (0.002) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.753) | Expanded portfolio hybrid legislature (0.864) | Unicameral majority + pairwise alternatives (0.003) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.845) | Unicameral majority + pairwise alternatives (0.001) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.769) | Default pass unless 2/3 block (0.833) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Committee amendment and revision power (0.749) | Default pass + multi-round mediation + challenge (0.863) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Committee amendment and revision power (0.762) | Default pass + multi-round mediation + challenge (0.894) | Parliamentary coalition confidence (0.000) |
| Adversarial High-Benefit Extreme Reform | Unicameral 60 percent passage (0.870) | Expanded portfolio hybrid legislature (0.993) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature (0.344) | Default pass unless 2/3 block (1.000) | Committee amendment and revision power (0.000) |
| Adversarial Moderate Capture | Committee discharge-petition target (0.475) | Default pass unless 2/3 block (1.000) | Committee amendment and revision power (0.000) |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature (0.818) | Expanded portfolio hybrid legislature (0.985) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.616) | Default pass unless 2/3 block (0.977) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature (0.731) | Default pass unless 2/3 block (0.890) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Revision Dilution | Portfolio hybrid legislature (0.882) | Expanded portfolio hybrid legislature (0.980) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Lobby Information | Pairwise alternatives + no support/revision vote kernel (0.783) | Default pass unless 2/3 block (0.995) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Public Opinion Error | Committee amendment and revision power (0.735) | Expanded portfolio hybrid legislature (0.938) | Expanded portfolio hybrid legislature (0.000) |

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
