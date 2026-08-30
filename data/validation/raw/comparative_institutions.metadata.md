# Comparative Institutions Raw Validation Dataset

Generated: 2026-07-02T21:09:50+00:00

Sources:

- QoG Data Finder selected-variable CSV endpoint for `gol_adm`, `gol_enpp`, `h_l1`, and `h_l2`.
- Democratic Electoral Systems 1919-2020 dataset via QoG for lower-house district magnitude and effective number of legislative parties.
- Henisz POLCON dataset via QoG for effective first and second legislative chamber indicators.
- Our World in Data/V-Dem judicial constraints on the executive index (`v2x_jucon`).
- Our World in Data/V-Dem legislative constraints on the executive index (`v2xlg_legcon`).

Source URLs:

- QoG selected CSV: https://datafinder.qog.gu.se/data_generator?download=gol_adm,gol_enpp,h_l1,h_l2&type=csv
- DES metadata: https://datafinder.qog.gu.se/dataset/gol
- POLCON metadata: https://datafinder.qog.gu.se/dataset/h
- OWID/V-Dem judicial constraints: https://ourworldindata.org/grapher/judicial-constraints-on-the-executive-index
- OWID/V-Dem legislative constraints: https://ourworldindata.org/grapher/legislative-constraints-on-the-executive-index
- V-Dem dataset page: https://www.v-dem.net/data/the-v-dem-dataset/

Transformation:

- Source year window requested: 2010-2020.
- Output mode: latest complete country-year per ISO3 country.
- `chambers` is encoded as 1 plus `h_l2` when `h_l1` indicates an effective lower chamber; otherwise it is 0.
- `district_magnitude` is QoG/DES `gol_adm`.
- `party_fragmentation` is QoG/DES `gol_enpp`, the effective number of parliamentary or legislative parties.
- `judicial_review` is OWID/V-Dem `v2x_jucon`, a 0-1 judicial-constraints index.
- `legislative_productivity` is OWID/V-Dem `v2xlg_legcon`, a 0-1 legislative-constraints and oversight index. The column name is kept for schema compatibility; it is not observed law-output productivity.

Rows:

- QoG source rows read: 11101
- Complete QoG rows in window: 856
- Normalized rows written: 130
- Countries represented: 130
- Output year range: 2011-2020
- Skipped outside requested window: 9197
- Skipped for missing QoG fields: 1048
- Skipped for missing ISO3 code: 0
- Skipped for missing OWID/V-Dem judicial index: 78
- Skipped for missing OWID/V-Dem legislative index: 0

Claim boundary:

This file supports a bounded comparative-institution profile for chamber structure, district magnitude, judicial constraints, party fragmentation, and legislative-constraint proxies. It does not validate comparative institutional fit, bicameral disagreement, chamber-specific representation, law-output productivity, or country-level adoption claims.
