# Figure and Table Plan

## Main Figures

1. Mechanism-effect decomposition plot
   - Source: `reports/simulation-campaign-v21-paper.csv` plus new paired-difference report.
   - Shows paired differences from `CUR` and `SM` for productivity, revision moderation, public support, risk control, and admin cost.
   - Purpose: distinguish threshold changes from content-transformation changes.

2. Generator-world sensitivity plot
   - Source: new generator-correlation campaign plus existing adversarial cases in `reports/scenario-selection-manifest.md`.
   - Shows how family-level results change across moderation-friendly, reform-friendly, public-opinion-error, and lobbying-information worlds.

3. Cost-budget fairness plot
   - Source: new cost-budgeted fairness campaign.
   - Shows output/risk tradeoffs under equal process budgets.

4. Two-dimensional stress plot
   - Source: new two-dimensional policy campaign.
   - Shows whether SEL, PORT, CUR, and SM shift when policy is multidimensional.

## Main Tables

1. Institutional hypotheses table
   - Columns: hypothesis, mechanism families, expected direction, tested metrics.
   - Purpose: make the political-science contribution explicit.

2. Mechanism-family summary table
   - Use fewer rows than the ACM appendix.
   - Combine PAIR/AMT as `SEL`.

3. Generator assumptions table
   - Include the moderation-friendly public-benefit assumption.
   - Explicitly mark synthetic, not empirical.

4. Empirical flow sanity checks table
   - Source: `reports/calibration-baseline.csv`, `reports/empirical-bridge.csv`.
   - Title must remain modest: "Flow sanity checks", not validation.

## Appendix Tables

- Full scenario averages from `reports/simulation-campaign-v21-paper.csv`.
- Seed robustness from `reports/seed-robustness-summary.csv`.
- Family champions from `reports/family-champions.md`.
- Exact scenario catalog from `reports/scenario-selection-manifest.md`.

## Tables to Avoid in the Main Paper

- A full 212-column metric export.
- Any table that presents PAIR and AMT as independent top-performing mechanisms.
- Mean plus case half-range as the only uncertainty display.
