# District Public Opinion CES Source Freshness

This report compares the cached district public-opinion raw-source metadata to the live Harvard Dataverse metadata for the Cumulative CES Common Content dataset.

- Audit generated: 2026-07-27T00:35:53Z
- Source family: District public opinion and affected groups
- Dataset DOI: 10.7910/DVN/II2DB6
- Official latest version: 12.0
- Official release time: 2026-07-14T14:49:08Z
- Local cached metadata version: 11.0
- Local cached source file: `cumulative_2006-2024.feather`
- Local extract year: 2024
- Freshness status: `official_ces_source_newer_than_cached_extract` (stale relative to the official latest CES distribution)

The local district public-opinion extract remains a bounded 2024 direct-aggregation snapshot until it is rebuilt from the current official distribution. This source-freshness audit is intentionally separate from the offline paper checks because it depends on live Dataverse metadata.

## Official Files

| Role | File | File id | Size bytes | MD5 |
| --- | --- | --- | ---: | --- |
| current_distribution_file | `cumulative_2006-2025.dta` | 14076515 | 724803550 | `73eeb2933cc0c84ccfbbdacdcd227939` |
| preferred_current_microdata_file | `cumulative_2006-2025.feather` | 14076522 | 143996970 | `f6dc08617b87949433dea7e74a251ef9` |
| current_distribution_file | `cumulative_2006-2025.rds` | 14076530 | 40503900 | `e96ff7c785ffd4f58eaa3e9a6e09b193` |
| current_guide_pdf | `guide_cumulative_2006-2025.pdf` | 14076560 | 131598 | `526b30decd01a4edfed88640b2c80f65` |

## Action Required

Refresh district_public_opinion.csv from the latest Cumulative CES distribution after optional Feather/Stata tooling is available, then rerun the district linkage, policy-context, bill-topic readiness, source-packet, Census, ACS, survey-source crosswalk, raw-source manifest, and empirical-boundary reports before treating the public-opinion cache as current.

## Claim Boundary

Source freshness audit only. It does not acquire survey item IDs, estimate bill-topic public support, build MRP/small-area estimates, define bill-text-specific affected populations, measure affected-group support or harm, or validate public benefit.

## Source URLs

- https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/II2DB6
- https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/II2DB6
- https://tischcollege.tufts.edu/research-faculty/research-centers/cooperative-election-study/data-downloads
