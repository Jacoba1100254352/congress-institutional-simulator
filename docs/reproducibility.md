# Reproducibility

This repository is Makefile-first. Core reproduction should not require network
access.

## Required Local Tools

- Java 21
- GNU Make
- Python 3
- LaTeX with `latexmk`

The repository includes `.java-version` with `21`, and the Makefile enforces
Java 21 through `check-java`.

On macOS:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```

## Core Commands

Smoke test:

```sh
make test
```

Default simulator run:

```sh
make run
```

Main paper campaign:

```sh
make paper-campaign
```

Full no-network paper reproduction:

```sh
make reproduce-paper-offline
```

Paper readiness checks:

```sh
make paper-checks
```

This includes the PDF, anonymity, figure/table, empirical-boundary, linkage,
and linkage-roadmap consistency checks used before treating paper-facing output
as ready.

Anonymous supplement:

```sh
make supplement-anonymous
```

## Determinism Policy

The Makefile campaign targets use fixed seeds, currently `20260428` for the
paper-facing workflows. Fixed-seed CSV outputs should be reproducible for the
same code, Java version, and command.

PDF bytes can vary by TeX distribution, fonts, and build metadata. The paper
workflow therefore checks stable extracted-text and manifest metadata through
`paper/pdf-manifest.json`.

## Generated Outputs

Expected generated locations:

- `out/`: Java build outputs.
- `reports/`: simulation campaigns, diagnostics, validation reports, and
  manifests.
- `paper/figures/`: generated LaTeX tables and figures.
- `paper/build/`: LaTeX build intermediates.
- `paper/acm-ci-framework/acm-ci-framework.pdf`: main PDF.
- `paper/technical-appendix/odd-d-appendix.pdf`: appendix PDF.
- `dist/`: anonymous supplement outputs.

## Optional Network Workflows

Optional empirical refreshes are separate from core reproduction:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-govinfo-billstatus-linkage-raw
make build-core-raw-validation
make build-sponsor-bill-linkage-raw
make build-voteview-member-context-raw
make build-voteview-bill-linkage-raw
make build-lobbying-issue-linkage-raw
make build-campaign-finance-linkage-raw
make build-campaign-finance-member-context-raw
make build-campaign-finance-issue-context-raw
make build-district-public-opinion-linkage-raw
make build-district-public-opinion-policy-context-raw
make build-court-law-linkage-raw
make build-rulemaking-implementation-linkage-raw
make build-rulemaking-authority-linkage-raw
make build-rulemaking-history-linkage-raw
make build-rulemaking-comment-metadata-raw
make build-law-revision-bill-linkage-raw
make build-statutory-lineage-source-scan-raw
make build-statutory-lineage-olrc-current-scan-raw
make build-statutory-lineage-olrc-historical-scan-raw
make build-statutory-lineage-olrc-annual-text-diff-raw
make build-statutory-lineage-adjudication-raw
make build-statutory-lineage-target-review-packets-raw
make build-comparative-institution-linkage-raw
make empirical-linkage-report
make empirical-linkage-roadmap
make sponsor-bill-linkage
make comparative-institution-linkage
make court-law-linkage
make rulemaking-authority-linkage
make rulemaking-history-linkage
make rulemaking-comment-metadata
make bill-law-evidence-spine
make bill-law-lifecycle-readiness
make bill-law-lifecycle-next-actions
make statutory-lineage-review-queue
make statutory-lineage-source-scan
make statutory-lineage-target-section-triage
make statutory-lineage-olrc-current-scan
make statutory-lineage-olrc-historical-scan
make statutory-lineage-olrc-annual-text-diff
make statutory-lineage-adjudication
make statutory-lineage-target-review-packets
make statutory-lineage-target-section-diff-review
make statutory-lineage-target-lifecycle-bridge
make court-public-law-review-queue
make court-public-law-temporal-triage
make court-public-law-direct-review
make campaign-finance-district-context
make campaign-finance-issue-context
make campaign-finance-sponsor-bill-context
make district-public-opinion-policy-context
make lobbying-bill-policy-context
make raw-source-manifest
```

