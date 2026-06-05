# Political Science / Computational Social Science Breakout

Final decision: NEEDS DATA/VALIDATION FIRST.

This folder plans a future political science / computational social science paper about institutional model behavior. It must not reuse the ACM CI paper's main contribution. The ACM CI paper owns the reusable-framework claim; this breakout must be about institutional theory, benchmark fairness, and politically meaningful mechanism behavior.

## Working Purpose

Turn the legislative-mechanism simulator into a deeper computational political science paper about legislative bargaining, agenda control, vetoes, committees, lobbying, public-support proxies, and empirical calibration/validation.

## Primary Question

Under what assumptions do agenda control, committee routing, veto structures, lobbying pressure, proposal access, and content-improvement stages change legislative productivity, representative responsiveness, capture risk, and public-support failure?

## Readiness Audit

Not ready for a full draft.

The repository has a broad implemented simulator, a canonical main campaign, mechanism inventories, seed checks, flow sanity checks, and validation-gap reports. It does not yet have enough validation or fair benchmark controls to support a standalone political-science results paper.

The strongest blockers are:

- district-level public opinion is missing;
- campaign finance and lobbying-to-bill linkage are missing;
- court review, implementation, law revision, and comparative-institution datasets are missing;
- conventional benchmarks do not yet receive fully comparable information/amendment/review budgets;
- public-support and generated public-benefit relationships remain synthetic and generator-dependent;
- scenario variation and stochastic uncertainty need cleaner separation.

## Files

- `paper-plan.md`: readiness decision, mechanism inventory, theory framing, artifacts, missing work, and go/no-go.
- `claims-ledger.md`: claim-by-claim support, limitations, and citation/data needs.
- `experiment-plan.md`: benchmark fairness controls, parameter sweeps, paired comparisons, and uncertainty plan.
- `validation-plan.md`: missing data inventory and validation sequence.
- `figure-table-plan.md`: required figures and tables for a future draft.
- `draft-outline.md`: paper outline only; no full manuscript.
- `related-work-targets.md`: literature areas to verify before drafting.
- `go-no-go.md`: explicit readiness gates for drafting.

## Next Concrete Repo Tasks

1. Extend the empirical-validation pipeline first: public opinion, campaign finance, implementation/correction, and source registry remain blockers.
2. Implement benchmark fairness controls that give conventional and simple-majority baselines comparable information, amendment, review, and attention budgets.
3. Add paired-comparison reports that compare mechanisms on the same generated worlds.
4. Separate seed variance from scenario variation in any political-science result table.
5. Keep `PORT` and content-selection findings as conditional mechanism-behavior hypotheses, not reform rankings.
