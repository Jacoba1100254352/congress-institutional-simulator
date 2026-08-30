# A7 Administrative-Overload Adversarial Stress Summary

Status: `partial_a7_executable_pilot`.

A7 executable pilot only. Rows pair the same generated worlds and target bill ids under a portfolio-hybrid safeguard path with a shared synthetic review-capacity budget. The attack injects fixed-budget proposal, objection, harm-claim, panel-noise, camouflage, and review demand before each target; overflow uses an explicitly traced ordinary-majority fallback. Capacity, backlog, and recovery-cycle values are modeling assumptions, not empirical agency or congressional staffing estimates, not a full A1-A9 sweep, and not evidence for real-world institutional ranking.

- Adversary: A7 administrative overload coalition
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Capacity / recovery units per cycle: 18.000000 / 3.600000
- Trace rows: 1800
- Trace artifact: `reports/adversarial-failure-traces-a7.jsonl`
- Recovery metric: no-case cycles until queue clearance and defended-path readiness, capped at 240 cycles

| Information | Budget | Trace rows | Success | Saturation | Overflow fallback | Median queue added | Worst queue added | Risk-control failure added | Median risk degradation | Mean admin burden added | Recovery rate | Mean recovery cycles |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| medium | 1 | 300 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.103333 | 0.000000 | 1.440899 | 0.000000 | 0.000000 |
| medium | 3 | 300 | 0.900000 | 0.900000 | 0.900000 | 54.753971 | 122.683099 | 0.393333 | 0.000000 | 10.097202 | 1.000000 | 38.000000 |
| medium | 6 | 300 | 0.966667 | 0.966667 | 0.966667 | 185.014224 | 378.697017 | 0.420000 | 0.000000 | 27.368182 | 1.000000 | 109.000000 |
| high | 1 | 300 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.130000 | 0.000000 | 1.700516 | 0.000000 | 0.000000 |
| high | 3 | 300 | 0.933333 | 0.933333 | 0.930000 | 78.227475 | 168.799979 | 0.410000 | 0.000000 | 13.202838 | 1.000000 | 51.000000 |
| high | 6 | 300 | 0.983333 | 0.983333 | 0.983333 | 232.495803 | 472.092191 | 0.420000 | 0.000000 | 33.673276 | 1.000000 | 135.000000 |

Gate status: this supplies the first bounded A7 capacity-saturation and recovery pilot, but the robustness breakout remains below manuscript gate because broader mechanism coverage, multi-seed sensitivity, substantive correction, and external validation remain incomplete.
