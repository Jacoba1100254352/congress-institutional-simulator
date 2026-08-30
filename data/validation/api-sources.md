# Public API Adapter Fixtures

The optional fetcher in `scripts/validation/fetch_public_api_samples.py` can
populate small adapter fixtures from public APIs. These files are not raw
validation data and are not calibrated datasets.

The separate builder in `scripts/validation/build_bill_progression_dataset.py`
creates the bill-progression raw validation sample:
`data/validation/raw/bill_progression.csv`. It uses Congress.gov bill-detail and
bill-action records and writes a metadata note next to the CSV. The broader
builder in `scripts/validation/build_core_raw_validation_datasets.py` adds
Voteview roll-call rows, Congress.gov-derived topic/sponsor/committee rows, and
Senate LDA lobbying rows. These raw samples are suitable for empirical-bridge
checks, but they are not complete censuses or fitted benchmarks.
`scripts/validation/build_govinfo_billstatus_linkage_dataset.py` adds a
bounded govinfo BILLSTATUS XML cross-check for the cached bill-progression
rows. It uses public bulk XML files, requires no API key, and joins only by
congress, bill type, and bill number. It is not a full bill census or
implementation, court, public-opinion, welfare, or model-validation dataset.
`scripts/validation/build_sponsor_bill_linkage_dataset.py` adds a bounded
sponsor aggregate to public bill-metadata linkage by Bioguide sponsor ID. It is
not full Center for Effective Lawmaking data, a complete sponsor history,
legislative-quality, causal-effect, or model-validation evidence.
`scripts/validation/build_voteview_member_context_dataset.py` adds Voteview
member metadata for the cached roll-call rows by Congress, chamber, and ICPSR
member ID. It is still not roll-call-to-bill, public-law, district-opinion,
sponsor-effectiveness, public-support, or model-validation linkage.
`scripts/validation/build_voteview_bill_linkage_dataset.py` adds a bounded
Voteview roll-call bill-number crosswalk for cached roll-call IDs by Congress,
chamber, and roll number. It parses bill numbers and flags overlap with the
cached Congress.gov bill-progression sample, but it is still not complete
roll-call-to-bill, public-law, public-opinion, outcome, or model-validation
linkage.
`scripts/validation/build_court_review_dataset.py` adds a Supreme Court
Database merits-case extract, and
`scripts/validation/build_rulemaking_implementation_dataset.py` adds a Federal
Register final-rule effective-date extract. Both are raw validation bridge
inputs with documented claim boundaries, not full validation datasets.
`scripts/validation/build_court_law_linkage_dataset.py` adds a bounded
SCDB-to-public-law authority-overlap cache by parsing SCDB `lawMinor` U.S.C.
sections and matching them to Federal Register authority U.S.C. citations
attached to cached public-law rows. It is still not direct case-to-public-law
review, invalidation, lower-court, emergency-order, or model-validation
evidence.
`scripts/validation/build_rulemaking_implementation_linkage_dataset.py` adds
Federal Register document metadata for cached final-rule rows, including docket,
RIN, CFR, agency, and Federal Register-exposed Regulations.gov metadata when
present. It is still not public-law authority, proposed-rule history,
enforcement, appropriations, or complete comment-record linkage.
`scripts/validation/build_rulemaking_authority_linkage_dataset.py` adds a
bounded Federal Register public-law authority-search cache for cached
public-law rows. It text-verifies rule documents that cite those public laws as
authority, but it is still not exhaustive implementation coverage,
proposed-rule history, enforcement, appropriations, court-review, welfare, or
model-validation evidence.
`scripts/validation/build_rulemaking_history_linkage_dataset.py` adds a
bounded Federal Register proposed-rule history cache for authority-matched
final-rule rows. It keeps proposed-rule rows only when they share RIN or docket
identifiers with the final rule and are not later than the final rule, but it
is still not complete Regulations.gov comment coverage, Unified Agenda stage
coverage, enforcement, appropriations, welfare, or model-validation evidence.
`scripts/validation/build_rulemaking_comment_records_dataset.py` adds a bounded
Regulations.gov comment-record metadata cache for Federal Register-exposed
dockets. It fetches only small public comment-record metadata sets by default,
records zero-comment dockets as complete no-comment rows, and leaves
high-volume or unknown-count dockets as explicit gaps. It is still not comment
text, attachment, commenter-identity, Unified Agenda, enforcement,
appropriations, welfare, or model-validation evidence.
`scripts/validation/build_campaign_finance_dataset.py` adds a bounded OpenFEC
raw extract for campaign-finance concentration and outside-spending bridges.
It is still not a bill-linked campaign-finance validation dataset.
`scripts/validation/build_campaign_finance_linkage_dataset.py` adds a public
FEC committee/candidate recipient-metadata crosswalk for the bounded
campaign-finance extract. It is still not a sponsor, issue,
committee-of-jurisdiction, bill, or causal influence linkage.
`scripts/validation/build_campaign_finance_member_context_dataset.py` adds a
local candidate-to-Voteview member-context cache from the FEC recipient
metadata and Voteview member-context cache. It requires name, chamber, state,
and district evidence and does not infer identity from district alone.
`scripts/validation/build_campaign_finance_issue_context_dataset.py` adds a
local transaction-label to broad policy-topic cache from the bounded OpenFEC
extract, recipient metadata, and local topic throughput. It is still not a
bill, committee-of-jurisdiction, legislative-outcome, private-contributor, or
causal influence linkage.
`scripts/validation/build_law_revision_history_dataset.py` adds a bounded
Congress.gov public-law title and CRS-summary text extract for amendment,
reauthorization/extension, repeal, and sunset/expiration revision-language
proxies. It is not a codified statutory-lineage or direct court-invalidation dataset.
`scripts/validation/build_law_revision_bill_linkage_dataset.py` adds bounded
Congress.gov bill-detail and bill-action metadata for public-law rows. It is
still not codified statutory lineage, implementation feedback, court-review
linkage, or U.S. Code target-section evidence.
`scripts/validation/build_district_public_opinion_dataset.py` adds a bounded
Cumulative CES Common Content district aggregate for public-opinion and turnout
proxy signals. It is not MRP, bill-topic support, or issue-specific
affected-group measurement.
`scripts/validation/build_district_public_opinion_linkage_dataset.py` adds a
Congress.gov member-term and public-law bill metadata crosswalk for cached CES
district rows. It links some district-opinion rows to House-sponsored
public-law bill metadata by sponsor district only; it is not bill-topic support,
MRP, affected-group harm, representative-responsiveness, or public-benefit
validation.
`scripts/validation/build_district_public_opinion_policy_context_dataset.py`
adds bounded sponsor-district public-law bill policy-area context by joining the
local district-public-opinion linkage cache to local topic-throughput rows. It is
not issue-specific bill support, MRP, affected-group harm, representative
responsiveness, or public-benefit validation.
`scripts/validation/build_district_public_opinion_census_denominator_dataset.py`
adds official Census TIGERweb 116th congressional-district 2020 population,
housing-unit, and geography denominators for the queued sponsor districts. It
requires no API key, but it is still not ACS policy-specific affected-population
detail, bill-topic support, MRP, affected-group harm, representative
responsiveness, or public-benefit validation.
`scripts/validation/build_district_public_opinion_acs_context_dataset.py`
adds official ACS 2017-2021 5-year broad 116th congressional-district
demographic, economic, citizenship, language, disability, internet, poverty,
and veteran context for those queued sponsor districts from the keyless
Census table-based Summary File. It is not bill-topic support, MRP,
bill-text-specific affected-population definitions, affected-group support/harm,
representative responsiveness, public-benefit, or model-validation evidence.
`scripts/validation/build_comparative_institutions_dataset.py` adds a bounded
QoG Data Finder plus OWID/V-Dem comparative-institutions profile for chamber
count, district magnitude, judicial constraints, party fragmentation, and a
legislative-constraints proxy. It is not observed legislative productivity or
comparative institutional-fit validation.
`scripts/validation/build_comparative_institution_linkage_dataset.py` adds a
bounded bridge from that profile to simulator scenario-family metadata anchors.
It is not observed law-output, bicameral-disagreement, institutional-fit,
adoption, welfare, causal-effect, or model-validation evidence.

