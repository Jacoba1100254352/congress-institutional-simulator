# Data Pipeline and Reproducibility Plan

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

## Pipeline Goal

Build a reproducible benchmark-data pipeline that makes empirical signals available for calibration, sanity checks, and future validation without overstating what each signal proves.

## Current Commands

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make validation-readiness
make empirical-bridge
make empirical-linkage-report
make empirical-linkage-roadmap
make court-law-linkage
make rulemaking-authority-linkage
make rulemaking-history-linkage
make rulemaking-comment-metadata
make rulemaking-comment-records
make rulemaking-comment-text-review
make bill-law-evidence-spine
make bill-law-lifecycle-readiness
make bill-law-lifecycle-next-actions
make bill-law-lifecycle-corpus
make bill-finance-lobbying-review-queue
make bill-finance-lobbying-local-context-review
make bill-finance-lobbying-external-search-review
make bill-finance-lobbying-external-lda-mention-review
make bill-finance-lobbying-campaign-finance-target-scope-review
make bill-finance-lobbying-committee-action-context
make bill-finance-lobbying-committee-action-source-review
make bill-finance-lobbying-roll-call-source-review
make bill-finance-lobbying-member-vote-target-review
make bill-finance-lobbying-source-acquisition-queue
make lobbying-bill-action-context
make lobbying-bill-text-review
make lobbying-bill-disposition-review
make lobbying-bill-manual-disposition-review
make lobbying-bill-medium-disposition-packets
make lobbying-bill-medium-directional-packet-review
make lobbying-bill-medium-position-activity-packet-review
make statutory-lineage-review-queue
make statutory-lineage-source-scan
make statutory-lineage-target-section-triage
make statutory-lineage-olrc-current-scan
make statutory-lineage-olrc-historical-scan
make statutory-lineage-olrc-annual-text-diff
make court-public-law-review-queue
make court-public-law-temporal-triage
make court-public-law-direct-review
make statutory-lineage-target-lifecycle-bridge
make statutory-lineage-codified-progress
make statutory-lineage-effective-text-review
make statutory-lineage-public-law-attribution-review
make statutory-lineage-completion-queue
make statutory-lineage-complete-lineage-expansion-queue
make statutory-lineage-target-packet-expansion-queue
make statutory-lineage-target-packet-source-gap-queue
make statutory-lineage-target-reference-resolution-candidates
make lobbying-bill-policy-context
make campaign-finance-district-context
make campaign-finance-sponsor-bill-context
make district-public-opinion-policy-context
make district-public-opinion-bill-topic-readiness
make district-public-opinion-source-packets
make district-public-opinion-census-denominators
make district-public-opinion-acs-context
make district-public-opinion-survey-source-crosswalk
make district-public-opinion-survey-item-proxy-review
make district-public-opinion-ces-policy-item-candidate-review
make district-public-opinion-ces-policy-item-response-distribution-review
make validation-gap-report
make raw-source-manifest
make calibration-check
```

Optional network/data rebuilds:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-core-raw-validation
make build-campaign-finance-raw
make build-campaign-finance-linkage-raw
make build-district-public-opinion-raw
make build-district-public-opinion-linkage-raw
make build-district-public-opinion-policy-context-raw
make build-district-public-opinion-census-denominators-raw
make build-district-public-opinion-acs-context-raw
make build-district-public-opinion-ces-policy-item-candidates-raw
make build-district-public-opinion-ces-policy-item-response-distributions-raw
make district-public-opinion-ces-source-freshness
make build-court-review-raw
make build-court-law-linkage-raw
make build-rulemaking-implementation-raw
make build-rulemaking-implementation-linkage-raw
make build-rulemaking-authority-linkage-raw
make build-rulemaking-history-linkage-raw
make build-rulemaking-comment-metadata-raw
make build-rulemaking-comment-records-raw
make build-rulemaking-comment-text-review-raw
make build-law-revision-raw
make build-law-revision-bill-linkage-raw
make build-statutory-lineage-olrc-historical-scan-raw
make build-statutory-lineage-olrc-annual-text-diff-raw
make build-comparative-institutions-raw
```

## Current Inputs and Outputs

Inputs under current readiness workflow:

- `voteview_rollcalls.csv`
- `bill_progression.csv`
- `lobbying_disclosure.csv`
- `topic_throughput.csv`
- `sponsor_success.csv`
- `district_public_opinion.csv`
- `committee_activity.csv`
- `campaign_finance.csv`
- `court_review.csv`
- `rulemaking_implementation.csv`
- `law_revision_history.csv`
- `comparative_institutions.csv`

Outputs:

