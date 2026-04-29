# Simulation Campaign v21 Paper

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 120
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 16
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

- Open default-pass averaged 0.841 productivity, versus 0.271 for simple majority.
- Open default-pass also averaged 0.444 low-support passage and 0.658 policy shift.
- Highest directional score, where lower-better risk metrics are inverted before combination, came from Default pass + adaptive strategy bundle at 0.720.
- Challenge vouchers averaged 0.431 challenge use, changed productivity by -0.191, and changed low-support passage by -0.081 relative to open default-pass.
- Public objection windows triggered on 0.642 of potential bills and changed low-support passage by -0.176 relative to open default-pass.
- Pairwise policy tournaments changed proposer agenda advantage by 0.002, policy shift by -0.653, and status-quo wins averaged 0.449 relative to open default-pass.
- Best average welfare in this campaign came from Current U.S.-style system at 0.786.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, and risk control. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts low-support passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bicameral simple majority | 0.558 | 0.596 | 0.898 | 0.181 | 15.789 | 95.400 | 0.665 | 0.000 | 0.079 | 0.592 | 0.056 | 0.231 | 0.239 | 0.000 | 0.000 | 0.000 | 0.000 | 0.462 | 0.000 | 1.000 |
| Current U.S.-style system | 0.550 | 0.671 | 0.931 | 0.048 | 3.914 | 16.922 | 0.786 | 0.000 | 0.032 | 0.720 | 0.010 | 0.145 | 0.156 | 0.000 | 0.000 | 0.000 | 0.000 | 0.192 | 0.000 | 0.182 |
| Default pass unless 2/3 block | 0.651 | 0.468 | 0.644 | 0.841 | 80.223 | 95.400 | 0.498 | 0.444 | 0.167 | 0.393 | 0.658 | 0.650 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.000 | 1.000 |
| Default pass + adaptive tracks strict | 0.576 | 0.569 | 0.871 | 0.289 | 26.190 | 67.022 | 0.649 | 0.082 | 0.084 | 0.567 | 0.113 | 0.309 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.714 | 0.000 | 0.713 |
| Default pass + affected-group sponsor gate | 0.567 | 0.606 | 0.889 | 0.206 | 17.857 | 17.892 | 0.722 | 0.167 | 0.033 | 0.666 | 0.070 | 0.244 | 0.137 | 0.000 | 0.000 | 0.000 | 0.000 | 0.719 | 0.000 | 0.206 |
| Default pass + pairwise policy tournament | 0.710 | 0.652 | 0.929 | 0.551 | 51.996 | 52.008 | 0.643 | 0.049 | 0.046 | 0.645 | 0.005 | 0.004 | 0.202 | 0.000 | 0.000 | 0.551 | 0.000 | 0.942 | 0.000 | 0.551 |
| Default pass + challenge vouchers | 0.616 | 0.483 | 0.716 | 0.651 | 69.618 | 95.400 | 0.519 | 0.363 | 0.156 | 0.413 | 0.433 | 0.520 | 0.255 | 0.000 | 0.000 | 0.000 | 0.000 | 0.876 | 0.431 | 1.000 |
| Default pass + constituent public will + citizen panel | 0.595 | 0.548 | 0.828 | 0.410 | 38.321 | 95.400 | 0.630 | 0.247 | 0.106 | 0.517 | 0.212 | 0.431 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.961 | 0.000 | 1.000 |
| Default pass + lobby-surcharge proposal costs | 0.560 | 0.472 | 0.706 | 0.500 | 47.416 | 50.823 | 0.534 | 0.454 | 0.145 | 0.425 | 0.519 | 0.915 | 0.179 | 0.000 | 0.000 | 0.000 | 0.000 | 0.841 | 0.000 | 0.536 |
| Default pass + adaptive strategy bundle | 0.720 | 0.494 | 0.701 | 0.965 | 91.546 | 94.833 | 0.458 | 0.374 | 0.120 | 0.434 | 0.368 | 0.343 | 0.240 | 0.129 | 0.557 | 0.996 | 0.229 | 0.990 | 0.000 | 0.996 |
| Default pass + law registry | 0.659 | 0.474 | 0.636 | 0.866 | 82.662 | 95.400 | 0.494 | 0.395 | 0.170 | 0.393 | 0.828 | 0.593 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.993 | 0.000 | 1.000 |
| Default pass + multi-round mediation + challenge | 0.671 | 0.499 | 0.732 | 0.781 | 78.775 | 95.400 | 0.464 | 0.289 | 0.113 | 0.441 | 0.294 | 0.338 | 0.276 | 0.000 | 0.000 | 0.714 | 0.240 | 0.864 | 0.401 | 1.000 |
| Default pass + public objection window | 0.597 | 0.529 | 0.813 | 0.450 | 41.784 | 95.400 | 0.595 | 0.268 | 0.104 | 0.507 | 0.211 | 0.375 | 0.215 | 0.000 | 0.000 | 0.000 | 0.000 | 0.896 | 0.000 | 1.000 |
| Bicameral majority + presidential veto | 0.545 | 0.611 | 0.906 | 0.118 | 10.238 | 95.400 | 0.682 | 0.000 | 0.070 | 0.617 | 0.033 | 0.208 | 0.240 | 0.000 | 0.000 | 0.000 | 0.000 | 0.314 | 0.000 | 1.000 |
| Unicameral simple majority | 0.573 | 0.568 | 0.879 | 0.271 | 24.329 | 95.400 | 0.636 | 0.000 | 0.091 | 0.553 | 0.105 | 0.307 | 0.237 | 0.000 | 0.000 | 0.000 | 0.000 | 0.643 | 0.000 | 1.000 |
| Unicameral 60 percent passage | 0.550 | 0.641 | 0.913 | 0.097 | 8.157 | 95.400 | 0.707 | 0.000 | 0.060 | 0.654 | 0.022 | 0.150 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 | 0.264 | 0.000 | 1.000 |

