# Paper Plan

## Final Decision

BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

The current pipeline is useful but not substantially extended beyond flow sanity checks. A full paper should wait until the data pipeline covers more source families, especially public opinion, campaign finance, implementation feedback, and law revision.

## Working Title

Empirical Boundary Conditions for Legislative Mechanism Simulation

## Target Venue Category

Future data/resource paper, computational social science methods note, political methodology data paper, or social simulation validation paper.

## One-Sentence Contribution

The future paper would define and implement a benchmark-data pipeline that maps empirical legislative signals to simulation calibration, sanity-check, proxy, synthetic-only, and missing-model categories.

## What This Paper Is Not

- Not proof that the simulator is valid.
- Not a mechanism-ranking paper.
- Not a political-science results paper.
- Not a substitute for district opinion, campaign finance, implementation, court review, or law-revision data.

## Existing Artifacts

- `reports/empirical-validation-readiness.md`: raw-input readiness.
- `reports/empirical-validation-summary.md`: computed empirical summaries.
- `reports/empirical-bridge.md`: flow sanity-check mapping.
- `reports/empirical-validation-gap-report.md`: claim boundaries and missing areas.
- `reports/core-raw-validation-build.md`: current source-backed sample counts.
- `reports/calibration-baseline.md`: 7 / 7 broad conventional-baseline screens.
- `scripts/validation/`: validation and empirical-bridge scripts.

## Deliverables for Future Paper

1. Empirical signal taxonomy.
2. Mapping from empirical signal to simulator metric.
3. Claim boundary table:
   - validated;
   - sanity-checkable;
   - proxy only;
   - synthetic only;
   - not currently modeled.
4. Data pipeline plan.
5. Reproducibility plan.
6. Validation-readiness scorecard.
7. Missing-data roadmap.

## Current Go/No-Go

No-go for full paper draft.

Go for:

- source registry;
- expanded data inventory;
- missing-source acquisition plan;
- offline summary cache;
- metric-boundary reports;
- held-out validation design.

## Full Draft Gate

Draft only after:

- data pipeline includes substantially more than the current ready inputs;
- public support and campaign finance are integrated or explicitly replaced by a defensible alternative;
- implementation feedback or law revision data is integrated;
- source registry and reproducibility manifests are complete;
- held-out validation design exists;
- claims remain boundary-focused rather than validation-overclaiming.
