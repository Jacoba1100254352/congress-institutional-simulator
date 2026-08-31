# Output Schema

This document describes the main generated output families. It is a software
guide, not a claim that any output validates real legislative behavior.

## Report Locations

| Location | Produced by | Contents |
|---|---|---|
| `reports/simulation-*.csv` | Java campaign targets | Scenario-by-case simulation results. |
| `reports/simulation-*.md` | Java campaign targets | Human-readable campaign summaries. |
| `reports/*-manifest.json` | Java campaign targets or paper scripts | Provenance and freshness metadata. |
| `reports/calibration-baseline.*` | `make calibration-check` | Conventional-baseline flow screens. |
| `reports/empirical-*.csv` and `.md` | `scripts/validation/` | Readiness, empirical summaries, bridge, inventory, linkage, and held-out benchmark reports. |
| `paper/figures/*.tex` | `paper/scripts/generate_figures.py` and reporting scripts | LaTeX tables and figures consumed by the paper. |
| `paper/acm-ci-framework/acm-ci-framework.pdf` | `make paper` or `make paper-checks` | Main manuscript PDF. |
| `paper/technical-appendix/odd-d-appendix.pdf` | `make paper` or `make paper-checks` | Technical appendix PDF. |
| `paper/pdf-manifest.json` | `paper/scripts/write_pdf_manifest.py` | Stable PDF extracted-text hashes and metadata. |

## Campaign CSV Shape

Campaign CSVs such as `reports/simulation-campaign-v21-paper.csv` use one row
per scenario/case summary.

Core identity columns:

- `caseKey`
- `caseName`
- `caseDescription`
- `caseWeight`
- `scenarioKey`
- `scenario`

Core scale columns:

- `totalBills`
- `potentialBillsPerRun`
- `enactedBills`
- `enactedPerRun`
- `floorPerRun`

Main score columns:

- `directionalScore`
- `representativeQuality`
- `riskControl`
- `administrativeFeasibility`
- `productivity`
- `floor`
- `avgSupport`
- `welfare`
- `cooperation`
- `compromise`
- `gridlock`

Diagnostic and supplemental columns then follow. These include agenda access,
committee, lobbying, chamber, court, public-input, campaign-finance-like,
implementation, law-registry, and strategy-learning metrics. The authoritative
metric names and directions are maintained in `MetricDefinition`; many
additional columns are sourced from `ScenarioReport.SUPPLEMENTAL_METRIC_KEYS`.

## Empirical Boundary Outputs

The current validation pipeline writes:

- `reports/empirical-validation-readiness.csv`: raw input presence and required
  columns.
- `reports/empirical-validation-summary.csv`: computed summaries for available
  raw inputs.
- `reports/empirical-bridge.csv`: mapping from empirical summaries to simulator
  flow-check proxies.
- `reports/empirical-flow-heldout.csv`: deterministic held-out benchmarks for
  bill progression, Voteview roll-call behavior, sponsor proposal-access
  concentration, OpenFEC campaign-finance concentration, CES district-opinion
  proxies, SCDB court review, Federal Register implementation delay,
  Congress.gov law-revision text, and comparative-institution context.
- `reports/govinfo-bill-census-116.csv`: complete 116th-Congress H.R./S.
  lifecycle summary used only as an external no-refit temporal cohort.
- `reports/govinfo-bill-census.csv`: complete 117th-Congress H.R./S. lifecycle
  summary used for threshold selection and within-Congress stability checks.
- `reports/govinfo-bill-census-118.csv`: complete 118th-Congress H.R./S.
  lifecycle summary used only as an external no-refit temporal cohort.
- `reports/legislative-lifecycle-calibration.csv`: fixed threshold grid and
  selected 117th-Congress calibration result.
- `reports/legislative-lifecycle-temporal-replication.csv`: no-refit transport
  errors against the complete 116th and 118th censuses, including Wilson
  intervals, prespecified tolerances, and pass/fail status. The current result
  passes five of six cohort-metric tolerances and retains the 118th-Congress
  enactment miss.
