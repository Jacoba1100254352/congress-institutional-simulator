# Paper Plan: Empirical Validation

## Working Title

From Flow Sanity Checks to Validation: Empirical Boundaries for a Legislative Mechanism Simulator

## Target Venue Category

Future computational social science, political methodology, data/resource, or simulation-validation venue.

## One-Sentence Contribution

The paper would develop and test an empirical validation program for mapping observed legislative data to simulator quantities such as agenda flow, coalition structure, lobbying concentration, public support, harm, implementation feedback, and correction.

## Why This Is Not Redundant With the ACM CI Paper

The ACM paper intentionally limits empirical material to flow sanity checks. This breakout would be a validation/data paper only after new empirical datasets and mappings are added.

## Current Readiness Decision

Only a future-work plan. Not ready for an extended empirical manuscript.

The current empirical files are useful but too small and too indirect for an independent validation paper.

## Existing Artifacts and Results It Can Use

- `reports/calibration-baseline.csv` and `.md`: 7/7 flow checks passed for the conventional benchmark.
- `reports/empirical-bridge.csv` and `.md`: 19 rows of empirical comparison material.
- `reports/empirical-validation-gap-report.csv` and `.md`: 12 rows of validation gap reporting.
- `reports/empirical-validation-readiness.csv` and `.md`: readiness checks.
- `reports/empirical-validation-summary.csv` and `.md`: summary outputs.
- `reports/core-raw-validation-build.md`: current raw sample counts.
- `reports/public-api-sample-fetch.md`: public API sample-fetch notes.
- Validation scripts under `scripts/validation/`.

Current raw samples include a 180-row Congress.gov-derived bill-progression extract and smaller Voteview, LDA, topic, sponsor, and committee summaries. These do not validate synthetic welfare, support, harm, capture, or correction metrics.

## Missing Experiments or Validation Needed Before Submission

- District-level public opinion data mapped to bills, issue domains, or roll calls.
- Campaign finance and lobbying data linked to proposal access, sponsorship, and votes.
- Court review, law revision, implementation, and rollback data.
- Cross-national institutional comparison data.
- Held-out validation targets and a real train/test distinction.
- A validation design that separates calibration, plausibility screening, and prediction.
- Error metrics and tolerance rules.

## Go/No-Go Recommendation

No-go for a paper. Go only for a staged validation workplan.

## Next Concrete Commands or Repo Tasks

Current checks:

```sh
make validation-readiness
make validation-gap-report
make empirical-bridge
make calibration-check
```

Optional network-dependent rebuilds:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-core-raw-validation
```

Required new work:

- Add a data inventory with licenses, identifiers, and reproducibility status.
- Add no-network cached summaries for every empirical check.
- Add held-out comparison targets before using the word validation in a title.
