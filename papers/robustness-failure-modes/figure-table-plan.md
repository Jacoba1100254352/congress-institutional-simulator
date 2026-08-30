# Figure and Table Plan

## Status

Readiness level: figure/table specifications are ready; most figures cannot be generated until adversary experiments are implemented.

## Main Tables

| ID | Table | Purpose | Source | Readiness |
|---|---|---|---|---|
| T1 | Scope and overlap boundary | Show how this paper differs from the ACM framework and other breakout papers. | `paper-plan.md` | Ready now. |
| T2 | Adversary model table | Define actor type, objective, information, budget, strategy set, success metric, and degradation metric. | `reports/adversary-catalog.md` and `adversary-model.md` | Ready as generated design table. |
| T3 | Attack experiment design | Map each first-wave attack to target mechanisms, budgets, information levels, and outputs. | `experiment-plan.md` | Ready as design table. |
| T4 | Claims ledger | Separate supported, conditional, unsupported, and deferred claims. | `claims-ledger.md` | Ready now. |
| T5 | Mechanism vulnerability matrix | Report robust, partial vulnerability, high vulnerability, untested, or not applicable by attack family. | Future adversarial-stress output. | Not ready. |
| T6 | Recovery/correction table | Report recovery rate, residual harm, and admin cost by attack type. | A7 queue-recovery and A8 same-case signal-correction pilots plus future adversarial-stress output. | Partial: bounded A7 queue recovery and A8 signal correction only. |
| T7 | Validation-needs table | List internal checks, empirical data gaps, and modeling weaknesses. | `validation-needs.md` | Ready now. |
| T8 | Mixed-attack interaction table | Compare strongest single attack against fixed-budget mixed adversary portfolios. | `reports/adversarial-stress-a9-summary.md` | Ready as A9 pilot appendix only. |
| T9 | Pilot failure-trace candidate index | Rank aggregate manipulation-stress comparisons that should receive full traces first. | `reports/adversarial-failure-trace-index.md` | Ready as pilot appendix only. |
| T10 | Pilot adversary cell map | Show which A1-A9 adversaries currently have only aggregate stress proxies and which have no pilot cell. | `reports/adversarial-pilot-cell-map.md` | Ready as pilot appendix only. |
| T11 | A1 clone/decoy adversarial-stress summary | Report budget, information level, success rate, median/worst degradation, and trace counts for the first executable A1 pilot. | `reports/adversarial-stress-summary.md` | Ready as A1 pilot appendix only. |
| T12 | A2 poison-pill/sequencing adversarial-stress summary | Report budget, information level, success rate, median/worst degradation, and trace counts for the first executable A2 pilot. | `reports/adversarial-stress-a2-summary.md` | Ready as A2 pilot appendix only. |
| T13 | A3 public-input adversarial-stress summary | Report budget, information level, success rate, false-positive blockage, false-negative clearance, public-signal movement, administrative burden, and trace counts for the first executable A3 pilot. | `reports/adversarial-stress-a3-summary.md` | Ready as A3 pilot appendix only. |
| T14 | A4 bad-faith harm-claim adversarial-stress summary | Report budget, success rate, false-positive harm-review burden, false-negative clearance, concentrated-harm passage, administrative burden, and trace counts for the first executable A4 pilot. | `reports/adversarial-stress-a4-summary.md` | Ready as A4 pilot appendix only. |
| T15 | A5 proposal-flooding adversarial-stress summary | Report budget, information level, success rate, high-benefit crowdout, high-benefit blockage, low-support flood enactment, proposal-load, floor-slot, policy-yield, administrative burden, and trace counts for the first executable A5 pilot. | `reports/adversarial-stress-a5-summary.md` | Ready as A5 pilot appendix only. |
| T16 | A6 lobbying-camouflage adversarial-stress summary | Report budget, information level, success rate, anti-capture bypass, capture enactment added, visible-spend decline with capture persistence, shadow-share movement, detection decline, observed screen-risk decline, administrative burden, and trace counts for the first executable A6 pilot. | `reports/adversarial-stress-a6-summary.md` | Ready as A6 pilot appendix only. |
| T17 | A7 administrative-overload adversarial-stress summary | Report budget, information level, capacity saturation, queue overflow, overflow fallback, latent-risk control failure, administrative burden, and post-attack recovery cycles. | `reports/adversarial-stress-a7-summary.md` | Ready as A7 pilot appendix only. |
| T18 | A8 public-support-distortion adversarial-stress summary | Report mechanism path, budget, information level, residual signal distortion, generated-support error, decision failures, false consensus/opposition, and same-case signal correction. | `reports/adversarial-stress-a8-summary.md` | Ready as A8 pilot appendix only. |
| T19 | A9 mixed-adversary adversarial-stress summary | Report exact joint allocation, strongest same-budget single control, mixed-only success, interaction degradation, superadditive loss, administrative burden, and bounded recovery/correction outcomes. | `reports/adversarial-stress-a9-summary.md` | Ready as A9 pilot appendix only. |