- `data/validation/raw/govinfo_executive_action_panel.csv`: compact 108th-118th-
  Congress panel retaining 4,021 presented H.R./S. measures from 126,760 parsed
  GovInfo records, with presidential outcomes, party context, source/action
  hashes, and classifier integrity fields.
- `reports/legislative-executive-action-diagnostic.csv`: empirical presentment,
  veto, override, and enactment counts by Congress, administration, government
  control, and sponsor-party relation, plus pooled empirical and frozen
  simulator rows with conditional-rate intervals and a descriptive
  mechanism-boundary comparison. Party strata are not causal estimates.
- `reports/empirical-data-inventory.csv`: source-family inventory joined from
  the registry and current reports.
- `reports/empirical-linkage-report.csv`: explicit raw-data join coverage by
  source family, separating source coverage from linked bill/topic/statute or
  actor evidence. Metadata-only joins, such as FEC recipient IDs to public
  candidate/committee records, are reported separately from fully linked
  validation evidence.
- `reports/empirical-linkage-roadmap.csv`: source-family linkage upgrade gates
  for families that are not yet fully linked.
- `reports/govinfo-billstatus-linkage.csv`: bounded govinfo BILLSTATUS
  cross-check for cached Congress.gov bill-progression rows. It is not a full
  bill census, implementation, court, public-opinion, welfare, or model
  validation dataset.
- `reports/sponsor-bill-linkage.csv`: bounded sponsor aggregate to public
  bill-metadata linkage by Bioguide sponsor ID. It is not full Center for
  Effective Lawmaking data, a complete sponsor history, legislative-quality,
  welfare, causal-effect, or model validation evidence.
- `reports/comparative-institution-linkage.csv`: bounded QoG/OWID/V-Dem
  country-profile to simulator scenario-family metadata bridge. It is not
  observed law-output productivity, bicameral-disagreement evidence,
  country-level institutional fit, adoption, welfare, causal-effect, or model
  validation evidence.
- `reports/court-law-linkage.csv`: bounded SCDB merits-case U.S.C.-section to
  Federal Register authority-citation overlap for cached public-law rows. It is
  not direct case-to-public-law review, invalidation, lower-court,
  emergency-order, welfare, or model validation evidence.
- `reports/voteview-member-context.csv`: bounded Voteview member-context
  inventory showing which cached roll-call member-vote rows carry Bioguide,
  party, state/district, and ideal-point metadata. It is not bill-level
  roll-call validation.
- `reports/voteview-bill-linkage.csv`: bounded Voteview roll-call bill-number
  crosswalk showing which cached roll-call IDs carry parsed bill IDs and which
  overlap the cached Congress.gov bill-progression sample. It is not complete
  roll-call-to-bill coverage or public-opinion validation.
- `reports/lobbying-issue-linkage.csv`: bounded Senate LDA issue-label to
  Congress.gov policy-area topic bridge showing which cached lobbying rows carry
  broad issue context. It is not bill-level lobbying influence, sponsor,
  committee, or capture validation.
- `reports/lobbying-bill-policy-context.csv`: bounded Senate LDA issue-label to
  cached govinfo bill/action context by shared Congress.gov policy area. It
  exposes issue-policy bill contexts only; it is not client-to-specific-bill
  lobbying influence, sponsor targeting, committee-action influence, roll-call
  influence, legislative-outcome causality, public benefit, or capture
  validation.
- `reports/lobbying-bill-manual-disposition-review.csv`: source-reviewed
  manual disposition/target classifications for the high-priority LDA
  disposition queue. It confirms activity-text support or bill-reference-only
  context only; it is not lobbying-contact, committee-action, roll-call,
  outcome-causality, public-benefit, capture, or model-validation evidence.
- `reports/lobbying-bill-medium-disposition-packets.csv`: grouped
  medium-priority LDA disposition-review packets. It is review infrastructure
  for follow-up source review, not manual disposition confirmation, lobbying
  contact, targeting, committee-action, roll-call, outcome-causality, capture,
  or model-validation evidence.