- `reports/empirical-validation-readiness.csv`
- `reports/empirical-validation-summary.csv`
- `reports/empirical-bridge.csv`
- `reports/empirical-flow-heldout.csv`
- `reports/empirical-data-inventory.csv`
- `reports/empirical-linkage-report.csv`
- `reports/empirical-linkage-roadmap.csv`
- `reports/court-law-linkage.csv`
- `reports/rulemaking-authority-linkage.csv`
- `reports/rulemaking-history-linkage.csv`
- `reports/rulemaking-comment-metadata.csv`
- `reports/rulemaking-comment-records.csv`
- `reports/rulemaking-comment-text-review.csv`
- `reports/bill-law-evidence-spine.csv`
- `reports/bill-law-lifecycle-readiness.csv`
- `reports/bill-law-lifecycle-next-actions.csv`
- `reports/bill-law-lifecycle-corpus.csv`
- `reports/bill-finance-lobbying-review-queue.csv`
- `reports/bill-finance-lobbying-local-context-review.csv`
- `reports/bill-finance-lobbying-external-search-review.csv`
- `reports/bill-finance-lobbying-external-lda-mention-review.csv`
- `reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv`
- `reports/bill-finance-lobbying-committee-action-context.csv`
- `reports/bill-finance-lobbying-committee-action-source-review.csv`
- `reports/bill-finance-lobbying-roll-call-source-review.csv`
- `reports/bill-finance-lobbying-member-vote-target-review.csv`
- `reports/bill-finance-lobbying-source-acquisition-queue.csv`
- `reports/lobbying-bill-action-context.csv`
- `reports/lobbying-bill-text-review.csv`
- `reports/lobbying-bill-disposition-review.csv`
- `reports/lobbying-bill-manual-disposition-review.csv`
- `reports/lobbying-bill-medium-disposition-packets.csv`
- `reports/lobbying-bill-medium-directional-packet-review.csv`
- `reports/lobbying-bill-medium-position-activity-packet-review.csv`
- `reports/statutory-lineage-review-queue.csv`
- `reports/statutory-lineage-source-scan.csv`
- `reports/statutory-lineage-target-section-triage.csv`
- `reports/statutory-lineage-olrc-current-scan.csv`
- `reports/statutory-lineage-olrc-historical-scan.csv`
- `reports/statutory-lineage-olrc-annual-text-diff.csv`
- `reports/statutory-lineage-adjudication.csv`
- `reports/statutory-lineage-target-review-packets.csv`
- `reports/statutory-lineage-target-section-diff-review.csv`
- `reports/statutory-lineage-target-lifecycle-bridge.csv`
- `reports/statutory-lineage-codified-progress.csv`
- `reports/statutory-lineage-effective-text-review.csv`
- `reports/statutory-lineage-public-law-attribution-review.csv`
- `reports/statutory-lineage-completion-queue.csv`
- `reports/statutory-lineage-complete-lineage-expansion-queue.csv`
- `reports/statutory-lineage-target-packet-expansion-queue.csv`
- `reports/statutory-lineage-target-packet-source-gap-queue.csv`
- `reports/statutory-lineage-target-reference-resolution-candidates.csv`
- `reports/court-public-law-review-queue.csv`
- `reports/court-public-law-temporal-triage.csv`
- `reports/court-public-law-direct-review.csv`
- `reports/lobbying-bill-policy-context.csv`
- `reports/campaign-finance-district-context.csv`
- `reports/campaign-finance-sponsor-bill-context.csv`
- `reports/district-public-opinion-policy-context.csv`
- `reports/district-public-opinion-bill-topic-readiness.csv`
- `reports/district-public-opinion-source-packets.csv`
- `reports/district-public-opinion-census-denominators.csv`
- `reports/district-public-opinion-acs-context.csv`
- `reports/district-public-opinion-survey-source-crosswalk.csv`
- `reports/district-public-opinion-survey-item-proxy-review.csv`
- `reports/district-public-opinion-ces-policy-item-candidate-review.csv`
- `reports/district-public-opinion-ces-policy-item-response-distribution-review.csv`
- `reports/district-public-opinion-ces-source-freshness.csv`
- `reports/validation-boundary-matrix.csv`
- `reports/empirical-validation-gap-report.csv`
- `reports/raw-source-manifest.csv`
- `reports/calibration-baseline.csv`

## Proposed Pipeline Stages

### Stage 1: Source Registry

Create:

- `data/validation/source-registry.csv`
- `reports/empirical-data-inventory.csv`

Fields:

- source family;
- specific source;
- access method;
- license/terms;
- API key required;
- network required;
- cache path;
- refresh command;
- row count;
- date range;
- unit of observation;
- simulator metric family;
- boundary category.

### Stage 2: Raw Fetch and Cache

Rules:

- Network fetches should be optional.
- Offline artifact review must use cached summaries.
- API keys must not be required for core reproduction.
- Raw-data transformations should write provenance manifests.
- `make raw-source-manifest` writes the current registry-backed offline manifest
  with raw row counts, metadata-note paths, source hashes, claim boundaries, and
  refresh scripts.
- `make rulemaking-authority-linkage` writes a bounded Federal Register
  public-law authority-search report showing which cached public-law rows have
  text-verified rule documents that cite the public law.
- `make rulemaking-history-linkage` writes a bounded Federal Register
  proposed-history report showing which authority-matched final-rule rows have
  proposed-rule metadata sharing RIN or docket identifiers.
- `make rulemaking-comment-metadata` writes a bounded Federal Register-exposed
  Regulations.gov metadata report for authority-matched final-rule chains. It
  records docket IDs, comment URLs, comment counts, and comment-close dates only;
  it is not comment-record evidence by itself, commenter-identity,
  comment-text, enforcement, appropriations, or model-validation evidence.
- `make build-rulemaking-comment-records-raw` optionally fetches bounded public
  Regulations.gov comment-record metadata for dockets within configured known
  comment-count thresholds, preserves partial retrieved metadata after API
  errors, and records zero-comment, high-volume, unknown-count, or API-blocked
  rows without treating absent records as evidence.
- `make rulemaking-comment-records` writes the offline report for that bounded
  comment-record cache. Complete rows mean all public comment-record metadata
  for a docket within the configured retrieval threshold was retrieved, or
  Federal Register metadata exposed zero expected comments. Partial rows do not
  prove completeness. It is not comment text, attachments, commenter identity,
  sentiment, Unified Agenda, enforcement, appropriations, implementation
  outcome, welfare, causal, or model-validation evidence.
- `make build-rulemaking-comment-text-review-raw` optionally fetches bounded
  public Regulations.gov comment-detail records for complete comment-record
  metadata rows with retrieved comment IDs and bounded partial-docket samples.
  It stores text availability, normalized text hashes, lengths, attachment
  counts, source record status, and coarse implementation cue flags while
  omitting the full comment body and submitter/contact fields. Partial sample
  rows do not prove complete docket coverage.
- `make rulemaking-comment-text-review` writes the offline report for that
  sanitized detail cache. It is not a full comment-text corpus, attachment-text
  review, commenter-identity validation, sentiment or position coding,
  implementation outcome, welfare, causal, or model-validation evidence.
- `make court-law-linkage` writes a bounded SCDB/Federal Register U.S.C.-section
  authority-overlap report showing which merits-case rows overlap authority
  sections attached to cached public-law rows.
