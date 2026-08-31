# GovInfo Bill Lifecycle Census

- generated_at_utc: 2026-08-31T02:58:15+00:00
- classification_version: `govinfo-bill-lifecycle-v3`
- configuration_sha256: `804bbef440e3929eb3f03b20e313d62ab709ac1e84cd527bd2af84e8a6c5e766`
- builder_sha256: `75587c72a049635cea9c70d7cf48adda1e4f7d0a4e7bc468796ef23f199a0422`
- output_sha256: `422265c48bd344ebd132815f7d711bda9b76ffda7b2d2182d8682ef7fa05e374`
- congress: 116
- bill_types: hr,s
- rows: 14148
- parsed_action_records: 68345
- enacted_rows: 333
- public_law_rows: 333
- private_law_rows: 0
- integrity_valid_rows: 14124
- source_date_anomaly_rows: 24

## Source Archives

| Bill type | URL | Bytes | XML members | SHA-256 | Latest member timestamp | Pin status |
| --- | --- | ---: | ---: | --- | --- | --- |
| `hr` | https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116-hr.zip | 33194205 | 9062 | `b3775e79914a9db29b3a8d55ae13638020c44822dcecb9e4517371e093d01dde` | 2023-12-28T16:44:40+00:00 | matched |
| `s` | https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116-s.zip | 13941002 | 5086 | `e876253f4e3c8b58b28278c8e6e3b901eff0c336b74dfc6e90834d9d3af98132` | 2023-12-28T16:44:48+00:00 | matched |

## Lifecycle Coverage

| Stage | Rows | Share |
| --- | ---: | ---: |
| Referred to committee | 14086 | 0.995618 |
| Committee hearing | 676 | 0.047781 |
| Committee markup | 1297 | 0.091674 |
| Committee ordered reported | 1264 | 0.089341 |
| Committee reported | 1035 | 0.073155 |
| Committee discharged | 540 | 0.038168 |
| Committee advanced | 1488 | 0.105174 |
| Substantive floor consideration | 1048 | 0.074074 |
| Passed origin chamber | 1039 | 0.073438 |
| Completed congressional passage | 334 | 0.023608 |
| Presented to President | 334 | 0.023608 |
| Vetoed | 2 | 0.000141 |
| Veto overridden | 1 | 0.000071 |
| Enacted | 333 | 0.023537 |

## Operational Definitions

- Scope is limited to H.R. and S. measures. Resolutions and joint resolutions are excluded.
- Every direct `bill/actions/item` record is parsed. The committed bill row stores action counts and a canonical action hash; the source XML row stores a byte-level hash.
- Referral, hearing, markup, reporting, discharge, floor consideration, chamber passage, presentment, veto, successful override, and enactment use documented action codes where available and conservative text rules where codes are absent.
- `committee_ordered_reported` records a committee vote or action ordering the measure reported; `committee_reported` requires a report action or report citation. `committee_advanced` means ordered reported, reported, or discharged. None of these fields asserts a hearing, favorable recommendation, or committee influence.
- `floor_considered` means substantive consideration or passage evidence. Administrative receipt, message, calendar, and special-rule actions alone do not satisfy it.
- `completed_congressional_passage` requires presentment, final chamber agreement, a second-chamber passage without amendment, or enactment. Separate chamber passage flags can describe passage of nonidentical versions and are not alone treated as completed passage.
- `veto_overridden` requires affirmative House and Senate override evidence. A vetoed enacted bill without both chamber stages fails the integrity audit.
- Missing explicit intermediate records may be conservatively inferred from completed passage or enactment; each inferred field carries an `inferred_from:` basis and may have only the downstream date.
- The GPO guide states that no complete authoritative action-code list exists and that action type values are processing categories. Therefore every stage remains an operational classification, not an official legal-status determination.

Official format guide: https://github.com/usgpo/bill-status/blob/main/BILLSTATUS-XML_User_User-Guide.md

Claim boundary: Complete GovInfo BILLSTATUS bill/action coverage for H.R. and S. measures in Congress 116, with conservative operational lifecycle stages. This is descriptive legislative-flow evidence, not causal model validation, public-opinion evidence, public benefit, welfare, or institutional ranking.
