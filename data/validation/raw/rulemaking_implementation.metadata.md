# Rulemaking Implementation Raw Validation Dataset

Generated: 2026-07-02T18:50:46+00:00

Source:

- Federal Register API v1 document search endpoint.
- API documentation: https://www.federalregister.gov/developers/documentation/api/v1
- Query: final rules (`conditions[type][]=RULE`), non-corrections, newest first.
- Publication date range: 2026-01-01 to 2026-07-02.

Transformation:

- `law_id` is the Federal Register document number.
- `final_rule_date` is the Federal Register publication date.
- `effective_date` is the API `effective_on` field when available.
- `enforcement_capacity` is a coarse implementation-speed proxy derived from final-to-effective delay: 1.00 for 0-30 days, 0.75 for 31-90 days, 0.50 for 91-180 days or missing dates, and 0.25 for longer delays.
- `proposed_rule_date` is blank because the document search response does not reliably link final rules to earlier proposed-rule publications.
- `comment_count` is blank because the Federal Register document-search response used for this raw extract does not provide Regulations.gov comment totals; use `rulemaking_implementation_linkage.csv` for Federal Register-exposed docket and comment-count metadata.
- `nonenforced` and `underfunded` are fixed at 0 because this source does not observe enforcement failure or appropriations capacity.

Rows:

- Normalized rows: 500
- Rows with effective date: 442

Claim boundary:

This file supports a final-rule implementation-delay bridge from Federal Register publication to effective date. It does not validate public comments, enforcement capacity, nonenforcement, underfunding, or proposed-to-final rulemaking duration.
