# Experiment Plan

## Current Empirical Baseline

Run:

```sh
make validation-readiness
make empirical-bridge
make validation-gap-report
make calibration-check
```

Current files:

- `reports/calibration-baseline.csv`
- `reports/empirical-bridge.csv`
- `reports/empirical-validation-gap-report.csv`
- `reports/empirical-validation-readiness.csv`
- `reports/empirical-validation-summary.csv`

## Stage 1: Data Inventory and Provenance

Tasks:

- List every empirical source, license, access method, cached summary, and reproducibility status.
- Mark which targets are available offline and which require network/API keys.
- Add stable IDs for samples and generated summaries.

Output:

- `reports/empirical-data-inventory.csv`
- `reports/empirical-data-inventory.md`

## Stage 2: Flow Validation Targets

Observable targets:

- Bill introduction to committee attrition.
- Committee reporting.
- Floor consideration.
- Roll-call coalition size.
- Veto frequency.
- Sponsor concentration.
- Topic throughput.

Tasks:

- Split samples into calibration and held-out checks.
- Define error metrics and tolerances.
- Report failures instead of only pass/fail screens.

## Stage 3: Representation and Public Support

Required data:

- District-level public opinion or issue preferences.
- Bill-topic or roll-call mapping.
- Constituency exposure or affected groups.

Tasks:

- Separate national support, district support, affected-group support, and intensity.
- Do not map party unity directly to public support.

## Stage 4: Lobbying and Capture

Required data:

- Lobbying disclosure linked to issues, sponsors, committees, or bill topics.
- Campaign finance if available and appropriate.
- Interest-group type or information-quality proxy if feasible.

Tasks:

- Split lobbying into pressure/access, private gain, information, and public persuasion.
- Test whether simulator capture diagnostics track observed concentration proxies.

## Stage 5: Correction and Implementation

Required data:

- Court review or challenge data.
- Law revision and sunset-review data.
- Implementation feedback or administrative burden proxies.

Tasks:

- Define active-law quality and correction over time.
- Add held-out comparison targets.

## Proposed Make Targets

```make
empirical-data-inventory
empirical-flow-heldout
empirical-public-support
empirical-lobbying-linkage
empirical-correction-data
```
