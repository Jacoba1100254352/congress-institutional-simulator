# Stage 6: Software and Artifact Paper

## Go/No-Go Decision

Conditional go for artifact hardening. No-go for software-paper drafting until the repository passes a clean reproducibility and packaging audit.

Primary workspace: `papers/software-artifact/`.

## Repo Tasks

- Add an explicit `LICENSE` if this is intended to be public reusable software.
- Add `CITATION.cff`.
- Add optional `codemeta.json`.
- Add documentation:
  - `docs/architecture.md`
  - `docs/adding-a-mechanism.md`
  - `docs/adding-a-campaign.md`
  - `docs/output-schema.md`
  - `docs/reproducibility.md`
- Add a clean-checkout reproduction log.
- Confirm anonymous artifact packaging excludes old drafts, strategy notes, and local metadata.
- Add or document deterministic-output tolerances for CSV and PDF artifacts.

## Experiments to Run

Artifact verification:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
make reproduce-paper-offline
make supplement-anonymous
```

Clean-checkout audit:

```sh
tmpdir=$(mktemp -d)
git clone . "$tmpdir/congress-institutional-simulator"
cd "$tmpdir/congress-institutional-simulator"
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
make reproduce-paper-offline
```

New targets to add:

```make
artifact-smoke
artifact-schema-check
artifact-release-check
artifact-offline-check
```

## Figures and Tables to Generate

Required:

- Software architecture diagram.
- Reproduction workflow diagram.
- Output artifact map.
- Artifact capabilities table: command, output, offline status, runtime.
- Package/module table.
- Reproducibility checklist.
- Output schema table.

Appendix:

- Full Make target list.
- Dependency/version log.
- Clean-checkout reproduction log.
- Release checklist.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| The software builds and tests through a Makefile-first workflow. | `Makefile`, `make test`. | Must pass clean-checkout audit. | Conditional. |
| The artifact reproduces paper-facing outputs offline. | `make reproduce-paper-offline`, README. | TeX/PDF byte variance needs tolerance documentation. | Conditional. |
| The repo is ready for a software paper now. | Not supported. | Missing license/citation/release metadata. | No-go. |
| A software artifact paper would be independent from ACM framework claims. | It could focus on reproducibility and reuse. | Must not retell mechanism results as novelty. | Conditional. |

## Paper Outline

Draft only after packaging audit:

1. Summary.
2. Statement of need.
3. Software architecture.
4. Functionality and command workflow.
5. Reproducibility.
6. Quality control.
7. Reuse and extension.
8. Availability, license, and citation.
9. Conclusion.