Current sources:

- Congress.gov API: bill list, law list, bill-detail, and bill-action endpoints.
  Generated files: `bill_progression.csv`, `topic_throughput.csv`, and
  `sponsor_success.csv`.
- govinfo BILLSTATUS bulk XML: public bill/action metadata for cached
  bill-progression rows. Generated file: `govinfo_billstatus_linkage.csv`.
- Congress.gov/govinfo sponsor metadata plus the bounded sponsor aggregate:
  sponsor-to-bill metadata by Bioguide ID. Generated file:
  `sponsor_bill_linkage.csv`.
- QoG/OWID/V-Dem comparative institution profile plus local simulator scenario
  family anchors. Generated file: `comparative_institution_linkage.csv`.
- OpenFEC API: Schedule A individual receipts and Schedule E independent
  expenditure endpoints. Generated file: `campaign_finance.csv`.
- FEC bulk downloads: committee master, candidate master, and
  candidate-committee linkage files. Generated file:
  `campaign_finance_linkage.csv`.
- Voteview static CSVs: member and vote rows. Generated file:
  `voteview_rollcalls.csv`.
- Voteview static CSVs: member metadata rows. Generated file:
  `voteview_member_context.csv`.
- Voteview static CSVs: roll-call metadata rows. Generated file:
  `voteview_bill_linkage.csv`.
