# Empirical Validation Readiness

This report checks whether optional raw empirical inputs are present and shaped for future validation. It is a readiness check, not a validation result.

| Dataset | Purpose | Status | Missing columns |
| --- | --- | --- | --- |
| `voteview_rollcalls.csv` | party unity, coalition size, and ideological voting checks | missing | all |
| `bill_progression.csv` | bill attrition, floor load, and enactment-rate checks | missing | all |
| `lobbying_disclosure.csv` | lobby spending distribution and issue-pressure checks | missing | all |
| `topic_throughput.csv` | topic-level throughput and agenda distribution checks | missing | all |
| `sponsor_success.csv` | sponsor success and proposal-access concentration checks | missing | all |

- Files present: 0 / 5
- Files with required columns: 0 / 5

Next empirical step: add dataset-specific adapters that compute target distributions and compare them to simulator outputs with documented tolerances.
