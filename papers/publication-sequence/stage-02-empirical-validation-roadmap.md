# Stage 2: Empirical-Validation and Data Roadmap

## Go/No-Go Decision

Go for a data roadmap and validation work package. No-go for an empirical-validation paper draft.

This stage creates value because it supports the later political-science and chamber papers. It defines validation boundaries, data sources, held-out targets, and proxy risks before anyone writes stronger mechanism claims. The current implementation now includes complete paired 117th/118th GovInfo H.R./S. censuses and one frozen no-refit temporal transport test, but remains below the threshold for an empirical-validation paper.

Primary workspace: `papers/empirical-validation/`.

## Repo Tasks

- Expand `papers/empirical-validation/experiment-plan.md` into an implementation checklist.
- Add a machine-readable empirical data inventory under `reports/`.
- Separate current flow sanity checks from future validation targets.
- Add cached no-network summaries for any empirical input used in paper-facing claims.
- Add a validation-target registry that records:
  - source,
  - observable signal,
  - simulator proxy,
  - metric supported,
  - what the signal cannot validate,
  - offline availability,
  - license/access constraints.
- Keep current terminology modest: "flow sanity checks", not validation.

Current lifecycle milestone:

- complete source-pinned 117th- and 118th-Congress H.R./S. censuses;
- frozen 117th-Congress threshold selection across 50 simulator seeds;
- no-refit 118th-Congress test passing committee advancement and floor consideration;
- retained enactment miss of 0.000825 beyond the prespecified tolerance;
- classifier-v2 audit for context-dependent GovInfo presidential-action coding.

## Experiments to Run

Current baseline:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make validation-readiness
make empirical-bridge
make empirical-linkage-report
make empirical-linkage-roadmap
make sponsor-bill-linkage
make bill-law-evidence-spine
make campaign-finance-district-context
make campaign-finance-sponsor-bill-context
make bill-finance-lobbying-local-context-review
make bill-finance-lobbying-external-search-review
make bill-finance-lobbying-external-lda-mention-review
make bill-finance-lobbying-campaign-finance-target-scope-review
make bill-finance-lobbying-committee-action-context
make bill-finance-lobbying-source-acquisition-queue
make validation-gap-report
make calibration-check
make legislative-lifecycle-temporal-replication
make govinfo-bill-census-check
```

Optional network-dependent rebuilds:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-govinfo-billstatus-linkage-raw
make build-core-raw-validation
make build-sponsor-bill-linkage-raw
```

New targets to add before a paper is drafted:

Implemented targets:

```make
empirical-data-inventory
empirical-flow-heldout
legislative-lifecycle-calibration
legislative-lifecycle-temporal-replication
govinfo-bill-census-check
```

Remaining targets before a paper is drafted:

```make
empirical-public-support-map
empirical-lobbying-linkage
empirical-correction-map
```

## Figures and Tables to Generate

Required first outputs:

- Empirical data inventory table.
- Validation-boundary matrix: simulator metric by empirical observability.
- Flow sanity-check table for the conventional benchmark.
- Gap-priority table: missing source, target metric, next task.
- Proxy-risk table showing why coalition size, party unity, and floor flow are not public opinion or welfare validation.

Future outputs after data integration:

- Observed-versus-simulated flow plots.
- Held-out error/tolerance table.
- District/public-support mapping figure.
- Lobbying/capture linkage diagram.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| Current empirical material screens conventional flow plausibility and tests narrow temporal transport. | `reports/calibration-baseline.md`, `reports/empirical-bridge.csv`, paired GovInfo census reports, and `reports/legislative-lifecycle-temporal-replication.md`. | The no-refit test covers only three aggregate rates, and enactment fails its stricter tolerance. | Usable with explicit miss. |
| Current empirical material validates public support, public benefit, harm, capture, or correction. | Not supported. | These remain synthetic or unvalidated. | Exclude. |
| A data roadmap can identify validation targets for later papers. | Gap reports and validation scripts exist. | Requires new data integration before empirical paper. | Usable. |
| Political-science and chamber papers need stronger empirical boundaries. | Current limitations, gap reports, and the narrow temporal transport result. | One flow design is implemented, but mechanism-specific and representation validation remain missing. | Usable. |

## Paper Outline

Do not draft a paper yet. Use this future-paper outline only:

1. Motivation: why simulation claims need empirical boundaries.
2. Current flow sanity checks and what they support.
3. Validation taxonomy: calibration, plausibility screening, held-out validation.
4. Data inventory and proxy risks.
5. Planned validation targets for flow, public support, lobbying, harm, and correction.
6. Reproducibility and no-network data summaries.
7. Remaining gaps and dependency on new data.