- U.S. Senate LDA API: filing rows with activity issue labels and disclosed
  income/expense amounts. Generated file: `lobbying_disclosure.csv`.
- U.S. Senate LDA API: filing activity-text search rows and exact current-bill
  mention rows for a bounded public-law candidate set. Generated files:
  `lobbying_bill_mention_searches.csv` and `lobbying_bill_mentions.csv`.
  The derived `reports/lobbying-bill-action-context.*` report joins those exact
  bill IDs to cached Congress.gov public-law bill/action metadata. The derived
  `reports/lobbying-bill-text-review.*` report classifies bounded stored
  activity-text support/position signals and records rows that need full
  activity-text refetch before text review. The derived
  `reports/lobbying-bill-disposition-review.*` report prioritizes rows for
  manual disposition or target review. The derived
  `reports/lobbying-bill-manual-disposition-review.*` report source-reviews the
  4 high-priority rows, confirming 3 current-bill support rows and preserving 1
  bill-reference-only row without outcome-influence evidence. The derived
  `reports/lobbying-bill-medium-disposition-packets.*` report groups the 152
  medium-priority rows into 102 review packets. The derived
  `reports/lobbying-bill-medium-directional-packet-review.*` report
  source-reviews the 28 support/opposition packets, confirming 20 current-bill
  support packets representing 32 rows and 1 current-bill opposition packet
  while downgrading 7 packets to other-measure direction or monitoring/reference
  context. These reports are not lobbying-contact, targeting beyond the
  activity-text reference, influence, outcome-causality, welfare, or
  model-validation evidence.
- Local bill-finance/lobbying queue context: curated review file
  `bill_finance_lobbying_local_context_review.csv`, derived from
  `reports/bill-finance-lobbying-review-queue.*`,
  `reports/campaign-finance-sponsor-bill-context.*`, and
  `reports/lobbying-bill-policy-context.*`. The generated
  `reports/bill-finance-lobbying-local-context-review.*` report records only
  that the current local same-policy context lacks current-bill exact matches
  for the 10 queued public-law rows; it is not external target/source,
  outside-spending target, lobbying-contact, influence, outcome, welfare,
  capture, or model-validation evidence.
