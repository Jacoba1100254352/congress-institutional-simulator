# Go/No-Go

## Current Decision

Go for benchmark-data pipeline planning.

No-go for a full empirical-validation or data/resource manuscript.

The current repository supports flow smoke tests and empirical-boundary mapping. It does not yet support a paper claiming validation of public support, public benefit, harm, capture, administrative cost, correction over time, or mechanism rankings.

## Readiness Level

| Level | Meaning | Current? |
|---|---|---|
| 0 | Idea only. | No. |
| 1 | Current flow checks and readiness reports exist. | Yes. |
| 2 | Source map, metric mapping, boundary table, and pipeline plan exist. | Yes, current level. |
| 3 | Source registry, expanded raw/cached data, and held-out checks exist. | No. |
| 4 | Full data/resource manuscript evidence is ready. | No. |

## Proceed Now

Proceed with:

- source registry;
- empirical data inventory report;
- public opinion and affected-group support sourcing;
- OpenFEC/campaign-finance sourcing;
- lobbying-to-bill or lobbying-to-topic linkage;
- implementation and law-revision sourcing;
- held-out flow-check design;
- offline summary cache and source manifests.

## Defer

Defer:

- a full empirical-validation manuscript;
- any claim that the simulator is validated;
- public-support or public-benefit validation claims;
- mechanism-ranking validation claims;
- cross-national fit claims;
- any table that labels proxy checks as validation.

## Full Draft Go Conditions

Move to manuscript drafting only when all of the following are true:

1. `data/validation/source-registry.csv` exists and covers every source family in `data-source-map.md`.
2. At least 10 of 12 source families have usable raw or cached summary inputs, or the paper scope is narrowed to a smaller explicitly named benchmark subset.
3. District public opinion or an explicitly justified representation substitute is integrated.
4. Campaign finance or a defensible influence-data substitute is integrated.
5. At least one implementation, law-revision, or court-review source is integrated.
6. Held-out flow checks exist and report error/tolerance behavior.
7. Offline reproduction regenerates all paper-facing summaries.
8. Every claim in `claims-ledger.md` has a boundary category and citation target.
9. The paper remains a benchmark/readiness paper, not a simulator-validation claim.

## Final Recommendation

Keep this as an empirical-foundation plan until the data pipeline is substantially expanded beyond the current six ready source families and broad flow smoke tests.
