# Go/No-Go Decision

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST. DO NOT DRAFT SOFTWARE PAPER YET.

## Decision

No-go for a full software or model-description manuscript.

Go for artifact hardening and reproducibility packaging. This is currently one of the strongest breakout candidates after the ACM framework paper, but only if it becomes a clean, citable, reusable software artifact rather than a results paper.

## Current Readiness

| Gate | Current status | Evidence from this workspace pass |
|---|---|---|
| Current checkout builds/tests | Pass | `make test` passed under Java 21 on 2026-07-02. |
| Clean-clone reproduction | Not verified | No clean-clone log exists. |
| Offline reproduction target | Target exists, not clean-clone verified | `make reproduce-paper-offline` is documented and present. |
| Anonymous supplement audit | Pass in current checkout; clean clone not verified | `make supplement-anonymous-current` passed on 2026-07-27 after the report whitelist update; archive inspection found required source-review reports present and identity-bearing public metadata plus planning/private folders absent. |
| License metadata | Fail | No `LICENSE*` or `COPYING*` file found. |
| Citation metadata | Pass | Root `CITATION.cff` exists as pre-release software citation metadata; DOI/version metadata remains pending public archival release. |
| Software metadata | Pass | Root `codemeta.json` exists as pre-release CodeMeta metadata; DOI/license/final-version metadata remains pending public archival release. |
| Architecture/extension docs | Pass | `docs/architecture.md`, `docs/output-schema.md`, `docs/adding-a-mechanism.md`, `docs/adding-a-campaign.md`, and `docs/reproducibility.md` exist. |
| Release/archive metadata | Partial | Root `RELEASE.md` records a release checklist, but no tagged release, archive, DOI, or final release version exists. |

## Proceed Now

- Choose and add a license.
- Keep software-facing architecture, output, extension, and reproducibility docs synchronized with code changes.
- Run a clean-clone audit and save the log.
- Run `make reproduce-paper-offline` and `make supplement-anonymous` in the clean clone.
- After clean-clone reproduction passes, tag and archive a release, then update citation and CodeMeta metadata with final DOI/version/license fields.
- Repeat anonymous and public artifact bundle audits from the clean clone before claiming release readiness.

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
- architecture, output-schema, extension, and reproducibility docs exist and remain synchronized with the current code;
- the reproducibility checklist has no fail or unverified required items;
- the claims ledger contains only supported software/artifact claims.
