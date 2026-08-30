# Empirical Validation Readiness

This directory is a scaffold for raw-data validation. It is not used to fit the
current paper results, but the repository now includes documented raw samples
for bill progression, Voteview roll calls, lobbying disclosures, topic
throughput, sponsor proposal concentration, committee-report signals, SCDB
court-review summaries, Federal Register final-rule effective-date rows,
authority-search matches, and proposed-history matches, a bounded OpenFEC
campaign-finance sample, an official LDA filing-text bill-mention cache, and a
QoG/OWID/V-Dem comparative
institutions profile so the empirical bridge can exercise several real
agenda-access, representation, influence, review, implementation-delay, and
comparative-institution signals rather than only missing-data placeholders.
It also includes a bounded Congress.gov public-law revision-text sample for
amendment, reauthorization/extension, repeal, and sunset/expiration language.
The govinfo family is represented by a bounded BILLSTATUS XML cross-check for
the cached Congress.gov bill-progression sample.
The public-opinion family is represented by a bounded Cumulative CES Common
Content district aggregate for 2024 representative approval, presidential-party
preference, House-party preference, turnout, and uninsured-share proxy signals,
plus an official Census TIGERweb population/housing denominator cache for the
queued sponsor districts and an official ACS 2017-2021 broad district-context
cache for those same queued districts.
The comparative-institution family is represented by a bounded QoG Data
Finder plus OWID/V-Dem extract for chamber count, district magnitude,
party-system fragmentation, judicial constraints, and legislative-constraints
proxies.

Expected optional raw validation inputs under `data/validation/raw/`:

- `voteview_rollcalls.csv`: roll-call or member-level vote summaries with
  `congress`, `party`, `vote_id`, `vote`, and `ideology` columns.
- `bill_progression.csv`: bill-stage histories from Congress.gov or govinfo
  with `bill_id`, `introduced`, `committee_reported`, `floor_considered`, and
  `enacted` columns.
- `govinfo_billstatus_linkage.csv`: govinfo BILLSTATUS bill/action metadata
  joined to the cached bill-progression sample by congress, bill type, and bill
  number. It is an independent bounded cross-check, not a full bill census.
- `lobbying_disclosure.csv`: lobbying spending or client reports with
  `client`, `issue`, `amount`, and `period` columns.
- `lobbying_bill_mentions.csv`: official LDA filing activity-text rows with
  exact current-bill identifier mentions for a bounded public-law candidate set.
  This is bill-identifier source-review context, not lobbying influence,
  sponsor-target, committee-action, roll-call, outcome, welfare, or
  model-validation evidence.
- `bill_finance_lobbying_local_context_review.csv`: curated local-context
  review for the 10 public-law rows whose remaining action gate is
  bill-specific campaign-finance or lobbying evidence. It records that current
  cached same-policy campaign-finance sponsor context and LDA issue/bill
  context do not contain the reviewed current bill ID; it is not external
  target/source, influence, outcome, welfare, capture, or model-validation
  evidence.
- `bill_finance_lobbying_external_lda_searches.csv` and
  `bill_finance_lobbying_external_lda_mentions.csv`: targeted official LDA
  current-bill search cache for those 10 rows. The derived report finds exact
  LDA activity-text current-bill mentions for 2 queued bills, but these are
  bill-reference rows only, not lobbying-contact, target, support/opposition,
  committee-action, roll-call, outcome, welfare, capture, or model-validation
  evidence.
  The derived external LDA mention-review report groups those exact mentions
  into 19 filing packets, classifies 16 current-bill issue-reference packets and
  3 current-bill issue-advocacy packets without explicit support/opposition
  text, and records no named sponsor/member/committee target, committee-action
  influence, roll-call influence, or legislative-outcome causality evidence.
  The derived committee/action context report joins the 10 queued rows to cached
  public bill-action metadata, recording committee-reported and floor-considered
  flags only; it does not provide committee-of-jurisdiction names,
  committee-action influence, roll-call influence, legislative-outcome
  causality, public benefit, capture, or model-validation evidence.
- `topic_throughput.csv`: topic-level bill throughput with `topic`,
  `introduced`, `floor_considered`, and `enacted` columns.
- `sponsor_success.csv`: sponsor-level effectiveness or success measures with
  `sponsor_id`, `party`, `introduced`, and `enacted` columns.
- `sponsor_bill_linkage.csv`: bounded sponsor aggregate to public bill-metadata
  rows by Bioguide sponsor ID; it is not full Center for Effective Lawmaking or
  legislative-quality evidence.
- `district_public_opinion.csv`: district-level opinion and intensity rows with
  `district_id`, `issue`, `support`, `intensity`, `turnout`, and
  `affected_group_share` columns.
- `district_public_opinion_policy_context.csv`: bounded sponsor-district
  public-law bill policy-area context rows keyed to district-opinion linkage
  rows, with local topic-throughput counts and explicit missing-link flags.
- `district_public_opinion_census_denominators.csv`: official Census TIGERweb
  116th congressional-district 2020 population, housing-unit, land/water area,
  and centroid attributes for queued sponsor districts. This is district-frame
  denominator context, not ACS policy-specific affected-population detail.
