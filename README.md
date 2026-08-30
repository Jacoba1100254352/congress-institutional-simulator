# Reproducing the ACM CI Framework Paper

This repository contains the Congress Institutional Simulator, a Java 21
comparative institutional-design simulator, plus the ACM Collective
Intelligence framework manuscript and ODD+D appendix generated from it.

The submitted paper is a framework and stress-test artifact. It compares
selected legislative mechanism bundles under shared synthetic worlds and reports
diagnostics for productivity, revision moderation, generated public support,
risk, administrative cost, and generated public benefit. The results are
synthetic design hypotheses, not empirical rankings of real legislatures.

## Requirements

- Java 21 on `PATH`
- GNU Make
- Python 3 for report and figure-generation scripts
- LaTeX with `latexmk` for rebuilding the PDFs

On macOS, set Java 21 explicitly when needed:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```

The paper workspace vendors the ACM class files used by the review build. With a
minimal TeX Live Basic install, see [paper/README.md](paper/README.md) for the
extra LaTeX packages that may be needed.

## Citation, Release, and License Status

Pre-release citation metadata is available in `CITATION.cff`, and software
metadata is available in `codemeta.json`. `RELEASE.md` records the remaining
release checklist.

This repository is not yet a public archived release. No root `LICENSE` file has
been chosen yet, so do not treat the software as open-source reusable until a
license is added.

## Quick Smoke Test

```sh
make test
```

Expected runtime: under one minute on the authoring workstation.

Expected result: Java sources compile and the simulator test suite passes.

## Full Offline Reproduction

```sh
make reproduce-paper-offline
```

Expected runtime: several minutes on the authoring workstation.

This no-network target regenerates:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/simulation-campaign-v21-paper-manifest.json`
- generated diagnostic reports under `reports/`
- `reports/voteview-member-context.csv`
- `reports/voteview-bill-linkage.csv`
- `reports/lobbying-issue-linkage.csv`
- `reports/lobbying-bill-policy-context.csv`
- `reports/lobbying-bill-mention-review.csv`
- `reports/lobbying-bill-action-context.csv`
- `reports/lobbying-bill-text-review.csv`
- `reports/lobbying-bill-disposition-review.csv`
- `reports/govinfo-billstatus-linkage.csv`
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
- `reports/bill-finance-lobbying-source-acquisition-queue.csv`
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
- `reports/campaign-finance-district-context.csv`
- `reports/campaign-finance-member-context.csv`
- `reports/campaign-finance-issue-context.csv`
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
- `reports/district-public-opinion-ces-policy-item-codebook-direction-review.csv`
- `reports/district-public-opinion-ces-source-freshness.csv`
- generated LaTeX tables and figures under `paper/figures/`
- `paper/acm-ci-framework/acm-ci-framework.pdf`
- `paper/technical-appendix/odd-d-appendix.pdf`
- `paper/pdf-manifest.json`

The workflow uses fixed seeds. Reproduced CSV values and PDF extracted-text
hashes should match `paper/pdf-manifest.json` within the tracked manifest
checks.

## Paper Checks

Before treating paper-facing output as ready, run:

```sh
make paper-checks
```

This runs the paper workflow plus word-count, anonymity, figure-label,
table/figure-consistency, empirical-boundary, linkage, and linkage-roadmap
consistency, PDF-render, and PDF-manifest checks.

GitHub Actions uses:

```sh
make github-ci
```

Local full CI uses:

```sh
make ci
```

## Optional Network-Dependent Inputs

