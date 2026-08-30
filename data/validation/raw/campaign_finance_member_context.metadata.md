# Campaign-Finance Member-Context Linkage

Generated: 2026-07-05T08:09:32+00:00

Sources:

- FEC recipient metadata cache: `data/validation/raw/campaign_finance_linkage.csv`.
- Voteview member-context cache: `data/validation/raw/voteview_member_context.csv`.
- Voteview member source URLs are retained row-by-row from the member-context cache.

Transformation:

- Reads public FEC recipient/candidate metadata and Voteview member metadata.
- For House candidates, requires matching chamber, state, district, last name, and compatible first name or initial.
- For Senate candidates, requires matching chamber, state, last name, and compatible first name or initial.
- Leaves challengers, presidential candidates, noncandidate committees, and ambiguous rows unmatched.
- Does not infer identity from district alone.

Rows:

- Recipient rows inspected: 32.
- Candidate metadata rows inspected: 24.
- Candidate rows with Voteview member context: 15.
- Campaign-finance transaction rows with Voteview member context: 30.
- Unique Voteview/Bioguide members linked: 15.

Rows by member-context status:

- candidate_metadata_noncongressional_office: 4
- candidate_voteview_member_context: 15
- candidate_without_voteview_member_match: 5
- recipient_without_candidate_metadata: 8

Claim boundary:

Bounded public FEC candidate/committee recipient to Voteview member-context inventory only; not bill-level influence, sponsor effectiveness, committee jurisdiction, issue targeting, private contributor disclosure, causal capture validation, public benefit, or model validation.