- `reports/lobbying-bill-medium-directional-packet-review.csv`: source-reviewed
  medium-priority LDA support/opposition packet dispositions. It confirms or
  narrows activity-text directions only; it is not lobbying-contact, targeting,
  committee-action, roll-call, outcome-causality, capture, welfare, or
  model-validation evidence.
- `reports/lobbying-bill-medium-position-activity-packet-review.csv`:
  source-reviewed medium-priority LDA position/activity packet dispositions. It
  classifies activity-text dispositions without explicit support/opposition
  direction and records one opposition cue found in that queue; it is not
  lobbying-contact, targeting, committee-action, roll-call, outcome-causality,
  capture, welfare, or model-validation evidence.
- `reports/rulemaking-authority-linkage.csv`: bounded Federal Register
  public-law authority-search bridge showing which cached public-law rows have
  text-verified rule documents that cite the public law. It is not exhaustive
  implementation coverage, proposed-rule history, enforcement, court-review,
  welfare, or model validation.
- `reports/rulemaking-history-linkage.csv`: bounded Federal Register
  proposed-to-final history bridge for authority-matched final-rule rows,
  retaining proposed-rule records only when RIN or docket identifiers match.
  It is not complete Regulations.gov comment coverage, Unified Agenda stage
  coverage, enforcement, appropriations, welfare, or model validation.
- `reports/rulemaking-comment-metadata.csv`: bounded Federal Register detail
  refetch for authority-matched final-rule chains, recording only Federal
  Register-exposed Regulations.gov docket IDs, comment URLs, comment counts, and
  comment-close dates. It is not complete comment-record, commenter-identity,
  comment-text, Unified Agenda, enforcement, appropriations, welfare, or model
  validation evidence.
- `reports/bill-law-evidence-spine.csv`: bounded public-law bill/action
  metadata spine showing which public-law rows currently carry revision-text
  proxy fields, sponsor-district public-opinion context, bounded
  sponsor-district bill policy-area context, same-policy campaign-finance
  sponsor context, same-policy LDA issue/bill context, Federal Register
  authority-search matches, bounded proposed-rule history matches, proposed-rule
  Regulations.gov docket/comment-portal metadata, Federal Register-exposed
  comment metadata, final-rule timing metadata,
  proposed-to-final timing metadata, bounded court U.S.C.-section overlaps, and
  remaining missing joins. It is a join inventory, not bill-specific finance or
  lobbying evidence, causal evidence, or validation evidence.
- `reports/bill-law-lifecycle-readiness.csv`: generated review queue ranking
  the bill-law spine rows by direct metadata, context-only metadata, unresolved
  high-priority lifecycle gates, next upgrade gate, next source family/command,
  and copied source pointers such as authority documents, proposed-rule dockets,
  comment portals, court case IDs, U.S.C. sections, and context bill IDs. It is
  not validation evidence and does not add new direct source joins.
- `reports/bill-law-lifecycle-next-actions.csv`: post-disposition action queue
  that consumes `reports/court-public-law-direct-review.csv`, closes
  direct-review gates when queued court/public-law overlaps are temporally
  excluded or source-reviewed not direct, and selects the next actionable
  lifecycle gate. It is not validation evidence and does not create new
  statutory-lineage, implementation-outcome, finance/lobbying, public-support,
  or direct court-review evidence beyond the reviewed disposition.
- `reports/bill-finance-lobbying-review-queue.csv`: generated queue for
  public-law rows whose next actionable lifecycle gate is bill-specific
  campaign-finance or lobbying evidence. It carries same-policy FEC/LDA context
  and exact-match flags for review, but it is not bill-targeting, influence,
  capture, outcome, welfare, or validation evidence.
- `reports/bill-finance-lobbying-local-context-review.csv`: curated/generated
  local-context review over that queue. It records that 4 same-policy
  campaign-finance rows and 9 same-policy LDA issue/bill rows lack current-bill
  exact matches in the current local context, leaves all 10 rows for external
  target/source expansion, and is not absence-of-spending, influence, outcome,
  welfare, capture, or validation evidence.
