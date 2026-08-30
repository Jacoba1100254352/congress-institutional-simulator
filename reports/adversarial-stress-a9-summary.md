# A9 Mixed-Adversary Portfolio Stress Summary

Status: `partial_a9_executable_pilot`.

A9 executable pilot only. Each row pairs the same generated world, target bill, status quo, and vote-random seed across a no-attack baseline, a fixed-total-budget mixed portfolio, full-budget single-attack controls, and single-action controls at the mixed allocation. The three portfolios implement the combinations specified in the experiment plan: A1+A2, A3+A4, and A5+A6+A8. Interaction coefficients, resource conversion, review capacity, and recovery behavior are synthetic stress assumptions, not empirical coordination rates, not a general mechanism ranking, and not evidence for real-world institutional adoption.

- Adversary: A9 mixed adversary portfolio
- Same-world, same-bill, same-status-quo, same-vote-seed runs: 5
- Legislators: 101
- Base bills per run: 60
- Portfolio families: 3
- Joint budgets: 4, 8, and 12 exact attack units
- Information levels: medium and high
- Summary cells: 18
- Trace rows: 5400
- Trace artifact: `reports/adversarial-failure-traces-a9.jsonl`
- Success metric: mixed adverse failure with no adverse failure in any full-budget constituent control
- Interaction metric: mixed degradation minus the strongest full-budget single degradation
- Superadditive metric: mixed degradation minus the sum of allocated-component single degradations

| Portfolio | Components | Information | Budget | Rows | Mixed-only success | Mixed failure | Any single failure | Mixed dominates | Median mixed degradation | Median strongest single | Median interaction | Worst interaction | Superadditive rate | Correction failure | Mean admin burden |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| clone-decoy-poison-pill | A1+A2 | medium | 4 | 300 | 0.060000 | 0.610000 | 0.613333 | 0.113333 | 0.032259 | 0.053084 | -0.006480 | 0.132149 | 0.630000 | 0.000000 | 0.018633 |
| clone-decoy-poison-pill | A1+A2 | medium | 8 | 300 | 0.046667 | 0.393333 | 0.423333 | 0.103333 | 0.000000 | 0.000000 | 0.000000 | 0.240014 | 0.243333 | 0.000000 | 0.021320 |
| clone-decoy-poison-pill | A1+A2 | medium | 12 | 300 | 0.013333 | 0.326667 | 0.353333 | 0.023333 | 0.000000 | 0.000000 | 0.000000 | 0.470034 | 0.060000 | 0.000000 | 0.021320 |
| clone-decoy-poison-pill | A1+A2 | high | 4 | 300 | 0.056667 | 0.580000 | 0.600000 | 0.080000 | 0.032259 | 0.052607 | -0.003105 | 0.078576 | 0.600000 | 0.000000 | 0.017247 |
| clone-decoy-poison-pill | A1+A2 | high | 8 | 300 | 0.043333 | 0.383333 | 0.386667 | 0.093333 | 0.000000 | 0.000000 | 0.000000 | 0.327152 | 0.226667 | 0.000000 | 0.020973 |
| clone-decoy-poison-pill | A1+A2 | high | 12 | 300 | 0.003333 | 0.283333 | 0.323333 | 0.013333 | 0.000000 | 0.000000 | 0.000000 | 0.231633 | 0.053333 | 0.000000 | 0.019500 |
| astroturf-harm-claims | A3+A4 | medium | 4 | 300 | 0.013333 | 0.020000 | 0.006667 | 0.013333 | 0.000000 | 0.000000 | 0.000000 | 0.535448 | 0.003333 | 0.020000 | 0.132850 |
| astroturf-harm-claims | A3+A4 | medium | 8 | 300 | 0.003333 | 0.010000 | 0.286667 | 0.003333 | 0.000000 | 0.000000 | 0.000000 | 0.094151 | 0.003333 | 0.010000 | 0.311933 |
| astroturf-harm-claims | A3+A4 | medium | 12 | 300 | 0.016667 | 0.063333 | 0.320000 | 0.020000 | 0.000000 | 0.000000 | 0.000000 | 0.229262 | 0.020000 | 0.063333 | 0.488917 |
| astroturf-harm-claims | A3+A4 | high | 4 | 300 | 0.026667 | 0.036667 | 0.053333 | 0.026667 | 0.000000 | 0.000000 | 0.000000 | 0.565127 | 0.010000 | 0.033333 | 0.134817 |
| astroturf-harm-claims | A3+A4 | high | 8 | 300 | 0.013333 | 0.070000 | 0.310000 | 0.013333 | 0.000000 | 0.000000 | 0.000000 | 0.384906 | 0.020000 | 0.070000 | 0.386333 |
| astroturf-harm-claims | A3+A4 | high | 12 | 300 | 0.010000 | 0.046667 | 0.316667 | 0.013333 | 0.000000 | 0.000000 | 0.000000 | 0.097386 | 0.016667 | 0.046667 | 0.491283 |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 4 | 300 | 0.000000 | 0.523333 | 0.696667 | 0.000000 | 0.313925 | 0.480337 | 0.000000 | 0.000000 | 0.003333 | 0.523333 | 5.935339 |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 8 | 300 | 0.003333 | 0.603333 | 0.686667 | 0.003333 | 0.417420 | 0.490471 | 0.000000 | 0.484727 | 0.003333 | 0.603333 | 12.103015 |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 12 | 300 | 0.010000 | 0.616667 | 0.700000 | 0.010000 | 0.442617 | 0.494451 | 0.000000 | 0.567683 | 0.013333 | 0.616667 | 18.490519 |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 4 | 300 | 0.003333 | 0.506667 | 0.636667 | 0.003333 | 0.246016 | 0.468456 | 0.000000 | 0.618611 | 0.010000 | 0.506667 | 7.445494 |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 8 | 300 | 0.006667 | 0.626667 | 0.713333 | 0.006667 | 0.449190 | 0.496467 | 0.000000 | 0.648335 | 0.010000 | 0.626667 | 14.350259 |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 12 | 300 | 0.000000 | 0.646667 | 0.720000 | 0.000000 | 0.472987 | 0.497179 | 0.000000 | 0.000000 | 0.010000 | 0.646667 | 21.498493 |

Gate status: this completes bounded executable coverage for A1-A9 and supplies the required mixed-only comparison design. A separate fixed-specification 30-base-seed replication is available in `reports/adversarial-replication-a9-summary.md`. The robustness breakout remains below manuscript gate until A1-A8 seed replication, broader mechanism and alternative A9 specification sweeps, temporal or substantive correction, and external validation are complete.
