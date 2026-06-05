# Go/No-Go

## Current Decision

Go for structured planning and implementation.

No-go for a full manuscript.

The evidence is not ready for manuscript drafting because the repo has pilot manipulation-stress and ablation screens, not explicit adversary experiments with budgets, information levels, success rates, worst-case degradation, recovery metrics, and traces.

## Readiness Level

| Level | Meaning | Current? |
|---|---|---|
| 0 | Idea only. | No. |
| 1 | Stable framework and paper boundary identified. | Yes. |
| 2 | Pilot evidence and experiment plan exist. | Yes, current level. |
| 3 | Explicit adversary experiments implemented and run. | No. |
| 4 | Manuscript-ready evidence and validation boundaries complete. | No. |

## Proceed Now

Proceed with:

- adversary model implementation;
- attack-budget and information-level sweeps;
- same-seed baseline pairing;
- failure trace logging;
- worst-case, median, and success-rate reporting;
- validation-boundary documentation.

## Defer

Defer:

- full manuscript drafting;
- broad literature synthesis;
- general mechanism ranking;
- broad normative conclusions;
- any new umbrella-paper framing;
- a default-enactment-centered paper.

## Manuscript Go Conditions

Move to manuscript drafting only when all of the following are true:

1. Experiments 1-8 in `experiment-plan.md` have generated outputs.
2. Every attack report includes actor type, objective, budget, information level, strategy set, and success metric.
3. Same-seed baseline pairing exists for core attack cells.
4. Attack success rates are computed.
5. Worst-case and median degradation are both reported.
6. Failure traces exist for at least three attack families.
7. Recovery/correction and administrative burden are reported where relevant.
8. Seed sensitivity is run for the core attack families.
9. `make test` passes after implementation.
10. Validation gaps in `validation-needs.md` are reflected in claim wording.

## Stop Conditions

Stop or narrow the project if:

- adversary models cannot be implemented without rewriting the ACM framework;
- results collapse into a general mechanism catalog;
- the strongest claims depend only on generated public benefit without sensitivity checks;
- default-pass or burden-shifting cases dominate the evidence chain;
- validation gaps are too large for the planned claim set;
- the output starts making institutional adoption claims.

## Final Recommendation

Proceed with the robustness/failure-mode paper as an experiment-first breakout. Do not draft the manuscript yet.
