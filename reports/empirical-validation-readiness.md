# Empirical Validation Readiness

This report checks whether optional raw empirical inputs are present and shaped for future validation. It is a readiness check, not a validation result. Adapter fixtures under `data/validation/fixtures/` are intentionally ignored.

| Dataset | Purpose | Status | Missing columns |
| --- | --- | --- | --- |
| `voteview_rollcalls.csv` | party unity, coalition size, and ideological voting checks | ready | none |
| `bill_progression.csv` | bounded Congress.gov bill-flow and independent source-cross-check rows | ready | none |
| `govinfo_bill_census_116.csv` | complete 116th-Congress no-refit temporal bill-lifecycle backcast | ready | none |
| `govinfo_bill_census.csv` | 117th-Congress calibration and within-Congress bill-lifecycle checks | ready | none |
| `govinfo_bill_census_118.csv` | complete 118th-Congress no-refit temporal bill-lifecycle test | ready | none |
| `lobbying_disclosure.csv` | lobby spending distribution and issue-pressure checks | ready | none |
| `topic_throughput.csv` | topic-level throughput and agenda distribution checks | ready | none |
| `sponsor_success.csv` | sponsor success and proposal-access concentration checks | ready | none |
| `district_public_opinion.csv` | district-level public will, issue intensity, turnout, and affected-group checks | ready | none |
| `committee_activity.csv` | committee referral, hearing, reporting, amendment, and discharge checks | ready | none |
| `campaign_finance.csv` | campaign-finance and outside-spending influence checks | ready | none |
| `court_review.csv` | constitutional review, emergency docket, signed-opinion, and invalidation checks | ready | none |
| `rulemaking_implementation.csv` | post-enactment implementation delay, enforcement capacity, comment, and nonenforcement checks | ready | none |
| `law_revision_history.csv` | law revision text flags and optional invalidation-linkage checks | ready | none |
| `comparative_institutions.csv` | cross-national chamber, court, party-system, and legislative-capacity checks | ready | none |

- Files present: 15 / 15
- Files with required columns: 15 / 15
- Adapter fixture CSVs ignored: 4

Next empirical step: extend mechanism-specific agenda and executive-action evidence beyond aggregate lifecycle rates while continuing to upgrade bounded source-family checks into linked bill-topic, sponsor, finance, implementation, court, and statutory-lineage evidence. The configured datasets cover roll calls, bounded Congress.gov bill progress, three complete GovInfo bill censuses, lobbying, topics, sponsor success, district opinion, committee activity, campaign finance, court review, post-enactment implementation, law revision, and comparative institutions.