- `district_public_opinion_acs_context.csv`: official ACS 2017-2021 5-year
  broad 116th congressional-district demographic, economic, citizenship,
  language, disability, internet, poverty, and veteran context for queued
  sponsor districts. This is broad district context, not bill-topic support,
  MRP/small-area estimation, bill-text-specific affected-population definitions,
  affected-group support/harm, public-benefit, or model-validation evidence.
- `committee_activity.csv`: committee referral and work-product rows with
  `committee`, `issue`, `referred`, `hearings`, `reported`, `amendments`, and
  `discharged` columns.
- `campaign_finance.csv`: campaign-finance and outside-spending rows with
  `cycle`, `recipient`, `industry`, `amount`, and `independent_expenditure`
  columns.
- `court_review.csv`: constitutional-review rows with `case_id`, `issue`,
  `emergency_order`, `invalidated`, `vote_margin`, `signed_opinion`, and
  optional SCDB legal-authority metadata columns such as `law_minor` and
  `usc_sections`.
- `court_law_linkage.csv`: bounded SCDB U.S.C.-section to Federal Register
  authority-citation overlap rows keyed by `case_id`, with matched public-law
  and bill IDs when exact normalized U.S.C. sections overlap. This is not
  direct case-to-public-law review or invalidation evidence.
- `rulemaking_implementation.csv`: post-enactment implementation rows from
  Federal Register, Unified Agenda, Regulations.gov, or comparable sources with
  `law_id`, `proposed_rule_date`, `final_rule_date`, `effective_date`,
  `comment_count`, `enforcement_capacity`, `nonenforced`, and `underfunded`
  columns.
- `rulemaking_authority_linkage.csv`: Federal Register public-law
  authority-search rows keyed by `public_law_number`, with candidate and
  text-verified rule counts, verified document numbers, U.S. Code citations,
  evidence layers, missing links, and claim boundaries.
- `rulemaking_history_linkage.csv`: Federal Register proposed-to-final history
  rows keyed by `public_law_number` and final-rule document number, with
  proposed-rule candidate counts, shared RIN/docket evidence, proposed document
  numbers, evidence layers, missing links, and claim boundaries.
- `law_revision_history.csv`: law-lineage rows from Congress.gov, govinfo,
  statutory-history datasets, or comparable sources with `law_id`,
  `enacted_date`, `amended`, `reauthorized`, `repealed`, `expired`, and
  `invalidated` columns.
- `comparative_institutions.csv`: comparative institutional rows with
  `country`, `year`, `chambers`, `district_magnitude`, `judicial_review`,
  `party_fragmentation`, and `legislative_productivity` columns.
- `comparative_institution_linkage.csv`: bounded comparative-institution rows
  mapped to simulator scenario-family metadata anchors, with evidence layers,
  missing links, and claim boundaries.
- `campaign_finance_issue_context.csv`: bounded campaign-finance transaction
  rows mapped from high-confidence public OpenFEC labels to broad local
  policy-area topics, with unmapped rows retained and claim boundaries.

Run `make validation-readiness` to generate a report showing which inputs are
present and whether the required columns are available. A passing readiness
report would only mean the raw files are shaped correctly; it would not by
itself validate the simulator.

Run `make empirical-data-inventory` to build the registry-backed source-family
inventory and validation-boundary matrix from
`data/validation/source-registry.csv`. This writes:

- `reports/empirical-data-inventory.csv`
- `reports/empirical-data-inventory.md`
- `reports/validation-boundary-matrix.csv`
- `reports/validation-boundary-matrix.md`

The boundary matrix uses four conservative labels: `held-out benchmark`, `flow
sanity check`, `calibration proxy`, and `not validated`.

Run `make empirical-validation` after adding one or more raw files to compute
dataset-specific summary metrics such as party unity, bill attrition, lobbying
spending concentration, topic throughput, sponsor success concentration,
committee activity, public-opinion intensity, court-review invalidation and
vote-margin rates, implementation delay, enforcement capacity, and
post-enactment correction rates, and comparative chamber or party-system
profiles.
The command writes `reports/empirical-validation-summary.csv` and `.md`; missing
datasets are reported as missing rather than treated as build failures. These
adapters are deliberately source-shaped: adding real data still requires a
documented extraction and cleaning note for each source before the paper should
claim empirical validation rather than validation readiness.

Run `make empirical-flow-heldout` to perform the current concrete held-out
benchmark paths. The implementation splits the committed Congress.gov
bill-progression sample deterministically by `bill_id` hash, the committed
Voteview roll-call sample by `vote_id` hash, and the committed sponsor sample
by `sponsor_id` hash. It reports calibration-slice, held-out-slice, and all-row
bill-flow, roll-call, and sponsor-access metrics in:

- `reports/empirical-flow-heldout.csv`
- `reports/empirical-flow-heldout.md`

These are narrow held-out benchmarks for legislative flow, roll-call coalition
behavior, and sponsor proposal-access concentration only. They are not
validation of public benefit, public support, welfare, harm, capture,
correction, representation, full member effectiveness, or mechanism rankings.

