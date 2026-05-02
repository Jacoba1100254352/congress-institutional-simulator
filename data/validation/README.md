# Empirical Validation Readiness

This directory is a scaffold for future raw-data validation. It is not used to
fit the current paper results.

Expected optional inputs under `data/validation/raw/`:

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
- `comparative_institutions.csv`: comparative institutional rows with
  `country`, `year`, `chambers`, `district_magnitude`, `judicial_review`,
  `party_fragmentation`, and `legislative_productivity` columns.

Run `make validation-readiness` to generate a report showing which inputs are
present and whether the required columns are available. A passing readiness
report would only mean the raw files are shaped correctly; it would not by
itself validate the simulator.

Run `make empirical-validation` after adding one or more raw files to compute
dataset-specific summary metrics such as party unity, bill attrition, lobbying
spending concentration, topic throughput, and sponsor success concentration.
The command writes `reports/empirical-validation-summary.csv` and `.md`; missing
datasets are reported as missing rather than treated as build failures. These
adapters are deliberately source-shaped: adding real data still requires a
documented extraction and cleaning note for each source before the paper should
claim empirical validation rather than validation readiness.

Optional API smoke-test samples can be fetched with:

```sh
make fetch-validation-samples ARGS="--env-file /path/to/.env"
```

The fetcher currently reads `CONGRESS_API_KEY` and `OPENFEC_API_KEY` when
available. It writes small normalized samples for bill progression, topic
throughput, sponsor success, and campaign finance. These samples are useful for
testing the adapters against real public API shapes, but they are deliberately
too small and too lightly cleaned to count as empirical validation.