- U.S. Senate LDA API targeted current-bill search for the bill-finance/lobbying
  queue: `bill_finance_lobbying_external_lda_searches.csv` and
  `bill_finance_lobbying_external_lda_mentions.csv`. The generated
  `reports/bill-finance-lobbying-external-search-review.*` report records exact
  activity-text bill-reference evidence for 2 queued bills and complete no-exact
  LDA search status for 8 queued bills. It also marks 4 campaign-finance rows
  for public FEC/OpenFEC candidate/committee/outside-spending target-scope
  review. The derived
  `reports/bill-finance-lobbying-campaign-finance-target-scope-review.*`
  report closes that public target-scope review with 0 bill-ID, sponsor-overlap,
  committee-action, or outcome-influence links; public FEC/OpenFEC data still
  does not expose bill IDs or bill-specific campaign-finance influence.
- Supreme Court Database 2025 Release 01: case-centered merits rows. Generated
  file: `court_review.csv`.
- Supreme Court Database 2025 Release 01 plus Federal Register authority
  citations: bounded U.S.C.-section overlap rows. Generated file:
  `court_law_linkage.csv`.
- Federal Register API v1: final-rule publication, effective-date rows, and
  document-level metadata. Generated files: `rulemaking_implementation.csv`
  and `rulemaking_implementation_linkage.csv`.
- Congress.gov API: public-law list plus bill-title and bill-summary endpoints.
  Generated file: `law_revision_history.csv`.
- Congress.gov API: bill-detail and bill-action endpoints for public-law bill
  IDs. Generated file: `law_revision_bill_linkage.csv`.
- Harvard Dataverse Cumulative CES Common Content DOI 10.7910/DVN/II2DB6:
  2024 district survey aggregate. Generated file:
  `district_public_opinion.csv`.
- Congress.gov API: member endpoint plus public-law bill/action metadata for
  sponsor district terms. Generated file:
  `district_public_opinion_linkage.csv`.
- Local district-public-opinion linkage and topic-throughput caches: bounded
  sponsor-district public-law bill policy-area context. Generated file:
  `district_public_opinion_policy_context.csv`.
- Census TIGERweb Legislative MapServer layer 12: 116th congressional-district
  2020 population, housing-unit, land/water area, and centroid denominator
  attributes for queued sponsor districts. Generated file:
  `district_public_opinion_census_denominators.csv`.
- QoG Data Finder selected-variable CSV: DES district magnitude and effective
  legislative-party count plus Henisz POLCON chamber indicators. Generated
  file: `comparative_institutions.csv`.
- Our World in Data/V-Dem Grapher CSVs: judicial constraints on the executive
  and legislative constraints on the executive. Generated file:
  `comparative_institutions.csv`.

Run example:

```sh
make fetch-validation-samples ARGS="--env-file /path/to/.env --bill-limit 50 --law-limit 25 --fec-limit 100"
```

The fetcher reads `CONGRESS_API_KEY` and `OPENFEC_API_KEY` from the environment
or from the provided env file. It never writes API keys to disk. The OpenFEC
normalization intentionally omits contributor names and street addresses; the
sample keeps only recipient, coarse industry/occupation text, amount, cycle, and
whether the row came from independent-expenditure data.

A documented govinfo BILLSTATUS cross-check for the cached bill sample can be
generated with:

```sh
make build-govinfo-billstatus-linkage-raw
```

The builder downloads public govinfo BILLSTATUS XML records for the cached
bill-progression rows and writes a bounded cross-check by congress, bill type,
and bill number. It does not require an API key and does not create a full bill
census, bill-topic opinion, lobbying or campaign-finance influence,
implementation, court-outcome, welfare, or model-validation evidence.

A documented Voteview member-metadata context can be generated with:

```sh
make build-voteview-member-context-raw
```

The builder downloads Voteview static member CSVs for the Congresses present in
the cached roll-call rows and writes a bounded member-context cache. It maps
roll-call member-vote rows to Bioguide, party, state/district, and ideal-point
metadata only.

A documented Voteview roll-call bill-number crosswalk can be generated with:

```sh
make build-voteview-bill-linkage-raw
```

