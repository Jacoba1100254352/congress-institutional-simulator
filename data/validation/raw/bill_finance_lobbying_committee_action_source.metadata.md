# Bill Finance/Lobbying Committee-Action Source Cache

Generated: 2026-07-27T06:57:38+00:00

Sources:

- Input queue context: `reports/bill-finance-lobbying-committee-action-context.csv`.
- govinfo BILLSTATUS bulk XML URL pattern: `https://www.govinfo.gov/bulkdata/BILLSTATUS/<congress>/<bill_type>/BILLSTATUS-<congress><bill_type><bill_number>.xml`.
- govinfo BILLSTATUS feature page: `https://www.govinfo.gov/features/bill-status-xml-bulk-data`.

Transformation:

- Fetches one public govinfo BILLSTATUS XML record per queued finance/lobbying bill.
- Joins records only by congress, bill type, and bill number parsed from local bill_id.
- Extracts official committee names, committee activities, committee report citations, bounded action snippets, roll-call references when exposed in action text, and public-law outcome metadata.
- Preserves finance/lobbying influence, roll-call influence, outcome-causality, welfare, capture, and model-validation gaps as explicit missing links.

Rows:

- Queue rows inspected: 10.
- Rows with govinfo BILLSTATUS fetched: 10.
- Rows with official committee names: 9.
- Rows source-reviewed without direct committee names: 1.
- Rows with committee action snippets: 9.
- Rows source-reviewed without direct committee action records: 1.
- Rows with floor action snippets: 10.
- Rows with roll-call references in BILLSTATUS action text: 8.

Status counts:

- official_govinfo_billstatus_fetched: 10

Claim boundary: Bill finance/lobbying committee/action source review only; rows cache official govinfo BILLSTATUS committee, action, roll-call-reference, and public-law outcome metadata for queued bills. The artifact provides committee/action source context, not lobbying contact confirmation, campaign-finance target evidence, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, welfare, causal capture, or model validation.
