# Validation Plan

Final decision: NEEDS DATA/VALIDATION FIRST.

The current empirical layer supports flow sanity checks and one narrow no-refit temporal transport test for aggregate legislative flow. A political-science paper still needs broader mechanism-specific validation and calibration before it can make claims about institutional behavior.

## Current Empirical Status

Existing checks:

- `reports/calibration-baseline.md`: 15/15 flow and proxy sanity checks passed.
- `reports/govinfo-bill-census.md` and `reports/govinfo-bill-census-118.md`: complete, source-pinned H.R./S. lifecycle censuses for the 117th and 118th Congresses.
- `reports/legislative-lifecycle-temporal-replication.md`: frozen 117th-to-118th no-refit transport; committee advancement and floor consideration pass, while enactment misses its 0.010 tolerance by 0.000825.
- `reports/empirical-bridge.csv`: empirical comparison signals.
- `reports/empirical-linkage-report.md`: source-family linkage audit; currently 13 / 13 families are linked, metadata-linked, or partially linked.
- `reports/empirical-linkage-roadmap.md`: required join keys and acceptance gates for non-fully-linked families.
- `reports/empirical-validation-gap-report.md`: proxy-data and synthetic-construct boundaries.
- `reports/core-raw-validation-build.md`: current raw sample counts.

Current checks cover:

- bill progression;
- floor load;
- roll-call coalition size / party-unity proxy;
- veto frequency;
- sponsor access concentration;
- lobbying spend observability;
- merits-case court invalidation and signed-opinion rates;
- final-rule effective-date delay;
- campaign-finance concentration and outside-spending share;
- topic throughput.

Current checks do not validate:

- public support;
- generated public benefit;
- revision moderation;
- minority or concentrated harm;
- lobbying capture;
- administrative cost;
- correction over time;
- implementation feedback beyond final-rule effective-date delay.

## Missing Data Inventory

| Data need | Why it matters | Candidate source family | Current status |
|---|---|---|---|
| District-level public opinion | Needed for representation and public-support claims. | CCES/CES, MRP estimates, ACS demographics. | Partial: one historical related-issue alignment has two privacy-thresholded annual district aggregates; exact/contemporaneous bill support, uncertainty/MRP, validated geography, and affected-group support remain missing. |
| Campaign finance / OpenFEC | Needed to separate campaign-finance influence from lobbying proxies. | FEC/OpenFEC receipts, independent expenditures, industry classifications. | Partial: bounded OpenFEC concentration and outside-spending extract ready; recipient metadata, issue-topic, member, district, sponsored-bill, and same-policy public-law spine context present; bill-specific finance, committee-action, reviewed outside-spending target, and outcome linkage missing. |
| Sponsor histories / effectiveness | Needed for proposer-access and legislative-effectiveness claims. | Congress.gov sponsor metadata, CEL-style effectiveness scores. | Partial: bounded sponsor aggregate and sponsor-bill metadata cache ready; complete sponsor histories, CEL-style effectiveness measures, and outcome-linked member histories missing. |
| Lobbying-to-bill linkage | Needed to connect lobbying pressure to proposal access, committee routing, and outcomes. | LDA filings, bill subjects, client/issue matching, committee referrals. | Partial issue-taxonomy bridge plus shared-policy-area bill/action context; client-specific bill, sponsor, committee-action, roll-call, and outcome linkage missing. |
| Committee hearings / markups / referrals | Needed to validate committee gatekeeping and information-gain claims. | Congress.gov, committee calendars, hearing records, markup/amendment records. | Partial/referral-ready, hearings/markups incomplete. |
| Court review / invalidation | Needed for review/veto/correction modules. | Supreme Court Database, shadow-docket/emergency-order datasets, invalidation coding. | Partial: SCDB merits-case extract and bounded U.S.C.-section authority-overlap metadata ready; direct case-to-statute/public-law identifiers, emergency-order data, and simulator calibration proxy missing. |
| Implementation and agency enforcement | Needed for administrative burden and implementation feedback. | Federal Register, Regulations.gov, Unified Agenda, agency enforcement rows. | Partial: Federal Register final-rule effective-date extract, document metadata, bounded authority-search matches, bounded proposed-history matches, proposed-rule comment-portal metadata, bounded small/zero-comment Regulations.gov comment-record metadata, and timing metadata ready; high-volume comments, comment text, Unified Agenda stages, enforcement, nonenforcement, underfunding, and appropriations capacity missing. |
| Law revision / repeal / sunset / reauthorization | Needed for law-registry, rollback, sunset, and correction claims. | Congress.gov, GovInfo, OLRC/statutory lineage, reauthorization histories. | Partial: Congress.gov public-law title and CRS-summary text flags, bill/action metadata, authority-search matches, proposed-history/comment-portal/comment-record metadata, timing metadata, and bounded court U.S.C.-section overlaps ready; OLRC/govinfo lineage, codified diffs, observed expiration outcomes, high-volume comments, comment text, and direct court invalidation remain missing. |
| Cross-national parliamentary or bicameral comparisons | Needed for party-system and chamber claims beyond U.S.-like flows. | QoG DES/POLCON, OWID/V-Dem, ParlGov, IPU/chamber data, electoral systems, productivity proxies. | Partial: bounded QoG/OWID/V-Dem profile and simulator scenario-family metadata anchors ready; IPU/ParlGov chamber details, bicameral disagreement, and observed productivity remain missing. |