The builder downloads Voteview static roll-call metadata for the Congresses
present in the cached roll-call rows. It writes a bounded vote-level cache that
normalizes Voteview bill numbers into `congress-bill_type-number` IDs when
possible and flags whether those IDs overlap the cached Congress.gov
bill-progression sample.

A documented Senate LDA issue-to-policy-area crosswalk can be generated with:

```sh
make build-lobbying-issue-linkage-raw
```

The builder reads cached Senate LDA issue labels and cached Congress.gov
policy-area topic aggregates, then applies a deterministic issue-label
crosswalk. It writes broad issue context for 144 / 146 cached LDA activity rows.
It does not fetch private information and does not create client-to-bill,
sponsor, committee, causal capture, or model-validation evidence.

A documented official LDA filing-text bill-mention cache can be generated with:

```sh
make build-lobbying-bill-mentions-raw
```

The builder searches the public Senate LDA filings API for exact current-bill
identifiers from the bounded public-law candidate set and writes search audit
rows plus exact filing activity-text mention rows. The committed cache currently
records 484 exact activity-text bill mention rows across 26 cached public-law
bill IDs from 40 searched public-law rows. It does not create
support/opposition, sponsor/member targeting, committee-action influence,
roll-call influence, legislative-outcome causality, welfare, causal capture, or
model-validation evidence.
The current committed cache was refreshed with `ARGS="--description-limit 0"` so
it stores full LDA activity descriptions for exact-match rows; the derived
`reports/lobbying-bill-text-review.*` report preserves the no-influence claim
boundary while classifying deterministic text signals. The derived
`reports/lobbying-bill-disposition-review.*` report prioritizes 156 of those
484 exact-match rows for manual disposition or target review, and
`reports/lobbying-bill-manual-disposition-review.*` records source-reviewed
disposition/target classifications for the 4 high-priority rows without
upgrading them to influence evidence. `reports/lobbying-bill-medium-disposition-packets.*`
groups the 152 medium-priority rows into packets for follow-up review.
`reports/lobbying-bill-medium-directional-packet-review.*` source-reviews the
support/opposition packet subset and confirms or narrows activity-text
directions without upgrading them to contact, target, outcome, or influence
evidence. `reports/lobbying-bill-medium-position-activity-packet-review.*`
source-reviews the position/activity packet subset and classifies issue/provision
activity, monitoring/analysis, all-provisions, position-represented, and one
current-bill opposition packet without upgrading the result to contact, target,
outcome, or influence evidence.

A documented raw OpenFEC campaign-finance sample can be generated with:

```sh
make build-campaign-finance-raw ARGS="--env-file /path/to/.env --cycle 2024 --receipts-limit 100 --independent-limit 100"
```

The raw builder reads `OPENFEC_API_KEY` from the environment or env file and
falls back to OpenFEC's public `DEMO_KEY` for small bounded samples. It never
writes API keys to disk. The committed raw file omits contributor names,
contributor street addresses, and payee names; it keeps committee/candidate
recipient IDs, coarse occupation/employer/category labels, positive amounts,
cycle, transaction date, and whether the row is an independent expenditure.

A documented FEC recipient-metadata linkage for the campaign-finance sample can
be generated with:

```sh
make build-campaign-finance-linkage-raw ARGS="--cycle 2024"
```

The linkage builder uses public FEC bulk downloads and does not require an API
key. It maps cached recipient IDs to committee or candidate metadata and
candidate-committee linkage IDs where available. It omits treasurer names,
street addresses, contributor names, contributor addresses, payee names, and
raw contribution records. The output remains metadata linkage only.

A documented FEC candidate-to-Voteview member context cache can be generated
from local caches with:

```sh
make build-campaign-finance-member-context-raw
```

The builder does not require network access. It reads
`campaign_finance_linkage.csv` and `voteview_member_context.csv`, then matches
congressional candidate rows to Voteview/Bioguide member metadata only when
candidate name, chamber, state, and district evidence agree. It leaves
challengers, presidential candidates, noncandidate committees, and ambiguous
rows unmatched. It remains member-context metadata only, not bill-level
influence, sponsor effectiveness, committee-of-jurisdiction, issue targeting,
private-contributor, or capture validation evidence.

