# Lobbying Issue Linkage

Generated: 2026-07-05T07:37:52+00:00

Sources:

- `data/validation/raw/lobbying_disclosure.csv`
- `data/validation/raw/topic_throughput.csv`
- Senate LDA filings API: https://lda.senate.gov/api/v1/filings/

Transformation:

- Groups cached Senate LDA rows by public issue label.
- Applies a deterministic issue-label to Congress.gov policy-area topic crosswalk.
- Preserves unmatched ambiguous labels rather than inferring hidden topics.
- Attaches topic-throughput aggregate counts when the mapped policy area exists locally.

Issue rows represented: 48

Lobbying rows represented: 146

Lobbying rows with issue-topic context: 144

Linkage statuses:

- issue_topic_crosswalk: 47
- unmatched_issue: 1

Claim boundary: this cache links public LDA issue labels to broad local policy-area topic labels. It does not link lobbying clients to bills, sponsors, committees, roll calls, legislative outcomes, public benefit, welfare, causal capture, or model validation.
