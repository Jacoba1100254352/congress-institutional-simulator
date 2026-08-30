# A2 Poison-Pill Adversarial Stress Summary

Status: `partial_a2_executable_pilot`.

A2 executable pilot only. Rows use same generated worlds and bill ids for benign amendment and poison-pill/sequencing attack cells with synthetic amendment-slot budgets. This is not an empirical rider frequency estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A2 poison-pill or sequencing actor
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 1800
- Trace artifact: `reports/adversarial-failure-traces-a2.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | Median benefit loss | Worst benefit loss | Median support loss | Harm added | High-benefit blockage | Harmful rider passage | Overload added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| medium | 1 | 300 | 0.146667 | 0.000000 | 0.052666 | 0.000000 | 0.000000 | 0.066667 | 0.003333 | -0.000441 |
| medium | 3 | 300 | 0.380000 | 0.000132 | 0.176615 | 0.000210 | 0.000000 | 0.123333 | 0.143333 | 0.021142 |
| medium | 6 | 300 | 0.576667 | 0.007457 | 0.295854 | 0.103984 | 0.000067 | 0.253333 | 0.180000 | 0.039007 |
| high | 1 | 300 | 0.196667 | 0.000000 | 0.056544 | 0.000000 | 0.000000 | 0.066667 | 0.006667 | -0.001661 |
| high | 3 | 300 | 0.516667 | 0.003301 | 0.176614 | 0.019409 | 0.000000 | 0.196667 | 0.160000 | 0.025263 |
| high | 6 | 300 | 0.663333 | 0.016452 | 0.350144 | 0.190593 | 0.038334 | 0.333333 | 0.130000 | 0.065794 |

Gate status: this moves A2 beyond unsupported planning, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader mechanism coverage, multi-seed replication, and external validation remain incomplete.
