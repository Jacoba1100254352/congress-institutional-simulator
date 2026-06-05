# Claims Ledger

## Status

Current claim level: benchmark-readiness planning only. No claim in this folder supports saying the simulator is empirically validated.

Allowed language now: "current artifacts support flow smoke tests and empirical-boundary mapping."

Disallowed language now: "the simulator is validated," "public support is empirically validated," "Voteview validates representation," or "empirical checks validate mechanism rankings."

## Ledger

| ID | Proposed claim | Supporting evidence currently available | Limitation | Citation needed | Allowed wording now | Status |
|---|---|---|---|---|---|---|
| C1 | The project has empirical flow smoke tests for the conventional benchmark. | `reports/calibration-baseline.md` reports 7 / 7 checks passed. | These are broad flow screens, not held-out validation of model behavior. | Legislative productivity and flow measurement. | The conventional benchmark passes current flow smoke tests. | Supported as smoke test. |
| C2 | Current empirical samples include bill progression, roll calls, lobbying, topics, sponsors, and committee summaries. | `reports/core-raw-validation-build.md`; `reports/empirical-validation-readiness.md`; `reports/empirical-bridge.csv`. | Six of twelve raw source families are ready; samples remain bounded. | Congress.gov, Voteview, LDA, CAP, CEL, and committee-data documentation. | Six empirical source families are currently shaped for summaries. | Supported as inventory. |
| C3 | Current checks do not validate public benefit, revision moderation, harm, capture, or public support. | `reports/empirical-validation-gap-report.md`; ACM paper caveats. | This limitation prevents a validation paper now. | Simulation validation and empirical measurement literature. | Central welfare/support/harm/capture metrics remain synthetic or proxy-only. | Supported as boundary. |
| C4 | A future validation paper needs separate calibration, plausibility screening, and held-out evaluation. | Current pipeline has broad pass/fail screens but no train/test or held-out workflow. | No implemented held-out validation workflow yet. | Model validation in agent-based and computational social science. | Held-out validation is required future work. | Planning-supported. |
| C5 | Public opinion and affected-group support are the most important missing representation inputs. | `reports/empirical-validation-gap-report.md` lists public support as high-priority missing. | No MRP/CCES-style raw input or issue mapping currently exists. | Public-opinion measurement and representation literature. | Public support remains synthetic until district/affected-group data are integrated. | Supported as gap. |
| C6 | Campaign finance and lobbying-to-bill linkage are required before influence/capture validation. | LDA summary exists; OpenFEC/campaign-finance raw input is missing. | Lobby spending concentration is not bill-level capture. | Lobbying, campaign finance, and interest-group measurement. | Current influence checks are proxy-only. | Supported as gap. |
| C7 | Implementation feedback and law revision are required before correction-over-time validation. | `rulemaking_implementation.csv` and `law_revision_history.csv` are missing. | Law registry, sunset, rollback, and implementation-delay outputs remain synthetic. | Rulemaking, implementation, statutory lineage, and repeal/reauthorization literature. | Correction metrics remain synthetic until implementation and lineage data exist. | Supported as gap. |
| C8 | Roll-call coalition size and party unity are not public opinion. | `reports/empirical-bridge.csv` maps them only to coalition/support proxies; caveats are explicit. | Must avoid treating legislative coalitions as public-support validation. | Representation and public-opinion measurement. | Coalition metrics are proxy-only. | Supported as boundary. |
| C9 | A data/resource paper is ready for full drafting. | No. | Source registry, high-priority missing data, and held-out checks are absent. | Data/resource paper standards and reproducibility literature. | No full paper yet. | No-go. |

## Evidence Thresholds

A claim can move from boundary/planning to draft-ready only after it has:

- a named empirical source and source-registry row;
- a raw or cached summary artifact with row count and date range;
- a transformation script or documented manual extraction path;
- an explicit simulator metric/proxy mapping;
- a boundary category;
- a calibration-versus-held-out distinction when the claim uses validation language;
- a citation target for the empirical source and measurement construct.