- `reports/bill-finance-lobbying-external-search-review.csv`: generated
  external-search review over the same 10-row queue. It summarizes the targeted
  official LDA current-bill search cache, records exact activity-text
  current-bill mentions for 2 queued bills, keeps 8 rows at complete no-exact
  LDA search status, and marks 4 campaign-finance rows for FEC/OpenFEC
  candidate, committee, or outside-spending target-scope review. It is not
  lobbying-contact, support/opposition, campaign-finance influence, outcome,
  welfare, capture, or validation evidence.
- `reports/bill-finance-lobbying-external-lda-mention-review.csv`:
  source-reviewed packet classification for exact external LDA current-bill
  mention rows. It groups 55 exact activity-text mention rows into 19 filing
  packets, classifies 16 current-bill issue-reference packets and 3
  current-bill issue-advocacy packets without explicit support/opposition text,
  and records no named sponsor/member/committee target, committee-action
  influence, roll-call influence, or legislative-outcome causality evidence. It
  is bounded activity-text disposition evidence only.
- `reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv`:
  source-reviewed public FEC/OpenFEC target-scope classification for the 4
  queued campaign-finance public-law rows. It covers 5 candidate/recipient
  context attachments, 5 transaction attachments, 2 unique public FEC candidate
  recipients, and 2 unique raw OpenFEC transactions, while recording 0
  current-bill ID matches, 0 reviewed bill sponsor/candidate overlaps, 0
  committee-of-jurisdiction or committee-action links, and 0 legislative-outcome
  or influence links.
- `reports/statutory-lineage-review-queue.csv`: source-review queue for rows
  whose next actionable lifecycle gate is `codified_usc_lineage`. It carries
  public-law, law-revision, authority-document, U.S.C.-citation, proposed-rule,
  docket, and court-overlap pointers from upstream reports, but it is not
  statutory-lineage evidence and does not establish target sections, text diffs,
  implementation outcomes, court review, welfare, or model validation.
- `reports/statutory-lineage-source-scan.csv`: official GovInfo public-law text
  scan for the statutory-lineage review queue. It records public-law text
  source URLs, source hashes, U.S.C.-reference counts, amendment/repeal/
  redesignation counts, and compact target-section candidate snippets. It is
  not codified-lineage evidence and does not establish OLRC classification,
  target-section text diffs, implementation outcomes, court review, welfare, or
  model validation.
- `reports/statutory-lineage-target-section-triage.csv`: normalized target
  reference triage derived from the statutory-lineage source scan. It ranks
  candidate U.S.C. references for manual OLRC and codified-text review while
  preserving missing-link markers for OLRC classification, codified lineage,
  target-section diffs, effective text, and model validation. It is not
  codified-lineage evidence and does not establish text diffs, implementation
  outcomes, court review, welfare, or model validation.
- `reports/statutory-lineage-olrc-current-scan.csv`: official OLRC current
  U.S. Code page availability scan for target-section triage rows. It records
  section-page URLs, source hashes, byte counts, current-page public-law
  mentions, and non-fetched reasons for title-only, incomplete, or missing
  target rows. It is not historical codified-lineage evidence and does not
  establish before/after text diffs, implementation outcomes, court review,
  welfare, or model validation.
- `reports/statutory-lineage-olrc-historical-scan.csv`: official OLRC annual
  U.S. Code page availability scan for current-page candidates whose current
  page mentions the queued public law. It records year-before-enactment and
  enactment-year URLs, hashes, byte counts, and public-law mention windows. It
  is not codified-lineage evidence, public-law causation, before/after text
  diffs, implementation outcomes, court review, welfare, or model validation.
- `reports/statutory-lineage-olrc-annual-text-diff.csv`: bounded annual OLRC
  text-diff cue scan for the historical-scan rows. It records refetched annual
  page hashes, normalized section-text hashes, bounded first-change windows,
  post-edition public-law context snippets, and manual-review priorities. It is
  not source-reviewed codified-lineage evidence, public-law causation,
  adjudicated target-section text diffs, implementation outcomes, court review,
  welfare, or model validation.
