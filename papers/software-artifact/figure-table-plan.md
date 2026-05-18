# Figure and Table Plan

## Main Figures

1. Software architecture diagram
   - Source: code package structure and existing pipeline figure.
   - Shows CLI/Make targets, simulator core, mechanism modules, reporting scripts, paper-generation scripts, and outputs.

2. Reproduction workflow diagram
   - Shows `make test`, `make campaign`, `make mechanism-diagnostics`, `make paper`, `make paper-checks`, `make supplement-anonymous`.

3. Output artifact map
   - Shows source code, reports, paper PDFs, ODD+D appendix, figures, checks, and anonymous supplement bundle.

## Main Tables

1. Artifact capabilities table
   - Capability, command, output, offline status, expected runtime.

2. Package/module table
   - Package, responsibility, extension points.

3. Reproducibility checklist
   - Requirement, current status, evidence, missing work.

4. Data/output schema table
   - Key CSV, row count, purpose, core columns.

## Appendix Tables

- Full Make target list.
- Full output file inventory.
- Clean-checkout reproduction log.
- Dependency/version log.

## Presentation Rules

- Do not reprint the ACM paper's scientific results as the software paper's main evidence.
- The central evidence should be reproducibility, extensibility, documentation, and command coverage.
- Clearly label empirical scripts as sanity-check support, not validation.
