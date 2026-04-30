# Mechanism Ablation Analysis

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 64
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 15
- experiment cases: 24

## Headline Findings

- This focused campaign does not include the open default-pass baseline, so relative headline deltas are reported in the diagnostic sections below.
- Highest average welfare in this campaign came from Stylized U.S.-like conventional benchmark at 0.694.
- Highest productivity came from Unicameral majority + pairwise alternatives at 0.542, while highest compromise came from Unicameral majority + pairwise alternatives at 0.507.
- Highest directional score, where lower-better risk metrics are inverted, came from Unicameral majority + pairwise alternatives at 0.712.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Affected-group consent + majority | 0.663 | 0.566 | 0.836 | 0.937 | 0.313 | 26.314 | 83.205 | 0.602 | 0.000 | 0.195 | 0.063 | 0.084 | 0.548 | 0.111 | 0.296 | 0.253 | 0.000 | 0.000 | 0.000 | 0.195 | 0.625 | 0.000 | 0.905 |
| Majority + anti-capture bundle | 0.676 | 0.578 | 0.883 | 0.935 | 0.308 | 26.963 | 86.500 | 0.649 | 0.000 | 0.152 | 0.065 | 0.121 | 0.544 | 0.116 | 0.304 | 0.137 | 0.101 | 0.553 | 0.000 | 0.000 | 0.732 | 0.000 | 0.929 |
| Compensation amendments + majority | 0.663 | 0.564 | 0.837 | 0.930 | 0.321 | 26.962 | 92.500 | 0.601 | 0.000 | 0.211 | 0.070 | 0.091 | 0.540 | 0.113 | 0.295 | 0.258 | 0.000 | 0.000 | 0.000 | 0.178 | 0.628 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.652 | 0.645 | 0.927 | 0.984 | 0.052 | 4.340 | 20.620 | 0.694 | 0.000 | 0.015 | 0.016 | 0.070 | 0.676 | 0.011 | 0.158 | 0.209 | 0.000 | 0.000 | 0.000 | 0.000 | 0.163 | 0.000 | 0.224 |
| Harm-weighted double majority | 0.662 | 0.571 | 0.877 | 0.930 | 0.271 | 23.400 | 92.500 | 0.615 | 0.000 | 0.198 | 0.070 | 0.115 | 0.536 | 0.089 | 0.269 | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 0.578 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.655 | 0.555 | 0.835 | 0.881 | 0.346 | 29.295 | 92.500 | 0.596 | 0.000 | 0.239 | 0.119 | 0.138 | 0.511 | 0.193 | 0.340 | 0.259 | 0.000 | 0.000 | 0.000 | 0.000 | 0.647 | 0.000 | 1.000 |
| Multidimensional package bargaining + majority | 0.640 | 0.557 | 0.834 | 0.827 | 0.341 | 28.628 | 92.500 | 0.582 | 0.000 | 0.215 | 0.173 | 0.106 | 0.528 | 0.124 | 0.313 | 0.265 | 0.000 | 0.000 | 0.371 | 0.371 | 0.651 | 0.000 | 1.000 |
| Package bargaining + majority | 0.655 | 0.560 | 0.841 | 0.890 | 0.329 | 27.566 | 92.500 | 0.601 | 0.000 | 0.217 | 0.110 | 0.120 | 0.524 | 0.118 | 0.301 | 0.261 | 0.000 | 0.000 | 0.283 | 0.283 | 0.636 | 0.000 | 1.000 |
| Majority + public-interest screen | 0.657 | 0.569 | 0.872 | 0.941 | 0.246 | 21.692 | 79.195 | 0.627 | 0.000 | 0.180 | 0.059 | 0.121 | 0.538 | 0.092 | 0.296 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 | 0.531 | 0.000 | 0.849 |
| Risk-routed majority legislature | 0.686 | 0.545 | 0.841 | 0.829 | 0.529 | 45.395 | 92.500 | 0.509 | 0.000 | 0.232 | 0.171 | 0.104 | 0.511 | 0.179 | 0.317 | 0.291 | 0.000 | 0.000 | 0.657 | 0.239 | 0.674 | 0.000 | 1.000 |
| Risk-routed majority without citizen review | 0.688 | 0.545 | 0.840 | 0.838 | 0.531 | 45.471 | 92.500 | 0.508 | 0.000 | 0.233 | 0.162 | 0.103 | 0.511 | 0.180 | 0.317 | 0.291 | 0.000 | 0.000 | 0.657 | 0.240 | 0.669 | 0.000 | 1.000 |
| Unicameral simple majority | 0.666 | 0.562 | 0.852 | 0.930 | 0.321 | 26.974 | 92.500 | 0.608 | 0.000 | 0.208 | 0.070 | 0.131 | 0.523 | 0.114 | 0.293 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.631 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.712 | 0.655 | 0.937 | 0.715 | 0.542 | 48.783 | 51.318 | 0.628 | 0.000 | 0.002 | 0.285 | 0.058 | 0.640 | 0.005 | 0.004 | 0.229 | 0.000 | 0.000 | 0.563 | 0.000 | 0.798 | 0.000 | 0.563 |
| Unicameral majority + lobby firewall | 0.674 | 0.570 | 0.862 | 0.930 | 0.333 | 28.179 | 92.500 | 0.617 | 0.000 | 0.184 | 0.070 | 0.122 | 0.535 | 0.120 | 0.300 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 | 0.720 | 0.000 | 1.000 |
| Unicameral majority + mediation | 0.639 | 0.545 | 0.799 | 0.815 | 0.398 | 34.049 | 92.500 | 0.576 | 0.000 | 0.274 | 0.185 | 0.109 | 0.507 | 0.156 | 0.374 | 0.278 | 0.000 | 0.000 | 0.825 | 0.190 | 0.665 | 0.000 | 1.000 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest weak public-mandate passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.757) | Unicameral majority + pairwise alternatives (0.541) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.738) | Risk-routed majority without citizen review (0.686) | Unicameral majority + pairwise alternatives (0.002) |
| High Polarization | Stylized U.S.-like conventional benchmark (0.767) | Unicameral majority + pairwise alternatives (0.492) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.765) | Unicameral majority + pairwise alternatives (0.546) | Unicameral majority + pairwise alternatives (0.002) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.763) | Unicameral majority + pairwise alternatives (0.547) | Unicameral majority + pairwise alternatives (0.002) |
| Low Compromise Culture | Stylized U.S.-like conventional benchmark (0.757) | Unicameral majority + pairwise alternatives (0.533) | Stylized U.S.-like conventional benchmark (0.000) |
| High Compromise Culture | Stylized U.S.-like conventional benchmark (0.735) | Risk-routed majority legislature (0.583) | Unicameral majority + pairwise alternatives (0.004) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Unicameral majority + pairwise alternatives (0.571) | Unicameral majority + pairwise alternatives (0.002) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.755) | Unicameral majority + pairwise alternatives (0.487) | Unicameral majority + pairwise alternatives (0.005) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.755) | Unicameral majority + pairwise alternatives (0.530) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.750) | Unicameral majority + pairwise alternatives (0.551) | Stylized U.S.-like conventional benchmark (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.753) | Unicameral majority + pairwise alternatives (0.540) | Unicameral majority + pairwise alternatives (0.002) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.752) | Unicameral majority + pairwise alternatives (0.539) | Unicameral majority + pairwise alternatives (0.001) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.747) | Unicameral majority + pairwise alternatives (0.540) | Unicameral majority + pairwise alternatives (0.000) |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark (0.733) | Unicameral majority + pairwise alternatives (0.461) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Compromise Flooding | Stylized U.S.-like conventional benchmark (0.749) | Unicameral majority + pairwise alternatives (0.492) | Unicameral majority + pairwise alternatives (0.001) |
| Capture Crisis | Stylized U.S.-like conventional benchmark (0.707) | Unicameral majority + pairwise alternatives (0.402) | Unicameral majority + pairwise alternatives (0.001) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.766) | Unicameral majority + pairwise alternatives (0.547) | Unicameral majority + pairwise alternatives (0.001) |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives (0.821) | Unicameral majority + pairwise alternatives (0.645) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives (0.325) | Risk-routed majority legislature (0.983) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives (0.380) | Risk-routed majority without citizen review (0.987) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives (0.811) | Risk-routed majority without citizen review (0.711) | Unicameral majority + pairwise alternatives (0.003) |
| Adversarial Concentrated Rights Harm | Majority + anti-capture bundle (0.518) | Risk-routed majority without citizen review (0.765) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Majority + anti-capture bundle (0.700) | Majority + anti-capture bundle (0.541) | Unicameral majority + pairwise alternatives (0.003) |

## Interpretation

- The next model extension should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms, because agenda screening is now the central default-pass tradeoff.

## Reproduction

```sh
make campaign
```
