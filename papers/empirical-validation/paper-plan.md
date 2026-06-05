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

## Why This Is Not Redundant With The ACM CI Framework Paper

The ACM CI paper contributes the simulator architecture and a synthetic framework demonstration. This breakout would contribute empirical boundary infrastructure: a source registry, validation-readiness scorecard, metric-to-signal mapping, held-out-check design, and missing-data roadmap that other simulation papers can reuse. It should not repeat the ACM mechanism comparison or claim that the framework is validated.

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
- `data/validation/raw/`: six current raw empirical summaries.
- `data/validation/fixtures/`: adapter fixtures, intentionally ignored by readiness scoring.
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

## Required New Code Or Data Work

Before a full paper draft:

1. Add `data/validation/source-registry.csv` with licensing, access, date range, row count, cache path, network/API requirement, and simulator-boundary category.
2. Add a generated `reports/empirical-data-inventory.csv` and Markdown companion.
3. Add raw or cached summaries for at least public opinion, campaign finance, implementation feedback, and law revision, or explicitly justify replacements.
4. Add a held-out flow-check target that reports error/tolerance rather than only pass/fail broad ranges.
5. Keep adapter fixtures separate from raw empirical summaries and preserve the no-network review path.

## Next Concrete Commands

Current refresh:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make validation-readiness
make empirical-validation
make empirical-bridge
make validation-gap-report
make calibration-check
```

Future targets to add:

```make
empirical-data-inventory
empirical-flow-heldout
empirical-summarize-offline
empirical-boundary-report
```

## Full Draft Gate

Draft only after:

- data pipeline includes substantially more than the current ready inputs;
- public support and campaign finance are integrated or explicitly replaced by a defensible alternative;
- implementation feedback or law revision data is integrated;
- source registry and reproducibility manifests are complete;
- held-out validation design exists;
- claims remain boundary-focused rather than validation-overclaiming.
