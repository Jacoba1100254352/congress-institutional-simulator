# A1-A8 Multi-Seed Replication Summary

Deterministic replication of the fixed first-wave A1 through A8 adversarial pilots across independent base seeds.

- Adversaries: 8 (A1 through A8)
- Base seeds: 30 (20260428 through 20260457)
- Runs per seed: 5
- Bills per run: 60
- Attack cells: 57
- Seed-cell summaries: 1710
- Seed-metric rows: 28800
- Evaluated attack rows: 567000
- Exact attack-success rows: 338274
- Interval method: `two_sided_student_t_on_base_seed_estimates`
- Replication traces: not written; compact per-seed summaries are checkpointed under `out/`.

The interval unit is the base seed. These intervals do not treat bills within a simulated world as independent observations.
Success criteria and evaluated-row units differ by adversary. The cross-family exact-success total is an audit count, not a pooled attack rate.

| Adversary | Mechanism | Information | Budget | Evaluated rows | Exact successes | Seeds with success | Success rate mean [95% CI] | Primary metric | Primary mean [95% CI] |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | medium | 1 | 18000 | 8346 | 30/30 | 0.464 [0.455, 0.472] | Mean public-benefit loss | 0.011 [0.011, 0.011] |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | medium | 3 | 18000 | 9352 | 30/30 | 0.520 [0.511, 0.528] | Mean public-benefit loss | 0.020 [0.020, 0.021] |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | medium | 6 | 18000 | 9459 | 30/30 | 0.525 [0.517, 0.534] | Mean public-benefit loss | 0.031 [0.031, 0.032] |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | high | 1 | 18000 | 8654 | 30/30 | 0.481 [0.473, 0.489] | Mean public-benefit loss | 0.016 [0.016, 0.017] |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | high | 3 | 18000 | 9477 | 30/30 | 0.526 [0.518, 0.535] | Mean public-benefit loss | 0.029 [0.029, 0.030] |
| A1 Clone/decoy pressure | policy_tournament_pairwise_majority | high | 6 | 18000 | 9492 | 30/30 | 0.527 [0.519, 0.536] | Mean public-benefit loss | 0.041 [0.040, 0.041] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | medium | 1 | 9000 | 1364 | 30/30 | 0.152 [0.141, 0.162] | Mean public-benefit loss | 0.003 [0.002, 0.003] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | medium | 3 | 9000 | 3375 | 30/30 | 0.375 [0.363, 0.387] | Mean public-benefit loss | 0.012 [0.011, 0.012] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | medium | 6 | 9000 | 5162 | 30/30 | 0.574 [0.562, 0.585] | Mean public-benefit loss | 0.033 [0.031, 0.034] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | high | 1 | 9000 | 2060 | 30/30 | 0.229 [0.218, 0.240] | Mean public-benefit loss | 0.004 [0.004, 0.004] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | high | 3 | 9000 | 4473 | 30/30 | 0.497 [0.485, 0.509] | Mean public-benefit loss | 0.016 [0.016, 0.017] |
| A2 Poison-pill sequencing | multi_round_amendment_majority | high | 6 | 9000 | 6146 | 30/30 | 0.683 [0.672, 0.694] | Mean public-benefit loss | 0.044 [0.043, 0.046] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | low | 1 | 9000 | 5883 | 30/30 | 0.654 [0.642, 0.665] | Mean public-preference distortion added | -0.072 [-0.074, -0.070] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | low | 3 | 9000 | 8995 | 30/30 | 0.999 [0.999, 1.000] | Mean public-preference distortion added | -0.146 [-0.149, -0.143] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | low | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean public-preference distortion added | -0.143 [-0.146, -0.140] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | medium | 1 | 9000 | 8532 | 30/30 | 0.948 [0.943, 0.953] | Mean public-preference distortion added | -0.014 [-0.016, -0.012] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | medium | 3 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean public-preference distortion added | -0.041 [-0.044, -0.038] |
| A3 Public-input manipulation | public_objection_and_citizen_panel_majority | medium | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean public-preference distortion added | -0.028 [-0.032, -0.024] |
| A4 Bad-faith harm claims | harm_weighted_majority | medium | 1 | 9000 | 5446 | 30/30 | 0.605 [0.594, 0.617] | Mean false-positive burden added | 0.121 [0.118, 0.125] |
| A4 Bad-faith harm claims | harm_weighted_majority | medium | 3 | 9000 | 7538 | 30/30 | 0.838 [0.830, 0.845] | Mean false-positive burden added | 0.281 [0.276, 0.285] |
| A4 Bad-faith harm claims | harm_weighted_majority | medium | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean false-positive burden added | 0.569 [0.566, 0.572] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | low | 1 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.004 [-0.001, 0.009] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | low | 3 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.011 [0.007, 0.015] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | low | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.011 [0.006, 0.015] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | medium | 1 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.005 [0.000, 0.011] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | medium | 3 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.010 [0.006, 0.014] |
| A5 Proposal flooding | fixed_capacity_agenda_lottery_majority | medium | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean policy-yield loss | 0.010 [0.006, 0.014] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | medium | 1 | 9000 | 313 | 30/30 | 0.035 [0.030, 0.040] | Mean observed-screen-risk decline | 0.217 [0.216, 0.217] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | medium | 3 | 9000 | 520 | 30/30 | 0.058 [0.050, 0.066] | Mean observed-screen-risk decline | 0.280 [0.279, 0.280] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | medium | 6 | 9000 | 658 | 30/30 | 0.073 [0.064, 0.082] | Mean observed-screen-risk decline | 0.374 [0.373, 0.375] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | high | 1 | 9000 | 507 | 30/30 | 0.056 [0.049, 0.064] | Mean observed-screen-risk decline | 0.286 [0.286, 0.287] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | high | 3 | 9000 | 731 | 30/30 | 0.081 [0.069, 0.093] | Mean observed-screen-risk decline | 0.363 [0.362, 0.364] |
| A6 Lobbying camouflage | anti_capture_public_interest_influence_system | high | 6 | 9000 | 299 | 30/30 | 0.033 [0.028, 0.039] | Mean observed-screen-risk decline | 0.478 [0.477, 0.479] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | medium | 1 | 9000 | 0 | 0/30 | 0.000 [0.000, 0.000] | Mean risk-control degradation added | 0.065 [0.061, 0.069] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | medium | 3 | 9000 | 8102 | 30/30 | 0.900 [0.900, 0.901] | Mean risk-control degradation added | 0.218 [0.211, 0.225] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | medium | 6 | 9000 | 8700 | 30/30 | 0.967 [0.967, 0.967] | Mean risk-control degradation added | 0.224 [0.217, 0.231] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | high | 1 | 9000 | 0 | 0/30 | 0.000 [0.000, 0.000] | Mean risk-control degradation added | 0.074 [0.070, 0.078] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | high | 3 | 9000 | 8399 | 30/30 | 0.933 [0.933, 0.933] | Mean risk-control degradation added | 0.223 [0.216, 0.230] |
| A7 Administrative overload | portfolio_hybrid_administrative_review_capacity | high | 6 | 9000 | 8850 | 30/30 | 0.983 [0.983, 0.983] | Mean risk-control degradation added | 0.226 [0.220, 0.233] |
| A8 Public-support distortion | constituent_verified_majority | low | 1 | 9000 | 113 | 29/30 | 0.013 [0.010, 0.015] | Mean residual signal distortion | 0.016 [0.016, 0.016] |
| A8 Public-support distortion | constituent_verified_majority | low | 3 | 9000 | 200 | 30/30 | 0.022 [0.020, 0.025] | Mean residual signal distortion | 0.027 [0.027, 0.027] |
| A8 Public-support distortion | constituent_verified_majority | low | 6 | 9000 | 8492 | 30/30 | 0.944 [0.940, 0.947] | Mean residual signal distortion | 0.043 [0.043, 0.043] |
| A8 Public-support distortion | constituent_verified_majority | medium | 1 | 9000 | 160 | 30/30 | 0.018 [0.015, 0.021] | Mean residual signal distortion | 0.023 [0.023, 0.023] |
| A8 Public-support distortion | constituent_verified_majority | medium | 3 | 9000 | 254 | 30/30 | 0.028 [0.025, 0.032] | Mean residual signal distortion | 0.033 [0.033, 0.033] |
| A8 Public-support distortion | constituent_verified_majority | medium | 6 | 9000 | 2662 | 30/30 | 0.296 [0.285, 0.306] | Mean residual signal distortion | 0.048 [0.048, 0.048] |
| A8 Public-support distortion | constituent_verified_majority | high | 1 | 9000 | 203 | 30/30 | 0.023 [0.019, 0.026] | Mean residual signal distortion | 0.030 [0.030, 0.030] |
| A8 Public-support distortion | constituent_verified_majority | high | 3 | 9000 | 2556 | 30/30 | 0.284 [0.275, 0.293] | Mean residual signal distortion | 0.040 [0.040, 0.040] |
| A8 Public-support distortion | constituent_verified_majority | high | 6 | 9000 | 2691 | 30/30 | 0.299 [0.290, 0.308] | Mean residual signal distortion | 0.054 [0.054, 0.055] |
| A8 Public-support distortion | signal_reliant_majority | low | 1 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean residual signal distortion | 0.053 [0.053, 0.053] |
| A8 Public-support distortion | signal_reliant_majority | low | 3 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean residual signal distortion | 0.089 [0.089, 0.089] |
| A8 Public-support distortion | signal_reliant_majority | low | 6 | 9000 | 9000 | 30/30 | 1.000 [1.000, 1.000] | Mean residual signal distortion | 0.143 [0.143, 0.143] |
| A8 Public-support distortion | signal_reliant_majority | medium | 1 | 9000 | 8856 | 30/30 | 0.984 [0.981, 0.987] | Mean residual signal distortion | 0.077 [0.076, 0.077] |
| A8 Public-support distortion | signal_reliant_majority | medium | 3 | 9000 | 8857 | 30/30 | 0.984 [0.981, 0.987] | Mean residual signal distortion | 0.111 [0.111, 0.112] |
| A8 Public-support distortion | signal_reliant_majority | medium | 6 | 9000 | 8858 | 30/30 | 0.984 [0.981, 0.987] | Mean residual signal distortion | 0.161 [0.160, 0.161] |
| A8 Public-support distortion | signal_reliant_majority | high | 1 | 9000 | 8844 | 30/30 | 0.983 [0.980, 0.986] | Mean residual signal distortion | 0.101 [0.100, 0.101] |
| A8 Public-support distortion | signal_reliant_majority | high | 3 | 9000 | 8849 | 30/30 | 0.983 [0.980, 0.986] | Mean residual signal distortion | 0.134 [0.134, 0.135] |
| A8 Public-support distortion | signal_reliant_majority | high | 6 | 9000 | 8846 | 30/30 | 0.983 [0.980, 0.986] | Mean residual signal distortion | 0.182 [0.181, 0.182] |

Claim boundary: A1-A8 multi-seed synthetic replication only. The fixed base-seed panel is the uncertainty unit; bills and worlds within a seed are not treated as independent replications. Intervals summarize Monte Carlo sensitivity under the fixed first-wave attack mechanisms, budgets, information levels, institutional paths, and recovery assumptions. They are not population intervals, empirical attack-frequency estimates, general mechanism rankings, or evidence for real-world institutional adoption. Success criteria and evaluated-row units differ by adversary, so the cross-family success total is an audit count rather than a pooled attack rate.

Gate status: fixed-specification base-seed replication is available for all first-wave A1-A8 pilots. The robustness paper remains below manuscript gate because broader mechanism variants, substantive recovery and correction, alternative A9 specifications, and external validation remain incomplete.