- `reports/statutory-lineage-adjudication.csv`: conservative classification of
  annual OLRC cue rows into official post-only public-law marker evidence. It
  records marker status, marker strength, and remaining target-section diff
  review gaps. It is not a source-reviewed target-section text diff,
  public-law causal attribution, effective statutory text, implementation
  outcome, court review, welfare, or model validation.
- `reports/statutory-lineage-target-review-packets.csv`: reviewer packet layer
  for annual OLRC marker rows. It records pre/post annual U.S. Code URLs,
  source hashes, normalized section-text signatures, first-change windows,
  public-law context snippets, packet readiness, and downstream target-section
  diff-review disposition annotations where curated review rows exist. It is
  review infrastructure plus disposition context, not public-law causation,
  effective statutory text, implementation, court, welfare, or model-validation
  evidence.
- `reports/statutory-lineage-target-section-diff-review.csv`: bounded
  source-reviewed pilot for official GovInfo/OLRC target-section diff
  dispositions. It records review status, source-reviewed diff flags,
  codified-lineage relationship labels, source URLs, and source-review notes
  for Public Laws 117-146, 117-166, 117-167, 117-168, 117-169, 117-174,
  117-180, 117-203, 117-219, 117-223, 117-229, 117-263, and 117-297 target
  packets. It is not public-law causal
  attribution, effective statutory text, implementation outcome, court review,
  welfare, causal-effect, or model-validation evidence.
- `reports/statutory-lineage-target-lifecycle-bridge.csv`: target-section
  lifecycle bridge from reviewed target-section diff rows to bounded
  public-law-level implementation authority, rulemaking history, Federal
  Register-exposed comment metadata, SCDB U.S.C.-section overlap,
  court/public-law direct-review disposition, and bill-law spine context. Base
  U.S.C. section overlaps are metadata context and are separated from stricter
  exact target-reference/subsection flags; public-law-level rows are context
  only. It is not implementation-outcome, direct target-section court-review,
  effective-text, causal, welfare, or model-validation evidence.
- `reports/statutory-lineage-no-target-review.csv`: curated source-reviewed
  no-target dispositions for designation laws whose official GovInfo
  public-law text and OLRC public-law PDFs expose no U.S.C. references,
  amendment/repeal/redesignation cues, or target-section candidates. It closes
  the no-target classification gate for those designation laws only; it is not
  target-section text-diff, implementation-outcome, court-review, welfare,
  causal-effect, or model-validation evidence.
- `reports/statutory-lineage-codified-progress.csv`: progress classifier for
  the current codified-lineage slice. It keeps source-reviewed target-section
  diff rows and reviewed designation-law no-structured-U.S.C.-target
  dispositions visible while preserving the remaining full-lineage,
  effective-text, implementation, court-review, welfare, and model-validation
  gaps.
- `reports/court-public-law-review-queue.csv`: generated case/public-law
  review queue for rows where bounded SCDB U.S.C.-section metadata overlaps
  Federal Register authority citations attached to cached public-law rows. It
  is not direct court-review, invalidation, emergency-order, lower-court,
  welfare, causal-effect, or model validation evidence.
- `reports/court-public-law-temporal-triage.csv`: date-screened derivative of
  the court/public-law review queue comparing SCDB decision dates to cached
  public-law enacted dates. It can rule out direct review of listed public laws
  that postdate the case, but it does not prove direct review for
  post-enactment rows or resolve codified statutory lineage.
- `reports/court-public-law-direct-review.csv`: source-reviewed disposition
  table for post-enactment court/public-law review tasks, plus generated
  temporal exclusions for pre-enactment rows. It distinguishes direct public-law
  review from reviewed not-direct shared-section overlaps, but it is not
  lower-court, emergency-order, implementation-outcome, causal-invalidation,
  welfare, or model validation evidence.
- `reports/district-public-opinion-policy-context.csv`: bounded
  sponsor-district public-law policy-context inventory showing which CES
  district public-opinion proxy rows can be attached to public-law bill metadata
  and local topic-throughput policy areas. It is not bill-topic public-support,
  MRP, affected-group harm, representative-responsiveness, or public-benefit
  validation.