The offline reproduction path does not require API keys or live network access.
Optional empirical sample rebuilds are separate:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-govinfo-billstatus-linkage-raw
make build-core-raw-validation
make build-sponsor-bill-linkage-raw
make build-voteview-member-context-raw
make build-voteview-bill-linkage-raw
make build-lobbying-issue-linkage-raw
make build-lobbying-bill-mentions-raw
make build-campaign-finance-raw
make build-campaign-finance-linkage-raw
make build-campaign-finance-member-context-raw
make build-campaign-finance-issue-context-raw
make build-district-public-opinion-raw
make build-district-public-opinion-linkage-raw
make build-district-public-opinion-policy-context-raw
make build-district-public-opinion-census-denominators-raw
make build-district-public-opinion-acs-context-raw
make build-district-public-opinion-ces-policy-item-candidates-raw
make build-district-public-opinion-ces-policy-item-response-distributions-raw
make build-district-public-opinion-ces-policy-item-codebook-direction-raw
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
make build-statutory-lineage-source-scan-raw
make build-statutory-lineage-olrc-current-scan-raw
make build-statutory-lineage-olrc-historical-scan-raw
make build-statutory-lineage-olrc-annual-text-diff-raw
make build-statutory-lineage-adjudication-raw
make build-statutory-lineage-target-review-packets-raw
make build-comparative-institutions-raw
make build-comparative-institution-linkage-raw
```

For credential-backed source refreshes, copy `.env.example` to `.env` and add
local values there. The `.env` file is ignored by Git; the tracked template
contains only blank placeholders for `CONGRESS_API_KEY`, `OPENFEC_API_KEY`, and
`REGULATIONS_GOV_API_KEY`.

Some optional rebuilds may require public data access, API credentials, or
optional Python packages. The govinfo BILLSTATUS linkage builder uses public
bulk XML records to cross-check the cached Congress.gov bill-progression
sample by congress, bill type, and bill number; it does not create a full bill
census, public-opinion, implementation, court, welfare, or model-validation
dataset. The sponsor-bill linkage builder joins the bounded sponsor aggregate to
public govinfo/Congress.gov bill metadata by Bioguide ID only; it does not
create full Center for Effective Lawmaking, complete sponsor-history,
legislative-quality, or model-validation evidence. The campaign-finance
linkage builder uses public FEC bulk files to map cached recipient IDs to
committee/candidate metadata only; it does not create bill, sponsor, issue, or
causal influence evidence. The
campaign-finance member-context builder joins cached FEC candidate metadata to
cached Voteview member metadata only when candidate name, chamber, state, and
district evidence agree; it does not infer identity from district alone and
does not create bill-level influence, committee, issue, or causal capture
evidence. The campaign-finance issue-context builder maps high-confidence
transaction occupation, employer, or expenditure-purpose labels to broad local
policy-area topics only; it does not create bill, committee, legislative
outcome, private-contributor, causal-capture, or model-validation evidence. The
campaign-finance sponsor-bill context report joins the bounded matched-candidate
member subset to cached govinfo sponsored-bill metadata by Bioguide ID only; it
does not show that campaign finance funded, targeted, influenced, or benefited
any bill, committee action, public law, implementation outcome, or model result. The
Voteview member-context builder uses Voteview static member CSVs to map cached
roll-call rows to public member metadata only; it does not create
roll-call-to-bill, public-law, district-opinion, public-support, or model
validation evidence. The Voteview bill-linkage builder uses Voteview static
roll-call metadata to parse bill numbers for sampled roll calls and flag
bounded overlap with the cached Congress.gov bill sample only; it does not
create complete roll-call-to-bill, public-opinion, public-law, outcome, or model
validation evidence. The lobbying issue-linkage builder maps cached Senate LDA
issue labels to broad local Congress.gov policy-area topic labels for 144 / 146
LDA activity rows. The lobbying bill-policy context report then maps those
issue labels to cached govinfo bill/action metadata by shared policy area for
308 issue-policy bill contexts across 144 unique cached bills and 3 unique
enacted cached bills. The LDA bill-mention builder searches official LDA filing
activity text for exact current-bill identifiers in the public-law candidate
set and currently records 484 exact activity-text bill mention rows across 26
cached public-law bill IDs from 40 searched public-law rows. The lobbying
bill-action context report then joins those 26 exact-mentioned public-law bill
IDs to cached Congress.gov bill/action metadata, including sponsor metadata for
26, committee-reported flags for 21, floor-considered flags for 26, and enacted
public-law outcome metadata for 26.
The stored activity-text review locates all 484 bill references and the
disposition/target review queue prioritizes 156 rows for manual review,
including 4 high-priority rows and 152 medium-priority rows. These joins,
exact filing-text identifiers, deterministic text signals, and review queues do
not create lobbying influence, manual disposition confirmation, sponsor-target,
committee-action, roll-call, legislative-outcome causality, causal capture, or
model-validation evidence. The
court-law linkage builder parses SCDB `lawMinor` U.S.C. sections and overlaps
them with Federal Register authority U.S.C. citations attached to cached
public-law rows; it does not create direct case-to-public-law review,
invalidation, lower-court, emergency-order, or model validation evidence. The
rulemaking implementation linkage builder uses the Federal Register
single-document endpoint to map cached final-rule rows to document, docket, RIN,
CFR, agency, and Federal Register-exposed Regulations.gov metadata only; it does
not create public-law, proposed-rule, enforcement, appropriations, or complete
comment-record evidence. The rulemaking authority-linkage builder uses Federal
Register search and full-text records to text-verify bounded public-law
authority mentions for the cached public-law sample; it does not create
exhaustive implementation, proposed-rule, enforcement, appropriations,
complete-comment, court-review, welfare, or model-validation evidence. The
rulemaking history-linkage builder uses Federal Register search and
single-document records to link authority-matched final rules to proposed-rule
metadata only when RIN or docket identifiers match; it does not create complete
comment records, Unified Agenda stage coverage, enforcement, appropriations,
welfare, or model-validation evidence. The rulemaking comment-metadata builder
refetches Federal Register detail records for those authority-matched final
rules and matched proposed rules and records only Federal Register-exposed
Regulations.gov docket, comment URL, comment-count, and comment-close metadata;
it does not create complete comment-record, commenter-identity, comment-text,
Unified Agenda, enforcement, appropriations, welfare, or model-validation
evidence. The rulemaking comment-record builder starts from those docket/count
metadata rows and retrieves bounded Regulations.gov public comment-record
metadata when configured thresholds and API availability allow, preserving
partial retrieved metadata separately from complete rows, or records
no-comment/high-volume/unknown-count statuses; it does not create comment-text,
attachment, commenter-identity,
Unified Agenda, enforcement, appropriations, welfare, or model-validation
evidence. The rulemaking comment-text review builder prioritizes complete
comment-record rows and then adds bounded partial-docket sample rows with
retrieved comment IDs. It fetches bounded public Regulations.gov comment
details, but stores only text availability, normalized text hashes, lengths,
attachment counts, source record status, and coarse cue flags while omitting the
full comment body and submitter/contact fields. Partial sample rows do not prove
complete docket coverage; this is not a full comment-text corpus, sentiment,
commenter-identity, implementation-outcome, welfare, or model-validation
evidence. The
law-revision bill-linkage builder uses Congress.gov bill-detail and bill-action
endpoints to map bounded public-law rows to bill/action metadata only; it does
not create codified statutory-lineage, implementation outcomes, or direct
court-review evidence.
The district public-opinion builder uses the Cumulative CES Common Content
Feather file and therefore requires `pyarrow`. The district public-opinion
linkage builder uses the Congress.gov member endpoint and public-law
bill/action metadata to link some CES district rows to House-sponsored
public-law bills by sponsor district only. The district public-opinion
policy-context builder adds bounded sponsor-district bill policy-area context
from local topic-throughput rows; it does not create bill-topic public-support,
MRP, affected-group-harm, representative-responsiveness, or public-benefit
evidence.
The district public-opinion CES policy-item candidate builder uses the official
Cumulative CES Policy Preferences metadata and tabular header to attach exact
source variable IDs to queued policy-area packets where broad candidates exist.
The candidate review remains item metadata only; it does not create acquired
bill-topic support estimates, MRP/small-area estimates, affected-group support,
or public-benefit evidence.
The district public-opinion CES policy-item response-distribution builder streams
the official Cumulative CES Policy Preferences tabular file and summarizes
unweighted raw response-code distributions for the candidate variables. The
distribution review is still not directionally recoded support/opposition,
bill-topic public support, district MRP/small-area evidence, affected-group
support or harm, public-benefit evidence, or model validation.
The district public-opinion CES policy-item codebook-direction builder parses
the official guide PDF and maps guide response labels or continuous endpoint
labels to observed candidate-variable response codes. The codebook-direction
review is survey-item wording direction only; it is still not bill-text-aligned
support/opposition, bill-topic public support, district MRP/small-area evidence,
affected-group support or harm, public-benefit evidence, or model validation.
The comparative-institutions builder uses QoG Data Finder selected CSV output
and OWID/V-Dem Grapher CSVs. The comparative-institution linkage builder maps
those bounded country-year profiles to simulator scenario-family metadata
anchors only; it does not create observed law-output, bicameral-disagreement,
institutional-fit, or model-validation evidence. These targets are useful for
refreshing empirical flow and boundary smoke tests, but they are not part of the
no-network artifact reproduction path.

The offline empirical reports also include `reports/govinfo-billstatus-linkage.*`,
which records the bounded govinfo BILLSTATUS cross-check for the cached
Congress.gov bill sample. `reports/sponsor-bill-linkage.*` records the bounded
sponsor aggregate to public bill-metadata join by Bioguide ID.
`reports/comparative-institution-linkage.*` records the bounded QoG/OWID/V-Dem
country-profile to simulator scenario-family metadata bridge.
`reports/court-law-linkage.*` records the bounded SCDB U.S.C.-section to
Federal Register authority-citation overlap for current
public-law rows. `reports/bill-law-evidence-spine.*` records the
bounded public-law bill/action metadata rows and which of those rows currently
carry revision-text proxy fields, sponsor-district public-opinion context,
bounded sponsor-district bill policy-area context,
same-policy campaign-finance sponsor context, same-policy LDA issue/bill
context,
bounded Federal Register authority-search/proposed-history matches, proposed-rule
Regulations.gov docket/comment-portal metadata, Federal Register-exposed
comment metadata, final-rule/proposed-to-final timing metadata, or bounded court
U.S.C.-section overlaps, plus official OLRC post-only public-law marker
adjudication and target-section review packets where present.
`reports/bill-law-lifecycle-readiness.*` ranks those spine rows by direct
metadata, context-only metadata, and remaining high-priority lifecycle upgrade
gates; it is a work queue, not validation evidence.
`reports/bill-law-lifecycle-next-actions.*` refines that queue after
court/public-law temporal and source-review dispositions, closing direct-review
tasks that are temporally excluded or reviewed not direct and moving those rows
to the next actionable lifecycle gate.
`reports/bill-law-lifecycle-corpus.*` assembles one bounded packet per
public-law row by joining the action queue to current public-opinion proxy
review, finance/lobbying source review, statutory-lineage progress,
implementation/comment-detail review, and court direct-review dispositions.
It is a row-by-row source-acquisition work surface, not validation evidence.
`reports/bill-finance-lobbying-review-queue.*` isolates the public-law rows
whose next actionable gate is bill-specific campaign-finance or lobbying
evidence. It preserves same-policy FEC/LDA context for source review, but is
not bill-targeting, influence, capture, outcome, welfare, or model-validation
evidence.
`reports/bill-finance-lobbying-local-context-review.*` source-reviews those 10
queued rows against the current local same-policy campaign-finance sponsor
context and LDA issue/bill context, confirming 4 same-policy finance rows and 9
same-policy lobbying rows have no current-bill exact match in that local
context. It leaves all 10 rows for external target/source expansion and is not
absence-of-spending, targeting, influence, outcome, welfare, capture, or
model-validation evidence.
`reports/bill-finance-lobbying-external-search-review.*` then searches those
queued bills against a targeted official LDA current-bill activity-text cache
using compact and dotted bill terms. It finds exact external LDA current-bill
mentions for 2 rows, with 55 exact activity-text mention rows across 19 filings
and 2 clients, while 8 rows have complete no-exact-match LDA search status. It
also marks 4 campaign-finance rows for public FEC/OpenFEC candidate, committee,
or outside-spending target-scope review; the FEC scope triage is not
bill-specific campaign-finance influence evidence.
`reports/bill-finance-lobbying-external-lda-mention-review.*` source-reviews
those 55 external LDA activity-text mention rows as 19 filing packets. It
classifies 16 current-bill issue-reference packets and 3 current-bill
issue-advocacy packets without explicit support/opposition text; all 19 packets
remain generic chamber or agency text references with no named sponsor/member/
committee target, committee-action influence, roll-call influence, or
legislative-outcome causality evidence.
`reports/bill-finance-lobbying-campaign-finance-target-scope-review.*`
source-reviews those 4 campaign-finance rows against the cached public
FEC/OpenFEC recipient, committee, independent-expenditure, member, district,
issue, and sponsored-bill context. It covers 5 candidate/recipient context
attachments, 5 transaction attachments, 2 unique public FEC candidate
recipients, and 2 unique raw OpenFEC transactions, while recording 0
current-bill ID matches, 0 reviewed bill sponsor/candidate overlaps, 0
committee-of-jurisdiction or committee-action links, and 0 legislative-outcome
or influence links.
`reports/bill-finance-lobbying-committee-action-context.*` joins the same 10
queued public-law rows to cached public bill-action metadata and the current
LDA/FEC review dispositions. It records 8 rows with cached committee-reported
flags and 10 rows with cached floor-considered flags, but no
committee-of-jurisdiction names, finance/lobbying committee-action influence
rows, roll-call influence rows, or legislative-outcome causality rows.
`reports/bill-finance-lobbying-committee-action-source-review.*` fetches
official govinfo BILLSTATUS source rows for those 10 bills, recording 9 rows
with committee names, 1 row source-reviewed without direct committee names, 9
rows with direct committee-action records, 1 row source-reviewed without direct
committee-action records, 10 rows with floor-action records, 8 rows with
BILLSTATUS roll-call references, and 10 rows with public-law outcome metadata.
This is official source context only, not finance/lobbying influence evidence.
`reports/bill-finance-lobbying-roll-call-source-review.*` joins those
BILLSTATUS roll-call references to the cached official House Clerk XML vote
source rows. It records 8 official House Clerk roll-call rows with matching
bill numbers and 3,435 represented member-vote rows, plus 2 reviewed floor
actions without numbered roll calls. This is floor-vote source coverage only,
not member-position influence, campaign/lobbying targeting, roll-call
influence, outcome causality, welfare, capture, or model validation evidence.
`reports/bill-finance-lobbying-member-vote-target-review.*` joins the 3,435
official House Clerk member-vote rows across 8 numbered roll calls to reviewed
public FEC/OpenFEC candidate/member context by Bioguide. It records 0 same-bill
reviewed campaign target Bioguide overlaps and 40 broad public FEC
member-context overlaps. This is member-vote target-scope context only, not
direct target-document, influence, outcome-causality, welfare, capture, or
model-validation evidence.
`reports/bill-finance-lobbying-source-acquisition-queue.*` ranks those 10 rows
for committee/no-direct-committee dispositions, direct member target documents,
independent target-source, and outcome-document follow-up. It records 9
official govinfo committee-name rows, 1 official no-direct-committee
source-reviewed row, 8 official House Clerk roll-call source rows, 8 official
member-vote target-scope review rows, 2 floor-action rows without numbered roll
calls, 0 rows still needing roll-call source acquisition, 0 rows still needing
committee-of-jurisdiction source follow-up, 2 LDA packet-priority rows, and 4
campaign target-scope priority rows. This is an acquisition queue only, not
finance/lobbying influence evidence.
`reports/statutory-lineage-review-queue.*` isolates the current
codified-lineage candidates from that action queue, preserving public-law,
authority, U.S.C.-citation, proposed-rule, docket, and court-overlap pointers
for official source review. It is a source-review queue, not statutory-lineage
evidence or model validation.
`reports/statutory-lineage-source-scan.*` scans official GovInfo public-law
text for those candidates and records compact U.S.C.-reference, amendment,
repeal, redesignation, and candidate-snippet counts. It is a source scan, not
codified U.S.C. lineage, target-section text diffs, implementation-outcome, or
model-validation evidence.
`reports/statutory-lineage-target-section-triage.*` normalizes candidate
U.S.C. target references from that source scan and ranks them for manual OLRC
and codified-text review. It is a target-section triage queue, not codified
lineage, target-section text diffs, implementation-outcome, or model-validation
evidence.
`reports/statutory-lineage-olrc-current-scan.*` fetches official OLRC current
U.S. Code pages for structured triage references and records source hashes plus
whether the current page mentions the queued public law. It is a current-source
availability scan, not historical codified lineage, before/after text diffs, or
model-validation evidence.
`reports/statutory-lineage-olrc-historical-scan.*` fetches official OLRC annual
U.S. Code pages for the year before enactment and the enactment year for
current-page candidates that mention the queued public law. It compares source
hashes and public-law mentions only; it is not codified lineage, public-law
causation, before/after text-diff, implementation-outcome, or model-validation
evidence.
`reports/statutory-lineage-olrc-annual-text-diff.*` refetches those annual
pages and records bounded post-edition public-law context snippets, raw-hash
comparison flags, normalized section-text signatures, and bounded first-change
windows. It is an automated cue queue for manual OLRC review, not
source-reviewed codified lineage, public-law causation, adjudicated
target-section text diffs, implementation-outcome, or model-validation evidence.
`reports/statutory-lineage-adjudication.*` classifies those annual cue rows
into official OLRC post-only public-law marker evidence. It is still not a
source-reviewed target-section text diff, public-law causal attribution,
effective statutory text, implementation-outcome, or model-validation evidence.
`reports/statutory-lineage-target-review-packets.*` packages those OLRC marker
rows with pre/post annual URLs, hashes, first-change windows, and post-edition
public-law context for manual target-section source review, and annotates rows
that now have downstream target-section diff-review dispositions. It is review
infrastructure plus disposition context, not public-law causal attribution,
effective statutory text, implementation-outcome, court-review, welfare, or
model-validation evidence.
`reports/statutory-lineage-target-section-diff-review.*` records a bounded
source-reviewed pilot for Public Laws 117-146, 117-166, 117-167, 117-168,
117-169, 117-174, 117-180, 117-203, 117-219, 117-223, 117-229, 117-263,
and 117-297 target-section diffs, with 75 reviewed dispositions, 73
source-reviewed target-section diff rows, and 2 reviewed related-section/no-
exact-target rows. It is not
exclusive public-law causal attribution, effective statutory text,
implementation-outcome, court-review, welfare, causal-effect, or
model-validation evidence.
`reports/statutory-lineage-target-lifecycle-bridge.*` attaches those reviewed
target-section diff rows to bounded public-law-level implementation, comment,
court-overlap, direct-review disposition, raw SCDB target-section citation
context, and bill-law spine context. It reports
19 authority base U.S.C. section overlaps, 13 exact authority target-reference
overlaps, 0 court base U.S.C. section overlaps, 0 exact court target-reference
overlaps, 2 raw SCDB target base-section overlap rows, 0 raw SCDB exact
target-reference rows, 0 post-enactment target base-section case attachments,
and 55 public-law-context-only rows. Base-section overlaps and raw SCDB section
citations are metadata context, not exact target-subsection evidence. It is a
target-section lifecycle bridge, not implementation-outcome, direct target-section
court-review, effective-text, causal, welfare, or model-validation evidence.
`reports/statutory-lineage-codified-progress.*` classifies the 15 current
codified-lineage candidates by progress status: 13 public laws have
source-reviewed target-section diff rows attached and 2 designation laws have
source-reviewed no-structured-U.S.C.-target dispositions. It is progress
tracking, not full codified-lineage evidence, target-section text-diff evidence
for designation laws, public-law causal attribution, effective statutory text,
implementation-outcome, or model-validation evidence.
`reports/statutory-lineage-effective-text-review.*` reviews the 73
source-reviewed target-section diff rows against official OLRC current U.S.
Code page metadata and current public-law note scans. All 73 rows have current
official source text and current public-law note presence, but 0 rows have
public-law causal-attribution review. It is effective-text source review, not
exclusive public-law causation, complete codified lineage, implementation,
court-review, welfare, or model-validation evidence.
`reports/statutory-lineage-public-law-attribution-review.*` then reviews the
same 73 source-reviewed target-section diff rows against official GovInfo
public-law text scans, official OLRC annual pre/post text-diff cues, and the
effective-text source review. All 73 rows receive bounded target-section
public-law attribution review, but the artifact is not complete codified
lineage, implementation, court-review, welfare, causal-effect, or
model-validation evidence.
`reports/statutory-lineage-completion-queue.*` ranks those 15 candidates for
the next completion pass: 13 positive target-diff public laws now have
law-revision effective-text and public-law attribution review rows, while 2
designation-law rows remain reviewed no-structured-target dispositions. The
remaining open gates are complete codified lineage, implementation/enforcement,
direct target-section court review, welfare/public-benefit evidence, and model
validation. It is a completion work queue, not full codified-lineage,
implementation, court-review, welfare, or model-validation evidence.
`reports/statutory-lineage-complete-lineage-expansion-queue.*` turns that open
complete-lineage gate into a ranked expansion surface. It joins the completion
queue to source-scan candidate counts, target triage, review packets,
source-reviewed diffs, effective-text review, and bounded public-law attribution
review, showing 12 active rows with candidate-expansion work, 1 active row
ready for final complete-lineage inventory audit, and 2 reviewed no-structured
target dispositions. It is a planning and coverage artifact, not complete
codified lineage, implementation, court-review, welfare, causal-effect, or
model-validation evidence.
`reports/statutory-lineage-target-packet-expansion-queue.*` expands the
triage-to-packet gap into 50 row-level target-review packet tasks: 50 direct
U.S.C. note-review tasks, 0 title-only manual-target tasks, and 0 incomplete
fragment review tasks. It is a packet-building queue, not codified-lineage,
target-section diff, effective-text, public-law attribution, implementation,
court-review, welfare, causal-effect, or model-validation evidence.
`reports/statutory-lineage-target-packet-source-gap-queue.*` classifies those
50 packet-expansion rows by source blocker: 50 fetched current OLRC pages
without a public-law marker, 0 fetched current OLRC pages with a public-law
marker but no downstream packet, 0 title-only references needing section
resolution, 0 incomplete or nonsection references needing manual resolution,
and 0 manual current-scan source-gap review rows. It is a source-gap queue, not codified-lineage, target-section
diff, effective-text, public-law attribution, implementation, court-review,
welfare, causal-effect, or model-validation evidence.
`reports/statutory-lineage-target-packet-source-gap-review.*` records 50 curated
official-source dispositions across 10 public laws for reviewed current-OLRC
no-marker blockers, including 17 temporary overrides, 17
appropriation-authority or program-authority references, 4 table or
preceding-section cues, and 12 cross-reference-only rows. It is a blocker
disposition review, not codified-lineage or target-section diff evidence.
`reports/statutory-lineage-target-reference-resolution-candidates.*` audits the
ambiguous target-reference blockers from that source-gap queue when any remain.
The current refreshed source-scan/triage path leaves 0 ambiguous rows, 0 bounded
concrete U.S.C. candidates requiring confirmation, and 0 rows without bounded
source-scan candidates. It is a target-reference candidate audit, not confirmed
target-section, codified-lineage, OLRC packet, diff, effective-text,
public-law attribution, implementation, court-review, welfare, causal-effect, or
model-validation evidence.
`reports/court-public-law-review-queue.*` expands bounded SCDB/Federal Register
U.S.C.-section overlaps into case/public-law review tasks. It is a direct-review
queue, not proof that a case challenged, interpreted, reviewed, or invalidated a
listed public law, bill, agency rule, or implementation chain.
`reports/court-public-law-temporal-triage.*` applies an enacted-date screen to
that queue, ruling out pre-enactment decisions as direct review of the listed
public law while leaving post-enactment rows for source review.
`reports/court-public-law-direct-review.*` records the source-reviewed
disposition for post-enactment court/public-law tasks and generated temporal
exclusions for pre-enactment rows; it is a direct-review audit rather than
lower-court, emergency-order, implementation-outcome, welfare, causal
invalidation, or model-validation evidence.
`reports/campaign-finance-district-context.*` records the bounded
House-candidate subset where public FEC recipient metadata can be joined to CES
district public-opinion context. `reports/campaign-finance-member-context.*`
records the bounded candidate subset where public FEC recipient metadata can be
joined to public Voteview member context. `reports/campaign-finance-issue-context.*`
records the bounded transaction-label subset that can be mapped to broad local
policy-area issue context. `reports/campaign-finance-sponsor-bill-context.*`
records the bounded matched-candidate subset that can be joined by Bioguide ID
to cached govinfo sponsored-bill metadata. `reports/district-public-opinion-policy-context.*`
records 66 sponsor-district public-law policy-context rows across 22 public-law
bills and 11 local policy areas. `reports/district-public-opinion-bill-topic-readiness.*`
queues those 22 public-law bills for issue-specific support, MRP/small-area,
and affected-group evidence review while recording 0 current issue-specific
support or affected-group support/harm rows. `reports/district-public-opinion-source-packets.*`
turns the same 22-bill queue into survey, MRP/small-area, and affected-population
source-acquisition packets across 11 policy areas, with 22 packets still carrying
no acquired external bill-topic dataset. `reports/district-public-opinion-census-denominators.*`
joins those 22 source packets to official Census TIGERweb 116th congressional-district
2020 population and housing-unit denominators across 21 sponsor districts; this
is a district-frame denominator only. `reports/district-public-opinion-acs-context.*`
joins the same 22 source packets to official ACS 2017-2021 broad district
demographic, economic, citizenship, language, disability, internet, and veteran
context across 21 sponsor districts. `reports/district-public-opinion-survey-source-crosswalk.*`
maps those same packets to official survey/source families and candidate
item-search terms while retaining no acquired item IDs or estimates.
`reports/district-public-opinion-survey-item-proxy-review.*` records the exact
current CES proxy variables attached to those 22 queued packets while still
retaining 0 acquired bill-topic survey item IDs or estimates. These
district-frame context, crosswalk, and proxy-variable review layers are not bill-text-specific
affected-population definitions, bill-topic support, MRP/small-area,
affected-group support/harm, public-benefit, or model-validation evidence.
`reports/district-public-opinion-ces-policy-item-candidate-review.*` joins the
same packets to the official Cumulative CES Policy Preferences item metadata,
mapping 18 / 22 packet rows to 43 exact candidate variable IDs across 11 policy
areas and leaving 4 packet rows without a candidate item in that source. It
still records 0 exact bill-topic support estimates and 0 MRP/small-area
estimates, so it is candidate item metadata only.
`reports/district-public-opinion-ces-policy-item-response-distribution-review.*`
joins those candidate variables to unweighted raw response-code distributions
from the official Cumulative CES Policy Preferences tabular file, covering
18 / 22 packet rows, 43 candidate variable IDs, 16 source years, and 32,667,671
packet-level attached item-response observations. It still records 0 exact
bill-topic support estimates, 0 directionally recoded support/opposition
estimates, and 0 MRP/small-area estimates.
`reports/district-public-opinion-ces-policy-item-codebook-direction-review.*`
joins those same packet candidates to official guide response labels or
continuous endpoint labels, covering 18 / 22 packet rows and 43 candidate
variable IDs. It records 14 packet rows with at least one binary item-wording
support/oppose direction and 28 unique attached binary candidate variables, but
still records 0 bill-text direction-alignment rows, 0 exact bill-topic support
estimates, and 0 MRP/small-area estimates.
`reports/district-public-opinion-ces-source-freshness.*` compares the cached
CES source metadata to the live Harvard Dataverse Cumulative CES metadata and
currently marks the local 2024 cache as stale relative to the official 2006-2025
distribution; it is a source-freshness audit only, not acquired bill-topic
opinion evidence.
`reports/lobbying-issue-linkage.*`
records the bounded LDA issue-label to policy-area topic bridge.
`reports/lobbying-bill-policy-context.*` records the bounded LDA
issue-label to cached govinfo bill/action context by shared policy area.
`reports/lobbying-bill-action-context.*` records exact LDA filing-text bill
identifiers joined to cached Congress.gov public-law bill/action, sponsor, and
enacted-outcome metadata for the 26 exact-mentioned public-law bill IDs. These
are join inventories, not validation evidence. `reports/lobbying-bill-text-review.*`
adds bounded stored activity-text review for those exact-match rows: all 484
rows now have the bill reference visible in stored full activity text, with 46
support-only rows, 3 opposition-only rows, 2 mixed support/opposition rows, 104
position/activity rows without direction, and 329 bill-list or title-only rows.
`reports/lobbying-bill-disposition-review.*` adds a prioritized manual
disposition/target review queue for the same 484 rows: 156 rows need manual
review, including 4 high-priority rows and 152 medium-priority rows, while 328
remain bill-reference-only context. `reports/lobbying-bill-manual-disposition-review.*`
adds source-reviewed classifications for the 4 high-priority rows, confirming 3
current-bill support rows, preserving 1 bill-reference-only row, and recording 0
rows with outcome-influence evidence. These are text signals and bounded source
reviews only. `reports/lobbying-bill-medium-disposition-packets.*` groups the
152 medium-priority rows into 102 source-review packets, collapsing 50 repeated
rows for review planning.
`reports/lobbying-bill-medium-directional-packet-review.*` source-reviews the
28 medium-priority support/opposition packets, confirming 20 current-bill
support packets representing 32 rows, 1 current-bill opposition packet, and
downgrading 7 packets to other-measure direction or monitoring/reference
context. `reports/lobbying-bill-medium-position-activity-packet-review.*`
source-reviews the 74 position/activity packets representing 104 rows,
classifying 59 issue/provision activity packets, 5 monitoring/analysis packets,
7 all-provisions packets, 2 position-represented packets, and 1 current-bill
opposition packet found in the position/activity queue. These reports remain
activity-text disposition evidence only, not
lobbying-contact, target, committee-action, roll-call, outcome-causality,
welfare, capture, or validation evidence.
`reports/bill-finance-lobbying-local-context-review.*` then closes the current
local no-exact-match review for the 10 bill-finance/lobbying queue rows while
preserving external campaign-finance target search, external lobbying search,
outside-spending target review, committee-action, roll-call, and outcome links
as missing.
`reports/bill-finance-lobbying-external-search-review.*` upgrades the external
LDA search layer for that same queue, finding current-bill activity-text mentions
for `117-hr-3359` and `117-hr-4693`.
`reports/bill-finance-lobbying-external-lda-mention-review.*` then closes the
current activity-text packet review for those external mentions, but it still
leaves independent contact or target source documents, committee-action,
roll-call, outcome, and external campaign-finance source documents open.
`reports/bill-finance-lobbying-campaign-finance-target-scope-review.*` closes
the current public FEC/OpenFEC target-scope review for the 4 campaign-finance
rows without upgrading them to bill-specific influence evidence.
`reports/bill-finance-lobbying-committee-action-context.*` adds cached
committee/floor bill-action flags for the 10 queued rows while keeping
committee-of-jurisdiction names, committee-action influence, roll-call
influence, and legislative-outcome causality open.
`reports/bill-finance-lobbying-committee-action-source-review.*` adds official
govinfo committee/action context for those rows, and
`reports/bill-finance-lobbying-roll-call-source-review.*` adds official House
Clerk roll-call source context for the numbered House roll calls without
upgrading any influence claim.
`reports/bill-finance-lobbying-member-vote-target-review.*` adds official
member-vote target-scope context for those roll calls, with 0 same-bill reviewed
campaign target Bioguide overlaps and 40 broad public FEC member-context
overlaps, without upgrading any influence claim.
`reports/bill-finance-lobbying-source-acquisition-queue.*` turns those open
gates into a ranked official-source acquisition queue for committee/no-direct-
committee dispositions, direct member target documents, outcome, independent LDA
target, and external campaign-finance target source documents without upgrading
the claim boundary.

## Main Paper Files

- Main ACM manuscript: [paper/acm-ci-framework/acm-ci-framework.tex](paper/acm-ci-framework/acm-ci-framework.tex)
- Main ACM PDF: [paper/acm-ci-framework/acm-ci-framework.pdf](paper/acm-ci-framework/acm-ci-framework.pdf)
- ODD+D appendix source: [paper/technical-appendix/odd-d-appendix.tex](paper/technical-appendix/odd-d-appendix.tex)
- ODD+D appendix PDF: [paper/technical-appendix/odd-d-appendix.pdf](paper/technical-appendix/odd-d-appendix.pdf)
- Paper build notes: [paper/README.md](paper/README.md)
- Simulator usage reference: [docs/usage.md](docs/usage.md)
- Empirical-boundary notes: [docs/calibration.md](docs/calibration.md)

Publication-strategy notes are kept under `paper/notes/` for project planning
and are excluded from the anonymous supplement.

## Anonymous Supplement

Build the double-blind artifact bundle with:

```sh
make supplement-anonymous
```

This writes:

- `dist/congress-institutional-simulator-anonymous.zip`

The supplement builder excludes local build products, private local files,
project-planning notes, and identity-bearing paths. It writes its own
reviewer-facing README inside the archive. The `dist/anonymous-supplement/`
directory is temporary staging and is left as a clean marker directory after a
successful build.

## Extended Documentation

Use [docs/usage.md](docs/usage.md) for the full simulator command reference,
historical campaign targets, scenario keys, and metric glossary.

Software-facing documentation:

- [docs/architecture.md](docs/architecture.md): package layout, runtime flow,
  extension points, and evidence boundaries.
- [docs/output-schema.md](docs/output-schema.md): generated report families,
  campaign CSV shape, empirical-boundary outputs, and stability expectations.
- [docs/adding-a-mechanism.md](docs/adding-a-mechanism.md): process, scenario,
  metric, and test workflow for new mechanisms.
- [docs/adding-a-campaign.md](docs/adding-a-campaign.md): campaign, CLI,
  Makefile, reporting, and verification workflow.
- [docs/reproducibility.md](docs/reproducibility.md): environment, commands,
  determinism policy, generated outputs, optional network workflows, and
  clean-clone audit template.
