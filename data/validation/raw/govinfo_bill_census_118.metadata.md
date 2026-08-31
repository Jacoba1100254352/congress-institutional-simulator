# GovInfo Bill Lifecycle Census

- generated_at_utc: 2026-08-30T23:31:55+00:00
- classification_version: `govinfo-bill-lifecycle-v2`
- configuration_sha256: `ab264648aab606148d408cbf33b7ae77b293688746c1c492280e66f8b08b1c04`
- builder_sha256: `0f195c23faac0e0bcacb9d5fcd80ab240f33e44749ab10155bc509e8bf8904be`
- output_sha256: `b5d89515836e7209b6ef0d1d12b86627ebe2b2e6c8914a28a4994ae32278359b`
- congress: 118
- bill_types: hr,s
- rows: 16213
- parsed_action_records: 75239
- enacted_rows: 269
- public_law_rows: 269
- private_law_rows: 0
- integrity_valid_rows: 16193
- source_date_anomaly_rows: 20

## Source Archives

| Bill type | URL | Bytes | XML members | SHA-256 | Latest member timestamp | Pin status |
| --- | --- | ---: | ---: | --- | --- | --- |
| `hr` | https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118-hr.zip | 35522726 | 10564 | `8e7ca7dab50a7b9b977f021ec1b3231f8fedf82c33494553857b892fadfdba98` | 2026-05-15T20:20:26+00:00 | matched |
| `s` | https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118-s.zip | 14410894 | 5649 | `269261c0989db3ced789680ee2202747df9a7298f1ac8d2b074d3356b06e399c` | 2026-05-15T20:20:32+00:00 | matched |

## Lifecycle Coverage

| Stage | Rows | Share |
| --- | ---: | ---: |
| Referred to committee | 16155 | 0.996423 |
| Committee hearing | 664 | 0.040955 |
| Committee markup | 1683 | 0.103806 |
| Committee ordered reported | 1677 | 0.103436 |
| Committee reported | 1426 | 0.087954 |
| Committee discharged | 510 | 0.031456 |
| Committee advanced | 1843 | 0.113674 |
| Substantive floor consideration | 957 | 0.059027 |
| Passed origin chamber | 935 | 0.057670 |
| Completed congressional passage | 270 | 0.016653 |
| Presented to President | 270 | 0.016653 |
| Vetoed | 1 | 0.000062 |
| Enacted | 269 | 0.016592 |

## Operational Definitions

- Scope is limited to H.R. and S. measures. Resolutions and joint resolutions are excluded.
- Every direct `bill/actions/item` record is parsed. The committed bill row stores action counts and a canonical action hash; the source XML row stores a byte-level hash.
- Referral, hearing, markup, reporting, discharge, floor consideration, chamber passage, presentment, veto, and enactment use documented action codes where available and conservative text rules where codes are absent.
- `committee_ordered_reported` records a committee vote or action ordering the measure reported; `committee_reported` requires a report action or report citation. `committee_advanced` means ordered reported, reported, or discharged. None of these fields asserts a hearing, favorable recommendation, or committee influence.
- `floor_considered` means substantive consideration or passage evidence. Administrative receipt, message, calendar, and special-rule actions alone do not satisfy it.
- `completed_congressional_passage` requires presentment, final chamber agreement, a second-chamber passage without amendment, or enactment. Separate chamber passage flags can describe passage of nonidentical versions and are not alone treated as completed passage.
- Missing explicit intermediate records may be conservatively inferred from completed passage or enactment; each inferred field carries an `inferred_from:` basis and may have only the downstream date.
- The GPO guide states that no complete authoritative action-code list exists and that action type values are processing categories. Therefore every stage remains an operational classification, not an official legal-status determination.

Official format guide: https://github.com/usgpo/bill-status/blob/main/BILLSTATUS-XML_User_User-Guide.md

Claim boundary: Complete GovInfo BILLSTATUS bill/action coverage for H.R. and S. measures in Congress 118, with conservative operational lifecycle stages. This is descriptive legislative-flow evidence, not causal model validation, public-opinion evidence, public benefit, welfare, or institutional ranking.