Some optional workflows may require API keys or public data access. Adapter
fixtures are not validation data. Curated raw extracts belong under
`data/validation/raw/` with source notes.
`make build-govinfo-billstatus-linkage-raw` refreshes the optional govinfo
BILLSTATUS cross-check for the cached Congress.gov bill-progression sample. It
uses public bulk XML, requires no API key, and does not establish a full bill
census, public-opinion, implementation, court, welfare, or model-validation
dataset.
`make build-sponsor-bill-linkage-raw` refreshes the optional sponsor aggregate
to public bill-metadata cache by Bioguide ID. It uses existing local sponsor and
bill metadata caches and does not establish full Center for Effective Lawmaking,
complete sponsor-history, legislative-quality, causal-effect, or
model-validation evidence.
`make build-comparative-institution-linkage-raw` refreshes the optional
QoG/OWID/V-Dem country-profile to simulator scenario-family metadata bridge. It
does not establish observed law-output productivity, bicameral disagreement,
country-level institutional fit, adoption, welfare, causal-effect, or
model-validation evidence.
`make build-campaign-finance-linkage-raw` refreshes the optional FEC
recipient-metadata crosswalk used by the linkage audit; it is not part of the
offline reproduction path and does not establish bill-level campaign-finance
validation. `make build-law-revision-bill-linkage-raw` refreshes the optional
Congress.gov public-law-to-bill/action metadata cache; it does not establish
codified statutory-lineage, implementation, or direct court-review validation.
`make build-campaign-finance-member-context-raw` refreshes the optional
candidate-to-Voteview member-context cache from local FEC recipient metadata and
Voteview member metadata; it does not infer identity from district alone and
does not establish bill-level influence, committee, issue, or causal-capture
validation.
`make build-campaign-finance-issue-context-raw` refreshes the optional
campaign-finance transaction-label to broad policy-topic cache from local
OpenFEC rows and local topic throughput; it does not establish bill-level
influence, committee jurisdiction, legislative outcome, private-contributor, or
causal-capture validation.
`make build-voteview-member-context-raw` refreshes the optional Voteview
member-metadata cache used to join cached roll-call rows to public member
metadata; it does not establish roll-call-to-bill, public-law, district-opinion,
sponsor-effectiveness, public-support, or model-validation evidence.
`make build-voteview-bill-linkage-raw` refreshes the optional Voteview
roll-call bill-number cache used to join sampled roll-call IDs to parsed bill
IDs and bounded Congress.gov bill-sample overlaps; it does not establish
complete roll-call-to-bill coverage, public-law linkage, public support,
outcomes, or model-validation evidence.
`make build-lobbying-issue-linkage-raw` refreshes the optional Senate LDA
issue-to-policy-area crosswalk used to join cached lobbying rows to broad local
topic context; it does not establish client-to-specific-bill, sponsor,
committee, causal capture, or model-validation evidence.
`make lobbying-bill-policy-context` derives the no-network bounded LDA
issue-label to cached govinfo bill/action context by shared policy area from
local reports; it does not establish client-to-specific-bill, sponsor target,
committee-action, roll-call, legislative-outcome causality, causal capture, or
model-validation evidence.
`make build-court-law-linkage-raw` refreshes the optional SCDB-to-public-law
authority-overlap cache. It parses SCDB `lawMinor` U.S.C. sections and overlaps
them with Federal Register authority U.S.C. citations attached to cached
public-law rows; it does not establish direct case-to-public-law review,
invalidation, lower-court, emergency-order, welfare, or model-validation
evidence.
`make build-district-public-opinion-linkage-raw` refreshes the optional
Congress.gov member-term and public-law sponsor-district metadata cache used to
join some CES district public-opinion rows to House-sponsored public-law bill
metadata; it does not establish bill-topic support, MRP, affected-group harm, or
public-benefit validation.
`make build-district-public-opinion-policy-context-raw` refreshes the optional
bounded sponsor-district bill policy-area context cache from local
district-public-opinion linkage rows and topic-throughput rows; it does not
establish issue-specific public support, MRP/small-area estimates,
affected-group harm, representative responsiveness, or public-benefit
validation.
`make build-rulemaking-implementation-linkage-raw` refreshes the optional
Federal Register document-metadata cache used to link final-rule rows to docket,
RIN, CFR, agency, and Federal Register-exposed Regulations.gov metadata; it does
not establish public-law, proposed-rule, enforcement, appropriations, or complete
comment-record validation.
`make build-rulemaking-authority-linkage-raw` refreshes the optional Federal
Register public-law authority-search cache used to text-verify rule documents
that mention cached public laws as authority; it does not establish exhaustive
implementation coverage, proposed-rule history, complete comments, enforcement,
appropriations, court review, welfare, or model validation.
`make build-rulemaking-history-linkage-raw` refreshes the optional Federal
Register proposed-rule history cache for authority-matched final rules. It
keeps proposed-rule records only when RIN or docket identifiers match and the
proposed rule is not later than the final rule; it does not establish complete
comment records, Unified Agenda stage coverage, enforcement, appropriations,
welfare, or model validation.
`make build-rulemaking-comment-metadata-raw` refreshes the optional Federal
Register detail-record comment-metadata cache for those authority-matched final
rules and matched proposed rules. It records only Federal Register-exposed
Regulations.gov docket, comment URL, comment-count, and comment-close metadata;
it does not establish complete comment records, commenter identities, comment
text, Unified Agenda stage coverage, enforcement, appropriations, welfare, or
model validation.
`reports/raw-source-manifest.*` records the committed raw extracts, metadata
notes, source hashes, and claim boundaries used by the offline empirical
pipeline. `reports/empirical-linkage-report.*` records which current raw
source families can actually join to another bill, topic, statute, agency,
court, sponsor, committee, or public-opinion source family.
`reports/empirical-linkage-roadmap.*` records the required join keys and
acceptance gates for source families that are not yet fully linked.
`reports/govinfo-billstatus-linkage.*` records the bounded govinfo BILLSTATUS
cross-check for the cached Congress.gov bill-progression sample; it is not a
full bill census or validation evidence.
`reports/sponsor-bill-linkage.*` records the bounded sponsor aggregate to public
bill-metadata linkage by Bioguide ID; it is not CEL effectiveness,
legislative-quality, or model-validation evidence.
`reports/comparative-institution-linkage.*` records the bounded comparative
country-profile to simulator scenario-family metadata bridge; it is not observed
law-output, bicameral-disagreement, institutional-fit, adoption, welfare, or
model-validation evidence.
`reports/court-law-linkage.*` records the bounded SCDB U.S.C.-section to
Federal Register authority-citation overlap for current public-law rows; it is
not direct judicial review or invalidation evidence.
`reports/rulemaking-authority-linkage.*` records the bounded Federal Register
public-law authority-search cache; it is not implementation-outcome,
enforcement, court-review, welfare, or model-validation evidence.
`reports/rulemaking-history-linkage.*` records the bounded Federal Register
proposed-to-final history cache for authority-matched final rules; it is not
complete public-comment, Unified Agenda, enforcement, appropriations, welfare,
or model-validation evidence.
`reports/rulemaking-comment-metadata.*` records bounded Federal Register-exposed
Regulations.gov comment metadata for authority-matched final-rule chains; it is
not complete comment-record, commenter-identity, comment-text, Unified Agenda,
enforcement, appropriations, welfare, or model-validation evidence.
`reports/voteview-member-context.*` records the bounded Voteview member rows
available for the cached roll-call sample; it does not establish bill-level or
public-opinion validation.
`reports/voteview-bill-linkage.*` records the bounded Voteview roll-call
bill-number crosswalk available for the cached roll-call sample; it does not
establish complete bill-level coverage, public-law linkage, or public-opinion
validation.
`reports/lobbying-issue-linkage.*` records the bounded LDA issue-label to
Congress.gov policy-area topic bridge for 144 / 146 cached LDA activity rows;
it does not establish bill-level lobbying influence, sponsor, committee, or
capture validation.
`reports/lobbying-bill-policy-context.*` records the bounded LDA issue-label to
cached govinfo bill/action context by shared Congress.gov policy area for 308
issue-policy bill contexts across 144 unique cached bills and 3 unique enacted
cached bills; it does not establish client-to-specific-bill lobbying influence,
sponsor targeting, committee-action influence, roll-call influence,
legislative-outcome causality, public benefit, or capture validation.
`reports/bill-law-evidence-spine.*` records the bounded public-law bill/action
metadata rows and attached revision-text proxy fields or sponsor-district
public-opinion context, bounded sponsor-district bill policy-area context,
same-policy campaign-finance sponsor context, same-policy LDA issue/bill
context,
Federal Register authority-search/proposed-history matches, proposed-rule
Regulations.gov docket/comment-portal metadata, Federal Register-exposed
comment metadata, final-rule timing metadata,
proposed-to-final timing metadata, or court U.S.C.-section overlaps; it is a
join inventory, not bill-specific finance or lobbying evidence and not
validation evidence.
`reports/bill-law-lifecycle-readiness.*` ranks those spine rows by direct
metadata, context-only metadata, and remaining high-priority lifecycle upgrade
gates, with copied source pointers for the next review pass. It is a review
queue, not validation evidence.
`reports/bill-law-lifecycle-next-actions.*` refines that queue after
court/public-law direct-review dispositions, closing direct-review gates that
are temporally excluded or source-reviewed not direct and selecting the next
actionable lifecycle gate. It is not validation evidence.
`reports/statutory-lineage-review-queue.*` narrows those next actions to the
codified U.S.C. lineage candidates and carries official-source review targets
plus authority, U.S.C.-citation, proposed-rule, docket, and court-overlap
pointers. It is a source-review queue, not statutory-lineage evidence, target
section diffs, implementation outcomes, court-review proof, welfare, or
model-validation evidence.
`reports/statutory-lineage-source-scan.*` records official GovInfo public-law
text scan results for that queue, including source hashes, U.S.C. references,
amendment/repeal/redesignation counts, and compact candidate snippets. It is
still not codified U.S.C. lineage, OLRC classification, target-section text
diffs, implementation-outcome, court-review, welfare, or model-validation
evidence.
`reports/statutory-lineage-target-section-triage.*` normalizes candidate
U.S.C. targets from the source scan and ranks them for manual OLRC and
codified-text review. It is still not codified U.S.C. lineage, target-section
text diffs, implementation-outcome, court-review, welfare, or model-validation
evidence.
`reports/statutory-lineage-olrc-current-scan.*` records official OLRC current
U.S. Code page availability for structured triage rows, including source
hashes and current-page public-law mentions. It is still not historical
codified U.S.C. lineage, before/after target-section text diffs,
implementation-outcome, court-review, welfare, or model-validation evidence.
`reports/statutory-lineage-olrc-historical-scan.*` records official OLRC annual
U.S. Code page availability for the year before enactment and the enactment
year for current-page candidates that mention the queued public law. It compares
source hashes and public-law mentions only; it is still not historical codified
U.S.C. lineage, public-law causation, before/after target-section text diffs,
implementation-outcome, court-review, welfare, or model-validation evidence.
`reports/statutory-lineage-olrc-annual-text-diff.*` records bounded post-year
public-law context snippets, raw-hash comparison flags, normalized section-text
signatures, and bounded first-change windows from those annual OLRC pages. It
is an automated cue queue for manual source review, not source-reviewed
codified U.S.C. lineage, public-law causation, adjudicated target-section text
diffs, implementation-outcome, court-review, welfare, or model-validation
evidence.
`reports/statutory-lineage-adjudication.*` classifies the annual OLRC cue rows
into official post-only public-law marker evidence and preserves the remaining
source-reviewed target-section diff, public-law causal attribution, effective
text, implementation, court-review, welfare, and model-validation gaps.
`reports/statutory-lineage-target-review-packets.*` packages those marker rows
with pre/post annual U.S. Code URLs, source hashes, normalized section-text
signatures, public-law context, first-change windows, and any downstream
target-section diff-review disposition annotation for manual review. It is
review infrastructure plus disposition context, not public-law causal
attribution, effective text, implementation, court-review, welfare, or
model-validation evidence.
`reports/statutory-lineage-target-section-diff-review.*` records the current
bounded official-source review pilot for Public Laws 117-146, 117-166,
117-167, 117-168, 117-169, 117-174, 117-180, 117-203, 117-219, 117-223,
117-229, 117-263, and 117-297. It attaches 75 reviewed target-section
dispositions to the packet queue and counts 73 source-reviewed target-section
diff rows while preserving public-law causal attribution, effective-text,
implementation, court-review, welfare, and model-validation gaps.
`reports/statutory-lineage-target-lifecycle-bridge.*` bridges those reviewed
target-section diff rows to bounded public-law-level implementation authority,
rulemaking history, Federal Register-exposed comment metadata, SCDB
U.S.C.-section overlap, court/public-law direct-review disposition, and bill-law
spine context. It records 19 authority base-section overlaps, 13 exact
authority target-reference overlaps, 0 court base-section overlaps, 0 exact
court target-reference overlaps, and 55 public-law-context-only rows. Base-section
overlaps are metadata context, not exact target-subsection evidence; the bridge
continues to preserve implementation-outcome, direct target-section
court-review, effective-text, causal, welfare, and model-validation gaps.
`reports/statutory-lineage-no-target-review.*` records curated source-reviewed
designation-law no-target dispositions for Public Laws 117-238 and 117-269,
where official GovInfo public-law text and official OLRC public-law PDFs expose
no U.S.C. references, amendment/repeal/redesignation cues, or target-section
candidates. It is not target-section text-diff, implementation-outcome,
court-review, welfare, causal-effect, or model-validation evidence.
`reports/statutory-lineage-codified-progress.*` keeps the current statutory
lineage progress rows visible: 13 public laws with source-reviewed
target-section diff rows and 2 reviewed designation-law
no-structured-U.S.C.-target dispositions.
`reports/court-public-law-review-queue.*` expands bounded court/public-law
U.S.C.-section overlaps into direct-review tasks. It is not direct court-review
evidence and does not establish that a case challenged, interpreted, reviewed,
or invalidated the listed public law, bill, rule, or implementation chain.
`reports/court-public-law-temporal-triage.*` applies a decision-date versus
enacted-date screen to that queue. It can rule out direct review of listed
public laws that postdate the case, but it does not prove direct court review
for post-enactment rows.
`reports/court-public-law-direct-review.*` records source-reviewed dispositions
for post-enactment court/public-law tasks and generated temporal exclusions for
pre-enactment rows. It is a direct-review audit only, not lower-court,
emergency-order, implementation-outcome, causal-invalidation, welfare, or model
validation evidence.
`reports/district-public-opinion-policy-context.*` records the bounded
sponsor-district public-law bill policy-area context rows that join CES district
proxies to local topic-throughput policy areas; it is not issue-specific
bill-support, MRP, affected-group harm, or public-benefit validation.
`reports/campaign-finance-district-context.*` records the bounded
House-candidate subset where public FEC recipient metadata can be joined to CES
district public-opinion context; it does not establish sponsor, bill, issue, or
causal influence evidence.
`reports/campaign-finance-member-context.*` records the bounded candidate subset
where public FEC recipient metadata can be joined to public Voteview member
context; it does not establish bill-level influence, committee, issue,
legislative-outcome, or causal-capture evidence.
`reports/campaign-finance-issue-context.*` records the bounded transaction-label
subset where public OpenFEC labels can be mapped to broad local policy-area
topics; it does not establish bill-level influence, committee jurisdiction,
legislative outcome, private-contributor, or causal-capture evidence.
`reports/campaign-finance-sponsor-bill-context.*` records the bounded matched
candidate/member subset where public FEC recipient metadata can be joined by
Bioguide ID to cached govinfo sponsored-bill metadata; it does not establish
campaign-finance influence, committee-action influence, legislative-outcome
causality, private-contributor disclosure, public benefit, or causal capture.

## Clean-Clone Audit Template

Run from outside the repository:

```sh
tmpdir=$(mktemp -d)
git clone /path/to/congress-institutional-simulator "$tmpdir/congress-institutional-simulator"
cd "$tmpdir/congress-institutional-simulator"
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
make reproduce-paper-offline
make supplement-anonymous
git status --short
```

Record the command output, runtime, Java version, TeX version, generated files,
and whether the final worktree is clean or only expected generated artifacts
changed.
