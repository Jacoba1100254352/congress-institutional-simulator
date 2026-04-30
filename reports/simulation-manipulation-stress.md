# Manipulation Stress Campaign

Deterministic batch campaign for comparing institutional regimes across assumption sweeps.

## Run Configuration

- runs per case: 64
- legislators: 101
- base bills per run: 60
- base seed: 20260428
- scenarios per case: 13
- experiment cases: 7

## Headline Findings

- Open default-pass averaged 0.888 productivity, versus 0.372 for simple majority.
- Open default-pass also averaged 0.398 weak public-mandate passage and 0.583 policy shift.
- Highest directional score, where lower-better risk metrics are inverted before combination, came from Default pass unless 2/3 block at 0.729.
- Highest average welfare in this campaign came from Citizen assembly threshold gate at 0.646.

## Metric Direction Legend

- `↑` means a higher raw value is usually better.
- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.
- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

## Scenario Averages Across Cases

| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Weighted agenda lottery + majority | 0.645 | 0.556 | 0.862 | 0.968 | 0.196 | 17.076 | 47.571 | 0.576 | 0.000 | 0.134 | 0.032 | 0.192 | 0.514 | 0.071 | 0.293 | 0.291 | 0.000 | 0.000 | 0.000 | 0.000 | 0.367 | 0.000 | 0.464 |
| Majority + anti-capture bundle | 0.679 | 0.567 | 0.875 | 0.937 | 0.336 | 30.449 | 93.960 | 0.606 | 0.000 | 0.112 | 0.063 | 0.185 | 0.513 | 0.119 | 0.298 | 0.154 | 0.141 | 0.572 | 0.000 | 0.000 | 0.687 | 0.000 | 0.898 |
| Citizen assembly under manipulation stress | 0.623 | 0.595 | 0.886 | 0.810 | 0.201 | 19.074 | 102.857 | 0.627 | 0.000 | 0.040 | 0.190 | 0.160 | 0.603 | 0.062 | 0.247 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 | 0.461 | 0.000 | 1.000 |
| Citizen assembly threshold gate | 0.619 | 0.602 | 0.896 | 0.810 | 0.167 | 16.239 | 102.857 | 0.646 | 0.000 | 0.061 | 0.190 | 0.156 | 0.580 | 0.046 | 0.214 | 0.259 | 0.000 | 0.000 | 0.000 | 0.000 | 0.443 | 0.000 | 1.000 |
| Stylized U.S.-like conventional benchmark | 0.646 | 0.631 | 0.911 | 0.981 | 0.063 | 4.940 | 25.379 | 0.630 | 0.000 | 0.003 | 0.019 | 0.132 | 0.646 | 0.013 | 0.147 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 | 0.157 | 0.000 | 0.268 |
| Default pass unless 2/3 block | 0.729 | 0.471 | 0.628 | 0.930 | 0.888 | 89.172 | 102.857 | 0.460 | 0.406 | 0.398 | 0.070 | 0.260 | 0.376 | 0.583 | 0.562 | 0.317 | 0.000 | 0.000 | 0.000 | 0.000 | 0.983 | 0.000 | 1.000 |
| Harm-weighted majority + loose harm claims | 0.643 | 0.593 | 0.889 | 0.930 | 0.161 | 14.931 | 102.857 | 0.594 | 0.000 | 0.101 | 0.070 | 0.158 | 0.555 | 0.040 | 0.189 | 0.279 | 0.000 | 0.000 | 0.000 | 0.000 | 0.398 | 0.000 | 1.000 |
| Harm-weighted double majority | 0.652 | 0.570 | 0.870 | 0.930 | 0.239 | 22.824 | 102.857 | 0.567 | 0.000 | 0.141 | 0.070 | 0.178 | 0.524 | 0.075 | 0.243 | 0.307 | 0.000 | 0.000 | 0.000 | 0.000 | 0.466 | 0.000 | 1.000 |
| Public objection window + astroturf stress | 0.624 | 0.587 | 0.885 | 0.851 | 0.172 | 14.710 | 102.857 | 0.592 | 0.000 | 0.068 | 0.149 | 0.170 | 0.559 | 0.042 | 0.191 | 0.278 | 0.000 | 0.000 | 0.000 | 0.000 | 0.356 | 0.000 | 1.000 |
| Public objection window + majority | 0.639 | 0.579 | 0.880 | 0.863 | 0.235 | 20.527 | 102.857 | 0.591 | 0.000 | 0.080 | 0.137 | 0.167 | 0.551 | 0.061 | 0.206 | 0.258 | 0.000 | 0.000 | 0.000 | 0.000 | 0.512 | 0.000 | 1.000 |
| Unicameral simple majority | 0.669 | 0.547 | 0.828 | 0.930 | 0.372 | 31.484 | 102.857 | 0.553 | 0.000 | 0.164 | 0.070 | 0.206 | 0.495 | 0.136 | 0.303 | 0.316 | 0.000 | 0.000 | 0.000 | 0.000 | 0.595 | 0.000 | 1.000 |
| Unicameral majority + pairwise alternatives | 0.701 | 0.642 | 0.918 | 0.714 | 0.532 | 52.672 | 57.042 | 0.580 | 0.000 | 0.001 | 0.286 | 0.081 | 0.641 | 0.004 | 0.004 | 0.272 | 0.000 | 0.000 | 0.565 | 0.000 | 0.701 | 0.000 | 0.565 |
| Majority ratification + strategic policy tournament | 0.621 | 0.622 | 0.932 | 0.813 | 0.116 | 12.681 | 15.350 | 0.537 | 0.000 | 0.023 | 0.187 | 0.070 | 0.616 | 0.006 | 0.036 | 0.288 | 0.000 | 0.000 | 0.099 | 0.000 | 0.245 | 0.000 | 0.135 |

## Case Highlights

| Case | Best welfare | Most productive | Lowest weak public-mandate passage |
| --- | --- | --- | --- |
| Baseline | Stylized U.S.-like conventional benchmark (0.757) | Default pass unless 2/3 block (0.838) | Stylized U.S.-like conventional benchmark (0.000) |
| Proposal Flooding | Stylized U.S.-like conventional benchmark (0.736) | Default pass unless 2/3 block (0.833) | Stylized U.S.-like conventional benchmark (0.000) |
| Capture And Flooding | Stylized U.S.-like conventional benchmark (0.749) | Default pass unless 2/3 block (0.839) | Stylized U.S.-like conventional benchmark (0.000) |
| Clone/Decoy Tournament Pressure | Stylized U.S.-like conventional benchmark (0.753) | Default pass unless 2/3 block (0.839) | Unicameral majority + pairwise alternatives (0.002) |
| Rights-Harm Pressure | Citizen assembly threshold gate (0.638) | Default pass unless 2/3 block (0.980) | Stylized U.S.-like conventional benchmark (0.000) |
| Popular Harmful Pressure | Unicameral majority + pairwise alternatives (0.317) | Default pass unless 2/3 block (1.000) | Stylized U.S.-like conventional benchmark (0.000) |
| Anti-Lobbying Backlash | Citizen assembly threshold gate (0.705) | Default pass unless 2/3 block (0.889) | Unicameral majority + pairwise alternatives (0.002) |

## Interpretation

- The next model extension should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms, because agenda screening is now the central default-pass tradeoff.

## Reproduction

```sh
make campaign
```
