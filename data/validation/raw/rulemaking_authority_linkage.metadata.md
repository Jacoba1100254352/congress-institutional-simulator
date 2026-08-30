# Rulemaking Authority Linkage Raw Dataset

Generated: 2026-07-05T09:03:33+00:00

Source:

- Federal Register API v1 document search and single-document endpoints.
- Federal Register full-text text URLs exposed by the single-document endpoint.
- Public-law input file: `data/validation/raw/law_revision_bill_linkage.csv`.

Transformation:

- Reads bounded public-law bill/action rows from the cached Congress.gov linkage file.
- Searches Federal Register rule documents for exact public-law citation forms.
- Fetches matched rule metadata and raw text, then verifies whether the text contains the public-law number.
- Extracts bounded public-law citation lists, U.S. Code citation lists, agencies, CFR references, RINs, dockets, and a short authority-citation excerpt.
- Rows are keyed by public-law number; this is an authority-search bridge, not an exhaustive implementation census.

Rows:

- Public-law rows searched: 40.
- Rows with text-verified Federal Register authority matches: 15.
- Candidate rule documents inspected: 122.
- Text-verified matched rule documents: 51.
- Rows with U.S. Code citations in matched rule text: 15.

Linkage statuses:

- federal_register_authority_match: 15
- no_federal_register_authority_match: 25

Claim boundary:

Bounded Federal Register text search for public-law authority citations only; not proof of exhaustive implementation, proposed-rule history, enforcement outcome, appropriations capacity, complete public-comment record, court review, public benefit, welfare, causal effect, or model validation.
