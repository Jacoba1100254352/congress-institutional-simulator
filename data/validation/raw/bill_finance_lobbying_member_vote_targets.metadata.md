# Bill Finance/Lobbying Member-Vote Target-Scope Cache

Generated: 2026-08-30T15:51:01+00:00

Sources:

- Input roll-call source review: `reports/bill-finance-lobbying-roll-call-source-review.csv`.
- Input campaign target-scope review: `reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv`.
- Input campaign member context: `reports/campaign-finance-member-context.csv`.

Rows:

- Member-vote rows reviewed: 3435.
- Numbered roll calls reviewed: 8.
- Unique voting Bioguide IDs reviewed: 438.
- Floor-action rows without numbered roll calls excluded: 2.
- Rows with same-bill reviewed campaign target Bioguide overlap: 0.
- Rows with broad public FEC candidate/member-context overlap: 40.

Status counts:

- member_vote_overlaps_broad_public_fec_candidate_context_not_current_bill_target: 25
- no_public_fec_campaign_member_target_context_overlap: 2119
- reviewed_same_bill_campaign_target_scope_no_member_vote_overlap: 1291

Claim boundary: Bill finance/lobbying member-vote target-scope review only; rows join official House Clerk member-vote metadata to reviewed public FEC/OpenFEC candidate/member target-scope context by Bioguide where available. The artifact provides vote/member target-scope context only, not lobbying contact confirmation, campaign spending for or against the bill, direct member target documents, roll-call influence, legislative-outcome causality, capture, public benefit, welfare, or model validation.
