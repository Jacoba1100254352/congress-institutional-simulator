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

Run `make validation-readiness` to generate a report showing which inputs are
present and whether the required columns are available. A passing readiness
report would only mean the raw files are shaped correctly; it would not by
itself validate the simulator.

Run `make empirical-validation` after adding one or more raw files to compute
dataset-specific summary metrics such as party unity, bill attrition, lobbying
spending concentration, topic throughput, and sponsor success concentration.
The command writes `reports/empirical-validation-summary.csv` and `.md`; missing
datasets are reported as missing rather than treated as build failures.
