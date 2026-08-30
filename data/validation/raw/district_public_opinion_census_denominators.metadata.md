# District Public-Opinion Census Denominators

Generated: 2026-08-30T15:50:58+00:00

Sources:

- District queue: `reports/district-public-opinion-source-packets.csv`.
- Census TIGERweb 116th Congressional District layer: https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Legislative/MapServer/12.

Transformation:

- Extracts unique sponsor districts from the district public-opinion source-packet queue.
- Queries Census TIGERweb Legislative MapServer layer 12 by state FIPS and congressional district basename.
- Preserves 2020 population count, 2020 housing-unit count, land/water area, centroid, and internal point fields.
- Uses the 116th congressional-district layer because the current queue is built from 117th Congress bills, before the 118th/119th post-2020 redistricting frame.
- Does not fetch ACS socioeconomic, veteran, citizenship, language, disability, industry, employment, income, internet-access, survey, or MRP estimates.

Rows:

- Requested sponsor districts: 21.
- Retrieved denominator rows: 21.
- Total represented 2020 population across retrieved sponsor districts: 16319488.
- Total represented 2020 housing units across retrieved sponsor districts: 6876330.
- States represented: 15.

Claim boundary:

Official Census TIGERweb 116th congressional-district 2020 population, housing, and geography denominator only; not ACS socioeconomic or demographic affected-population detail, not bill-topic public support, not MRP or small-area estimates, not issue-specific affected-group support or harm, not public-benefit evidence, and not model validation.
