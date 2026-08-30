# Paper Plan

## Final Decision

BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

The current pipeline now has a registry-backed benchmark v1 and nine narrow held-out source-family checks: bill progression, Voteview roll-call coalition behavior, sponsor proposal-access concentration, OpenFEC campaign-finance concentration and outside-spending observability, bounded Cumulative CES district public-will proxies, SCDB merits-case invalidation, Federal Register final-to-effective delay, Congress.gov public-law revision text flags, and comparative bicameral context. The linkage audit currently reports 13 / 13 source families as linked, metadata-linked, or partially linked, including a bounded govinfo BILLSTATUS cross-check over the cached bill sample, bounded sponsor-bill metadata matches for 22 / 22 sponsor rows across 56 unique bill IDs and 1 public-law overlap, bounded comparative country-profile to simulator scenario-family metadata anchors for 130 / 130 country-year rows, bounded OpenFEC transaction-label issue-topic context for 46 / 194 campaign-finance rows across 8 broad policy topics, bounded OpenFEC candidate-to-sponsored-bill context for 3 matched transaction rows across 9 cached bill IDs, a bounded district public-opinion policy-context report with 66 sponsor-district public-law rows across 22 bills and 11 local policy areas, exact current CES proxy-variable review for 22 queued packet rows, a bounded SCDB/Federal Register U.S.C.-section authority-overlap inventory for 26 / 9341 SCDB court rows across 9 cached public-law rows, a bounded Federal Register authority-search bridge for 15 / 40 cached public-law rows, bounded proposed-history matches plus proposed-rule Regulations.gov docket/comment-portal and timing metadata for authority-matched final-rule rows, and bounded Regulations.gov comment-record metadata for 48 public-law/docket rows with 19 complete bounded or zero-comment rows and 1 fully represented public-law row; the roadmap records upgrade gates for 10 non-fully-linked families. A full paper should still wait until the data pipeline has stronger linkages, especially roll-call-to-bill/action linkage beyond Voteview member metadata and the current bounded bill-number crosswalk, complete sponsor histories or CEL-style effectiveness data beyond sponsor-bill metadata, observed comparative law-output and bicameral-disagreement data beyond simulator scenario-family anchors, bill-topic public opinion beyond sponsor-district public-law bill metadata, bounded bill policy-area context, and exact current CES proxy-variable review, campaign-finance linkage beyond FEC recipient metadata, bounded issue-sector context, current member/district context, and bounded candidate-to-sponsored-bill context to reviewed outside-spending targets, committee-action influence, legislative outcomes, and causal boundaries, direct case-to-statute/public-law court-review linkage beyond U.S.C.-section overlaps, full statutory lineage beyond Congress.gov bill/action metadata, authority text, proposed-rule/comment-portal/comment-record metadata, timing metadata, and court-overlap metadata, and implementation feedback beyond Federal Register document/docket metadata, authority citations, proposed-rule/comment-portal metadata, bounded complete, zero-comment, and partial comment-record metadata, and timing metadata.

The district public-opinion path now extends that candidate-item scaffolding through official bill-text review and a bounded historical pilot. All 22 packets have a source-reviewed disposition: one retains a directionally related historical issue item and 21 reject forced policy-area matches. The retained item produces two privacy-thresholded annual NY-10 direct-weighted aggregates for 2012 and 2016, representing 372 published aggregate responses. Exact bill-wording and contemporaneous support, design-based uncertainty, MRP/small-area estimation, affected-group evidence, causal representation, and model validation remain absent. Treat the pilot as historical related-issue context, not public-support validation.

## Working Title

Empirical Boundary Conditions for Legislative Mechanism Simulation

## Target Venue Category

Future data/resource paper, computational social science methods note, political methodology data paper, or social simulation validation paper.

## One-Sentence Contribution

The future paper would define and implement a benchmark-data pipeline that maps empirical legislative signals to simulation calibration, sanity-check, proxy, synthetic-only, and missing-model categories.

## Why This Is Not Redundant With The ACM CI Framework Paper

The ACM CI paper contributes the simulator architecture and a synthetic framework demonstration. This breakout would contribute empirical boundary infrastructure: a source registry, validation-readiness scorecard, metric-to-signal mapping, held-out-check design, and missing-data roadmap that other simulation papers can reuse. It should not repeat the ACM mechanism comparison or claim that the framework is validated.

