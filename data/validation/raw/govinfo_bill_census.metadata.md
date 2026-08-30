# GovInfo Bill Lifecycle Census

- generated_at_utc: 2026-08-30T22:39:15+00:00
- classification_version: `govinfo-bill-lifecycle-v1`
- configuration_sha256: `b2412df0b02e75fbcb6203a18201592991483043d773fc619662f78aeb4aa416`
- builder_sha256: `8b764e3d4577190a1da15b865911ca8191337415774a968df41662cc42c3b7fa`
- output_sha256: `8e43e521148f113e95a2040ec592d7c5470c6303676a534f3d272497cc7bea36`
- congress: 117
- bill_types: hr,s
- rows: 15066
- parsed_action_records: 72047
- enacted_rows: 358
- public_law_rows: 355
- private_law_rows: 3
- integrity_valid_rows: 15061
- source_date_anomaly_rows: 5

## Source Archives

| Bill type | URL | Bytes | XML members | SHA-256 | Latest member timestamp | Pin status |
| --- | --- | ---: | ---: | --- | --- | --- |
| `hr` | https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117-hr.zip | 33733417 | 9709 | `658b2d280e4e7972c86bfd810ebff0c9bb61c115b242de8c8774034dea08de03` | 2024-06-11T13:16:50+00:00 | matched |
| `s` | https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117-s.zip | 14088276 | 5357 | `69561f19333de31afd2e288700757f3794ecffa35287b9fb86bb2d5d313a1294` | 2023-12-24T06:59:16+00:00 | matched |

## Lifecycle Coverage

| Stage | Rows | Share |
| --- | ---: | ---: |
| Referred to committee | 14959 | 0.992898 |
| Committee hearing | 790 | 0.052436 |
| Committee markup | 1347 | 0.089407 |
| Committee ordered reported | 1347 | 0.089407 |
| Committee reported | 967 | 0.064184 |
| Committee discharged | 573 | 0.038033 |
| Committee advanced | 1511 | 0.100292 |
| Substantive floor consideration | 1003 | 0.066574 |
| Passed origin chamber | 991 | 0.065777 |
| Completed congressional passage | 358 | 0.023762 |
| Presented to President | 358 | 0.023762 |
| Vetoed | 0 | 0.000000 |
| Enacted | 358 | 0.023762 |

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

Claim boundary: Complete GovInfo BILLSTATUS bill/action coverage for H.R. and S. measures in the 117th Congress, with conservative operational lifecycle stages. This is descriptive legislative-flow evidence, not causal model validation, public-opinion evidence, public benefit, welfare, or institutional ranking.
