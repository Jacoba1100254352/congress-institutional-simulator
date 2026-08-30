# Campaign-Finance Issue-Context Linkage

Generated: 2026-07-05T12:02:26+00:00

Sources:

- Campaign-finance transaction sample: `data/validation/raw/campaign_finance.csv`.
- FEC recipient metadata cache: `data/validation/raw/campaign_finance_linkage.csv`.
- Local Congress.gov policy-area topic throughput: `data/validation/raw/topic_throughput.csv`.

Transformation:

- Preserves one output row per cached campaign-finance transaction.
- Maps high-confidence occupation, employer, or expenditure-purpose labels to broad policy-area topics using a deterministic local keyword table.
- Requires the mapped topic to exist in the local topic-throughput sample.
- Leaves generic roles, support/oppose flags, unknown labels, and campaign-administrative labels unmapped.
- Adds no contributor names, contributor addresses, payee names, or private contact information.

Rows:

- Campaign-finance transaction rows inspected: 194.
- Rows with bounded issue-topic context: 46.
- Rows left unmapped: 148.
- Unique mapped topics: 8.
- Total amount represented: 1022899.82.
- Amount in mapped issue-topic rows: 2763.72.

Statuses:

- campaign_finance_issue_topic_context: 46
- unmapped_campaign_finance_label: 148

Mapped topics:

- Health: 32
- Transportation and Public Works: 6
- Finance and Financial Sector: 3
- Commerce: 1
- Crime and Law Enforcement: 1
- Education: 1
- Law: 1
- Science, Technology, Communications: 1

Claim boundary:

Bounded public OpenFEC transaction-label to broad policy-topic context only; not bill-level influence, committee jurisdiction, outside-spending target beyond public FEC recipient IDs, legislative outcome, private contributor disclosure, causal capture validation, public benefit, or model validation.