Run `make validation-gap-report` to regenerate the paper-facing boundary report
and appendix table. That workflow joins the source registry, readiness, raw
summary metrics, empirical bridge, data inventory, held-out benchmark report,
linkage audit, linkage roadmap, and bill-law evidence spine into
`reports/empirical-validation-gap-report.*`,
`reports/govinfo-billstatus-linkage.*`,
`reports/sponsor-bill-linkage.*`,
`reports/court-law-linkage.*`,
`reports/rulemaking-authority-linkage.*`,
`reports/rulemaking-history-linkage.*`,
`reports/rulemaking-comment-metadata.*`,
`reports/rulemaking-comment-records.*`,
`reports/rulemaking-comment-text-review.*`,
`reports/bill-law-evidence-spine.*`,
`reports/bill-law-lifecycle-readiness.*`,
`reports/bill-law-lifecycle-next-actions.*`,
`reports/lobbying-bill-mention-review.*`,
`reports/lobbying-bill-action-context.*`,
`reports/lobbying-bill-text-review.*`,
`reports/lobbying-bill-disposition-review.*`,
`reports/statutory-lineage-review-queue.*`,
`reports/statutory-lineage-source-scan.*`,
`reports/statutory-lineage-no-target-review.*`,
`reports/statutory-lineage-target-section-triage.*`,
`reports/statutory-lineage-olrc-current-scan.*`,
`reports/statutory-lineage-olrc-historical-scan.*`,
`reports/statutory-lineage-olrc-annual-text-diff.*`,
`reports/statutory-lineage-adjudication.*`,
`reports/statutory-lineage-target-review-packets.*`,
`reports/statutory-lineage-target-section-diff-review.*`,
`reports/statutory-lineage-target-lifecycle-bridge.*`,
`reports/statutory-lineage-codified-progress.*`,
`reports/statutory-lineage-effective-text-review.*`,
`reports/statutory-lineage-public-law-attribution-review.*`,
`reports/statutory-lineage-completion-queue.*`,
`reports/statutory-lineage-complete-lineage-expansion-queue.*`,
`reports/statutory-lineage-target-packet-expansion-queue.*`,
`reports/statutory-lineage-target-packet-source-gap-queue.*`,
`reports/court-public-law-review-queue.*`,
`reports/court-public-law-temporal-triage.*`,
`reports/court-public-law-direct-review.*`,
`reports/district-public-opinion-acs-context.*`,
`reports/district-public-opinion-survey-source-crosswalk.*`,
`reports/district-public-opinion-survey-item-proxy-review.*`,
`reports/district-public-opinion-ces-source-freshness.*`,
and `paper/figures/empirical_validation_gap_table.tex`. The point is to keep paper
claims honest: rows with raw inputs can be discussed as empirical bridges,
held-out benchmarks, linkage inventories, or bounded spine rows, while
unsupported constructs remain synthetic or speculative model components.

Optional API adapter fixtures can be fetched with:

```sh
make fetch-validation-samples ARGS="--env-file /path/to/.env"
```

The fetcher currently reads `CONGRESS_API_KEY` and `OPENFEC_API_KEY` when
available. It writes small normalized fixtures under `data/validation/fixtures/`
for bill progression, topic throughput, sponsor success, and campaign finance.
These fixtures are useful for testing adapters against public API shapes, but
they are deliberately too small and too lightly cleaned to count as empirical
validation. Move or copy only curated, documented extracts into
`data/validation/raw/`.

A documented raw bill-progression sample can be generated from Congress.gov
with:

```sh
make build-bill-progression-raw ARGS="--env-file /path/to/.env --congress 118 --page-limit 60 --offsets 0,500,1500"
```

This writes `data/validation/raw/bill_progression.csv` and
`data/validation/raw/bill_progression.metadata.md`. It is still a sample rather
than a full congressional census, so paper claims should describe it as an
empirical bridge or plausibility check, not final validation.

A documented govinfo BILLSTATUS cross-check for the cached bill sample can be
generated with:

```sh
make build-govinfo-billstatus-linkage-raw
```

This writes `data/validation/raw/govinfo_billstatus_linkage.csv` and
`data/validation/raw/govinfo_billstatus_linkage.metadata.md`. The builder uses
public govinfo bulk XML records, requires no API key, and joins only by
congress, bill type, and bill number. It cross-checks bill/action metadata
against the bounded Congress.gov bill-progression sample but does not create a
full bill census, public-opinion evidence, campaign-finance or lobbying
influence evidence, implementation or court-outcome linkage, public benefit,
welfare, or model validation.

The broader raw-validation sample can be generated with:

```sh
make build-core-raw-validation ARGS="--env-file /path/to/.env --derive-congress-from-bill-progression --preserve-sponsor-success"
```

A documented Voteview member-metadata context can be generated from the cached
Voteview roll-call rows with:

```sh
make build-voteview-member-context-raw
```

This writes `data/validation/raw/voteview_member_context.csv` and
`data/validation/raw/voteview_member_context.metadata.md`. It maps cached
roll-call rows to public Voteview member metadata by Congress, chamber, and
ICPSR member ID. It remains member metadata only, not roll-call-to-bill,
public-law, district-opinion, sponsor-effectiveness, public-support, or model
validation evidence.

A documented Voteview roll-call bill-number crosswalk can be generated from the
cached Voteview roll-call rows with:

```sh
make build-voteview-bill-linkage-raw
```

This writes `data/validation/raw/voteview_bill_linkage.csv` and
`data/validation/raw/voteview_bill_linkage.metadata.md`. It maps cached
roll-call IDs to Voteview roll-call metadata by Congress, chamber, and roll
number, normalizes Voteview bill numbers when possible, and flags bounded
overlap with the cached Congress.gov bill-progression sample. It remains a
bounded crosswalk only, not complete roll-call-to-bill, public-law,
district-opinion, sponsor-effectiveness, public-support, outcome, or model
validation evidence.

