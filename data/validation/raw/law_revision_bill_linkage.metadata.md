# Law Revision Bill Metadata Linkage

Generated: 2026-07-05T04:33:05+00:00

Source:

- Congress.gov API v3 bill-detail and bill-action endpoints.
- API documentation: https://api.congress.gov/
- Input law-revision file: `data/validation/raw/law_revision_history.csv`.
- Row limit: 40.
- API key: provided key, not recorded.

Transformation:

- Reads public-law rows from the cached law-revision dataset and parses `bill_id` into Congress, bill type, and bill number.
- Fetches Congress.gov bill details and action histories for each unique public-law bill ID.
- Retains bill/action metadata needed for linkage auditing: dates, policy area, sponsor identifiers, action count, and coarse action flags.
- Does not fetch bill text, codified U.S. Code text, OLRC editorial notes, court-review links, implementation records, or Regulations.gov dockets.

Rows:

- Unique public-law bill rows: 40.
- Rows with Congress.gov bill/action metadata: 40.
- Linkage share: 1.000.

Rows by Congress:

- 117: 40

Linkage statuses:

- bill_action_metadata: 40

Claim boundary:

This file links bounded public-law revision proxy rows to official Congress.gov bill/action metadata. It does not provide codified statutory lineage, target-section diffs, observed expiration outcomes, implementation-feedback linkage, or later judicial-invalidation linkage.
