# Claims Ledger

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST. DO NOT DRAFT SOFTWARE PAPER YET.

| ID | Claim | Supporting evidence currently available | Limitation | Citation or evidence needed | Status |
|---|---|---|---|---|---|
| S1 | The artifact builds and tests through a Makefile-first workflow in the current checkout. | `Makefile`; `README.md`; `make test` passed under Java 21 on 2026-06-05. | Current checkout is not a clean clone. | Clean-clone reproduction log. | Supported for current checkout only. |
| S2 | The artifact is designed to reproduce the ACM paper outputs offline. | `README.md`; `make reproduce-paper-offline`; `paper/pdf-manifest.json`; generated paper PDFs. | Clean-clone reproduction has not been logged; TeX/PDF bytes may vary. | Clean-clone offline reproduction log and tolerance notes. | Conditional. |
| S3 | The simulator is implemented in Java 21 with generated reports under `reports/`. | Source tree, Makefile, root README, reports directory. | Need software-facing architecture and output-schema docs for outside users. | `docs/architecture.md`; `docs/output-schema.md`. | Supported as implementation claim. |
| S4 | The project includes empirical and validation-related scripts. | `scripts/validation`; `reports/empirical-*`; `reports/calibration-baseline.*`. | These scripts perform flow sanity checks, not model validation. | Data-source documentation if discussed. | Supported with boundary language. |
| S5 | The project includes ODD+D-style model documentation. | `docs/odd-model.md`; `docs/odd-d-appendix.md`; `paper/technical-appendix/odd-d-appendix.pdf`. | Appendix is dense and not a software API guide. | Standalone architecture/extension docs. | Supported as documentation claim. |
| S6 | The repository is a complete public software artifact. | No. Current audit found no root `LICENSE`, `CITATION.cff`, or `codemeta.json`. | Missing packaging and release metadata. | License, citation metadata, release/archive plan, clean-clone log. | Not supported. |
| S7 | The software can be cited or archived as a released artifact. | No formal release/archive metadata found. | Needs target venue and archival DOI plan. | Release tag, archive metadata, venue instructions. | Not supported. |
| S8 | The software validates or forecasts real legislative outcomes. | No. Current ACM paper and empirical gap reports explicitly avoid this claim. | The simulator remains synthetic and assumption-dependent. | Would require independent empirical validation. | Unsafe claim. |

## Safe Claim Language

- "The current checkout builds and tests under Java 21."
- "The repository contains Makefile targets for paper reproduction and anonymous supplement generation."
- "The simulator implements modular mechanism families and emits reproducible campaign reports under fixed seeds."
- "Empirical scripts support flow sanity checks and source inventory work, not predictive validation."

## Unsafe Claim Language

- "The software artifact is release-ready."
- "The package has been reproduced from a clean clone" until the log exists.
- "The simulator validates Congress."
- "The software paper can use the ACM results as empirical validation."