- `make bill-law-evidence-spine` writes a bounded public-law bill/action spine
  showing which current public-law rows carry revision-text proxy fields,
  sponsor-district public-opinion context, bounded sponsor-district bill
  policy-area context, same-policy campaign-finance sponsor context,
  same-policy LDA issue/bill context, authority-search matches,
  proposed-history matches, Federal Register-exposed Regulations.gov
  docket/comment metadata, bounded complete or skipped Regulations.gov
  comment-record metadata, final-rule and proposed-to-final timing metadata,
  court U.S.C.-section overlaps, and unresolved joins.
- `make bill-law-lifecycle-readiness` writes a generated review queue ranking
  public-law spine rows by direct metadata, context-only metadata, unresolved
  high-priority lifecycle gates, the next source-backed upgrade gate, and
  copied source pointers for the next review pass. It is a work queue, not
  validation evidence.
- `make bill-law-lifecycle-next-actions` writes a post-disposition action queue
  after court/public-law direct-review review, closing direct-review gates that
  are temporally excluded or source-reviewed not direct and moving those rows to
  the next actionable lifecycle gate. It is not validation evidence.
- `make statutory-lineage-review-queue` writes a codified U.S.C. lineage
  source-review queue for rows whose post-disposition next action is
  `codified_usc_lineage`, carrying public-law, law-revision,
  authority-document, U.S.C.-citation, proposed-rule, docket, and court-overlap
  pointers. It is not statutory-lineage evidence.
- `make statutory-lineage-source-scan` writes an official GovInfo public-law
  text scan report for that queue, preserving source hashes, U.S.C.-reference
  counts, amendment/repeal/redesignation counts, and compact candidate snippets.
  It is not OLRC classification, codified-lineage evidence, or target-section
  text diffs.
- `make statutory-lineage-target-section-triage` normalizes those candidate
  U.S.C. references into a bounded target-section review queue for OLRC and
  codified-text follow-up. It is not codified-lineage evidence or target-section
  text diffs.
- `make statutory-lineage-olrc-current-scan` writes the offline report for
  official OLRC current U.S. Code page availability rows. It records current
  section source hashes and public-law mentions, but it is not historical
  codified-lineage evidence or before/after target-section text diffs.
- `make statutory-lineage-olrc-historical-scan` writes the offline report for
  official OLRC annual U.S. Code page availability rows. It records
  year-before-enactment and enactment-year source hashes and public-law mention
  windows, but it is not codified-lineage evidence, public-law causation, or
  before/after target-section text diffs.
- `make statutory-lineage-olrc-annual-text-diff` writes the offline report for
  bounded automated annual-page text cues. It records post-edition public-law
  context snippets and manual-review priorities, but it is not source-reviewed
  codified-lineage evidence, public-law causation, or adjudicated target-section
  text diffs.
- `make court-public-law-review-queue` writes a bounded case/public-law review
  queue for SCDB/Federal Register U.S.C.-section overlap rows. It is designed
  to drive direct source review and does not itself prove direct court review,
  interpretation, invalidation, emergency-order coverage, causal effects, or
  model validation.
- `make court-public-law-temporal-triage` applies a date screen to that queue,
  using cached public-law enacted dates to rule out pre-enactment cases as
  direct review of the listed law and isolate post-enactment rows for source
  review. It does not prove direct court review.
- `make court-public-law-direct-review` records source-reviewed dispositions for
  post-enactment court/public-law tasks and generated temporal exclusions for
  pre-enactment rows. It now includes source-evidence summaries for reviewed
  post-enactment rows and a grouped temporal-exclusion summary by public law. It
  can close a direct-review task as reviewed not direct, but it is not
  lower-court, emergency-order, implementation-outcome, causal-invalidation,
  welfare, or model-validation evidence.
- `make statutory-lineage-target-lifecycle-bridge` attaches reviewed
  target-section diff rows to bounded public-law-level implementation
  authority, rulemaking history, Federal Register-exposed comment metadata,
  court-overlap, direct-review disposition, raw SCDB target-section citation
  context, and bill-law spine context. Exact U.S.C. section overlaps remain
  metadata, raw SCDB overlaps are date-screened section-citation context, and
  public-law context is not target-section implementation, direct court-review,
  causation, welfare, or model-validation evidence.
- `make statutory-lineage-no-target-review` writes curated source-reviewed
  no-target dispositions for designation laws whose official GovInfo
  public-law text and OLRC public-law PDFs expose no U.S.C. references,
  amendment/repeal/redesignation cues, or target-section candidates. It is not
  target-section text-diff, implementation-outcome, court-review, welfare, or
  model-validation evidence.
- `make statutory-lineage-codified-progress` classifies the 15
  codified-lineage progress rows into source-reviewed target-diff coverage
  versus reviewed designation-law no-structured-U.S.C.-target dispositions. It
  is progress tracking, not full codified lineage, target-section text-diff
  evidence for designation laws, effective text, causation, welfare, or
  validation evidence.
- `make statutory-lineage-effective-text-review` reviews the 73
  source-reviewed target-section diff rows against official OLRC current U.S.
  Code page metadata and current public-law note scans. It records
  effective-text source review, not exclusive public-law causation, complete
  lineage, implementation, court-review, welfare, or validation evidence.
- `make statutory-lineage-public-law-attribution-review` reviews the same 73
  source-reviewed target-section diff rows against official GovInfo
  public-law text scans, annual OLRC pre/post target-section text-diff cues,
  and effective-text source review. It records bounded target-section
  public-law attribution review, not complete codified lineage,
  implementation, court-review, welfare, causal-effect, or validation evidence.
- `make statutory-lineage-completion-queue` ranks those 15 candidates for the
  next completion pass, preserving that 13 positive target-diff public laws
  now have effective-text and bounded public-law attribution review rows while
  complete lineage, implementation, direct target-section court-review,
  welfare, and validation gates remain open. It is a work queue, not full
  lineage, implementation, court-review, welfare, or validation evidence.
- `make statutory-lineage-complete-lineage-expansion-queue` turns that open
  complete-lineage gate into a ranked target-inventory expansion surface. It
  keeps source-scan candidate gaps, triage-to-packet gaps, final audit work,
  and reviewed no-structured-target dispositions explicit without upgrading the
  statutory-lineage claim boundary.
