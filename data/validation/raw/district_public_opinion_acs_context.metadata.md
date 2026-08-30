# District Public-Opinion ACS Context

Generated: 2026-08-30T15:50:59+00:00
Reused existing extract: yes

Sources:

- District queue: `reports/district-public-opinion-source-packets.csv`.
- ACS geography labels: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/Geos20215YR.txt.
- ACS table-based Summary File data directory: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData.

Tables:

- `B02001`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b02001.dat
- `B03003`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b03003.dat
- `B05002`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b05002.dat
- `B16001`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b16001.dat
- `B18101`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b18101.dat
- `B19013`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b19013.dat
- `B21001`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b21001.dat
- `B23025`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b23025.dat
- `B28002`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-b28002.dat
- `C17002`: https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/5YRData/acsdt5y2021-c17002.dat

Transformation:

- Extracts unique sponsor districts from the district public-opinion source-packet queue.
- Joins those districts to 116th congressional-district GEO_IDs in `Geos20215YR.txt`.
- Streams selected ACS detailed-table files and stores only queued district rows.
- Treats Census ACS special numeric estimate/MOE sentinel values as missing numeric fields.
- Preserves estimates and margins of error for selected variables; derived sums use root-sum-square MOE where component MOEs are present.

Rows:

- Retrieved ACS district context rows: 21.
- Total ACS race-table population across retrieved sponsor districts: 16208837.
- Total ACS veteran estimate across retrieved sponsor districts: 787655.
- Total ACS below-poverty estimate across retrieved sponsor districts: 1825862.
- Total ACS noncitizen estimate across retrieved sponsor districts: 1126638.
- Total ACS no-internet-access household estimate across retrieved sponsor districts: 550255.

Claim boundary:

Official ACS 2017-2021 5-year broad congressional-district demographic, economic, language, disability, internet, citizenship, and veteran context only; not bill-topic public support, not MRP or small-area estimates, not bill-text-specific affected-population definitions, not issue-specific affected-group support or harm, not public-benefit evidence, and not model validation.
