# A9 Multi-Seed Replication Summary

Deterministic replication of the fixed-specification A9 mixed-adversary pilot across independent base seeds.

- Base seeds: 30 (20260428 through 20260457)
- Runs per seed: 5
- Bills per run: 60
- Portfolio/information/budget cells: 18
- Seed-cell rows: 540
- Evaluated A9 trace rows: 162000
- Strict mixed-only success rows: 2626
- Interval method: `two_sided_student_t_on_base_seed_estimates`
- Replication traces: not written; compact per-seed summaries are checkpointed under `out/`.

The interval unit is the base seed. These intervals do not treat bills within a simulated world as independent observations.

| Portfolio | Components | Information | Budget | Evaluated rows | Strict successes | Seeds with success | Success rate mean [95% CI] | Interaction mean [95% CI] | Superadditive mean [95% CI] | Positive-interaction seeds | Correction failure mean [95% CI] |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| clone-decoy-poison-pill | A1+A2 | medium | 4 | 9000 | 333 | 30/30 | 0.037 [0.033, 0.041] | -0.012 [-0.013, -0.011] | 0.013 [0.012, 0.014] | 0.000 | 0.000 [0.000, 0.000] |
| clone-decoy-poison-pill | A1+A2 | medium | 8 | 9000 | 470 | 30/30 | 0.052 [0.044, 0.061] | -0.004 [-0.007, -0.002] | 0.012 [0.010, 0.014] | 0.267 | 0.000 [0.000, 0.000] |
| clone-decoy-poison-pill | A1+A2 | medium | 12 | 9000 | 85 | 26/30 | 0.009 [0.007, 0.012] | -0.005 [-0.007, -0.003] | -0.022 [-0.027, -0.017] | 0.100 | 0.000 [0.000, 0.000] |
| clone-decoy-poison-pill | A1+A2 | high | 4 | 9000 | 415 | 30/30 | 0.046 [0.039, 0.054] | -0.011 [-0.012, -0.011] | 0.013 [0.012, 0.014] | 0.000 | 0.000 [0.000, 0.000] |
| clone-decoy-poison-pill | A1+A2 | high | 8 | 9000 | 462 | 30/30 | 0.051 [0.042, 0.060] | -0.004 [-0.007, -0.002] | 0.007 [0.005, 0.009] | 0.300 | 0.000 [0.000, 0.000] |
| clone-decoy-poison-pill | A1+A2 | high | 12 | 9000 | 69 | 23/30 | 0.008 [0.005, 0.010] | -0.007 [-0.010, -0.004] | -0.023 [-0.028, -0.018] | 0.033 | 0.000 [0.000, 0.000] |
| astroturf-harm-claims | A3+A4 | medium | 4 | 9000 | 93 | 29/30 | 0.010 [0.008, 0.013] | 0.004 [0.003, 0.005] | 0.001 [0.001, 0.002] | 0.900 | 0.019 [0.016, 0.022] |
| astroturf-harm-claims | A3+A4 | medium | 8 | 9000 | 15 | 12/30 | 0.002 [0.001, 0.003] | -0.140 [-0.145, -0.136] | -0.000 [-0.000, 0.000] | 0.000 | 0.017 [0.014, 0.020] |
| astroturf-harm-claims | A3+A4 | medium | 12 | 9000 | 104 | 29/30 | 0.012 [0.010, 0.013] | -0.138 [-0.142, -0.134] | -0.135 [-0.139, -0.132] | 0.000 | 0.061 [0.055, 0.066] |
| astroturf-harm-claims | A3+A4 | high | 4 | 9000 | 96 | 29/30 | 0.011 [0.009, 0.013] | -0.001 [-0.002, 0.000] | 0.001 [0.000, 0.001] | 0.233 | 0.022 [0.020, 0.025] |
| astroturf-harm-claims | A3+A4 | high | 8 | 9000 | 100 | 29/30 | 0.011 [0.009, 0.013] | -0.134 [-0.138, -0.129] | 0.001 [0.000, 0.002] | 0.000 | 0.062 [0.057, 0.068] |
| astroturf-harm-claims | A3+A4 | high | 12 | 9000 | 102 | 28/30 | 0.011 [0.009, 0.014] | -0.136 [-0.140, -0.131] | -0.132 [-0.136, -0.128] | 0.000 | 0.062 [0.055, 0.069] |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 4 | 9000 | 20 | 15/30 | 0.002 [0.001, 0.003] | -0.072 [-0.075, -0.069] | -0.036 [-0.041, -0.031] | 0.000 | 0.524 [0.515, 0.532] |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 8 | 9000 | 34 | 22/30 | 0.004 [0.002, 0.005] | -0.043 [-0.046, -0.039] | -0.128 [-0.138, -0.118] | 0.000 | 0.603 [0.589, 0.618] |
| flood-camouflage-support-distortion | A5+A6+A8 | medium | 12 | 9000 | 58 | 23/30 | 0.006 [0.004, 0.009] | -0.032 [-0.036, -0.029] | -0.205 [-0.223, -0.188] | 0.000 | 0.631 [0.620, 0.642] |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 4 | 9000 | 25 | 17/30 | 0.003 [0.002, 0.004] | -0.063 [-0.066, -0.060] | -0.046 [-0.050, -0.041] | 0.000 | 0.554 [0.543, 0.565] |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 8 | 9000 | 52 | 23/30 | 0.006 [0.004, 0.008] | -0.035 [-0.039, -0.031] | -0.158 [-0.172, -0.145] | 0.000 | 0.619 [0.605, 0.632] |
| flood-camouflage-support-distortion | A5+A6+A8 | high | 12 | 9000 | 93 | 27/30 | 0.010 [0.008, 0.013] | -0.024 [-0.026, -0.021] | -0.227 [-0.247, -0.206] | 0.000 | 0.638 [0.626, 0.650] |

Claim boundary: A9 multi-seed synthetic replication only. The fixed base-seed panel is the uncertainty unit; bills and worlds within a seed are not treated as independent replications. Intervals summarize Monte Carlo sensitivity under the fixed A9 mechanisms, allocations, resource conversion, interaction coefficients, review capacity, and recovery assumptions. They are not population intervals, empirical attack-frequency estimates, general mechanism rankings, or evidence for real-world institutional adoption.

Gate status: independent-seed replication is available for the fixed A1-A9 pilots. The robustness paper remains below manuscript gate because broader mechanism variants, alternative A9 allocation/resource/interaction specifications, substantive outcome replay, and external validation remain incomplete.
