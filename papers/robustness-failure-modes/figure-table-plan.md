# Figure and Table Plan

## Main Figures

1. Attack-budget degradation curves
   - Source: new `attack-budget-sweep` outputs.
   - X-axis: adversary budget.
   - Y-axis: degradation in risk control, low-support enactment, or admin cost.
   - One panel per major attack family.

2. Mechanism failure-mode matrix
   - Rows: attack types.
   - Columns: mechanism families.
   - Cell: worst-case degradation or qualitative vulnerability.

3. Defense cost-benefit plot
   - X-axis: administrative cost.
   - Y-axis: attack reduction.
   - Shows whether defenses merely shift the failure mode into overload.

4. Ablation waterfall
   - Source: `reports/simulation-ablation-analysis.csv`.
   - Shows the effect of removing alternatives, mediation, harm review, lobbying safeguards, or correction.

## Main Tables

1. Adversary model table
   - Objective, information, budget, action set, success criterion.

2. Attack library table
   - Attack, targeted mechanism, implementation, expected failure mode.

3. Worst-case summary table
   - Mechanism family, worst attack, largest degradation, remaining safeguard.

4. Current baseline stress table
   - Summarize current `ablation-analysis` and `manipulation-stress` outputs as pilot evidence only.

## Appendix Tables

- Full ablation numeric deltas from `reports/simulation-ablation-analysis.csv`.
- Full manipulation-stress numeric deltas from `reports/simulation-manipulation-stress.csv`.
- Attack-intensity sweep results.
- Seed robustness for selected adversarial cases.

## Presentation Rules

- Do not mix ablations and adversarial attacks in the same main table.
- Use consistent sign conventions: positive values should always mean worse degradation in stress tables, or explicitly invert all metrics.
- Report worst-case outcomes alongside averages.
