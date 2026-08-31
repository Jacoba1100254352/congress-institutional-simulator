# Stage 2: Empirical-Validation and Data Roadmap

## Go/No-Go Decision

Go for a data roadmap and validation work package. No-go for an empirical-validation paper draft.

This stage creates value because it supports the later political-science and chamber papers. It defines validation boundaries, data sources, held-out targets, and proxy risks before anyone writes stronger mechanism claims. The current implementation includes complete 116th-, 117th-, and 118th-Congress GovInfo H.R./S. lifecycle censuses, two frozen external-Congress no-refit temporal tests, and a compact 108th-118th-Congress executive-action boundary diagnostic, but remains below the threshold for an empirical-validation paper.

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

- complete source-pinned 116th-, 117th-, and 118th-Congress H.R./S. censuses;
- frozen 117th-Congress threshold selection across 50 simulator seeds;
- no-refit 116th- and 118th-Congress tests passing 5 / 6 aggregate cohort-metric tolerances;
- retained enactment miss of 0.000825 beyond the prespecified tolerance;
- classifier-v3 audit for context-dependent GovInfo presidential-action coding and two-chamber veto overrides;
- separate 108th-118th-Congress bill and joint-resolution decision panels plus final chamber approvals, retaining a 22.101-fold combined simulator-to-empirical veto-rate mismatch as a model boundary;
- one post-source-audit/pre-fit locked presidential-choice temporal study that passes its 118th-Congress log-loss and aggregate-calibration gate, with a post-fit warning that 12 of 13 test vetoes occur among only 17 joint resolutions.

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
| Current empirical material screens conventional flow plausibility, tests narrow temporal transport, and audits executive decisions across 11 Congresses. | `reports/calibration-baseline.md`, `reports/empirical-bridge.csv`, three GovInfo lifecycle census reports, separate decision/final-vote panels, `reports/legislative-lifecycle-temporal-replication.md`, `reports/legislative-executive-action-diagnostic.md`, and `reports/presidential-choice-study.md`. | The no-refit lifecycle tests cover only three aggregate rates in two external Congresses; 118th-Congress enactment fails its stricter tolerance. The locked presidential-choice gate passes, but its primary test events are concentrated in joint resolutions and the simulator veto rate remains badly mis-scaled. | Usable with explicit miss, narrow predictive result, concentration warning, and stress-mechanism boundary. |
| Current empirical material validates public support, public benefit, harm, capture, or correction. | Not supported. | These remain synthetic or unvalidated. | Exclude. |
| A data roadmap can identify validation targets for later papers. | Gap reports and validation scripts exist. | Requires new data integration before empirical paper. | Usable. |
| Political-science and chamber papers need stronger empirical boundaries. | Current limitations, gap reports, the two-cohort lifecycle result, executive-action diagnostic, and locked presidential-choice study. | One flow design and one concentrated predictive veto design are implemented, but broader mechanism-specific and representation validation remain missing. | Usable. |

## Paper Outline

Do not draft a paper yet. Use this future-paper outline only:

1. Motivation: why simulation claims need empirical boundaries.
2. Current flow sanity checks and what they support.
3. Validation taxonomy: calibration, plausibility screening, held-out validation.
4. Data inventory and proxy risks.
5. Planned validation targets for flow, public support, lobbying, harm, and correction.
6. Reproducibility and no-network data summaries.
7. Remaining gaps and dependency on new data.
