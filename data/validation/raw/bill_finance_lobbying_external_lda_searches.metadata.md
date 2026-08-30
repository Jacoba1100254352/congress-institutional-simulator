# Bill Finance/Lobbying External LDA Search Cache

Generated: 2026-07-26T20:30:21+00:00

Source:

- U.S. Senate LDA API filings endpoint: https://lda.gov/api/v1/filings/
- API documentation: https://lda.gov/api/redoc/v1/

Scope:

- Queued bill-finance/lobbying public-law rows searched: 10.
- LDA term/year query rows: 30.
- Deduplicated exact activity-text current-bill mention rows: 55.
- Queued bills with exact LDA activity-text current-bill mentions: 2.
- Page size: 25.
- Max pages per query: 10.
- Term variants: compact,dotted.
- Sleep seconds between API requests: 4.2.

API status counts:

- ok: 30

Claim boundary: Official LDA external current-bill search only; exact filing activity-text bill-number mentions identify disclosed lobbying activity mentioning the reviewed bill, not support, opposition, sponsor/member targeting, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, welfare, causal capture, or model validation.