A documented FEC transaction-label issue-context cache can be generated from
local caches with:

```sh
make build-campaign-finance-issue-context-raw
```

The builder does not require network access. It reads `campaign_finance.csv`,
`campaign_finance_linkage.csv`, and `topic_throughput.csv`, then maps
high-confidence occupation, employer, or expenditure-purpose labels to broad
local policy-area topics. Generic roles, support/oppose flags, unknown labels,
and campaign-administrative labels remain unmapped. It remains broad
issue-sector context only, not bill-level influence, committee jurisdiction,
reviewed outside-spending target, legislative outcome, private-contributor, or
causal-capture evidence.

A documented Federal Register document-metadata linkage for the final-rule
implementation sample can be generated with:

```sh
make build-rulemaking-implementation-linkage-raw
```

The linkage builder does not require an API key. It maps cached Federal
Register document numbers to official document metadata, docket IDs, RINs, CFR
references, agency identifiers, topics, and Federal Register-exposed
Regulations.gov docket, document, and comment-count metadata when present. It
does not fetch full rule text, proposed-rule histories, public-law authorities,
enforcement outcomes, appropriations records, or private comment submitter
fields.

A documented Federal Register public-law authority-search cache can be
generated for the cached public-law rows with:

```sh
make build-rulemaking-authority-linkage-raw
```

The authority builder does not require an API key. It searches Federal Register
rule documents for cached public-law citation forms, fetches public full-text
records, and keeps only text-verified public-law authority matches. It does not
provide exhaustive implementation coverage, proposed-to-final histories,
complete Regulations.gov comment records, enforcement outcomes, appropriations
capacity, court review, public benefit, welfare, causal effects, or model
validation.

A documented Federal Register proposed-to-final history cache can be generated
for authority-matched final-rule rows with:

```sh
make build-rulemaking-history-linkage-raw
```

The history builder does not require an API key. It searches Federal Register
proposed-rule records by final-rule RIN and docket identifiers and keeps only
metadata rows that share normalized identifiers with the final rule and are not
published later than the final rule. It does not fetch complete Regulations.gov
comment records, Unified Agenda stages, enforcement outcomes, appropriations
records, or private comment submitter fields.

A documented bounded Regulations.gov comment-record metadata cache can be
generated for Federal Register-exposed rulemaking dockets with:

```sh
make build-rulemaking-comment-records-raw
```

The comment-record builder may use `REGULATIONS_GOV_API_KEY` or the public demo
key for bounded retrieval. It starts from Federal Register-exposed docket
and comment-count metadata, fetches only bounded public comment-record metadata
sets by default, and records high-volume or unknown-count dockets as still
incomplete. It does not fetch comment text, attachments, private submitter
details, Unified Agenda stages, enforcement outcomes, appropriations records,
public benefit, welfare, causal effects, or model validation.

A documented sanitized Regulations.gov comment-detail review can be generated
for complete bounded comment-record rows and bounded partial-docket samples with:

```sh
make build-rulemaking-comment-text-review-raw
```

The comment-text review builder may use `REGULATIONS_GOV_API_KEY` or the public
demo key for bounded retrieval. It prioritizes complete comment-record metadata
rows with retrieved comment IDs, then adds bounded partial-docket sample rows.
It fetches public comment-detail records and stores text availability,
normalized text hashes, lengths, attachment counts, source record status, and
coarse implementation-related cue flags. It deliberately omits the full comment
body and submitter/contact fields. Partial sample rows do not prove complete
docket coverage, and the layer does not create a full comment-text corpus,
attachment-text, commenter-identity, sentiment, implementation-outcome, welfare,
or model-validation evidence.

A documented raw Congress.gov public-law revision-text sample can be generated
with:

```sh
make build-law-revision-raw ARGS="--env-file /path/to/.env --congresses 117,118 --laws-per-congress 60"
```

