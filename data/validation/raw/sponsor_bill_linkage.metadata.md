# Sponsor-Bill Linkage Raw Dataset

Generated: 2026-07-05

Inputs:

- `data/validation/raw/sponsor_success.csv`
- `data/validation/raw/govinfo_billstatus_linkage.csv`
- `data/validation/raw/law_revision_bill_linkage.csv`

Transformation:

- Joins sponsor aggregate rows to bounded govinfo BILLSTATUS rows by Bioguide sponsor ID.
- Adds public-law bill/action overlap when the same sponsor ID appears in the bounded public-law linkage cache.
- Keeps unmatched sponsor rows in the output so the sponsor denominator remains explicit.

Rows:

- Sponsor rows checked: 22
- Sponsor rows with bill metadata matches: 22
- Unique matched bill IDs: 56
- Matched govinfo bill links attached: 56
- Matched govinfo enacted bill links attached: 0
- Unique matched public laws: 1

Claim boundary:

Bounded sponsor aggregate to public bill-metadata linkage only; not full Center for Effective Lawmaking data, not a complete sponsor history, not bill effectiveness, not legislative quality, not campaign-finance or lobbying influence, not public-opinion, welfare, causal-effect, or model validation evidence.