- `make statutory-lineage-target-packet-expansion-queue` turns triage-to-packet
  gaps into row-level OLRC packet-construction tasks for already-triaged
  references that are absent from the target-review packet set. It is a
  packet-building queue, not lineage evidence.
- `make statutory-lineage-target-packet-source-gap-queue` classifies why those
  packet-expansion rows have not advanced into historical OLRC, annual
  text-diff, adjudication, or target-review packet layers. It is a source-gap
  blocker queue, not lineage evidence.
- `make statutory-lineage-target-reference-resolution-candidates` pairs the
  ambiguous title-only and incomplete source-gap rows with ordered GovInfo
  public-law source-scan snippets to suggest bounded concrete U.S.C. candidates
  for manual review. It is not confirmed target-section or lineage evidence.
- `make bill-finance-lobbying-review-queue` isolates public-law rows whose
  next lifecycle gate is bill-specific finance or lobbying evidence. It carries
  forward same-policy FEC/LDA context and exact-match flags for source review,
  but it is not evidence of bill targeting, influence, capture, public benefit,
  legislative outcome causality, or model validation.
- `make bill-finance-lobbying-local-context-review` source-reviews that queue
  against current local same-policy campaign-finance sponsor context and LDA
  issue/bill context. It records no current-bill exact match for the local
  context rows and leaves external target/source expansion open; it is not
  absence-of-spending, targeting, influence, outcome, welfare, capture, or
  model-validation evidence.
- `make bill-finance-lobbying-external-search-review` summarizes the targeted
  official LDA external current-bill search cache and FEC/OpenFEC source-scope
  triage for that queue. It records exact LDA activity-text bill-reference rows
  for 2 queued bills and marks 4 campaign-finance rows for candidate,
  committee, or outside-spending target-scope review; it is not lobbying-contact,
  campaign-finance influence, committee-action, roll-call, outcome, welfare,
  capture, or model-validation evidence.
- `make bill-finance-lobbying-external-lda-mention-review` source-reviews the
  external LDA exact mention rows as filing packets. It classifies 19 packets
  representing 55 rows, with 0 packets carrying explicit support/opposition
  text, named sponsor/member/committee targets, committee-action influence,
  roll-call influence, or outcome-causality evidence.
- `make bill-finance-lobbying-campaign-finance-target-scope-review`
  source-reviews the 4 queued campaign-finance rows against public FEC/OpenFEC
  target-scope fields. It records 0 current-bill ID matches, sponsor/candidate
  overlaps, committee-action links, or outcome-influence links.
- `make bill-finance-lobbying-committee-action-context` joins the 10 queued
  rows to cached public bill-action metadata and current LDA/FEC review
  dispositions. It records committee/floor flags only, not committee names,
  committee-action influence, roll-call influence, outcome causality, welfare,
  capture, or validation evidence.
- `make bill-finance-lobbying-committee-action-source-review` source-reviews
  official govinfo BILLSTATUS committee/action metadata for those 10 queued
  rows. It records 9 committee-name rows, 10 committee-action rows, 10
  floor-action rows, 8 BILLSTATUS roll-call-reference rows, and 10 public-law
  outcome metadata rows without upgrading any influence claim.
- `make bill-finance-lobbying-roll-call-source-review` caches official House
  Clerk roll-call XML for the 8 numbered House roll calls, confirms 8 bill-ID
  matches, classifies 2 floor-action rows without numbered roll calls, and
  represents 3,435 member-vote rows as vote-source context only.
- `make bill-finance-lobbying-member-vote-target-review` joins those official
  House Clerk member-vote rows to reviewed public FEC/OpenFEC candidate/member
  context by Bioguide, recording 0 same-bill reviewed campaign target overlaps
  and 40 broad public FEC member-context overlaps as target-scope context only.
- `make bill-finance-lobbying-source-acquisition-queue` ranks those 10 rows for
  committee/no-direct-committee dispositions, direct member target documents,
  independent target-source, and outcome-document follow-up. It is acquisition
  planning only, not finance/lobbying influence evidence.
- `make lobbying-bill-policy-context` writes a bounded LDA issue-label to
  cached govinfo bill/action context report by shared policy area. It is useful
  for issue-level exposure context, but it is not client-to-specific-bill,
  sponsor-target, committee-action, roll-call, legislative-outcome, or capture
  evidence.
- `make lobbying-bill-mention-review` writes a bounded official LDA filing-text
  bill-reference review for the public-law candidate set. It records exact
  current-bill identifiers where the filing activity text mentions a bill, but
  it is not support/opposition, sponsor-target, committee-action, roll-call,
  legislative-outcome, influence, capture, welfare, or validation evidence.
- `make lobbying-bill-action-context` joins those exact LDA filing-text bill
  identifiers to cached Congress.gov public-law bill/action, sponsor,
  committee-reported, floor-considered, and enacted-outcome metadata. It is
  identifier and legislative metadata context only, not support/opposition,
  sponsor-target, committee-action, roll-call, legislative-outcome causality,
  influence, capture, welfare, or validation evidence.
- `make lobbying-bill-text-review` reviews the stored LDA activity-text
  excerpts for those exact bill mentions. It separates rows where the stored
  excerpt contains the bill reference from rows needing full activity-text
  refetch, and classifies bounded support, opposition, position/activity, and
  bill-list text signals. It is text-signal evidence only, not manual
  disposition, sponsor-target, committee-action, roll-call, legislative-outcome
  causality, influence, capture, welfare, or validation evidence.
- `make campaign-finance-district-context` writes a bounded OpenFEC
  candidate-recipient district-context report showing which House candidate
  rows can be joined to CES district public-opinion context.
- `make campaign-finance-sponsor-bill-context` writes a bounded OpenFEC
  candidate/member to sponsored-bill context report showing which matched
  candidate rows can be joined by Bioguide ID to cached govinfo bill metadata.
- `make district-public-opinion-policy-context` writes a bounded
  sponsor-district public-law bill policy-area context report showing which CES
  district proxy rows attach to local bill policy-area context.
- `make district-public-opinion-bill-topic-readiness` writes a 22-bill
  readiness queue showing which public-law rows remain proxy-only for
  bill-topic support and affected-group support/harm.
