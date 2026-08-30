# Voteview Member Metadata Context

Generated: 2026-07-05T06:41:09+00:00

Sources:

- https://voteview.com/static/data/out/members/HS118_members.csv
- Voteview data page: https://voteview.com/data

Transformation:

- Reads the cached `voteview_rollcalls.csv` sample.
- Downloads the matching Voteview HS member CSV for each Congress in that sample.
- Joins roll-call member rows to Voteview member metadata by congress, chamber, and ICPSR ID.
- Retains Bioguide ID, state, district, party, and ideal-point fields needed for later member-level linkage design.
- Does not join roll calls to bills, public laws, sponsor histories, public-opinion rows, or legislative outcomes.

Rows:

- Member-context rows: 541.
- Raw roll-call member-vote rows represented: 83636.
- Roll-call rows with Bioguide member metadata: 83636.

Linkage statuses:

- voteview_member_metadata: 541

Claim boundary:

Voteview member metadata context only; not roll-call-to-bill linkage, district public-opinion representation, sponsor effectiveness, public benefit, welfare, or model validation.
