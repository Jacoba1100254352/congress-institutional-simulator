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

- district-level public opinion now includes one bounded historical related-issue pilot, but still lacks exact or contemporaneous bill support, design-based uncertainty or MRP, and affected-group evidence;
- campaign-finance linkage beyond FEC recipient metadata, bounded issue-sector context, matched member context, bounded House-candidate district context, and bounded candidate-to-sponsored-bill context to reviewed targets, committee-action influence, and outcomes, plus lobbying linkage beyond current LDA issue taxonomy, shared-policy-area bill context, and exact filing-text bill identifiers for a bounded public-law subset to sponsor/member targets, committees, roll calls, influence, and outcomes, is missing;
- full statutory-lineage and emergency-order court review datasets are missing; SCDB merits-case court review, Federal Register final-rule effective dates with bounded document/docket metadata, authority-search matches, and proposed-history matches, Congress.gov law-revision text flags with bounded bill/action metadata, and QoG/OWID/V-Dem comparative-institution profiles with bounded simulator scenario-family metadata anchors are present only as bounded proxies;
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

1. Extend the empirical-validation pipeline first: exact or closer contemporaneous bill-topic public opinion beyond the historical related-issue pilot, affected-group mapping, campaign-finance linkage beyond FEC recipient metadata and bounded context layers, full statutory lineage/correction beyond current review layers, and fuller implementation-feedback sources remain blockers.
2. Implement benchmark fairness controls that give conventional and simple-majority baselines comparable information, amendment, review, and attention budgets.
3. Add paired-comparison reports that compare mechanisms on the same generated worlds.
4. Separate seed variance from scenario variation in any political-science result table.
5. Keep `PORT` and content-selection findings as conditional mechanism-behavior hypotheses, not reform rankings.