- `make district-public-opinion-source-packets` writes survey, MRP/small-area,
  and affected-population source-acquisition packets for those queued rows
  without treating the packets as acquired evidence.
- `make district-public-opinion-census-denominators` joins those source
  packets to official Census TIGERweb 116th congressional-district 2020
  population and housing-unit denominators; this is denominator context only,
  not bill-topic support, MRP/small-area, ACS policy-specific affected
  population, or affected-group harm evidence.
- `make district-public-opinion-acs-context` joins those source packets to
  official ACS 2017-2021 broad 116th congressional-district demographic,
  economic, citizenship, language, disability, internet, poverty, employment,
  and veteran context; this is broad district context only, not bill-topic
  support, MRP/small-area, bill-text-specific affected population, or
  affected-group harm evidence.
- `make district-public-opinion-survey-source-crosswalk` maps those source
  packets to official survey/source families and candidate item-search terms;
  this is source-review planning only, not acquired survey item IDs,
  bill-topic support, MRP/small-area, bill-text-specific affected population,
  or affected-group harm evidence.
- `make district-public-opinion-survey-item-proxy-review` records the exact
  current CES proxy variables attached to those source packets; this is
  proxy-variable review only, not acquired bill-topic item IDs, bill-topic
  support, MRP/small-area, bill-text-specific affected population, or
  affected-group harm evidence.
- `make build-district-public-opinion-ces-policy-item-candidates-raw` fetches
  official Cumulative CES Policy Preferences source metadata and validates the
  tabular header against the expected 54 policy-preference variables.
- `make district-public-opinion-ces-policy-item-candidate-review` joins queued
  source packets to those official policy-preference variable IDs where broad
  policy-area candidates exist; this is candidate item metadata only, not
  source-reviewed exact bill-topic support, MRP/small-area estimation, or
  affected-group evidence.
- `make build-district-public-opinion-ces-policy-item-response-distributions-raw`
  streams the official Cumulative CES Policy Preferences tabular file and writes
  unweighted raw response-code distributions for the 54 policy-preference
  variables. It is raw response-code context only, not recoded support/opposition
  direction.
- `make district-public-opinion-ces-policy-item-response-distribution-review`
  joins queued source packets to those raw response-code distributions where
  candidate variables exist; this is not source-reviewed exact bill-topic
  support, MRP/small-area estimation, or affected-group evidence.
- `make build-district-public-opinion-ces-policy-item-codebook-direction-raw`
  parses the official Cumulative CES Policy Preferences guide and records
  guide response labels, endpoint labels, and item-wording direction types for
  the 54 policy-preference variables. It is codebook response-direction context
  only, not bill-text-aligned support/opposition.
- `make district-public-opinion-ces-policy-item-codebook-direction-review`
  joins queued source packets to those guide labels where candidate variables
  exist; this is not source-reviewed exact bill-topic support,
  bill-text-aligned support/opposition, MRP/small-area estimation, or
  affected-group evidence.
- `make build-district-public-opinion-bill-text-context-raw` reuses a matching
  committed cache by default and, with `ARGS=--refresh`, fetches official
  GovInfo BILLSTATUS titles, legislative subjects, and latest CRS summaries for
  all 22 queued packets.
- `make district-public-opinion-bill-item-alignment-review` records one curated
  bill-to-item disposition per packet. The current review retains one
  historical related-issue item and preserves 21 negative dispositions.
- `make build-district-public-opinion-bill-topic-support-raw` reuses a matching
  aggregate cache by default. With `ARGS=--refresh`, it joins retained items only
  to pinned annual CCES geography and validated-voter weights, verifies the
  downloaded bytes against the pinned checksums, confirms each question's
  pre-election wave from the pinned annual guide, and checks every nonmissing
  cumulative response against the original annual question field. It publishes
  aggregate district rows above the 30-response threshold with no respondent
  identifiers.
- `make district-public-opinion-bill-topic-support` writes the two current
  annual NY-10 estimates as historical related-issue context. It does not pool
  years or claim exact, contemporaneous, MRP, uncertainty, affected-group,
  causal, or model-validation evidence.

Candidate targets:

```make
fetch-congressgov-bill-history
fetch-govinfo-billstatus
fetch-voteview-rollcalls
fetch-lda-lobbying
fetch-openfec-finance
fetch-committee-activity
fetch-rulemaking-implementation
fetch-law-revision-history
fetch-comparative-institutions
```

### Stage 3: Normalization

Normalize every source into a stable schema:

- observation ID;
- chamber/session/date;
- bill or issue identifier;
- actor identifier;
- issue/topic/domain;
- action type;
- amount/count/share;
- source provenance;
- transformation notes.

### Stage 4: Empirical Signal Summaries

Produce one summary table per signal family:

- bill flow;
- roll-call behavior;
- lobbying concentration;
- campaign finance;
- topic throughput;
- sponsor effectiveness;
- district opinion;
- committee process;
- court review;
- implementation feedback;
- law revision;
- comparative institutions.

### Stage 5: Metric Mapping and Boundary Classification

For each summary statistic:

- map to simulator metric/proxy;
- assign boundary category;
- define target range or validation target if appropriate;
- mark unsupported claims.

### Stage 6: Linkage Audit

For each source family:

- identify whether current rows can join to another bill, topic, statute,
  agency, court, sponsor, committee, or public-opinion source family;
- count linked rows and linked share from the cached raw CSVs;
- preserve a `not independently linked` status when a registry row is only
  represented through another source-family cache;
- keep linked evidence separate from source-family held-out benchmark evidence.

