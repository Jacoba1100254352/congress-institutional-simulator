# Chamber-Structure Breakout

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

This folder plans a separate representation-architecture paper. It is not a side section of the ACM framework paper and should not reuse the ACM paper's main framework contribution.

## Working Purpose

Develop a paper on how chamber architecture, apportionment, committee assignment, review bodies, and selection/retention filters affect representation and legislative tradeoffs.

## Primary Research Question

How do chamber and representation architectures shift productivity, revision moderation, public-support diagnostics, minority harm, committee capture, malapportionment, and review delay?

## Current Readiness

Not ready for a full paper draft.

The repository has a substantial chamber campaign and several chamber/committee/review modules, but it does not yet have the representation model needed for a stand-alone paper. The main blockers are:

- status quo and representation diagnostics are not clearly domain-aware enough for chamber claims;
- public support is not yet cleanly separated into national support, district support, affected-group support, and chamber coalition support;
- district/population support distributions need to be strengthened;
- validation planning for apportionment, district population, chamber votes, committee assignment, bicameral disagreement, and review bodies is incomplete;
- expanded sweeps are needed for malapportionment, upper-chamber power, committee capture, selection/retention filters, and review bodies.

## Required Files

- `paper-plan.md`: stand-alone paper decision, core mechanisms, artifacts, and go/no-go.
- `go-no-go.md`: explicit readiness gate and full-draft conditions.
- `representation-model.md`: model changes needed for domain-aware representation diagnostics.
- `validation-plan.md`: data and validation roadmap for representation architecture.
- `experiment-plan.md`: required chamber experiments and code tasks.
- `claims-ledger.md`: claim support, limitations, and evidence gates.
- `figure-table-plan.md`: required figures and tables.
- `draft-outline.md`: outline only; no full manuscript.

## Full Draft Rule

Do not draft the full paper unless expanded chamber scenarios and representation-validation planning are complete.

## Next Concrete Repo Tasks

1. Add support diagnostics that distinguish national, district, affected-group, lower/upper chamber coalition, population-weighted, and chamber-weighted support.
2. Add paired sweep targets for malapportionment, upper-chamber power, committee capture, selection/retention, review bodies, bicameral conflict, and support weighting.
3. Create a chamber validation data inventory before treating any representation claim as more than a synthetic sensitivity result.
4. Keep current `chamber-family-champions` and `chamber-stress-screen` outputs in the appendix or planning materials only; they are not recommendation tables.