A bounded official House Clerk roll-call source cache for the finance/lobbying
public-law queue can be generated with:

```sh
make build-bill-finance-lobbying-roll-call-source-raw
```

This writes `data/validation/raw/bill_finance_lobbying_roll_call_source.csv`
and `.metadata.md`, fetching official House Clerk XML rows for numbered roll
calls exposed in govinfo BILLSTATUS action text. The paired
`reports/bill-finance-lobbying-roll-call-source-review.*` report records 8
official House Clerk roll-call rows and 2 floor-action rows without numbered
roll calls. It is floor-vote source coverage only, not evidence of
campaign-finance or lobbying influence, member persuasion, roll-call
influence, outcome causality, welfare, capture, or model validation.

A documented Senate LDA issue-to-policy-area crosswalk can be generated from
the cached lobbying rows with:

```sh
make build-lobbying-issue-linkage-raw
```

This writes `data/validation/raw/lobbying_issue_linkage.csv` and
`data/validation/raw/lobbying_issue_linkage.metadata.md`. It maps cached Senate
LDA issue labels to broad local Congress.gov policy-area topic labels for
144 / 146 LDA activity rows. It remains issue-taxonomy context only, not
client-to-bill, sponsor, committee, causal capture, or model validation
evidence.

A documented official LDA filing-text bill-mention cache can be generated from
the public-law candidate set with:

```sh
make build-lobbying-bill-mentions-raw
```

This writes `data/validation/raw/lobbying_bill_mention_searches.csv`,
`data/validation/raw/lobbying_bill_mentions.csv`, and
`data/validation/raw/lobbying_bill_mentions.metadata.md`. The committed cache
currently records 484 exact activity-text bill mention rows across 26 cached
public-law bill IDs from 40 searched public-law rows. It is bill-identifier
source-review context only, not support/opposition, lobbying influence,
sponsor/member targeting, committee-action influence, roll-call influence,
legislative-outcome causality, welfare, causal capture, or model validation.
The current cache was refreshed with `ARGS="--description-limit 0"` so stored
activity descriptions contain the full public API text returned for each exact
match.

The derived LDA bill-action context report can be regenerated with:

```sh
make lobbying-bill-action-context
```

This writes `reports/lobbying-bill-action-context.csv` and `.md`, joining those
exact LDA bill identifiers to cached Congress.gov public-law bill/action,
sponsor, committee-reported, floor-considered, and enacted-outcome metadata. It
is identifier and legislative metadata context only, not support/opposition,
sponsor/member targeting, committee-action influence, roll-call influence,
legislative-outcome causality, welfare, causal capture, or model validation.

The derived LDA bill text-review report can be regenerated with:

```sh
make lobbying-bill-text-review
```

This writes `reports/lobbying-bill-text-review.csv` and `.md`. The current
cache represents 484 exact-match rows; all 484 rows have the bill reference
visible in stored full activity text. The report classifies 46 support-only
rows, 3 opposition-only rows, 2 mixed support/opposition rows, 104
position/activity rows without direction, and 329 bill-list or title-only rows.
These are deterministic stored-text signals only, not manual disposition,
targeting, committee-action, roll-call, outcome, influence, welfare, or
validation evidence.

The derived LDA disposition/target review report can be regenerated with:

```sh
make lobbying-bill-disposition-review
```

This writes `reports/lobbying-bill-disposition-review.csv` and `.md`. It
prioritizes the same 484 exact-match rows for manual disposition and target
review: 156 rows need manual review, with 4 high-priority rows, 152
medium-priority rows, and 328 low-priority bill-reference-only rows. It remains
a source-review queue only, not manual disposition confirmation, sponsor/member
targeting evidence, committee-action influence, roll-call influence,
legislative-outcome causality, welfare, capture, or validation evidence.

The high-priority LDA manual disposition/target review can be regenerated with:

```sh
make lobbying-bill-manual-disposition-review
```

This writes `reports/lobbying-bill-manual-disposition-review.csv` and `.md`
from `data/validation/raw/lobbying_bill_manual_disposition_review.csv`. It
source-reviews the 4 high-priority queue rows, confirms 3 current-bill support
rows, preserves 1 bill-reference-only row, and records no outcome-influence
evidence. It remains activity-text disposition and target-reference review only,
not lobbying-contact, committee-action, roll-call, outcome-causality, welfare,
capture, or validation evidence.

The medium-priority LDA disposition packet report can be regenerated with:

```sh
make lobbying-bill-medium-disposition-packets
```

This writes `reports/lobbying-bill-medium-disposition-packets.csv` and `.md`.
It groups the 152 medium-priority LDA disposition rows into 102 review packets
and collapses 50 repeated rows. It is review infrastructure only, not manual
disposition confirmation, lobbying-contact, target, committee-action, roll-call,
outcome-causality, welfare, capture, or validation evidence.

The medium-priority LDA directional packet review can be regenerated with:

```sh
make lobbying-bill-medium-directional-packet-review
```

