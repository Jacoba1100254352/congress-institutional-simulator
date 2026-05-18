# Mechanism Ablation Analysis

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 64
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 15
- experiment cases: 27

## Headline Findings

- This focused campaign does not include the open burden-shifting baseline, so relative headline deltas are reported in the diagnostic sections below.
- Highest average welfare in this campaign came from Stylized U.S.-like conventional benchmark at 0.680.
- Highest productivity came from Unicameral majority + pairwise alternatives at 0.557, while highest revision moderation came from Unicameral majority + pairwise alternatives at 0.508.
- Highest directional score, where lower-better risk metrics are inverted, came from Unicameral majority + pairwise alternatives at 0.715.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, revision moderation, public alignment, and legitimacy. Risk control inverts chamber low-support passage, low-public-support enactment, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Low-public-support enactment ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Affected-group consent + majority | 0.664 | 0.565 | 0.834 | 0.936 | 0.319 | 25.841 | 80.381 | 0.605 | 0.000 | 0.206 | 0.064 | 0.087 | 0.541 | 0.113 | 0.296 | 0.252 | 0.000 | 0.000 | 0.000 | 0.187 | 0.611 | 0.000 | 0.912 |
| Majority + anti-capture bundle | 0.677 | 0.577 | 0.880 | 0.935 | 0.318 | 26.624 | 83.378 | 0.654 | 0.000 | 0.152 | 0.065 | 0.124 | 0.536 | 0.119 | 0.302 | 0.137 | 0.102 | 0.552 | 0.000 | 0.000 | 0.700 | 0.000 | 0.934 |
| Compensation amendments + majority | 0.664 | 0.563 | 0.835 | 0.930 | 0.327 | 26.449 | 88.889 | 0.605 | 0.000 | 0.219 | 0.070 | 0.095 | 0.534 | 0.115 | 0.294 | 0.257 | 0.000 | 0.000 | 0.000 | 0.169 | 0.614 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.651 | 0.641 | 0.927 | 0.985 | 0.052 | 4.212 | 19.546 | 0.680 | 0.000 | 0.014 | 0.015 | 0.075 | 0.666 | 0.011 | 0.164 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 | 0.159 | 0.000 | 0.219 |
| Harm-weighted double majority | 0.663 | 0.570 | 0.874 | 0.930 | 0.278 | 23.010 | 88.889 | 0.619 | 0.000 | 0.210 | 0.070 | 0.117 | 0.529 | 0.092 | 0.270 | 0.251 | 0.000 | 0.000 | 0.000 | 0.000 | 0.560 | 0.000 | 1.000 |
| Active-law registry + majority review | 0.657 | 0.554 | 0.830 | 0.886 | 0.355 | 29.120 | 88.889 | 0.601 | 0.000 | 0.253 | 0.114 | 0.141 | 0.503 | 0.203 | 0.348 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.640 | 0.000 | 1.000 |
| Multidimensional package bargaining + majority | 0.641 | 0.557 | 0.832 | 0.825 | 0.349 | 28.166 | 88.889 | 0.586 | 0.000 | 0.222 | 0.175 | 0.106 | 0.523 | 0.127 | 0.315 | 0.264 | 0.000 | 0.000 | 0.378 | 0.378 | 0.641 | 0.000 | 1.000 |
| Package bargaining + majority | 0.656 | 0.560 | 0.838 | 0.890 | 0.336 | 27.108 | 88.889 | 0.605 | 0.000 | 0.226 | 0.110 | 0.121 | 0.518 | 0.121 | 0.301 | 0.260 | 0.000 | 0.000 | 0.286 | 0.286 | 0.624 | 0.000 | 1.000 |
| Majority + public-interest screen | 0.658 | 0.567 | 0.866 | 0.940 | 0.257 | 21.601 | 76.765 | 0.630 | 0.000 | 0.195 | 0.060 | 0.124 | 0.530 | 0.096 | 0.296 | 0.228 | 0.000 | 0.000 | 0.000 | 0.000 | 0.507 | 0.000 | 0.861 |
| Risk-routed majority legislature | 0.691 | 0.547 | 0.837 | 0.829 | 0.550 | 45.146 | 88.889 | 0.522 | 0.000 | 0.230 | 0.171 | 0.104 | 0.510 | 0.187 | 0.318 | 0.286 | 0.000 | 0.000 | 0.664 | 0.239 | 0.680 | 0.000 | 1.000 |
| Risk-routed majority without citizen review | 0.693 | 0.547 | 0.836 | 0.837 | 0.551 | 45.163 | 88.889 | 0.522 | 0.000 | 0.231 | 0.163 | 0.104 | 0.510 | 0.187 | 0.318 | 0.286 | 0.000 | 0.000 | 0.664 | 0.239 | 0.673 | 0.000 | 1.000 |
| Unicameral simple majority | 0.666 | 0.561 | 0.848 | 0.930 | 0.327 | 26.463 | 88.889 | 0.612 | 0.000 | 0.218 | 0.070 | 0.133 | 0.517 | 0.116 | 0.295 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 | 0.615 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.715 | 0.658 | 0.936 | 0.711 | 0.557 | 47.843 | 50.141 | 0.638 | 0.000 | 0.002 | 0.289 | 0.058 | 0.637 | 0.005 | 0.004 | 0.229 | 0.000 | 0.000 | 0.576 | 0.000 | 0.782 | 0.000 | 0.576 |
| Unicameral majority + lobby firewall | 0.673 | 0.569 | 0.858 | 0.930 | 0.335 | 27.413 | 88.889 | 0.619 | 0.000 | 0.192 | 0.070 | 0.126 | 0.528 | 0.120 | 0.297 | 0.227 | 0.000 | 0.000 | 0.000 | 0.000 | 0.698 | 0.000 | 1.000 |
| Unicameral majority + mediation | 0.641 | 0.546 | 0.797 | 0.814 | 0.406 | 33.419 | 88.889 | 0.584 | 0.000 | 0.282 | 0.186 | 0.111 | 0.502 | 0.160 | 0.380 | 0.276 | 0.000 | 0.000 | 0.826 | 0.182 | 0.653 | 0.000 | 1.000 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest low-public-support enactment |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.757) | Unicameral majority + pairwise alternatives (0.541) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Polarization | Stylized U.S.-like conventional benchmark (0.738) | Risk-routed majority without citizen review (0.686) | Unicameral majority + pairwise alternatives (0.002) |
| High Polarization | Stylized U.S.-like conventional benchmark (0.767) | Unicameral majority + pairwise alternatives (0.492) | Stylized U.S.-like conventional benchmark (0.000) |
| Low Party Loyalty | Stylized U.S.-like conventional benchmark (0.765) | Unicameral majority + pairwise alternatives (0.546) | Unicameral majority + pairwise alternatives (0.002) |
| High Party Loyalty | Stylized U.S.-like conventional benchmark (0.763) | Unicameral majority + pairwise alternatives (0.547) | Unicameral majority + pairwise alternatives (0.002) |
| Low Revision-Moderation Culture | Stylized U.S.-like conventional benchmark (0.757) | Unicameral majority + pairwise alternatives (0.533) | Stylized U.S.-like conventional benchmark (0.000) |
| High Revision-Moderation Culture | Stylized U.S.-like conventional benchmark (0.735) | Risk-routed majority legislature (0.583) | Unicameral majority + pairwise alternatives (0.004) |
| Low Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.763) | Unicameral majority + pairwise alternatives (0.571) | Unicameral majority + pairwise alternatives (0.002) |
| High Lobbying Pressure | Stylized U.S.-like conventional benchmark (0.755) | Unicameral majority + pairwise alternatives (0.487) | Unicameral majority + pairwise alternatives (0.005) |
| Weak Constituency Pressure | Stylized U.S.-like conventional benchmark (0.755) | Unicameral majority + pairwise alternatives (0.530) | Unicameral majority + pairwise alternatives (0.003) |
| Two-Party System | Stylized U.S.-like conventional benchmark (0.750) | Unicameral majority + pairwise alternatives (0.551) | Stylized U.S.-like conventional benchmark (0.000) |
| Multi-Party System | Stylized U.S.-like conventional benchmark (0.753) | Unicameral majority + pairwise alternatives (0.540) | Unicameral majority + pairwise alternatives (0.002) |
| High Proposal Pressure | Stylized U.S.-like conventional benchmark (0.752) | Unicameral majority + pairwise alternatives (0.539) | Unicameral majority + pairwise alternatives (0.001) |
| Extreme Proposal Pressure | Stylized U.S.-like conventional benchmark (0.747) | Unicameral majority + pairwise alternatives (0.540) | Unicameral majority + pairwise alternatives (0.000) |
| Lobby-Fueled Flooding | Stylized U.S.-like conventional benchmark (0.733) | Unicameral majority + pairwise alternatives (0.461) | Unicameral majority + pairwise alternatives (0.001) |
| Low-Revision-Moderation Flooding | Stylized U.S.-like conventional benchmark (0.749) | Unicameral majority + pairwise alternatives (0.492) | Unicameral majority + pairwise alternatives (0.001) |
| Capture Crisis | Stylized U.S.-like conventional benchmark (0.707) | Unicameral majority + pairwise alternatives (0.402) | Unicameral majority + pairwise alternatives (0.001) |
| Popular Anti-Lobbying Push | Stylized U.S.-like conventional benchmark (0.766) | Unicameral majority + pairwise alternatives (0.547) | Unicameral majority + pairwise alternatives (0.001) |
| Adversarial High-Benefit Extreme Reform | Unicameral majority + pairwise alternatives (0.821) | Unicameral majority + pairwise alternatives (0.645) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Popular Harmful Bill | Unicameral majority + pairwise alternatives (0.325) | Risk-routed majority legislature (0.983) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Moderate Capture | Unicameral majority + pairwise alternatives (0.380) | Risk-routed majority without citizen review (0.987) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Delayed-Benefit Reform | Unicameral majority + pairwise alternatives (0.811) | Risk-routed majority without citizen review (0.711) | Unicameral majority + pairwise alternatives (0.003) |
| Adversarial Concentrated Rights Harm | Majority + anti-capture bundle (0.518) | Risk-routed majority without citizen review (0.765) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Anti-Lobbying Backlash | Majority + anti-capture bundle (0.700) | Majority + anti-capture bundle (0.541) | Unicameral majority + pairwise alternatives (0.003) |
| Adversarial Revision Dilution | Unicameral majority + pairwise alternatives (0.864) | Risk-routed majority legislature (0.555) | Stylized U.S.-like conventional benchmark (0.000) |
| Adversarial Lobby Information | Unicameral majority + pairwise alternatives (0.779) | Risk-routed majority legislature (0.877) | Unicameral majority + pairwise alternatives (0.000) |
| Adversarial Public Opinion Error | Majority + anti-capture bundle (0.540) | Risk-routed majority legislature (0.725) | Stylized U.S.-like conventional benchmark (0.000) |

## Interpretation

- Future model extensions should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms because agenda screening is central to burden-shifting tradeoffs.

## Reproduction

```sh
make campaign
```