The builder reads `CONGRESS_API_KEY` from the environment or env file and never
writes the key to disk. The normalized rows are enacted public laws. Revision
flags are text-derived indicators from public-law titles and CRS summaries;
`invalidated` is fixed at `0` because Congress.gov titles and summaries are not
a judicial-invalidation source.

A documented Congress.gov public-law-to-bill/action metadata linkage can be
generated with:

```sh
make build-law-revision-bill-linkage-raw ARGS="--env-file /path/to/.env --limit 40"
```

The linkage builder reads `CONGRESS_API_KEY` from the environment or env file
and never writes the key to disk. The committed cache links a bounded subset of
public-law rows to Congress.gov bill details and bill-action histories. It does
not fetch bill text, codified U.S. Code text, OLRC editorial notes,
implementation records, Regulations.gov dockets, or later court-review links.

A documented district public-opinion proxy can be generated from Cumulative CES
Common Content with:

```sh
make build-district-public-opinion-raw ARGS="--year 2024 --min-support-respondents 30"
```

The builder downloads the public Harvard Dataverse Feather file into
`no-include/validation-cache/ces/` unless `--source-file` is supplied. It
requires `pyarrow` for Feather parsing. The normalized rows are weighted
district-issue aggregates for House-representative approval, Democratic
presidential preference, Democratic House preference, turnout, and an
uninsured-share vulnerability proxy. They are not MRP estimates and do not
validate bill-topic public support, affected-group harm, or generated public
benefit.

A live CES source-freshness audit can be generated with:

```sh
make district-public-opinion-ces-source-freshness
```

The audit reads the current Harvard Dataverse metadata for DOI
10.7910/DVN/II2DB6 and compares it to
`data/validation/raw/district_public_opinion.metadata.md`. It is intentionally
separate from offline paper checks because it depends on live source metadata.
It does not refresh the raw extract or acquire bill-topic item IDs, MRP
estimates, or affected-population evidence.

A documented district public-opinion bill-sponsor metadata linkage can be
generated from the CES district aggregate, Congress.gov member endpoint, and
public-law bill/action metadata with:

```sh
make build-district-public-opinion-linkage-raw ARGS="--env-file /path/to/.env"
```

The linkage builder reads `CONGRESS_API_KEY` from the environment or env file
and never writes the key to disk. The committed cache links some CES
district-opinion rows to House-sponsored public-law bill metadata by sponsor
district. It does not fetch public-opinion microdata, infer bill-topic support,
build MRP estimates, measure issue-specific affected-group support or harm, or
validate representative responsiveness, welfare, or public benefit.

A documented district public-opinion policy-context cache can be generated from
local caches with:

```sh
make build-district-public-opinion-policy-context-raw
```

The builder does not require network access. It reads
`district_public_opinion_linkage.csv` and `topic_throughput.csv`, then attaches
local bill policy-area topic context to cached sponsor-district public-law bill
metadata rows. It remains policy-area context only, not issue-specific
bill-support, MRP, affected-group harm, representative responsiveness, welfare,
or public-benefit validation.

A documented district public-opinion Census denominator cache can be generated
from the source-packet queue with:

```sh
make build-district-public-opinion-census-denominators-raw
```

The builder uses the public Census TIGERweb 116th congressional-district layer
to add 2020 population, housing-unit, land/water area, and centroid
denominators for queued sponsor districts. It remains district-frame
denominator context only, not bill-topic support, MRP/small-area estimation,
ACS detail, affected-group support/harm, welfare, or public-benefit validation.

A documented district public-opinion ACS context cache can be generated from
the source-packet queue with:

```sh
make build-district-public-opinion-acs-context-raw
```

The builder uses the public ACS 2017-2021 5-year table-based Summary File and
requires no API key. It extracts broad 116th congressional-district population,
race/ethnicity, citizenship, language, disability, income, poverty, veteran,
employment, and internet-access context for queued sponsor districts. It treats
Census ACS special numeric estimate/MOE sentinel values as missing numeric
fields and remains broad district context only, not bill-topic support,
MRP/small-area estimation, bill-text-specific affected-population definitions,
affected-group support/harm, welfare, or public-benefit validation.

