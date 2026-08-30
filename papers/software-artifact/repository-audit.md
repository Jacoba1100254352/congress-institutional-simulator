# Repository Readiness Audit

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

Audit date: 2026-07-27 workspace metadata pass.

## Summary

The repository is strong as a paper artifact but not yet ready as a standalone open-source software publication.

Hard blockers:

- no `LICENSE` file found;
- no clean-clone reproduction log found;
- no tagged release or DOI/archive record found.

Current verification performed in this pass:

- `make test` was run with Java 21 selected explicitly and passed.
- Repository metadata search found `CITATION.cff`, `codemeta.json`, `RELEASE.md`, and `.java-version` at depth 2. It still found no `LICENSE*` or `COPYING*`.
- Stale draft search found no tracked `main*.pdf`, `main*.tex`, or `*draft*.pdf` files at depth 3.
- Root `README.md` was inspected and is reproduction-focused.
- root README, docs, Makefile targets, source layout, tracked PDFs, and metadata files were inspected.
- `make supplement-anonymous-current` passed on 2026-07-27 after the report whitelist was updated; archive inspection confirmed the official finance/lobbying source-review reports, member-vote target review, statutory-lineage source-gap review, and target-reference resolution reports were included, while identity-bearing public metadata (`CITATION.cff`, `codemeta.json`, `RELEASE.md`), `papers/`, `paper/notes/`, `no-include/`, and `.git/` were absent.

## Audit Table

| Criterion | Status | Evidence | Gap / task |
|---|---|---|---|
| Build works from clean clone | not verified | Current checkout builds during `make test`; no clean-clone log found. | Run clean-clone audit and record output. |
| Java version pinned | pass | Makefile uses `JAVA_RELEASE ?= 21`, `javac --release 21`, root README requires Java 21, and `.java-version` records `21`. | Keep Java 21 selected in clean-clone audit. |
| Makefile targets documented | pass | Root `README.md` and `docs/usage.md` document `make test`, `make run`, `make campaign`, `make paper-checks`, `make reproduce-paper-offline`, and diagnostics. | Keep docs synchronized with Makefile. |
| No-network reproduction path works | target exists, not verified this pass | `make reproduce-paper-offline` target exists and README documents it. | Run in clean clone and save reproduction log. |
| Random seeds fixed | pass for core campaigns | Makefile campaign targets use fixed seed `20260428`; ODD docs and `docs/reproducibility.md` describe seeded deterministic runs. | Keep seed policy synchronized with Makefile changes. |
| Generated outputs tracked or reproducible | partial pass | `reports/`, `paper/figures/`, PDFs, `paper/pdf-manifest.json`, and `docs/output-schema.md` exist; paper checks regenerate them. | Add clean-clone reproduction log. |
| Tests pass | pass in current checkout | `make test` passed with Java 21. | Add clean-clone test log. |
| Figures/tables regenerate | target exists, not verified this pass | `make paper-assets`, `make paper-checks`, and `paper/scripts/generate_figures.py` exist. | Run `make reproduce-paper-offline` during packaging audit. |
| Artifact anonymity separation works | pass in current checkout | `make supplement-anonymous-current` passed on 2026-07-27; archive inspection found the newly whitelisted source-review reports present and identity-bearing public metadata plus planning/private folders absent. | Repeat from clean clone before software submission. |
| Stale drafts removed | mostly pass | Tracked PDFs are descriptive: `acm-ci-framework.pdf`, `odd-d-appendix.pdf`; no tracked `main.pdf` found. | Ensure `paper/notes/` and planning docs are excluded from anonymous/public artifacts as appropriate. |
| Root README is reproduction-focused | pass | Root README is titled "Reproducing the ACM CI Framework Paper" and lists commands/outputs. | For software publication, add user/developer installation sections or link to docs. |
| Code organization understandable | pass | Packages are organized by `behavior`, `calibration`, `experiment`, `institution/*`, `model`, `simulation`, `reporting`, and `util`; `docs/architecture.md` and extension guides exist. | Keep docs synchronized with source changes. |
| License exists | fail | No `LICENSE*` or `COPYING*` found in current audit. | Choose and add a project license before software submission. |
| Citation file exists | pass | Root `CITATION.cff` exists with software title, author, repository, candidate version, abstract, and keywords. | Update version, DOI, and release date after public archival release. |
| CodeMeta metadata exists | pass | Root `codemeta.json` exists with software description, repository, runtime, requirements, author/maintainer, and candidate version. | Update DOI, license, and final version after public archival release. |
| Dependency list exists | partial pass | README and `docs/reproducibility.md` list Java 21, GNU Make, Python 3, and LaTeX; project has no external Java dependencies. | Add clean-clone environment log before software submission. |
| Model documentation exists | pass | `docs/odd-model.md`, `docs/odd-d-appendix.md`, and `paper/technical-appendix/odd-d-appendix.pdf`. | Summarize for software-paper audience. |
| Empirical inputs separated from core reproduction | pass | README separates optional network-dependent inputs from offline reproduction. | Add source registry if publishing data-resource artifact. |

## Current Build/Test Evidence

Command run:

```sh
env JAVA_HOME="$(/usr/libexec/java_home -v 21)" PATH="$(/usr/libexec/java_home -v 21)/bin:$PATH" make test
```

Observed result:

```text
All simulator tests passed.
```

## Required Before Software Paper Draft

1. Choose and add `LICENSE`.
2. Add clean-clone reproduction log.
3. Run and record from a clean clone:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
```

4. Keep architecture, output-schema, extension, and reproducibility documentation current.
5. Finalize release/archive metadata after a tagged release and DOI/archive exist.
6. Confirm anonymous and public artifact bundles exclude stale drafts and strategy notes.

## Audit Commands Used

```sh
find . -maxdepth 2 \( -iname 'LICENSE*' -o -iname 'COPYING*' -o -iname 'CITATION.cff' -o -iname 'codemeta.json' -o -iname 'RELEASE*' -o -iname '.java-version' \) -print | sort
find . -maxdepth 3 -type f \( -iname 'main*.pdf' -o -iname '*draft*.pdf' -o -iname 'main*.tex' \) -print | sort
find docs -maxdepth 1 -type f -print | sort
ls -1 paper/acm-ci-framework/*.pdf paper/technical-appendix/*.pdf
```

The metadata search still lacks license files; `.java-version`, `CITATION.cff`, `codemeta.json`, and `RELEASE.md` are now expected. The stale-draft search returned no matching files except the expected current descriptive PDFs under `paper/acm-ci-framework/` and `paper/technical-appendix/`.
