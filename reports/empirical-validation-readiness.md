# Empirical Validation Readiness

This report checks whether optional raw empirical inputs are present and shaped for future validation. It is a readiness check, not a validation result. Adapter fixtures under `data/validation/fixtures/` are intentionally ignored.

| Dataset | Purpose | Status | Missing columns |
| --- | --- | --- | --- |
| `voteview_rollcalls.csv` | party unity, coalition size, and ideological voting checks | missing | all |
| `bill_progression.csv` | bill attrition, floor load, and enactment-rate checks | ready | none |
| `lobbying_disclosure.csv` | lobby spending distribution and issue-pressure checks | missing | all |
| `topic_throughput.csv` | topic-level throughput and agenda distribution checks | missing | all |
| `sponsor_success.csv` | sponsor success and proposal-access concentration checks | missing | all |
| `district_public_opinion.csv` | district-level public will, issue intensity, turnout, and affected-group checks | missing | all |
| `committee_activity.csv` | committee referral, hearing, reporting, amendment, and discharge checks | missing | all |
| `campaign_finance.csv` | campaign-finance and outside-spending influence checks | missing | all |
| `court_review.csv` | constitutional review, emergency docket, signed-opinion, and invalidation checks | missing | all |
| `rulemaking_implementation.csv` | post-enactment implementation delay, enforcement capacity, comment, and nonenforcement checks | missing | all |
| `law_revision_history.csv` | post-enactment amendment, reauthorization, repeal, expiration, and invalidation checks | missing | all |
| `comparative_institutions.csv` | cross-national chamber, court, party-system, and productivity checks | missing | all |

- Files present: 1 / 12
- Files with required columns: 1 / 12
- Adapter fixture CSVs ignored: 4

Next empirical step: add curated raw files and document source-specific transformations. The adapters now cover roll calls, bill progress, lobbying, topics, sponsor success, district opinion, committee activity, campaign finance, court review, post-enactment implementation, law revision, and comparative institutions.
