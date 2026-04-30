# Main Comparison Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 29
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

- The main comparison campaign is breadth-first: 29 scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.
- The scalar directional score is productivity-sensitive: its highest value came from Default pass unless 2/3 block at 0.724, which is why the report treats the score as a profile aid rather than a recommendation.
- Highest average welfare came from Stylized U.S.-like conventional benchmark at 0.710; highest compromise came from Unicameral majority + pairwise alternatives at 0.504.
- Highest productivity came from Default pass unless 2/3 block at 0.860.
- Open default-pass averaged 0.860 productivity, 0.476 weak public-mandate passage, and 0.628 policy shift, so it functions as a throughput/risk endpoint.
- The stylized U.S.-like conventional benchmark averaged 0.055 productivity and 0.710 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.
- The portfolio hybrid combines risk routing, pairwise alternatives, citizen/harm review, proposal bonds, anti-capture safeguards, and law review. It averaged 0.503 productivity, 0.417 compromise, 0.931 risk control, and 0.705 directional score, situating it between pairwise alternatives and risk routing rather than replacing the tradeoff frontier.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.647 | 0.572 | 0.880 | 0.967 | 0.170 | 13.924 | 41.032 | 0.636 | 0.000 | 0.175 | 0.033 | 0.111 | 0.550 | 0.060 | 0.290 | 0.232 | 0.000 | 0.000 | 0.000 | 0.000 | 0.395 | 0.000 | 0.465 |
| Majority + anti-capture bundle | 0.678 | 0.580 | 0.886 | 0.935 | 0.309 | 25.704 | 82.910 | 0.656 | 0.000 | 0.150 | 0.065 | 0.111 | 0.553 | 0.117 | 0.304 | 0.133 | 0.100 | 0.551 | 0.000 | 0.000 | 0.745 | 0.000 | 0.934 |
| Bicameral simple majority | 0.654 | 0.588 | 0.880 | 0.930 | 0.219 | 17.106 | 88.548 | 0.637 | 0.000 | 0.149 | 0.070 | 0.111 | 0.564 | 0.063 | 0.225 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.459 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.633 | 0.612 | 0.909 | 0.810 | 0.200 | 16.413 | 88.548 | 0.694 | 0.000 | 0.055 | 0.190 | 0.086 | 0.630 | 0.063 | 0.249 | 0.207 | 0.000 | 0.000 | 0.000 | 0.000 | 0.584 | 0.000 | 1.000 |
| Citizen initiative and referendum | 0.693 | 0.582 | 0.837 | 0.930 | 0.422 | 35.662 | 88.548 | 0.597 | 0.000 | 0.222 | 0.070 | 0.128 | 0.539 | 0.202 | 0.407 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.857 | 0.000 | 1.000 |
| Cloture, conference, and judicial review | 0.644 | 0.630 | 0.929 | 0.967 | 0.050 | 3.918 | 23.055 | 0.696 | 0.000 | 0.033 | 0.033 | 0.084 | 0.624 | 0.010 | 0.146 | 0.199 | 0.000 | 0.000 | 0.068 | 0.000 | 0.167 | 0.000 | 0.270 |
| Committee-first regular order | 0.665 | 0.594 | 0.893 | 0.969 | 0.203 | 15.950 | 20.820 | 0.652 | 0.000 | 0.097 | 0.031 | 0.110 | 0.556 | 0.055 | 0.210 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.453 | 0.000 | 0.258 |
| Compensation amendments + majority | 0.661 | 0.565 | 0.837 | 0.930 | 0.312 | 25.217 | 88.548 | 0.608 | 0.000 | 0.211 | 0.070 | 0.088 | 0.544 | 0.112 | 0.297 | 0.255 | 0.000 | 0.000 | 0.000 | 0.170 | 0.629 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.655 | 0.651 | 0.930 | 0.984 | 0.055 | 4.290 | 19.872 | 0.710 | 0.000 | 0.007 | 0.016 | 0.064 | 0.683 | 0.012 | 0.150 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.177 | 0.000 | 0.227 |
| Default pass unless 2/3 block | 0.724 | 0.475 | 0.630 | 0.930 | 0.860 | 75.561 | 88.548 | 0.501 | 0.422 | 0.476 | 0.070 | 0.187 | 0.390 | 0.628 | 0.609 | 0.276 | 0.000 | 0.000 | 0.000 | 0.000 | 0.988 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.683 | 0.490 | 0.701 | 0.893 | 0.645 | 63.364 | 88.548 | 0.520 | 0.339 | 0.440 | 0.107 | 0.176 | 0.409 | 0.391 | 0.477 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.852 | 0.458 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.705 | 0.508 | 0.724 | 0.794 | 0.795 | 73.445 | 88.548 | 0.462 | 0.257 | 0.380 | 0.206 | 0.115 | 0.448 | 0.279 | 0.317 | 0.286 | 0.000 | 0.000 | 0.736 | 0.276 | 0.865 | 0.415 | 1.000 |
| Harm-weighted double majority | 0.663 | 0.571 | 0.878 | 0.930 | 0.271 | 22.271 | 88.548 | 0.622 | 0.000 | 0.200 | 0.070 | 0.107 | 0.542 | 0.092 | 0.276 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 | 0.590 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.654 | 0.556 | 0.839 | 0.886 | 0.336 | 27.408 | 88.548 | 0.600 | 0.000 | 0.242 | 0.114 | 0.129 | 0.517 | 0.184 | 0.339 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.645 | 0.000 | 1.000 |
| Leadership agenda cartel + majority | 0.659 | 0.588 | 0.908 | 0.973 | 0.165 | 13.685 | 33.658 | 0.662 | 0.000 | 0.112 | 0.027 | 0.090 | 0.584 | 0.051 | 0.234 | 0.150 | 0.000 | 0.000 | 0.000 | 0.000 | 0.589 | 0.000 | 0.385 |
| Multidimensional package bargaining + majority | 0.639 | 0.558 | 0.836 | 0.828 | 0.332 | 26.715 | 88.548 | 0.589 | 0.000 | 0.220 | 0.172 | 0.100 | 0.533 | 0.121 | 0.309 | 0.262 | 0.000 | 0.000 | 0.368 | 0.368 | 0.643 | 0.000 | 1.000 |
| Endogenous norm erosion + majority | 0.631 | 0.559 | 0.847 | 0.800 | 0.318 | 25.778 | 83.598 | 0.610 | 0.000 | 0.245 | 0.200 | 0.122 | 0.516 | 0.114 | 0.320 | 0.257 | 0.000 | 0.000 | 0.950 | 0.022 | 0.608 | 0.000 | 0.950 |
| Package bargaining + majority | 0.654 | 0.562 | 0.844 | 0.890 | 0.321 | 25.894 | 88.548 | 0.607 | 0.000 | 0.221 | 0.110 | 0.112 | 0.529 | 0.116 | 0.302 | 0.257 | 0.000 | 0.000 | 0.283 | 0.283 | 0.634 | 0.000 | 1.000 |
| Parliamentary coalition confidence | 0.664 | 0.539 | 0.910 | 0.981 | 0.224 | 17.289 | 21.458 | 0.598 | 0.000 | 0.065 | 0.019 | 0.074 | 0.555 | 0.062 | 0.189 | 0.170 | 0.000 | 0.000 | 0.000 | 0.000 | 0.566 | 0.000 | 0.277 |
| Portfolio hybrid legislature | 0.705 | 0.624 | 0.931 | 0.763 | 0.503 | 43.170 | 55.100 | 0.620 | 0.000 | 0.033 | 0.237 | 0.064 | 0.600 | 0.076 | 0.091 | 0.148 | 0.104 | 0.598 | 0.405 | 0.016 | 0.777 | 0.000 | 0.624 |
| Bicameral majority + presidential veto | 0.643 | 0.602 | 0.893 | 0.930 | 0.146 | 11.297 | 88.548 | 0.649 | 0.000 | 0.117 | 0.070 | 0.103 | 0.587 | 0.038 | 0.208 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.000 | 1.000 |
| Proposal bonds + majority | 0.665 | 0.563 | 0.855 | 0.931 | 0.312 | 25.101 | 87.238 | 0.614 | 0.000 | 0.211 | 0.069 | 0.122 | 0.529 | 0.111 | 0.295 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.628 | 0.000 | 0.992 |
| Majority + public-interest screen | 0.659 | 0.570 | 0.874 | 0.940 | 0.252 | 20.908 | 76.064 | 0.633 | 0.000 | 0.182 | 0.060 | 0.112 | 0.544 | 0.093 | 0.294 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.546 | 0.000 | 0.858 |
| Public objection window + majority | 0.644 | 0.590 | 0.895 | 0.866 | 0.227 | 18.234 | 88.548 | 0.651 | 0.000 | 0.121 | 0.134 | 0.093 | 0.580 | 0.063 | 0.218 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.567 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.621 | 0.576 | 0.880 | 0.780 | 0.246 | 19.072 | 49.285 | 0.633 | 0.000 | 0.172 | 0.220 | 0.106 | 0.552 | 0.076 | 0.246 | 0.224 | 0.000 | 0.000 | 0.000 | 0.000 | 0.556 | 0.000 | 0.602 |
| Risk-routed majority legislature | 0.684 | 0.544 | 0.843 | 0.831 | 0.518 | 42.687 | 88.548 | 0.512 | 0.000 | 0.238 | 0.169 | 0.102 | 0.513 | 0.178 | 0.319 | 0.290 | 0.000 | 0.000 | 0.641 | 0.225 | 0.672 | 0.000 | 1.000 |
| Unicameral simple majority | 0.665 | 0.563 | 0.855 | 0.930 | 0.312 | 25.216 | 88.548 | 0.613 | 0.000 | 0.211 | 0.070 | 0.122 | 0.529 | 0.112 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.629 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.711 | 0.656 | 0.938 | 0.715 | 0.536 | 46.156 | 48.984 | 0.632 | 0.000 | 0.002 | 0.285 | 0.055 | 0.643 | 0.005 | 0.004 | 0.226 | 0.000 | 0.000 | 0.561 | 0.000 | 0.808 | 0.000 | 0.561 |
| Unicameral 60 percent passage | 0.648 | 0.629 | 0.905 | 0.930 | 0.128 | 9.545 | 88.548 | 0.672 | 0.000 | 0.060 | 0.070 | 0.093 | 0.622 | 0.027 | 0.153 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.270 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, compromises less, or enacts more bills with generated public support below majority.