Current status: `reports/empirical-linkage-report.md` reports 13 / 13 source
families as linked, metadata-linked, or partially linked. Govinfo BILLSTATUS
rows now cross-check the bounded Congress.gov bill sample; sponsor aggregate
rows now join to bounded bill metadata for 22 / 22 sponsor rows; Voteview roll-call
rows now carry public member metadata plus a bounded bill-number crosswalk for
sampled roll calls, but still lack complete bill/action, public-law, topic,
district-opinion, implementation, court, or outcome linkage. LDA rows now carry
issue-policy context, cached bill/action context by shared policy area, exact
filing-text bill identifiers, exact bill/action metadata context, bounded
stored full activity-text support/opposition/position signals, and a
disposition/target source-review queue plus high-priority manual
disposition/target review for a bounded public-law subset, but still lack
medium-priority manual disposition confirmation,
sponsor/member targeting beyond activity-text references,
committee-action, roll-call, legislative-outcome causality, influence, capture,
welfare, or model-validation linkage. OpenFEC campaign
finance has FEC recipient metadata plus bounded issue-sector topic context,
House-candidate district context, and matched-candidate member-context subsets;
district public opinion has sponsor-district public-law bill metadata plus
bounded bill policy-area context, a bill-topic readiness queue,
  source-acquisition packets, Census population/housing denominators, broad
  ACS district context, survey-source crosswalk planning, exact current CES
  proxy-variable review, official CES policy-preference candidate-item
  metadata, unweighted raw CES response-code distributions, and official guide
  codebook item-direction labels. It now also has 22 official bill-text
  dispositions, one retained historical related-issue alignment, 21 negative
  dispositions, and two privacy-thresholded annual district aggregates. The
  retained item is not the bill wording and predates enactment; exact or
  contemporaneous bill support, design-based uncertainty, MRP/small-area estimates,
  bill-text-specific affected-population detail, and affected-group evidence
  remain absent; implementation is linked