## What This Paper Is Not

- Not proof that the simulator is valid.
- Not a mechanism-ranking paper.
- Not a political-science results paper.
- Not a substitute for bill-topic district opinion, MRP/small-area representation estimates, bill-linked campaign finance beyond the current issue-sector/member/district/sponsored-bill context, full implementation/enforcement feedback, high-volume comment records or comment-text review, direct case-to-statute/public-law court review, emergency-order court review, or full statutory-lineage data.

## Existing Artifacts

- `reports/empirical-validation-readiness.md`: raw-input readiness.
- `data/validation/source-registry.csv`: source-family registry with offline status and claim boundaries.
- `reports/empirical-data-inventory.md`: source-family inventory.
- `reports/validation-boundary-matrix.md`: held-out benchmark / flow sanity check / calibration proxy / not validated matrix.
- `reports/empirical-flow-heldout.md`: nine source-family held-out benchmarks with explicit claim boundaries.
- `reports/empirical-linkage-report.md`: explicit raw-data join coverage by source family.
- `reports/empirical-linkage-roadmap.md`: source-family linkage upgrade gates.
- `reports/govinfo-billstatus-linkage.md`: bounded govinfo BILLSTATUS cross-check for the cached Congress.gov bill-progression rows.
- `reports/sponsor-bill-linkage.md`: bounded sponsor aggregate to public bill-metadata linkage by Bioguide sponsor ID.
- `reports/rulemaking-authority-linkage.md`: bounded Federal Register public-law authority-search inventory for cached public-law rows.
- `reports/rulemaking-history-linkage.md`: bounded Federal Register proposed-history inventory for authority-matched final-rule rows.
- `reports/rulemaking-comment-records.md`: bounded Regulations.gov comment-record metadata inventory for complete bounded, zero-comment, partial, skipped, and unknown-count docket rows, with incomplete rows left explicit.
- `reports/court-law-linkage.md`: bounded SCDB/Federal Register U.S.C.-section authority-overlap inventory for cached public-law rows.
- `reports/bill-law-evidence-spine.md`: bounded bill/public-law join inventory for current bill-action metadata, revision-text proxy fields, sponsor-district public-opinion context, same-policy campaign-finance sponsor context, same-policy LDA issue/bill context, authority-search matches, proposed-history matches, proposed-rule Regulations.gov docket/comment-portal metadata, bounded complete, zero-comment, and partial comment-record metadata, timing metadata, and court U.S.C.-section overlaps.
- `reports/district-public-opinion-policy-context.md`: bounded sponsor-district public-law bill policy-area context inventory for CES district proxy rows.
- `reports/district-public-opinion-ces-policy-item-candidate-review.md`: official Cumulative CES Policy Preferences candidate-item inventory for queued district public-opinion source packets.
- `reports/district-public-opinion-ces-policy-item-response-distribution-review.md`: unweighted raw Cumulative CES Policy Preferences response-code distribution review for queued district public-opinion source packets.
- `reports/district-public-opinion-ces-policy-item-codebook-direction-review.md`: official guide codebook item-direction review for queued district public-opinion source packets.
- `reports/district-public-opinion-bill-item-alignment-review.md`: official bill-text disposition review retaining one historical related-issue alignment and 21 negative dispositions.
- `reports/district-public-opinion-bill-topic-support.md`: two privacy-thresholded annual district aggregates for the retained historical related-issue item.
- `reports/campaign-finance-district-context.md`: bounded OpenFEC candidate-recipient district-context inventory for the House candidate rows that can be joined to CES district public-opinion context.
- `reports/campaign-finance-member-context.md`: bounded OpenFEC candidate-recipient member-context inventory for matched candidates that can be joined to Voteview/Bioguide member metadata.
- `reports/campaign-finance-issue-context.md`: bounded OpenFEC transaction-label issue-context inventory for public labels that can be mapped to broad local policy-area topics.
- `reports/campaign-finance-sponsor-bill-context.md`: bounded OpenFEC candidate/member to sponsored-bill context inventory for matched candidates that can be joined by Bioguide ID to cached govinfo bill metadata.
- `reports/empirical-validation-summary.md`: computed empirical summaries.
- `reports/empirical-bridge.md`: flow sanity-check mapping.
- `reports/empirical-validation-gap-report.md`: claim boundaries and missing areas.
- `reports/core-raw-validation-build.md`: current source-backed sample counts.
- `reports/calibration-baseline.md`: 15 / 15 broad conventional-baseline and proxy screens.
- `data/validation/raw/`: current raw empirical summaries and auxiliary linkage caches, including the govinfo BILLSTATUS cross-check, sponsor-bill metadata linkage, OpenFEC campaign-finance extract, FEC recipient-metadata linkage, Cumulative CES district-opinion aggregate, district public-opinion policy-context cache, CES policy-preference candidate, response-distribution, and codebook-direction caches, official bill-text context, the curated bill-item disposition ledger, privacy-thresholded annual historical district aggregates, SCDB court-review and court-law overlap extracts, Federal Register implementation and authority/history caches, Regulations.gov comment metadata, and Congress.gov law-revision and bill/action linkage.
- `data/validation/fixtures/`: adapter fixtures, intentionally ignored by readiness scoring.
- `scripts/validation/`: validation and empirical-bridge scripts.

