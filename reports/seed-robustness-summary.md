# Seed Robustness Summary

Deterministic multi-seed sweep for all v21-paper scenarios.
The main paper table still reports sensitivity intervals across broad and adversarial assumption cases; this report checks whether paper-scenario relationships are stable across independent base seeds.

- Seeds: 20260428, 20260429, 20260430, 20260501, 20260502
- Runs per seed: 24
- Cases summarized: broad and adversarial assumption cases only

| Scenario | Metric | Mean | Min | Max | Range |
| --- | --- | ---: | ---: | ---: | ---: |
| Stylized U.S.-like benchmark | directionalScore | 0.537 | 0.532 | 0.540 | 0.009 |
| Stylized U.S.-like benchmark | productivity | 0.048 | 0.047 | 0.049 | 0.002 |
| Stylized U.S.-like benchmark | compromise | 0.376 | 0.370 | 0.381 | 0.010 |
| Stylized U.S.-like benchmark | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Stylized U.S.-like benchmark | welfare | 0.688 | 0.664 | 0.712 | 0.049 |
| Stylized U.S.-like benchmark | riskControl | 0.924 | 0.922 | 0.925 | 0.003 |
| Unicameral simple majority | directionalScore | 0.581 | 0.580 | 0.581 | 0.001 |
| Unicameral simple majority | productivity | 0.321 | 0.320 | 0.321 | 0.002 |
| Unicameral simple majority | compromise | 0.246 | 0.244 | 0.248 | 0.004 |
| Unicameral simple majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Unicameral simple majority | welfare | 0.607 | 0.606 | 0.609 | 0.003 |
| Unicameral simple majority | riskControl | 0.861 | 0.859 | 0.862 | 0.003 |
| Unicameral 60 percent passage | directionalScore | 0.550 | 0.545 | 0.553 | 0.008 |
| Unicameral 60 percent passage | productivity | 0.132 | 0.130 | 0.133 | 0.003 |
| Unicameral 60 percent passage | compromise | 0.356 | 0.353 | 0.361 | 0.008 |
| Unicameral 60 percent passage | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Unicameral 60 percent passage | welfare | 0.651 | 0.628 | 0.666 | 0.038 |
| Unicameral 60 percent passage | riskControl | 0.900 | 0.898 | 0.902 | 0.004 |
| Bicameral simple majority | directionalScore | 0.564 | 0.564 | 0.564 | 0.000 |
| Bicameral simple majority | productivity | 0.223 | 0.221 | 0.227 | 0.005 |
| Bicameral simple majority | compromise | 0.287 | 0.285 | 0.288 | 0.003 |
| Bicameral simple majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Bicameral simple majority | welfare | 0.631 | 0.629 | 0.633 | 0.005 |
| Bicameral simple majority | riskControl | 0.881 | 0.881 | 0.882 | 0.001 |
| Bicameral majority + presidential veto | directionalScore | 0.548 | 0.547 | 0.548 | 0.001 |
| Bicameral majority + presidential veto | productivity | 0.150 | 0.148 | 0.152 | 0.003 |
| Bicameral majority + presidential veto | compromise | 0.311 | 0.307 | 0.319 | 0.013 |
| Bicameral majority + presidential veto | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Bicameral majority + presidential veto | welfare | 0.643 | 0.637 | 0.648 | 0.010 |
| Bicameral majority + presidential veto | riskControl | 0.892 | 0.890 | 0.893 | 0.003 |
| Committee-first regular order | directionalScore | 0.563 | 0.562 | 0.564 | 0.001 |
| Committee-first regular order | productivity | 0.209 | 0.207 | 0.210 | 0.003 |
| Committee-first regular order | compromise | 0.287 | 0.285 | 0.289 | 0.004 |
| Committee-first regular order | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Committee-first regular order | welfare | 0.644 | 0.643 | 0.647 | 0.004 |
| Committee-first regular order | riskControl | 0.889 | 0.888 | 0.889 | 0.001 |
| Parliamentary coalition confidence | directionalScore | 0.568 | 0.567 | 0.568 | 0.001 |
| Parliamentary coalition confidence | productivity | 0.225 | 0.223 | 0.227 | 0.004 |
| Parliamentary coalition confidence | compromise | 0.292 | 0.291 | 0.293 | 0.003 |
| Parliamentary coalition confidence | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Parliamentary coalition confidence | welfare | 0.638 | 0.636 | 0.640 | 0.004 |
| Parliamentary coalition confidence | riskControl | 0.900 | 0.899 | 0.901 | 0.001 |
| Majority pairwise policy tournament | directionalScore | 0.708 | 0.707 | 0.709 | 0.002 |
| Majority pairwise policy tournament | productivity | 0.542 | 0.539 | 0.544 | 0.005 |
| Majority pairwise policy tournament | compromise | 0.505 | 0.499 | 0.517 | 0.018 |
| Majority pairwise policy tournament | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Majority pairwise policy tournament | welfare | 0.627 | 0.626 | 0.628 | 0.002 |
| Majority pairwise policy tournament | riskControl | 0.928 | 0.927 | 0.929 | 0.002 |
| Strategic policy tournament | directionalScore | 0.708 | 0.707 | 0.709 | 0.002 |
| Strategic policy tournament | productivity | 0.542 | 0.541 | 0.545 | 0.004 |
| Strategic policy tournament | compromise | 0.504 | 0.499 | 0.517 | 0.018 |
| Strategic policy tournament | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Strategic policy tournament | welfare | 0.627 | 0.626 | 0.628 | 0.002 |
| Strategic policy tournament | riskControl | 0.928 | 0.927 | 0.929 | 0.002 |
| Citizen assembly threshold gate | directionalScore | 0.570 | 0.569 | 0.571 | 0.001 |
| Citizen assembly threshold gate | productivity | 0.198 | 0.196 | 0.200 | 0.004 |
| Citizen assembly threshold gate | compromise | 0.283 | 0.282 | 0.284 | 0.002 |
| Citizen assembly threshold gate | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Citizen assembly threshold gate | welfare | 0.686 | 0.683 | 0.688 | 0.004 |
| Citizen assembly threshold gate | riskControl | 0.902 | 0.901 | 0.902 | 0.001 |
| Majority + public-interest screen | directionalScore | 0.565 | 0.565 | 0.566 | 0.001 |
| Majority + public-interest screen | productivity | 0.246 | 0.244 | 0.247 | 0.003 |
| Majority + public-interest screen | compromise | 0.249 | 0.245 | 0.252 | 0.007 |
| Majority + public-interest screen | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Majority + public-interest screen | welfare | 0.628 | 0.626 | 0.630 | 0.005 |
| Majority + public-interest screen | riskControl | 0.881 | 0.880 | 0.882 | 0.003 |
| Weighted agenda lottery + majority | directionalScore | 0.544 | 0.543 | 0.544 | 0.001 |
| Weighted agenda lottery + majority | productivity | 0.173 | 0.171 | 0.175 | 0.004 |
| Weighted agenda lottery + majority | compromise | 0.253 | 0.252 | 0.253 | 0.001 |
| Weighted agenda lottery + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Weighted agenda lottery + majority | welfare | 0.630 | 0.629 | 0.632 | 0.002 |
| Weighted agenda lottery + majority | riskControl | 0.886 | 0.885 | 0.888 | 0.003 |
| Quadratic attention budget + majority | directionalScore | 0.569 | 0.568 | 0.570 | 0.002 |
| Quadratic attention budget + majority | productivity | 0.247 | 0.243 | 0.251 | 0.008 |
| Quadratic attention budget + majority | compromise | 0.266 | 0.264 | 0.267 | 0.002 |
| Quadratic attention budget + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Quadratic attention budget + majority | welfare | 0.627 | 0.625 | 0.628 | 0.003 |
| Quadratic attention budget + majority | riskControl | 0.886 | 0.885 | 0.886 | 0.002 |
| Proposal bonds + majority | directionalScore | 0.581 | 0.580 | 0.581 | 0.001 |
| Proposal bonds + majority | productivity | 0.319 | 0.315 | 0.321 | 0.006 |
| Proposal bonds + majority | compromise | 0.247 | 0.245 | 0.249 | 0.004 |
| Proposal bonds + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Proposal bonds + majority | welfare | 0.608 | 0.607 | 0.610 | 0.004 |
| Proposal bonds + majority | riskControl | 0.862 | 0.861 | 0.863 | 0.002 |
| Harm-weighted double majority | directionalScore | 0.577 | 0.576 | 0.578 | 0.002 |
| Harm-weighted double majority | productivity | 0.272 | 0.269 | 0.275 | 0.006 |
| Harm-weighted double majority | compromise | 0.263 | 0.261 | 0.267 | 0.006 |
| Harm-weighted double majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Harm-weighted double majority | welfare | 0.616 | 0.614 | 0.618 | 0.004 |
| Harm-weighted double majority | riskControl | 0.888 | 0.887 | 0.890 | 0.003 |
| Compensation amendments + majority | directionalScore | 0.575 | 0.575 | 0.576 | 0.002 |
| Compensation amendments + majority | productivity | 0.320 | 0.318 | 0.321 | 0.003 |
| Compensation amendments + majority | compromise | 0.247 | 0.245 | 0.249 | 0.004 |
| Compensation amendments + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Compensation amendments + majority | welfare | 0.601 | 0.599 | 0.602 | 0.003 |
| Compensation amendments + majority | riskControl | 0.842 | 0.841 | 0.845 | 0.004 |
| Package bargaining + majority | directionalScore | 0.580 | 0.579 | 0.581 | 0.002 |
| Package bargaining + majority | productivity | 0.330 | 0.327 | 0.333 | 0.006 |
| Package bargaining + majority | compromise | 0.244 | 0.242 | 0.246 | 0.004 |
| Package bargaining + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Package bargaining + majority | welfare | 0.601 | 0.600 | 0.602 | 0.002 |
| Package bargaining + majority | riskControl | 0.850 | 0.849 | 0.852 | 0.002 |
| Active-law registry + majority review | directionalScore | 0.583 | 0.582 | 0.583 | 0.002 |
| Active-law registry + majority review | productivity | 0.345 | 0.343 | 0.347 | 0.003 |
| Active-law registry + majority review | compromise | 0.238 | 0.235 | 0.239 | 0.004 |
| Active-law registry + majority review | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Active-law registry + majority review | welfare | 0.596 | 0.596 | 0.597 | 0.002 |
| Active-law registry + majority review | riskControl | 0.847 | 0.846 | 0.848 | 0.002 |
| Public objection window + majority | directionalScore | 0.571 | 0.570 | 0.572 | 0.002 |
| Public objection window + majority | productivity | 0.231 | 0.229 | 0.232 | 0.003 |
| Public objection window + majority | compromise | 0.285 | 0.284 | 0.287 | 0.003 |
| Public objection window + majority | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Public objection window + majority | welfare | 0.643 | 0.641 | 0.645 | 0.004 |
| Public objection window + majority | riskControl | 0.895 | 0.894 | 0.896 | 0.002 |
| Majority + anti-capture bundle | directionalScore | 0.592 | 0.591 | 0.593 | 0.002 |
| Majority + anti-capture bundle | productivity | 0.308 | 0.304 | 0.311 | 0.007 |
| Majority + anti-capture bundle | compromise | 0.248 | 0.247 | 0.251 | 0.004 |
| Majority + anti-capture bundle | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Majority + anti-capture bundle | welfare | 0.650 | 0.647 | 0.652 | 0.005 |
| Majority + anti-capture bundle | riskControl | 0.890 | 0.889 | 0.890 | 0.001 |
| Risk-routed majority legislature | directionalScore | 0.643 | 0.642 | 0.644 | 0.002 |
| Risk-routed majority legislature | productivity | 0.531 | 0.529 | 0.533 | 0.004 |
| Risk-routed majority legislature | compromise | 0.264 | 0.263 | 0.265 | 0.002 |
| Risk-routed majority legislature | lowSupport | 0.000 | 0.000 | 0.000 | 0.000 |
| Risk-routed majority legislature | welfare | 0.509 | 0.507 | 0.511 | 0.004 |
| Risk-routed majority legislature | riskControl | 0.853 | 0.851 | 0.854 | 0.003 |
| Default pass unless 2/3 block | directionalScore | 0.662 | 0.661 | 0.663 | 0.002 |
| Default pass unless 2/3 block | productivity | 0.866 | 0.864 | 0.868 | 0.005 |
| Default pass unless 2/3 block | compromise | 0.136 | 0.136 | 0.137 | 0.002 |
| Default pass unless 2/3 block | lowSupport | 0.420 | 0.418 | 0.421 | 0.003 |
| Default pass unless 2/3 block | welfare | 0.500 | 0.499 | 0.501 | 0.002 |
| Default pass unless 2/3 block | riskControl | 0.645 | 0.642 | 0.646 | 0.003 |
| Default pass + challenge vouchers | directionalScore | 0.620 | 0.618 | 0.621 | 0.003 |
| Default pass + challenge vouchers | productivity | 0.658 | 0.656 | 0.661 | 0.005 |
| Default pass + challenge vouchers | compromise | 0.160 | 0.159 | 0.162 | 0.003 |
| Default pass + challenge vouchers | lowSupport | 0.352 | 0.348 | 0.356 | 0.009 |
| Default pass + challenge vouchers | welfare | 0.513 | 0.512 | 0.514 | 0.001 |
| Default pass + challenge vouchers | riskControl | 0.714 | 0.711 | 0.716 | 0.005 |
| Default pass + mediation + challenge | directionalScore | 0.684 | 0.683 | 0.686 | 0.003 |
| Default pass + mediation + challenge | productivity | 0.801 | 0.799 | 0.802 | 0.003 |
| Default pass + mediation + challenge | compromise | 0.243 | 0.242 | 0.244 | 0.002 |
| Default pass + mediation + challenge | lowSupport | 0.256 | 0.253 | 0.258 | 0.005 |
| Default pass + mediation + challenge | welfare | 0.460 | 0.459 | 0.461 | 0.002 |
| Default pass + mediation + challenge | riskControl | 0.742 | 0.739 | 0.747 | 0.007 |
