# Campaign-Finance Sponsor-Bill Context

This report derives a bounded candidate-to-sponsored-bill context join from cached public FEC recipient/member context and cached govinfo BILLSTATUS sponsor metadata. It is a metadata inventory, not campaign-finance influence validation.

- FEC candidate rows with Voteview member context inspected: 15
- Candidate/member rows with sponsored-bill context: 3
- Campaign-finance transaction rows with sponsored-bill context: 3
- Unique Bioguide members with sponsored-bill context: 3
- Unique matched bill IDs: 9
- Unique enacted matched bill IDs: 0
- Unique matched policy areas: 8

Claim boundary: Bounded public FEC candidate/member context joined by Bioguide ID to cached govinfo sponsored-bill metadata only; not evidence that contributions, spending, candidates, or committees funded, caused, influenced, targeted, or benefited any bill, committee decision, public law, implementation outcome, public benefit, causal capture, private contributor disclosure, or model validation.

Sponsor-bill context statuses:
- candidate_sponsored_bill_context: 3

| Recipient | Candidate/member | Transactions | Matched bills | Enacted bills | Policy areas | Missing links |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `S2TX00312` | CRUZ, RAFAEL EDWARD TED / CRUZ, Rafael Edward (Ted) (`C001098`) | 1 | 6 | 0 | Government Operations and Politics; Armed Forces and National Security; Taxation | bill_specific_finance_or_lobbying_influence; committee_action_influence; reviewed_outside_spending_target; private_contributor_disclosure; legislative_outcome_causality; public_benefit_or_welfare_validation; causal_influence_or_capture_validation |
| `H0IL15129` | MILLER, MARY / MILLER, Mary E. (`M001211`) | 1 | 1 | 0 | Civil Rights and Liberties, Minority Issues | bill_specific_finance_or_lobbying_influence; committee_action_influence; reviewed_outside_spending_target; private_contributor_disclosure; legislative_outcome_causality; public_benefit_or_welfare_validation; causal_influence_or_capture_validation |
| `S8FL00273` | SCOTT, RICK SEN / SCOTT, Richard Lynn (Rick) (`S001217`) | 1 | 2 | 0 | Congress; Economics and Public Finance | bill_specific_finance_or_lobbying_influence; committee_action_influence; reviewed_outside_spending_target; private_contributor_disclosure; legislative_outcome_causality; public_benefit_or_welfare_validation; causal_influence_or_capture_validation |