| Era | Scenario | Productivity | Compromise | Gridlock | Weak public mandate | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.952 | 0.000 | 0.663 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.183 | 0.638 |
| Baseline | Committee-first regular order | 0.154 | 0.274 | 0.846 | 0.080 | 0.656 |
| Baseline | Parliamentary coalition confidence | 0.180 | 0.284 | 0.820 | 0.047 | 0.634 |
| Baseline | Unicameral majority + pairwise alternatives | 0.545 | 0.490 | 0.455 | 0.003 | 0.381 |
| Baseline | Citizen assembly threshold gate | 0.181 | 0.262 | 0.819 | 0.029 | 0.637 |
| Baseline | Risk-routed majority legislature | 0.482 | 0.235 | 0.518 | 0.247 | 0.538 |
| Baseline | Portfolio hybrid legislature | 0.513 | 0.399 | 0.487 | 0.041 | 0.432 |
| Baseline | Default pass unless 2/3 block | 0.838 | 0.104 | 0.162 | 0.491 | 0.448 |
| Baseline | Default pass + multi-round mediation + challenge | 0.725 | 0.218 | 0.275 | 0.403 | 0.452 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.172 | 0.386 | 0.828 | 0.011 | 0.600 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.182 | 0.494 |
| Low Polarization | Committee-first regular order | 0.388 | 0.309 | 0.612 | 0.082 | 0.530 |
| Low Polarization | Parliamentary coalition confidence | 0.486 | 0.301 | 0.514 | 0.104 | 0.488 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.632 | 0.633 | 0.368 | 0.001 | 0.295 |
| Low Polarization | Citizen assembly threshold gate | 0.410 | 0.294 | 0.590 | 0.041 | 0.515 |
| Low Polarization | Risk-routed majority legislature | 0.675 | 0.275 | 0.325 | 0.243 | 0.429 |
| Low Polarization | Portfolio hybrid legislature | 0.648 | 0.432 | 0.352 | 0.051 | 0.357 |
| Low Polarization | Default pass unless 2/3 block | 0.839 | 0.201 | 0.161 | 0.373 | 0.395 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.803 | 0.266 | 0.197 | 0.338 | 0.386 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.022 | 0.361 | 0.978 | 0.000 | 0.680 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.188 | 0.687 |
| High Polarization | Committee-first regular order | 0.094 | 0.269 | 0.906 | 0.068 | 0.686 |
| High Polarization | Parliamentary coalition confidence | 0.096 | 0.297 | 0.904 | 0.023 | 0.668 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.489 | 0.448 | 0.511 | 0.003 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.119 | 0.244 | 0.881 | 0.015 | 0.670 |
| High Polarization | Risk-routed majority legislature | 0.366 | 0.228 | 0.634 | 0.239 | 0.596 |
| High Polarization | Portfolio hybrid legislature | 0.441 | 0.389 | 0.559 | 0.031 | 0.469 |
| High Polarization | Default pass unless 2/3 block | 0.835 | 0.081 | 0.165 | 0.544 | 0.467 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.684 | 0.205 | 0.316 | 0.446 | 0.486 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.052 | 0.346 | 0.948 | 0.011 | 0.673 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.183 | 0.630 |
| Low Party Loyalty | Committee-first regular order | 0.166 | 0.264 | 0.834 | 0.089 | 0.656 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.183 | 0.281 | 0.817 | 0.052 | 0.635 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.536 | 0.502 | 0.464 | 0.003 | 0.382 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.200 | 0.246 | 0.800 | 0.034 | 0.633 |
| Low Party Loyalty | Risk-routed majority legislature | 0.505 | 0.232 | 0.495 | 0.251 | 0.528 |
| Low Party Loyalty | Portfolio hybrid legislature | 0.528 | 0.395 | 0.472 | 0.043 | 0.426 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.844 | 0.105 | 0.156 | 0.503 | 0.447 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.746 | 0.220 | 0.254 | 0.409 | 0.443 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.050 | 0.371 | 0.950 | 0.006 | 0.665 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.193 | 0.635 |
| High Party Loyalty | Committee-first regular order | 0.163 | 0.283 | 0.837 | 0.094 | 0.652 |
| High Party Loyalty | Parliamentary coalition confidence | 0.196 | 0.288 | 0.804 | 0.058 | 0.627 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.554 | 0.503 | 0.446 | 0.002 | 0.372 |
| High Party Loyalty | Citizen assembly threshold gate | 0.196 | 0.262 | 0.804 | 0.028 | 0.629 |
| High Party Loyalty | Risk-routed majority legislature | 0.476 | 0.238 | 0.524 | 0.246 | 0.540 |
| High Party Loyalty | Portfolio hybrid legislature | 0.521 | 0.404 | 0.479 | 0.041 | 0.427 |
| High Party Loyalty | Default pass unless 2/3 block | 0.844 | 0.110 | 0.156 | 0.477 | 0.441 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.716 | 0.221 | 0.284 | 0.393 | 0.454 |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark | 0.032 | 0.372 | 0.968 | 0.000 | 0.673 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.147 | 0.652 |
| Low Compromise Culture | Committee-first regular order | 0.123 | 0.292 | 0.877 | 0.069 | 0.664 |
| Low Compromise Culture | Parliamentary coalition confidence | 0.148 | 0.299 | 0.853 | 0.017 | 0.640 |
| Low Compromise Culture | Unicameral majority + pairwise alternatives | 0.526 | 0.470 | 0.474 | 0.002 | 0.396 |
| Low Compromise Culture | Citizen assembly threshold gate | 0.160 | 0.269 | 0.840 | 0.010 | 0.641 |
| Low Compromise Culture | Risk-routed majority legislature | 0.383 | 0.237 | 0.617 | 0.207 | 0.579 |
| Low Compromise Culture | Portfolio hybrid legislature | 0.485 | 0.396 | 0.515 | 0.036 | 0.446 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.830 | 0.102 | 0.170 | 0.494 | 0.453 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.672 | 0.212 | 0.328 | 0.404 | 0.481 |
| High Compromise Culture | Stylized U.S.-like conventional benchmark | 0.070 | 0.372 | 0.930 | 0.006 | 0.654 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.222 | 0.617 |
| High Compromise Culture | Committee-first regular order | 0.194 | 0.283 | 0.806 | 0.111 | 0.640 |
| High Compromise Culture | Parliamentary coalition confidence | 0.236 | 0.274 | 0.764 | 0.088 | 0.618 |
| High Compromise Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.534 | 0.443 | 0.002 | 0.362 |
| High Compromise Culture | Citizen assembly threshold gate | 0.219 | 0.257 | 0.781 | 0.055 | 0.624 |
| High Compromise Culture | Risk-routed majority legislature | 0.579 | 0.233 | 0.421 | 0.287 | 0.498 |
| High Compromise Culture | Portfolio hybrid legislature | 0.554 | 0.417 | 0.446 | 0.049 | 0.408 |
| High Compromise Culture | Default pass unless 2/3 block | 0.853 | 0.109 | 0.147 | 0.498 | 0.440 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.761 | 0.224 | 0.239 | 0.400 | 0.432 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.383 | 0.943 | 0.007 | 0.658 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.180 | 0.633 |
| Low Lobbying Pressure | Committee-first regular order | 0.162 | 0.296 | 0.838 | 0.081 | 0.646 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.203 | 0.280 | 0.797 | 0.082 | 0.631 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.570 | 0.515 | 0.430 | 0.003 | 0.361 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.192 | 0.256 | 0.808 | 0.030 | 0.633 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.477 | 0.222 | 0.523 | 0.295 | 0.554 |
| Low Lobbying Pressure | Portfolio hybrid legislature | 0.563 | 0.410 | 0.437 | 0.039 | 0.403 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.847 | 0.103 | 0.153 | 0.495 | 0.445 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.709 | 0.207 | 0.291 | 0.425 | 0.468 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.366 | 0.973 | 0.005 | 0.678 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.205 | 0.654 |
| High Lobbying Pressure | Committee-first regular order | 0.137 | 0.266 | 0.863 | 0.096 | 0.671 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.135 | 0.307 | 0.865 | 0.027 | 0.646 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.490 | 0.476 | 0.510 | 0.004 | 0.413 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.156 | 0.271 | 0.844 | 0.035 | 0.648 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.398 | 0.253 | 0.602 | 0.221 | 0.570 |
| High Lobbying Pressure | Portfolio hybrid legislature | 0.462 | 0.394 | 0.538 | 0.038 | 0.458 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.834 | 0.106 | 0.166 | 0.504 | 0.452 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.718 | 0.228 | 0.282 | 0.417 | 0.456 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.387 | 0.973 | 0.016 | 0.674 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.231 | 0.658 |
| Weak Constituency Pressure | Committee-first regular order | 0.129 | 0.282 | 0.871 | 0.117 | 0.674 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.121 | 0.331 | 0.879 | 0.058 | 0.652 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.524 | 0.468 | 0.476 | 0.003 | 0.399 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.160 | 0.270 | 0.840 | 0.033 | 0.645 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.462 | 0.246 | 0.538 | 0.336 | 0.562 |
| Weak Constituency Pressure | Portfolio hybrid legislature | 0.475 | 0.402 | 0.525 | 0.043 | 0.450 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.874 | 0.102 | 0.126 | 0.520 | 0.436 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.742 | 0.225 | 0.258 | 0.462 | 0.454 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.011 | 0.666 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.189 | 0.633 |
| Two-Party System | Committee-first regular order | 0.157 | 0.286 | 0.843 | 0.066 | 0.649 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.544 | 0.485 | 0.456 | 0.003 | 0.383 |
| Two-Party System | Citizen assembly threshold gate | 0.190 | 0.262 | 0.810 | 0.027 | 0.632 |
| Two-Party System | Risk-routed majority legislature | 0.474 | 0.238 | 0.526 | 0.251 | 0.542 |
| Two-Party System | Portfolio hybrid legislature | 0.517 | 0.398 | 0.483 | 0.041 | 0.430 |
| Two-Party System | Default pass unless 2/3 block | 0.841 | 0.108 | 0.159 | 0.502 | 0.447 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.828 | 0.206 | 0.172 | 0.413 | 0.407 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.054 | 0.360 | 0.946 | 0.005 | 0.666 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.191 | 0.628 |
| Multi-Party System | Committee-first regular order | 0.175 | 0.275 | 0.825 | 0.104 | 0.651 |
| Multi-Party System | Parliamentary coalition confidence | 0.268 | 0.252 | 0.732 | 0.075 | 0.605 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.541 | 0.511 | 0.459 | 0.004 | 0.377 |
| Multi-Party System | Citizen assembly threshold gate | 0.199 | 0.263 | 0.801 | 0.025 | 0.627 |
| Multi-Party System | Risk-routed majority legislature | 0.500 | 0.241 | 0.500 | 0.261 | 0.530 |
| Multi-Party System | Portfolio hybrid legislature | 0.528 | 0.403 | 0.472 | 0.047 | 0.425 |
| Multi-Party System | Default pass unless 2/3 block | 0.840 | 0.108 | 0.160 | 0.507 | 0.449 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.640 | 0.234 | 0.360 | 0.376 | 0.485 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.050 | 0.373 | 0.950 | 0.005 | 0.664 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.186 | 0.634 |
| High Proposal Pressure | Committee-first regular order | 0.159 | 0.283 | 0.841 | 0.091 | 0.654 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.186 | 0.293 | 0.814 | 0.050 | 0.629 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.495 | 0.460 | 0.001 | 0.382 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.186 | 0.262 | 0.814 | 0.032 | 0.635 |
| High Proposal Pressure | Risk-routed majority legislature | 0.480 | 0.240 | 0.520 | 0.253 | 0.539 |
| High Proposal Pressure | Portfolio hybrid legislature | 0.513 | 0.400 | 0.487 | 0.038 | 0.431 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.846 | 0.107 | 0.154 | 0.502 | 0.445 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.901 | 0.204 | 0.099 | 0.434 | 0.375 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.371 | 0.951 | 0.006 | 0.665 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.188 | 0.635 |
| Extreme Proposal Pressure | Committee-first regular order | 0.160 | 0.283 | 0.840 | 0.084 | 0.652 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.289 | 0.815 | 0.047 | 0.630 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.382 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.185 | 0.265 | 0.815 | 0.028 | 0.634 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.478 | 0.237 | 0.523 | 0.251 | 0.540 |
| Extreme Proposal Pressure | Portfolio hybrid legislature | 0.514 | 0.400 | 0.486 | 0.037 | 0.430 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.842 | 0.105 | 0.158 | 0.499 | 0.447 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.941 | 0.199 | 0.059 | 0.436 | 0.357 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.023 | 0.353 | 0.977 | 0.002 | 0.683 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.216 | 0.661 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.126 | 0.273 | 0.874 | 0.092 | 0.673 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.114 | 0.319 | 0.886 | 0.034 | 0.654 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.460 | 0.455 | 0.540 | 0.001 | 0.434 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.145 | 0.278 | 0.855 | 0.039 | 0.652 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.373 | 0.259 | 0.627 | 0.239 | 0.584 |
| Lobby-Fueled Flooding | Portfolio hybrid legislature | 0.430 | 0.381 | 0.570 | 0.033 | 0.477 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.840 | 0.107 | 0.160 | 0.514 | 0.451 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.897 | 0.207 | 0.103 | 0.451 | 0.379 |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark | 0.020 | 0.380 | 0.980 | 0.011 | 0.678 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.160 | 0.675 |
| Low-Compromise Flooding | Committee-first regular order | 0.094 | 0.286 | 0.906 | 0.078 | 0.683 |
| Low-Compromise Flooding | Parliamentary coalition confidence | 0.100 | 0.314 | 0.900 | 0.014 | 0.658 |
| Low-Compromise Flooding | Unicameral majority + pairwise alternatives | 0.495 | 0.461 | 0.505 | 0.001 | 0.415 |
| Low-Compromise Flooding | Citizen assembly threshold gate | 0.125 | 0.266 | 0.875 | 0.016 | 0.661 |
| Low-Compromise Flooding | Risk-routed majority legislature | 0.340 | 0.234 | 0.660 | 0.215 | 0.602 |
| Low-Compromise Flooding | Portfolio hybrid legislature | 0.430 | 0.402 | 0.570 | 0.026 | 0.470 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.835 | 0.091 | 0.165 | 0.521 | 0.459 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.884 | 0.188 | 0.116 | 0.444 | 0.390 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.015 | 0.366 | 0.985 | 0.006 | 0.684 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.231 | 0.687 |
| Capture Crisis | Committee-first regular order | 0.099 | 0.257 | 0.901 | 0.085 | 0.691 |
| Capture Crisis | Parliamentary coalition confidence | 0.069 | 0.333 | 0.931 | 0.023 | 0.670 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.405 | 0.455 | 0.595 | 0.001 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.109 | 0.270 | 0.891 | 0.044 | 0.673 |
| Capture Crisis | Risk-routed majority legislature | 0.329 | 0.256 | 0.671 | 0.233 | 0.606 |
| Capture Crisis | Portfolio hybrid legislature | 0.378 | 0.386 | 0.622 | 0.029 | 0.501 |
| Capture Crisis | Default pass unless 2/3 block | 0.841 | 0.100 | 0.159 | 0.519 | 0.453 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.890 | 0.205 | 0.110 | 0.449 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.074 | 0.375 | 0.926 | 0.003 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.195 | 0.593 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.224 | 0.283 | 0.776 | 0.081 | 0.619 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.271 | 0.285 | 0.729 | 0.068 | 0.593 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.545 | 0.543 | 0.455 | 0.001 | 0.365 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.253 | 0.275 | 0.747 | 0.045 | 0.600 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.507 | 0.267 | 0.493 | 0.221 | 0.511 |
| Popular Anti-Lobbying Push | Portfolio hybrid legislature | 0.520 | 0.411 | 0.480 | 0.049 | 0.426 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.826 | 0.128 | 0.174 | 0.462 | 0.441 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.866 | 0.230 | 0.134 | 0.406 | 0.379 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.052 | 0.370 | 0.948 | 0.003 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.180 | 0.632 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.161 | 0.291 | 0.839 | 0.085 | 0.649 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.541 | 0.507 | 0.459 | 0.002 | 0.378 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.190 | 0.264 | 0.810 | 0.026 | 0.631 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.470 | 0.237 | 0.530 | 0.240 | 0.542 |
| Weighted Two-Party Baseline | Portfolio hybrid legislature | 0.515 | 0.413 | 0.485 | 0.038 | 0.426 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.839 | 0.108 | 0.161 | 0.499 | 0.448 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.828 | 0.206 | 0.172 | 0.414 | 0.407 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.393 | 0.950 | 0.000 | 0.657 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.193 | 0.637 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.159 | 0.279 | 0.841 | 0.082 | 0.653 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.254 | 0.258 | 0.746 | 0.085 | 0.613 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.545 | 0.509 | 0.455 | 0.002 | 0.375 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.188 | 0.268 | 0.813 | 0.033 | 0.632 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.487 | 0.236 | 0.513 | 0.265 | 0.538 |
| Weighted Two Major Plus Minors | Portfolio hybrid legislature | 0.522 | 0.407 | 0.478 | 0.039 | 0.425 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.845 | 0.107 | 0.155 | 0.504 | 0.446 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.639 | 0.228 | 0.361 | 0.387 | 0.489 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.070 | 0.363 | 0.930 | 0.006 | 0.657 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.190 | 0.608 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.205 | 0.287 | 0.795 | 0.097 | 0.631 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.342 | 0.246 | 0.658 | 0.073 | 0.570 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.551 | 0.531 | 0.449 | 0.003 | 0.366 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.230 | 0.266 | 0.770 | 0.034 | 0.612 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.533 | 0.244 | 0.467 | 0.265 | 0.513 |
| Weighted Fragmented Multiparty | Portfolio hybrid legislature | 0.548 | 0.412 | 0.453 | 0.048 | 0.412 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.840 | 0.122 | 0.160 | 0.483 | 0.440 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.633 | 0.245 | 0.367 | 0.352 | 0.480 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.048 | 0.384 | 0.952 | 0.003 | 0.661 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.181 | 0.628 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.170 | 0.284 | 0.830 | 0.072 | 0.644 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.198 | 0.287 | 0.802 | 0.042 | 0.623 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.550 | 0.524 | 0.450 | 0.003 | 0.368 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.205 | 0.264 | 0.795 | 0.024 | 0.623 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.475 | 0.239 | 0.525 | 0.243 | 0.540 |
| Weighted Dominant-Party Legislature | Portfolio hybrid legislature | 0.531 | 0.411 | 0.469 | 0.046 | 0.420 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.806 | 0.117 | 0.194 | 0.470 | 0.456 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.660 | 0.227 | 0.340 | 0.376 | 0.477 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.177 | 0.377 | 0.823 | 0.010 | 0.600 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.204 | 0.507 |
| Era 1 Low Contention | Committee-first regular order | 0.369 | 0.298 | 0.631 | 0.102 | 0.546 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.510 | 0.275 | 0.490 | 0.118 | 0.486 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.639 | 0.375 | 0.002 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.390 | 0.284 | 0.610 | 0.049 | 0.529 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.715 | 0.255 | 0.285 | 0.282 | 0.423 |
| Era 1 Low Contention | Portfolio hybrid legislature | 0.669 | 0.439 | 0.331 | 0.050 | 0.344 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.846 | 0.179 | 0.154 | 0.400 | 0.404 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.781 | 0.255 | 0.219 | 0.334 | 0.400 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.111 | 0.377 | 0.889 | 0.008 | 0.633 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.219 | 0.564 |
| Era 2 Normal Contention | Committee-first regular order | 0.285 | 0.293 | 0.715 | 0.094 | 0.588 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.419 | 0.263 | 0.581 | 0.099 | 0.531 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.569 | 0.413 | 0.003 | 0.337 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.303 | 0.279 | 0.697 | 0.043 | 0.573 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.624 | 0.253 | 0.376 | 0.288 | 0.469 |
| Era 2 Normal Contention | Portfolio hybrid legislature | 0.608 | 0.418 | 0.392 | 0.053 | 0.381 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.839 | 0.149 | 0.161 | 0.450 | 0.425 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.736 | 0.245 | 0.264 | 0.363 | 0.431 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.061 | 0.380 | 0.939 | 0.005 | 0.656 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.184 | 0.612 |
| Era 3 Polarizing | Committee-first regular order | 0.198 | 0.280 | 0.802 | 0.097 | 0.636 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.298 | 0.257 | 0.702 | 0.071 | 0.588 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.554 | 0.510 | 0.446 | 0.002 | 0.370 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.224 | 0.266 | 0.776 | 0.029 | 0.614 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.508 | 0.245 | 0.492 | 0.252 | 0.523 |
| Era 3 Polarizing | Portfolio hybrid legislature | 0.532 | 0.400 | 0.468 | 0.043 | 0.423 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.841 | 0.119 | 0.159 | 0.479 | 0.439 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.663 | 0.237 | 0.338 | 0.370 | 0.472 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.028 | 0.372 | 0.972 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.179 | 0.656 |
| Era 4 High Contention | Committee-first regular order | 0.125 | 0.280 | 0.875 | 0.090 | 0.671 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.123 | 0.308 | 0.877 | 0.026 | 0.651 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.516 | 0.475 | 0.484 | 0.002 | 0.400 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.153 | 0.259 | 0.847 | 0.017 | 0.649 |
| Era 4 High Contention | Risk-routed majority legislature | 0.400 | 0.248 | 0.600 | 0.231 | 0.572 |
| Era 4 High Contention | Portfolio hybrid legislature | 0.463 | 0.399 | 0.537 | 0.035 | 0.456 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.834 | 0.100 | 0.166 | 0.510 | 0.455 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.763 | 0.212 | 0.237 | 0.423 | 0.440 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.347 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.206 | 0.698 |
| Era 5 Capture Contention | Committee-first regular order | 0.087 | 0.256 | 0.913 | 0.091 | 0.698 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.441 | 0.428 | 0.559 | 0.003 | 0.452 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.104 | 0.261 | 0.896 | 0.028 | 0.675 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.327 | 0.240 | 0.673 | 0.232 | 0.611 |
| Era 5 Capture Contention | Portfolio hybrid legislature | 0.382 | 0.377 | 0.618 | 0.029 | 0.502 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.836 | 0.087 | 0.164 | 0.541 | 0.464 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.866 | 0.194 | 0.134 | 0.449 | 0.399 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.010 | 0.352 | 0.990 | 0.007 | 0.691 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.241 | 0.721 |
| Era 6 Crisis | Committee-first regular order | 0.064 | 0.255 | 0.936 | 0.099 | 0.711 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.359 | 0.412 | 0.641 | 0.002 | 0.497 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.076 | 0.263 | 0.924 | 0.032 | 0.690 |
| Era 6 Crisis | Risk-routed majority legislature | 0.266 | 0.237 | 0.734 | 0.227 | 0.641 |
| Era 6 Crisis | Portfolio hybrid legislature | 0.317 | 0.376 | 0.683 | 0.022 | 0.533 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.840 | 0.082 | 0.160 | 0.558 | 0.467 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.892 | 0.188 | 0.108 | 0.465 | 0.391 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.340 | 0.810 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.016 | 0.129 | 0.984 | 0.035 | 0.760 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.036 | 0.125 | 0.964 | 0.152 | 0.775 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.639 | 0.499 | 0.361 | 0.001 | 0.331 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.098 | 0.103 | 0.903 | 0.038 | 0.728 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.619 | 0.187 | 0.381 | 0.177 | 0.470 |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature | 0.793 | 0.508 | 0.207 | 0.000 | 0.251 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.907 | 0.046 | 0.093 | 0.575 | 0.448 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.765 | 0.182 | 0.235 | 0.246 | 0.412 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.206 | 0.404 | 0.794 | 0.001 | 0.576 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.010 | 0.280 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.624 | 0.319 | 0.376 | 0.062 | 0.404 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.422 | 0.408 | 0.578 | 0.001 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.209 | 0.418 | 0.791 | 0.225 | 0.615 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.982 | 0.361 | 0.018 | 0.010 | 0.203 |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature | 0.371 | 0.503 | 0.629 | 0.000 | 0.463 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 1.000 | 0.262 | 0.000 | 0.013 | 0.224 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.989 | 0.360 | 0.011 | 0.008 | 0.199 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.059 | 0.552 | 0.941 | 0.002 | 0.605 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.290 | 0.226 |
| Adversarial Moderate Capture | Committee-first regular order | 0.834 | 0.498 | 0.166 | 0.272 | 0.288 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.849 | 0.532 | 0.151 | 0.106 | 0.237 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.568 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.434 | 0.534 | 0.566 | 0.497 | 0.522 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.987 | 0.525 | 0.013 | 0.241 | 0.197 |
| Adversarial Moderate Capture | Portfolio hybrid legislature | 0.190 | 0.486 | 0.810 | 0.022 | 0.564 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.308 | 0.216 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.993 | 0.524 | 0.007 | 0.246 | 0.195 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.003 | 0.283 | 0.997 | 0.045 | 0.723 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.593 | 0.752 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.139 | 0.287 | 0.861 | 0.093 | 0.663 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.209 | 0.276 | 0.791 | 0.391 | 0.691 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.490 | 0.476 | 0.510 | 0.005 | 0.413 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.273 | 0.235 | 0.727 | 0.055 | 0.604 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.687 | 0.268 | 0.313 | 0.353 | 0.447 |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature | 0.708 | 0.474 | 0.292 | 0.005 | 0.305 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.861 | 0.114 | 0.139 | 0.752 | 0.486 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.843 | 0.260 | 0.157 | 0.423 | 0.385 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.048 | 0.373 | 0.952 | 0.003 | 0.665 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.117 | 0.495 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.264 | 0.307 | 0.736 | 0.129 | 0.602 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.386 | 0.304 | 0.614 | 0.027 | 0.521 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.475 | 0.519 | 0.525 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.071 | 0.380 | 0.929 | 0.061 | 0.663 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.766 | 0.287 | 0.234 | 0.075 | 0.346 |
| Adversarial Concentrated Rights Harm | Portfolio hybrid legislature | 0.434 | 0.463 | 0.566 | 0.001 | 0.444 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.977 | 0.174 | 0.023 | 0.189 | 0.297 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.846 | 0.286 | 0.154 | 0.104 | 0.312 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.043 | 0.373 | 0.957 | 0.013 | 0.669 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.295 | 0.614 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.197 | 0.303 | 0.803 | 0.184 | 0.648 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.326 | 0.319 | 0.674 | 0.109 | 0.563 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.417 | 0.498 | 0.583 | 0.004 | 0.443 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.268 | 0.328 | 0.732 | 0.029 | 0.573 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.410 | 0.335 | 0.590 | 0.253 | 0.545 |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature | 0.590 | 0.446 | 0.410 | 0.008 | 0.373 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.893 | 0.208 | 0.107 | 0.576 | 0.406 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.703 | 0.315 | 0.297 | 0.460 | 0.446 |

