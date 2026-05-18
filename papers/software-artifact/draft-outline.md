# Extended Draft Outline

Status: outline only. A full software paper should wait for license, citation metadata, documentation, and clean-checkout reproduction.

## 1. Summary

- Congress Institutional Simulator is a Java 21 toolkit for synthetic legislative mechanism stress tests.
- It supports Makefile-first campaign generation, diagnostics, paper assets, and offline reproduction.
- Scope: simulation and reproducible experimentation, not empirical prediction of Congress.

## 2. Statement of Need

- Researchers need inspectable tools for comparing institutional mechanisms under shared synthetic assumptions.
- Existing manuscripts often under-document generator assumptions and reproducibility paths.
- This artifact provides a reusable simulator and reporting workflow.

## 3. Software Architecture

- Core simulator.
- Institutional modules.
- Campaign runners.
- Reporting scripts.
- Validation/sanity-check scripts.
- Paper-generation pipeline.

## 4. Functionality

- Run default simulation.
- Run canonical campaign.
- Run chamber, ablation, manipulation, and seed robustness diagnostics.
- Generate reports and figures.
- Build ACM paper and ODD+D appendix.
- Build anonymous supplement.

## 5. Reproducibility

- Fixed seeds.
- No-network reproduction target.
- Expected runtimes.
- Output directories.
- PDF manifest and checks.
- Network-dependent optional data rebuilds.

## 6. Quality Control

- Java tests.
- Calibration screen.
- Seed robustness check.
- Anonymity check.
- Figure/table consistency checks.
- PDF render check.

## 7. Reuse and Extension

- Adding a mechanism.
- Adding a campaign.
- Adding a metric.
- Adding a report.
- Boundaries for empirical claims.

## 8. Availability

- License.
- Citation metadata.
- DOI/release archive.
- Repository location.
- This section should not be drafted until release metadata exists.

## 9. Conclusion

- Main contribution after hardening: a reproducible legislative-mechanism simulation toolkit with transparent outputs and paper-generation workflow.
