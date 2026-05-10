# Empirical Validation Readiness

This directory is a scaffold for raw-data validation. It is not used to fit the
current paper results, but the repository now includes documented raw samples
for bill progression, Voteview roll calls, lobbying disclosures, topic
throughput, sponsor proposal concentration, and committee-report signals so the
empirical bridge can exercise several real agenda-access and representation
signals rather than only missing-data placeholders.

Expected optional raw validation inputs under `data/validation/raw/`:

- `voteview_rollcalls.csv`: roll-call or member-level vote summaries with
  `congress`, `party`, `vote_id`, `vote`, and `ideology` columns.
- `bill_progression.csv`: bill-stage histories from Congress.gov or govinfo
  with `bill_id`, `introduced`, `committee_reported`, `floor_considered`, and
  `enacted` columns.
- `lobbying_disclosure.csv`: lobbying spending or client reports with
  `client`, `issue`, `amount`, and `period` columns.
- `topic_throughput.csv`: topic-level bill throughput with `topic`,
  `introduced`, `floor_considered`, and `enacted` columns.
- `sponsor_success.csv`: sponsor-level effectiveness or success measures with
  `sponsor_id`, `party`, `introduced`, and `enacted` columns.
- `district_public_opinion.csv`: district-level opinion and intensity rows with
  `district_id`, `issue`, `support`, `intensity`, `turnout`, and
  `affected_group_share` columns.
- `committee_activity.csv`: committee referral and work-product rows with
  `committee`, `issue`, `referred`, `hearings`, `reported`, `amendments`, and
  `discharged` columns.
- `campaign_finance.csv`: campaign-finance and outside-spending rows with
  `cycle`, `recipient`, `industry`, `amount`, and `independent_expenditure`
  columns.
- `court_review.csv`: constitutional-review rows with `case_id`, `issue`,
  `emergency_order`, `invalidated`, `vote_margin`, and `signed_opinion`
  columns.
- `rulemaking_implementation.csv`: post-enactment implementation rows from
  Federal Register, Unified Agenda, Regulations.gov, or comparable sources with
  `law_id`, `proposed_rule_date`, `final_rule_date`, `effective_date`,
  `comment_count`, `enforcement_capacity`, `nonenforced`, and `underfunded`
  columns.
- `law_revision_history.csv`: law-lineage rows from Congress.gov, govinfo,
  statutory-history datasets, or comparable sources with `law_id`,
  `enacted_date`, `amended`, `reauthorized`, `repealed`, `expired`, and
  `invalidated` columns.
- `comparative_institutions.csv`: comparative institutional rows with
  `country`, `year`, `chambers`, `district_magnitude`, `judicial_review`,
  `party_fragmentation`, and `legislative_productivity` columns.

Run `make validation-readiness` to generate a report showing which inputs are
present and whether the required columns are available. A passing readiness
report would only mean the raw files are shaped correctly; it would not by
itself validate the simulator.

Run `make empirical-validation` after adding one or more raw files to compute
dataset-specific summary metrics such as party unity, bill attrition, lobbying
spending concentration, topic throughput, sponsor success concentration,
committee activity, public-opinion intensity, implementation delay, enforcement
capacity, and post-enactment correction rates.
The command writes `reports/empirical-validation-summary.csv` and `.md`; missing
datasets are reported as missing rather than treated as build failures. These
adapters are deliberately source-shaped: adding real data still requires a
documented extraction and cleaning note for each source before the paper should
claim empirical validation rather than validation readiness.

Run `make validation-gap-report` to regenerate the paper-facing boundary report
and appendix table. That workflow joins readiness, raw summary metrics, and the
empirical bridge into `reports/empirical-validation-gap-report.*` and
`paper/figures/empirical_validation_gap_table.tex`. The point is to keep paper
claims honest: rows with raw inputs can be discussed as empirical bridges, while
missing rows remain synthetic or speculative model components.

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

The broader raw-validation sample can be generated with:

```sh
make build-core-raw-validation ARGS="--env-file /path/to/.env --derive-congress-from-bill-progression --preserve-sponsor-success"
```

That builder uses Voteview static CSVs, the existing Congress.gov bill-action
sample, optional Congress.gov bill-detail sponsor enrichment, and Senate LDA
filings. It is intentionally bounded and documented. Committee activity is
currently an action-derived committee-report signal rather than a full hearing
calendar, and the sponsor sample is a proposal-access bridge rather than a final
Center for Effective Lawmaking replacement.