## Main Figures

| ID | Figure | Purpose | Source | Readiness |
|---|---|---|---|---|
| F1 | Attack-budget degradation curves | Show how degradation changes across low, medium, and high budgets. | Future `attack-budget-sweep` output. | Not ready. |
| F2 | Median versus worst-case degradation | Show whether average/median behavior hides catastrophic cases. | Future `worst-case-degradation-report` output. | Not ready. |
| F3 | Attack success heatmap | Show success rates by adversary, mechanism family, budget, and information level. | Future adversarial-stress summary. | Not ready. |
| F4 | Robustness/cost frontier | Compare risk-control retention against administrative burden under attack. | Future defense-cost sweep. | Not ready. |
| F5 | Failure trace diagrams | Explain 2-3 concrete paths from adversary action to institutional outcome. | Future failure traces. | Not ready. |
| F6 | Recovery/correction plot | Show whether review, substitute selection, rollback, or routing correction reduces attack harm. | A7 queue-recovery and A8 same-case signal-correction pilots plus future correction metrics. | Partial: bounded queue recovery and signal correction only. |
| F7 | Mixed-attack interaction plot | Show whether mixed adversary portfolios create additive, subadditive, or superadditive degradation. | `reports/adversarial-stress-a9-summary.csv` | Partial: bounded A9 source data exist; multi-seed uncertainty is missing. |

## Appendix Tables

| ID | Appendix item | Source |
|---|---|---|
| A1 | Current manipulation-stress pilot summary. | `reports/manipulation-stress-summary.md` |
| A2 | Current ablation pilot summary. | `reports/ablation-analysis-summary.md` |
| A3 | Aggregate pilot failure-trace candidate index. | `reports/adversarial-failure-trace-index.md` |
| A4 | Generated adversary catalog and pilot cell map. | `reports/adversary-catalog.md`; `reports/adversarial-pilot-cell-map.md` |
| A5 | A1 executable clone/decoy stress summary. | `reports/adversarial-stress-summary.md` |
| A6 | A1 executable per-bill failure traces. | `reports/adversarial-failure-traces.jsonl` |
| A7 | A2 executable poison-pill/sequencing stress summary. | `reports/adversarial-stress-a2-summary.md` |
| A8 | A2 executable per-bill failure traces. | `reports/adversarial-failure-traces-a2.jsonl` |
| A9 | A3 executable public-input manipulation stress summary. | `reports/adversarial-stress-a3-summary.md` |
| A10 | A3 executable per-bill failure traces. | `reports/adversarial-failure-traces-a3.jsonl` |
| A11 | A4 executable bad-faith harm-claim stress summary. | `reports/adversarial-stress-a4-summary.md` |
| A12 | A4 executable per-bill failure traces. | `reports/adversarial-failure-traces-a4.jsonl` |
| A13 | A5 executable proposal-flooding stress summary. | `reports/adversarial-stress-a5-summary.md` |
| A14 | A5 executable per-original-bill failure traces. | `reports/adversarial-failure-traces-a5.jsonl` |
| A15 | A6 executable lobbying-camouflage stress summary. | `reports/adversarial-stress-a6-summary.md` |
| A16 | A6 executable per-bill failure traces. | `reports/adversarial-failure-traces-a6.jsonl` |
| A17 | A7 executable administrative-overload stress summary. | `reports/adversarial-stress-a7-summary.md` |
| A18 | A7 executable per-bill failure and recovery traces. | `reports/adversarial-failure-traces-a7.jsonl` |
| A19 | A8 executable public-support-distortion stress summary. | `reports/adversarial-stress-a8-summary.md` |
| A20 | A8 executable per-bill direct-signal and correction traces. | `reports/adversarial-failure-traces-a8.jsonl` |
| A21 | A9 executable mixed-adversary stress summary. | `reports/adversarial-stress-a9-summary.md` |
| A22 | A9 executable mixed and single-control traces. | `reports/adversarial-failure-traces-a9.jsonl` |
| A23 | Full A1-A9 attack-budget sweep output. | Future expanded adversarial-stress summaries |
| A24 | Full per-bill failure trace index for A1-A9. | Future expanded trace artifact under `reports/` or `out/` |
| A25 | Seed robustness for selected adversarial cases. | Future adversarial seed sweep |
| A26 | Validation gap matrix. | `validation-needs.md` plus future validation reports |

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
