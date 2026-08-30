# District Public Opinion Raw Validation Dataset

Generated: 2026-07-02T20:43:20+00:00

Source:

- Cumulative CES Common Content, Harvard Dataverse DOI 10.7910/DVN/II2DB6.
- Dataset version: 11.0.
- Distribution date: 2025-10-08.
- License: CC0 1.0.
- Source file: cumulative_2006-2024.feather (Dataverse file id 12134962).
- Source cache path: no-include/validation-cache/ces/cumulative_2006-2024.feather.

Transformation:

- Filtered to survey year 2024.
- District-issue rows are retained only when at least 30 respondents answered the issue signal.
- Unit of observation is district issue.
- District ID is the CES `cd` congressional-district identifier.
- `support` is a weighted district share for one of three survey-derived signals: own House representative approval, Democratic presidential preference, or Democratic House preference.
- `intensity` is the weighted strong-opinion share for representative approval and the weighted major-party response share for the two preference rows.
- `turnout` is the weighted self-reported post-election turnout share where available, with pre-election turnout intent as fallback.
- `affected_group_share` is the weighted uninsured share from `no_healthins`; it is a generic district vulnerability proxy and not issue-specific affected-population mapping.

Rows:

- Normalized district-issue rows: 1305
- Districts represented: 436
- house_democratic_preference: 436 rows
- house_representative_approval: 433 rows
- presidential_democratic_preference: 436 rows

Claim boundary:

This file supports a bounded district-level public-opinion and turnout proxy. It is a direct aggregation of CES survey responses, not an MRP estimate, not bill-topic support, not issue-specific affected-group measurement, and not validation of generated public benefit or harm.
