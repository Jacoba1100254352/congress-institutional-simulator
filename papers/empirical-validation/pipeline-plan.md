# Data Pipeline and Reproducibility Plan

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

## Pipeline Goal

Build a reproducible benchmark-data pipeline that makes empirical signals available for calibration, sanity checks, and future validation without overstating what each signal proves.

## Current Commands

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make validation-readiness
make empirical-bridge
make validation-gap-report
make calibration-check
```

Optional network/data rebuilds:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-core-raw-validation
```

## Current Inputs and Outputs

Inputs under current readiness workflow:

- `voteview_rollcalls.csv`
- `bill_progression.csv`
- `lobbying_disclosure.csv`
- `topic_throughput.csv`
- `sponsor_success.csv`
- `committee_activity.csv`

Missing configured inputs:

- `district_public_opinion.csv`
- `campaign_finance.csv`
- `court_review.csv`
- `rulemaking_implementation.csv`
- `law_revision_history.csv`
- `comparative_institutions.csv`

Outputs:

- `reports/empirical-validation-readiness.csv`
- `reports/empirical-validation-summary.csv`
- `reports/empirical-bridge.csv`
- `reports/empirical-validation-gap-report.csv`
- `reports/calibration-baseline.csv`

## Proposed Pipeline Stages

### Stage 1: Source Registry

Create:

- `data/validation/source-registry.csv`
- `reports/empirical-data-inventory.csv`

Fields:

- source family;
- specific source;
- access method;
- license/terms;
- API key required;
- network required;
- cache path;
- refresh command;
- row count;
- date range;
- unit of observation;
- simulator metric family;
- boundary category.

### Stage 2: Raw Fetch and Cache

Rules:

- Network fetches should be optional.
- Offline artifact review must use cached summaries.
- API keys must not be required for core reproduction.
- Raw-data transformations should write provenance manifests.

Candidate targets:

```make
fetch-congressgov-bill-history
fetch-govinfo-billstatus
fetch-voteview-rollcalls
fetch-lda-lobbying
fetch-openfec-finance
fetch-committee-activity
fetch-rulemaking-implementation
```

### Stage 3: Normalization

Normalize every source into a stable schema:

- observation ID;
- chamber/session/date;
- bill or issue identifier;
- actor identifier;
- issue/topic/domain;
- action type;
- amount/count/share;
- source provenance;
- transformation notes.

### Stage 4: Empirical Signal Summaries

Produce one summary table per signal family:

- bill flow;
- roll-call behavior;
- lobbying concentration;
- campaign finance;
- topic throughput;
- sponsor effectiveness;
- district opinion;
- committee process;
- court review;
- implementation feedback;
- law revision;
- comparative institutions.

### Stage 5: Metric Mapping and Boundary Classification

For each summary statistic:

- map to simulator metric/proxy;
- assign boundary category;
- define target range or validation target if appropriate;
- mark unsupported claims.

### Stage 6: Calibration and Held-Out Validation

Current state: broad calibration/sanity screens only.

Future requirements:

- define calibration period and held-out period;
- separate target-setting data from evaluation data;
- report errors, tolerance rules, and failures;
- preserve synthetic-only labels for unsupported metrics.

## Reproducibility Plan

Required:

- no-network path for current reports;
- cached raw summaries for paper-facing claims;
- source manifests with date, query, row count, and schema version;
- deterministic scripts for transformations;
- checks for missing required columns;
- clear separation of fixture data from empirical data;
- no API keys in repository.

Suggested targets:

```make
empirical-data-inventory
empirical-refresh-optional
empirical-summarize-offline
empirical-boundary-report
empirical-heldout-check
```

## Quality Gates

Before this can become a data/resource paper:

- at least 10 / 12 source families have usable raw or cached summary inputs;
- public support and campaign finance are no longer missing;
- implementation or law-revision data is present;
- source registry documents licensing/access;
- held-out validation design exists;
- all paper-facing results regenerate offline.
