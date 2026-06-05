# Go/No-Go Decision

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST. DO NOT DRAFT SOFTWARE PAPER YET.

## Decision

No-go for a full software or model-description manuscript.

Go for artifact hardening and reproducibility packaging. This is currently one of the strongest breakout candidates after the ACM framework paper, but only if it becomes a clean, citable, reusable software artifact rather than a results paper.

## Current Readiness

| Gate | Current status | Evidence from this workspace pass |
|---|---|---|
| Current checkout builds/tests | Pass | `make test` passed under Java 21 on 2026-06-05. |
| Clean-clone reproduction | Not verified | No clean-clone log exists. |
| Offline reproduction target | Target exists, not clean-clone verified | `make reproduce-paper-offline` is documented and present. |
| Anonymous supplement audit | Target exists, not clean-clone verified | `make supplement-anonymous` is documented and present. |
| License metadata | Fail | No `LICENSE*` or `COPYING*` file found. |
| Citation metadata | Fail | No `CITATION.cff` found. |
| Software metadata | Fail | No `codemeta.json` found. |
| Architecture/extension docs | Partial | ODD docs exist; dedicated software architecture and extension docs are missing. |
| Release/archive metadata | Fail | No tagged release or DOI/archive plan recorded. |

## Proceed Now

- Add license, citation, and optional CodeMeta metadata.
- Add software-facing docs for architecture, outputs, adding a mechanism, adding a campaign, and reproduction tolerances.
- Run a clean-clone audit and save the log.
- Run `make reproduce-paper-offline` and `make supplement-anonymous` in the clean clone.
- Audit anonymous and public artifact bundles for stale drafts, planning notes, local paths, and identity-bearing metadata.

## Defer

- Full software manuscript.
- Claims that the simulator is public reusable software.
- Claims that the artifact is archived, citable, or DOI-ready.
- Claims that the simulator validates Congress or real legislative outcomes.

## Full Draft Conditions

Draft only after all of the following are true:

- a clean clone passes `make test`;
- a clean clone passes `make reproduce-paper-offline`;
- `make supplement-anonymous` builds and the bundle audit shows no planning/private files;
- license, `CITATION.cff`, and release/archive metadata exist;
- architecture, output-schema, extension, and reproducibility docs exist;
- the reproducibility checklist has no fail or unverified required items;
- the claims ledger contains only supported software/artifact claims.