This writes `reports/lobbying-bill-medium-directional-packet-review.csv` and
`.md` from
`data/validation/raw/lobbying_bill_medium_directional_packet_review.csv`. It
source-reviews the 28 support/opposition packets, confirming 20 current-bill
support packets representing 32 rows and 1 current-bill opposition packet, while
downgrading 7 packets representing 15 rows to other-measure direction or
monitoring/reference context. It remains activity-text disposition review only,
not lobbying-contact, target, committee-action, roll-call, outcome-causality,
welfare, capture, or validation evidence.

The medium-priority LDA position/activity packet review can be regenerated with:

```sh
make lobbying-bill-medium-position-activity-packet-review
```

This writes `reports/lobbying-bill-medium-position-activity-packet-review.csv`
and `.md` from
`data/validation/raw/lobbying_bill_medium_position_activity_packet_review.csv`.
It source-reviews the 74 position/activity packets representing 104 rows,
classifying 59 current-bill issue/provision activity packets, 5
monitoring/analysis packets, 7 all-provisions packets, 2 position-represented
packets, and 1 current-bill opposition packet found in the position/activity
queue. It remains activity-text disposition review only, not lobbying-contact,
target, committee-action, roll-call, outcome-causality, welfare, capture, or
validation evidence.

A documented raw OpenFEC campaign-finance sample can be generated with:

```sh
make build-campaign-finance-raw ARGS="--env-file /path/to/.env --cycle 2024 --receipts-limit 100 --independent-limit 100"
```

This writes `data/validation/raw/campaign_finance.csv` and
`data/validation/raw/campaign_finance.metadata.md`. The sample is intentionally
privacy-minimized: it omits contributor names, contributor street addresses,
and payee names. It supports campaign-finance concentration and
outside-spending bridge metrics only, not bill-level influence or capture
validation.

A documented FEC recipient-metadata linkage can be generated with:

```sh
make build-campaign-finance-linkage-raw ARGS="--cycle 2024"
```

This writes `data/validation/raw/campaign_finance_linkage.csv` and
`data/validation/raw/campaign_finance_linkage.metadata.md`. It maps cached
recipient IDs to public FEC committee/candidate metadata and
candidate-committee linkage IDs where available. It remains metadata linkage
only, not bill, sponsor, issue, committee-of-jurisdiction, or influence
validation.

A documented candidate-to-member context cache for the campaign-finance sample
can be generated with:

```sh
make build-campaign-finance-member-context-raw
```

This writes `data/validation/raw/campaign_finance_member_context.csv` and
`data/validation/raw/campaign_finance_member_context.metadata.md`. It reads the
cached FEC recipient metadata and cached Voteview member context, then links
candidate rows to Voteview/Bioguide member metadata only when candidate name,
chamber, state, and district evidence agree. It leaves challengers,
presidential candidates, noncandidate committees, and ambiguous rows unmatched.
It remains member-context metadata only, not bill-level influence, sponsor
effectiveness, committee-of-jurisdiction, issue targeting, or capture
validation.

The broader raw-validation builder uses Voteview static CSVs, the existing
Congress.gov bill-action sample, optional Congress.gov bill-detail sponsor
enrichment, and Senate LDA filings. It is intentionally bounded and documented.
Committee activity is currently an action-derived committee-report signal
rather than a full hearing calendar, and the sponsor sample is a proposal-access
bridge rather than a final Center for Effective Lawmaking replacement.

A bounded sponsor aggregate to public bill-metadata linkage can be generated
with:

```sh
make build-sponsor-bill-linkage-raw
```

This writes `data/validation/raw/sponsor_bill_linkage.csv` and
`data/validation/raw/sponsor_bill_linkage.metadata.md`. It joins sponsor
aggregate rows to bounded govinfo/Congress.gov bill metadata by Bioguide sponsor
ID only. It does not provide full Center for Effective Lawmaking data, complete
sponsor histories, bill quality, causal effects, welfare, or model validation.

A merits-case court-review sample can be generated from the Supreme Court
Database 2025 Release 01 with:

```sh
make build-court-review-raw
```

This writes `data/validation/raw/court_review.csv` and
`data/validation/raw/court_review.metadata.md`. The normalized file maps SCDB
case-centered rows to invalidation, vote-margin, and signed-opinion rates. It
does not cover emergency or shadow-docket orders; the `emergency_order` column
is therefore fixed at `0` and should not be used as evidence about emergency
review behavior.

A final-rule implementation-delay sample can be generated from the Federal
Register API with:

```sh
make build-rulemaking-implementation-raw
```

This writes `data/validation/raw/rulemaking_implementation.csv` and
`data/validation/raw/rulemaking_implementation.metadata.md`. The normalized
file maps Federal Register final rules to final-rule publication date,
effective date, and a coarse implementation-speed proxy. The raw final-rule
sample does not itself link final rules to proposed rules, Regulations.gov
comment totals, enforcement failures, or appropriations capacity; the bounded
history cache below adds proposed-rule metadata for authority-matched final
rules only, and the remaining sources still have to be added before the paper
can make implementation-feedback claims.

A Federal Register document-metadata linkage for those final-rule rows can be
generated with:

```sh
make build-rulemaking-implementation-linkage-raw
```

