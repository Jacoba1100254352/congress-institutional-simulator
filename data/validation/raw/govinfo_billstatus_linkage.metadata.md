# govinfo BILLSTATUS Linkage Cache

Generated: 2026-07-05T08:32:28+00:00

Sources:

- Input bill sample: `data/validation/raw/bill_progression.csv`.
- govinfo BILLSTATUS bulk XML URL pattern: `https://www.govinfo.gov/bulkdata/BILLSTATUS/<congress>/<bill_type>/BILLSTATUS-<congress><bill_type><bill_number>.xml`.
- govinfo BILLSTATUS feature page: `https://www.govinfo.gov/features/bill-status-xml-bulk-data`.

Transformation:

- Fetches one public govinfo BILLSTATUS XML record per cached bill-progression row.
- Joins records only by congress, bill type, and bill number.
- Extracts bill identifiers, titles, policy area, actions, committees, subjects, sponsor metadata, and coarse action-stage flags.
- Compares coarse govinfo action flags and policy area to the cached Congress.gov bill-progression sample.

Rows:

- Bill rows inspected: 180.
- Rows with govinfo BILLSTATUS metadata: 180.
- Rows with aligned coarse action flags: 180.
- Rows with aligned policy area: 180.

Rows by linkage status:

- govinfo_billstatus_metadata: 180

Claim boundary:

Bounded govinfo BILLSTATUS to Congress.gov bill-sample cross-check only; not a full bill census, public-opinion evidence, lobbying or campaign-finance influence, implementation or court outcome linkage, public benefit, welfare, or model validation.