to Federal Register document/docket metadata, bounded authority-search matches,
bounded proposed-history matches, bounded comment metadata, bounded
comment-record metadata, and bounded timing metadata; court review is linked only through
bounded SCDB/Federal Register U.S.C.-section authority overlaps; and statutory
revision is linked to bounded Congress.gov bill/action metadata plus Federal
Register authority-search, proposed-history, comment metadata,
comment-record metadata, timing, and court-overlap metadata. No high-priority family is
wholly unlinked, but all high-priority acceptance gates still require joins
beyond metadata or proxy boundaries.
`reports/empirical-linkage-roadmap.md` converts the 10 non-fully-linked
families into required join keys, minimum viable datasets, and acceptance gates.
`reports/bill-law-evidence-spine.md` then exposes the current public-law rows as
the bill-centered spine available from cached metadata, including same-policy
campaign-finance sponsor context, same-policy LDA issue/bill context, exact
official LDA filing-text bill identifiers for 26 public-law rows, and bounded
stored LDA activity-text signals. It is useful for audit and future joins, but
it is still not bill-topic opinion,
bill-specific campaign-finance or lobbying influence, implementation outcome,
high-volume comment-record evidence, comment text, direct court-review
disposition, or codified statutory lineage.
`reports/bill-law-lifecycle-readiness.md` ranks those spine rows for the next
direct-linkage pass; it is a queue for review, not a claim upgrade.
`reports/bill-law-lifecycle-next-actions.md` refines that queue after
court/public-law source review so closed direct-review tasks do not remain the
next actionable evidence gate.
`reports/bill-law-lifecycle-corpus.md` joins that action queue to the current
public-opinion proxy review, finance/lobbying source review, statutory-lineage
progress, implementation/comment-detail review, and court direct-review
dispositions. It is the durable public-law-by-public-law corpus for future
source acquisition, not validation evidence.
`reports/lobbying-bill-mention-review.md` records 484 exact official LDA
activity-text bill mention rows across 26 cached public-law bill IDs from 40
searched public-law rows. It is bill-identifier evidence only, not
influence, capture, outcome, welfare, or validation evidence.
`reports/lobbying-bill-action-context.md` joins those 26 exact-mentioned bill
IDs to cached Congress.gov public-law bill/action metadata, including sponsor
metadata for 26, committee-reported flags for 21, floor-considered flags for
26, and enacted public-law outcome metadata for 26. It is identifier and
legislative metadata context only, not support/opposition, targeting,
committee-action, roll-call, outcome-causality, influence, capture, welfare, or
validation evidence.
`reports/lobbying-bill-text-review.md` then reviews the stored LDA activity
text for those cached exact-match rows. It represents 484 cached exact-match
rows, locates the bill reference in all 484 stored full-text rows, and
classifies 46 support-only rows, 3 opposition-only rows, 2 mixed
support/opposition rows, 104 position/activity rows without direction, and 329
bill-list or title-only rows. `reports/lobbying-bill-disposition-review.md`
prioritizes those same rows for manual disposition and target review: 156 rows
need manual review, with 4 high-priority rows, 152 medium-priority rows, and
328 bill-reference-only rows. `reports/lobbying-bill-manual-disposition-review.md`
source-reviews the 4 high-priority rows, confirming 3 current-bill support rows,
preserving 1 bill-reference-only row, and recording no outcome-influence
evidence. `reports/lobbying-bill-medium-disposition-packets.md` groups the
remaining 152 medium-priority rows into 102 source-review packets, collapsing 50
repeated rows. `reports/lobbying-bill-medium-directional-packet-review.md`
source-reviews the 28 support/opposition packets, confirming 20 current-bill
support packets representing 32 rows and 1 current-bill opposition packet while
downgrading 7 packets to other-measure direction or monitoring/reference
context. These are text signals, bounded source reviews, and review packets
only. `reports/lobbying-bill-medium-position-activity-packet-review.md`
source-reviews the 74 position/activity packets representing 104 rows,
classifying 59 issue/provision activity packets, 5 monitoring/analysis packets,
7 all-provisions packets, 2 position-represented packets, and 1 current-bill
opposition packet found in the position/activity queue. These are not
lobbying-contact, sponsor/member targeting beyond activity-text
references, committee-action, roll-call, outcome-causality, influence, capture,
welfare, or validation evidence.
`reports/bill-finance-lobbying-review-queue.md` then isolates the 10 rows whose
next actionable gate remains bill-specific campaign-finance or lobbying
evidence, with 4 rows carrying same-policy finance context and 9 rows carrying
same-policy lobbying context. It is a source-review queue, not influence,
capture, outcome, welfare, or validation evidence.
`reports/bill-finance-lobbying-local-context-review.md` then source-reviews
those 10 rows against the current local same-policy context, confirming 4
same-policy campaign-finance rows and 9 same-policy lobbying rows have no
current-bill exact match locally, while all 10 rows still require external
target/source expansion and preserve no-outcome-influence status.
`reports/bill-finance-lobbying-external-search-review.md` then adds targeted
official LDA external current-bill search evidence, finding 55 exact
activity-text bill-reference rows across 2 queued bills and complete no-exact
LDA search status for the other 8 rows. It also marks 4 campaign-finance rows
for FEC/OpenFEC candidate, committee, or outside-spending target-scope review.
`reports/bill-finance-lobbying-external-lda-mention-review.md` then
source-reviews those exact external LDA mentions as 19 filing packets,
classifying 16 current-bill issue-reference packets and 3 current-bill
issue-advocacy packets without explicit support/opposition text and preserving
no named target, committee-action, roll-call, or outcome-causality evidence.
`reports/bill-finance-lobbying-campaign-finance-target-scope-review.md` then
source-reviews the 4 campaign-finance rows against cached public FEC/OpenFEC
candidate, committee, receipt, independent-expenditure, member, district, issue,
and same-policy sponsored-bill context. It covers 5 candidate/recipient context
attachments, 5 transaction attachments, 2 unique public FEC candidate
recipients, and 2 unique raw OpenFEC transactions, while preserving 0
current-bill ID matches, 0 reviewed bill sponsor/candidate overlaps, 0
committee-of-jurisdiction or committee-action links, and 0 legislative-outcome
or influence links.
`reports/bill-finance-lobbying-committee-action-context.md` then adds cached
public bill-action committee/floor flags for the 10 queued rows, while
leaving committee names, committee-action influence rows, roll-call influence
rows, and legislative-outcome causality rows to follow-on source review.
`reports/bill-finance-lobbying-committee-action-source-review.md` adds official
govinfo BILLSTATUS source context for those rows, recording 9 committee-name
rows, 10 committee-action rows, 10 floor-action rows, 8 BILLSTATUS roll-call
reference rows, and 10 public-law outcome metadata rows without upgrading any
finance/lobbying influence claim.
`reports/bill-finance-lobbying-roll-call-source-review.md` caches official
House Clerk roll-call XML for the 8 numbered House roll calls, confirms 8
bill-ID matches, classifies 2 floor-action rows without numbered roll calls,
and represents 3,435 member-vote rows as vote-source context only.
`reports/bill-finance-lobbying-member-vote-target-review.md` joins those
member-vote rows to reviewed public FEC/OpenFEC candidate/member context by
Bioguide, records 0 same-bill reviewed campaign target overlaps and 40 broad
public FEC member-context overlaps, and remains target-scope context only.
`reports/bill-finance-lobbying-source-acquisition-queue.md` turns those open
gates into a ranked official-source queue for committee/no-direct-committee
dispositions, direct member target documents, independent target-source, and outcome
documents. It records 9 official govinfo committee-name rows, 1 official
no-direct-committee source-reviewed row, 8 official House Clerk roll-call
source rows, 8 official member-vote target-scope review rows, 2 floor-action
rows without numbered roll calls, 0 rows needing
roll-call source acquisition, 0 rows needing committee-of-jurisdiction source
follow-up, 2 LDA packet-priority rows, and 4 campaign target-scope
priority rows, without upgrading the finance/lobbying claim boundary.
`reports/statutory-lineage-review-queue.md` then isolates the current 15
codified-lineage source-review candidates and makes their official-source
targets explicit before any target-section or text-diff claims are added.
`reports/statutory-lineage-source-scan.md` adds a bounded official GovInfo
public-law text scan for those candidates, which makes amendment and U.S.C.
reference density visible without treating the scan as codified-lineage
evidence.
`reports/statutory-lineage-target-section-triage.md` then normalizes candidate
U.S.C. target references from the source scan into a 15-bill review queue for
OLRC and codified-text follow-up; it still does not upgrade the row to
codified-lineage evidence.
`reports/statutory-lineage-olrc-current-scan.md` adds current official OLRC
U.S. Code page availability and public-law-mention checks for structured target
references, which is useful source scaffolding but still not historical
codified lineage or text-diff evidence.
`reports/statutory-lineage-olrc-historical-scan.md` adds official OLRC annual
edition availability checks for year-before-enactment and enactment-year pages
where the current page mentions the queued public law. It compares hashes and
public-law mentions only; it still does not establish codified lineage,
causation, or before/after text-diff evidence.
`reports/statutory-lineage-olrc-annual-text-diff.md` adds bounded post-edition
public-law context snippets and priority labels for manual OLRC review. It is
useful review scaffolding but still does not establish codified lineage,
causation, or adjudicated target-section text-diff evidence.
`reports/statutory-lineage-target-section-diff-review.md` records the current
thirteen-public-law source-reviewed target-section diff pilot. It upgrades bounded
target packets into reviewed diff dispositions but still leaves public-law
causal attribution, effective text, implementation outcomes, court review,
welfare, and model validation outside the claim boundary.
`reports/statutory-lineage-target-lifecycle-bridge.md` then attaches those
reviewed target-section diff rows to bounded public-law-level implementation
authority, rulemaking history, comment metadata, court overlap, direct-review
disposition, raw SCDB target-section citation context, and bill-law spine
context. It records 2 raw SCDB target base-section overlap rows, 0 exact raw
target-reference rows, and 0 post-enactment target base-section case
attachments without converting public-law-level metadata or raw section
citations into target-section outcome evidence.
`reports/statutory-lineage-codified-progress.md` classifies the 15 current
codified-lineage progress rows by progress status: 13 public laws have
source-reviewed target-section diff rows, while 2 designation laws have
source-reviewed no-structured-U.S.C.-target dispositions. It is progress
tracking only, not full codified-lineage evidence, target-section text-diff
evidence for designation laws, public-law causal attribution, effective
statutory text, implementation outcome, direct court-review evidence, welfare,
causal effects, or model validation.
`reports/statutory-lineage-effective-text-review.md` then records bounded
effective-text source review for the 73 source-reviewed target-section diff
rows using official OLRC current U.S. Code page metadata and current
public-law note scans. It leaves public-law causal attribution, complete
lineage, implementation outcomes, direct court-review evidence, welfare,
causal effects, and model validation outside the claim boundary.
`reports/statutory-lineage-public-law-attribution-review.md` adds bounded
target-section public-law attribution review for those same 73 rows using
official GovInfo public-law text scans, annual OLRC pre/post text-diff cues,
and effective-text source review. It closes the target-diff attribution layer
without claiming complete codified lineage, implementation outcomes, direct
court-review evidence, welfare, causal effects, or model validation.
`reports/statutory-lineage-completion-queue.md` turns that progress classifier
into a next-pass source-review queue. It ranks 15 candidates, keeps 13
source-reviewed target-diff public laws past effective-text and bounded
target-diff attribution review, and preserves 2 no-structured-target
designation laws as claim-boundary rows. It is not a claim upgrade.
`reports/statutory-lineage-complete-lineage-expansion-queue.md` turns that
next-pass queue into a concrete complete-lineage expansion surface by joining
source-scan candidate counts, target triage, review packets, source-reviewed
diffs, effective-text review, and bounded attribution review. It is not a claim
upgrade.
`reports/statutory-lineage-target-packet-expansion-queue.md` then decomposes
the triage-to-packet gap into 50 target-review packet tasks for direct U.S.C.
references, with 0 remaining title-only or incomplete-fragment references. It is packet-construction
planning, not a claim upgrade.
`reports/statutory-lineage-target-packet-source-gap-queue.md` classifies those
50 packet tasks into current-source blockers: 50 fetched current OLRC pages
without a public-law marker, 0 fetched current OLRC pages with a public-law
marker but no downstream packet, and 0 manual current-scan source-gap review rows. It is
source-gap planning, not a claim upgrade.
`reports/statutory-lineage-target-packet-source-gap-review.md` records curated
official-source no-packet dispositions for 50 current-OLRC no-marker blockers
across 10 public laws, separating 17 temporary overrides, 17 appropriation or
program-authority references, 12 cross-reference-only rows, and 4 table or
preceding-section rows. It is blocker disposition review, not a claim upgrade.
`reports/statutory-lineage-target-reference-resolution-candidates.md` reviews
the ambiguous title-only and incomplete packet blockers from that source-gap
queue. The current refreshed source-scan/triage path leaves 0 ambiguous rows, 0
bounded concrete U.S.C. candidates requiring confirmation, and 0 rows without
bounded source-scan candidates. It is target-reference review planning, not a
claim upgrade.
`reports/court-public-law-review-queue.md` breaks the current court-overlap
slice into case/public-law review tasks for direct source checking; it is not a
court-review claim upgrade.
`reports/court-public-law-temporal-triage.md` applies the first automated
screen to those tasks by excluding pre-enactment decisions from direct-review
coding for the listed public law.
`reports/court-public-law-direct-review.md` then records the source-reviewed
disposition for post-enactment tasks and keeps shared-section overlaps separate
from direct public-law review.
`reports/campaign-finance-district-context.md`, `reports/campaign-finance-member-context.md`,
`reports/campaign-finance-issue-context.md`, and
`reports/campaign-finance-sponsor-bill-context.md` expose the current FEC
recipient rows that can be assigned to House candidate districts, Voteview
member metadata, broad local policy topics, or cached sponsored-bill metadata.
They are useful for audit and future member/sponsor joins, but they are still
not campaign-finance influence, committee-action influence, reviewed
outside-spending target evidence, legislative-outcome causality, or capture
evidence.
`reports/bill-finance-lobbying-external-lda-mention-review.md` is now the
reviewed external LDA mention packet layer over those inventories and the LDA
policy context, and `reports/bill-finance-lobbying-committee-action-context.md`
is the cached bill-action committee/floor context layer.
`reports/bill-finance-lobbying-roll-call-source-review.md` is the official
House Clerk vote-source layer for numbered House roll calls.
`reports/bill-finance-lobbying-member-vote-target-review.md` is the official
member-vote target-scope layer that separates public FEC/OpenFEC Bioguide
overlaps from direct member target documents.
`reports/bill-finance-lobbying-source-acquisition-queue.md` is the ranked
official-source target list for the remaining independent contact, target,
committee-action, direct member target document,
roll-call influence, outcome, or external campaign-finance source documents
beyond the public target-scope fields, cached bill-action flags, and vote-source
metadata.

