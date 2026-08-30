# A4 Bad-Faith Harm-Claim Adversarial Stress Summary

Status: `partial_a4_executable_pilot`.

A4 executable pilot only. Rows use same generated worlds and bill ids for targeted synthetic harm-claim cases under benign and bad-faith claim signals with medium-information harm-claim budgets. This is not an empirical claim-filing, litigation, or legal-review frequency estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A4 bad-faith harm claimant
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 900
- Trace artifact: `reports/adversarial-failure-traces-a4.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | False-positive block | False-negative clearance | Median FP burden added | Worst FP burden added | Mean harm passage added | Mean admin burden added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| medium | 1 | 300 | 0.603333 | 0.150000 | 0.336667 | 0.000000 | 0.460000 | 0.162327 | 0.084300 |
| medium | 3 | 300 | 0.853333 | 0.220000 | 0.353333 | 0.000000 | 0.750000 | 0.158250 | 0.376800 |
| medium | 6 | 300 | 1.000000 | 0.313333 | 0.346667 | 0.000000 | 1.185000 | 0.142141 | 0.818800 |

Gate status: this moves A4 beyond aggregate loose-claims mapping, but the robustness breakout remains below manuscript gate because A7-A9 executable sweeps, recovery/correction metrics, broader mechanism coverage, seed sensitivity, and external harm-claim validation remain incomplete.