This writes `data/validation/raw/rulemaking_implementation_linkage.csv` and
`data/validation/raw/rulemaking_implementation_linkage.metadata.md`. It links
cached final-rule rows to Federal Register document metadata and, when exposed
by Federal Register, Regulations.gov docket, document, and comment-count
metadata. It does not provide public-law authority, proposed-to-final histories,
complete comment records, enforcement outcomes, appropriations capacity, or
observed nonenforcement.

A documented Federal Register public-law authority-search cache can be
generated for the cached public-law rows with:

```sh
make build-rulemaking-authority-linkage-raw
```

This writes `data/validation/raw/rulemaking_authority_linkage.csv` and
`data/validation/raw/rulemaking_authority_linkage.metadata.md`. It searches
Federal Register rule text for cached public-law citations and keeps only
text-verified authority matches as linked evidence. It does not provide
exhaustive implementation coverage, proposed-rule histories, complete comment
records, enforcement outcomes, appropriations capacity, court review, public
benefit, welfare, causal effects, or model validation.

A documented Federal Register proposed-to-final history cache can be generated
for the authority-matched final-rule rows with:

```sh
make build-rulemaking-history-linkage-raw
```

This writes `data/validation/raw/rulemaking_history_linkage.csv` and
`data/validation/raw/rulemaking_history_linkage.metadata.md`. It searches
Federal Register proposed-rule records by final-rule RIN and docket identifiers
and keeps only proposed-rule rows sharing those identifiers and not later than
the final rule. It does not provide complete Regulations.gov comment records,
Unified Agenda stages, enforcement outcomes, appropriations capacity,
exhaustive implementation coverage, public benefit, welfare, causal effects,
or model validation.

A bounded authority-chain comment-metadata cache can be generated with:

```sh
make build-rulemaking-comment-metadata-raw
```

This writes `data/validation/raw/rulemaking_comment_metadata.csv` and
`data/validation/raw/rulemaking_comment_metadata.metadata.md`. It refetches
Federal Register detail records for authority-matched final-rule rows and their
matched proposed-rule records, then extracts only Federal Register-exposed
Regulations.gov docket IDs, comment URLs, comment counts, and comment-close
dates. It does not fetch complete comment records, commenter identities,
comment text, Unified Agenda stages, enforcement outcomes, appropriations
capacity, public benefit, welfare, causal effects, or model validation.

A bounded Regulations.gov comment-record cache can be generated with:

```sh
make build-rulemaking-comment-records-raw
```

This writes `data/validation/raw/rulemaking_comment_records.csv` and
`data/validation/raw/rulemaking_comment_records.metadata.md`. It starts from the
Federal Register-exposed docket/comment-count metadata, retrieves only small
Regulations.gov comment-record metadata sets by default, treats zero-comment
dockets as complete no-comment rows, and leaves high-volume or unknown-count
dockets as explicit gaps. It may use `REGULATIONS_GOV_API_KEY` or the public
demo key for bounded retrieval. It does not fetch comment text,
attachments, private submitter details, Unified Agenda stages, enforcement
outcomes, appropriations capacity, public benefit, welfare, causal effects, or
model validation.

A bounded sanitized Regulations.gov comment-detail review can be generated with:

```sh
make build-rulemaking-comment-text-review-raw
```

This writes `data/validation/raw/rulemaking_comment_text_review.csv` and
`data/validation/raw/rulemaking_comment_text_review.metadata.md`. It
prioritizes complete comment-record metadata rows with retrieved comment IDs,
then adds bounded partial-docket sample rows. It fetches bounded public
comment-detail records and stores text availability, normalized text hashes,
lengths, attachment counts, source record status, and coarse implementation cue
flags while omitting the full comment body and submitter/contact fields. Partial
sample rows do not prove complete docket coverage. It is not a full comment-text
corpus, attachment-text review, commenter-identity validation, sentiment or
position coding, implementation outcome, welfare, causal-effect, or
model-validation evidence.

A bounded public-law revision-text sample can be generated from Congress.gov
with:

```sh
make build-law-revision-raw ARGS="--env-file /path/to/.env --congresses 117,118 --laws-per-congress 60"
```

This writes `data/validation/raw/law_revision_history.csv` and
`data/validation/raw/law_revision_history.metadata.md`. The normalized file maps
public-law titles and CRS summaries to amendment, reauthorization/extension,
repeal, and sunset/expiration text flags. It does not provide OLRC/govinfo
statutory lineage, codified-text diffs, observed expiration outcomes, or later
court invalidation; the `invalidated` column is therefore fixed at `0`.

A bounded Congress.gov public-law-to-bill/action metadata linkage can be
generated with:

```sh
make build-law-revision-bill-linkage-raw ARGS="--env-file /path/to/.env --limit 40"
```

This writes `data/validation/raw/law_revision_bill_linkage.csv` and
`data/validation/raw/law_revision_bill_linkage.metadata.md`. It links public-law
rows to Congress.gov bill details and action histories only. It does not provide
codified statutory lineage, implementation-feedback linkage, court-review
linkage, or U.S. Code target-section evidence.

A bounded official public-law text scan for codified-lineage candidates can be
generated from GovInfo with:

```sh
make build-statutory-lineage-source-scan-raw
```