### Stage 7: Calibration and Held-Out Validation

Current state: broad calibration/sanity screens only.

Future requirements:

- define calibration period and held-out period;
- separate target-setting data from evaluation data;
- report errors, tolerance rules, and failures;
- preserve synthetic-only labels for unsupported metrics.

## Reproducibility Plan

Required:

- no-network path for current reports;
- cached raw summaries for paper-facing claims;
- source manifests with date, query, row count, schema version, and stable file hashes;
- deterministic scripts for transformations;
- checks for missing required columns;
- clear separation of fixture data from empirical data;
- no API keys in repository.

Suggested targets:

```make
empirical-data-inventory
empirical-refresh-optional
empirical-summarize-offline
empirical-linkage-report
empirical-linkage-roadmap
empirical-boundary-report
empirical-heldout-check
```

## Quality Gates

Before this can become a data/resource paper:

- all 12 configured raw inputs have usable raw or cached summary inputs;
- public support advances beyond the one historical related-issue pilot to exact or closer contemporaneous questions, validated geography, design-based uncertainty or MRP where needed, and bill-text-specific affected-population evidence, and campaign finance is linked beyond the current bounded concentration, issue-sector, member, district-context, sponsored-bill, local no-exact-match, target-scope, cached bill-action, and source-acquisition queue layers;
- the linkage report shows bill/topic/statute or actor joins for the high-priority public-opinion, finance, implementation, and statutory-lineage areas;
- implementation, law-revision, and comparative-institution proxy data are present, with bounded comparative scenario-family metadata anchors added and full lineage, observed productivity, and institutional-fit data still documented as future work;
- source registry documents licensing/access;
- held-out validation design exists;
- all paper-facing results regenerate offline.
