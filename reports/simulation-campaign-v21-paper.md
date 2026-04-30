# Simulation Campaign v21 Paper

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 24
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

- The canonical paper campaign is breadth-first: 24 scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.
- Highest directional score, where lower-better risk metrics are inverted before combination, came from Majority ratification + strategic policy tournament at 0.707.
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
| Weighted agenda lottery + majority | 0.544 | 0.573 | 0.888 | 0.169 | 13.874 | 41.032 | 0.638 | 0.000 | 0.110 | 0.551 | 0.060 | 0.288 | 0.233 | 0.000 | 0.000 | 0.000 | 0.000 | 0.396 | 0.000 | 0.465 |
| Majority + anti-capture bundle | 0.594 | 0.580 | 0.891 | 0.310 | 25.783 | 82.911 | 0.655 | 0.000 | 0.111 | 0.552 | 0.118 | 0.306 | 0.133 | 0.099 | 0.551 | 0.000 | 0.000 | 0.749 | 0.000 | 0.934 |
| Bicameral simple majority | 0.564 | 0.588 | 0.884 | 0.219 | 17.106 | 88.548 | 0.637 | 0.000 | 0.111 | 0.564 | 0.063 | 0.225 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.459 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.572 | 0.612 | 0.903 | 0.199 | 16.392 | 88.548 | 0.694 | 0.000 | 0.086 | 0.630 | 0.062 | 0.249 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.581 | 0.000 | 1.000 |
| Committee-first regular order | 0.563 | 0.594 | 0.891 | 0.204 | 16.006 | 20.842 | 0.653 | 0.000 | 0.110 | 0.556 | 0.055 | 0.211 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.453 | 0.000 | 0.258 |
| Compensation amendments + majority | 0.574 | 0.565 | 0.844 | 0.313 | 25.254 | 88.548 | 0.608 | 0.000 | 0.088 | 0.544 | 0.112 | 0.297 | 0.255 | 0.000 | 0.000 | 0.000 | 0.170 | 0.628 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.543 | 0.654 | 0.923 | 0.051 | 3.996 | 17.968 | 0.716 | 0.000 | 0.061 | 0.691 | 0.011 | 0.148 | 0.191 | 0.000 | 0.000 | 0.000 | 0.000 | 0.174 | 0.000 | 0.204 |
| Default pass unless 2/3 block | 0.660 | 0.475 | 0.645 | 0.860 | 75.614 | 88.548 | 0.500 | 0.422 | 0.187 | 0.390 | 0.628 | 0.609 | 0.276 | 0.000 | 0.000 | 0.000 | 0.000 | 0.988 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.619 | 0.490 | 0.721 | 0.645 | 63.337 | 88.548 | 0.520 | 0.338 | 0.176 | 0.409 | 0.391 | 0.478 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.852 | 0.458 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.681 | 0.509 | 0.738 | 0.795 | 73.416 | 88.548 | 0.463 | 0.256 | 0.115 | 0.449 | 0.279 | 0.317 | 0.286 | 0.000 | 0.000 | 0.736 | 0.276 | 0.864 | 0.415 | 1.000 |
| Harm-weighted double majority | 0.577 | 0.571 | 0.889 | 0.272 | 22.299 | 88.548 | 0.621 | 0.000 | 0.106 | 0.542 | 0.092 | 0.276 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 | 0.592 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.581 | 0.556 | 0.851 | 0.336 | 27.448 | 88.548 | 0.601 | 0.000 | 0.130 | 0.516 | 0.184 | 0.339 | 0.256 | 0.000 | 0.000 | 0.000 | 0.000 | 0.649 | 0.000 | 1.000 |
| Package bargaining + majority | 0.579 | 0.562 | 0.853 | 0.321 | 25.900 | 88.548 | 0.607 | 0.000 | 0.112 | 0.530 | 0.116 | 0.300 | 0.257 | 0.000 | 0.000 | 0.283 | 0.283 | 0.632 | 0.000 | 1.000 |
| Parliamentary coalition confidence | 0.557 | 0.540 | 0.906 | 0.225 | 17.328 | 21.437 | 0.598 | 0.000 | 0.073 | 0.554 | 0.062 | 0.189 | 0.170 | 0.000 | 0.000 | 0.000 | 0.000 | 0.570 | 0.000 | 0.276 |
| Bicameral majority + presidential veto | 0.547 | 0.602 | 0.894 | 0.146 | 11.297 | 88.548 | 0.649 | 0.000 | 0.103 | 0.587 | 0.038 | 0.208 | 0.260 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.000 | 1.000 |
| Proposal bonds + majority | 0.580 | 0.563 | 0.865 | 0.312 | 25.071 | 87.238 | 0.615 | 0.000 | 0.122 | 0.529 | 0.111 | 0.294 | 0.253 | 0.000 | 0.000 | 0.000 | 0.000 | 0.628 | 0.000 | 0.992 |
| Majority + public-interest screen | 0.568 | 0.570 | 0.882 | 0.251 | 20.869 | 76.064 | 0.633 | 0.000 | 0.112 | 0.544 | 0.093 | 0.291 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.542 | 0.000 | 0.858 |
| Public objection window + majority | 0.571 | 0.590 | 0.897 | 0.227 | 18.237 | 88.548 | 0.651 | 0.000 | 0.093 | 0.579 | 0.063 | 0.218 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.565 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.570 | 0.576 | 0.888 | 0.247 | 19.104 | 49.345 | 0.634 | 0.000 | 0.106 | 0.551 | 0.076 | 0.246 | 0.223 | 0.000 | 0.000 | 0.000 | 0.000 | 0.562 | 0.000 | 0.603 |
| Risk-routed majority legislature | 0.639 | 0.544 | 0.854 | 0.518 | 42.723 | 88.548 | 0.512 | 0.000 | 0.102 | 0.512 | 0.178 | 0.319 | 0.290 | 0.000 | 0.000 | 0.641 | 0.225 | 0.669 | 0.000 | 1.000 |
| Unicameral simple majority | 0.580 | 0.563 | 0.865 | 0.312 | 25.216 | 88.548 | 0.613 | 0.000 | 0.122 | 0.529 | 0.112 | 0.296 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.629 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.707 | 0.656 | 0.929 | 0.536 | 46.117 | 48.991 | 0.631 | 0.000 | 0.055 | 0.643 | 0.005 | 0.004 | 0.227 | 0.000 | 0.000 | 0.561 | 0.000 | 0.806 | 0.000 | 0.561 |
| Majority ratification + strategic policy tournament | 0.707 | 0.656 | 0.929 | 0.536 | 46.099 | 48.980 | 0.632 | 0.000 | 0.055 | 0.643 | 0.005 | 0.004 | 0.226 | 0.000 | 0.000 | 0.561 | 0.000 | 0.807 | 0.000 | 0.561 |
| Unicameral 60 percent passage | 0.552 | 0.629 | 0.900 | 0.128 | 9.545 | 88.548 | 0.672 | 0.000 | 0.093 | 0.622 | 0.027 | 0.153 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.270 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`, so it rises when a system blocks more, compromises less, or passes more weak-support bills.

| Era | Scenario | Productivity | Compromise | Gridlock | Low-support | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Stylized U.S.-like conventional benchmark | 0.046 | 0.369 | 0.954 | 0.000 | 0.666 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.000 | 0.601 |
| Baseline | Committee-first regular order | 0.153 | 0.278 | 0.847 | 0.000 | 0.640 |
| Baseline | Parliamentary coalition confidence | 0.182 | 0.284 | 0.818 | 0.000 | 0.623 |
| Baseline | Unicameral majority + pairwise alternatives | 0.547 | 0.490 | 0.453 | 0.000 | 0.380 |
| Baseline | Citizen assembly threshold gate | 0.181 | 0.262 | 0.819 | 0.000 | 0.631 |
| Baseline | Risk-routed majority legislature | 0.481 | 0.236 | 0.519 | 0.000 | 0.488 |
| Baseline | Default pass unless 2/3 block | 0.837 | 0.104 | 0.163 | 0.454 | 0.441 |
| Baseline | Default pass + multi-round mediation + challenge | 0.725 | 0.219 | 0.275 | 0.252 | 0.422 |
| Low Polarization | Stylized U.S.-like conventional benchmark | 0.158 | 0.377 | 0.842 | 0.000 | 0.608 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.000 | 0.457 |
| Low Polarization | Committee-first regular order | 0.388 | 0.308 | 0.612 | 0.000 | 0.514 |
| Low Polarization | Parliamentary coalition confidence | 0.485 | 0.301 | 0.515 | 0.000 | 0.468 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.631 | 0.633 | 0.369 | 0.000 | 0.295 |
| Low Polarization | Citizen assembly threshold gate | 0.406 | 0.298 | 0.594 | 0.000 | 0.508 |
| Low Polarization | Risk-routed majority legislature | 0.675 | 0.275 | 0.325 | 0.000 | 0.380 |
| Low Polarization | Default pass unless 2/3 block | 0.847 | 0.200 | 0.153 | 0.319 | 0.380 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.812 | 0.264 | 0.188 | 0.132 | 0.341 |
| High Polarization | Stylized U.S.-like conventional benchmark | 0.020 | 0.371 | 0.980 | 0.000 | 0.679 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.000 | 0.649 |
| High Polarization | Committee-first regular order | 0.094 | 0.279 | 0.906 | 0.000 | 0.669 |
| High Polarization | Parliamentary coalition confidence | 0.096 | 0.300 | 0.904 | 0.000 | 0.662 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.490 | 0.445 | 0.510 | 0.000 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.117 | 0.258 | 0.883 | 0.000 | 0.664 |
| High Polarization | Risk-routed majority legislature | 0.361 | 0.225 | 0.639 | 0.000 | 0.552 |
| High Polarization | Default pass unless 2/3 block | 0.834 | 0.081 | 0.166 | 0.485 | 0.456 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.682 | 0.206 | 0.318 | 0.354 | 0.468 |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark | 0.046 | 0.350 | 0.954 | 0.000 | 0.672 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.000 | 0.594 |
| Low Party Loyalty | Committee-first regular order | 0.170 | 0.262 | 0.830 | 0.000 | 0.636 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.185 | 0.277 | 0.815 | 0.000 | 0.624 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.536 | 0.504 | 0.464 | 0.000 | 0.381 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.199 | 0.247 | 0.801 | 0.000 | 0.626 |
| Low Party Loyalty | Risk-routed majority legislature | 0.503 | 0.233 | 0.497 | 0.000 | 0.478 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.841 | 0.105 | 0.159 | 0.454 | 0.439 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.746 | 0.219 | 0.254 | 0.244 | 0.410 |
| High Party Loyalty | Stylized U.S.-like conventional benchmark | 0.048 | 0.378 | 0.953 | 0.000 | 0.663 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.000 | 0.596 |
| High Party Loyalty | Committee-first regular order | 0.164 | 0.286 | 0.836 | 0.000 | 0.632 |
| High Party Loyalty | Parliamentary coalition confidence | 0.197 | 0.285 | 0.803 | 0.000 | 0.616 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.553 | 0.503 | 0.447 | 0.000 | 0.372 |
| High Party Loyalty | Citizen assembly threshold gate | 0.192 | 0.263 | 0.808 | 0.000 | 0.625 |
| High Party Loyalty | Risk-routed majority legislature | 0.479 | 0.238 | 0.521 | 0.000 | 0.489 |
| High Party Loyalty | Default pass unless 2/3 block | 0.841 | 0.110 | 0.159 | 0.438 | 0.434 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.714 | 0.221 | 0.286 | 0.247 | 0.426 |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark | 0.030 | 0.371 | 0.970 | 0.000 | 0.674 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.000 | 0.623 |
| Low Compromise Culture | Committee-first regular order | 0.128 | 0.290 | 0.872 | 0.000 | 0.649 |
| Low Compromise Culture | Parliamentary coalition confidence | 0.151 | 0.295 | 0.849 | 0.000 | 0.636 |
| Low Compromise Culture | Unicameral majority + pairwise alternatives | 0.526 | 0.470 | 0.474 | 0.000 | 0.396 |
| Low Compromise Culture | Citizen assembly threshold gate | 0.159 | 0.270 | 0.841 | 0.000 | 0.639 |
| Low Compromise Culture | Risk-routed majority legislature | 0.384 | 0.236 | 0.616 | 0.000 | 0.537 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.831 | 0.102 | 0.169 | 0.482 | 0.450 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.683 | 0.212 | 0.318 | 0.344 | 0.464 |
| High Compromise Culture | Stylized U.S.-like conventional benchmark | 0.065 | 0.376 | 0.935 | 0.000 | 0.655 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.000 | 0.573 |
| High Compromise Culture | Committee-first regular order | 0.194 | 0.285 | 0.806 | 0.000 | 0.618 |
| High Compromise Culture | Parliamentary coalition confidence | 0.233 | 0.275 | 0.767 | 0.000 | 0.601 |
| High Compromise Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.533 | 0.443 | 0.000 | 0.361 |
| High Compromise Culture | Citizen assembly threshold gate | 0.224 | 0.256 | 0.776 | 0.000 | 0.611 |
| High Compromise Culture | Risk-routed majority legislature | 0.581 | 0.232 | 0.419 | 0.000 | 0.440 |
| High Compromise Culture | Default pass unless 2/3 block | 0.852 | 0.110 | 0.148 | 0.421 | 0.425 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.752 | 0.223 | 0.248 | 0.175 | 0.392 |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.057 | 0.388 | 0.943 | 0.000 | 0.655 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.000 | 0.597 |
| Low Lobbying Pressure | Committee-first regular order | 0.171 | 0.283 | 0.829 | 0.000 | 0.630 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.199 | 0.282 | 0.801 | 0.000 | 0.616 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.570 | 0.515 | 0.430 | 0.000 | 0.361 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.193 | 0.258 | 0.807 | 0.000 | 0.626 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.484 | 0.220 | 0.516 | 0.000 | 0.492 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.843 | 0.104 | 0.157 | 0.440 | 0.435 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.709 | 0.206 | 0.291 | 0.258 | 0.435 |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark | 0.026 | 0.367 | 0.974 | 0.000 | 0.677 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.000 | 0.613 |
| High Lobbying Pressure | Committee-first regular order | 0.134 | 0.270 | 0.866 | 0.000 | 0.652 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.136 | 0.310 | 0.864 | 0.000 | 0.639 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.484 | 0.476 | 0.516 | 0.000 | 0.415 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.157 | 0.278 | 0.843 | 0.000 | 0.638 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.397 | 0.253 | 0.603 | 0.000 | 0.526 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.833 | 0.107 | 0.167 | 0.467 | 0.445 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.708 | 0.230 | 0.293 | 0.293 | 0.436 |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark | 0.027 | 0.372 | 0.973 | 0.000 | 0.675 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.000 | 0.612 |
| Weak Constituency Pressure | Committee-first regular order | 0.127 | 0.283 | 0.873 | 0.000 | 0.651 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.123 | 0.327 | 0.877 | 0.000 | 0.640 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.525 | 0.466 | 0.475 | 0.000 | 0.397 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.155 | 0.276 | 0.845 | 0.000 | 0.640 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.464 | 0.244 | 0.536 | 0.000 | 0.495 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.873 | 0.102 | 0.127 | 0.456 | 0.424 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.743 | 0.225 | 0.257 | 0.258 | 0.412 |
| Two-Party System | Stylized U.S.-like conventional benchmark | 0.048 | 0.382 | 0.952 | 0.000 | 0.661 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.000 | 0.596 |
| Two-Party System | Committee-first regular order | 0.160 | 0.276 | 0.840 | 0.000 | 0.637 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.486 | 0.457 | 0.000 | 0.382 |
| Two-Party System | Citizen assembly threshold gate | 0.192 | 0.257 | 0.808 | 0.000 | 0.627 |
| Two-Party System | Risk-routed majority legislature | 0.475 | 0.235 | 0.525 | 0.000 | 0.492 |
| Two-Party System | Default pass unless 2/3 block | 0.846 | 0.107 | 0.154 | 0.451 | 0.435 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.826 | 0.207 | 0.174 | 0.320 | 0.389 |
| Multi-Party System | Stylized U.S.-like conventional benchmark | 0.050 | 0.356 | 0.950 | 0.000 | 0.668 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.000 | 0.589 |
| Multi-Party System | Committee-first regular order | 0.171 | 0.278 | 0.829 | 0.000 | 0.631 |
| Multi-Party System | Parliamentary coalition confidence | 0.265 | 0.253 | 0.735 | 0.000 | 0.592 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.542 | 0.511 | 0.458 | 0.000 | 0.376 |
| Multi-Party System | Citizen assembly threshold gate | 0.200 | 0.264 | 0.800 | 0.000 | 0.621 |
| Multi-Party System | Risk-routed majority legislature | 0.505 | 0.239 | 0.495 | 0.000 | 0.476 |
| Multi-Party System | Default pass unless 2/3 block | 0.836 | 0.109 | 0.164 | 0.444 | 0.438 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.635 | 0.234 | 0.365 | 0.145 | 0.441 |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.048 | 0.381 | 0.952 | 0.000 | 0.662 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.000 | 0.597 |
| High Proposal Pressure | Committee-first regular order | 0.161 | 0.285 | 0.839 | 0.000 | 0.634 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.187 | 0.289 | 0.813 | 0.000 | 0.619 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.496 | 0.460 | 0.000 | 0.381 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.262 | 0.813 | 0.000 | 0.628 |
| High Proposal Pressure | Risk-routed majority legislature | 0.482 | 0.240 | 0.518 | 0.000 | 0.487 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.845 | 0.107 | 0.155 | 0.454 | 0.436 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.901 | 0.203 | 0.099 | 0.358 | 0.360 |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark | 0.049 | 0.372 | 0.952 | 0.000 | 0.664 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.000 | 0.597 |
| Extreme Proposal Pressure | Committee-first regular order | 0.161 | 0.285 | 0.839 | 0.000 | 0.634 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.290 | 0.815 | 0.000 | 0.621 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.382 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.000 | 0.628 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.480 | 0.240 | 0.520 | 0.000 | 0.488 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.844 | 0.105 | 0.156 | 0.447 | 0.436 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.941 | 0.199 | 0.059 | 0.378 | 0.346 |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark | 0.021 | 0.366 | 0.979 | 0.000 | 0.680 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.000 | 0.618 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.127 | 0.270 | 0.873 | 0.000 | 0.655 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.116 | 0.321 | 0.884 | 0.000 | 0.646 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.459 | 0.455 | 0.541 | 0.000 | 0.434 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.146 | 0.277 | 0.854 | 0.000 | 0.644 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.379 | 0.259 | 0.621 | 0.000 | 0.533 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.841 | 0.107 | 0.159 | 0.478 | 0.443 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.896 | 0.207 | 0.104 | 0.419 | 0.373 |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark | 0.018 | 0.407 | 0.982 | 0.000 | 0.669 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.000 | 0.643 |
| Low-Compromise Flooding | Committee-first regular order | 0.091 | 0.288 | 0.909 | 0.000 | 0.668 |
| Low-Compromise Flooding | Parliamentary coalition confidence | 0.100 | 0.313 | 0.900 | 0.000 | 0.656 |
| Low-Compromise Flooding | Unicameral majority + pairwise alternatives | 0.495 | 0.461 | 0.505 | 0.000 | 0.414 |
| Low-Compromise Flooding | Citizen assembly threshold gate | 0.125 | 0.266 | 0.875 | 0.000 | 0.658 |
| Low-Compromise Flooding | Risk-routed majority legislature | 0.339 | 0.233 | 0.661 | 0.000 | 0.561 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.838 | 0.091 | 0.162 | 0.485 | 0.451 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.885 | 0.188 | 0.115 | 0.467 | 0.394 |
| Capture Crisis | Stylized U.S.-like conventional benchmark | 0.012 | 0.365 | 0.988 | 0.000 | 0.685 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.000 | 0.641 |
| Capture Crisis | Committee-first regular order | 0.099 | 0.263 | 0.901 | 0.000 | 0.671 |
| Capture Crisis | Parliamentary coalition confidence | 0.069 | 0.339 | 0.931 | 0.000 | 0.664 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.404 | 0.456 | 0.596 | 0.000 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.113 | 0.267 | 0.887 | 0.000 | 0.663 |
| Capture Crisis | Risk-routed majority legislature | 0.325 | 0.257 | 0.675 | 0.000 | 0.560 |
| Capture Crisis | Default pass unless 2/3 block | 0.840 | 0.099 | 0.160 | 0.487 | 0.448 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.889 | 0.205 | 0.111 | 0.444 | 0.383 |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark | 0.070 | 0.380 | 0.930 | 0.000 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.000 | 0.554 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.219 | 0.285 | 0.781 | 0.000 | 0.605 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.273 | 0.285 | 0.727 | 0.000 | 0.578 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.544 | 0.544 | 0.456 | 0.000 | 0.365 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.255 | 0.272 | 0.745 | 0.000 | 0.591 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.506 | 0.267 | 0.494 | 0.000 | 0.467 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.827 | 0.128 | 0.173 | 0.424 | 0.433 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.865 | 0.230 | 0.135 | 0.299 | 0.358 |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark | 0.048 | 0.374 | 0.952 | 0.000 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.000 | 0.596 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.157 | 0.295 | 0.843 | 0.000 | 0.633 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.541 | 0.507 | 0.459 | 0.000 | 0.377 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.194 | 0.262 | 0.806 | 0.000 | 0.625 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.480 | 0.240 | 0.520 | 0.000 | 0.488 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.833 | 0.108 | 0.167 | 0.449 | 0.441 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.823 | 0.206 | 0.178 | 0.326 | 0.392 |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark | 0.050 | 0.384 | 0.950 | 0.000 | 0.660 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.000 | 0.598 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.164 | 0.286 | 0.836 | 0.000 | 0.632 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.253 | 0.259 | 0.747 | 0.000 | 0.596 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.543 | 0.508 | 0.457 | 0.000 | 0.376 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.000 | 0.628 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.480 | 0.234 | 0.520 | 0.000 | 0.490 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.846 | 0.107 | 0.154 | 0.449 | 0.434 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.648 | 0.228 | 0.353 | 0.160 | 0.440 |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark | 0.067 | 0.360 | 0.933 | 0.000 | 0.658 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.000 | 0.570 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.210 | 0.282 | 0.790 | 0.000 | 0.610 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.344 | 0.244 | 0.656 | 0.000 | 0.555 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.550 | 0.532 | 0.450 | 0.000 | 0.365 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.235 | 0.266 | 0.765 | 0.000 | 0.603 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.529 | 0.244 | 0.471 | 0.000 | 0.462 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.838 | 0.123 | 0.162 | 0.429 | 0.430 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.635 | 0.246 | 0.365 | 0.092 | 0.427 |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark | 0.046 | 0.378 | 0.954 | 0.000 | 0.664 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.000 | 0.592 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.176 | 0.286 | 0.824 | 0.000 | 0.626 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.202 | 0.286 | 0.798 | 0.000 | 0.613 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.552 | 0.523 | 0.448 | 0.000 | 0.367 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.205 | 0.267 | 0.795 | 0.000 | 0.617 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.481 | 0.241 | 0.519 | 0.000 | 0.487 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.808 | 0.116 | 0.192 | 0.451 | 0.451 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.660 | 0.227 | 0.340 | 0.193 | 0.441 |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark | 0.164 | 0.377 | 0.836 | 0.000 | 0.605 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.000 | 0.466 |
| Era 1 Low Contention | Committee-first regular order | 0.370 | 0.300 | 0.630 | 0.000 | 0.525 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.514 | 0.274 | 0.486 | 0.000 | 0.461 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.638 | 0.375 | 0.000 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.383 | 0.288 | 0.617 | 0.000 | 0.522 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.709 | 0.255 | 0.291 | 0.000 | 0.369 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.846 | 0.179 | 0.154 | 0.318 | 0.387 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.782 | 0.253 | 0.218 | 0.067 | 0.346 |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark | 0.105 | 0.387 | 0.895 | 0.000 | 0.631 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.000 | 0.520 |
| Era 2 Normal Contention | Committee-first regular order | 0.284 | 0.291 | 0.716 | 0.000 | 0.571 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.421 | 0.264 | 0.579 | 0.000 | 0.510 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.570 | 0.413 | 0.000 | 0.336 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.304 | 0.280 | 0.696 | 0.000 | 0.564 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.616 | 0.253 | 0.384 | 0.000 | 0.416 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.842 | 0.149 | 0.158 | 0.379 | 0.410 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.736 | 0.246 | 0.264 | 0.114 | 0.381 |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark | 0.059 | 0.378 | 0.941 | 0.000 | 0.657 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.000 | 0.575 |
| Era 3 Polarizing | Committee-first regular order | 0.197 | 0.282 | 0.803 | 0.000 | 0.617 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.296 | 0.260 | 0.704 | 0.000 | 0.574 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.556 | 0.509 | 0.444 | 0.000 | 0.369 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.222 | 0.267 | 0.778 | 0.000 | 0.609 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.513 | 0.247 | 0.487 | 0.000 | 0.470 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.838 | 0.119 | 0.162 | 0.441 | 0.433 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.656 | 0.240 | 0.344 | 0.155 | 0.431 |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark | 0.029 | 0.371 | 0.971 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.000 | 0.620 |
| Era 4 High Contention | Committee-first regular order | 0.125 | 0.279 | 0.875 | 0.000 | 0.654 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.126 | 0.311 | 0.874 | 0.000 | 0.644 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.517 | 0.476 | 0.483 | 0.000 | 0.399 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.153 | 0.268 | 0.847 | 0.000 | 0.643 |
| Era 4 High Contention | Risk-routed majority legislature | 0.405 | 0.245 | 0.595 | 0.000 | 0.524 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.834 | 0.100 | 0.166 | 0.475 | 0.448 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.765 | 0.212 | 0.235 | 0.336 | 0.421 |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark | 0.016 | 0.345 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.000 | 0.656 |
| Era 5 Capture Contention | Committee-first regular order | 0.081 | 0.263 | 0.919 | 0.000 | 0.681 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.438 | 0.428 | 0.562 | 0.000 | 0.453 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.106 | 0.259 | 0.894 | 0.000 | 0.669 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.330 | 0.239 | 0.670 | 0.000 | 0.563 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.837 | 0.086 | 0.163 | 0.483 | 0.452 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.866 | 0.194 | 0.134 | 0.447 | 0.398 |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark | 0.009 | 0.363 | 0.991 | 0.000 | 0.686 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.000 | 0.673 |
| Era 6 Crisis | Committee-first regular order | 0.063 | 0.260 | 0.937 | 0.000 | 0.691 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.358 | 0.412 | 0.643 | 0.000 | 0.498 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.075 | 0.265 | 0.925 | 0.000 | 0.683 |
| Era 6 Crisis | Risk-routed majority legislature | 0.267 | 0.238 | 0.733 | 0.000 | 0.595 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.842 | 0.082 | 0.158 | 0.498 | 0.454 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.894 | 0.188 | 0.106 | 0.496 | 0.396 |
| Adversarial High-Benefit Extreme Reform | Stylized U.S.-like conventional benchmark | 0.000 | 0.184 | 1.000 | 0.000 | 0.745 |
| Adversarial High-Benefit Extreme Reform | Unicameral simple majority | 0.050 | 0.108 | 0.950 | 0.000 | 0.742 |
| Adversarial High-Benefit Extreme Reform | Committee-first regular order | 0.019 | 0.127 | 0.981 | 0.000 | 0.752 |
| Adversarial High-Benefit Extreme Reform | Parliamentary coalition confidence | 0.037 | 0.126 | 0.963 | 0.000 | 0.744 |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives | 0.640 | 0.499 | 0.360 | 0.000 | 0.330 |
| Adversarial High-Benefit Extreme Reform | Citizen assembly threshold gate | 0.090 | 0.103 | 0.910 | 0.000 | 0.724 |
| Adversarial High-Benefit Extreme Reform | Risk-routed majority legislature | 0.615 | 0.186 | 0.385 | 0.000 | 0.437 |
| Adversarial High-Benefit Extreme Reform | Default pass unless 2/3 block | 0.908 | 0.046 | 0.092 | 0.484 | 0.429 |
| Adversarial High-Benefit Extreme Reform | Default pass + multi-round mediation + challenge | 0.768 | 0.183 | 0.232 | 0.160 | 0.393 |
| Adversarial Popular Harmful Bill | Stylized U.S.-like conventional benchmark | 0.174 | 0.412 | 0.826 | 0.000 | 0.590 |
| Adversarial Popular Harmful Bill | Unicameral simple majority | 0.871 | 0.289 | 0.129 | 0.000 | 0.278 |
| Adversarial Popular Harmful Bill | Committee-first regular order | 0.631 | 0.317 | 0.369 | 0.000 | 0.390 |
| Adversarial Popular Harmful Bill | Parliamentary coalition confidence | 0.422 | 0.407 | 0.578 | 0.000 | 0.467 |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives | 0.819 | 0.565 | 0.181 | 0.000 | 0.221 |
| Adversarial Popular Harmful Bill | Citizen assembly threshold gate | 0.206 | 0.420 | 0.794 | 0.000 | 0.571 |
| Adversarial Popular Harmful Bill | Risk-routed majority legislature | 0.983 | 0.360 | 0.017 | 0.000 | 0.200 |
| Adversarial Popular Harmful Bill | Default pass unless 2/3 block | 1.000 | 0.262 | 0.000 | 0.114 | 0.244 |
| Adversarial Popular Harmful Bill | Default pass + multi-round mediation + challenge | 0.989 | 0.359 | 0.011 | 0.005 | 0.199 |
| Adversarial Moderate Capture | Stylized U.S.-like conventional benchmark | 0.045 | 0.572 | 0.955 | 0.000 | 0.606 |
| Adversarial Moderate Capture | Unicameral simple majority | 0.967 | 0.493 | 0.033 | 0.000 | 0.168 |
| Adversarial Moderate Capture | Committee-first regular order | 0.836 | 0.499 | 0.164 | 0.000 | 0.233 |
| Adversarial Moderate Capture | Parliamentary coalition confidence | 0.848 | 0.532 | 0.152 | 0.000 | 0.216 |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives | 0.671 | 0.568 | 0.329 | 0.000 | 0.294 |
| Adversarial Moderate Capture | Citizen assembly threshold gate | 0.430 | 0.532 | 0.570 | 0.000 | 0.425 |
| Adversarial Moderate Capture | Risk-routed majority legislature | 0.981 | 0.525 | 0.019 | 0.000 | 0.152 |
| Adversarial Moderate Capture | Default pass unless 2/3 block | 1.000 | 0.487 | 0.000 | 0.028 | 0.160 |
| Adversarial Moderate Capture | Default pass + multi-round mediation + challenge | 0.993 | 0.524 | 0.007 | 0.007 | 0.148 |
| Adversarial Delayed-Benefit Reform | Stylized U.S.-like conventional benchmark | 0.002 | 0.352 | 0.998 | 0.000 | 0.693 |
| Adversarial Delayed-Benefit Reform | Unicameral simple majority | 0.175 | 0.262 | 0.825 | 0.000 | 0.634 |
| Adversarial Delayed-Benefit Reform | Committee-first regular order | 0.148 | 0.273 | 0.852 | 0.000 | 0.644 |
| Adversarial Delayed-Benefit Reform | Parliamentary coalition confidence | 0.207 | 0.279 | 0.793 | 0.000 | 0.613 |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives | 0.488 | 0.476 | 0.512 | 0.000 | 0.413 |
| Adversarial Delayed-Benefit Reform | Citizen assembly threshold gate | 0.261 | 0.241 | 0.739 | 0.000 | 0.597 |
| Adversarial Delayed-Benefit Reform | Risk-routed majority legislature | 0.688 | 0.267 | 0.312 | 0.000 | 0.376 |
| Adversarial Delayed-Benefit Reform | Default pass unless 2/3 block | 0.864 | 0.114 | 0.136 | 0.491 | 0.432 |
| Adversarial Delayed-Benefit Reform | Default pass + multi-round mediation + challenge | 0.840 | 0.260 | 0.160 | 0.165 | 0.335 |
| Adversarial Concentrated Rights Harm | Stylized U.S.-like conventional benchmark | 0.042 | 0.386 | 0.958 | 0.000 | 0.663 |
| Adversarial Concentrated Rights Harm | Unicameral simple majority | 0.505 | 0.255 | 0.495 | 0.000 | 0.471 |
| Adversarial Concentrated Rights Harm | Committee-first regular order | 0.275 | 0.297 | 0.725 | 0.000 | 0.574 |
| Adversarial Concentrated Rights Harm | Parliamentary coalition confidence | 0.384 | 0.305 | 0.616 | 0.000 | 0.516 |
| Adversarial Concentrated Rights Harm | Unicameral majority + pairwise alternatives | 0.475 | 0.519 | 0.525 | 0.000 | 0.407 |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate | 0.072 | 0.377 | 0.928 | 0.000 | 0.651 |
| Adversarial Concentrated Rights Harm | Risk-routed majority legislature | 0.765 | 0.285 | 0.235 | 0.000 | 0.332 |
| Adversarial Concentrated Rights Harm | Default pass unless 2/3 block | 0.980 | 0.174 | 0.020 | 0.338 | 0.325 |
| Adversarial Concentrated Rights Harm | Default pass + multi-round mediation + challenge | 0.848 | 0.285 | 0.152 | 0.063 | 0.303 |
| Adversarial Anti-Lobbying Backlash | Stylized U.S.-like conventional benchmark | 0.040 | 0.363 | 0.960 | 0.000 | 0.671 |
| Adversarial Anti-Lobbying Backlash | Unicameral simple majority | 0.322 | 0.280 | 0.678 | 0.000 | 0.555 |
| Adversarial Anti-Lobbying Backlash | Committee-first regular order | 0.202 | 0.299 | 0.798 | 0.000 | 0.609 |
| Adversarial Anti-Lobbying Backlash | Parliamentary coalition confidence | 0.323 | 0.322 | 0.677 | 0.000 | 0.542 |
| Adversarial Anti-Lobbying Backlash | Unicameral majority + pairwise alternatives | 0.415 | 0.497 | 0.585 | 0.000 | 0.443 |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate | 0.268 | 0.330 | 0.732 | 0.000 | 0.567 |
| Adversarial Anti-Lobbying Backlash | Risk-routed majority legislature | 0.404 | 0.335 | 0.596 | 0.000 | 0.497 |
| Adversarial Anti-Lobbying Backlash | Default pass unless 2/3 block | 0.892 | 0.208 | 0.108 | 0.513 | 0.394 |
| Adversarial Anti-Lobbying Backlash | Default pass + multi-round mediation + challenge | 0.703 | 0.317 | 0.297 | 0.342 | 0.422 |

## Default-Pass Side Note: Challenge-Voucher Deltas

Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.183 | -0.253 | 0.022 | -0.076 | -0.292 | -0.134 | 0.500 |
| Low Polarization | -11.492 | -0.192 | 0.031 | -0.141 | -0.146 | -0.067 | 0.500 |
| High Polarization | -16.675 | -0.278 | 0.012 | -0.040 | -0.354 | -0.163 | 0.500 |
| Low Party Loyalty | -15.108 | -0.252 | 0.028 | -0.092 | -0.298 | -0.140 | 0.500 |
| High Party Loyalty | -15.342 | -0.256 | 0.022 | -0.069 | -0.299 | -0.142 | 0.500 |
| Low Compromise Culture | -16.075 | -0.268 | 0.021 | -0.061 | -0.308 | -0.145 | 0.500 |
| High Compromise Culture | -14.817 | -0.247 | 0.026 | -0.093 | -0.283 | -0.134 | 0.500 |
| Low Lobbying Pressure | -15.750 | -0.262 | 0.023 | -0.074 | -0.298 | -0.140 | 0.500 |
| High Lobbying Pressure | -15.233 | -0.254 | 0.017 | -0.052 | -0.292 | -0.139 | 0.500 |
| Weak Constituency Pressure | -18.108 | -0.302 | 0.024 | -0.066 | -0.331 | -0.148 | 0.499 |
| Two-Party System | -6.833 | -0.114 | -0.007 | -0.023 | -0.146 | -0.076 | 0.333 |
| Multi-Party System | -30.033 | -0.501 | 0.116 | -0.302 | -0.529 | -0.337 | 0.801 |
| High Proposal Pressure | 2.633 | 0.015 | -0.016 | 0.007 | -0.030 | -0.053 | 0.167 |
| Extreme Proposal Pressure | 21.867 | 0.073 | -0.022 | 0.021 | 0.020 | -0.048 | 0.100 |
| Lobby-Fueled Flooding | 2.867 | 0.016 | -0.016 | 0.008 | -0.031 | -0.055 | 0.167 |
| Low-Compromise Flooding | 2.183 | 0.012 | -0.017 | 0.020 | -0.049 | -0.073 | 0.167 |
| Capture Crisis | 2.592 | 0.014 | -0.014 | 0.014 | -0.041 | -0.065 | 0.167 |
| Popular Anti-Lobbying Push | -2.283 | -0.019 | -0.013 | -0.008 | -0.055 | -0.056 | 0.250 |
| Weighted Two-Party Baseline | -6.100 | -0.102 | -0.007 | -0.015 | -0.143 | -0.081 | 0.333 |
| Weighted Two Major Plus Minors | -31.125 | -0.519 | 0.113 | -0.281 | -0.544 | -0.342 | 0.801 |
| Weighted Fragmented Multiparty | -29.308 | -0.488 | 0.114 | -0.362 | -0.480 | -0.294 | 0.854 |
| Weighted Dominant-Party Legislature | -20.025 | -0.334 | 0.042 | -0.157 | -0.351 | -0.179 | 0.667 |
| Era 1 Low Contention | -15.892 | -0.265 | 0.052 | -0.217 | -0.230 | -0.118 | 0.659 |
| Era 2 Normal Contention | -22.442 | -0.374 | 0.084 | -0.281 | -0.369 | -0.216 | 0.721 |
| Era 3 Polarizing | -28.642 | -0.477 | 0.107 | -0.293 | -0.495 | -0.321 | 0.781 |
| Era 4 High Contention | -13.408 | -0.179 | 0.001 | -0.024 | -0.217 | -0.099 | 0.400 |
| Era 5 Capture Contention | -2.975 | -0.033 | -0.013 | 0.016 | -0.100 | -0.088 | 0.222 |
| Era 6 Crisis | 1.158 | 0.010 | -0.016 | 0.029 | -0.063 | -0.086 | 0.167 |
| Adversarial High-Benefit Extreme Reform | -33.400 | -0.557 | -0.003 | -0.005 | -0.590 | -0.174 | 0.664 |
| Adversarial Popular Harmful Bill | -6.500 | -0.108 | -0.000 | -0.093 | -0.095 | -0.052 | 0.462 |
| Adversarial Moderate Capture | -1.250 | -0.021 | -0.000 | -0.017 | -0.009 | -0.002 | 0.330 |
| Adversarial Delayed-Benefit Reform | -27.450 | -0.458 | 0.002 | -0.101 | -0.438 | -0.220 | 0.666 |
| Adversarial Concentrated Rights Harm | -23.550 | -0.393 | 0.028 | -0.223 | -0.330 | -0.179 | 0.651 |
| Adversarial Anti-Lobbying Backlash | -22.608 | -0.377 | 0.046 | -0.156 | -0.260 | -0.157 | 0.648 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.837) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.746) | Default pass unless 2/3 block (0.847) | Stylized U.S.-like conventional benchmark (0.000) |
| High Polarization | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.834) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.774) | Default pass unless 2/3 block (0.841) | Stylized U.S.-like conventional benchmark (0.000) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.771) | Default pass unless 2/3 block (0.841) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark (0.765) | Default pass unless 2/3 block (0.831) | Stylized U.S.-like conventional benchmark (0.000) |
| High Compromise Culture | Stylized U.S.-like conventional benchmark (0.750) | Default pass unless 2/3 block (0.852) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.843) | Stylized U.S.-like conventional benchmark (0.000) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.833) | Stylized U.S.-like conventional benchmark (0.000) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.760) | Default pass unless 2/3 block (0.873) | Stylized U.S.-like conventional benchmark (0.000) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.846) | Stylized U.S.-like conventional benchmark (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.756) | Default pass unless 2/3 block (0.836) | Stylized U.S.-like conventional benchmark (0.000) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.757) | Default pass + multi-round mediation + challenge (0.901) | Stylized U.S.-like conventional benchmark (0.000) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.754) | Default pass + multi-round mediation + challenge (0.941) | Stylized U.S.-like conventional benchmark (0.000) |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark (0.757) | Default pass + multi-round mediation + challenge (0.896) | Stylized U.S.-like conventional benchmark (0.000) |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark (0.749) | Default pass + multi-round mediation + challenge (0.885) | Stylized U.S.-like conventional benchmark (0.000) |
| Capture Crisis | Parliamentary coalition confidence (0.752) | Default pass + multi-round mediation + challenge (0.889) | Stylized U.S.-like conventional benchmark (0.000) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.771) | Default pass + multi-round mediation + challenge (0.865) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Two-Party Baseline | Stylized U.S.-like conventional benchmark (0.766) | Default pass unless 2/3 block (0.833) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Two Major Plus Minors | Stylized U.S.-like conventional benchmark (0.758) | Default pass unless 2/3 block (0.846) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Fragmented Multiparty | Stylized U.S.-like conventional benchmark (0.752) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Weighted Dominant-Party Legislature | Stylized U.S.-like conventional benchmark (0.740) | Default pass unless 2/3 block (0.808) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 1 Low Contention | Stylized U.S.-like conventional benchmark (0.737) | Default pass unless 2/3 block (0.846) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 2 Normal Contention | Stylized U.S.-like conventional benchmark (0.764) | Default pass unless 2/3 block (0.842) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 3 Polarizing | Stylized U.S.-like conventional benchmark (0.767) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 4 High Contention | Stylized U.S.-like conventional benchmark (0.774) | Default pass unless 2/3 block (0.834) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 5 Capture Contention | Stylized U.S.-like conventional benchmark (0.744) | Default pass + multi-round mediation + challenge (0.866) | Stylized U.S.-like conventional benchmark (0.000) |
| Era 6 Crisis | Stylized U.S.-like conventional benchmark (0.761) | Default pass + multi-round mediation + challenge (0.894) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial High-Benefit Extreme Reform | Majority ratification + strategic policy tournament (0.815) | Default pass unless 2/3 block (0.908) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Majority ratification + strategic policy tournament (0.320) | Default pass unless 2/3 block (1.000) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives (0.381) | Default pass unless 2/3 block (1.000) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives (0.801) | Default pass unless 2/3 block (0.864) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Concentrated Rights Harm | Citizen assembly threshold gate (0.618) | Default pass unless 2/3 block (0.980) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Anti-Lobbying Backlash | Citizen assembly threshold gate (0.711) | Default pass unless 2/3 block (0.892) | Stylized U.S.-like conventional benchmark (0.000) |

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
