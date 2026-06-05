# Paper Plan

## Current Decision

Readiness level: 2 of 4, pilot evidence and executable surface available, but no full manuscript yet.

Recommendation: proceed now with adversary-model implementation and targeted experiments; defer manuscript drafting.

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
- `reports/seed-robustness-summary.md`: multi-seed check for the main comparison campaign, not for explicit adversary attacks.
- `reports/empirical-validation-readiness.md`: empirical readiness screen with 6 of 12 raw validation datasets present.
- `reports/calibration-baseline.md`: 7 of 7 conventional baseline screens passed, but not an adversarial validation result.

Pilot findings that may be used only as motivation:

- Policy tournament clone/decoy stress shows material vulnerability in the current summary: directional loss 0.087, revision-moderation loss 0.046, and low-public-support passage added 0.010.
- Open burden-shifting capture/flooding stress shows material vulnerability: directional loss 0.021, revision-moderation loss 0.027, and low-public-support passage added 0.063.
- Citizen-panel manipulation, loose harm claims, astroturf pressure, and proposal flooding show limited observed degradation under current bounded probes.
- Anti-capture defensive backlash improves the current score profile, which is a warning that the stress setup is not yet a general adversary model.
- Ablation results show that some modules change metrics, but ablations are not adversary experiments.

## Scope for First Version

First-wave attacks should be limited to cases where the simulator already has relevant mechanism surfaces:

- clone/decoy alternatives against content-selection mechanisms;
- poison-pill or sequencing attacks against amendment/tournament mechanisms;
- astroturf/noise attacks against public-input paths;
- bad-faith harm claims against harm-protection paths;
- proposal flooding against agenda systems;
- lobbying camouflage against anti-capture paths;
- administrative overload against layered portfolio systems.
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
| Pilot stress evidence | Useful screens exist, but they are not explicit adversary experiments. | Partial. |
| Adversary definitions | Planning taxonomy exists; implementation missing. | Not ready. |
| Attack-budget sweeps | Not implemented. | Not ready. |
| Worst-case degradation | Not systematically reported for adversaries. | Not ready. |
| Attack success rates | Not computed. | Not ready. |
| Recovery/correction metrics | Not computed. | Not ready. |
| Failure traces | Not logged in a paper-ready schema. | Not ready. |
| Empirical validation | Dataset readiness is partial and attack-rate validation is absent. | Not ready. |

## Proceed or Defer

Proceed now with planning and implementation of adversary experiments.

Defer a full manuscript until the go/no-go gates in `go-no-go.md` are satisfied.