## Timeline Contention Path

This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`, so it rises when a system blocks more, compromises less, or passes more weak-support bills.

| Era | Scenario | Productivity | Compromise | Gridlock | Low-support | Contention index |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Current U.S.-style system | 0.045 | 0.374 | 0.955 | 0.000 | 0.665 |
| Baseline | Unicameral simple majority | 0.259 | 0.230 | 0.741 | 0.000 | 0.601 |
| Baseline | Default pass unless 2/3 block | 0.836 | 0.105 | 0.164 | 0.452 | 0.441 |
| Baseline | Default pass + challenge vouchers | 0.586 | 0.130 | 0.414 | 0.374 | 0.543 |
| Baseline | Default pass + multi-round mediation + challenge | 0.724 | 0.218 | 0.276 | 0.254 | 0.423 |
| Baseline | Default pass + pairwise policy tournament | 0.552 | 0.487 | 0.448 | 0.013 | 0.380 |
| Low Polarization | Current U.S.-style system | 0.145 | 0.383 | 0.855 | 0.000 | 0.612 |
| Low Polarization | Unicameral simple majority | 0.519 | 0.277 | 0.481 | 0.000 | 0.457 |
| Low Polarization | Default pass unless 2/3 block | 0.849 | 0.198 | 0.151 | 0.315 | 0.379 |
| Low Polarization | Default pass + challenge vouchers | 0.659 | 0.239 | 0.341 | 0.177 | 0.434 |
| Low Polarization | Default pass + multi-round mediation + challenge | 0.808 | 0.264 | 0.193 | 0.128 | 0.343 |
| Low Polarization | Default pass + pairwise policy tournament | 0.633 | 0.632 | 0.367 | 0.002 | 0.294 |
| High Polarization | Current U.S.-style system | 0.022 | 0.371 | 0.978 | 0.000 | 0.678 |
| High Polarization | Unicameral simple majority | 0.169 | 0.221 | 0.831 | 0.000 | 0.649 |
| High Polarization | Default pass unless 2/3 block | 0.835 | 0.081 | 0.165 | 0.483 | 0.455 |
| High Polarization | Default pass + challenge vouchers | 0.552 | 0.097 | 0.448 | 0.453 | 0.585 |
| High Polarization | Default pass + multi-round mediation + challenge | 0.682 | 0.207 | 0.318 | 0.344 | 0.466 |
| High Polarization | Default pass + pairwise policy tournament | 0.507 | 0.442 | 0.493 | 0.035 | 0.421 |
| Low Party Loyalty | Current U.S.-style system | 0.046 | 0.354 | 0.954 | 0.000 | 0.671 |
| Low Party Loyalty | Unicameral simple majority | 0.285 | 0.213 | 0.715 | 0.000 | 0.594 |
| Low Party Loyalty | Default pass unless 2/3 block | 0.841 | 0.105 | 0.159 | 0.454 | 0.439 |
| Low Party Loyalty | Default pass + challenge vouchers | 0.587 | 0.131 | 0.413 | 0.361 | 0.539 |
| Low Party Loyalty | Default pass + multi-round mediation + challenge | 0.749 | 0.218 | 0.251 | 0.248 | 0.409 |
| Low Party Loyalty | Default pass + pairwise policy tournament | 0.543 | 0.500 | 0.457 | 0.013 | 0.381 |
| High Party Loyalty | Current U.S.-style system | 0.045 | 0.394 | 0.955 | 0.000 | 0.659 |
| High Party Loyalty | Unicameral simple majority | 0.266 | 0.238 | 0.734 | 0.000 | 0.596 |
| High Party Loyalty | Default pass unless 2/3 block | 0.841 | 0.110 | 0.159 | 0.452 | 0.437 |
| High Party Loyalty | Default pass + challenge vouchers | 0.583 | 0.136 | 0.417 | 0.373 | 0.542 |
| High Party Loyalty | Default pass + multi-round mediation + challenge | 0.713 | 0.222 | 0.287 | 0.252 | 0.427 |
| High Party Loyalty | Default pass + pairwise policy tournament | 0.559 | 0.502 | 0.441 | 0.010 | 0.372 |
| Low Compromise Culture | Current U.S.-style system | 0.028 | 0.377 | 0.972 | 0.000 | 0.673 |
| Low Compromise Culture | Unicameral simple majority | 0.209 | 0.242 | 0.791 | 0.000 | 0.623 |
| Low Compromise Culture | Default pass unless 2/3 block | 0.823 | 0.103 | 0.177 | 0.481 | 0.454 |
| Low Compromise Culture | Default pass + challenge vouchers | 0.561 | 0.129 | 0.439 | 0.429 | 0.567 |
| Low Compromise Culture | Default pass + multi-round mediation + challenge | 0.679 | 0.212 | 0.321 | 0.343 | 0.465 |
| Low Compromise Culture | Default pass + pairwise policy tournament | 0.551 | 0.464 | 0.449 | 0.046 | 0.394 |
| High Compromise Culture | Current U.S.-style system | 0.063 | 0.385 | 0.937 | 0.000 | 0.653 |
| High Compromise Culture | Unicameral simple majority | 0.323 | 0.220 | 0.677 | 0.000 | 0.573 |
| High Compromise Culture | Default pass unless 2/3 block | 0.855 | 0.108 | 0.145 | 0.423 | 0.425 |
| High Compromise Culture | Default pass + challenge vouchers | 0.606 | 0.139 | 0.394 | 0.324 | 0.520 |
| High Compromise Culture | Default pass + multi-round mediation + challenge | 0.758 | 0.224 | 0.242 | 0.184 | 0.391 |
| High Compromise Culture | Default pass + pairwise policy tournament | 0.558 | 0.534 | 0.442 | 0.003 | 0.362 |
| Low Lobbying Pressure | Current U.S.-style system | 0.055 | 0.382 | 0.945 | 0.000 | 0.658 |
| Low Lobbying Pressure | Unicameral simple majority | 0.268 | 0.231 | 0.732 | 0.000 | 0.597 |
| Low Lobbying Pressure | Default pass unless 2/3 block | 0.845 | 0.103 | 0.155 | 0.434 | 0.433 |
| Low Lobbying Pressure | Default pass + challenge vouchers | 0.585 | 0.130 | 0.415 | 0.364 | 0.541 |
| Low Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.710 | 0.207 | 0.290 | 0.262 | 0.435 |
| Low Lobbying Pressure | Default pass + pairwise policy tournament | 0.573 | 0.514 | 0.427 | 0.007 | 0.360 |
| High Lobbying Pressure | Current U.S.-style system | 0.022 | 0.392 | 0.978 | 0.000 | 0.671 |
| High Lobbying Pressure | Unicameral simple majority | 0.237 | 0.227 | 0.763 | 0.000 | 0.613 |
| High Lobbying Pressure | Default pass unless 2/3 block | 0.833 | 0.107 | 0.167 | 0.471 | 0.446 |
| High Lobbying Pressure | Default pass + challenge vouchers | 0.583 | 0.133 | 0.417 | 0.401 | 0.549 |
| High Lobbying Pressure | Default pass + multi-round mediation + challenge | 0.716 | 0.229 | 0.284 | 0.296 | 0.433 |
| High Lobbying Pressure | Default pass + pairwise policy tournament | 0.538 | 0.463 | 0.462 | 0.089 | 0.410 |
| Weak Constituency Pressure | Current U.S.-style system | 0.025 | 0.382 | 0.975 | 0.000 | 0.673 |
| Weak Constituency Pressure | Unicameral simple majority | 0.229 | 0.245 | 0.771 | 0.000 | 0.612 |
| Weak Constituency Pressure | Default pass unless 2/3 block | 0.872 | 0.102 | 0.128 | 0.453 | 0.424 |
| Weak Constituency Pressure | Default pass + challenge vouchers | 0.573 | 0.132 | 0.428 | 0.392 | 0.553 |
| Weak Constituency Pressure | Default pass + multi-round mediation + challenge | 0.743 | 0.224 | 0.257 | 0.262 | 0.414 |
| Weak Constituency Pressure | Default pass + pairwise policy tournament | 0.546 | 0.462 | 0.454 | 0.041 | 0.397 |
| Two-Party System | Current U.S.-style system | 0.040 | 0.394 | 0.960 | 0.000 | 0.662 |
| Two-Party System | Unicameral simple majority | 0.271 | 0.229 | 0.729 | 0.000 | 0.596 |
| Two-Party System | Default pass unless 2/3 block | 0.847 | 0.107 | 0.153 | 0.447 | 0.434 |
| Two-Party System | Default pass + challenge vouchers | 0.735 | 0.111 | 0.265 | 0.432 | 0.486 |
| Two-Party System | Default pass + multi-round mediation + challenge | 0.830 | 0.207 | 0.170 | 0.325 | 0.388 |
| Two-Party System | Default pass + pairwise policy tournament | 0.549 | 0.483 | 0.451 | 0.012 | 0.383 |
| Multi-Party System | Current U.S.-style system | 0.046 | 0.375 | 0.954 | 0.000 | 0.665 |
| Multi-Party System | Unicameral simple majority | 0.282 | 0.232 | 0.718 | 0.000 | 0.589 |
| Multi-Party System | Default pass unless 2/3 block | 0.838 | 0.109 | 0.162 | 0.442 | 0.437 |
| Multi-Party System | Default pass + challenge vouchers | 0.343 | 0.211 | 0.657 | 0.134 | 0.592 |
| Multi-Party System | Default pass + multi-round mediation + challenge | 0.644 | 0.234 | 0.356 | 0.147 | 0.437 |
| Multi-Party System | Default pass + pairwise policy tournament | 0.547 | 0.509 | 0.453 | 0.012 | 0.376 |
| High Proposal Pressure | Current U.S.-style system | 0.044 | 0.382 | 0.956 | 0.000 | 0.664 |
| High Proposal Pressure | Unicameral simple majority | 0.267 | 0.232 | 0.733 | 0.000 | 0.597 |
| High Proposal Pressure | Default pass unless 2/3 block | 0.845 | 0.107 | 0.155 | 0.451 | 0.436 |
| High Proposal Pressure | Default pass + challenge vouchers | 0.861 | 0.102 | 0.139 | 0.462 | 0.431 |
| High Proposal Pressure | Default pass + multi-round mediation + challenge | 0.902 | 0.203 | 0.098 | 0.360 | 0.360 |
| High Proposal Pressure | Default pass + pairwise policy tournament | 0.546 | 0.494 | 0.454 | 0.011 | 0.381 |
| Extreme Proposal Pressure | Current U.S.-style system | 0.044 | 0.380 | 0.956 | 0.000 | 0.664 |
| Extreme Proposal Pressure | Unicameral simple majority | 0.266 | 0.232 | 0.734 | 0.000 | 0.597 |
| Extreme Proposal Pressure | Default pass unless 2/3 block | 0.845 | 0.105 | 0.155 | 0.447 | 0.435 |
| Extreme Proposal Pressure | Default pass + challenge vouchers | 0.916 | 0.096 | 0.084 | 0.467 | 0.406 |
| Extreme Proposal Pressure | Default pass + multi-round mediation + challenge | 0.942 | 0.199 | 0.058 | 0.381 | 0.346 |
| Extreme Proposal Pressure | Default pass + pairwise policy tournament | 0.546 | 0.489 | 0.455 | 0.009 | 0.382 |
| Lobby-Fueled Flooding | Current U.S.-style system | 0.018 | 0.374 | 0.982 | 0.000 | 0.678 |
| Lobby-Fueled Flooding | Unicameral simple majority | 0.223 | 0.235 | 0.777 | 0.000 | 0.618 |
| Lobby-Fueled Flooding | Default pass unless 2/3 block | 0.842 | 0.107 | 0.158 | 0.479 | 0.443 |
| Lobby-Fueled Flooding | Default pass + challenge vouchers | 0.856 | 0.102 | 0.144 | 0.484 | 0.438 |
| Lobby-Fueled Flooding | Default pass + multi-round mediation + challenge | 0.895 | 0.208 | 0.105 | 0.414 | 0.373 |
| Lobby-Fueled Flooding | Default pass + pairwise policy tournament | 0.532 | 0.437 | 0.468 | 0.134 | 0.430 |
| Low-Compromise Flooding | Current U.S.-style system | 0.018 | 0.382 | 0.983 | 0.000 | 0.677 |
| Low-Compromise Flooding | Unicameral simple majority | 0.169 | 0.241 | 0.831 | 0.000 | 0.643 |
| Low-Compromise Flooding | Default pass unless 2/3 block | 0.835 | 0.092 | 0.165 | 0.486 | 0.452 |
| Low-Compromise Flooding | Default pass + challenge vouchers | 0.850 | 0.086 | 0.150 | 0.505 | 0.450 |
| Low-Compromise Flooding | Default pass + multi-round mediation + challenge | 0.883 | 0.188 | 0.118 | 0.471 | 0.396 |
| Low-Compromise Flooding | Default pass + pairwise policy tournament | 0.531 | 0.453 | 0.469 | 0.069 | 0.412 |
| Capture Crisis | Current U.S.-style system | 0.011 | 0.371 | 0.989 | 0.000 | 0.683 |
| Capture Crisis | Unicameral simple majority | 0.185 | 0.222 | 0.815 | 0.000 | 0.641 |
| Capture Crisis | Default pass unless 2/3 block | 0.838 | 0.099 | 0.162 | 0.485 | 0.448 |
| Capture Crisis | Default pass + challenge vouchers | 0.856 | 0.095 | 0.144 | 0.499 | 0.444 |
| Capture Crisis | Default pass + multi-round mediation + challenge | 0.890 | 0.205 | 0.110 | 0.444 | 0.382 |
| Capture Crisis | Default pass + pairwise policy tournament | 0.529 | 0.424 | 0.471 | 0.235 | 0.455 |
| Popular Anti-Lobbying Push | Current U.S.-style system | 0.064 | 0.384 | 0.936 | 0.000 | 0.653 |
| Popular Anti-Lobbying Push | Unicameral simple majority | 0.351 | 0.234 | 0.649 | 0.000 | 0.554 |
| Popular Anti-Lobbying Push | Default pass unless 2/3 block | 0.823 | 0.129 | 0.177 | 0.421 | 0.434 |
| Popular Anti-Lobbying Push | Default pass + challenge vouchers | 0.808 | 0.128 | 0.192 | 0.415 | 0.440 |
| Popular Anti-Lobbying Push | Default pass + multi-round mediation + challenge | 0.864 | 0.230 | 0.136 | 0.298 | 0.358 |
| Popular Anti-Lobbying Push | Default pass + pairwise policy tournament | 0.554 | 0.540 | 0.446 | 0.017 | 0.364 |
| Weighted Two-Party Baseline | Current U.S.-style system | 0.043 | 0.382 | 0.957 | 0.000 | 0.664 |
| Weighted Two-Party Baseline | Unicameral simple majority | 0.267 | 0.234 | 0.733 | 0.000 | 0.596 |
| Weighted Two-Party Baseline | Default pass unless 2/3 block | 0.835 | 0.107 | 0.165 | 0.453 | 0.441 |
| Weighted Two-Party Baseline | Default pass + challenge vouchers | 0.733 | 0.113 | 0.267 | 0.433 | 0.486 |
| Weighted Two-Party Baseline | Default pass + multi-round mediation + challenge | 0.825 | 0.206 | 0.175 | 0.329 | 0.391 |
| Weighted Two-Party Baseline | Default pass + pairwise policy tournament | 0.547 | 0.505 | 0.453 | 0.012 | 0.377 |
| Weighted Two Major Plus Minors | Current U.S.-style system | 0.046 | 0.375 | 0.954 | 0.000 | 0.665 |
| Weighted Two Major Plus Minors | Unicameral simple majority | 0.265 | 0.231 | 0.735 | 0.000 | 0.598 |
| Weighted Two Major Plus Minors | Default pass unless 2/3 block | 0.846 | 0.107 | 0.154 | 0.450 | 0.435 |
| Weighted Two Major Plus Minors | Default pass + challenge vouchers | 0.329 | 0.210 | 0.671 | 0.170 | 0.607 |
| Weighted Two Major Plus Minors | Default pass + multi-round mediation + challenge | 0.641 | 0.227 | 0.359 | 0.160 | 0.444 |
| Weighted Two Major Plus Minors | Default pass + pairwise policy tournament | 0.549 | 0.507 | 0.451 | 0.008 | 0.375 |
| Weighted Fragmented Multiparty | Current U.S.-style system | 0.063 | 0.379 | 0.937 | 0.000 | 0.655 |
| Weighted Fragmented Multiparty | Unicameral simple majority | 0.319 | 0.237 | 0.681 | 0.000 | 0.570 |
| Weighted Fragmented Multiparty | Default pass unless 2/3 block | 0.833 | 0.123 | 0.167 | 0.423 | 0.431 |
| Weighted Fragmented Multiparty | Default pass + challenge vouchers | 0.350 | 0.233 | 0.650 | 0.059 | 0.567 |
| Weighted Fragmented Multiparty | Default pass + multi-round mediation + challenge | 0.634 | 0.244 | 0.366 | 0.087 | 0.427 |
| Weighted Fragmented Multiparty | Default pass + pairwise policy tournament | 0.555 | 0.530 | 0.445 | 0.008 | 0.365 |
| Weighted Dominant-Party Legislature | Current U.S.-style system | 0.043 | 0.361 | 0.957 | 0.000 | 0.670 |
| Weighted Dominant-Party Legislature | Unicameral simple majority | 0.272 | 0.241 | 0.728 | 0.000 | 0.592 |
| Weighted Dominant-Party Legislature | Default pass unless 2/3 block | 0.801 | 0.118 | 0.199 | 0.445 | 0.453 |
| Weighted Dominant-Party Legislature | Default pass + challenge vouchers | 0.469 | 0.167 | 0.531 | 0.295 | 0.574 |
| Weighted Dominant-Party Legislature | Default pass + multi-round mediation + challenge | 0.659 | 0.229 | 0.341 | 0.193 | 0.440 |
| Weighted Dominant-Party Legislature | Default pass + pairwise policy tournament | 0.558 | 0.521 | 0.442 | 0.016 | 0.368 |
| Era 1 Low Contention | Current U.S.-style system | 0.156 | 0.389 | 0.844 | 0.000 | 0.605 |
| Era 1 Low Contention | Unicameral simple majority | 0.512 | 0.260 | 0.488 | 0.000 | 0.466 |
| Era 1 Low Contention | Default pass unless 2/3 block | 0.850 | 0.178 | 0.150 | 0.321 | 0.386 |
| Era 1 Low Contention | Default pass + challenge vouchers | 0.574 | 0.242 | 0.426 | 0.099 | 0.460 |
| Era 1 Low Contention | Default pass + multi-round mediation + challenge | 0.783 | 0.252 | 0.217 | 0.072 | 0.347 |
| Era 1 Low Contention | Default pass + pairwise policy tournament | 0.626 | 0.639 | 0.374 | 0.001 | 0.296 |
| Era 2 Normal Contention | Current U.S.-style system | 0.101 | 0.392 | 0.899 | 0.000 | 0.632 |
| Era 2 Normal Contention | Unicameral simple majority | 0.411 | 0.249 | 0.589 | 0.000 | 0.520 |
| Era 2 Normal Contention | Default pass unless 2/3 block | 0.844 | 0.149 | 0.156 | 0.386 | 0.410 |
| Era 2 Normal Contention | Default pass + challenge vouchers | 0.462 | 0.241 | 0.538 | 0.095 | 0.516 |
| Era 2 Normal Contention | Default pass + multi-round mediation + challenge | 0.742 | 0.244 | 0.258 | 0.112 | 0.378 |
| Era 2 Normal Contention | Default pass + pairwise policy tournament | 0.588 | 0.569 | 0.412 | 0.002 | 0.336 |
| Era 3 Polarizing | Current U.S.-style system | 0.057 | 0.395 | 0.943 | 0.000 | 0.653 |
| Era 3 Polarizing | Unicameral simple majority | 0.307 | 0.237 | 0.693 | 0.000 | 0.575 |
| Era 3 Polarizing | Default pass unless 2/3 block | 0.843 | 0.119 | 0.157 | 0.440 | 0.431 |
| Era 3 Polarizing | Default pass + challenge vouchers | 0.366 | 0.222 | 0.634 | 0.141 | 0.579 |
| Era 3 Polarizing | Default pass + multi-round mediation + challenge | 0.665 | 0.239 | 0.335 | 0.154 | 0.426 |
| Era 3 Polarizing | Default pass + pairwise policy tournament | 0.560 | 0.508 | 0.440 | 0.011 | 0.370 |
| Era 4 High Contention | Current U.S.-style system | 0.024 | 0.375 | 0.976 | 0.000 | 0.675 |
| Era 4 High Contention | Unicameral simple majority | 0.215 | 0.240 | 0.785 | 0.000 | 0.620 |
| Era 4 High Contention | Default pass unless 2/3 block | 0.836 | 0.100 | 0.164 | 0.467 | 0.445 |
| Era 4 High Contention | Default pass + challenge vouchers | 0.653 | 0.109 | 0.347 | 0.449 | 0.530 |
| Era 4 High Contention | Default pass + multi-round mediation + challenge | 0.767 | 0.210 | 0.233 | 0.335 | 0.420 |
| Era 4 High Contention | Default pass + pairwise policy tournament | 0.541 | 0.468 | 0.459 | 0.046 | 0.398 |
| Era 5 Capture Contention | Current U.S.-style system | 0.014 | 0.376 | 0.986 | 0.000 | 0.681 |
| Era 5 Capture Contention | Unicameral simple majority | 0.154 | 0.223 | 0.846 | 0.000 | 0.656 |
| Era 5 Capture Contention | Default pass unless 2/3 block | 0.836 | 0.086 | 0.164 | 0.479 | 0.452 |
| Era 5 Capture Contention | Default pass + challenge vouchers | 0.804 | 0.083 | 0.196 | 0.499 | 0.473 |
| Era 5 Capture Contention | Default pass + multi-round mediation + challenge | 0.864 | 0.194 | 0.136 | 0.446 | 0.399 |
| Era 5 Capture Contention | Default pass + pairwise policy tournament | 0.507 | 0.412 | 0.493 | 0.131 | 0.449 |
| Era 6 Crisis | Current U.S.-style system | 0.008 | 0.363 | 0.992 | 0.000 | 0.687 |
| Era 6 Crisis | Unicameral simple majority | 0.123 | 0.219 | 0.877 | 0.000 | 0.673 |
| Era 6 Crisis | Default pass unless 2/3 block | 0.843 | 0.082 | 0.157 | 0.498 | 0.453 |
| Era 6 Crisis | Default pass + challenge vouchers | 0.853 | 0.078 | 0.147 | 0.523 | 0.455 |
| Era 6 Crisis | Default pass + multi-round mediation + challenge | 0.893 | 0.188 | 0.108 | 0.494 | 0.396 |
| Era 6 Crisis | Default pass + pairwise policy tournament | 0.498 | 0.380 | 0.502 | 0.277 | 0.492 |

## Challenge-Voucher Deltas

Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.

| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | -15.025 | -0.250 | 0.022 | -0.079 | -0.292 | -0.138 | 0.500 |
| Low Polarization | -11.425 | -0.190 | 0.030 | -0.138 | -0.147 | -0.069 | 0.500 |
| High Polarization | -16.958 | -0.283 | 0.011 | -0.029 | -0.352 | -0.155 | 0.500 |
| Low Party Loyalty | -15.233 | -0.254 | 0.028 | -0.093 | -0.296 | -0.137 | 0.500 |
| High Party Loyalty | -15.500 | -0.258 | 0.023 | -0.080 | -0.299 | -0.140 | 0.500 |
| Low Compromise Culture | -15.742 | -0.262 | 0.019 | -0.052 | -0.305 | -0.146 | 0.500 |
| High Compromise Culture | -14.892 | -0.248 | 0.026 | -0.100 | -0.286 | -0.139 | 0.500 |
| Low Lobbying Pressure | -15.600 | -0.260 | 0.023 | -0.070 | -0.299 | -0.138 | 0.500 |
| High Lobbying Pressure | -15.008 | -0.250 | 0.018 | -0.070 | -0.292 | -0.140 | 0.500 |
| Weak Constituency Pressure | -17.992 | -0.300 | 0.024 | -0.062 | -0.323 | -0.141 | 0.499 |
| Two-Party System | -6.700 | -0.112 | -0.007 | -0.015 | -0.144 | -0.075 | 0.333 |
| Multi-Party System | -29.717 | -0.495 | 0.116 | -0.308 | -0.521 | -0.323 | 0.801 |
| High Proposal Pressure | 2.875 | 0.016 | -0.016 | 0.011 | -0.029 | -0.053 | 0.167 |
| Extreme Proposal Pressure | 21.333 | 0.071 | -0.022 | 0.020 | 0.019 | -0.048 | 0.100 |
| Lobby-Fueled Flooding | 2.592 | 0.014 | -0.015 | 0.005 | -0.032 | -0.055 | 0.167 |
| Low-Compromise Flooding | 2.783 | 0.015 | -0.017 | 0.019 | -0.046 | -0.073 | 0.167 |
| Capture Crisis | 3.125 | 0.017 | -0.015 | 0.014 | -0.040 | -0.066 | 0.167 |
| Popular Anti-Lobbying Push | -1.825 | -0.015 | -0.013 | -0.006 | -0.052 | -0.054 | 0.250 |
| Weighted Two-Party Baseline | -6.083 | -0.101 | -0.006 | -0.020 | -0.146 | -0.084 | 0.333 |
| Weighted Two Major Plus Minors | -31.008 | -0.517 | 0.113 | -0.281 | -0.545 | -0.347 | 0.799 |
| Weighted Fragmented Multiparty | -29.000 | -0.483 | 0.114 | -0.364 | -0.478 | -0.294 | 0.854 |
| Weighted Dominant-Party Legislature | -19.925 | -0.332 | 0.039 | -0.150 | -0.341 | -0.174 | 0.667 |
| Era 1 Low Contention | -16.517 | -0.275 | 0.052 | -0.222 | -0.238 | -0.119 | 0.661 |
| Era 2 Normal Contention | -22.958 | -0.383 | 0.086 | -0.291 | -0.371 | -0.216 | 0.722 |
| Era 3 Polarizing | -28.633 | -0.477 | 0.105 | -0.299 | -0.497 | -0.322 | 0.778 |
| Era 4 High Contention | -13.708 | -0.183 | -0.000 | -0.019 | -0.222 | -0.102 | 0.400 |
| Era 5 Capture Contention | -2.908 | -0.032 | -0.013 | 0.020 | -0.099 | -0.088 | 0.222 |
| Era 6 Crisis | 1.225 | 0.010 | -0.016 | 0.025 | -0.062 | -0.085 | 0.167 |

## Law-Registry Deltas

Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.

| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + law registry | 0.024 | -0.005 | 0.444 | 5.126 | 0.609 | 0.040 | 0.170 |

## Policy-Tournament Deltas

Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.

| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Default pass + pairwise policy tournament | -0.291 | 0.144 | -0.395 | -0.653 | -0.646 | 0.001 | 0.002 | 6.000 | 0.449 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-support passage |
| --- | --- | --- | --- |
| Baseline | Current U.S.-style system (0.785) | Default pass + adaptive strategy bundle (0.974) | Current U.S.-style system (0.000) |
| Low Polarization | Current U.S.-style system (0.780) | Default pass + adaptive strategy bundle (0.990) | Current U.S.-style system (0.000) |
| High Polarization | Current U.S.-style system (0.782) | Default pass + adaptive strategy bundle (0.962) | Current U.S.-style system (0.000) |
| Low Party Loyalty | Current U.S.-style system (0.793) | Default pass + adaptive strategy bundle (0.978) | Current U.S.-style system (0.000) |
| High Party Loyalty | Current U.S.-style system (0.788) | Default pass + adaptive strategy bundle (0.975) | Current U.S.-style system (0.000) |
| Low Compromise Culture | Current U.S.-style system (0.783) | Default pass + adaptive strategy bundle (0.957) | Current U.S.-style system (0.000) |
| High Compromise Culture | Current U.S.-style system (0.778) | Default pass + adaptive strategy bundle (0.983) | Current U.S.-style system (0.000) |
| Low Lobbying Pressure | Current U.S.-style system (0.784) | Default pass + adaptive strategy bundle (0.981) | Current U.S.-style system (0.000) |
| High Lobbying Pressure | Current U.S.-style system (0.791) | Default pass + adaptive strategy bundle (0.949) | Current U.S.-style system (0.000) |
| Weak Constituency Pressure | Current U.S.-style system (0.776) | Default pass + adaptive strategy bundle (0.983) | Current U.S.-style system (0.000) |
| Two-Party System | Current U.S.-style system (0.791) | Default pass + adaptive strategy bundle (0.972) | Current U.S.-style system (0.000) |
| Multi-Party System | Current U.S.-style system (0.779) | Default pass + adaptive strategy bundle (0.976) | Current U.S.-style system (0.000) |
| High Proposal Pressure | Current U.S.-style system (0.787) | Default pass + adaptive strategy bundle (0.969) | Current U.S.-style system (0.000) |
| Extreme Proposal Pressure | Current U.S.-style system (0.780) | Default pass + adaptive strategy bundle (0.966) | Current U.S.-style system (0.000) |
| Lobby-Fueled Flooding | Current U.S.-style system (0.790) | Default pass + adaptive strategy bundle (0.939) | Current U.S.-style system (0.000) |
| Low-Compromise Flooding | Current U.S.-style system (0.790) | Default pass + adaptive strategy bundle (0.950) | Current U.S.-style system (0.000) |
| Capture Crisis | Current U.S.-style system (0.768) | Default pass + adaptive strategy bundle (0.927) | Current U.S.-style system (0.000) |
| Popular Anti-Lobbying Push | Current U.S.-style system (0.801) | Default pass + adaptive strategy bundle (0.952) | Current U.S.-style system (0.000) |
| Weighted Two-Party Baseline | Current U.S.-style system (0.788) | Default pass + adaptive strategy bundle (0.971) | Current U.S.-style system (0.000) |
| Weighted Two Major Plus Minors | Current U.S.-style system (0.781) | Default pass + adaptive strategy bundle (0.974) | Current U.S.-style system (0.000) |
| Weighted Fragmented Multiparty | Current U.S.-style system (0.785) | Default pass + adaptive strategy bundle (0.978) | Current U.S.-style system (0.000) |
| Weighted Dominant-Party Legislature | Current U.S.-style system (0.767) | Default pass + adaptive strategy bundle (0.971) | Current U.S.-style system (0.000) |
| Era 1 Low Contention | Current U.S.-style system (0.766) | Default pass + adaptive strategy bundle (0.992) | Current U.S.-style system (0.000) |
| Era 2 Normal Contention | Current U.S.-style system (0.788) | Default pass + adaptive strategy bundle (0.987) | Current U.S.-style system (0.000) |
| Era 3 Polarizing | Current U.S.-style system (0.796) | Default pass + adaptive strategy bundle (0.975) | Current U.S.-style system (0.000) |
| Era 4 High Contention | Current U.S.-style system (0.797) | Default pass + adaptive strategy bundle (0.957) | Current U.S.-style system (0.000) |
| Era 5 Capture Contention | Current U.S.-style system (0.789) | Default pass + adaptive strategy bundle (0.940) | Current U.S.-style system (0.000) |
| Era 6 Crisis | Default pass + affected-group sponsor gate (0.808) | Default pass + adaptive strategy bundle (0.921) | Current U.S.-style system (0.000) |

## Interpretation

- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.
- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.
- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.
- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.
- Timeline scenarios are stylized stress paths, not historical calibration. They increase polarization, party loyalty, lobbying pressure, and proposal pressure while reducing compromise culture and constituency responsiveness.
- The timeline comparison should be read as a degradation test: institutions that preserve compromise and productivity under later-era assumptions are more robust than systems that only work in low-contention settings.

## Reproduction

```sh
make campaign
```
