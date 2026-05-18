# Figure and Table Plan

Final decision: NEEDS ADVERSARY EXPERIMENTS FIRST.

## Required Main Tables

1. Adversary taxonomy table
   - Source: `adversary-model.md`.
   - Columns: actor type, objective, information, budget, strategy set, success metric, worst-case degradation metric.

2. Mechanism vulnerability matrix
   - Rows: mechanism families.
   - Columns: attack types.
   - Cell: robust, partial vulnerability, high vulnerability, untested, or not applicable.

3. Attack experiment design table
   - Rows: required experiments 1-9.
   - Columns: target mechanisms, adversary, budget, information, success metric, output report.

4. Recovery/correction table
   - Rows: attack types.
   - Columns: correction mechanism, recovery rate, residual harm, admin cost.

## Required Main Figures

1. Worst-case degradation plot
   - X-axis: mechanism family.
   - Y-axis: worst-case degradation under attack.
   - Facet by attack family or use small multiples.

2. Attack success rate plot
   - X-axis: adversary budget.
   - Y-axis: success rate.
   - Lines for information levels.

3. Robustness/cost frontier
   - X-axis: administrative burden under attack.
   - Y-axis: risk-control retention or attack-resistance score.
   - Shows whether safeguards survive without overload.

4. Median versus worst-case degradation plot
   - Shows whether average/median behavior hides catastrophic cases.

5. Failure trace diagrams for 2-3 mechanisms
   - Required examples:
     - clone/decoy content-selection failure;
     - astroturf or harm-claim overload;
     - strategic silence or proposal flooding under burden-shifting.

## Required Appendix Tables

- Full attack-budget sweep output.
- Full failure traces.
- Current pilot manipulation-stress table from `reports/manipulation-stress-summary.md`.
- Current ablation table from `reports/ablation-analysis-summary.md`.
- Seed robustness for selected adversarial cases.

## Presentation Rules

- Do not report only average degradation.
- Use consistent sign conventions: higher degradation values should mean worse attack outcomes.
- Mark untested attack/mechanism cells explicitly.
- Do not rank mechanisms as generally better; rank vulnerabilities under specified adversary models only.
- Keep current pilot stress results separate from new explicit-adversary results.
