# Paper Plan

## Current Decision

Readiness level: 3 of 4 for bounded first-wave implementation, but no full manuscript yet.

Recommendation: extend the completed fixed-specification A1-A9 replication into broader mechanism and parameter sweeps, stronger correction tests, and validation; defer manuscript drafting.

This breakout should become a failure-mode and robustness paper, not a second umbrella paper. The ACM CI framework paper remains the stable core artifact. This paper should only ask how specified legislative mechanisms behave under bounded adversaries with explicit objectives, budgets, information levels, and success metrics.

## Working Title

Adversarial Failure Modes in Legislative Collective-Decision Mechanisms

## Contribution Boundary

The contribution, after new evidence exists, should be a bounded adversarial stress-test method and result set:

- explicit adversary models for legislative mechanism families;
- paired baseline-versus-attack experiments;
- attack success rates and worst-case degradation metrics;
- administrative-burden and recovery/correction diagnostics;
- traceable examples of failure paths.

The paper should not contribute:

- a new simulation framework;
- a general mechanism catalog;
- broad institutional rankings;
- a normative reform argument;
- a "legislative design space" search frame;
- a default-enactment-centered paper.

## Relationship to Stable Core Artifacts

| Stable artifact | Owned contribution | Allowed use in this paper |
|---|---|---|
| `paper/acm-ci-framework/acm-ci-framework.pdf` | Reproducible framework and main diagnostic campaign. | Cite as the platform and baseline evidence source only. |
| `paper/technical-appendix/odd-d-appendix.pdf` | Model documentation and technical detail. | Reference for simulator assumptions and ODD+D documentation. |
| `docs/odd-model.md` | ODD model notes. | Use to define model scope and limitations. |
| `docs/calibration.md` and `reports/calibration-baseline.md` | Calibration-screening workflow. | Use as a boundary check, not validation of adversarial behavior. |

## Overlap Controls

| Adjacent paper path | Overlap risk | Boundary rule |
|---|---|---|
| ACM CI framework paper | High if this becomes another framework comparison paper. | Use the framework as fixed infrastructure; only report adversarial robustness results that are new. |
| Empirical-validation roadmap | Medium if validation becomes the main contribution. | Include validation needs and data roadmap only as gates for interpreting robustness claims. |
| Political science simulation paper | Medium if this turns into a general simulation-method paper. | Focus on adversarial failure modes, not broad simulation positioning. |
| Chamber-structure paper | Low to medium for bicameral or committee stress cases. | Treat chamber architecture as a target family only where an adversary exploits it; defer representation architecture claims. |
| Software/artifact paper | Low. | Mention reproducibility targets only as required experiment infrastructure. |

## Current Evidence

Existing pilot artifacts can motivate the project but are not publication-ready evidence:

- `reports/simulation-manipulation-stress.csv`: 91 data rows.
- `reports/manipulation-stress-summary.md`: paired pilot stress summary.
- `reports/simulation-ablation-analysis.csv`: 405 data rows.
- `reports/ablation-analysis-summary.md`: mechanism ablation summary.
- `reports/adversary-catalog.md`: generated first-wave A1-A9 adversary schema from simulator code.
- `reports/adversarial-stress-manifest.json`: machine-readable schema manifest for future adversarial outputs.
- `reports/adversarial-stress-run-manifest.json`: machine-readable manifest for the first executable A1 stress run.
- `reports/adversarial-stress-summary.md`: first executable A1 clone/decoy budget/information summary.
- `reports/adversarial-failure-traces.jsonl`: same-generated-world A1 per-bill trace rows.
- `reports/adversarial-stress-a2-run-manifest.json`: machine-readable manifest for the first executable A2 stress run.
- `reports/adversarial-stress-a2-summary.md`: first executable A2 poison-pill/sequencing budget/information summary.
- `reports/adversarial-failure-traces-a2.jsonl`: same-generated-world A2 per-bill trace rows.
- `reports/adversarial-stress-a3-run-manifest.json`: machine-readable manifest for the first executable A3 stress run.
- `reports/adversarial-stress-a3-summary.md`: first executable A3 public-input manipulation budget/information summary.
- `reports/adversarial-failure-traces-a3.jsonl`: same-generated-world A3 per-bill trace rows.
- `reports/adversarial-stress-a4-run-manifest.json`: machine-readable manifest for the first executable A4 stress run.
- `reports/adversarial-stress-a4-summary.md`: first executable A4 bad-faith harm-claim budget summary.
- `reports/adversarial-failure-traces-a4.jsonl`: same-generated-world A4 per-bill trace rows.
- `reports/adversarial-stress-a5-run-manifest.json`: machine-readable manifest for the first executable A5 stress run.
- `reports/adversarial-stress-a5-summary.md`: first executable A5 proposal-flooding budget/information summary.
- `reports/adversarial-failure-traces-a5.jsonl`: same-generated-world A5 per-original-bill trace rows.
- `reports/adversarial-stress-a6-run-manifest.json`: machine-readable manifest for the first executable A6 stress run.
- `reports/adversarial-stress-a6-summary.md`: first executable A6 lobbying-camouflage budget/information summary.
- `reports/adversarial-failure-traces-a6.jsonl`: same-generated-world A6 per-bill trace rows.
- `reports/adversarial-stress-a7-run-manifest.json`: machine-readable manifest for the first executable A7 stress run.
- `reports/adversarial-stress-a7-summary.md`: first executable A7 administrative-overload budget/information and queue-recovery summary.
- `reports/adversarial-failure-traces-a7.jsonl`: same-generated-world A7 per-bill overload and recovery trace rows.
- `reports/adversarial-stress-a8-run-manifest.json`: machine-readable manifest for the first executable A8 stress run.
- `reports/adversarial-stress-a8-summary.md`: first executable A8 public-support-distortion mechanism/budget/information and same-case correction summary.
- `reports/adversarial-failure-traces-a8.jsonl`: same-world, same-bill, same-status-quo A8 direct-signal and correction trace rows.
- `reports/adversarial-stress-a9-run-manifest.json`: machine-readable manifest for the first executable A9 mixed-portfolio stress run.
- `reports/adversarial-stress-a9-summary.md`: three-portfolio fixed-budget comparison against full-budget and allocated-component single controls.
- `reports/adversarial-failure-traces-a9.jsonl`: same-world, same-bill, same-status-quo A9 mixed and single-control traces.
- `reports/adversarial-replication-a1-a8-run-manifest.json`: fixed 30-base-seed panel, source hashes, output hashes, and trace-storage boundary for A1-A8.
- `reports/adversarial-replication-a1-a8-seed-metrics.csv`: compact long-form seed estimates across all 57 A1-A8 cells and metrics.
- `reports/adversarial-replication-a1-a8-summary.md`: seed-level intervals and exact success counts across 567,000 evaluated rows.
- `reports/adversarial-replication-a9-run-manifest.json`: fixed 30-base-seed panel, source hashes, output hashes, and trace-storage boundary.
- `reports/adversarial-replication-a9-seed-results.csv`: compact seed-level estimates for all 18 A9 cells.
- `reports/adversarial-replication-a9-summary.md`: seed-level uncertainty intervals and strict mixed-only event counts across 162,000 evaluated rows.
- `reports/adversarial-pilot-cell-map.md`: map from the A1-A9 schema to current aggregate pilot stress cells and executable A1-A9 artifacts.
- `reports/adversarial-failure-trace-index.md`: aggregate pilot trace-candidate ranking.
- `reports/seed-robustness-summary.md`: multi-seed check for the main comparison campaign; explicit A1-A8 and A9 adversary replications are separate.
- `reports/empirical-validation-readiness.md`: empirical readiness screen with 12 of 12 raw validation datasets present.
- `reports/calibration-baseline.md`: 7 of 7 conventional baseline screens passed, but not an adversarial validation result.

Pilot findings that may be used only as motivation:

- Policy tournament clone/decoy stress shows material vulnerability in the current summary: directional loss 0.087, revision-moderation loss 0.046, and low-public-support passage added 0.010.
- Open burden-shifting capture/flooding stress shows material vulnerability: directional loss 0.021, revision-moderation loss 0.027, and low-public-support passage added 0.063.
- Citizen-panel manipulation, loose harm claims, astroturf pressure, and proposal flooding show limited observed degradation under current bounded probes.
- Anti-capture defensive backlash improves the current score profile, which is a warning that the stress setup is not yet a general adversary model.
- Ablation results show that some modules change metrics, but ablations are not adversary experiments.
- A1-A8 replication covers 30 base seeds, 57 cells, 567,000 evaluated rows, and 338,274 exact successes. The total is an audit count rather than a pooled rate because family definitions and row units differ. A5 and A7 show why binary success must be interpreted separately from continuous degradation.
- A9 replication records 2,626 strict mixed-only failures across 30 base seeds and 162,000 evaluated rows, while mean interaction intervals are negative in 16 of 18 cells. Mixed-only event recurrence is therefore not evidence of generally superadditive average degradation.

## Scope for First Version

First-wave attacks should be limited to cases where the simulator already has relevant mechanism surfaces:

- clone/decoy alternatives against content-selection mechanisms;
- poison-pill or sequencing attacks against amendment/tournament mechanisms;
- astroturf/noise attacks against public-input paths;
- bad-faith harm claims against harm-protection paths;
- proposal flooding against agenda systems;
- lobbying camouflage against anti-capture paths;
- administrative overload against layered portfolio systems;
- direct public-support distortion against signal-reliant and signal-verification paths;
- mixed adversary portfolios that combine two or more of the above attacks under one fixed budget.

Strategic silence under burden-shifting rules may remain a later or appendix case. It should not dominate the project.

## Repo Structure

Primary planning folder:

- `papers/robustness-failure-modes/`

Required planning files:

- `paper-plan.md`: scope, evidence readiness, overlap controls, and recommendation.
- `adversary-model.md`: actor taxonomy, fields, success metrics, and deferred adversaries.
- `experiment-plan.md`: required new experiments, reporting outputs, and implementation tasks.
- `claims-ledger.md`: claims, current support, gaps, and allowed wording.
- `figure-table-plan.md`: figures and tables with readiness gates.
- `validation-needs.md`: validation gaps, modeling weaknesses, and required checks.
- `go-no-go.md`: decision gate for experiment work and manuscript drafting.

Expected future implementation locations:

- `src/main/java/congresssim/institution/adversary/` for explicit adversary records or equivalent.
- `src/test/java/congresssim/` for deterministic adversary and trace tests.
- `scripts/reporting/` for adversarial-stress summaries.
- `reports/` for generated outputs.
- `out/` for generated traces or intermediate campaign files.

## Readiness Assessment

| Area | Current state | Readiness |
|---|---|---|
| Framework dependency | Stable enough to use as infrastructure. | Ready. |
| Pilot stress evidence | Aggregate screens and bounded explicit A1-A9 adversary experiments exist, but they do not provide broad or externally validated robustness estimates. | Partial. |
| Adversary definitions | Planning taxonomy, generated Java-backed A1-A9 catalog, and bounded executable pilots for all nine entries exist. | Ready for bounded first-wave use. |
| Attack-budget sweeps | Implemented with 30-base-seed replication for bounded A1-A9 fixed specifications; broader mechanism and parameter sweeps are missing. | Partial. |
| Worst-case degradation | Reported for bounded A1-A9 pilots and summarized across seeds for all fixed first-wave specifications; cross-mechanism worst cases are missing. | Partial. |
| Attack success rates | Computed for bounded A1-A9 pilots and across 30 base seeds for every first-wave attack; externally validated rates are missing. | Partial. |
| Recovery/correction metrics | A7 queue recovery, A8 same-case signal correction, and bounded A9 same-case/queue controls are computed; broader temporal or substantive correction is not. | Partial. |
| Failure traces | Canonical A1-A9 trace JSONL artifacts exist; both replication panels intentionally retain compact seed summaries rather than duplicate traces. Broader mechanisms and stronger correction remain missing. | Partial. |
| Empirical validation | Dataset readiness is partial and attack-rate validation is absent. | Not ready. |

## Proceed or Defer

Proceed now with planning and implementation of adversary experiments.

Defer a full manuscript until the go/no-go gates in `go-no-go.md` are satisfied.
