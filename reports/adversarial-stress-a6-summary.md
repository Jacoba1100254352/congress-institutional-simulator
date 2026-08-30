# A6 Lobbying-Camouflage Adversarial Stress Summary

Status: `partial_a6_executable_pilot`.

A6 executable pilot only. Rows use same generated worlds and bill ids for synthetic latent capture targets under a transparent anti-capture influence-system baseline and a camouflaged proxy/shadow-lobbying attack. Latent capture risk is traced separately from observed screen risk. This is not an empirical campaign-finance, lobbying-disclosure, or proxy-sponsorship estimate, not a full A1-A9 adversarial sweep, and not evidence for real-world institutional ranking.

- Adversary: A6 lobbying camouflage actor
- Same-seed generated-world runs: 5
- Legislators: 101
- Base bills per run: 60
- Trace rows: 1800
- Trace artifact: `reports/adversarial-failure-traces-a6.jsonl`
- Recovery metrics: not modeled in this pilot

| Information | Budget | Trace rows | Success rate | Anti-capture bypass | Capture enactment added | Visible-spend decline + capture | Shadow share added | Detection decline | Observed risk decline | Mean admin burden added |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| medium | 1 | 300 | 0.026667 | 0.026667 | 0.026667 | 0.016667 | 0.202630 | 0.202630 | 0.215425 | 0.066601 |
| medium | 3 | 300 | 0.026667 | 0.026667 | 0.026667 | 0.006667 | 0.268227 | 0.268227 | 0.277266 | 0.174224 |
| medium | 6 | 300 | 0.056667 | 0.056667 | 0.056667 | 0.000000 | 0.364384 | 0.364384 | 0.373972 | 0.341329 |
| high | 1 | 300 | 0.043333 | 0.043333 | 0.043333 | 0.013333 | 0.310267 | 0.310267 | 0.284652 | 0.137239 |
| high | 3 | 300 | 0.046667 | 0.046667 | 0.046667 | 0.000000 | 0.389463 | 0.389463 | 0.359886 | 0.258468 |
| high | 6 | 300 | 0.016667 | 0.016667 | 0.016667 | 0.000000 | 0.498925 | 0.498925 | 0.477647 | 0.447686 |

Gate status: this moves A6 beyond a defensive-backlash proxy, but the robustness breakout remains below manuscript gate because recovery/correction metrics, broader anti-capture mechanisms, multi-seed replication, and external lobbying-disclosure validation remain incomplete.
