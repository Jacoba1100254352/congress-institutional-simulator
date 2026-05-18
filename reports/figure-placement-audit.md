# Figure Placement Audit

Date: 2026-05-09

Audited artifacts:

- `paper/acm-ci-framework/acm-ci-framework.pdf`
- `paper/technical-appendix/odd-d-appendix.pdf`

Method:

- Scanned LaTeX figure and table declarations.
- Used `pdftotext -layout` to map tables and figures to PDF pages.
- Rendered main-paper pages 4--9 at 150 dpi and visually checked figure placement, caption separation, and large figure-induced blank regions.
- Checked generated picture coordinates for the value-profile matrix so drawn content stays inside the LaTeX box.

## Main Paper Placement Map

| Page | Floating/Display Content | Placement Assessment |
|---:|---|---|
| 3--4 | Figure 1, Table 1 | Pipeline and compact assumptions table now carry the simulator setup. |
| 5 | Table 2 and empirical flow table | Metric glossary and empirical boundary checks are setup material, not Results tables. |
| 6 | Mechanism-family table and Results opening | Mechanism labels appear once before the tradeoff displays. |
| 7 | Figure 2 | Productivity/risk-control and productivity/compromise plots carry the main tradeoff story. |
| 8 | Figure 3 and Table 4 | Metric-profile heatmap plus compact robustness summary replace the former dense results-table stack. |
| 9 | Limitations, Reproducibility, LLM disclosure, Conclusion | No side-experiment figure interrupts the close. |
| 10 | References | Natural reference-list pagination. |

## Appendix Placement Map

The ODD+D appendix contains the full numeric result tables, objective-frontier table, ablation/stress table, rising-contention figure, and chamber-structure supplement. These are intentionally outside the ACM main-paper argument.

## Findings And Fixes

1. The lifecycle pseudocode table was replaced with a pipeline figure.
2. The generator and vote-weight tables were merged into one compact assumptions table, with exact formulas moved to the appendix.
3. The main numeric result table, Pareto table, ablation/stress table, robustness detail table, chamber supplement, and rising-contention figure were moved to appendix material.
4. The main paper now renders as a tighter ACM framework paper, with dense diagnostics available but no longer driving the main Results section.

Residual note: the reference section has normal bibliography pagination. The appendix remains table-heavy by design.