## Default-Pass Side Note: Challenge-Voucher Deltas

Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.592 | -0.260 | 0.020 | -0.065 | -0.297 | -0.136 | 0.500 |
| Low Polarization | -10.825 | -0.180 | 0.027 | -0.138 | -0.137 | -0.065 | 0.500 |
| High Polarization | -16.875 | -0.281 | 0.011 | -0.039 | -0.358 | -0.164 | 0.500 |
| Low Party Loyalty | -15.167 | -0.253 | 0.030 | -0.094 | -0.298 | -0.138 | 0.500 |
| High Party Loyalty | -15.742 | -0.262 | 0.025 | -0.079 | -0.306 | -0.149 | 0.500 |
| Low Compromise Culture | -16.117 | -0.269 | 0.021 | -0.052 | -0.309 | -0.144 | 0.500 |
| High Compromise Culture | -15.008 | -0.250 | 0.025 | -0.082 | -0.288 | -0.138 | 0.500 |
| Low Lobbying Pressure | -15.408 | -0.257 | 0.024 | -0.087 | -0.296 | -0.139 | 0.500 |
| High Lobbying Pressure | -15.325 | -0.255 | 0.019 | -0.053 | -0.295 | -0.137 | 0.500 |
| Weak Constituency Pressure | -18.117 | -0.302 | 0.023 | -0.063 | -0.327 | -0.145 | 0.499 |
| Two-Party System | -6.408 | -0.107 | -0.008 | -0.010 | -0.141 | -0.076 | 0.333 |
| Multi-Party System | -29.942 | -0.499 | 0.113 | -0.316 | -0.523 | -0.323 | 0.801 |
| High Proposal Pressure | 2.858 | 0.016 | -0.016 | 0.016 | -0.031 | -0.054 | 0.167 |
| Extreme Proposal Pressure | 22.533 | 0.075 | -0.022 | 0.024 | 0.023 | -0.048 | 0.100 |
| Lobby-Fueled Flooding | 3.183 | 0.018 | -0.016 | 0.013 | -0.030 | -0.054 | 0.167 |
| Low-Compromise Flooding | 2.725 | 0.015 | -0.018 | 0.020 | -0.046 | -0.073 | 0.167 |
| Capture Crisis | 2.492 | 0.014 | -0.014 | 0.015 | -0.041 | -0.065 | 0.167 |
| Popular Anti-Lobbying Push | -2.408 | -0.020 | -0.013 | -0.008 | -0.056 | -0.054 | 0.250 |
| Weighted Two-Party Baseline | -6.325 | -0.105 | -0.005 | -0.027 | -0.147 | -0.082 | 0.333 |
| Weighted Two Major Plus Minors | -30.767 | -0.513 | 0.111 | -0.285 | -0.543 | -0.339 | 0.800 |
| Weighted Fragmented Multiparty | -29.083 | -0.485 | 0.114 | -0.368 | -0.480 | -0.296 | 0.854 |
| Weighted Dominant-Party Legislature | -20.292 | -0.338 | 0.039 | -0.155 | -0.345 | -0.170 | 0.667 |
| Era 1 Low Contention | -16.208 | -0.270 | 0.052 | -0.221 | -0.233 | -0.117 | 0.660 |
| Era 2 Normal Contention | -22.633 | -0.377 | 0.084 | -0.283 | -0.367 | -0.215 | 0.727 |
| Era 3 Polarizing | -28.608 | -0.477 | 0.105 | -0.290 | -0.498 | -0.321 | 0.779 |
| Era 4 High Contention | -13.258 | -0.177 | -0.000 | -0.026 | -0.217 | -0.102 | 0.400 |
| Era 5 Capture Contention | -2.875 | -0.032 | -0.014 | 0.026 | -0.098 | -0.087 | 0.222 |
| Era 6 Crisis | 1.492 | 0.012 | -0.016 | 0.028 | -0.062 | -0.087 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.192 | -0.553 | -0.002 | 0.001 | -0.594 | -0.189 | 0.664 |
| Adversarial Popular Harmful Bill | -6.758 | -0.113 | -0.000 | -0.091 | -0.098 | -0.053 | 0.463 |
| Adversarial Moderate Capture | -1.142 | -0.019 | 0.000 | -0.020 | -0.010 | -0.002 | 0.329 |
| Adversarial Delayed-Benefit Reform | -27.158 | -0.453 | 0.002 | -0.104 | -0.439 | -0.223 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.350 | -0.389 | 0.030 | -0.235 | -0.321 | -0.171 | 0.653 |
| Adversarial Anti-Lobbying Backlash | -22.533 | -0.376 | 0.044 | -0.164 | -0.255 | -0.153 | 0.650 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest weak public-mandate passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.763) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.739) | Default pass unless 2/3 block (0.839) | Unicameral majority + pairwise alternatives (0.001) |
| High Polarization | Cloture, conference, and judicial review (0.743) | Default pass unless 2/3 block (0.835) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.759) | Default pass unless 2/3 block (0.844) | Unicameral majority + pairwise alternatives (0.003) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.755) | Default pass unless 2/3 block (0.844) | Unicameral majority + pairwise alternatives (0.002) |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark (0.767) | Default pass unless 2/3 block (0.830) | Stylized U.S.-like conventional benchmark (0.000) |
| High Compromise Culture | Stylized U.S.-like conventional benchmark (0.744) | Default pass unless 2/3 block (0.853) | Unicameral majority + pairwise alternatives (0.002) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Default pass unless 2/3 block (0.847) | Unicameral majority + pairwise alternatives (0.003) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.753) | Default pass unless 2/3 block (0.834) | Unicameral majority + pairwise alternatives (0.004) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.874) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.841) | Parliamentary coalition confidence (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.840) | Unicameral majority + pairwise alternatives (0.004) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.756) | Default pass + multi-round mediation + challenge (0.901) | Unicameral majority + pairwise alternatives (0.001) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.746) | Default pass + multi-round mediation + challenge (0.941) | Unicameral majority + pairwise alternatives (0.000) |
| Lobby-Fueled Flooding | Parliamentary coalition confidence (0.734) | Default pass + multi-round mediation + challenge (0.897) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark (0.747) | Default pass + multi-round mediation + challenge (0.884) | Unicameral majority + pairwise alternatives (0.001) |
| Capture Crisis | Parliamentary coalition confidence (0.746) | Default pass + multi-round mediation + challenge (0.890) | Unicameral majority + pairwise alternatives (0.001) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.762) | Default pass + multi-round mediation + challenge (0.866) | Unicameral majority + pairwise alternatives (0.001) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.839) | Parliamentary coalition confidence (0.000) |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark (0.748) | Default pass unless 2/3 block (0.845) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Cloture, conference, and judicial review (0.749) | Default pass unless 2/3 block (0.840) | Unicameral majority + pairwise alternatives (0.003) |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark (0.745) | Default pass unless 2/3 block (0.806) | Unicameral majority + pairwise alternatives (0.003) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.730) | Default pass unless 2/3 block (0.846) | Unicameral majority + pairwise alternatives (0.002) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.753) | Default pass unless 2/3 block (0.839) | Unicameral majority + pairwise alternatives (0.003) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.841) | Unicameral majority + pairwise alternatives (0.002) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.769) | Default pass unless 2/3 block (0.834) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark (0.744) | Default pass + multi-round mediation + challenge (0.866) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark (0.761) | Default pass + multi-round mediation + challenge (0.892) | Parliamentary coalition confidence (0.000) |
| Adversarial High-Benefit Extreme Reform | Portfolio hybrid legislature (0.834) | Default pass unless 2/3 block (0.907) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Portfolio hybrid legislature (0.341) | Default pass unless 2/3 block (1.000) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Moderate Capture | Portfolio hybrid legislature (0.413) | Default pass unless 2/3 block (1.000) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Delayed-Benefit Reform | Portfolio hybrid legislature (0.819) | Default pass unless 2/3 block (0.861) | Unicameral majority + pairwise alternatives (0.005) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.625) | Default pass unless 2/3 block (0.977) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Portfolio hybrid legislature (0.730) | Default pass unless 2/3 block (0.893) | Unicameral majority + pairwise alternatives (0.004) |

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
