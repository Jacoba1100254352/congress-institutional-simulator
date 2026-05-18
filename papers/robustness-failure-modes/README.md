# Robustness and Failure-Mode Breakout

Final decision: NEEDS ADVERSARY EXPERIMENTS FIRST.

This folder plans a separate paper on adversarial failure modes in legislative collective-decision mechanisms. It is not a general mechanism-comparison paper and should not duplicate the ACM CI framework paper's reusable-framework contribution.

## Working Purpose

Develop a computational social science paper about how institutional mechanisms break under strategic manipulation: clone/decoy alternatives, sequencing attacks, poison-pill amendments, astroturf objection windows, noisy panels, bad-faith harm claims, proposal flooding, lobbying camouflage, public-support distortion, defensive lobbying, administrative overload, and strategic silence under burden-shifting passage.

## Primary Research Question

Which legislative mechanism families are robust or fragile under bounded adversaries with different goals, budgets, and information levels?

## Readiness Audit

Not ready for a full manuscript draft.

The repository has useful pilot artifacts:

- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.md`
- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.md`

Those reports are not enough for a standalone failure-mode paper because they do not yet specify explicit adversary actors, budgets, information levels, attack success rates, worst-case degradation, or recovery/correction behavior.

## Required Files

- `paper-plan.md`: paper decision, contribution boundary, current artifacts, and go/no-go.
- `adversary-model.md`: explicit adversary taxonomy and success metrics.
- `experiment-plan.md`: required adversarial experiments and code tasks.
- `claims-ledger.md`: claims, support, limitations, and required evidence.
- `figure-table-plan.md`: required figures/tables.
- `draft-outline.md`: outline only; no full manuscript.

## Full Draft Rule

Do not draft the full paper until explicit adversary experiments have been implemented and run.
