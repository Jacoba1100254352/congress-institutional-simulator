# Experiment Plan

## Current Evidence Baseline

Start from the canonical campaign and diagnostics:

```sh
make campaign
make seed-robustness
make findings-validation
make calibration-check
```

Primary input files:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/scenario-selection-manifest.md`
- `reports/paper-findings-validation.md`
- `reports/seed-robustness-summary.csv`
- `reports/calibration-baseline.csv`

## Required New Experiment 1: Two-Dimensional Policy Space

Purpose: test whether content-selection, amendment, compromise, and package-bargaining patterns survive when policy is not a one-dimensional line.

Implementation tasks:

- Add issue-position vectors for bills and ideal-point vectors for legislators.
- Support Euclidean or separable status-quo-relative utility.
- Compute public support and harm by issue or affected group rather than only scalar support.
- Add a campaign case such as `two-dimensional-policy`.

Minimum outputs:

- Productivity, revision moderation, public support, low-support enactment, risk control, admin cost.
- Paired comparison against current one-dimensional baseline.
- A failure-case note if PAIR/AMT diverge or cycling/agenda dependence appears.

## Required New Experiment 2: Cost-Budgeted Fairness Controls

Purpose: test whether content-selection mechanisms outperform because they receive more proposal-improvement opportunities.

Design:

- Match `CUR`, `SM`, `SEL`, `PORT`, and burden-shifting systems on an explicit process budget.
- Budget should include information gain, amendment count, mediation opportunities, review slots, and challenge/objection slots.
- Add administrative-cost ceiling as a hard constraint, not only a metric.

Minimum outputs:

- Table of budget assumptions.
- Paired differences against `CUR` and `SM`.
- Sensitivity to low, medium, and high process budgets.

## Required New Experiment 3: Generator Correlation Worlds

Purpose: make generator dependence the object of analysis instead of a limitation note.

Required worlds:

- Moderation-friendly baseline.
- Reform-friendly high-distance proposals.
- Public-support-lags-benefit world.
- Lobbying-information world.
- Capture-confounded lobbying world.
- Majority-support-with-minority-harm world.

Minimum outputs:

- Family-level pattern table.
- Distribution plot of changes in top family or paired regret.
- Explicit statement of which findings reverse.

## Required New Experiment 4: Statistical Presentation

Purpose: avoid treating scenario half-ranges like confidence intervals.

Tasks:

- Compute seed variance separately from scenario variation.
- Generate median and IQR by mechanism family.
- Generate paired within-world differences versus `CUR` and `SM`.
- Add bootstrap intervals only where the sampling interpretation is appropriate.

## New Data or Validation Work

- Expand empirical flow checks beyond the current 7/7 plausibility screens.
- Add held-out checks if possible: floor scheduling, committee reporting, coalition size, veto frequency, topic mix, and sponsor concentration.
- Do not claim validation of public benefit, public support, harm, capture, or revision moderation unless new empirical targets are added.

## Proposed New Targets

Potential Make targets:

```make
political-science-campaign
cost-budget-fairness
two-dimensional-sensitivity
paired-difference-report
```

These should write outputs under `reports/`, not inside the paper folder.
