# A8 Public-Support Distortion Adversarial Stress Summary

Status: `partial_a8_executable_pilot`.

A8 executable pilot only. Rows pair the same generated world, bill, status quo, formal process, and vote-random stream while an outside campaign changes only the observable public-support and salience signal plus traced campaign/attention spend. Generated support, public benefit, affected-group support, concentrated harm, and private gain remain latent evaluation values. The signal-reliant and constituent-verified paths use no objection window or citizen panel, separating this pilot from A3 formal public-input manipulation. Signal shifts and verification strengths are synthetic assumptions, not empirical campaign effects or district-opinion estimates, not a full A1-A9 sweep, and not evidence for real-world institutional ranking.

- Adversary: A8 public-support distortion actor
- Same-world, same-bill, same-status-quo, same-vote-random runs: 5
- Legislators: 101
- Base bills per run: 60
- Mechanism paths: signal-reliant majority; constituent-verified majority
- Budget/information cells per path: 9
- Trace rows: 5400
- Trace artifact: `reports/adversarial-failure-traces-a8.jsonl`
- A3 boundary: no objection window or citizen panel is used in either A8 path
- Correction metric: same-case signal attenuation by constituent verification, not post-enactment recovery

| Mechanism | Information | Budget | Rows | Success | Decision failure added | Median residual distortion | Worst support error added | Mean correction share | False consensus | False opposition | Low-support enactment | Popular failure |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| signal_reliant_majority | low | 1 | 300 | 1.000000 | 0.036667 | 0.053000 | 0.053000 | 0.000000 | 0.046667 | 0.033333 | 0.023333 | 0.013333 |
| signal_reliant_majority | low | 3 | 300 | 1.000000 | 0.066667 | 0.089000 | 0.089000 | 0.000000 | 0.100000 | 0.060000 | 0.033333 | 0.033333 |
| signal_reliant_majority | low | 6 | 300 | 1.000000 | 0.103333 | 0.143000 | 0.143000 | 0.000000 | 0.203333 | 0.136667 | 0.060000 | 0.043333 |
| signal_reliant_majority | medium | 1 | 300 | 0.993333 | 0.050000 | 0.078000 | 0.078000 | 0.000000 | 0.040000 | 0.013333 | 0.010000 | 0.003333 |
| signal_reliant_majority | medium | 3 | 300 | 0.993333 | 0.060000 | 0.114000 | 0.114000 | 0.000000 | 0.056667 | 0.020000 | 0.023333 | 0.003333 |
| signal_reliant_majority | medium | 6 | 300 | 0.993333 | 0.080000 | 0.168000 | 0.168000 | 0.000000 | 0.096667 | 0.026667 | 0.023333 | 0.003333 |
| signal_reliant_majority | high | 1 | 300 | 0.986667 | 0.076667 | 0.103000 | 0.103000 | 0.000000 | 0.063333 | 0.016667 | 0.030000 | 0.003333 |
| signal_reliant_majority | high | 3 | 300 | 0.986667 | 0.090000 | 0.139000 | 0.139000 | 0.000000 | 0.103333 | 0.023333 | 0.033333 | 0.010000 |
| signal_reliant_majority | high | 6 | 300 | 0.986667 | 0.090000 | 0.193000 | 0.193000 | 0.000000 | 0.166667 | 0.026667 | 0.040000 | 0.003333 |
| constituent_verified_majority | low | 1 | 300 | 0.003333 | 0.003333 | 0.015900 | 0.015900 | 0.700000 | 0.030000 | 0.040000 | 0.003333 | 0.000000 |
| constituent_verified_majority | low | 3 | 300 | 0.030000 | 0.030000 | 0.026700 | 0.026700 | 0.700000 | 0.050000 | 0.060000 | 0.013333 | 0.016667 |
| constituent_verified_majority | low | 6 | 300 | 0.953333 | 0.026667 | 0.042900 | 0.042900 | 0.700000 | 0.096667 | 0.100000 | 0.013333 | 0.013333 |
| constituent_verified_majority | medium | 1 | 300 | 0.020000 | 0.020000 | 0.023400 | 0.023400 | 0.700000 | 0.013333 | 0.010000 | 0.000000 | 0.006667 |
| constituent_verified_majority | medium | 3 | 300 | 0.056667 | 0.056667 | 0.034200 | 0.034200 | 0.700000 | 0.013333 | 0.023333 | 0.013333 | 0.000000 |
| constituent_verified_majority | medium | 6 | 300 | 0.300000 | 0.053333 | 0.050400 | 0.050400 | 0.700000 | 0.030000 | 0.030000 | 0.003333 | 0.003333 |
| constituent_verified_majority | high | 1 | 300 | 0.020000 | 0.020000 | 0.030900 | 0.030900 | 0.695333 | 0.016667 | 0.006667 | 0.006667 | 0.000000 |
| constituent_verified_majority | high | 3 | 300 | 0.276667 | 0.036667 | 0.041700 | 0.041700 | 0.695333 | 0.033333 | 0.013333 | 0.006667 | 0.000000 |
| constituent_verified_majority | high | 6 | 300 | 0.280000 | 0.043333 | 0.057900 | 0.057900 | 0.695333 | 0.060000 | 0.013333 | 0.010000 | 0.000000 |

Gate status: this supplies the first bounded A8 direct signal-distortion and same-case correction pilot, but the robustness breakout remains below manuscript gate because broad mechanism coverage, multi-seed replication, temporal recovery/correction, and external validation remain incomplete.
