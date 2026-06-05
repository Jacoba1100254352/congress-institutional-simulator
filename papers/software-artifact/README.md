# Software / Artifact Paper Plan

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST. DO NOT DRAFT SOFTWARE PAPER YET.

This folder evaluates whether the Congress Institutional Simulator can become a standalone open-source software paper, model-description paper, or artifact publication. It is not a results paper and should not repackage the ACM CI framework paper's empirical or mechanism-comparison claims.

## Working Purpose

Evaluate whether the simulator is sufficiently documented, tested, packaged, and reusable to support a software or model-description publication.

## Primary Question

Is the simulator sufficiently documented, tested, packaged, and reusable to support a software or model-description publication?

## Current Answer

Not yet.

The simulator has a strong internal artifact workflow: Java 21 enforcement, Makefile-first commands, tests, reproducible campaign targets, paper checks, ODD/ODD+D documentation, and an anonymous supplement builder. The repository is not yet ready for a software publication because the packaging layer is incomplete: no license file, no citation metadata, no clean-clone reproduction log, and no release/archival metadata were found.

## Required Files

- `go-no-go.md`: explicit software-paper readiness gate.
- `repository-audit.md`: readiness audit against software/artifact criteria.
- `software-paper-plan.md`: contribution statement, venue fit, and go/no-go.
- `model-documentation-summary.md`: ODD/ODD+D-style model summary.
- `reproducibility-checklist.md`: clean-reproduction and packaging checklist.
- `draft-outline.md`: short paper outline only.

Existing planning files such as `paper-plan.md`, `claims-ledger.md`, `experiment-plan.md`, `figure-table-plan.md`, and `related-work-targets.md` remain supplemental notes.

## Full Draft Rule

Do not draft a software paper unless the repository passes the reproducibility and packaging audit.

## Next Concrete Repo Tasks

1. Add a root `LICENSE`, `CITATION.cff`, and optional `codemeta.json`.
2. Add `docs/architecture.md`, `docs/output-schema.md`, `docs/adding-a-mechanism.md`, `docs/adding-a-campaign.md`, and `docs/reproducibility.md`.
3. Run a clean-clone audit with `make test`, `make reproduce-paper-offline`, and `make supplement-anonymous`.
4. Save the clean-clone log and artifact-bundle audit before drafting a software paper.
