# A5 Proposal-Flooding Adversarial Stress Summary

Status: `partial_a5_executable_pilot`.

A5 executable pilot only. Rows use same generated worlds and original bill ids for a fixed-capacity agenda-lottery majority baseline and an attacked agenda pool with synthetic flood proposals. This is not an empirical bill-volume, agenda-control, or lobbying-support estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A5 proposal flooder
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 1800
- Trace artifact: `reports/adversarial-failure-traces-a5.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | High-benefit crowdout | High-benefit blockage | Low-support flood enacted/run | Flood floor slots | Flood slot share | Mean proposal load added | Mean admin burden added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| low | 1 | 300 | 1.000000 | 0.293333 | 0.003333 | 1.200000 | 6.200000 | 0.221429 | 20.000000 | 0.408000 |
| low | 3 | 300 | 1.000000 | 0.330000 | 0.013333 | 2.600000 | 12.400000 | 0.442857 | 60.000000 | 0.976000 |
| low | 6 | 300 | 1.000000 | 0.366667 | 0.030000 | 1.600000 | 17.000000 | 0.607143 | 120.000000 | 1.640000 |
| medium | 1 | 300 | 1.000000 | 0.293333 | 0.003333 | 2.600000 | 6.200000 | 0.221429 | 20.000000 | 0.541000 |
| medium | 3 | 300 | 1.000000 | 0.326667 | 0.013333 | 4.400000 | 12.200000 | 0.435714 | 60.000000 | 1.271000 |
| medium | 6 | 300 | 1.000000 | 0.356667 | 0.030000 | 8.400000 | 16.800000 | 0.600000 | 120.000000 | 2.124000 |

Gate status: this moves A5 beyond aggregate proposal-flooding mapping, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader agenda and review mechanisms, multi-seed replication, and external agenda-load validation remain incomplete.