## Deliverables for Future Paper

1. Empirical signal taxonomy.
2. Mapping from empirical signal to simulator metric.
3. Claim boundary table:
   - validated;
   - sanity-checkable;
   - proxy only;
   - synthetic only;
   - not currently modeled.
4. Data pipeline plan.
5. Reproducibility plan.
6. Validation-readiness scorecard.
7. Missing-data roadmap.

## Current Go/No-Go

No-go for full paper draft.

Go for:

- expanded data inventory beyond the current v1 registry;
- missing-source acquisition plan;
- offline summary cache;
- broader metric-boundary reports;
- remaining held-out benchmark expansion for source families that are still flow sanity checks or calibration proxies.

## Required New Code Or Data Work

Before a full paper draft:

1. Upgrade the bounded public-opinion path beyond the one historical related-issue pilot with exact or closer contemporaneous bill-topic questions, validated geography crosswalks, design-based uncertainty or MRP where appropriate, and bill-text-specific affected-population evidence; add full statutory lineage beyond the current bounded review layers; add direct and emergency-order court review; add implementation-feedback sources beyond current rule/comment metadata; and link campaign finance to reviewed targets, committee action, roll calls, and outcomes, or explicitly justify replacements.
2. Expand bill-flow data so held-out checks and govinfo cross-checks are not limited to the bounded Congress.gov sample.
3. Broaden held-out roll-call and sponsor-access targets across more Congresses and chambers, replace bounded sponsor-bill metadata with complete sponsor histories or CEL-style effectiveness data, and add held-out or independent cross-check targets for topic throughput, lobbying, and committee activity.
4. Keep adapter fixtures separate from raw empirical summaries and preserve the no-network review path.

## Next Concrete Commands

Current refresh:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make validation-readiness
make empirical-validation
make empirical-bridge
make empirical-flow-heldout
make empirical-data-inventory
make empirical-linkage-report
make empirical-linkage-roadmap
make govinfo-billstatus-linkage
make rulemaking-authority-linkage
make rulemaking-history-linkage
make rulemaking-comment-records
make bill-law-evidence-spine
make campaign-finance-district-context
make campaign-finance-sponsor-bill-context
make district-public-opinion-policy-context
make validation-gap-report
make calibration-check
```

Current and future target surface:

```make
empirical-data-inventory
empirical-flow-heldout
empirical-linkage-report
empirical-linkage-roadmap
rulemaking-authority-linkage
rulemaking-history-linkage
rulemaking-comment-records
bill-law-evidence-spine
campaign-finance-district-context
campaign-finance-sponsor-bill-context
district-public-opinion-policy-context
empirical-public-support-map
empirical-lobbying-linkage
empirical-correction-map
```

## Full Draft Gate

Draft only after:

- data pipeline includes substantially more than the current ready inputs;
- bill-topic public support and bill-linked campaign finance beyond the current issue-sector/member/district/sponsored-bill context are integrated or explicitly replaced by defensible alternatives;
- full statutory-lineage data and fuller implementation-feedback data beyond bounded complete, zero-comment, and partial comment-record metadata are integrated;
- source registry and reproducibility manifests are complete;
- held-out design moves beyond the current source-family proxy checks into linked bill-topic, sponsor, finance, implementation, court, and statutory-lineage evidence;
- claims remain boundary-focused rather than validation-overclaiming.