This writes `data/validation/raw/statutory_lineage_source_scan.csv` and
`data/validation/raw/statutory_lineage_source_scan.metadata.md`. It scans
official GovInfo public-law text pages for the current statutory-lineage review
queue and records source hashes, U.S.C.-reference counts, amendment/repeal/
redesignation counts, and compact candidate snippets. It does not provide OLRC
classification, codified U.S.C. lineage, target-section text diffs,
implementation outcomes, court-review proof, welfare, or model validation.
`make statutory-lineage-target-section-triage` derives a no-network normalized
target-reference review queue from that source scan. It ranks candidate U.S.C.
targets for manual OLRC/codified-text review, but remains target-section
triage rather than codified lineage or target-section text-diff evidence.
`make build-statutory-lineage-olrc-current-scan-raw` fetches official OLRC
current U.S. Code pages for structured triage rows and writes
`data/validation/raw/statutory_lineage_olrc_current_scan.csv` plus metadata.
`make statutory-lineage-olrc-current-scan` then writes the offline report. This
scan records current-page availability, source hashes, and current-page
public-law mentions only; it is not historical codified lineage or
before/after target-section text-diff evidence.
`make build-statutory-lineage-olrc-historical-scan-raw` fetches official OLRC
annual U.S. Code pages for the year before enactment and the enactment year for
current-page candidates that mention the queued public law and writes
`data/validation/raw/statutory_lineage_olrc_historical_scan.csv` plus metadata.
`make statutory-lineage-olrc-historical-scan` then writes the offline report.
This scan compares annual source hashes and public-law mentions only; it is not
codified lineage, public-law causation, before/after target-section text-diff,
implementation-outcome, court-review, welfare, or model-validation evidence.
`make build-statutory-lineage-olrc-annual-text-diff-raw` refetches those annual
OLRC pages and writes
`data/validation/raw/statutory_lineage_olrc_annual_text_diff.csv` plus
metadata. `make statutory-lineage-olrc-annual-text-diff` then writes the
offline report. This scan records bounded post-edition public-law context
snippets, raw-hash comparison flags, normalized section-text signatures, and
bounded first-change windows only; it is not source-reviewed codified lineage,
public-law causation, adjudicated target-section text-diff,
implementation-outcome, court-review, welfare, or model-validation evidence.
`make build-statutory-lineage-adjudication-raw` derives
`data/validation/raw/statutory_lineage_adjudication.csv` from the annual OLRC
text-diff cue report. `make statutory-lineage-adjudication` mirrors it to the
report directory and summarizes official OLRC post-only public-law marker
evidence. This is codified-lineage marker evidence only; it is not a
source-reviewed target-section text diff, public-law causal attribution,
effective statutory text, implementation-outcome, court-review, welfare, or
model-validation evidence.
`make build-statutory-lineage-target-review-packets-raw` derives
`data/validation/raw/statutory_lineage_target_review_packets.csv` from the
OLRC adjudication and annual text-diff reports. `make
statutory-lineage-target-review-packets` writes the report directory packet
view and annotates packet rows with downstream target-section diff-review
dispositions where curated review rows exist. These packets are review
infrastructure plus disposition context; they are not public-law causal
attribution, effective statutory text, implementation-outcome, court-review,
welfare, or model-validation evidence.
`make statutory-lineage-target-section-diff-review` writes a bounded
source-reviewed pilot report from curated official-source dispositions in
`data/validation/raw/statutory_lineage_target_section_diff_review.csv`.
The current pilot covers Public Laws 117-146, 117-166, 117-167, 117-168,
117-169, 117-174, 117-180, 117-203, 117-219, 117-223, 117-229, 117-263,
and 117-297 with 75 reviewed dispositions, including 73 source-reviewed
target-section diff rows and 2 reviewed related-section/no-exact-target rows.
It is not
exclusive public-law causal attribution, effective
statutory text, implementation-outcome, direct court-review, welfare,
causal-effect, or model-validation evidence.
`make statutory-lineage-target-lifecycle-bridge` writes a derived report that
bridges those reviewed target-section diff rows to bounded public-law-level
implementation authority, rulemaking history, Federal Register-exposed comment
metadata, SCDB U.S.C.-section overlap, court/public-law direct-review
disposition, and bill-law spine context. It separates base U.S.C. section
metadata context from stricter exact target-reference/subsection flags and
public-law context; it is not implementation-outcome, direct target-section
court-review, effective-text, causal, welfare, or model-validation evidence.
`make statutory-lineage-effective-text-review` reviews the 73 positive
target-section diff rows against official OLRC current U.S. Code page metadata
and current public-law note scans. `make
statutory-lineage-public-law-attribution-review` then reviews those same rows
against official GovInfo public-law text scans, annual OLRC pre/post text-diff
cues, and the effective-text review. These close bounded effective-text and
target-diff public-law attribution layers only; complete codified lineage,
implementation outcomes, direct target-section court review, welfare evidence,
and model validation remain open.
`make statutory-lineage-completion-queue` and `make
statutory-lineage-complete-lineage-expansion-queue` convert those open gates
into ranked follow-up work surfaces. The expansion queue joins source-scan
candidate counts, target triage, review packets, source-reviewed diffs,
effective-text review, and bounded public-law attribution review to identify
which public laws still need target-inventory expansion or final
complete-lineage audit. It is not complete codified-lineage evidence.
`make statutory-lineage-target-packet-expansion-queue` then decomposes the
triage-to-packet gap into row-level OLRC packet-building tasks for target
references already present in the target-section triage but absent from the
current review-packet set. It is not codified-lineage or target-section diff
evidence.
`make statutory-lineage-target-packet-source-gap-queue` classifies those
packet-building tasks by current-source blocker: fetched current OLRC pages
without public-law markers, fetched current OLRC pages with public-law markers
but no downstream packet, and manual current-scan source-gap review rows. It is
not codified-lineage or target-section diff evidence.
`make statutory-lineage-target-packet-source-gap-review` adds curated
official-source dispositions for reviewed current-OLRC no-marker blockers. The
current review layer covers 50 blockers across 10 public laws and separates 17
temporary overrides, 17 appropriation-authority or program-authority references,
4 table or preceding-section cues, and 12 cross-reference-only rows while
preserving the boundary that these dispositions are not codified-lineage or
target-section diff evidence.

