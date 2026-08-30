# Rulemaking Comment Text Review

Generated: 2026-07-27T01:31:05+00:00

Source:

- Regulations.gov API v4 comment detail endpoint.
- API documentation: https://open.gsa.gov/api/regulationsgov/
- Input comment-record file: `data/validation/raw/rulemaking_comment_records.csv`.
- API key mode: public_demo_key.
- Max comments fetched: 25.
- Public-law filter: all.
- API key required: yes for non-demo production use; the bounded default may use the public DEMO_KEY for low-volume detail checks.

Transformation:

- Starts from complete Regulations.gov comment-record metadata rows and bounded partial rows with retrieved comment IDs.
- Prioritizes complete-docket detail rows, then adds partial-docket sample rows up to the max-comments limit.
- Fetches bounded public comment-detail records by comment ID.
- Records comment text availability, normalized text hash, text length, attachment count, and coarse implementation-related cue flags.
- Omits the full comment body and submitter/contact fields from the CSV and report.
- Does not fetch attachment text, validate commenter identity, code sentiment, or infer implementation outcomes.

Rows:

- Public-law rows represented: 2.
- Public comment-detail rows: 25.
- Detail rows fetched: 0.
- Rows with public comment text available and hashed: 0.

Review scopes:

- complete_docket_detail: 1
- partial_docket_sample_detail: 24

Detail statuses:

- comment_detail_api_error:HTTPError429: 25

Claim boundary:

Sanitized Regulations.gov public comment-detail review for complete bounded comment-record rows and bounded partial-docket samples. It records text availability, normalized text hash, text length, attachment count, source comment-record status, and coarse implementation-related cue flags while omitting the comment body and submitter/contact fields. Partial sample rows do not prove complete docket coverage. This is not a full comment-text corpus, attachment text, commenter-identity validation, sentiment or position coding, representativeness evidence, Unified Agenda stage coverage, enforcement outcome, appropriations capacity, implementation-outcome evidence, public benefit, welfare, causal-effect, or model-validation evidence.
