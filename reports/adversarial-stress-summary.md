# Adversarial Stress Summary

Status: `partial_a1_executable_pilot`.

A1 executable pilot only. Rows use same generated worlds and bill ids for baseline and attacked policy-tournament cells with synthetic clone/decoy budgets. This is not an empirical attack-rate estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A1 clone/decoy proposer
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 3600
- Trace artifact: `reports/adversarial-failure-traces.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | Median benefit loss | Worst benefit loss | Median support loss | Worst support loss | Enactment loss rate | Low-support added | Mean admin cost added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| medium | 1 | 600 | 0.433333 | 0.000000 | 0.096515 | 0.000000 | 0.278119 | 0.133333 | 0.001667 | 0.003667 |
| medium | 3 | 600 | 0.493333 | 0.000000 | 0.096515 | 0.000000 | 0.278119 | 0.170000 | 0.000000 | 0.152967 |
| medium | 6 | 600 | 0.503333 | 0.000716 | 0.123122 | 0.000000 | 0.278119 | 0.211667 | 0.000000 | 0.305333 |
| high | 1 | 600 | 0.451667 | 0.000000 | 0.096515 | 0.000000 | 0.278119 | 0.173333 | 0.001667 | -0.054633 |
| high | 3 | 600 | 0.506667 | 0.000000 | 0.115622 | 0.011712 | 0.278119 | 0.241667 | 0.000000 | 0.050267 |
| high | 6 | 600 | 0.505000 | 0.020941 | 0.168122 | 0.101543 | 0.362965 | 0.325000 | 0.000000 | 0.026067 |

Gate status: this moves A1 beyond schema-only planning, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader mechanism coverage, multi-seed replication, and external validation remain incomplete.
