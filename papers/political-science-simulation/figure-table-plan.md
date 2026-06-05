# Figure and Table Plan

Final decision: NEEDS DATA/VALIDATION FIRST.

## Required Main Tables

1. Political mechanism inventory
   - Rows: `CUR`, `SM`, `COMM`, `DIS`, `OPEN`, `VETO`, `BIC`, `ACG`, `CAP`, `SEL`, optional `PORT`.
   - Columns: political construct, implemented scenario, source module, empirical target, readiness.

2. Theory-to-mechanism mapping
   - Rows: spatial voting, pivotal politics, veto-player theory, committee gatekeeping, agenda control, lobbying, legislative effectiveness, public-support representation.
   - Columns: model representation, metric, validation target, limitation.

3. Empirical validation boundary table
   - Source: `validation-plan.md`, `reports/empirical-validation-gap-report.md`.
   - Must mark synthetic-only metrics clearly.

4. Benchmark fairness-control table
   - Lists conventional + committee information gain, conventional + negotiated amendment, conventional + conference compromise, simple majority + mediation, simple majority + committee revision, and cost-constrained comparisons.

5. Baseline calibration target table
   - Source: expanded `political-baseline-calibration`.
   - Keep as plausibility/calibration, not full validation.

6. Go/no-go and evidence threshold table
   - Source: `go-no-go.md` and `claims-ledger.md`.
   - Purpose: show why the current package is not yet a full draft.

## Required Main Figures

1. Paired mechanism comparison plot
   - Differences versus `CUR` and `SM` within matched synthetic worlds.

2. Cost-constrained fairness tradeoff plot
   - Productivity, public-support failure, capture, and admin cost under equal review/amendment/attention budgets.

3. Parameter sweep small multiples
   - Polarization, party loyalty, lobbying pressure, constituency pressure, agenda gate selectivity, and committee information quality.

4. Public-benefit/support sensitivity matrix
   - Shows whether findings change when support and generated benefit are decoupled.

5. Uncertainty decomposition figure
   - Separates seed variance from scenario variation.

## Appendix Tables

- Full scenario averages from `reports/simulation-campaign-v21-paper.csv`.
- Scenario selection manifest.
- Seed robustness from `reports/seed-robustness-summary.csv`.
- Empirical gap report.
- Chamber or bicameral details if referenced, but keep chamber-specific material limited.

## Figures and Tables to Avoid

- A giant all-metric campaign table in the main text.
- Separate PAIR and AMT rows as independent evidence unless new divergence is demonstrated.
- A portfolio-hybrid table that makes `PORT` look like a recommended design.
- Any display that treats synthetic public support as observed opinion.
- Any table that reports `PAIR` and `AMT` as independent robustness evidence unless new divergence is shown.
- Any plot that ranks `PORT` as a recommended institutional design.
