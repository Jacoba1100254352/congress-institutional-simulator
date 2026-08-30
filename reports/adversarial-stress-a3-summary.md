# A3 Public-Input Adversarial Stress Summary

Status: `partial_a3_executable_pilot`.

A3 executable pilot only. Rows use same generated worlds and bill ids for benign public-input and manipulated objection/panel cells with synthetic public-attention budgets. This is not an empirical astroturf, public-comment, or panel-manipulation frequency estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A3 public-input manipulator
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 1800
- Trace artifact: `reports/adversarial-failure-traces-a3.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | Median distortion added | Worst distortion added | Median signal movement added | False-positive block | False-negative clearance | Low-support enactment added | Mean admin burden added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| low | 1 | 300 | 0.670000 | -0.060000 | 0.215482 | 0.096500 | 0.100000 | 0.030000 | 0.016667 | 0.233300 |
| low | 3 | 300 | 1.000000 | -0.146371 | 0.293071 | 0.144500 | 0.170000 | 0.013333 | 0.046667 | 0.554600 |
| low | 6 | 300 | 1.000000 | -0.138758 | 0.318752 | 0.216500 | 0.130000 | 0.010000 | 0.050000 | 0.822900 |
| medium | 1 | 300 | 0.950000 | -0.008830 | 0.313039 | 0.134000 | 0.103333 | 0.043333 | 0.023333 | 0.335200 |
| medium | 3 | 300 | 1.000000 | -0.021792 | 0.420069 | 0.182000 | 0.150000 | 0.026667 | 0.053333 | 0.652600 |
| medium | 6 | 300 | 1.000000 | -0.008301 | 0.447036 | 0.254000 | 0.093333 | 0.033333 | 0.073333 | 0.994200 |

Gate status: this moves A3 beyond aggregate pilot mapping, but the robustness breakout remains below manuscript gate because A7-A9 executable sweeps, recovery/correction metrics, broader mechanism coverage, and seed sensitivity remain incomplete.