- `reports/district-public-opinion-bill-item-alignment-review.csv`:
  source-reviewed disposition ledger for the 22 official bill packets and CES
  candidate items. Positive rows are historical related-issue alignments, and
  negative rows prevent broad policy-area similarity from being treated as a
  bill-text match.
- `reports/district-public-opinion-bill-topic-support.csv`:
  privacy-thresholded annual direct-weighted district aggregates linked only to
  retained alignment rows, with separate Dataverse catalog checksums and
  access-stream byte-count/SHA-256 pins. Annual question field, wave, guide,
  validated-voter weight selection, and cumulative-to-original response-match
  fields make the weighting path auditable. The current rows are historical
  related-issue context, not exact or contemporaneous bill support, MRP,
  design-based uncertainty, affected-group evidence, causal representation, or
  model validation.
- `reports/campaign-finance-district-context.csv`: bounded OpenFEC
  candidate-recipient district-context inventory showing which public FEC
  recipient rows can be joined to CES district public-opinion context. It is not
  bill-level influence or capture validation.
- `reports/campaign-finance-member-context.csv`: bounded OpenFEC
  candidate-recipient member-context inventory showing which public FEC
  candidate rows can be joined to Voteview/Bioguide member metadata by
  conservative name, chamber, state, and district evidence. It is not bill,
  committee, issue, or influence validation.
- `reports/campaign-finance-issue-context.csv`: bounded OpenFEC transaction-label
  issue-context inventory showing which public occupation, employer, or
  expenditure-purpose labels can be mapped to broad local policy-area topics. It
  is not bill-level influence, committee jurisdiction, legislative outcome,
  private-contributor, or capture validation.
- `reports/campaign-finance-sponsor-bill-context.csv`: bounded OpenFEC
  candidate/member-to-sponsored-bill context inventory showing which matched
  public FEC candidate rows can be joined by Bioguide ID to cached govinfo bill
  metadata. It is not campaign-finance influence, committee-action influence,
  legislative-outcome causality, private-contributor disclosure, public benefit,
  or capture validation.
- `reports/validation-boundary-matrix.csv`: claim-boundary category by source
  family.
- `reports/empirical-validation-gap-report.csv`: paper-facing source-family
  readiness and gap report.
- `reports/raw-source-manifest.csv`: offline source-family manifest with raw
  file row counts, metadata-note paths, source hashes, transformation scripts,
  and claim boundaries.

`make empirical-boundary-check` verifies that the registry, held-out report,
inventory, linkage report, linkage roadmap, govinfo BILLSTATUS report, Voteview
member-context report, Voteview bill-linkage report, lobbying issue-linkage
report, lobbying bill-policy context report, lobbying bill manual-disposition
review, lobbying bill medium-disposition packets, lobbying bill medium-directional
packet review, lobbying bill medium-position/activity packet review, rulemaking authority-linkage
report, rulemaking history-linkage report, rulemaking comment-metadata report,
bill-law spine, bill-law lifecycle readiness report, bill-law lifecycle next-action report, statutory-lineage
review queue, statutory-lineage source scan, statutory-lineage target-section
triage, statutory-lineage OLRC current scan, statutory-lineage OLRC historical
scan, statutory-lineage OLRC annual text-diff cue scan, statutory-lineage
adjudication report, statutory-lineage target review packet report,
statutory-lineage target lifecycle bridge,
court/public-law review
queue, court/public-law temporal triage report,
court/public-law direct-review disposition report, campaign-finance
district-context, campaign-finance member-context report, campaign-finance
issue-context report, campaign-finance sponsor-bill context report, district
public-opinion policy-context report, bill-item alignment review, historical
bill-topic support report, gap report, and paper table agree on
source-family boundaries, held-out counts, linkage statuses, roadmap coverage,
and raw row counts.

Boundary categories are:

- `held-out benchmark`
- `flow sanity check`
- `calibration proxy`
- `not validated`

## Stability Expectations

Fixed-seed CSV outputs should be stable for a given code version, Java version,
and command. PDF bytes can vary across TeX/font environments, so the paper
workflow checks stable extracted-text and manifest metadata rather than relying
on raw PDF byte equality.