A documented comparative-institutions profile can be generated from QoG Data
Finder and OWID/V-Dem CSVs with:

```sh
make build-comparative-institutions-raw
```

The builder caches source CSVs under
`no-include/validation-cache/comparative-institutions/` unless source files are
supplied. The output uses the latest complete country-year per ISO3 country in
the requested 2010-2020 window. `legislative_productivity` is a
schema-compatible V-Dem legislative-constraints proxy, not observed law-output
productivity.

A bounded comparative-institution scenario-family linkage cache can be generated
from the cached comparative profile with:

```sh
make build-comparative-institution-linkage-raw
```

This writes `data/validation/raw/comparative_institution_linkage.csv` and
`data/validation/raw/comparative_institution_linkage.metadata.md`. It maps
country-year institutional profiles to simulator scenario-family metadata
anchors only; it does not provide observed legislative-output productivity,
bicameral disagreement, institutional-fit, adoption, welfare, causal-effect, or
model-validation evidence.

Limitations:

- The fixture sample is deliberately small.
- Congress.gov action text is reduced to coarse introduced, committee-reported,
  floor-considered, and enacted indicators.
- OpenFEC rows are not cleaned into a full campaign-finance ontology. Cached
  recipient IDs can now be linked to public FEC candidate/committee metadata,
  bounded Voteview member context, House-candidate district context, and broad
  transaction-label issue-sector context, but not to bills, sponsors,
  committees of jurisdiction, reviewed outside-spending targets, legislative
  outcomes, or causal influence.
- Voteview roll-call rows can now be linked to public member metadata and a
  bounded bill-number crosswalk for sampled roll-call IDs, but not to complete
  bill coverage, public laws, district public-opinion rows,
  sponsor-effectiveness records, implementation or court outcomes, or
  legislative-outcome validation.
- Committee activity derived from the current Congress.gov raw sample uses
  bill-action report flags, not complete hearing or markup calendars.
- Sponsor success in the committed sample is a proposal-access concentration
  bridge. A full member-effectiveness target still requires curated Center for
  Effective Lawmaking or comparable data.
- The Federal Register implementation sample now has document, docket, RIN,
  CFR, agency, and Federal Register-exposed Regulations.gov metadata for most
  cached rows, plus a bounded public-law authority-search cache and a bounded
  proposed-history cache for part of the cached public-law sample, plus bounded
  bounded complete and partial Regulations.gov comment-record metadata. It still does not
  provide high-volume comment retrieval, comment text, Unified Agenda stages,
  enforcement failures, appropriations capacity, court-review outcomes, or
  exhaustive implementation coverage. Implementation-feedback validation still
  requires those additional sources.
- The law-revision sample is a bounded revision-language proxy with a bounded
  Congress.gov bill/action metadata linkage. Full correction-over-time
  validation still requires OLRC/govinfo statutory lineage, codified-text
  diffs, observed expiration outcomes, implementation links, and later
  judicial-invalidation sources.
- The district public-opinion sample is a direct CES district aggregation with a
  bounded sponsor-district bill metadata linkage for some House-sponsored public
  laws, bounded bill policy-area context, source-acquisition packets, and
  Census population/housing denominators plus broad ACS district context. Full
  representation validation still requires issue-to-bill mapping, MRP or other
  small-area estimation where appropriate, bill-text-specific affected-population
  joins, and affected-group support/harm evidence.
- The comparative-institutions sample is a bounded country-profile proxy only.
  The auxiliary linkage cache maps rows to simulator scenario-family metadata
  anchors only. Full comparative claims still require IPU and ParlGov chamber
  details, bicameral disagreement data, and observed legislative-output
  productivity.
- These files should not be described as empirical validation of the simulator.
  Adapter fixtures remain under `data/validation/fixtures/`; curated documented
  raw extracts belong under `data/validation/raw/`.
