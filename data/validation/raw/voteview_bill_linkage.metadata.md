# Voteview Roll-Call Bill Linkage Context

Generated: 2026-07-05T07:05:00+00:00

Sources:

- https://voteview.com/static/data/out/rollcalls/HS118_rollcalls.csv
- Voteview data page: https://voteview.com/data
- Cached roll-call rows: data/validation/raw/voteview_rollcalls.csv
- Optional Congress.gov bill sample: data/validation/raw/bill_progression.csv
- Optional public-law bill metadata cache: data/validation/raw/law_revision_bill_linkage.csv

Transformation:

- Reads the cached `voteview_rollcalls.csv` member-vote sample.
- Downloads the matching Voteview HS roll-call metadata CSV for each Congress in that sample.
- Joins sampled vote IDs to roll-call metadata by congress, chamber, and roll number.
- Normalizes Voteview bill numbers into bounded `congress-bill_type-number` bill IDs when possible.
- Flags whether normalized bill IDs overlap the cached Congress.gov bill-progression sample or public-law bill metadata cache.
- Preserves member-vote row counts for each roll call but does not infer public support or bill outcomes.

Rows:

- Voteview roll-call metadata rows represented: 320.
- Raw roll-call member-vote rows represented: 83636.
- Voteview roll-call metadata rows with normalized bill IDs: 193.
- Member-vote rows on roll calls with normalized bill IDs: 64894.
- Voteview roll-call metadata rows matching cached bill progression rows: 8.
- Member-vote rows matching cached bill progression rows: 3075.

Bill match statuses:

- bill_progression_metadata: 8
- missing_bill_number: 19
- nomination_or_nonbill_vote: 108
- voteview_bill_number_only: 185

Claim boundary:

Voteview roll-call bill metadata context only; bill-number parsing and bounded Congress.gov sample overlap do not establish public-opinion representation, sponsor effectiveness, public benefit, welfare, causal influence, or model validation.
