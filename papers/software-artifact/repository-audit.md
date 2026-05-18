# Repository Readiness Audit

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

Audit date: current workspace pass.

## Summary

The repository is strong as a paper artifact but not yet ready as a standalone open-source software publication.

Hard blockers:

- no `LICENSE` file found;
- no `CITATION.cff` found;
- no `codemeta.json` found;
- no clean-clone reproduction log found;
- no formal release/archive metadata found.

Current verification performed in this pass:

- `make test` was run with Java 21 selected explicitly and passed.
- root README, docs, Makefile targets, source layout, tracked PDFs, and metadata files were inspected.

## Audit Table

| Criterion | Status | Evidence | Gap / task |
|---|---|---|---|
| Build works from clean clone | not verified | Current checkout builds during `make test`; no clean-clone log found. | Run clean-clone audit and record output. |
| Java version pinned | mostly pass | Makefile uses `JAVA_RELEASE ?= 21` and `javac --release 21`; root README requires Java 21. | Optional: add `.java-version` or toolchain note for public users. |
| Makefile targets documented | pass | Root `README.md` and `docs/usage.md` document `make test`, `make run`, `make campaign`, `make paper-checks`, `make reproduce-paper-offline`, and diagnostics. | Keep docs synchronized with Makefile. |
| No-network reproduction path works | target exists, not verified this pass | `make reproduce-paper-offline` target exists and README documents it. | Run in clean clone and save reproduction log. |
| Random seeds fixed | pass for core campaigns | Makefile campaign targets use fixed seed `20260428`; ODD docs describe seeded deterministic runs. | Add reproducibility doc with seed policy and stochastic tolerance. |
| Generated outputs tracked or reproducible | partial pass | `reports/`, `paper/figures/`, PDFs, and `paper/pdf-manifest.json` exist; paper checks regenerate them. | Add output schema/inventory and clean-regeneration expectations. |
| Tests pass | pass in current checkout | `make test` passed with Java 21. | Add clean-clone test log. |
| Figures/tables regenerate | target exists, not verified this pass | `make paper-assets`, `make paper-checks`, and `paper/scripts/generate_figures.py` exist. | Run `make reproduce-paper-offline` during packaging audit. |
| Artifact anonymity separation works | target exists, not verified this pass | `make supplement-anonymous`; README describes exclusions. | Run target and inspect bundle contents. |
| Stale drafts removed | mostly pass | Tracked PDFs are descriptive: `acm-ci-framework.pdf`, `odd-d-appendix.pdf`; no tracked `main.pdf` found. | Ensure `paper/notes/` and planning docs are excluded from anonymous/public artifacts as appropriate. |
| Root README is reproduction-focused | pass | Root README is titled "Reproducing the ACM CI Framework Paper" and lists commands/outputs. | For software publication, add user/developer installation sections or link to docs. |
| Code organization understandable | partial pass | Packages are organized by `behavior`, `calibration`, `experiment`, `institution/*`, `model`, `simulation`, `reporting`, and `util`; docs exist. | Add `docs/architecture.md` and extension guides. |
| License exists | fail | No `LICENSE*` or `COPYING*` found. | Add project license before software submission. |
| Citation file exists | fail | No `CITATION.cff` found. | Add citation metadata before software submission. |
| Dependency list exists | partial/fail | README lists Java 21, GNU Make, Python 3, LaTeX; project has no external Java dependencies. | Add formal dependency/environment file or `docs/reproducibility.md`. |
| Model documentation exists | pass | `docs/odd-model.md`, `docs/odd-d-appendix.md`, and `paper/technical-appendix/odd-d-appendix.pdf`. | Summarize for software-paper audience. |
| Empirical inputs separated from core reproduction | pass | README separates optional network-dependent inputs from offline reproduction. | Add source registry if publishing data-resource artifact. |

## Current Build/Test Evidence

Command run:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
```

Observed result:

```text
All simulator tests passed.
```

## Required Before Software Paper Draft

1. Add `LICENSE`.
2. Add `CITATION.cff`.
3. Add optional `codemeta.json`.
4. Add clean-clone reproduction log.
5. Run and record:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
```

6. Add architecture and extension documentation.
7. Add release/archive plan.
8. Confirm anonymous and public artifact bundles exclude stale drafts and strategy notes.
