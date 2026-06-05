# Figure and Table Plan

## Status

Readiness level: figure/table specifications are ready; most figures cannot be generated until adversary experiments are implemented.

## Main Tables

| ID | Table | Purpose | Source | Readiness |
|---|---|---|---|---|
| T1 | Scope and overlap boundary | Show how this paper differs from the ACM framework and other breakout papers. | `paper-plan.md` | Ready now. |
| T2 | Adversary model table | Define actor type, objective, information, budget, strategy set, success metric, and degradation metric. | `adversary-model.md` | Ready as design table. |
| T3 | Attack experiment design | Map each first-wave attack to target mechanisms, budgets, information levels, and outputs. | `experiment-plan.md` | Ready as design table. |
| T4 | Claims ledger | Separate supported, conditional, unsupported, and deferred claims. | `claims-ledger.md` | Ready now. |
| T5 | Mechanism vulnerability matrix | Report robust, partial vulnerability, high vulnerability, untested, or not applicable by attack family. | Future adversarial-stress output. | Not ready. |
| T6 | Recovery/correction table | Report recovery rate, residual harm, and admin cost by attack type. | Future adversarial-stress output. | Not ready. |
| T7 | Validation-needs table | List internal checks, empirical data gaps, and modeling weaknesses. | `validation-needs.md` | Ready now. |
| T8 | Mixed-attack interaction table | Compare strongest single attack against fixed-budget mixed adversary portfolios. | Future mixed adversary output. | Not ready. |

## Main Figures

| ID | Figure | Purpose | Source | Readiness |
|---|---|---|---|---|
| F1 | Attack-budget degradation curves | Show how degradation changes across low, medium, and high budgets. | Future `attack-budget-sweep` output. | Not ready. |
| F2 | Median versus worst-case degradation | Show whether average/median behavior hides catastrophic cases. | Future `worst-case-degradation-report` output. | Not ready. |
| F3 | Attack success heatmap | Show success rates by adversary, mechanism family, budget, and information level. | Future adversarial-stress summary. | Not ready. |
| F4 | Robustness/cost frontier | Compare risk-control retention against administrative burden under attack. | Future defense-cost sweep. | Not ready. |
| F5 | Failure trace diagrams | Explain 2-3 concrete paths from adversary action to institutional outcome. | Future failure traces. | Not ready. |
| F6 | Recovery/correction plot | Show whether review, substitute selection, rollback, or routing correction reduces attack harm. | Future recovery metrics. | Not ready. |
| F7 | Mixed-attack interaction plot | Show whether mixed adversary portfolios create additive, subadditive, or superadditive degradation. | Future mixed adversary output. | Not ready. |

## Appendix Tables

| ID | Appendix item | Source |
|---|---|---|
| A1 | Current manipulation-stress pilot summary. | `reports/manipulation-stress-summary.md` |
| A2 | Current ablation pilot summary. | `reports/ablation-analysis-summary.md` |
| A3 | Full attack-budget sweep output. | Future `reports/adversarial-stress-summary.csv` |
| A4 | Full failure trace index. | Future trace artifact under `reports/` or `out/` |
| A5 | Seed robustness for selected adversarial cases. | Future adversarial seed sweep |
| A6 | Validation gap matrix. | `validation-needs.md` plus future validation reports |

## Required Visual Standards

- Show current pilot stress results separately from new explicit-adversary results.
- Do not rank mechanisms as generally better; rank vulnerability only under named adversaries.
- Use consistent signs: positive degradation should always mean worse attacked outcome.
- Mark untested cells explicitly.
- Include budget and information levels in labels or facets.
- Show worst-case values next to median or mean values.
- Avoid broad summary graphics that imply a full mechanism catalog.

## Figure Generation Needs

Future reporting scripts should produce machine-readable intermediate files before plot generation:

- `reports/adversarial-stress-summary.csv`;
- `reports/adversarial-budget-sweep.csv`;
- `reports/adversarial-worst-case-degradation.csv`;
- `reports/adversarial-recovery-summary.csv`;
- `reports/adversarial-mixed-attack-summary.csv`;
- `reports/adversarial-failure-trace-index.csv`.

After those exist, figures can be generated under `paper/figures/` or a breakout-specific figure folder if this paper becomes a manuscript.