## Validation Sequence

### Phase 1: Flow Sanity Expansion

- Preserve the complete paired 117th/118th GovInfo censuses and add a third completed Congress without refitting.
- Add committee referral/reporting/markup coverage.
- Add veto-frequency and sponsor-concentration checks across multiple Congresses.
- Keep pass/fail bands broad and explicit.

### Phase 2: Proxy Risk Audit

- Mark every proxy as direct, indirect, weak, or missing.
- Do not use coalition size or party unity as public opinion.
- Do not use lobbying spend observability as capture validation.
- Do not use bill throughput as public benefit.

### Phase 3: Public Representation Data

- Extend the bounded district-level CES proxy into modeled public preference where appropriate.
- Map bills or issue domains to opinion topics.
- Split national support, district support, affected-group support, and intensity.

### Phase 4: Influence Linkage

- Link LDA client/issue data beyond the current issue-taxonomy bridge, shared-policy-area bill context, and exact filing-text bill identifiers for a bounded public-law subset to sponsor/member targets, committee referrals, roll calls, influence, and outcomes.
- Extend OpenFEC/FEC data beyond the current bounded proxy and link campaign-finance rows to candidates, sponsors, committees, issues, and bills where possible.
- Split lobbying into information, access, private-gain pressure, and public persuasion where possible.

### Phase 5: Review and Correction Data

- Add direct case-to-statute/public-law identifiers, emergency-order/shadow-docket court-review data, and a simulator court-review proxy target.
- Add Regulations.gov comments, Unified Agenda stages, and agency enforcement/nonenforcement data.
- Add full law revision, reauthorization, repeal, and sunset histories beyond the bounded Congress.gov text proxy.

### Phase 6: Held-Out Validation

- Extend the implemented 117th-selection/118th-test design to additional temporal cohorts and mechanism-specific observables.
- Continue reporting error metrics, fixed tolerance rules, and failures without retuning on test cohorts.
- Only after this phase should the paper use the word validation for central model outputs.

## Required Repo Tasks

- Maintain `reports/empirical-data-inventory.csv` and the 14 configured dataset files across 13 source families.
- Add `reports/political-validation-targets.csv`.
- Add cached no-network summaries for every empirical input used.
- Keep validation scripts separated into calibration, flow sanity, proxy checks, within-Congress held-out checks, and no-refit temporal transport.
- Reuse the empirical-validation source registry once it exists; do not create a competing source inventory for this paper.

## Proposed Make Targets

```make
empirical-data-inventory
political-validation-targets
legislative-lifecycle-temporal-replication
political-public-opinion-map
political-lobbying-linkage
political-correction-data
```

## Dependency On Empirical-Validation Breakout

This paper should still wait. The empirical-validation breakout now has a source registry, expanded raw/cached data, narrow source-family held-out checks, and one complete-Congress temporal transport test, but it does not validate the simulator's political mechanisms or central welfare, representation, influence, implementation, or correction constructs. Political-science claims should use "held-out benchmark," "temporal transport," "flow smoke test," "proxy," or "synthetic" language rather than unqualified "validation."
