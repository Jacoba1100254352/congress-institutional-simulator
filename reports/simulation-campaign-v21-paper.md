# Main Comparison Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 35
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

- The main comparison campaign is breadth-first: 35 scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.
- The scalar directional score is productivity-sensitive: its highest value came from Default pass unless 2/3 block at 0.724, which is why the report treats the score as a profile aid rather than a recommendation.
- Highest average welfare came from Stylized U.S.-like conventional benchmark at 0.710; highest compromise came from Unicameral majority + pairwise alternatives at 0.503.
- Highest productivity came from Default pass unless 2/3 block at 0.860.
- Open default-pass averaged 0.860 productivity, 0.477 weak public-mandate passage, and 0.628 policy shift, so it functions as a throughput/risk endpoint.
- The stylized U.S.-like conventional benchmark averaged 0.055 productivity and 0.710 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.
- The portfolio hybrid combines risk routing, pairwise alternatives, citizen/harm review, proposal bonds, anti-capture safeguards, and law review. It averaged 0.503 productivity, 0.417 compromise, 0.932 risk control, and 0.705 directional score, situating it between pairwise alternatives and risk routing rather than replacing the tradeoff frontier.
- The expanded portfolio hybrid adds district-public, long-horizon strategy, omnibus bargaining, influence-system, and constitutional-court architecture proxies. It averaged 0.772 productivity, 0.461 compromise, 0.904 risk control, and 0.676 directional score; its value is diagnostic because extra safeguards also increase complexity.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.647 | 0.572 | 0.879 | 0.967 | 0.171 | 14.016 | 41.032 | 0.635 | 0.000 | 0.179 | 0.033 | 0.111 | 0.548 | 0.061 | 0.295 | 0.233 | 0.000 | 0.000 | 0.000 | 0.000 | 0.391 | 0.000 | 0.465 |
| Majority + anti-capture bundle | 0.677 | 0.580 | 0.886 | 0.935 | 0.308 | 25.708 | 82.908 | 0.656 | 0.000 | 0.149 | 0.065 | 0.111 | 0.552 | 0.117 | 0.306 | 0.133 | 0.100 | 0.552 | 0.000 | 0.000 | 0.747 | 0.000 | 0.934 |
| Bicameral simple majority | 0.654 | 0.588 | 0.880 | 0.930 | 0.219 | 17.106 | 88.548 | 0.637 | 0.000 | 0.149 | 0.070 | 0.111 | 0.564 | 0.063 | 0.225 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.459 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.632 | 0.612 | 0.909 | 0.810 | 0.199 | 16.379 | 88.548 | 0.694 | 0.000 | 0.054 | 0.190 | 0.086 | 0.630 | 0.062 | 0.250 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.582 | 0.000 | 1.000 |
| Citizen initiative and referendum | 0.693 | 0.582 | 0.837 | 0.930 | 0.423 | 35.733 | 88.548 | 0.597 | 0.000 | 0.221 | 0.070 | 0.128 | 0.539 | 0.203 | 0.407 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.854 | 0.000 | 1.000 |
| Cloture, conference, and judicial review | 0.644 | 0.630 | 0.929 | 0.967 | 0.050 | 3.918 | 23.055 | 0.696 | 0.000 | 0.033 | 0.033 | 0.084 | 0.624 | 0.010 | 0.146 | 0.199 | 0.000 | 0.000 | 0.068 | 0.000 | 0.167 | 0.000 | 0.270 |
| Committee-first regular order | 0.665 | 0.594 | 0.893 | 0.969 | 0.203 | 15.950 | 20.820 | 0.652 | 0.000 | 0.097 | 0.031 | 0.110 | 0.556 | 0.055 | 0.210 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.453 | 0.000 | 0.258 |
| Compensation amendments + majority | 0.661 | 0.565 | 0.837 | 0.930 | 0.312 | 25.176 | 88.548 | 0.608 | 0.000 | 0.211 | 0.070 | 0.088 | 0.544 | 0.111 | 0.295 | 0.254 | 0.000 | 0.000 | 0.000 | 0.170 | 0.629 | 0.000 | 1.000 |
| Constitutional court architecture | 0.652 | 0.565 | 0.836 | 0.892 | 0.313 | 25.264 | 88.548 | 0.608 | 0.000 | 0.211 | 0.108 | 0.086 | 0.545 | 0.112 | 0.294 | 0.255 | 0.000 | 0.000 | 0.000 | 0.175 | 0.628 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.655 | 0.651 | 0.930 | 0.984 | 0.055 | 4.290 | 19.872 | 0.710 | 0.000 | 0.007 | 0.016 | 0.064 | 0.683 | 0.012 | 0.150 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.177 | 0.000 | 0.227 |
| Default pass unless 2/3 block | 0.724 | 0.475 | 0.630 | 0.930 | 0.860 | 75.564 | 88.548 | 0.500 | 0.422 | 0.477 | 0.070 | 0.187 | 0.390 | 0.628 | 0.609 | 0.276 | 0.000 | 0.000 | 0.000 | 0.000 | 0.988 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.682 | 0.491 | 0.701 | 0.893 | 0.645 | 63.336 | 88.548 | 0.520 | 0.339 | 0.440 | 0.107 | 0.176 | 0.409 | 0.391 | 0.477 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.853 | 0.458 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.705 | 0.509 | 0.721 | 0.794 | 0.795 | 73.413 | 88.548 | 0.463 | 0.256 | 0.379 | 0.206 | 0.115 | 0.449 | 0.279 | 0.317 | 0.286 | 0.000 | 0.000 | 0.736 | 0.276 | 0.864 | 0.415 | 1.000 |
| District-population public-will model | 0.655 | 0.565 | 0.860 | 0.930 | 0.264 | 21.151 | 88.548 | 0.622 | 0.000 | 0.333 | 0.070 | 0.126 | 0.457 | 0.080 | 0.249 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.556 | 0.000 | 1.000 |
| Expanded portfolio hybrid legislature | 0.676 | 0.623 | 0.904 | 0.402 | 0.772 | 65.955 | 80.352 | 0.556 | 0.000 | 0.003 | 0.598 | 0.047 | 0.581 | 0.047 | 0.035 | 0.229 | 0.466 | 0.386 | 1.000 | 0.653 | 0.797 | 0.000 | 0.908 |
| Harm-weighted double majority | 0.663 | 0.571 | 0.878 | 0.930 | 0.272 | 22.306 | 88.548 | 0.621 | 0.000 | 0.200 | 0.070 | 0.106 | 0.542 | 0.092 | 0.280 | 0.244 | 0.000 | 0.000 | 0.000 | 0.000 | 0.592 | 0.000 | 1.000 |
| Campaign-finance influence system | 0.675 | 0.574 | 0.874 | 0.938 | 0.317 | 26.278 | 78.881 | 0.628 | 0.000 | 0.139 | 0.062 | 0.113 | 0.559 | 0.122 | 0.311 | 0.205 | 0.465 | 0.384 | 0.000 | 0.000 | 0.684 | 0.000 | 0.892 |
| Active-law registry + majority review | 0.655 | 0.556 | 0.839 | 0.886 | 0.338 | 27.456 | 88.548 | 0.600 | 0.000 | 0.242 | 0.114 | 0.130 | 0.516 | 0.186 | 0.339 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.649 | 0.000 | 1.000 |
| Leadership agenda cartel + majority | 0.659 | 0.588 | 0.908 | 0.973 | 0.165 | 13.685 | 33.658 | 0.662 | 0.000 | 0.112 | 0.027 | 0.090 | 0.584 | 0.051 | 0.234 | 0.150 | 0.000 | 0.000 | 0.000 | 0.000 | 0.589 | 0.000 | 0.385 |
| Long-horizon strategic learning | 0.677 | 0.537 | 0.797 | 0.790 | 0.581 | 48.707 | 88.467 | 0.485 | 0.000 | 0.250 | 0.210 | 0.109 | 0.502 | 0.196 | 0.317 | 0.305 | 0.162 | 0.652 | 0.999 | 0.270 | 0.647 | 0.000 | 0.999 |
| Multidimensional package bargaining + majority | 0.639 | 0.558 | 0.837 | 0.828 | 0.332 | 26.746 | 88.548 | 0.588 | 0.000 | 0.220 | 0.172 | 0.099 | 0.532 | 0.121 | 0.308 | 0.262 | 0.000 | 0.000 | 0.368 | 0.368 | 0.641 | 0.000 | 1.000 |
| Endogenous norm erosion + majority | 0.631 | 0.559 | 0.846 | 0.800 | 0.318 | 25.758 | 83.618 | 0.610 | 0.000 | 0.247 | 0.200 | 0.123 | 0.515 | 0.114 | 0.319 | 0.258 | 0.000 | 0.000 | 0.950 | 0.022 | 0.608 | 0.000 | 0.950 |
| Omnibus bargaining + majority | 0.628 | 0.560 | 0.848 | 0.740 | 0.365 | 29.444 | 88.548 | 0.583 | 0.000 | 0.160 | 0.260 | 0.076 | 0.549 | 0.138 | 0.317 | 0.262 | 0.000 | 0.000 | 0.680 | 0.680 | 0.668 | 0.000 | 1.000 |
| Package bargaining + majority | 0.654 | 0.562 | 0.844 | 0.890 | 0.321 | 25.868 | 88.548 | 0.606 | 0.000 | 0.221 | 0.110 | 0.112 | 0.530 | 0.116 | 0.304 | 0.259 | 0.000 | 0.000 | 0.284 | 0.284 | 0.634 | 0.000 | 1.000 |
| Parliamentary coalition confidence | 0.664 | 0.540 | 0.910 | 0.981 | 0.225 | 17.323 | 21.461 | 0.598 | 0.000 | 0.064 | 0.019 | 0.073 | 0.555 | 0.062 | 0.189 | 0.170 | 0.000 | 0.000 | 0.000 | 0.000 | 0.568 | 0.000 | 0.277 |
| Portfolio hybrid legislature | 0.705 | 0.624 | 0.932 | 0.763 | 0.503 | 43.131 | 54.992 | 0.620 | 0.000 | 0.032 | 0.237 | 0.064 | 0.600 | 0.075 | 0.090 | 0.148 | 0.104 | 0.599 | 0.405 | 0.016 | 0.777 | 0.000 | 0.623 |
| Bicameral majority + presidential veto | 0.643 | 0.602 | 0.893 | 0.930 | 0.146 | 11.297 | 88.548 | 0.649 | 0.000 | 0.117 | 0.070 | 0.103 | 0.587 | 0.038 | 0.208 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.000 | 1.000 |
| Proposal bonds + majority | 0.665 | 0.563 | 0.856 | 0.931 | 0.311 | 25.095 | 87.238 | 0.614 | 0.000 | 0.210 | 0.069 | 0.122 | 0.529 | 0.111 | 0.296 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.630 | 0.000 | 0.992 |
| Majority + public-interest screen | 0.659 | 0.571 | 0.874 | 0.940 | 0.251 | 20.850 | 76.064 | 0.634 | 0.000 | 0.180 | 0.060 | 0.111 | 0.545 | 0.094 | 0.292 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.545 | 0.000 | 0.858 |
| Public objection window + majority | 0.644 | 0.590 | 0.895 | 0.866 | 0.227 | 18.243 | 88.548 | 0.651 | 0.000 | 0.119 | 0.134 | 0.093 | 0.580 | 0.063 | 0.218 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.566 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.621 | 0.576 | 0.880 | 0.780 | 0.246 | 19.103 | 49.314 | 0.634 | 0.000 | 0.175 | 0.220 | 0.105 | 0.552 | 0.076 | 0.245 | 0.224 | 0.000 | 0.000 | 0.000 | 0.000 | 0.559 | 0.000 | 0.603 |
| Risk-routed majority legislature | 0.684 | 0.544 | 0.844 | 0.831 | 0.517 | 42.634 | 88.548 | 0.512 | 0.000 | 0.236 | 0.169 | 0.102 | 0.513 | 0.178 | 0.319 | 0.290 | 0.000 | 0.000 | 0.642 | 0.225 | 0.671 | 0.000 | 1.000 |
| Unicameral simple majority | 0.665 | 0.563 | 0.855 | 0.930 | 0.312 | 25.216 | 88.548 | 0.613 | 0.000 | 0.211 | 0.070 | 0.122 | 0.529 | 0.112 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.629 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.711 | 0.655 | 0.938 | 0.715 | 0.536 | 46.154 | 48.987 | 0.632 | 0.000 | 0.002 | 0.285 | 0.055 | 0.643 | 0.005 | 0.004 | 0.226 | 0.000 | 0.000 | 0.561 | 0.000 | 0.809 | 0.000 | 0.561 |
| Unicameral 60 percent passage | 0.648 | 0.629 | 0.905 | 0.930 | 0.128 | 9.545 | 88.548 | 0.672 | 0.000 | 0.060 | 0.070 | 0.093 | 0.622 | 0.027 | 0.153 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.270 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, compromises less, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Compromise | Gridlock | Weak public mandate | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.952 | 0.000 | 0.663 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.183 | 0.638 |
| Baseline | Committee-first regular order | 0.154 | 0.274 | 0.846 | 0.080 | 0.656 |
| Baseline | Parliamentary coalition confidence | 0.179 | 0.287 | 0.821 | 0.050 | 0.635 |
| Baseline | Unicameral majority + pairwise alternatives | 0.545 | 0.488 | 0.455 | 0.002 | 0.381 |
| Baseline | Citizen assembly threshold gate | 0.180 | 0.259 | 0.820 | 0.037 | 0.640 |
| Baseline | Risk-routed majority legislature | 0.478 | 0.235 | 0.522 | 0.246 | 0.540 |
| Baseline | Portfolio hybrid legislature | 0.508 | 0.402 | 0.492 | 0.036 | 0.433 |
| Baseline | Expanded portfolio hybrid legislature | 0.800 | 0.443 | 0.200 | 0.005 | 0.268 |
| Baseline | Default pass unless 2/3 block | 0.838 | 0.104 | 0.162 | 0.491 | 0.448 |
| Baseline | Default pass + multi-round mediation + challenge | 0.719 | 0.218 | 0.281 | 0.399 | 0.455 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.172 | 0.386 | 0.828 | 0.011 | 0.600 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.182 | 0.494 |
| Low Polarization | Committee-first regular order | 0.388 | 0.309 | 0.612 | 0.082 | 0.530 |
| Low Polarization | Parliamentary coalition confidence | 0.479 | 0.302 | 0.521 | 0.097 | 0.489 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.632 | 0.633 | 0.368 | 0.002 | 0.294 |
| Low Polarization | Citizen assembly threshold gate | 0.407 | 0.298 | 0.593 | 0.035 | 0.514 |
| Low Polarization | Risk-routed majority legislature | 0.683 | 0.273 | 0.318 | 0.244 | 0.426 |
| Low Polarization | Portfolio hybrid legislature | 0.650 | 0.433 | 0.350 | 0.048 | 0.355 |
| Low Polarization | Expanded portfolio hybrid legislature | 0.866 | 0.512 | 0.134 | 0.008 | 0.215 |
| Low Polarization | Default pass unless 2/3 block | 0.845 | 0.199 | 0.155 | 0.376 | 0.393 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.804 | 0.266 | 0.196 | 0.340 | 0.386 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.022 | 0.361 | 0.978 | 0.000 | 0.680 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.188 | 0.687 |
| High Polarization | Committee-first regular order | 0.094 | 0.269 | 0.906 | 0.068 | 0.686 |
| High Polarization | Parliamentary coalition confidence | 0.096 | 0.301 | 0.904 | 0.017 | 0.665 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.489 | 0.446 | 0.511 | 0.003 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.122 | 0.249 | 0.878 | 0.017 | 0.668 |
| High Polarization | Risk-routed majority legislature | 0.367 | 0.223 | 0.633 | 0.236 | 0.597 |
| High Polarization | Portfolio hybrid legislature | 0.434 | 0.393 | 0.566 | 0.024 | 0.470 |
| High Polarization | Expanded portfolio hybrid legislature | 0.727 | 0.425 | 0.273 | 0.002 | 0.309 |
| High Polarization | Default pass unless 2/3 block | 0.839 | 0.081 | 0.161 | 0.548 | 0.466 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.685 | 0.206 | 0.315 | 0.443 | 0.484 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.052 | 0.346 | 0.948 | 0.011 | 0.673 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.183 | 0.630 |
| Low Party Loyalty | Committee-first regular order | 0.166 | 0.264 | 0.834 | 0.089 | 0.656 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.185 | 0.280 | 0.815 | 0.054 | 0.635 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.535 | 0.503 | 0.465 | 0.003 | 0.382 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.201 | 0.244 | 0.799 | 0.037 | 0.633 |
| Low Party Loyalty | Risk-routed majority legislature | 0.502 | 0.235 | 0.498 | 0.245 | 0.527 |
| Low Party Loyalty | Portfolio hybrid legislature | 0.519 | 0.395 | 0.481 | 0.041 | 0.430 |
| Low Party Loyalty | Expanded portfolio hybrid legislature | 0.802 | 0.452 | 0.198 | 0.003 | 0.264 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.839 | 0.105 | 0.161 | 0.502 | 0.449 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.735 | 0.221 | 0.265 | 0.403 | 0.447 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.050 | 0.371 | 0.950 | 0.006 | 0.665 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.193 | 0.635 |
| High Party Loyalty | Committee-first regular order | 0.163 | 0.283 | 0.837 | 0.094 | 0.652 |
| High Party Loyalty | Parliamentary coalition confidence | 0.196 | 0.284 | 0.804 | 0.057 | 0.629 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.553 | 0.503 | 0.447 | 0.002 | 0.373 |
| High Party Loyalty | Citizen assembly threshold gate | 0.191 | 0.260 | 0.809 | 0.037 | 0.634 |
| High Party Loyalty | Risk-routed majority legislature | 0.487 | 0.236 | 0.513 | 0.246 | 0.535 |
| High Party Loyalty | Portfolio hybrid legislature | 0.514 | 0.408 | 0.486 | 0.040 | 0.428 |
| High Party Loyalty | Expanded portfolio hybrid legislature | 0.805 | 0.453 | 0.195 | 0.003 | 0.262 |
| High Party Loyalty | Default pass unless 2/3 block | 0.847 | 0.110 | 0.153 | 0.479 | 0.440 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.710 | 0.221 | 0.290 | 0.390 | 0.456 |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark | 0.032 | 0.372 | 0.968 | 0.000 | 0.673 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.147 | 0.652 |
| Low Compromise Culture | Committee-first regular order | 0.123 | 0.292 | 0.877 | 0.069 | 0.664 |
| Low Compromise Culture | Parliamentary coalition confidence | 0.147 | 0.298 | 0.853 | 0.024 | 0.642 |
| Low Compromise Culture | Unicameral majority + pairwise alternatives | 0.528 | 0.471 | 0.472 | 0.002 | 0.395 |
| Low Compromise Culture | Citizen assembly threshold gate | 0.156 | 0.271 | 0.844 | 0.014 | 0.644 |
| Low Compromise Culture | Risk-routed majority legislature | 0.375 | 0.238 | 0.625 | 0.203 | 0.582 |
| Low Compromise Culture | Portfolio hybrid legislature | 0.488 | 0.394 | 0.512 | 0.032 | 0.444 |
| Low Compromise Culture | Expanded portfolio hybrid legislature | 0.745 | 0.429 | 0.255 | 0.002 | 0.299 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.823 | 0.103 | 0.177 | 0.493 | 0.456 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.681 | 0.212 | 0.319 | 0.402 | 0.476 |
| High Compromise Culture | Stylized U.S.-like conventional benchmark | 0.070 | 0.372 | 0.930 | 0.006 | 0.654 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.222 | 0.617 |
| High Compromise Culture | Committee-first regular order | 0.194 | 0.283 | 0.806 | 0.111 | 0.640 |
| High Compromise Culture | Parliamentary coalition confidence | 0.232 | 0.278 | 0.768 | 0.086 | 0.618 |
| High Compromise Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.534 | 0.443 | 0.002 | 0.362 |
| High Compromise Culture | Citizen assembly threshold gate | 0.223 | 0.256 | 0.778 | 0.054 | 0.623 |
| High Compromise Culture | Risk-routed majority legislature | 0.584 | 0.236 | 0.416 | 0.286 | 0.495 |
| High Compromise Culture | Portfolio hybrid legislature | 0.559 | 0.416 | 0.441 | 0.052 | 0.406 |
| High Compromise Culture | Expanded portfolio hybrid legislature | 0.842 | 0.475 | 0.158 | 0.005 | 0.237 |
| High Compromise Culture | Default pass unless 2/3 block | 0.858 | 0.109 | 0.142 | 0.498 | 0.438 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.760 | 0.224 | 0.240 | 0.400 | 0.433 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.383 | 0.943 | 0.007 | 0.658 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.180 | 0.633 |
| Low Lobbying Pressure | Committee-first regular order | 0.162 | 0.296 | 0.838 | 0.081 | 0.646 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.200 | 0.284 | 0.800 | 0.078 | 0.630 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.569 | 0.515 | 0.431 | 0.002 | 0.362 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.191 | 0.257 | 0.809 | 0.032 | 0.634 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.476 | 0.221 | 0.524 | 0.291 | 0.554 |
| Low Lobbying Pressure | Portfolio hybrid legislature | 0.562 | 0.409 | 0.438 | 0.040 | 0.404 |
| Low Lobbying Pressure | Expanded portfolio hybrid legislature | 0.863 | 0.457 | 0.137 | 0.005 | 0.233 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.846 | 0.103 | 0.154 | 0.494 | 0.445 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.714 | 0.206 | 0.286 | 0.427 | 0.467 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.366 | 0.973 | 0.005 | 0.678 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.205 | 0.654 |
| High Lobbying Pressure | Committee-first regular order | 0.137 | 0.266 | 0.863 | 0.096 | 0.671 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.137 | 0.309 | 0.863 | 0.029 | 0.645 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.487 | 0.476 | 0.513 | 0.005 | 0.415 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.158 | 0.275 | 0.842 | 0.032 | 0.645 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.396 | 0.251 | 0.604 | 0.228 | 0.572 |
| High Lobbying Pressure | Portfolio hybrid legislature | 0.454 | 0.393 | 0.546 | 0.035 | 0.462 |
| High Lobbying Pressure | Expanded portfolio hybrid legislature | 0.654 | 0.444 | 0.346 | 0.001 | 0.340 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.828 | 0.107 | 0.172 | 0.502 | 0.454 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.714 | 0.229 | 0.286 | 0.421 | 0.459 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.387 | 0.973 | 0.016 | 0.674 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.231 | 0.658 |
| Weak Constituency Pressure | Committee-first regular order | 0.129 | 0.282 | 0.871 | 0.117 | 0.674 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.123 | 0.329 | 0.877 | 0.055 | 0.651 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.527 | 0.467 | 0.473 | 0.003 | 0.397 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.156 | 0.279 | 0.844 | 0.036 | 0.646 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.457 | 0.247 | 0.543 | 0.331 | 0.564 |
| Weak Constituency Pressure | Portfolio hybrid legislature | 0.483 | 0.400 | 0.517 | 0.046 | 0.448 |
| Weak Constituency Pressure | Expanded portfolio hybrid legislature | 0.767 | 0.439 | 0.233 | 0.004 | 0.286 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.872 | 0.102 | 0.128 | 0.520 | 0.437 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.739 | 0.225 | 0.261 | 0.461 | 0.455 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.011 | 0.666 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.189 | 0.633 |
| Two-Party System | Committee-first regular order | 0.157 | 0.286 | 0.843 | 0.066 | 0.649 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.486 | 0.457 | 0.003 | 0.383 |
| Two-Party System | Citizen assembly threshold gate | 0.193 | 0.257 | 0.807 | 0.030 | 0.633 |
| Two-Party System | Risk-routed majority legislature | 0.467 | 0.236 | 0.533 | 0.238 | 0.543 |
| Two-Party System | Portfolio hybrid legislature | 0.513 | 0.401 | 0.487 | 0.037 | 0.431 |
| Two-Party System | Expanded portfolio hybrid legislature | 0.803 | 0.440 | 0.197 | 0.002 | 0.267 |
| Two-Party System | Default pass unless 2/3 block | 0.842 | 0.108 | 0.158 | 0.502 | 0.447 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.829 | 0.207 | 0.171 | 0.412 | 0.406 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.054 | 0.360 | 0.946 | 0.005 | 0.666 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.191 | 0.628 |
| Multi-Party System | Committee-first regular order | 0.175 | 0.275 | 0.825 | 0.104 | 0.651 |
| Multi-Party System | Parliamentary coalition confidence | 0.263 | 0.256 | 0.737 | 0.065 | 0.605 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.541 | 0.509 | 0.459 | 0.003 | 0.377 |
| Multi-Party System | Citizen assembly threshold gate | 0.202 | 0.260 | 0.798 | 0.034 | 0.628 |
| Multi-Party System | Risk-routed majority legislature | 0.502 | 0.239 | 0.498 | 0.258 | 0.529 |
| Multi-Party System | Portfolio hybrid legislature | 0.525 | 0.405 | 0.475 | 0.046 | 0.425 |
| Multi-Party System | Expanded portfolio hybrid legislature | 0.814 | 0.459 | 0.186 | 0.004 | 0.256 |
| Multi-Party System | Default pass unless 2/3 block | 0.837 | 0.110 | 0.163 | 0.505 | 0.450 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.639 | 0.232 | 0.361 | 0.371 | 0.485 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.050 | 0.373 | 0.950 | 0.005 | 0.664 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.186 | 0.634 |
| High Proposal Pressure | Committee-first regular order | 0.159 | 0.283 | 0.841 | 0.091 | 0.654 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.187 | 0.290 | 0.813 | 0.053 | 0.630 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.496 | 0.460 | 0.001 | 0.382 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.026 | 0.633 |
| High Proposal Pressure | Risk-routed majority legislature | 0.484 | 0.239 | 0.516 | 0.254 | 0.537 |
| High Proposal Pressure | Portfolio hybrid legislature | 0.510 | 0.403 | 0.490 | 0.038 | 0.432 |
| High Proposal Pressure | Expanded portfolio hybrid legislature | 0.799 | 0.448 | 0.201 | 0.003 | 0.267 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.842 | 0.107 | 0.158 | 0.500 | 0.447 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.901 | 0.203 | 0.099 | 0.431 | 0.375 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.371 | 0.951 | 0.006 | 0.665 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.188 | 0.635 |
| Extreme Proposal Pressure | Committee-first regular order | 0.160 | 0.283 | 0.840 | 0.084 | 0.652 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.184 | 0.290 | 0.816 | 0.046 | 0.630 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.383 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.186 | 0.264 | 0.814 | 0.029 | 0.633 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.474 | 0.239 | 0.526 | 0.250 | 0.541 |
| Extreme Proposal Pressure | Portfolio hybrid legislature | 0.514 | 0.399 | 0.486 | 0.039 | 0.431 |
| Extreme Proposal Pressure | Expanded portfolio hybrid legislature | 0.799 | 0.445 | 0.201 | 0.003 | 0.268 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.843 | 0.106 | 0.157 | 0.499 | 0.447 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.941 | 0.199 | 0.059 | 0.437 | 0.357 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.023 | 0.353 | 0.977 | 0.002 | 0.683 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.216 | 0.661 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.126 | 0.273 | 0.874 | 0.092 | 0.673 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.116 | 0.316 | 0.884 | 0.028 | 0.653 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.460 | 0.455 | 0.540 | 0.001 | 0.434 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.148 | 0.277 | 0.853 | 0.040 | 0.651 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.375 | 0.259 | 0.625 | 0.238 | 0.582 |
| Lobby-Fueled Flooding | Portfolio hybrid legislature | 0.428 | 0.381 | 0.572 | 0.032 | 0.478 |
| Lobby-Fueled Flooding | Expanded portfolio hybrid legislature | 0.610 | 0.426 | 0.390 | 0.002 | 0.367 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.842 | 0.107 | 0.158 | 0.516 | 0.451 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.895 | 0.208 | 0.105 | 0.452 | 0.380 |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.380 | 0.980 | 0.011 | 0.678 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.160 | 0.675 |
| Low-Compromise Flooding | Committee-first regular order | 0.094 | 0.286 | 0.906 | 0.078 | 0.683 |
| Low-Compromise Flooding | Parliamentary coalition confidence | 0.102 | 0.314 | 0.898 | 0.015 | 0.658 |
| Low-Compromise Flooding | Unicameral majority + pairwise alternatives | 0.498 | 0.461 | 0.502 | 0.001 | 0.413 |
| Low-Compromise Flooding | Citizen assembly threshold gate | 0.122 | 0.270 | 0.878 | 0.015 | 0.661 |
| Low-Compromise Flooding | Risk-routed majority legislature | 0.342 | 0.235 | 0.658 | 0.214 | 0.601 |
| Low-Compromise Flooding | Portfolio hybrid legislature | 0.433 | 0.400 | 0.568 | 0.027 | 0.469 |
| Low-Compromise Flooding | Expanded portfolio hybrid legislature | 0.696 | 0.433 | 0.304 | 0.001 | 0.322 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.835 | 0.092 | 0.165 | 0.521 | 0.459 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.884 | 0.189 | 0.116 | 0.442 | 0.390 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.015 | 0.366 | 0.985 | 0.006 | 0.684 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.231 | 0.687 |
| Capture Crisis | Committee-first regular order | 0.099 | 0.257 | 0.901 | 0.085 | 0.691 |
| Capture Crisis | Parliamentary coalition confidence | 0.070 | 0.329 | 0.930 | 0.017 | 0.670 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.405 | 0.455 | 0.595 | 0.001 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.110 | 0.268 | 0.890 | 0.045 | 0.674 |
| Capture Crisis | Risk-routed majority legislature | 0.324 | 0.258 | 0.676 | 0.231 | 0.607 |
| Capture Crisis | Portfolio hybrid legislature | 0.380 | 0.386 | 0.620 | 0.027 | 0.499 |
| Capture Crisis | Expanded portfolio hybrid legislature | 0.515 | 0.435 | 0.485 | 0.002 | 0.412 |
| Capture Crisis | Default pass unless 2/3 block | 0.839 | 0.100 | 0.161 | 0.517 | 0.454 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.890 | 0.205 | 0.110 | 0.448 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.074 | 0.375 | 0.926 | 0.003 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.195 | 0.593 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.224 | 0.283 | 0.776 | 0.081 | 0.619 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.273 | 0.282 | 0.727 | 0.065 | 0.592 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.543 | 0.543 | 0.457 | 0.001 | 0.366 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.254 | 0.276 | 0.746 | 0.046 | 0.600 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.508 | 0.266 | 0.492 | 0.220 | 0.510 |
| Popular Anti-Lobbying Push | Portfolio hybrid legislature | 0.521 | 0.412 | 0.479 | 0.052 | 0.426 |
| Popular Anti-Lobbying Push | Expanded portfolio hybrid legislature | 0.762 | 0.478 | 0.238 | 0.003 | 0.276 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.825 | 0.128 | 0.175 | 0.462 | 0.441 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.865 | 0.230 | 0.135 | 0.407 | 0.380 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.052 | 0.370 | 0.948 | 0.003 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.180 | 0.632 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.161 | 0.291 | 0.839 | 0.085 | 0.649 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.540 | 0.507 | 0.460 | 0.002 | 0.378 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.188 | 0.264 | 0.812 | 0.021 | 0.631 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.475 | 0.237 | 0.525 | 0.242 | 0.540 |
| Weighted Two-Party Baseline | Portfolio hybrid legislature | 0.516 | 0.412 | 0.484 | 0.038 | 0.426 |
| Weighted Two-Party Baseline | Expanded portfolio hybrid legislature | 0.793 | 0.455 | 0.207 | 0.003 | 0.267 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.836 | 0.108 | 0.164 | 0.501 | 0.450 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.821 | 0.206 | 0.179 | 0.417 | 0.411 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.393 | 0.950 | 0.000 | 0.657 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.193 | 0.637 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.159 | 0.279 | 0.841 | 0.082 | 0.653 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.254 | 0.256 | 0.746 | 0.088 | 0.614 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.544 | 0.509 | 0.456 | 0.002 | 0.376 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.193 | 0.259 | 0.807 | 0.029 | 0.632 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.488 | 0.237 | 0.512 | 0.262 | 0.537 |
| Weighted Two Major Plus Minors | Portfolio hybrid legislature | 0.521 | 0.408 | 0.479 | 0.043 | 0.426 |
| Weighted Two Major Plus Minors | Expanded portfolio hybrid legislature | 0.802 | 0.460 | 0.198 | 0.002 | 0.262 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.847 | 0.107 | 0.153 | 0.503 | 0.445 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.642 | 0.226 | 0.358 | 0.384 | 0.488 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.070 | 0.363 | 0.930 | 0.006 | 0.657 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.190 | 0.608 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.205 | 0.287 | 0.795 | 0.097 | 0.631 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.339 | 0.244 | 0.661 | 0.069 | 0.571 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.551 | 0.532 | 0.449 | 0.002 | 0.365 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.237 | 0.261 | 0.763 | 0.038 | 0.611 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.543 | 0.244 | 0.457 | 0.265 | 0.508 |
| Weighted Fragmented Multiparty | Portfolio hybrid legislature | 0.547 | 0.412 | 0.453 | 0.052 | 0.413 |
| Weighted Fragmented Multiparty | Expanded portfolio hybrid legislature | 0.822 | 0.470 | 0.178 | 0.004 | 0.249 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.835 | 0.122 | 0.165 | 0.479 | 0.442 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.628 | 0.245 | 0.372 | 0.345 | 0.481 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.048 | 0.384 | 0.952 | 0.003 | 0.661 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.181 | 0.628 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.170 | 0.284 | 0.830 | 0.072 | 0.644 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.200 | 0.286 | 0.800 | 0.033 | 0.621 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.552 | 0.524 | 0.448 | 0.002 | 0.367 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.208 | 0.264 | 0.792 | 0.029 | 0.623 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.477 | 0.241 | 0.523 | 0.258 | 0.541 |
| Weighted Dominant-Party Legislature | Portfolio hybrid legislature | 0.527 | 0.415 | 0.473 | 0.046 | 0.421 |
| Weighted Dominant-Party Legislature | Expanded portfolio hybrid legislature | 0.807 | 0.472 | 0.193 | 0.003 | 0.256 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.805 | 0.117 | 0.195 | 0.472 | 0.457 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.658 | 0.228 | 0.342 | 0.379 | 0.478 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.177 | 0.377 | 0.823 | 0.010 | 0.600 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.204 | 0.507 |
| Era 1 Low Contention | Committee-first regular order | 0.369 | 0.298 | 0.631 | 0.102 | 0.546 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.514 | 0.273 | 0.486 | 0.118 | 0.484 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.638 | 0.375 | 0.002 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.386 | 0.287 | 0.614 | 0.053 | 0.532 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.705 | 0.255 | 0.295 | 0.279 | 0.427 |
| Era 1 Low Contention | Portfolio hybrid legislature | 0.666 | 0.439 | 0.334 | 0.050 | 0.345 |
| Era 1 Low Contention | Expanded portfolio hybrid legislature | 0.889 | 0.520 | 0.111 | 0.008 | 0.201 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.849 | 0.180 | 0.151 | 0.402 | 0.402 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.780 | 0.254 | 0.220 | 0.335 | 0.401 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.111 | 0.377 | 0.889 | 0.008 | 0.633 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.219 | 0.564 |
| Era 2 Normal Contention | Committee-first regular order | 0.285 | 0.293 | 0.715 | 0.094 | 0.588 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.418 | 0.265 | 0.582 | 0.102 | 0.532 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.588 | 0.568 | 0.413 | 0.003 | 0.336 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.299 | 0.279 | 0.701 | 0.043 | 0.576 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.619 | 0.253 | 0.381 | 0.283 | 0.471 |
| Era 2 Normal Contention | Portfolio hybrid legislature | 0.613 | 0.420 | 0.387 | 0.057 | 0.379 |
| Era 2 Normal Contention | Expanded portfolio hybrid legislature | 0.865 | 0.484 | 0.135 | 0.005 | 0.223 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.842 | 0.149 | 0.158 | 0.453 | 0.425 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.737 | 0.244 | 0.263 | 0.362 | 0.431 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.061 | 0.380 | 0.939 | 0.005 | 0.656 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.184 | 0.612 |
| Era 3 Polarizing | Committee-first regular order | 0.198 | 0.280 | 0.802 | 0.097 | 0.636 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.300 | 0.256 | 0.700 | 0.067 | 0.587 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.554 | 0.510 | 0.446 | 0.002 | 0.371 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.221 | 0.269 | 0.779 | 0.031 | 0.615 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.511 | 0.248 | 0.489 | 0.264 | 0.523 |
| Era 3 Polarizing | Portfolio hybrid legislature | 0.535 | 0.400 | 0.465 | 0.044 | 0.422 |
| Era 3 Polarizing | Expanded portfolio hybrid legislature | 0.814 | 0.454 | 0.186 | 0.003 | 0.258 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.840 | 0.119 | 0.160 | 0.480 | 0.440 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.662 | 0.237 | 0.338 | 0.365 | 0.471 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.028 | 0.372 | 0.972 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.179 | 0.656 |
| Era 4 High Contention | Committee-first regular order | 0.125 | 0.280 | 0.875 | 0.090 | 0.671 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.124 | 0.309 | 0.876 | 0.027 | 0.651 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.517 | 0.475 | 0.483 | 0.001 | 0.399 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.152 | 0.260 | 0.848 | 0.017 | 0.649 |
| Era 4 High Contention | Risk-routed majority legislature | 0.405 | 0.245 | 0.595 | 0.235 | 0.571 |
| Era 4 High Contention | Portfolio hybrid legislature | 0.460 | 0.402 | 0.540 | 0.033 | 0.456 |
| Era 4 High Contention | Expanded portfolio hybrid legislature | 0.724 | 0.441 | 0.276 | 0.002 | 0.306 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.838 | 0.100 | 0.162 | 0.513 | 0.454 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.764 | 0.210 | 0.236 | 0.423 | 0.440 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.347 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.206 | 0.698 |
| Era 5 Capture Contention | Committee-first regular order | 0.087 | 0.256 | 0.913 | 0.091 | 0.698 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.439 | 0.428 | 0.561 | 0.003 | 0.452 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.111 | 0.255 | 0.889 | 0.028 | 0.674 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.328 | 0.238 | 0.672 | 0.233 | 0.611 |
| Era 5 Capture Contention | Portfolio hybrid legislature | 0.388 | 0.377 | 0.612 | 0.032 | 0.499 |
| Era 5 Capture Contention | Expanded portfolio hybrid legislature | 0.585 | 0.413 | 0.415 | 0.002 | 0.384 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.834 | 0.087 | 0.166 | 0.539 | 0.465 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.866 | 0.194 | 0.134 | 0.446 | 0.398 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.010 | 0.352 | 0.990 | 0.007 | 0.691 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.241 | 0.721 |
| Era 6 Crisis | Committee-first regular order | 0.064 | 0.255 | 0.936 | 0.099 | 0.711 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.359 | 0.414 | 0.641 | 0.002 | 0.497 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.075 | 0.262 | 0.925 | 0.031 | 0.690 |
| Era 6 Crisis | Risk-routed majority legislature | 0.267 | 0.237 | 0.733 | 0.229 | 0.641 |
| Era 6 Crisis | Portfolio hybrid legislature | 0.316 | 0.378 | 0.684 | 0.021 | 0.533 |
| Era 6 Crisis | Expanded portfolio hybrid legislature | 0.461 | 0.404 | 0.539 | 0.002 | 0.449 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.843 | 0.082 | 0.157 | 0.558 | 0.465 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.894 | 0.187 | 0.106 | 0.464 | 0.390 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.340 | 0.810 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.016 | 0.129 | 0.984 | 0.035 | 0.760 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.043 | 0.129 | 0.957 | 0.138 | 0.767 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.641 | 0.498 | 0.359 | 0.002 | 0.330 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.094 | 0.102 | 0.906 | 0.031 | 0.728 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.608 | 0.185 | 0.392 | 0.168 | 0.474 |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature | 0.794 | 0.506 | 0.206 | 0.000 | 0.251 |
| Adversarial High-Benefit Extreme Reform | Expanded portfolio hybrid legislature | 0.993 | 0.528 | 0.007 | 0.000 | 0.145 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.906 | 0.046 | 0.094 | 0.575 | 0.448 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.772 | 0.182 | 0.228 | 0.242 | 0.408 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.206 | 0.404 | 0.794 | 0.001 | 0.576 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.010 | 0.280 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.624 | 0.319 | 0.376 | 0.062 | 0.404 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.423 | 0.406 | 0.577 | 0.001 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.206 | 0.422 | 0.794 | 0.195 | 0.609 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.982 | 0.361 | 0.018 | 0.009 | 0.203 |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature | 0.368 | 0.507 | 0.632 | 0.000 | 0.464 |
| Adversarial Popular Harmful Bill | Expanded portfolio hybrid legislature | 0.899 | 0.520 | 0.101 | 0.000 | 0.195 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 0.999 | 0.262 | 0.001 | 0.013 | 0.224 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.990 | 0.358 | 0.010 | 0.010 | 0.200 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.059 | 0.552 | 0.941 | 0.002 | 0.605 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.290 | 0.226 |
| Adversarial Moderate Capture | Committee-first regular order | 0.834 | 0.498 | 0.166 | 0.272 | 0.288 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.850 | 0.533 | 0.150 | 0.107 | 0.237 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.567 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.423 | 0.533 | 0.577 | 0.468 | 0.522 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.985 | 0.525 | 0.015 | 0.239 | 0.198 |
| Adversarial Moderate Capture | Portfolio hybrid legislature | 0.187 | 0.485 | 0.813 | 0.018 | 0.565 |
| Adversarial Moderate Capture | Expanded portfolio hybrid legislature | 0.578 | 0.514 | 0.422 | 0.001 | 0.357 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.308 | 0.216 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.994 | 0.523 | 0.006 | 0.245 | 0.195 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.003 | 0.283 | 0.997 | 0.045 | 0.723 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.593 | 0.752 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.139 | 0.287 | 0.861 | 0.093 | 0.663 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.211 | 0.277 | 0.789 | 0.387 | 0.689 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.489 | 0.478 | 0.511 | 0.005 | 0.413 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.273 | 0.233 | 0.727 | 0.061 | 0.606 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.698 | 0.267 | 0.302 | 0.352 | 0.442 |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature | 0.709 | 0.473 | 0.291 | 0.004 | 0.304 |
| Adversarial Delayed-Benefit Reform | Expanded portfolio hybrid legislature | 0.986 | 0.494 | 0.014 | 0.000 | 0.159 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.863 | 0.114 | 0.137 | 0.753 | 0.485 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.843 | 0.260 | 0.157 | 0.426 | 0.386 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.048 | 0.373 | 0.952 | 0.003 | 0.665 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.117 | 0.495 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.264 | 0.307 | 0.736 | 0.129 | 0.602 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.390 | 0.303 | 0.610 | 0.029 | 0.520 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.476 | 0.518 | 0.524 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.073 | 0.378 | 0.928 | 0.067 | 0.664 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.757 | 0.287 | 0.243 | 0.081 | 0.352 |
| Adversarial Concentrated Rights Harm | Portfolio hybrid legislature | 0.434 | 0.463 | 0.566 | 0.001 | 0.444 |
| Adversarial Concentrated Rights Harm | Expanded portfolio hybrid legislature | 0.914 | 0.492 | 0.086 | 0.000 | 0.195 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.979 | 0.174 | 0.021 | 0.190 | 0.297 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.844 | 0.285 | 0.156 | 0.106 | 0.313 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.043 | 0.373 | 0.957 | 0.013 | 0.669 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.295 | 0.614 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.197 | 0.303 | 0.803 | 0.184 | 0.648 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.323 | 0.321 | 0.677 | 0.112 | 0.564 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.415 | 0.496 | 0.585 | 0.003 | 0.444 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.260 | 0.331 | 0.740 | 0.035 | 0.578 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.404 | 0.335 | 0.596 | 0.245 | 0.547 |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature | 0.589 | 0.444 | 0.411 | 0.009 | 0.374 |
| Adversarial Anti-Lobbying Backlash | Expanded portfolio hybrid legislature | 0.767 | 0.471 | 0.233 | 0.000 | 0.275 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.893 | 0.208 | 0.107 | 0.576 | 0.406 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.706 | 0.317 | 0.294 | 0.462 | 0.444 |

