# Robustness and Failure-Mode Breakout

Current decision: proceed with structured planning and adversary experiments; do not draft the manuscript yet.

This folder plans a separate paper on bounded adversarial failure modes in legislative collective-decision mechanisms. It is not a general mechanism-comparison paper and should not duplicate the ACM CI framework paper's reusable-framework contribution.

## Boundary

Use the ACM CI framework paper as fixed infrastructure. This breakout should study specified adversaries, not broad institutional design or reform rankings.

Avoid:

- giant mechanism catalogs;
- repeated caveat loops;
- design-space-search framing;
- default-enactment fixation;
- broad normative conclusions.

## Required Files

- `paper-plan.md`: scope, readiness, overlap controls, and repository structure.
- `adversary-model.md`: actor taxonomy, objectives, budgets, information levels, and success metrics.
- `experiment-plan.md`: required adversarial experiments and code/reporting tasks.
- `claims-ledger.md`: proposed claims, current support, gaps, and allowed wording.
- `figure-table-plan.md`: figure/table specifications and readiness.
- `validation-needs.md`: validation gaps and modeling weaknesses.
- `go-no-go.md`: proceed/defer decision gates.

Supporting files may include outlines or related-work notes, but they should not become a full manuscript until the go/no-go gate is satisfied.

## Current Evidence

The repository has useful pilot artifacts:

- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.md`
- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.md`

Those reports are not enough for a standalone failure-mode paper because they do not yet specify explicit adversary actors, budgets, information levels, attack success rates, worst-case degradation, or recovery/correction behavior.

## Coverage Check

The current plan covers the requested failure modes as planned experiments or bounded/deferred cases:

- clone/decoy alternatives: Experiment 1;
- agenda sequencing and poison-pill amendments: Experiment 2;
- astroturf objection windows and noisy/biased panels: Experiment 3;
- bad-faith harm claims: Experiment 4;
- proposal flooding: Experiment 5;
- lobbying camouflage and defensive lobbying: Experiment 6;
- public-support distortion: Experiments 3 and 8;
- administrative overload: Experiment 7;
- mixed attack portfolios: Experiment 8;
- strategic silence under burden-shifting rules: deferred boundary case after the first-wave experiments.

## Full Draft Rule

Do not draft the full paper until explicit adversary experiments have been implemented, run, and validated according to `go-no-go.md`.
