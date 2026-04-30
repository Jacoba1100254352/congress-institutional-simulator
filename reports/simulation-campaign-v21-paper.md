# Simulation Campaign v21 Paper

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 23
- experiment cases: 28

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

## Headline Findings

- The canonical paper campaign is breadth-first: 23 scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.
- Highest directional score, where lower-better risk metrics are inverted before combination, came from Unicameral majority + pairwise alternatives at 0.705.
- Best average welfare came from Current U.S.-style system at 0.757; highest compromise came from Unicameral majority + pairwise alternatives at 0.499.
- Highest productivity came from Default pass unless 2/3 block at 0.841.
- Open default-pass averaged 0.841 productivity, 0.444 low-support passage, and 0.658 policy shift, so it functions as a throughput/risk endpoint.
- The stylized current-system benchmark averaged 0.051 productivity and 0.757 welfare: it protects quality in the synthetic generator partly by allowing few proposals through.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, and risk control. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts low-support passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.544 | 0.580 | 0.897 | 0.155 | 13.886 | 44.160 | 0.663 | 0.000 | 0.078 | 0.578 | 0.058 | 0.298 | 0.213 | 0.000 | 0.000 | 0.000 | 0.000 | 0.423 | 0.000 | 0.464 |
| Majority + anti-capture bundle | 0.595 | 0.586 | 0.899 | 0.299 | 26.918 | 90.613 | 0.676 | 0.000 | 0.080 | 0.581 | 0.118 | 0.318 | 0.118 | 0.082 | 0.555 | 0.000 | 0.000 | 0.824 | 0.000 | 0.955 |
| Bicameral simple majority | 0.558 | 0.596 | 0.898 | 0.181 | 15.789 | 95.400 | 0.665 | 0.000 | 0.079 | 0.592 | 0.056 | 0.231 | 0.239 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.575 | 0.620 | 0.911 | 0.193 | 17.142 | 95.400 | 0.721 | 0.000 | 0.056 | 0.663 | 0.065 | 0.263 | 0.186 | 0.000 | 0.000 | 0.000 | 0.000 | 0.644 | 0.000 | 1.000 |
| Committee-first regular order | 0.558 | 0.602 | 0.905 | 0.168 | 14.784 | 19.855 | 0.681 | 0.000 | 0.077 | 0.583 | 0.048 | 0.217 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.460 | 0.000 | 0.220 |
| Compensation amendments + majority | 0.565 | 0.569 | 0.853 | 0.272 | 24.372 | 95.400 | 0.633 | 0.000 | 0.077 | 0.559 | 0.105 | 0.307 | 0.237 | 0.000 | 0.000 | 0.000 | 0.143 | 0.645 | 0.000 | 1.000 |
| Current U.S.-style system | 0.547 | 0.663 | 0.927 | 0.051 | 4.229 | 20.057 | 0.757 | 0.000 | 0.035 | 0.715 | 0.011 | 0.148 | 0.174 | 0.000 | 0.000 | 0.000 | 0.000 | 0.190 | 0.000 | 0.215 |
| Default pass unless 2/3 block | 0.651 | 0.468 | 0.644 | 0.841 | 80.199 | 95.400 | 0.498 | 0.444 | 0.167 | 0.394 | 0.658 | 0.651 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + challenge vouchers | 0.616 | 0.483 | 0.716 | 0.650 | 69.594 | 95.400 | 0.519 | 0.365 | 0.156 | 0.413 | 0.433 | 0.519 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.879 | 0.431 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.671 | 0.500 | 0.734 | 0.779 | 78.633 | 95.400 | 0.464 | 0.289 | 0.113 | 0.441 | 0.292 | 0.337 | 0.276 | 0.000 | 0.000 | 0.714 | 0.240 | 0.862 | 0.401 | 1.000 |
| Harm-weighted double majority | 0.576 | 0.573 | 0.897 | 0.257 | 22.859 | 95.400 | 0.643 | 0.000 | 0.079 | 0.562 | 0.096 | 0.296 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.640 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.574 | 0.561 | 0.867 | 0.295 | 26.605 | 95.400 | 0.621 | 0.000 | 0.100 | 0.538 | 0.161 | 0.347 | 0.239 | 0.000 | 0.000 | 0.000 | 0.000 | 0.661 | 0.000 | 1.000 |
| Parliamentary coalition confidence | 0.548 | 0.532 | 0.921 | 0.190 | 16.156 | 19.828 | 0.612 | 0.000 | 0.040 | 0.568 | 0.058 | 0.195 | 0.142 | 0.000 | 0.000 | 0.000 | 0.000 | 0.579 | 0.000 | 0.230 |
| Bicameral majority + presidential veto | 0.545 | 0.611 | 0.906 | 0.118 | 10.238 | 95.400 | 0.682 | 0.000 | 0.070 | 0.617 | 0.033 | 0.208 | 0.240 | 0.000 | 0.000 | 0.000 | 0.000 | 0.314 | 0.000 | 1.000 |
| Proposal bonds + majority | 0.573 | 0.569 | 0.879 | 0.271 | 24.141 | 93.795 | 0.637 | 0.000 | 0.091 | 0.553 | 0.104 | 0.306 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 | 0.642 | 0.000 | 0.990 |
| Majority + public-interest screen | 0.573 | 0.575 | 0.890 | 0.255 | 22.460 | 84.019 | 0.654 | 0.000 | 0.081 | 0.568 | 0.097 | 0.302 | 0.203 | 0.000 | 0.000 | 0.000 | 0.000 | 0.624 | 0.000 | 0.892 |
| Public objection window + majority | 0.570 | 0.596 | 0.908 | 0.206 | 18.130 | 95.400 | 0.679 | 0.000 | 0.063 | 0.605 | 0.063 | 0.231 | 0.185 | 0.000 | 0.000 | 0.000 | 0.000 | 0.598 | 0.000 | 1.000 |
| Quadratic attention budget + majority | 0.568 | 0.582 | 0.899 | 0.222 | 18.655 | 51.660 | 0.659 | 0.000 | 0.075 | 0.577 | 0.075 | 0.262 | 0.204 | 0.000 | 0.000 | 0.000 | 0.000 | 0.590 | 0.000 | 0.589 |
| Risk-routed majority legislature | 0.624 | 0.542 | 0.867 | 0.465 | 42.256 | 95.400 | 0.525 | 0.000 | 0.096 | 0.516 | 0.173 | 0.335 | 0.279 | 0.000 | 0.000 | 0.606 | 0.184 | 0.661 | 0.000 | 1.000 |
| Unicameral simple majority | 0.573 | 0.568 | 0.879 | 0.271 | 24.329 | 95.400 | 0.636 | 0.000 | 0.091 | 0.553 | 0.105 | 0.307 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.705 | 0.656 | 0.935 | 0.524 | 48.766 | 52.119 | 0.642 | 0.000 | 0.046 | 0.651 | 0.004 | 0.004 | 0.211 | 0.000 | 0.000 | 0.552 | 0.000 | 0.868 | 0.000 | 0.552 |
| Majority ratification + strategic policy tournament | 0.705 | 0.656 | 0.935 | 0.524 | 48.740 | 52.107 | 0.643 | 0.000 | 0.046 | 0.651 | 0.004 | 0.004 | 0.211 | 0.000 | 0.000 | 0.552 | 0.000 | 0.868 | 0.000 | 0.552 |
| Unicameral 60 percent passage | 0.550 | 0.641 | 0.913 | 0.097 | 8.157 | 95.400 | 0.707 | 0.000 | 0.060 | 0.654 | 0.022 | 0.150 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.264 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`, so it rises when a system blocks more, compromises less, or passes more weak-support bills.

| Era | Scenario | Productivity | Compromise | Gridlock | Low-support | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Current U.S.-style system | 0.046 | 0.369 | 0.954 | 0.000 | 0.666 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.000 | 0.601 |
| Baseline | Committee-first regular order | 0.153 | 0.278 | 0.847 | 0.000 | 0.640 |
| Baseline | Parliamentary coalition confidence | 0.182 | 0.284 | 0.818 | 0.000 | 0.623 |
| Baseline | Unicameral majority + pairwise alternatives | 0.547 | 0.490 | 0.453 | 0.000 | 0.380 |
| Baseline | Citizen assembly threshold gate | 0.181 | 0.262 | 0.819 | 0.000 | 0.631 |
| Baseline | Risk-routed majority legislature | 0.474 | 0.236 | 0.526 | 0.000 | 0.492 |
| Baseline | Default pass unless 2/3 block | 0.843 | 0.104 | 0.157 | 0.448 | 0.437 |
| Baseline | Default pass + multi-round mediation + challenge | 0.726 | 0.219 | 0.274 | 0.251 | 0.421 |
| Low Polarization | Current U.S.-style system | 0.158 | 0.377 | 0.842 | 0.000 | 0.608 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.000 | 0.457 |
| Low Polarization | Committee-first regular order | 0.388 | 0.308 | 0.612 | 0.000 | 0.514 |
| Low Polarization | Parliamentary coalition confidence | 0.485 | 0.301 | 0.515 | 0.000 | 0.468 |
| Low Polarization | Unicameral majority + pairwise alternatives | 0.631 | 0.633 | 0.369 | 0.000 | 0.295 |
| Low Polarization | Citizen assembly threshold gate | 0.406 | 0.298 | 0.594 | 0.000 | 0.508 |
| Low Polarization | Risk-routed majority legislature | 0.684 | 0.275 | 0.316 | 0.000 | 0.375 |
| Low Polarization | Default pass unless 2/3 block | 0.846 | 0.199 | 0.154 | 0.318 | 0.381 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.810 | 0.264 | 0.190 | 0.126 | 0.341 |
| High Polarization | Current U.S.-style system | 0.020 | 0.371 | 0.980 | 0.000 | 0.679 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.000 | 0.649 |
| High Polarization | Committee-first regular order | 0.094 | 0.279 | 0.906 | 0.000 | 0.669 |
| High Polarization | Parliamentary coalition confidence | 0.096 | 0.300 | 0.904 | 0.000 | 0.662 |
| High Polarization | Unicameral majority + pairwise alternatives | 0.490 | 0.445 | 0.510 | 0.000 | 0.422 |
| High Polarization | Citizen assembly threshold gate | 0.117 | 0.258 | 0.883 | 0.000 | 0.664 |
| High Polarization | Risk-routed majority legislature | 0.369 | 0.226 | 0.631 | 0.000 | 0.548 |
| High Polarization | Default pass unless 2/3 block | 0.837 | 0.081 | 0.163 | 0.487 | 0.455 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.679 | 0.206 | 0.321 | 0.355 | 0.470 |
| Low Party Loyalty | Current U.S.-style system | 0.046 | 0.350 | 0.954 | 0.000 | 0.672 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.000 | 0.594 |
| Low Party Loyalty | Committee-first regular order | 0.170 | 0.262 | 0.830 | 0.000 | 0.636 |
| Low Party Loyalty | Parliamentary coalition confidence | 0.185 | 0.277 | 0.815 | 0.000 | 0.624 |
| Low Party Loyalty | Unicameral majority + pairwise alternatives | 0.536 | 0.504 | 0.464 | 0.000 | 0.381 |
| Low Party Loyalty | Citizen assembly threshold gate | 0.199 | 0.247 | 0.801 | 0.000 | 0.626 |
| Low Party Loyalty | Risk-routed majority legislature | 0.514 | 0.231 | 0.486 | 0.000 | 0.473 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.839 | 0.105 | 0.161 | 0.452 | 0.439 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.739 | 0.220 | 0.261 | 0.252 | 0.415 |
| High Party Loyalty | Current U.S.-style system | 0.048 | 0.378 | 0.953 | 0.000 | 0.663 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.000 | 0.596 |
| High Party Loyalty | Committee-first regular order | 0.164 | 0.286 | 0.836 | 0.000 | 0.632 |
| High Party Loyalty | Parliamentary coalition confidence | 0.197 | 0.285 | 0.803 | 0.000 | 0.616 |
| High Party Loyalty | Unicameral majority + pairwise alternatives | 0.553 | 0.503 | 0.447 | 0.000 | 0.372 |
| High Party Loyalty | Citizen assembly threshold gate | 0.192 | 0.263 | 0.808 | 0.000 | 0.625 |
| High Party Loyalty | Risk-routed majority legislature | 0.474 | 0.239 | 0.526 | 0.000 | 0.492 |
| High Party Loyalty | Default pass unless 2/3 block | 0.841 | 0.110 | 0.159 | 0.441 | 0.434 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.714 | 0.221 | 0.286 | 0.246 | 0.426 |
| Low Compromise Culture | Current U.S.-style system | 0.030 | 0.371 | 0.970 | 0.000 | 0.674 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.000 | 0.623 |
| Low Compromise Culture | Committee-first regular order | 0.128 | 0.290 | 0.872 | 0.000 | 0.649 |
| Low Compromise Culture | Parliamentary coalition confidence | 0.151 | 0.295 | 0.849 | 0.000 | 0.636 |
| Low Compromise Culture | Unicameral majority + pairwise alternatives | 0.526 | 0.470 | 0.474 | 0.000 | 0.396 |
| Low Compromise Culture | Citizen assembly threshold gate | 0.159 | 0.270 | 0.841 | 0.000 | 0.639 |
| Low Compromise Culture | Risk-routed majority legislature | 0.376 | 0.237 | 0.624 | 0.000 | 0.541 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.826 | 0.103 | 0.174 | 0.475 | 0.451 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.672 | 0.212 | 0.328 | 0.352 | 0.471 |
| High Compromise Culture | Current U.S.-style system | 0.065 | 0.376 | 0.935 | 0.000 | 0.655 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.000 | 0.573 |
| High Compromise Culture | Committee-first regular order | 0.194 | 0.285 | 0.806 | 0.000 | 0.618 |
| High Compromise Culture | Parliamentary coalition confidence | 0.233 | 0.275 | 0.767 | 0.000 | 0.601 |
| High Compromise Culture | Unicameral majority + pairwise alternatives | 0.557 | 0.533 | 0.443 | 0.000 | 0.361 |
| High Compromise Culture | Citizen assembly threshold gate | 0.224 | 0.256 | 0.776 | 0.000 | 0.611 |
| High Compromise Culture | Risk-routed majority legislature | 0.576 | 0.236 | 0.424 | 0.000 | 0.441 |
| High Compromise Culture | Default pass unless 2/3 block | 0.856 | 0.109 | 0.144 | 0.425 | 0.424 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.761 | 0.223 | 0.239 | 0.175 | 0.388 |
| Low Lobbying Pressure | Current U.S.-style system | 0.057 | 0.388 | 0.943 | 0.000 | 0.655 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.000 | 0.597 |
| Low Lobbying Pressure | Committee-first regular order | 0.171 | 0.283 | 0.829 | 0.000 | 0.630 |
| Low Lobbying Pressure | Parliamentary coalition confidence | 0.199 | 0.282 | 0.801 | 0.000 | 0.616 |
| Low Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.570 | 0.515 | 0.430 | 0.000 | 0.361 |
| Low Lobbying Pressure | Citizen assembly threshold gate | 0.193 | 0.258 | 0.807 | 0.000 | 0.626 |
| Low Lobbying Pressure | Risk-routed majority legislature | 0.484 | 0.221 | 0.516 | 0.000 | 0.492 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.845 | 0.104 | 0.155 | 0.447 | 0.436 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.707 | 0.207 | 0.293 | 0.255 | 0.435 |
| High Lobbying Pressure | Current U.S.-style system | 0.026 | 0.367 | 0.974 | 0.000 | 0.677 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.000 | 0.613 |
| High Lobbying Pressure | Committee-first regular order | 0.134 | 0.270 | 0.866 | 0.000 | 0.652 |
| High Lobbying Pressure | Parliamentary coalition confidence | 0.136 | 0.310 | 0.864 | 0.000 | 0.639 |
| High Lobbying Pressure | Unicameral majority + pairwise alternatives | 0.484 | 0.476 | 0.516 | 0.000 | 0.415 |
| High Lobbying Pressure | Citizen assembly threshold gate | 0.157 | 0.278 | 0.843 | 0.000 | 0.638 |
| High Lobbying Pressure | Risk-routed majority legislature | 0.402 | 0.249 | 0.598 | 0.000 | 0.525 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.830 | 0.107 | 0.170 | 0.468 | 0.447 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.714 | 0.230 | 0.286 | 0.298 | 0.434 |
| Weak Constituency Pressure | Current U.S.-style system | 0.027 | 0.372 | 0.973 | 0.000 | 0.675 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.000 | 0.612 |
| Weak Constituency Pressure | Committee-first regular order | 0.127 | 0.283 | 0.873 | 0.000 | 0.651 |
| Weak Constituency Pressure | Parliamentary coalition confidence | 0.123 | 0.327 | 0.877 | 0.000 | 0.640 |
| Weak Constituency Pressure | Unicameral majority + pairwise alternatives | 0.525 | 0.466 | 0.475 | 0.000 | 0.397 |
| Weak Constituency Pressure | Citizen assembly threshold gate | 0.155 | 0.276 | 0.845 | 0.000 | 0.640 |
| Weak Constituency Pressure | Risk-routed majority legislature | 0.461 | 0.244 | 0.539 | 0.000 | 0.496 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.874 | 0.102 | 0.126 | 0.458 | 0.424 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.732 | 0.225 | 0.268 | 0.265 | 0.420 |
| Two-Party System | Current U.S.-style system | 0.048 | 0.382 | 0.952 | 0.000 | 0.661 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.000 | 0.596 |
| Two-Party System | Committee-first regular order | 0.160 | 0.276 | 0.840 | 0.000 | 0.637 |
| Two-Party System | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Two-Party System | Unicameral majority + pairwise alternatives | 0.543 | 0.486 | 0.457 | 0.000 | 0.382 |
| Two-Party System | Citizen assembly threshold gate | 0.192 | 0.257 | 0.808 | 0.000 | 0.627 |
| Two-Party System | Risk-routed majority legislature | 0.468 | 0.238 | 0.532 | 0.000 | 0.495 |
| Two-Party System | Default pass unless 2/3 block | 0.846 | 0.107 | 0.154 | 0.447 | 0.434 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.830 | 0.206 | 0.170 | 0.329 | 0.389 |
| Multi-Party System | Current U.S.-style system | 0.050 | 0.356 | 0.950 | 0.000 | 0.668 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.000 | 0.589 |
| Multi-Party System | Committee-first regular order | 0.171 | 0.278 | 0.829 | 0.000 | 0.631 |
| Multi-Party System | Parliamentary coalition confidence | 0.265 | 0.253 | 0.735 | 0.000 | 0.592 |
| Multi-Party System | Unicameral majority + pairwise alternatives | 0.542 | 0.511 | 0.458 | 0.000 | 0.376 |
| Multi-Party System | Citizen assembly threshold gate | 0.200 | 0.264 | 0.800 | 0.000 | 0.621 |
| Multi-Party System | Risk-routed majority legislature | 0.500 | 0.239 | 0.500 | 0.000 | 0.478 |
| Multi-Party System | Default pass unless 2/3 block | 0.838 | 0.109 | 0.162 | 0.448 | 0.438 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.642 | 0.232 | 0.358 | 0.143 | 0.438 |
| High Proposal Pressure | Current U.S.-style system | 0.048 | 0.381 | 0.952 | 0.000 | 0.662 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.000 | 0.597 |
| High Proposal Pressure | Committee-first regular order | 0.161 | 0.285 | 0.839 | 0.000 | 0.634 |
| High Proposal Pressure | Parliamentary coalition confidence | 0.187 | 0.289 | 0.813 | 0.000 | 0.619 |
| High Proposal Pressure | Unicameral majority + pairwise alternatives | 0.540 | 0.496 | 0.460 | 0.000 | 0.381 |
| High Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.262 | 0.813 | 0.000 | 0.628 |
| High Proposal Pressure | Risk-routed majority legislature | 0.479 | 0.239 | 0.521 | 0.000 | 0.489 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.847 | 0.107 | 0.153 | 0.448 | 0.434 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.902 | 0.203 | 0.098 | 0.357 | 0.359 |
| Extreme Proposal Pressure | Current U.S.-style system | 0.049 | 0.372 | 0.952 | 0.000 | 0.664 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.000 | 0.597 |
| Extreme Proposal Pressure | Committee-first regular order | 0.161 | 0.285 | 0.839 | 0.000 | 0.634 |
| Extreme Proposal Pressure | Parliamentary coalition confidence | 0.185 | 0.290 | 0.815 | 0.000 | 0.621 |
| Extreme Proposal Pressure | Unicameral majority + pairwise alternatives | 0.541 | 0.491 | 0.459 | 0.000 | 0.382 |
| Extreme Proposal Pressure | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.000 | 0.628 |
| Extreme Proposal Pressure | Risk-routed majority legislature | 0.479 | 0.238 | 0.521 | 0.000 | 0.489 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.843 | 0.105 | 0.157 | 0.444 | 0.436 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.940 | 0.199 | 0.060 | 0.381 | 0.347 |
| Lobby-Fueled Flooding | Current U.S.-style system | 0.021 | 0.366 | 0.979 | 0.000 | 0.680 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.000 | 0.618 |
| Lobby-Fueled Flooding | Committee-first regular order | 0.127 | 0.270 | 0.873 | 0.000 | 0.655 |
| Lobby-Fueled Flooding | Parliamentary coalition confidence | 0.116 | 0.321 | 0.884 | 0.000 | 0.646 |
| Lobby-Fueled Flooding | Unicameral majority + pairwise alternatives | 0.459 | 0.455 | 0.541 | 0.000 | 0.434 |
| Lobby-Fueled Flooding | Citizen assembly threshold gate | 0.146 | 0.277 | 0.854 | 0.000 | 0.644 |
| Lobby-Fueled Flooding | Risk-routed majority legislature | 0.376 | 0.259 | 0.624 | 0.000 | 0.534 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.840 | 0.107 | 0.160 | 0.474 | 0.443 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.896 | 0.208 | 0.104 | 0.411 | 0.372 |
| Low-Compromise Flooding | Current U.S.-style system | 0.018 | 0.407 | 0.982 | 0.000 | 0.669 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.000 | 0.643 |
| Low-Compromise Flooding | Committee-first regular order | 0.091 | 0.288 | 0.909 | 0.000 | 0.668 |
| Low-Compromise Flooding | Parliamentary coalition confidence | 0.100 | 0.313 | 0.900 | 0.000 | 0.656 |
| Low-Compromise Flooding | Unicameral majority + pairwise alternatives | 0.495 | 0.461 | 0.505 | 0.000 | 0.414 |
| Low-Compromise Flooding | Citizen assembly threshold gate | 0.125 | 0.266 | 0.875 | 0.000 | 0.658 |
| Low-Compromise Flooding | Risk-routed majority legislature | 0.338 | 0.234 | 0.662 | 0.000 | 0.561 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.833 | 0.092 | 0.167 | 0.489 | 0.454 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.885 | 0.189 | 0.115 | 0.469 | 0.395 |
| Capture Crisis | Current U.S.-style system | 0.012 | 0.365 | 0.988 | 0.000 | 0.685 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.000 | 0.641 |
| Capture Crisis | Committee-first regular order | 0.099 | 0.263 | 0.901 | 0.000 | 0.671 |
| Capture Crisis | Parliamentary coalition confidence | 0.069 | 0.339 | 0.931 | 0.000 | 0.664 |
| Capture Crisis | Unicameral majority + pairwise alternatives | 0.404 | 0.456 | 0.596 | 0.000 | 0.461 |
| Capture Crisis | Citizen assembly threshold gate | 0.113 | 0.267 | 0.887 | 0.000 | 0.663 |
| Capture Crisis | Risk-routed majority legislature | 0.323 | 0.257 | 0.677 | 0.000 | 0.561 |
| Capture Crisis | Default pass unless 2/3 block | 0.842 | 0.100 | 0.158 | 0.483 | 0.446 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.891 | 0.205 | 0.109 | 0.447 | 0.383 |
| Popular Anti-Lobbying Push | Current U.S.-style system | 0.070 | 0.380 | 0.930 | 0.000 | 0.651 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.000 | 0.554 |
| Popular Anti-Lobbying Push | Committee-first regular order | 0.219 | 0.285 | 0.781 | 0.000 | 0.605 |
| Popular Anti-Lobbying Push | Parliamentary coalition confidence | 0.273 | 0.285 | 0.727 | 0.000 | 0.578 |
| Popular Anti-Lobbying Push | Unicameral majority + pairwise alternatives | 0.544 | 0.544 | 0.456 | 0.000 | 0.365 |
| Popular Anti-Lobbying Push | Citizen assembly threshold gate | 0.255 | 0.272 | 0.745 | 0.000 | 0.591 |
| Popular Anti-Lobbying Push | Risk-routed majority legislature | 0.505 | 0.266 | 0.495 | 0.000 | 0.468 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.823 | 0.129 | 0.178 | 0.422 | 0.435 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.864 | 0.230 | 0.136 | 0.300 | 0.359 |
| Weighted Two-Party Baseline | Current U.S.-style system | 0.048 | 0.374 | 0.952 | 0.000 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.000 | 0.596 |
| Weighted Two-Party Baseline | Committee-first regular order | 0.157 | 0.295 | 0.843 | 0.000 | 0.633 |
| Weighted Two-Party Baseline | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Weighted Two-Party Baseline | Unicameral majority + pairwise alternatives | 0.541 | 0.507 | 0.459 | 0.000 | 0.377 |
| Weighted Two-Party Baseline | Citizen assembly threshold gate | 0.194 | 0.262 | 0.806 | 0.000 | 0.625 |
| Weighted Two-Party Baseline | Risk-routed majority legislature | 0.477 | 0.236 | 0.523 | 0.000 | 0.491 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.841 | 0.107 | 0.159 | 0.454 | 0.438 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.824 | 0.205 | 0.176 | 0.329 | 0.392 |
| Weighted Two Major Plus Minors | Current U.S.-style system | 0.050 | 0.384 | 0.950 | 0.000 | 0.660 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.000 | 0.598 |
| Weighted Two Major Plus Minors | Committee-first regular order | 0.164 | 0.286 | 0.836 | 0.000 | 0.632 |
| Weighted Two Major Plus Minors | Parliamentary coalition confidence | 0.253 | 0.259 | 0.747 | 0.000 | 0.596 |
| Weighted Two Major Plus Minors | Unicameral majority + pairwise alternatives | 0.543 | 0.508 | 0.457 | 0.000 | 0.376 |
| Weighted Two Major Plus Minors | Citizen assembly threshold gate | 0.187 | 0.263 | 0.813 | 0.000 | 0.628 |
| Weighted Two Major Plus Minors | Risk-routed majority legislature | 0.487 | 0.235 | 0.513 | 0.000 | 0.486 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.847 | 0.107 | 0.153 | 0.447 | 0.434 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.642 | 0.228 | 0.358 | 0.170 | 0.444 |
| Weighted Fragmented Multiparty | Current U.S.-style system | 0.067 | 0.360 | 0.933 | 0.000 | 0.658 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.000 | 0.570 |
| Weighted Fragmented Multiparty | Committee-first regular order | 0.210 | 0.282 | 0.790 | 0.000 | 0.610 |
| Weighted Fragmented Multiparty | Parliamentary coalition confidence | 0.344 | 0.244 | 0.656 | 0.000 | 0.555 |
| Weighted Fragmented Multiparty | Unicameral majority + pairwise alternatives | 0.550 | 0.532 | 0.450 | 0.000 | 0.365 |
| Weighted Fragmented Multiparty | Citizen assembly threshold gate | 0.235 | 0.266 | 0.765 | 0.000 | 0.603 |
| Weighted Fragmented Multiparty | Risk-routed majority legislature | 0.531 | 0.246 | 0.469 | 0.000 | 0.461 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.837 | 0.123 | 0.163 | 0.428 | 0.430 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.642 | 0.242 | 0.358 | 0.097 | 0.426 |
| Weighted Dominant-Party Legislature | Current U.S.-style system | 0.046 | 0.378 | 0.954 | 0.000 | 0.664 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.000 | 0.592 |
| Weighted Dominant-Party Legislature | Committee-first regular order | 0.176 | 0.286 | 0.824 | 0.000 | 0.626 |
| Weighted Dominant-Party Legislature | Parliamentary coalition confidence | 0.202 | 0.286 | 0.798 | 0.000 | 0.613 |
| Weighted Dominant-Party Legislature | Unicameral majority + pairwise alternatives | 0.552 | 0.523 | 0.448 | 0.000 | 0.367 |
| Weighted Dominant-Party Legislature | Citizen assembly threshold gate | 0.205 | 0.267 | 0.795 | 0.000 | 0.617 |
| Weighted Dominant-Party Legislature | Risk-routed majority legislature | 0.477 | 0.240 | 0.523 | 0.000 | 0.490 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.807 | 0.117 | 0.193 | 0.455 | 0.453 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.658 | 0.227 | 0.342 | 0.195 | 0.442 |
| Era 1 Low Contention | Current U.S.-style system | 0.164 | 0.377 | 0.836 | 0.000 | 0.605 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.000 | 0.466 |
| Era 1 Low Contention | Committee-first regular order | 0.370 | 0.300 | 0.630 | 0.000 | 0.525 |
| Era 1 Low Contention | Parliamentary coalition confidence | 0.514 | 0.274 | 0.486 | 0.000 | 0.461 |
| Era 1 Low Contention | Unicameral majority + pairwise alternatives | 0.625 | 0.638 | 0.375 | 0.000 | 0.296 |
| Era 1 Low Contention | Citizen assembly threshold gate | 0.383 | 0.288 | 0.617 | 0.000 | 0.522 |
| Era 1 Low Contention | Risk-routed majority legislature | 0.713 | 0.256 | 0.287 | 0.000 | 0.367 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.849 | 0.179 | 0.151 | 0.317 | 0.385 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.777 | 0.252 | 0.223 | 0.075 | 0.351 |
| Era 2 Normal Contention | Current U.S.-style system | 0.105 | 0.387 | 0.895 | 0.000 | 0.631 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.000 | 0.520 |
| Era 2 Normal Contention | Committee-first regular order | 0.284 | 0.291 | 0.716 | 0.000 | 0.571 |
| Era 2 Normal Contention | Parliamentary coalition confidence | 0.421 | 0.264 | 0.579 | 0.000 | 0.510 |
| Era 2 Normal Contention | Unicameral majority + pairwise alternatives | 0.587 | 0.570 | 0.413 | 0.000 | 0.336 |
| Era 2 Normal Contention | Citizen assembly threshold gate | 0.304 | 0.280 | 0.696 | 0.000 | 0.564 |
| Era 2 Normal Contention | Risk-routed majority legislature | 0.619 | 0.254 | 0.381 | 0.000 | 0.414 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.845 | 0.149 | 0.155 | 0.385 | 0.410 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.734 | 0.245 | 0.266 | 0.111 | 0.382 |
| Era 3 Polarizing | Current U.S.-style system | 0.059 | 0.378 | 0.941 | 0.000 | 0.657 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.000 | 0.575 |
| Era 3 Polarizing | Committee-first regular order | 0.197 | 0.282 | 0.803 | 0.000 | 0.617 |
| Era 3 Polarizing | Parliamentary coalition confidence | 0.296 | 0.260 | 0.704 | 0.000 | 0.574 |
| Era 3 Polarizing | Unicameral majority + pairwise alternatives | 0.556 | 0.509 | 0.444 | 0.000 | 0.369 |
| Era 3 Polarizing | Citizen assembly threshold gate | 0.222 | 0.267 | 0.778 | 0.000 | 0.609 |
| Era 3 Polarizing | Risk-routed majority legislature | 0.513 | 0.246 | 0.487 | 0.000 | 0.470 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.844 | 0.119 | 0.156 | 0.434 | 0.429 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.652 | 0.240 | 0.348 | 0.159 | 0.434 |
| Era 4 High Contention | Current U.S.-style system | 0.029 | 0.371 | 0.971 | 0.000 | 0.674 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.000 | 0.620 |
| Era 4 High Contention | Committee-first regular order | 0.125 | 0.279 | 0.875 | 0.000 | 0.654 |
| Era 4 High Contention | Parliamentary coalition confidence | 0.126 | 0.311 | 0.874 | 0.000 | 0.644 |
| Era 4 High Contention | Unicameral majority + pairwise alternatives | 0.517 | 0.476 | 0.483 | 0.000 | 0.399 |
| Era 4 High Contention | Citizen assembly threshold gate | 0.153 | 0.268 | 0.847 | 0.000 | 0.643 |
| Era 4 High Contention | Risk-routed majority legislature | 0.396 | 0.247 | 0.604 | 0.000 | 0.528 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.836 | 0.100 | 0.164 | 0.476 | 0.447 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.764 | 0.212 | 0.236 | 0.338 | 0.422 |
| Era 5 Capture Contention | Current U.S.-style system | 0.016 | 0.345 | 0.984 | 0.000 | 0.688 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.000 | 0.656 |
| Era 5 Capture Contention | Committee-first regular order | 0.081 | 0.263 | 0.919 | 0.000 | 0.681 |
| Era 5 Capture Contention | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 5 Capture Contention | Unicameral majority + pairwise alternatives | 0.438 | 0.428 | 0.562 | 0.000 | 0.453 |
| Era 5 Capture Contention | Citizen assembly threshold gate | 0.106 | 0.259 | 0.894 | 0.000 | 0.669 |
| Era 5 Capture Contention | Risk-routed majority legislature | 0.329 | 0.239 | 0.671 | 0.000 | 0.564 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.836 | 0.087 | 0.164 | 0.478 | 0.451 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.865 | 0.194 | 0.135 | 0.445 | 0.398 |
| Era 6 Crisis | Current U.S.-style system | 0.009 | 0.363 | 0.991 | 0.000 | 0.686 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.000 | 0.673 |
| Era 6 Crisis | Committee-first regular order | 0.063 | 0.260 | 0.937 | 0.000 | 0.691 |
| Era 6 Crisis | Parliamentary coalition confidence | 0.000 | 0.000 | 1.000 | 0.000 | 0.800 |
| Era 6 Crisis | Unicameral majority + pairwise alternatives | 0.358 | 0.412 | 0.643 | 0.000 | 0.498 |
| Era 6 Crisis | Citizen assembly threshold gate | 0.075 | 0.265 | 0.925 | 0.000 | 0.683 |
| Era 6 Crisis | Risk-routed majority legislature | 0.274 | 0.238 | 0.726 | 0.000 | 0.592 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.838 | 0.082 | 0.162 | 0.499 | 0.456 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.893 | 0.188 | 0.107 | 0.496 | 0.396 |

## Default-Pass Side Note: Challenge-Voucher Deltas

Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.717 | -0.262 | 0.021 | -0.070 | -0.301 | -0.140 | 0.500 |
| Low Polarization | -11.333 | -0.189 | 0.030 | -0.141 | -0.142 | -0.064 | 0.500 |
| High Polarization | -16.792 | -0.280 | 0.014 | -0.040 | -0.353 | -0.159 | 0.500 |
| Low Party Loyalty | -15.208 | -0.253 | 0.028 | -0.090 | -0.297 | -0.140 | 0.500 |
| High Party Loyalty | -15.675 | -0.261 | 0.022 | -0.070 | -0.306 | -0.148 | 0.500 |
| Low Compromise Culture | -15.667 | -0.261 | 0.020 | -0.051 | -0.302 | -0.140 | 0.500 |
| High Compromise Culture | -14.875 | -0.248 | 0.026 | -0.099 | -0.283 | -0.133 | 0.500 |
| Low Lobbying Pressure | -15.667 | -0.261 | 0.022 | -0.086 | -0.299 | -0.141 | 0.500 |
| High Lobbying Pressure | -15.025 | -0.250 | 0.018 | -0.056 | -0.291 | -0.140 | 0.500 |
| Weak Constituency Pressure | -18.067 | -0.301 | 0.023 | -0.073 | -0.328 | -0.145 | 0.499 |
| Two-Party System | -6.958 | -0.116 | -0.007 | -0.010 | -0.147 | -0.076 | 0.333 |
| Multi-Party System | -29.717 | -0.495 | 0.113 | -0.300 | -0.523 | -0.329 | 0.799 |
| High Proposal Pressure | 2.567 | 0.014 | -0.016 | 0.017 | -0.030 | -0.052 | 0.167 |
| Extreme Proposal Pressure | 22.317 | 0.074 | -0.022 | 0.027 | 0.021 | -0.049 | 0.100 |
| Lobby-Fueled Flooding | 2.833 | 0.016 | -0.016 | 0.015 | -0.031 | -0.055 | 0.167 |
| Low-Compromise Flooding | 3.333 | 0.019 | -0.017 | 0.016 | -0.045 | -0.075 | 0.167 |
| Capture Crisis | 2.058 | 0.011 | -0.015 | 0.019 | -0.042 | -0.063 | 0.167 |
| Popular Anti-Lobbying Push | -1.925 | -0.016 | -0.014 | -0.004 | -0.052 | -0.054 | 0.250 |
| Weighted Two-Party Baseline | -6.683 | -0.111 | -0.005 | -0.025 | -0.154 | -0.085 | 0.333 |
| Weighted Two Major Plus Minors | -30.967 | -0.516 | 0.114 | -0.284 | -0.545 | -0.346 | 0.800 |
| Weighted Fragmented Multiparty | -29.458 | -0.491 | 0.115 | -0.367 | -0.482 | -0.298 | 0.857 |
| Weighted Dominant-Party Legislature | -20.000 | -0.333 | 0.041 | -0.162 | -0.341 | -0.167 | 0.667 |
| Era 1 Low Contention | -16.050 | -0.267 | 0.052 | -0.219 | -0.236 | -0.121 | 0.659 |
| Era 2 Normal Contention | -23.108 | -0.385 | 0.086 | -0.292 | -0.376 | -0.222 | 0.722 |
| Era 3 Polarizing | -28.917 | -0.482 | 0.106 | -0.292 | -0.502 | -0.323 | 0.780 |
| Era 4 High Contention | -13.475 | -0.180 | 0.001 | -0.027 | -0.218 | -0.100 | 0.400 |
| Era 5 Capture Contention | -2.900 | -0.032 | -0.014 | 0.025 | -0.098 | -0.086 | 0.222 |
| Era 6 Crisis | 1.783 | 0.015 | -0.016 | 0.027 | -0.062 | -0.088 | 0.167 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Current U.S.-style system (0.758) | Default pass unless 2/3 block (0.843) | Current U.S.-style system (0.000) |
| Low Polarization | Current U.S.-style system (0.746) | Default pass unless 2/3 block (0.846) | Current U.S.-style system (0.000) |
| High Polarization | Current U.S.-style system (0.758) | Default pass unless 2/3 block (0.837) | Current U.S.-style system (0.000) |
| Low Party Loyalty | Current U.S.-style system (0.774) | Default pass unless 2/3 block (0.839) | Current U.S.-style system (0.000) |
| High Party Loyalty | Current U.S.-style system (0.771) | Default pass unless 2/3 block (0.841) | Current U.S.-style system (0.000) |
| Low Compromise Culture | Current U.S.-style system (0.765) | Default pass unless 2/3 block (0.826) | Current U.S.-style system (0.000) |
| High Compromise Culture | Current U.S.-style system (0.750) | Default pass unless 2/3 block (0.856) | Current U.S.-style system (0.000) |
| Low Lobbying Pressure | Current U.S.-style system (0.764) | Default pass unless 2/3 block (0.845) | Current U.S.-style system (0.000) |
| High Lobbying Pressure | Current U.S.-style system (0.752) | Default pass unless 2/3 block (0.830) | Current U.S.-style system (0.000) |
| Weak Constituency Pressure | Current U.S.-style system (0.760) | Default pass unless 2/3 block (0.874) | Current U.S.-style system (0.000) |
| Two-Party System | Current U.S.-style system (0.758) | Default pass unless 2/3 block (0.846) | Current U.S.-style system (0.000) |
| Multi-Party System | Current U.S.-style system (0.756) | Default pass unless 2/3 block (0.838) | Current U.S.-style system (0.000) |
| High Proposal Pressure | Current U.S.-style system (0.757) | Default pass + multi-round mediation + challenge (0.902) | Current U.S.-style system (0.000) |
| Extreme Proposal Pressure | Current U.S.-style system (0.754) | Default pass + multi-round mediation + challenge (0.940) | Current U.S.-style system (0.000) |
| Lobby-Fueled Flooding | Current U.S.-style system (0.757) | Default pass + multi-round mediation + challenge (0.896) | Current U.S.-style system (0.000) |
| Low-Compromise Flooding | Current U.S.-style system (0.749) | Default pass + multi-round mediation + challenge (0.885) | Current U.S.-style system (0.000) |
| Capture Crisis | Parliamentary coalition confidence (0.752) | Default pass + multi-round mediation + challenge (0.891) | Current U.S.-style system (0.000) |
| Popular Anti-Lobbying Push | Current U.S.-style system (0.771) | Default pass + multi-round mediation + challenge (0.864) | Current U.S.-style system (0.000) |
| Weighted Two-Party Baseline | Current U.S.-style system (0.766) | Default pass unless 2/3 block (0.841) | Current U.S.-style system (0.000) |
| Weighted Two Major Plus Minors | Current U.S.-style system (0.758) | Default pass unless 2/3 block (0.847) | Current U.S.-style system (0.000) |
| Weighted Fragmented Multiparty | Current U.S.-style system (0.752) | Default pass unless 2/3 block (0.837) | Current U.S.-style system (0.000) |
| Weighted Dominant-Party Legislature | Current U.S.-style system (0.740) | Default pass unless 2/3 block (0.807) | Current U.S.-style system (0.000) |
| Era 1 Low Contention | Current U.S.-style system (0.737) | Default pass unless 2/3 block (0.849) | Current U.S.-style system (0.000) |
| Era 2 Normal Contention | Current U.S.-style system (0.764) | Default pass unless 2/3 block (0.845) | Current U.S.-style system (0.000) |
| Era 3 Polarizing | Current U.S.-style system (0.767) | Default pass unless 2/3 block (0.844) | Current U.S.-style system (0.000) |
| Era 4 High Contention | Current U.S.-style system (0.774) | Default pass unless 2/3 block (0.836) | Current U.S.-style system (0.000) |
| Era 5 Capture Contention | Current U.S.-style system (0.744) | Default pass + multi-round mediation + challenge (0.865) | Current U.S.-style system (0.000) |
| Era 6 Crisis | Current U.S.-style system (0.761) | Default pass + multi-round mediation + challenge (0.893) | Current U.S.-style system (0.000) |

## Interpretation

- This is a breadth-first paper campaign. Default pass is retained as one burden-shifting stress test, while the main comparison spans conventional thresholds, committee-first regular order, coalition confidence, policy tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation rules, anti-capture safeguards, adaptive risk routing, and law-registry review.
- Open default-pass remains the throughput extreme, but its high low-support passage and policy movement make it a diagnostic endpoint rather than the project focus.
- Policy tournaments and risk-routed majority systems occupy the strongest compromise/productivity middle ground in this synthetic campaign; committee-first, public-interest, citizen, and parliamentary-style gates control risk but give up substantial throughput.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality, and generated welfare remains conditional on model assumptions.
- The next model extension should add stronger non-default families: multidimensional package bargaining, judicial/court intervention, executive emergency/delegated rulemaking, direct-democracy routes, electoral feedback, and media/information ecosystems.

## Reproduction

```sh
make campaign
```
