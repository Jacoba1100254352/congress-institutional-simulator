# Rulemaking Comment Metadata

Generated: 2026-07-05T20:36:30+00:00

Source:

- Federal Register API v1 single-document endpoint.
- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api
- Input history linkage file: `data/validation/raw/rulemaking_history_linkage.csv`.
- Row limit: all rulemaking history rows.
- API key required: no.

Transformation:

- Starts from authority-matched final-rule rows in the rulemaking history cache.
- Refetches each final-rule Federal Register detail record.
- Refetches matched proposed-rule Federal Register detail records already retained by shared RIN or docket identifiers.
- Extracts only Federal Register-exposed Regulations.gov docket, comment URL, comment-count, and comment-close metadata.
- Does not fetch complete Regulations.gov comment records, commenter identities, comment text, Unified Agenda stages, enforcement outcomes, appropriations data, or nonpublic submitter information.

Rows:

- Authority-matched final-rule rows reviewed: 51.
- Rows with final Federal Register detail fetched: 51.
- Rows with final Regulations.gov docket metadata: 45.
- Rows with final comments-count metadata: 51.
- Rows with final positive comments counts: 14.
- Rows with proposed-rule Regulations.gov docket metadata: 19.
- Rows with proposed-rule comment URLs: 19.
- Rows with proposed-rule comments-count metadata: 23.
- Rows with proposed-rule positive comments counts: 18.
- Proposed-rule comments counted in exposed metadata: 25816.

Comment metadata statuses:

- final_and_proposed_comment_metadata: 23
- final_comment_metadata_only: 28

Claim boundary:

Bounded Federal Register-exposed Regulations.gov metadata for authority-matched final-rule and matched proposed-rule records only; this is not complete Regulations.gov comment-record evidence, commenter identity or comment-text evidence, Unified Agenda stage coverage, enforcement outcomes, appropriations capacity, exhaustive implementation coverage, public benefit, welfare, causal effects, or model validation.
