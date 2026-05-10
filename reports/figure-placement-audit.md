# Figure Placement Audit

Date: 2026-05-09

Audited artifacts:

- `paper/main.pdf`
- `paper/appendix-odd-d.pdf`

Method:

- Scanned LaTeX figure and table declarations.
- Used `pdftotext -layout` to map tables and figures to PDF pages.
- Rendered main-paper pages 4--9 at 150 dpi and visually checked figure placement, caption separation, and large figure-induced blank regions.
- Checked generated picture coordinates for the value-profile matrix so drawn content stays inside the LaTeX box.

## Main Paper Placement Map

| Page | Floating/Display Content | Placement Assessment |
|---:|---|---|
| 4 | Table 1, design-space index | Good. The table is followed by explanatory campaign text; no figure-induced blank page. |
| 5 | Table 2 and Figure 1, chamber-family champion scatter | Good. The table and figure are adjacent to the chamber-supplement discussion and the Results opening. |
| 6 | Tables 3--6, main comparison and diagnostics | Dense but acceptable. This page is table-heavy by design and avoids large blank regions. |
| 7 | Figure 2, two productivity tradeoff plots | Good after adjustment. The figure remains near the Results discussion and the page continues into the Results synthesis. |
| 8 | Figures 3--4, value-profile matrix and rising-contention timeline | Good after adjustment. The matrix caption no longer overlaps the graphic; the matrix and timeline now share one page instead of forcing consecutive half-empty pages. |
| 9 | Limitations, Reproducibility, LLM disclosure, Conclusion | No figures. Text now starts cleanly after the Results figures rather than being interrupted by a floating figure mid-paragraph. |
| 10--11 | References | No figures. Natural reference-list pagination. |

## Appendix Placement Map

The ODD+D appendix has no figure floats. Its large content blocks are text sections and generated supplemental tables, including the new empirical validation-boundary table. I did not find figure-driven white space in the appendix.

## Findings And Fixes

1. Figure 3 originally drew below its declared LaTeX `picture` height. That caused the caption to collide with the matrix and made the rendered page misleadingly sparse. The figure generator now uses a tighter row height and a declared picture box that contains all rows.
2. Figures 2--4 were forced with `[H]`, which caused consecutive half-empty pages when a following figure narrowly missed the remaining space. Figure 2 now has flexible placement, while Figures 3--4 are scaled and held together in the Results block so they do not interrupt Limitations text.
3. The main paper now renders as 11 pages instead of 12 pages, with the affected figures distributed across pages 7--8 without caption overlap or figure-only pages.

Residual note: the reference section has normal bibliography pagination, and the main comparison table page is intentionally dense. Neither is a figure-placement problem.
