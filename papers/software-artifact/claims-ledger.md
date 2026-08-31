# Claims Ledger

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST. DO NOT DRAFT SOFTWARE PAPER YET.

| ID | Claim | Supporting evidence currently available | Limitation | Citation or evidence needed | Status |
|---|---|---|---|---|---|
| S1 | The artifact builds and tests through a Makefile-first workflow in the current checkout. | `Makefile`; `README.md`; `make test` passed under Java 21 on 2026-07-02. | Current checkout is not a clean clone. | Clean-clone reproduction log. | Supported for current checkout only. |
| S2 | The artifact is designed to reproduce the ACM paper outputs offline. | `README.md`; `make reproduce-paper-offline`; `paper/pdf-manifest.json`; generated paper PDFs. | Clean-clone reproduction has not been logged; TeX/PDF bytes may vary. | Clean-clone offline reproduction log and tolerance notes. | Conditional. |
| S3 | The simulator is implemented in Java 21 with generated reports under `reports/`. | Source tree, Makefile, root README, reports directory, `docs/architecture.md`, and `docs/output-schema.md`. | Software-facing docs must be kept synchronized with future source and output changes. | Clean-clone reproduction and release metadata before public artifact claims. | Supported as implementation claim. |
| S4 | The project includes empirical and validation-related scripts. | `scripts/validation`; `reports/empirical-*`; paired GovInfo census reports; `reports/legislative-lifecycle-calibration.*`; `reports/legislative-lifecycle-temporal-replication.*`. | These scripts perform source audits, proxy checks, and one narrow no-refit aggregate-flow transport test, not general model validation. | Data-source and claim-boundary documentation if discussed. | Supported with boundary language. |
| S5 | The project includes ODD+D-style model documentation and software-facing extension docs. | `docs/odd-model.md`; `docs/odd-d-appendix.md`; `paper/technical-appendix/odd-d-appendix.pdf`; `docs/adding-a-mechanism.md`; `docs/adding-a-campaign.md`; `docs/reproducibility.md`. | Documentation still needs clean-clone reproduction evidence and release metadata before publication claims. | Clean-clone reproduction log and artifact-bundle audit. | Supported as documentation claim. |
| S6 | The repository is a complete public software artifact. | No. Current audit found root `CITATION.cff`, `codemeta.json`, and `RELEASE.md`, but no root `LICENSE` and no clean-clone reproduction log. | Missing license choice, clean-clone evidence, and final release/archive metadata. | License, clean-clone log, release tag, archive/DOI metadata, and public bundle audit. | Not supported. |
| S7 | The software can be cited or archived as a released artifact. | Pre-release citation and CodeMeta files exist, and `RELEASE.md` records the release checklist. | Needs final tagged release, chosen license, archival DOI/URL, release date, and clean-clone evidence. | Release tag, archive metadata, DOI or archive URL, venue instructions. | Conditional metadata only; not supported as released artifact. |
| S8 | The software validates or forecasts real legislative outcomes. | No. Current ACM paper and empirical gap reports explicitly avoid this claim. | The simulator remains synthetic and assumption-dependent. | Would require independent empirical validation. | Unsafe claim. |

## Safe Claim Language

- "The current checkout builds and tests under Java 21."
- "The repository contains Makefile targets for paper reproduction and anonymous supplement generation."
- "The simulator implements modular mechanism families and emits reproducible campaign reports under fixed seeds."
- "Empirical scripts support source inventory work, flow checks, and one narrow no-refit temporal transport test, not predictive or general model validation."

## Unsafe Claim Language

- "The software artifact is release-ready."
- "The package has been reproduced from a clean clone" until the log exists.
- "The simulator validates Congress."
- "The software paper can use the ACM results as empirical validation."
