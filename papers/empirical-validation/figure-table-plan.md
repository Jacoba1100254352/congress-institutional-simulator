# Figure and Table Plan

## Future Main Figures

1. Validation pipeline diagram
   - Shows raw data, cached summaries, calibration screen, held-out checks, linkage audit, linkage roadmap, and gap reporting.

2. Flow-target observed versus simulated plot
   - Source: `reports/legislative-lifecycle-temporal-replication.csv` plus future broader held-out flow reports.
   - Current temporal metrics: committee advancement, floor consideration, and enactment with prespecified tolerance bands.
   - Preserve the failed enactment point-error check visually.

3. Empirical-boundary matrix
   - Rows: simulator metrics.
   - Columns: observable empirical targets.
   - Cell: direct, proxy, missing, or synthetic-only.

4. Public-support mapping figure
   - Future only.
   - Shows national, district, and affected-group support mapping if data exists.

## Future Main Tables

1. Empirical data inventory
   - Source, license, access, cached offline status, row count, fields, simulator proxy.

2. Calibration versus validation distinction
   - Calibration target, within-Congress held-out target, later-Congress target, error metric, tolerance, and pass/fail.

3. Current gap table
   - Start from `reports/empirical-validation-gap-report.csv`, `reports/empirical-linkage-report.csv`, and `reports/empirical-linkage-roadmap.csv`.
   - Add next data source and priority.

4. Proxy-risk table
   - Example: coalition size is not public opinion; party unity is not public support.

5. Validation-readiness scorecard
   - Source: `validation-boundary-table.md` and future `reports/empirical-data-inventory.csv`.
   - Columns: dimension, current status, score, missing upgrade, next command.

6. Missing-data roadmap
   - Source: `reports/empirical-validation-gap-report.csv`, `reports/empirical-linkage-report.csv`, and `reports/empirical-linkage-roadmap.csv`.
   - Rows: missing source families.
   - Columns: priority, next source, current boundary, dependent future papers.

## Appendix Tables

- Raw sample summaries from `reports/core-raw-validation-build.md`.
- Full `reports/empirical-bridge.csv`.
- Full `reports/empirical-linkage-report.csv`.
- Full `reports/empirical-linkage-roadmap.csv`.
- Full `reports/bill-law-evidence-spine.csv`.
- Full readiness/gap reports.
- Data licenses and access notes.

## Presentation Rules

- Do not title any table "validation" unless it includes held-out empirical checks.
- Use "flow sanity checks" for the current evidence.
- Make missing data visible rather than burying it in limitations.
