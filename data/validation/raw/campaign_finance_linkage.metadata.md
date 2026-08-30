# Campaign Finance Recipient-Metadata Linkage

Generated: 2026-07-05T04:07:20+00:00

Sources:

- https://www.fec.gov/files/bulk-downloads/2024/cm24.zip
- https://www.fec.gov/files/bulk-downloads/2024/cn24.zip
- https://www.fec.gov/files/bulk-downloads/2024/ccl24.zip
- FEC browse-data page: https://www.fec.gov/data/browse-data/

Transformation:

- Reads `data/validation/raw/campaign_finance.csv` and groups rows by `recipient`.
- Matches committee IDs to the FEC committee master file.
- Matches House, Senate, and presidential candidate IDs to the FEC candidate master file.
- Adds candidate-to-committee IDs from the FEC candidate-committee linkage file when available.
- Retains public committee and candidate-office metadata needed for later join design.
- Omits treasurer names, street addresses, contributor names, contributor addresses, payee names, and raw contribution records.

Rows:

- Recipient rows: 32.
- Raw campaign-finance transaction rows represented: 194.
- Transactions with recipient metadata linkage: 192.
- Recipient linkage share: 0.990.

Recipient types:

- candidate: 23
- committee: 9

Linkage statuses:

- candidate_committee_metadata: 21
- committee_candidate_metadata: 1
- committee_metadata: 8
- unmatched: 2

Claim boundary:

This file links the bounded campaign-finance sample to public FEC recipient metadata only. It does not link money to bills, sponsors, member offices, public-opinion issues, committees of jurisdiction, outside-spending targets beyond FEC candidate IDs, or legislative outcomes, and it does not support causal influence or capture claims.
