# Simulation Campaign v21 Paper

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 28
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

- The canonical paper campaign is breadth-first: 28 scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.
- Highest directional score, where lower-better risk metrics are inverted before combination, came from Unicameral majority + pairwise alternatives at 0.707.
- Best average welfare came from Stylized U.S.-like conventional benchmark at 0.716; highest compromise came from Unicameral majority + pairwise alternatives at 0.504.
- Highest productivity came from Default pass unless 2/3 block at 0.860.
- Open default-pass averaged 0.860 productivity, 0.422 low-support passage, and 0.628 policy shift, so it functions as a throughput/risk endpoint.
- The stylized U.S.-like conventional benchmark averaged 0.051 productivity and 0.716 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, and risk control. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts low-support passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.544 | 0.572 | 0.887 | 0.171 | 14.026 | 41.032 | 0.636 | 0.000 | 0.111 | 0.550 | 0.061 | 0.292 | 0.233 | 0.000 | 0.000 | 0.000 | 0.000 | 0.395 | 0.000 | 0.465 |
| Majority + anti-capture bundle | 0.593 | 0.580 | 0.891 | 0.309 | 25.704 | 82.910 | 0.656 | 0.000 | 0.111 | 0.553 | 0.117 | 0.304 | 0.133 | 0.100 | 0.551 | 0.000 | 0.000 | 0.745 | 0.000 | 0.934 |
| Bicameral simple majority | 0.564 | 0.588 | 0.884 | 0.219 | 17.106 | 88.548 | 0.637 | 0.000 | 0.111 | 0.564 | 0.063 | 0.225 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.459 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.572 | 0.612 | 0.903 | 0.199 | 16.460 | 88.548 | 0.693 | 0.000 | 0.087 | 0.629 | 0.063 | 0.248 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.582 | 0.000 | 1.000 |
| Citizen initiative and referendum | 0.617 | 0.582 | 0.846 | 0.422 | 35.662 | 88.548 | 0.597 | 0.000 | 0.128 | 0.539 | 0.202 | 0.407 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.857 | 0.000 | 1.000 |
| Cloture, conference, and judicial review | 0.535 | 0.630 | 0.924 | 0.050 | 3.918 | 23.055 | 0.696 | 0.000 | 0.084 | 0.624 | 0.010 | 0.146 | 0.199 | 0.000 | 0.000 | 0.068 | 0.000 | 0.167 | 0.000 | 0.270 |
| Committee-first regular order | 0.563 | 0.594 | 0.892 | 0.203 | 15.950 | 20.820 | 0.652 | 0.000 | 0.110 | 0.556 | 0.055 | 0.210 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.453 | 0.000 | 0.258 |
| Compensation amendments + majority | 0.574 | 0.565 | 0.844 | 0.313 | 25.237 | 88.548 | 0.608 | 0.000 | 0.088 | 0.543 | 0.112 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.170 | 0.628 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.543 | 0.654 | 0.923 | 0.051 | 3.996 | 17.968 | 0.716 | 0.000 | 0.061 | 0.691 | 0.011 | 0.148 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.174 | 0.000 | 0.204 |
| Default pass unless 2/3 block | 0.660 | 0.475 | 0.645 | 0.860 | 75.603 | 88.548 | 0.500 | 0.422 | 0.187 | 0.390 | 0.628 | 0.609 | 0.276 | 0.000 | 0.000 | 0.000 | 0.000 | 0.988 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.619 | 0.490 | 0.722 | 0.645 | 63.372 | 88.548 | 0.520 | 0.338 | 0.176 | 0.409 | 0.391 | 0.478 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.852 | 0.458 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.681 | 0.508 | 0.741 | 0.795 | 73.397 | 88.548 | 0.462 | 0.257 | 0.115 | 0.448 | 0.279 | 0.317 | 0.286 | 0.000 | 0.000 | 0.736 | 0.276 | 0.864 | 0.415 | 1.000 |
| Harm-weighted double majority | 0.577 | 0.571 | 0.889 | 0.271 | 22.277 | 88.548 | 0.621 | 0.000 | 0.106 | 0.542 | 0.092 | 0.279 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 | 0.592 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.581 | 0.556 | 0.851 | 0.336 | 27.408 | 88.548 | 0.600 | 0.000 | 0.129 | 0.517 | 0.184 | 0.339 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.645 | 0.000 | 1.000 |
| Leadership agenda cartel + majority | 0.555 | 0.588 | 0.910 | 0.165 | 13.685 | 33.658 | 0.662 | 0.000 | 0.090 | 0.584 | 0.051 | 0.234 | 0.150 | 0.000 | 0.000 | 0.000 | 0.000 | 0.589 | 0.000 | 0.385 |
| Endogenous norm erosion + majority | 0.579 | 0.559 | 0.860 | 0.319 | 25.848 | 83.612 | 0.609 | 0.000 | 0.122 | 0.515 | 0.114 | 0.319 | 0.258 | 0.000 | 0.000 | 0.950 | 0.022 | 0.609 | 0.000 | 0.950 |
| Package bargaining + majority | 0.579 | 0.562 | 0.853 | 0.321 | 25.860 | 88.548 | 0.607 | 0.000 | 0.112 | 0.530 | 0.116 | 0.301 | 0.257 | 0.000 | 0.000 | 0.283 | 0.283 | 0.635 | 0.000 | 1.000 |
| Parliamentary coalition confidence | 0.557 | 0.539 | 0.906 | 0.224 | 17.289 | 21.458 | 0.598 | 0.000 | 0.074 | 0.555 | 0.062 | 0.189 | 0.170 | 0.000 | 0.000 | 0.000 | 0.000 | 0.566 | 0.000 | 0.277 |
| Bicameral majority + presidential veto | 0.547 | 0.602 | 0.894 | 0.146 | 11.297 | 88.548 | 0.649 | 0.000 | 0.103 | 0.587 | 0.038 | 0.208 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.000 | 1.000 |
| Proposal bonds + majority | 0.580 | 0.563 | 0.865 | 0.312 | 25.091 | 87.236 | 0.615 | 0.000 | 0.122 | 0.529 | 0.111 | 0.294 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.625 | 0.000 | 0.992 |
| Majority + public-interest screen | 0.568 | 0.571 | 0.882 | 0.251 | 20.877 | 76.064 | 0.634 | 0.000 | 0.112 | 0.545 | 0.093 | 0.290 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.547 | 0.000 | 0.858 |
| Public objection window + majority | 0.571 | 0.590 | 0.897 | 0.227 | 18.234 | 88.548 | 0.651 | 0.000 | 0.093 | 0.580 | 0.063 | 0.218 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.567 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.570 | 0.576 | 0.888 | 0.247 | 19.118 | 49.321 | 0.634 | 0.000 | 0.106 | 0.552 | 0.077 | 0.247 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.562 | 0.000 | 0.603 |
| Risk-routed majority legislature | 0.639 | 0.544 | 0.855 | 0.518 | 42.687 | 88.548 | 0.512 | 0.000 | 0.102 | 0.513 | 0.178 | 0.319 | 0.290 | 0.000 | 0.000 | 0.641 | 0.225 | 0.672 | 0.000 | 1.000 |
| Unicameral simple majority | 0.580 | 0.563 | 0.865 | 0.312 | 25.216 | 88.548 | 0.613 | 0.000 | 0.122 | 0.529 | 0.112 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.629 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.707 | 0.656 | 0.929 | 0.536 | 46.156 | 48.984 | 0.632 | 0.000 | 0.055 | 0.643 | 0.005 | 0.004 | 0.226 | 0.000 | 0.000 | 0.561 | 0.000 | 0.808 | 0.000 | 0.561 |
| Majority ratification + strategic policy tournament | 0.707 | 0.656 | 0.929 | 0.537 | 46.165 | 48.987 | 0.632 | 0.000 | 0.055 | 0.643 | 0.005 | 0.004 | 0.226 | 0.000 | 0.000 | 0.561 | 0.000 | 0.809 | 0.000 | 0.561 |
| Unicameral 60 percent passage | 0.552 | 0.629 | 0.900 | 0.128 | 9.545 | 88.548 | 0.672 | 0.000 | 0.093 | 0.622 | 0.027 | 0.153 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.270 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`, so it rises when a system blocks more, compromises less, or passes more weak-support bills.

| Era | Scenario | Productivity | Compromise | Gridlock | Low-support | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.046 | 0.369 | 0.954 | 0.000 | 0.666 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.000 | 0.601 |
| Baseline | Committee-first regular order | 0.154 | 0.274 | 0.846 | 0.000 | 0.640 |
| Baseline | Parliamentary coalition confidence | 0.180 | 0.284 | 0.820 | 0.000 | 0.625 |
| Baseline | Unicameral majority + pairwise alternatives | 0.545 | 0.490 | 0.455 | 0.000 | 0.381 |
| Baseline | Citizen assembly threshold gate | 0.184 | 0.260 | 0.816 | 0.000 | 0.630 |
| Baseline | Risk-routed majority legislature | 0.482 | 0.235 | 0.518 | 0.000 | 0.489 |
| Baseline | Default pass unless 2/3 block | 0.841 | 0.105 | 0.159 | 0.447 | 0.437 |
| Baseline | Default pass + multi-round mediation + challenge | 0.724 | 0.219 | 0.276 | 0.257 | 0.424 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.158 | 0.377 | 0.842 | 0.000 | 0.608 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.000 | 0.457 |
| Low Polarization | Committee-first regular order | 0.388 | 0.309 | 0.612 | 0.000 | 0.513 |
| Low Polarization | Parliamentary coalition confidence | 0.486 | 0.301 | 0.514 | 0.000 | 0.467 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.632 | 0.633 | 0.368 | 0.000 | 0.294 |
| Low Polarization | Citizen assembly threshold gate | 0.408 | 0.300 | 0.593 | 0.000 | 0.506 |
| Low Polarization | Risk-routed majority legislature | 0.675 | 0.275 | 0.325 | 0.000 | 0.380 |
| Low Polarization | Default pass unless 2/3 block | 0.847 | 0.200 | 0.153 | 0.315 | 0.380 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.810 | 0.266 | 0.190 | 0.135 | 0.342 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.020 | 0.371 | 0.980 | 0.000 | 0.679 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.000 | 0.649 |
| High Polarization | Committee-first regular order | 0.094 | 0.269 | 0.906 | 0.000 | 0.672 |
| High Polarization | Parliamentary coalition confidence | 0.096 | 0.297 | 0.904 | 0.000 | 0.663 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.489 | 0.448 | 0.511 | 0.000 | 0.421 |
| High Polarization | Citizen assembly threshold gate | 0.121 | 0.254 | 0.879 | 0.000 | 0.663 |
| High Polarization | Risk-routed majority legislature | 0.366 | 0.228 | 0.634 | 0.000 | 0.549 |
| High Polarization | Default pass unless 2/3 block | 0.838 | 0.081 | 0.162 | 0.485 | 0.453 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.677 | 0.206 | 0.323 | 0.350 | 0.470 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.046 | 0.350 | 0.954 | 0.000 | 0.672 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.000 | 0.594 |
| Low Party Loyalty | Committee-first regular order | 0.166 | 0.264 | 0.834 | 0.000 | 0.638 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.183 | 0.281 | 0.817 | 0.000 | 0.624 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.536 | 0.502 | 0.464 | 0.000 | 0.381 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.202 | 0.244 | 0.798 | 0.000 | 0.626 |
| Low Party Loyalty | Risk-routed majority legislature | 0.505 | 0.232 | 0.495 | 0.000 | 0.478 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.843 | 0.105 | 0.157 | 0.447 | 0.436 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.739 | 0.220 | 0.261 | 0.250 | 0.414 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.953 | 0.000 | 0.663 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.000 | 0.596 |
| High Party Loyalty | Committee-first regular order | 0.163 | 0.283 | 0.837 | 0.000 | 0.633 |
| High Party Loyalty | Parliamentary coalition confidence | 0.196 | 0.288 | 0.804 | 0.000 | 0.616 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.554 | 0.503 | 0.446 | 0.000 | 0.372 |
| High Party Loyalty | Citizen assembly threshold gate | 0.194 | 0.258 | 0.806 | 0.000 | 0.626 |
| High Party Loyalty | Risk-routed majority legislature | 0.476 | 0.238 | 0.524 | 0.000 | 0.491 |
| High Party Loyalty | Default pass unless 2/3 block | 0.843 | 0.110 | 0.157 | 0.452 | 0.436 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.716 | 0.221 | 0.284 | 0.244 | 0.424 |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark | 0.030 | 0.371 | 0.970 | 0.000 | 0.674 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.000 | 0.623 |
| Low Compromise Culture | Committee-first regular order | 0.123 | 0.292 | 0.877 | 0.000 | 0.651 |
| Low Compromise Culture | Parliamentary coalition confidence | 0.148 | 0.299 | 0.853 | 0.000 | 0.637 |
| Low Compromise Culture | Unicameral majority + pairwise alternatives | 0.526 | 0.470 | 0.474 | 0.000 | 0.396 |
| Low Compromise Culture | Citizen assembly threshold gate | 0.160 | 0.266 | 0.840 | 0.000 | 0.640 |
| Low Compromise Culture | Risk-routed majority legislature | 0.383 | 0.237 | 0.617 | 0.000 | 0.537 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.826 | 0.102 | 0.174 | 0.478 | 0.452 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.677 | 0.212 | 0.323 | 0.352 | 0.468 |
| High Compromise Culture | Stylized U.S.-like conventional benchmark | 0.065 | 0.376 | 0.935 | 0.000 | 0.655 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.000 | 0.573 |
| High Compromise Culture | Committee-first regular order | 0.194 | 0.283 | 0.806 | 0.000 | 0.618 |
| High Compromise Culture | Parliamentary coalition confidence | 0.236 | 0.274 | 0.764 | 0.000 | 0.600 |
| High Compromise Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.534 | 0.443 | 0.000 | 0.362 |
| High Compromise Culture | Citizen assembly threshold gate | 0.221 | 0.256 | 0.779 | 0.000 | 0.613 |
| High Compromise Culture | Risk-routed majority legislature | 0.579 | 0.233 | 0.421 | 0.000 | 0.440 |
| High Compromise Culture | Default pass unless 2/3 block | 0.856 | 0.109 | 0.144 | 0.421 | 0.424 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.764 | 0.225 | 0.236 | 0.176 | 0.386 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.388 | 0.943 | 0.000 | 0.655 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.000 | 0.597 |
| Low Lobbying Pressure | Committee-first regular order | 0.162 | 0.296 | 0.838 | 0.000 | 0.630 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.203 | 0.280 | 0.797 | 0.000 | 0.615 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.570 | 0.515 | 0.430 | 0.000 | 0.360 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.199 | 0.251 | 0.801 | 0.000 | 0.625 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.477 | 0.222 | 0.523 | 0.000 | 0.495 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.847 | 0.103 | 0.153 | 0.441 | 0.434 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.708 | 0.208 | 0.293 | 0.260 | 0.436 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.026 | 0.367 | 0.974 | 0.000 | 0.677 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.000 | 0.613 |
| High Lobbying Pressure | Committee-first regular order | 0.137 | 0.266 | 0.863 | 0.000 | 0.652 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.135 | 0.307 | 0.865 | 0.000 | 0.640 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.490 | 0.476 | 0.510 | 0.000 | 0.412 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.158 | 0.276 | 0.842 | 0.000 | 0.638 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.398 | 0.253 | 0.602 | 0.000 | 0.525 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.832 | 0.106 | 0.168 | 0.477 | 0.447 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.712 | 0.228 | 0.288 | 0.305 | 0.436 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.372 | 0.973 | 0.000 | 0.675 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.000 | 0.612 |
| Weak Constituency Pressure | Committee-first regular order | 0.129 | 0.282 | 0.871 | 0.000 | 0.651 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.121 | 0.331 | 0.879 | 0.000 | 0.640 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.524 | 0.468 | 0.476 | 0.000 | 0.398 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.161 | 0.268 | 0.839 | 0.000 | 0.639 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.462 | 0.246 | 0.538 | 0.000 | 0.495 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.873 | 0.102 | 0.127 | 0.454 | 0.424 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.734 | 0.225 | 0.266 | 0.256 | 0.417 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.382 | 0.952 | 0.000 | 0.661 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.000 | 0.596 |
| Two-Party System | Committee-first regular order | 0.157 | 0.286 | 0.843 | 0.000 | 0.636 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.544 | 0.485 | 0.456 | 0.000 | 0.383 |
| Two-Party System | Citizen assembly threshold gate | 0.188 | 0.258 | 0.812 | 0.000 | 0.628 |
| Two-Party System | Risk-routed majority legislature | 0.474 | 0.238 | 0.526 | 0.000 | 0.492 |
| Two-Party System | Default pass unless 2/3 block | 0.842 | 0.108 | 0.158 | 0.445 | 0.436 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.829 | 0.205 | 0.171 | 0.325 | 0.389 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.050 | 0.356 | 0.950 | 0.000 | 0.668 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.000 | 0.589 |
| Multi-Party System | Committee-first regular order | 0.175 | 0.275 | 0.825 | 0.000 | 0.630 |
| Multi-Party System | Parliamentary coalition confidence | 0.268 | 0.252 | 0.732 | 0.000 | 0.590 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.541 | 0.511 | 0.459 | 0.000 | 0.376 |
| Multi-Party System | Citizen assembly threshold gate | 0.202 | 0.255 | 0.798 | 0.000 | 0.622 |
| Multi-Party System | Risk-routed majority legislature | 0.500 | 0.241 | 0.500 | 0.000 | 0.477 |
| Multi-Party System | Default pass unless 2/3 block | 0.837 | 0.109 | 0.163 | 0.442 | 0.437 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.644 | 0.232 | 0.356 | 0.145 | 0.437 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.048 | 0.381 | 0.952 | 0.000 | 0.662 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.000 | 0.597 |
| High Proposal Pressure | Committee-first regular order | 0.159 | 0.283 | 0.841 | 0.000 | 0.635 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.186 | 0.293 | 0.814 | 0.000 | 0.619 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.495 | 0.460 | 0.000 | 0.381 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.189 | 0.263 | 0.811 | 0.000 | 0.627 |
| High Proposal Pressure | Risk-routed majority legislature | 0.480 | 0.240 | 0.520 | 0.000 | 0.488 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.844 | 0.107 | 0.156 | 0.449 | 0.436 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.903 | 0.204 | 0.097 | 0.357 | 0.359 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.372 | 0.952 | 0.000 | 0.664 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.000 | 0.597 |
| Extreme Proposal Pressure | Committee-first regular order | 0.160 | 0.283 | 0.840 | 0.000 | 0.635 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.289 | 0.815 | 0.000 | 0.621 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.382 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.191 | 0.261 | 0.810 | 0.000 | 0.627 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.478 | 0.237 | 0.523 | 0.000 | 0.490 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.843 | 0.105 | 0.157 | 0.448 | 0.437 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.940 | 0.198 | 0.060 | 0.383 | 0.347 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.021 | 0.366 | 0.979 | 0.000 | 0.680 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.000 | 0.618 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.126 | 0.273 | 0.874 | 0.000 | 0.655 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.114 | 0.319 | 0.886 | 0.000 | 0.647 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.460 | 0.455 | 0.540 | 0.000 | 0.433 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.145 | 0.276 | 0.855 | 0.000 | 0.645 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.373 | 0.259 | 0.627 | 0.000 | 0.536 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.842 | 0.107 | 0.158 | 0.475 | 0.442 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.896 | 0.207 | 0.104 | 0.417 | 0.373 |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark | 0.018 | 0.407 | 0.982 | 0.000 | 0.669 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.000 | 0.643 |
| Low-Compromise Flooding | Committee-first regular order | 0.094 | 0.286 | 0.906 | 0.000 | 0.667 |
| Low-Compromise Flooding | Parliamentary coalition confidence | 0.100 | 0.314 | 0.900 | 0.000 | 0.656 |
| Low-Compromise Flooding | Unicameral majority + pairwise alternatives | 0.495 | 0.461 | 0.505 | 0.000 | 0.414 |
| Low-Compromise Flooding | Citizen assembly threshold gate | 0.122 | 0.272 | 0.878 | 0.000 | 0.657 |
| Low-Compromise Flooding | Risk-routed majority legislature | 0.340 | 0.234 | 0.660 | 0.000 | 0.559 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.836 | 0.092 | 0.164 | 0.486 | 0.452 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.883 | 0.189 | 0.117 | 0.469 | 0.396 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.012 | 0.365 | 0.988 | 0.000 | 0.685 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.000 | 0.641 |
| Capture Crisis | Committee-first regular order | 0.099 | 0.257 | 0.901 | 0.000 | 0.674 |
| Capture Crisis | Parliamentary coalition confidence | 0.069 | 0.333 | 0.931 | 0.000 | 0.666 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.405 | 0.455 | 0.595 | 0.000 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.113 | 0.273 | 0.887 | 0.000 | 0.662 |
| Capture Crisis | Risk-routed majority legislature | 0.329 | 0.256 | 0.671 | 0.000 | 0.559 |
| Capture Crisis | Default pass unless 2/3 block | 0.841 | 0.099 | 0.159 | 0.484 | 0.447 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.888 | 0.206 | 0.112 | 0.445 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.070 | 0.380 | 0.930 | 0.000 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.000 | 0.554 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.224 | 0.283 | 0.776 | 0.000 | 0.603 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.271 | 0.285 | 0.729 | 0.000 | 0.579 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.545 | 0.543 | 0.455 | 0.000 | 0.365 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.257 | 0.274 | 0.743 | 0.000 | 0.589 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.507 | 0.267 | 0.493 | 0.000 | 0.467 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.826 | 0.128 | 0.174 | 0.429 | 0.434 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.866 | 0.230 | 0.134 | 0.296 | 0.357 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.000 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.000 | 0.596 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.161 | 0.291 | 0.839 | 0.000 | 0.632 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.541 | 0.507 | 0.459 | 0.000 | 0.378 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.191 | 0.268 | 0.809 | 0.000 | 0.624 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.470 | 0.237 | 0.530 | 0.000 | 0.494 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.838 | 0.108 | 0.162 | 0.459 | 0.440 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.822 | 0.205 | 0.178 | 0.331 | 0.394 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.384 | 0.950 | 0.000 | 0.660 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.000 | 0.598 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.159 | 0.279 | 0.841 | 0.000 | 0.636 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.254 | 0.258 | 0.746 | 0.000 | 0.596 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.545 | 0.509 | 0.455 | 0.000 | 0.375 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.184 | 0.263 | 0.816 | 0.000 | 0.629 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.487 | 0.236 | 0.513 | 0.000 | 0.486 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.847 | 0.107 | 0.153 | 0.447 | 0.434 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.643 | 0.228 | 0.357 | 0.163 | 0.443 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.067 | 0.360 | 0.933 | 0.000 | 0.658 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.000 | 0.570 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.205 | 0.287 | 0.795 | 0.000 | 0.612 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.342 | 0.246 | 0.658 | 0.000 | 0.555 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.551 | 0.531 | 0.449 | 0.000 | 0.365 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.228 | 0.268 | 0.773 | 0.000 | 0.606 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.533 | 0.244 | 0.467 | 0.000 | 0.460 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.838 | 0.122 | 0.162 | 0.431 | 0.430 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.638 | 0.243 | 0.362 | 0.091 | 0.427 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.046 | 0.378 | 0.954 | 0.000 | 0.664 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.000 | 0.592 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.170 | 0.284 | 0.830 | 0.000 | 0.630 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.198 | 0.287 | 0.802 | 0.000 | 0.615 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.550 | 0.524 | 0.450 | 0.000 | 0.368 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.199 | 0.269 | 0.801 | 0.000 | 0.620 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.475 | 0.239 | 0.525 | 0.000 | 0.491 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.809 | 0.117 | 0.191 | 0.448 | 0.450 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.653 | 0.228 | 0.348 | 0.198 | 0.445 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.164 | 0.377 | 0.836 | 0.000 | 0.605 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.000 | 0.466 |
| Era 1 Low Contention | Committee-first regular order | 0.369 | 0.298 | 0.631 | 0.000 | 0.526 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.510 | 0.275 | 0.490 | 0.000 | 0.462 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.639 | 0.375 | 0.000 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.390 | 0.286 | 0.610 | 0.000 | 0.519 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.715 | 0.255 | 0.285 | 0.000 | 0.366 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.849 | 0.179 | 0.151 | 0.321 | 0.386 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.778 | 0.253 | 0.222 | 0.072 | 0.350 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.105 | 0.387 | 0.895 | 0.000 | 0.631 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.000 | 0.520 |
| Era 2 Normal Contention | Committee-first regular order | 0.285 | 0.293 | 0.715 | 0.000 | 0.569 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.419 | 0.263 | 0.581 | 0.000 | 0.512 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.569 | 0.413 | 0.000 | 0.336 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.303 | 0.282 | 0.697 | 0.000 | 0.564 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.624 | 0.253 | 0.376 | 0.000 | 0.412 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.843 | 0.149 | 0.157 | 0.387 | 0.411 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.733 | 0.246 | 0.267 | 0.117 | 0.383 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.059 | 0.378 | 0.941 | 0.000 | 0.657 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.000 | 0.575 |
| Era 3 Polarizing | Committee-first regular order | 0.198 | 0.280 | 0.802 | 0.000 | 0.617 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.298 | 0.257 | 0.702 | 0.000 | 0.574 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.554 | 0.510 | 0.446 | 0.000 | 0.370 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.224 | 0.264 | 0.776 | 0.000 | 0.609 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.508 | 0.245 | 0.492 | 0.000 | 0.473 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.838 | 0.119 | 0.162 | 0.433 | 0.432 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.667 | 0.238 | 0.333 | 0.160 | 0.427 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.029 | 0.371 | 0.971 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.000 | 0.620 |
| Era 4 High Contention | Committee-first regular order | 0.125 | 0.280 | 0.875 | 0.000 | 0.653 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.123 | 0.308 | 0.877 | 0.000 | 0.646 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.516 | 0.475 | 0.484 | 0.000 | 0.400 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.151 | 0.262 | 0.849 | 0.000 | 0.646 |
| Era 4 High Contention | Risk-routed majority legislature | 0.400 | 0.248 | 0.600 | 0.000 | 0.526 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.836 | 0.100 | 0.164 | 0.477 | 0.448 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.767 | 0.211 | 0.233 | 0.333 | 0.420 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.345 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.000 | 0.656 |
| Era 5 Capture Contention | Committee-first regular order | 0.087 | 0.256 | 0.913 | 0.000 | 0.680 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.441 | 0.428 | 0.559 | 0.000 | 0.451 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.104 | 0.264 | 0.896 | 0.000 | 0.669 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.327 | 0.240 | 0.673 | 0.000 | 0.564 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.832 | 0.087 | 0.168 | 0.477 | 0.453 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.864 | 0.194 | 0.136 | 0.439 | 0.397 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.009 | 0.363 | 0.991 | 0.000 | 0.686 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.000 | 0.673 |
| Era 6 Crisis | Committee-first regular order | 0.064 | 0.255 | 0.936 | 0.000 | 0.691 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.359 | 0.412 | 0.641 | 0.000 | 0.497 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.076 | 0.261 | 0.924 | 0.000 | 0.683 |
| Era 6 Crisis | Risk-routed majority legislature | 0.266 | 0.237 | 0.734 | 0.000 | 0.596 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.843 | 0.082 | 0.157 | 0.497 | 0.453 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.894 | 0.188 | 0.106 | 0.492 | 0.395 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.000 | 0.742 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.016 | 0.129 | 0.984 | 0.000 | 0.753 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.036 | 0.125 | 0.964 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.639 | 0.499 | 0.361 | 0.000 | 0.331 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.090 | 0.104 | 0.910 | 0.000 | 0.724 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.619 | 0.187 | 0.381 | 0.000 | 0.435 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.910 | 0.046 | 0.090 | 0.484 | 0.428 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.766 | 0.182 | 0.234 | 0.162 | 0.395 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.174 | 0.412 | 0.826 | 0.000 | 0.590 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.000 | 0.278 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.624 | 0.319 | 0.376 | 0.000 | 0.392 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.422 | 0.408 | 0.578 | 0.000 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.207 | 0.418 | 0.793 | 0.000 | 0.571 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.982 | 0.361 | 0.018 | 0.000 | 0.201 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 1.000 | 0.262 | 0.000 | 0.112 | 0.244 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.991 | 0.359 | 0.009 | 0.004 | 0.198 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.045 | 0.572 | 0.955 | 0.000 | 0.606 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.000 | 0.168 |
| Adversarial Moderate Capture | Committee-first regular order | 0.834 | 0.498 | 0.166 | 0.000 | 0.234 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.849 | 0.532 | 0.151 | 0.000 | 0.216 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.568 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.415 | 0.536 | 0.585 | 0.000 | 0.432 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.987 | 0.525 | 0.013 | 0.000 | 0.149 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.033 | 0.161 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.994 | 0.524 | 0.006 | 0.009 | 0.148 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.002 | 0.352 | 0.998 | 0.000 | 0.693 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.000 | 0.634 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.139 | 0.287 | 0.861 | 0.000 | 0.644 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.209 | 0.276 | 0.791 | 0.000 | 0.613 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.490 | 0.476 | 0.510 | 0.000 | 0.412 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.268 | 0.236 | 0.732 | 0.000 | 0.595 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.687 | 0.268 | 0.313 | 0.000 | 0.376 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.858 | 0.114 | 0.142 | 0.494 | 0.436 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.840 | 0.261 | 0.160 | 0.161 | 0.334 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.042 | 0.386 | 0.958 | 0.000 | 0.663 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.000 | 0.471 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.264 | 0.307 | 0.736 | 0.000 | 0.576 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.386 | 0.304 | 0.614 | 0.000 | 0.516 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.475 | 0.519 | 0.525 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.072 | 0.378 | 0.928 | 0.000 | 0.651 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.766 | 0.287 | 0.234 | 0.000 | 0.331 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.979 | 0.174 | 0.021 | 0.338 | 0.326 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.843 | 0.286 | 0.157 | 0.066 | 0.306 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.040 | 0.363 | 0.960 | 0.000 | 0.671 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.000 | 0.555 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.197 | 0.303 | 0.803 | 0.000 | 0.611 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.326 | 0.319 | 0.674 | 0.000 | 0.541 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.417 | 0.498 | 0.583 | 0.000 | 0.442 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.272 | 0.330 | 0.728 | 0.000 | 0.565 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.410 | 0.335 | 0.590 | 0.000 | 0.494 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.892 | 0.208 | 0.108 | 0.509 | 0.394 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.705 | 0.317 | 0.295 | 0.340 | 0.421 |

## Default-Pass Side Note: Challenge-Voucher Deltas

Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.508 | -0.258 | 0.023 | -0.073 | -0.300 | -0.143 | 0.500 |
| Low Polarization | -11.233 | -0.187 | 0.029 | -0.137 | -0.141 | -0.064 | 0.500 |
| High Polarization | -17.142 | -0.286 | 0.010 | -0.030 | -0.355 | -0.155 | 0.500 |
| Low Party Loyalty | -15.258 | -0.254 | 0.029 | -0.089 | -0.300 | -0.139 | 0.500 |
| High Party Loyalty | -15.650 | -0.261 | 0.022 | -0.075 | -0.305 | -0.144 | 0.500 |
| Low Compromise Culture | -15.733 | -0.262 | 0.018 | -0.053 | -0.302 | -0.140 | 0.500 |
| High Compromise Culture | -14.900 | -0.248 | 0.026 | -0.094 | -0.284 | -0.134 | 0.500 |
| Low Lobbying Pressure | -16.042 | -0.267 | 0.023 | -0.075 | -0.304 | -0.142 | 0.500 |
| High Lobbying Pressure | -15.142 | -0.252 | 0.019 | -0.073 | -0.293 | -0.141 | 0.500 |
| Weak Constituency Pressure | -18.150 | -0.303 | 0.023 | -0.067 | -0.329 | -0.146 | 0.499 |
| Two-Party System | -6.367 | -0.106 | -0.007 | -0.017 | -0.147 | -0.085 | 0.333 |
| Multi-Party System | -29.750 | -0.496 | 0.112 | -0.296 | -0.520 | -0.319 | 0.802 |
| High Proposal Pressure | 3.133 | 0.017 | -0.017 | 0.008 | -0.028 | -0.053 | 0.167 |
| Extreme Proposal Pressure | 22.075 | 0.074 | -0.022 | 0.018 | 0.022 | -0.047 | 0.100 |
| Lobby-Fueled Flooding | 2.833 | 0.016 | -0.015 | 0.011 | -0.031 | -0.055 | 0.167 |
| Low-Compromise Flooding | 2.608 | 0.014 | -0.017 | 0.018 | -0.048 | -0.074 | 0.167 |
| Capture Crisis | 2.258 | 0.013 | -0.014 | 0.016 | -0.043 | -0.066 | 0.167 |
| Popular Anti-Lobbying Push | -2.208 | -0.018 | -0.013 | -0.012 | -0.056 | -0.057 | 0.250 |
| Weighted Two-Party Baseline | -6.375 | -0.106 | -0.005 | -0.027 | -0.149 | -0.083 | 0.333 |
| Weighted Two Major Plus Minors | -31.050 | -0.518 | 0.112 | -0.281 | -0.546 | -0.339 | 0.800 |
| Weighted Fragmented Multiparty | -29.367 | -0.489 | 0.115 | -0.363 | -0.483 | -0.298 | 0.853 |
| Weighted Dominant-Party Legislature | -20.117 | -0.335 | 0.042 | -0.155 | -0.343 | -0.169 | 0.667 |
| Era 1 Low Contention | -16.150 | -0.269 | 0.054 | -0.218 | -0.233 | -0.115 | 0.659 |
| Era 2 Normal Contention | -22.792 | -0.380 | 0.086 | -0.291 | -0.374 | -0.221 | 0.723 |
| Era 3 Polarizing | -28.217 | -0.470 | 0.101 | -0.292 | -0.488 | -0.308 | 0.781 |
| Era 4 High Contention | -13.442 | -0.179 | 0.000 | -0.023 | -0.218 | -0.102 | 0.400 |
| Era 5 Capture Contention | -2.558 | -0.028 | -0.015 | 0.023 | -0.096 | -0.088 | 0.222 |
| Era 6 Crisis | 1.150 | 0.010 | -0.016 | 0.027 | -0.062 | -0.083 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.375 | -0.556 | -0.002 | -0.015 | -0.598 | -0.193 | 0.665 |
| Adversarial Popular Harmful Bill | -6.325 | -0.105 | 0.000 | -0.091 | -0.093 | -0.050 | 0.460 |
| Adversarial Moderate Capture | -1.158 | -0.019 | 0.000 | -0.021 | -0.009 | -0.002 | 0.329 |
| Adversarial Delayed-Benefit Reform | -26.808 | -0.447 | 0.003 | -0.101 | -0.434 | -0.221 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.900 | -0.398 | 0.030 | -0.215 | -0.328 | -0.175 | 0.653 |
| Adversarial Anti-Lobbying Backlash | -22.500 | -0.375 | 0.046 | -0.156 | -0.258 | -0.157 | 0.648 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.841) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.847) | Stylized U.S.-like conventional benchmark (0.000) |
| High Polarization | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.774) | Default pass unless 2/3 block (0.843) | Stylized U.S.-like conventional benchmark (0.000) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.771) | Default pass unless 2/3 block (0.843) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Compromise Culture | Cloture, conference, and judicial review (0.766) | Default pass unless 2/3 block (0.826) | Stylized U.S.-like conventional benchmark (0.000) |
| High Compromise Culture | Stylized U.S.-like conventional benchmark (0.750) | Default pass unless 2/3 block (0.856) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.847) | Stylized U.S.-like conventional benchmark (0.000) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.832) | Stylized U.S.-like conventional benchmark (0.000) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.760) | Default pass unless 2/3 block (0.873) | Stylized U.S.-like conventional benchmark (0.000) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.842) | Stylized U.S.-like conventional benchmark (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.756) | Default pass unless 2/3 block (0.837) | Stylized U.S.-like conventional benchmark (0.000) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.757) | Default pass + multi-round mediation + challenge (0.903) | Stylized U.S.-like conventional benchmark (0.000) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.754) | Default pass + multi-round mediation + challenge (0.940) | Stylized U.S.-like conventional benchmark (0.000) |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark (0.757) | Default pass + multi-round mediation + challenge (0.896) | Stylized U.S.-like conventional benchmark (0.000) |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark (0.749) | Default pass + multi-round mediation + challenge (0.883) | Stylized U.S.-like conventional benchmark (0.000) |
| Capture Crisis | Parliamentary coalition confidence (0.746) | Default pass + multi-round mediation + challenge (0.888) | Stylized U.S.-like conventional benchmark (0.000) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.771) | Default pass + multi-round mediation + challenge (0.866) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.847) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark (0.740) | Default pass unless 2/3 block (0.809) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.737) | Default pass unless 2/3 block (0.849) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.843) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.767) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.774) | Default pass unless 2/3 block (0.836) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark (0.744) | Default pass + multi-round mediation + challenge (0.864) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark (0.761) | Default pass + multi-round mediation + challenge (0.894) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial High-Benefit Extreme Reform | Majority ratification + strategic policy tournament (0.815) | Default pass unless 2/3 block (0.910) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives (0.320) | Default pass unless 2/3 block (1.000) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives (0.381) | Default pass unless 2/3 block (1.000) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Delayed-Benefit Reform | Majority ratification + strategic policy tournament (0.801) | Default pass unless 2/3 block (0.858) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.631) | Default pass unless 2/3 block (0.979) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate (0.710) | Default pass unless 2/3 block (0.892) | Stylized U.S.-like conventional benchmark (0.000) |

## Interpretation

- This is a breadth-first paper campaign. Default pass is retained as one burden-shifting stress test, while the main comparison spans conventional thresholds, committee-first regular order, coalition confidence, policy tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation rules, anti-capture safeguards, adaptive risk routing, and law-registry review.
- Open default-pass remains the throughput extreme, but its high low-support passage and policy movement make it a diagnostic endpoint rather than the project focus.
- Policy tournaments and risk-routed majority systems occupy the strongest compromise/productivity middle ground in this synthetic campaign; committee-first, public-interest, citizen, and parliamentary-style gates control risk but give up substantial throughput.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality, and generated welfare remains conditional on model assumptions.
- The next model extension should deepen non-default families beyond their current prototypes: multidimensional package bargaining, judicial/court intervention, executive emergency/delegated rulemaking, direct-democracy routes, electoral feedback, and media/information ecosystems.

## Reproduction

```sh
make campaign
```
