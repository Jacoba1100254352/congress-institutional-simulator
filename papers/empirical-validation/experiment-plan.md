# Experiment Plan

## Current Empirical Baseline

Run:

```sh
make validation-readiness
make empirical-bridge
make empirical-linkage-report
make empirical-linkage-roadmap
make rulemaking-authority-linkage
make rulemaking-history-linkage
make bill-law-evidence-spine
make campaign-finance-district-context
make campaign-finance-issue-context
make campaign-finance-sponsor-bill-context
make validation-gap-report
make calibration-check
```

Current files:

- `reports/calibration-baseline.csv`
- `reports/empirical-data-inventory.csv`
- `reports/empirical-bridge.csv`
- `reports/empirical-flow-heldout.csv`
- `reports/empirical-linkage-report.csv`
- `reports/empirical-linkage-roadmap.csv`
- `reports/rulemaking-authority-linkage.csv`
- `reports/rulemaking-history-linkage.csv`
- `reports/bill-law-evidence-spine.csv`
- `reports/campaign-finance-district-context.csv`
- `reports/campaign-finance-issue-context.csv`
- `reports/campaign-finance-sponsor-bill-context.csv`
- `reports/empirical-validation-gap-report.csv`
- `reports/empirical-validation-readiness.csv`
- `reports/empirical-validation-summary.csv`
- `reports/validation-boundary-matrix.csv`

## Stage 1: Data Inventory and Provenance

Tasks:

- List every empirical source, license, access method, cached summary, and reproducibility status.
- Mark which targets are available offline and which require network/API keys.
- Add stable IDs for samples and generated summaries.

Output:

- `reports/empirical-data-inventory.csv`
- `reports/empirical-data-inventory.md`
- `reports/validation-boundary-matrix.csv`
- `reports/validation-boundary-matrix.md`

## Stage 2: Flow and Roll-Call Validation Targets

Observable targets:

- Bill introduction to committee attrition.
- Committee reporting.
- Floor consideration.
- Roll-call coalition size.
- Veto frequency.
- Sponsor concentration.
- Topic throughput.

Implemented v1 task:

- Split the committed bill-progression sample into deterministic calibration and held-out slices.
- Report held-out enactment and floor-load checks against current conventional-baseline tolerance ranges.
- Split the committed Voteview roll-call sample into deterministic calibration and held-out slices by roll-call ID.
- Report held-out coalition-size behavior against the current coalition/support tolerance range while keeping party unity as a reported proxy.
- Split the committed sponsor aggregate sample into deterministic calibration and held-out slices by sponsor ID.
- Report held-out sponsor-introduction concentration against the current proposer-access tolerance range while keeping enacted-success concentration as a reported proxy.
- Split bounded OpenFEC campaign-finance rows, Cumulative CES district-opinion rows, SCDB merits-case rows, Federal Register final-rule rows, Congress.gov public-law revision rows, and QoG/V-Dem comparative-institution rows into deterministic calibration and held-out slices.
- Report narrow held-out source-family proxy checks for campaign-finance concentration, outside-spending share, district public-will, turnout skew, merits-case invalidation, final-to-effective delay, implementation-speed proxy, public-law correction text flags, and bicameral context.

Implemented temporal-flow extension:

- Build complete source-pinned 116th-, 117th-, and 118th-Congress H.R./S. GovInfo censuses with record/action hashes, archive pins, and explicit source-date anomalies.
- Freeze threshold selection on the 117th calibration split, then apply the selected 0.68 threshold to all 116th and 118th rows without refitting.
- Preserve the prespecified 0.020 committee, 0.015 floor, and 0.010 enactment tolerances and report the 5 / 6 external cohort-metric result, including the 118th-Congress enactment miss.
- Audit classifier drift across Congresses; classifier v3 preserves the context-dependent `E30000` veto/signature fix, adds two-chamber veto-override classification, and leaves established 117th- and 118th-Congress funnel counts unchanged.
- Audit presented-bill accounting and conditional executive-action rates separately from lifecycle-threshold selection. Preserve the 79.157-fold pooled empirical-to-simulator veto-rate mismatch as a model boundary rather than introducing a post hoc pass/fail tolerance.

Remaining tasks:

- Add separate calibration and held-out extracts rather than a hash split of one bounded sample.
- Broaden roll-call and sponsor-access held-out checks across more Congresses and chambers, extend the no-refit GovInfo panel across more administrations, and add independent or held-out checks for topic throughput, lobbying, and committee activity.
- Report error metrics for more targets instead of only broad tolerance membership.

## Stage 3: Representation and Public Support

Current data and remaining requirements:

- Bounded Cumulative CES district public-opinion aggregates are available for representative approval, presidential-party preference, House-party preference, turnout, and uninsured-share proxy signals.
- Bill-topic or roll-call mapping.
- Constituency exposure or affected-group support/harm mapping.

Tasks:

- Separate national support, district support, affected-group support, and intensity.
- Do not map party unity directly to public support.

## Stage 4: Lobbying and Capture

Required data:

- Lobbying disclosure linked to issues, sponsors, committees, or bill topics.
- Campaign finance if available and appropriate.
- Interest-group type or information-quality proxy if feasible.

Tasks:

- Split lobbying into pressure/access, private gain, information, and public persuasion.
- Test whether simulator capture diagnostics track observed concentration proxies.

## Stage 5: Correction and Implementation

Required data:

- Court review or challenge data.
- Law revision and sunset-review data, beyond the current Congress.gov title/summary text proxy where lineage claims are made.
- Implementation feedback or administrative burden proxies.

Tasks:

- Define active-law quality and correction over time.
- Add held-out comparison targets.

## Proposed Make Targets

```make
empirical-data-inventory
empirical-flow-heldout
empirical-public-support
empirical-lobbying-linkage
empirical-correction-data
```

## Acceptance Gates

Do not draft a full empirical-validation/data paper until:

1. The source registry exists and covers every source family in `data-source-map.md`.
2. Current ready source families have row counts, date ranges, units of observation, and license/access notes.
3. At least public support, campaign-finance linkage beyond FEC recipient metadata, broad issue-sector context, matched member context, bounded House-candidate district context, and bounded candidate-to-sponsored-bill context to reviewed targets/outcomes, and one correction/implementation source are no longer missing, or a defensible narrowed data-paper scope is chosen.
4. Held-out and independent cross-checks expand beyond the current 13 / 13 linked, metadata-linked, or partially linked source-family coverage by satisfying the linkage-roadmap gates for bill-topic, complete sponsor-history, finance, implementation, direct court, statutory-lineage, and observed comparative-output evidence and reporting errors or tolerance misses, not only broad pass/fail screens.
5. Every table explicitly labels each signal as validated, sanity-checkable, proxy-only, synthetic-only, or not modeled.
6. `make validation-readiness`, `make empirical-bridge`, `make empirical-linkage-report`, `make empirical-linkage-roadmap`, `make sponsor-bill-linkage`, `make court-law-linkage`, `make rulemaking-authority-linkage`, `make rulemaking-history-linkage`, `make bill-law-evidence-spine`, `make campaign-finance-district-context`, `make campaign-finance-issue-context`, `make campaign-finance-sponsor-bill-context`, `make validation-gap-report`, and `make calibration-check` pass.