A bounded district public-opinion proxy can be generated from the Cumulative CES
Common Content on Harvard Dataverse with:

```sh
make build-district-public-opinion-raw ARGS="--year 2024 --min-support-respondents 30"
```

This writes `data/validation/raw/district_public_opinion.csv` and
`data/validation/raw/district_public_opinion.metadata.md`. The builder downloads
and caches the CES Feather file under `no-include/validation-cache/ces/` unless
`--source-file` is supplied. It requires `pyarrow` because Dataverse distributes
the normalized Cumulative CES file as Feather. The output is a direct weighted
district aggregation, not MRP, not bill-topic opinion, and not issue-specific
affected-group measurement; `affected_group_share` is an uninsured-share
vulnerability proxy.

A bounded district public-opinion bill-sponsor metadata linkage can be generated
from the CES district aggregate, Congress.gov member terms, and the current
public-law bill/action metadata cache with:

```sh
make build-district-public-opinion-linkage-raw ARGS="--env-file /path/to/.env"
```

This writes `data/validation/raw/district_public_opinion_linkage.csv` and
`data/validation/raw/district_public_opinion_linkage.metadata.md`. It links some
CES district-opinion rows to House-sponsored public-law bill metadata by sponsor
district. It does not measure bill-topic public support, MRP estimates,
issue-specific affected-group support or harm, representative responsiveness,
welfare, or causal public-benefit validation.

A bounded district public-opinion policy-context cache can be generated from the
local district linkage cache and topic-throughput rows with:

```sh
make build-district-public-opinion-policy-context-raw
```

This writes `data/validation/raw/district_public_opinion_policy_context.csv` and
`data/validation/raw/district_public_opinion_policy_context.metadata.md`. It
preserves one row per cached sponsor-district public-law bill metadata row and
adds local bill policy-area topic context only. It does not measure
issue-specific bill support, MRP estimates, issue-specific affected-group support
or harm, representative responsiveness, welfare, or causal public-benefit
validation.

A bounded district public-opinion Census denominator cache can be generated from
the source-packet queue and Census TIGERweb with:

```sh
make build-district-public-opinion-census-denominators-raw
```

This writes `data/validation/raw/district_public_opinion_census_denominators.csv`
and `data/validation/raw/district_public_opinion_census_denominators.metadata.md`.
It queries the no-key Census TIGERweb 116th Congressional District layer for the
queued 117th Congress sponsor districts and preserves 2020 population,
housing-unit, land/water area, and centroid fields. It does not fetch ACS
socioeconomic, veteran, citizenship, language, disability, employment, income,
internet-access, survey, MRP, issue-specific support, affected-group harm, or
public-benefit evidence.

A bounded campaign-finance issue-context bridge can be generated from the local
OpenFEC transaction sample, FEC recipient metadata cache, and local topic
throughput with:

```sh
make build-campaign-finance-issue-context-raw
```

This writes `data/validation/raw/campaign_finance_issue_context.csv` and
`data/validation/raw/campaign_finance_issue_context.metadata.md`. It maps
high-confidence occupation, employer, or expenditure-purpose labels to broad
local policy-area topics and retains unmapped labels. It does not provide
bill-level influence, committee jurisdiction, reviewed outside-spending targets,
legislative outcomes, private-contributor details, causal capture validation, or
model-validation evidence.

A bounded comparative-institutions profile can be generated from QoG Data
Finder selected variables and OWID/V-Dem Grapher CSVs with:

```sh
make build-comparative-institutions-raw
```

This writes `data/validation/raw/comparative_institutions.csv` and
`data/validation/raw/comparative_institutions.metadata.md`. The normalized rows
use QoG/DES lower-house district magnitude, QoG/DES effective legislative-party
counts, QoG/Henisz POLCON effective-chamber indicators, OWID/V-Dem judicial
constraints, and OWID/V-Dem legislative constraints. The
`legislative_productivity` column is a schema-compatible legislative-capacity
proxy, not observed law-output productivity.

A bounded comparative-institution to simulator scenario-family metadata bridge
can be generated from the cached comparative-institutions profile with:

```sh
make build-comparative-institution-linkage-raw
```

This writes `data/validation/raw/comparative_institution_linkage.csv` and
`data/validation/raw/comparative_institution_linkage.metadata.md`. It classifies
country-year rows into chamber, district-magnitude, party-system,
judicial-review, and legislative-constraint bands and maps them to bounded
simulator scenario-family anchors. It does not provide observed law-output
productivity, bicameral disagreement, country-level institutional-fit, adoption,
welfare, causal-effect, or model-validation evidence.
