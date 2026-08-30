# Bill Finance/Lobbying Roll-Call Source Cache

Generated: 2026-07-27T06:28:37+00:00

Sources:

- Input source review: `reports/bill-finance-lobbying-committee-action-source-review.csv`.
- House Clerk XML pattern: `https://clerk.house.gov/evs/<year>/roll<roll-number>.xml`.

Rows:

- Source-review rows inspected: 10.
- Official House Clerk roll-call XML rows fetched: 8.
- Floor-action rows without numbered roll-call references: 2.
- Member vote rows represented: 3435.

Status counts:

- official_floor_action_reviewed_without_numbered_roll_call: 2
- official_house_clerk_roll_call_source_reviewed: 8

Claim boundary: Bill finance/lobbying roll-call source review only; rows cache official House Clerk roll-call metadata and member-vote row counts when govinfo BILLSTATUS action text exposes a numbered House roll call, or classify floor actions without a numbered roll-call reference. The artifact provides vote-source context, not member-position influence, lobbying contact confirmation, campaign-finance target evidence, roll-call influence, legislative-outcome causality, public benefit, welfare, causal capture, or model validation.
