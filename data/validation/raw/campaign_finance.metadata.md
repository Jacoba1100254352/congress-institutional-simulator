# Campaign Finance Raw Validation Dataset

Generated: 2026-07-02T19:15:55+00:00

Source:

- OpenFEC API Schedule A itemized receipts endpoint.
- OpenFEC API Schedule E independent expenditures endpoint.
- API documentation: https://api.open.fec.gov/developers/
- API key: provided API key, not recorded.
- Election cycle: 2024.
- Date filter: 2023-01-01 to 2024-12-31.

Transformation:

- Schedule A rows are limited to non-earmarked individual receipts with positive contribution amounts.
- Schedule E rows are limited to independent-expenditure records with positive expenditure amounts.
- `recipient` is a committee ID for receipts and a candidate ID when available for independent expenditures.
- `industry` is a bounded occupation, employer, expenditure category, or purpose label. It is not a full industry ontology.
- Contributor names, contributor street addresses, and payee names are intentionally omitted from the committed raw file.
- `independent_expenditure` is `1` only for Schedule E rows.

Rows:

- Schedule A rows fetched: 100 across 1 page(s).
- Schedule E rows fetched: 100 across 1 page(s).
- Positive-amount rows skipped: 6.
- Normalized rows: 194.
- Receipt rows: 99.
- Independent-expenditure rows: 95.

Claim boundary:

This file supports a campaign-finance concentration and outside-spending bridge only. It does not validate bill-level influence, sponsor capture, interest-group issue targeting, committee pressure, or causal effects of money on legislative outcomes.