## Default-Pass Side Note: Challenge-Voucher Deltas

Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.308 | -0.255 | 0.022 | -0.076 | -0.298 | -0.143 | 0.500 |
| Low Polarization | -11.108 | -0.185 | 0.029 | -0.136 | -0.140 | -0.063 | 0.499 |
| High Polarization | -17.208 | -0.287 | 0.012 | -0.025 | -0.356 | -0.157 | 0.500 |
| Low Party Loyalty | -15.100 | -0.252 | 0.028 | -0.086 | -0.298 | -0.142 | 0.500 |
| High Party Loyalty | -15.950 | -0.266 | 0.024 | -0.059 | -0.308 | -0.144 | 0.500 |
| Low Compromise Culture | -15.442 | -0.257 | 0.019 | -0.053 | -0.300 | -0.142 | 0.500 |
| High Compromise Culture | -15.283 | -0.255 | 0.026 | -0.093 | -0.291 | -0.137 | 0.500 |
| Low Lobbying Pressure | -15.642 | -0.261 | 0.023 | -0.068 | -0.302 | -0.142 | 0.500 |
| High Lobbying Pressure | -14.933 | -0.249 | 0.019 | -0.062 | -0.290 | -0.143 | 0.500 |
| Weak Constituency Pressure | -17.983 | -0.300 | 0.023 | -0.073 | -0.327 | -0.145 | 0.499 |
| Two-Party System | -6.358 | -0.106 | -0.007 | -0.012 | -0.142 | -0.080 | 0.333 |
| Multi-Party System | -30.017 | -0.500 | 0.117 | -0.301 | -0.523 | -0.322 | 0.802 |
| High Proposal Pressure | 3.325 | 0.018 | -0.016 | 0.016 | -0.028 | -0.055 | 0.167 |
| Extreme Proposal Pressure | 22.075 | 0.074 | -0.022 | 0.022 | 0.022 | -0.047 | 0.100 |
| Lobby-Fueled Flooding | 2.717 | 0.015 | -0.015 | 0.014 | -0.031 | -0.053 | 0.167 |
| Low-Compromise Flooding | 2.883 | 0.016 | -0.017 | 0.017 | -0.047 | -0.074 | 0.167 |
| Capture Crisis | 2.775 | 0.015 | -0.014 | 0.019 | -0.040 | -0.064 | 0.167 |
| Popular Anti-Lobbying Push | -2.142 | -0.018 | -0.013 | -0.008 | -0.056 | -0.057 | 0.250 |
| Weighted Two-Party Baseline | -6.158 | -0.103 | -0.005 | -0.026 | -0.145 | -0.083 | 0.333 |
| Weighted Two Major Plus Minors | -30.933 | -0.516 | 0.113 | -0.279 | -0.540 | -0.333 | 0.801 |
| Weighted Fragmented Multiparty | -29.683 | -0.495 | 0.116 | -0.357 | -0.485 | -0.302 | 0.857 |
| Weighted Dominant-Party Legislature | -19.642 | -0.327 | 0.040 | -0.166 | -0.338 | -0.170 | 0.667 |
| Era 1 Low Contention | -16.358 | -0.273 | 0.053 | -0.218 | -0.234 | -0.114 | 0.658 |
| Era 2 Normal Contention | -22.758 | -0.379 | 0.084 | -0.297 | -0.371 | -0.216 | 0.723 |
| Era 3 Polarizing | -28.742 | -0.479 | 0.107 | -0.299 | -0.499 | -0.323 | 0.781 |
| Era 4 High Contention | -13.492 | -0.180 | 0.001 | -0.028 | -0.222 | -0.104 | 0.400 |
| Era 5 Capture Contention | -2.642 | -0.029 | -0.014 | 0.026 | -0.094 | -0.085 | 0.222 |
| Era 6 Crisis | 1.158 | 0.010 | -0.016 | 0.025 | -0.062 | -0.084 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.133 | -0.552 | -0.001 | -0.003 | -0.595 | -0.191 | 0.664 |
| Adversarial Popular Harmful Bill | -6.467 | -0.108 | -0.000 | -0.101 | -0.096 | -0.052 | 0.462 |
| Adversarial Moderate Capture | -1.292 | -0.022 | -0.000 | -0.017 | -0.009 | -0.003 | 0.330 |
| Adversarial Delayed-Benefit Reform | -27.608 | -0.460 | 0.003 | -0.107 | -0.446 | -0.230 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.667 | -0.394 | 0.030 | -0.221 | -0.329 | -0.179 | 0.652 |
| Adversarial Anti-Lobbying Backlash | -22.558 | -0.376 | 0.044 | -0.158 | -0.256 | -0.151 | 0.650 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest weak public-mandate passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.763) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.739) | Expanded portfolio hybrid legislature (0.866) | Unicameral majority + pairwise alternatives (0.002) |
| High Polarization | Parliamentary coalition confidence (0.748) | Default pass unless 2/3 block (0.839) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.759) | Default pass unless 2/3 block (0.839) | Unicameral majority + pairwise alternatives (0.003) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.755) | Default pass unless 2/3 block (0.847) | Unicameral majority + pairwise alternatives (0.002) |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark (0.767) | Default pass unless 2/3 block (0.823) | Stylized U.S.-like conventional benchmark (0.000) |
| High Compromise Culture | Stylized U.S.-like conventional benchmark (0.744) | Default pass unless 2/3 block (0.858) | Unicameral majority + pairwise alternatives (0.002) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Expanded portfolio hybrid legislature (0.863) | Unicameral majority + pairwise alternatives (0.002) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.753) | Default pass unless 2/3 block (0.828) | Expanded portfolio hybrid legislature (0.001) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.872) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.842) | Parliamentary coalition confidence (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.837) | Unicameral majority + pairwise alternatives (0.003) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.756) | Default pass + multi-round mediation + challenge (0.901) | Unicameral majority + pairwise alternatives (0.001) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.746) | Default pass + multi-round mediation + challenge (0.941) | Unicameral majority + pairwise alternatives (0.000) |
| Lobby-Fueled Flooding | Parliamentary coalition confidence (0.736) | Default pass + multi-round mediation + challenge (0.895) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark (0.747) | Default pass + multi-round mediation + challenge (0.884) | Expanded portfolio hybrid legislature (0.001) |
| Capture Crisis | Parliamentary coalition confidence (0.751) | Default pass + multi-round mediation + challenge (0.890) | Unicameral majority + pairwise alternatives (0.001) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.762) | Default pass + multi-round mediation + challenge (0.865) | Unicameral majority + pairwise alternatives (0.001) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.836) | Parliamentary coalition confidence (0.000) |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark (0.748) | Default pass unless 2/3 block (0.847) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Cloture, conference, and judicial review (0.749) | Default pass unless 2/3 block (0.835) | Unicameral majority + pairwise alternatives (0.002) |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark (0.745) | Expanded portfolio hybrid legislature (0.807) | Unicameral majority + pairwise alternatives (0.002) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.730) | Expanded portfolio hybrid legislature (0.889) | Unicameral majority + pairwise alternatives (0.002) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.753) | Expanded portfolio hybrid legislature (0.865) | Unicameral majority + pairwise alternatives (0.003) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.840) | Unicameral majority + pairwise alternatives (0.002) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.769) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark (0.744) | Default pass + multi-round mediation + challenge (0.866) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark (0.761) | Default pass + multi-round mediation + challenge (0.894) | Parliamentary coalition confidence (0.000) |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature (0.834) | Expanded portfolio hybrid legislature (0.993) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature (0.342) | Default pass unless 2/3 block (0.999) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Moderate Capture | Portfolio hybrid legislature (0.410) | Default pass unless 2/3 block (1.000) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature (0.819) | Expanded portfolio hybrid legislature (0.986) | Expanded portfolio hybrid legislature (0.000) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.630) | Default pass unless 2/3 block (0.979) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature (0.730) | Default pass unless 2/3 block (0.893) | Expanded portfolio hybrid legislature (0.000) |

## Interpretation

- This is a breadth-first paper campaign. Default pass is retained as one burden-shifting stress test, while the main comparison spans conventional thresholds, committee-first regular order, coalition confidence, policy tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation rules, anti-capture safeguards, adaptive risk routing, and law-registry review.
- Open default-pass remains the throughput extreme, but its high weak public-mandate passage and policy movement make it a diagnostic endpoint rather than the project focus.
- Policy tournaments and risk-routed majority systems occupy a promising compromise/productivity middle ground in this synthetic campaign, but tournament variants remain sensitive to clone, decoy, and overload stress; committee-first, public-interest, citizen, and parliamentary-style gates control risk but give up substantial throughput.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality, and generated welfare remains conditional on model assumptions.
- The next model extension should deepen non-default families beyond their current prototypes: multidimensional package bargaining, judicial/court intervention, executive emergency/delegated rulemaking, direct-democracy routes, electoral feedback, and media/information ecosystems.

## Reproduction

```sh
make campaign
```
