# Rulemaking Comment Records

Generated: 2026-07-06T04:46:32+00:00

Source:

- Regulations.gov API v4 comments endpoint.
- API documentation: https://open.gsa.gov/api/regulationsgov/
- Input comment metadata file: `data/validation/raw/rulemaking_comment_metadata.csv`.
- API key mode: public_demo_key.
- Max expected comments fetched per docket: 4000.
- Page size: 250; max pages: 20.
- Public-law filter: 117-238.
- Merged with existing output: yes.
- API key required: yes for non-demo production use; the bounded default may use the public DEMO_KEY for low-volume or resumed bounded retrievals.

Transformation:

- Starts from Federal Register-exposed Regulations.gov docket and comment-count metadata.
- Builds one public-law/docket row per final or proposed-rule docket.
- Fetches only dockets at or below the configured expected-comment threshold.
- Preserves partial metadata rows when an API error occurs after records have been retrieved.
- Treats zero-comment dockets as complete no-comment rows without calling the API.
- Does not fetch comment text, attachments, private submitter details, Unified Agenda stages, enforcement outcomes, or appropriations records.

Rows:

- Public-law/docket rows: 48.
- Complete docket rows: 19.
- Expected comments counted from Federal Register metadata: 52860.
- Retrieved public comment record metadata rows: 2501.

Retrieval statuses:

- comment_record_api_error: 2
- complete_comment_record_metadata_retrieved: 1
- complete_no_comments_expected: 18
- expected_comment_count_unknown: 3
- partial_comment_record_metadata_api_error: 1
- skipped_high_volume_comment_docket: 23

Claim boundary:

Bounded Regulations.gov comment-record metadata for Federal Register-exposed dockets only; complete rows mean all public comment record metadata returned by the Regulations.gov comments endpoint for a docket within the configured retrieval threshold or no comments expected from Federal Register metadata. This is not comment-text, attachment, commenter-identity, sentiment, Unified Agenda, enforcement, appropriations, implementation-outcome, public benefit, welfare, causal-effect, or model-validation evidence.
