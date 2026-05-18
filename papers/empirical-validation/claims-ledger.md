# Claims Ledger

| Claim | Supporting evidence currently available | Limitation | Citation needed |
|---|---|---|---|
| The project has empirical flow sanity checks for the conventional benchmark. | `reports/calibration-baseline.md` reports 7/7 checks passed. | These are not validation of the main synthetic metrics. | Legislative productivity and flow measurement. |
| Current empirical samples include bill progression, roll calls, lobbying, topics, sponsors, and committee summaries. | `reports/core-raw-validation-build.md`; `reports/empirical-bridge.csv`. | Samples are small and not enough for held-out validation. | Congress.gov, Voteview, LDA, and related data-source documentation. |
| Current checks do not validate public benefit, revision moderation, harm, capture, or public support. | `reports/empirical-validation-gap-report.md`; ACM paper caveats. | This limitation prevents a validation paper now. | Simulation validation and empirical measurement literature. |
| A validation paper would need separate calibration, plausibility screening, and prediction. | Methodological need identified in reviews and current paper scope. | No implemented train/test validation workflow yet. | Model validation in agent-based and computational social science. |
| Cross-national and implementation datasets would broaden validation. | Gap report names missing areas. | No data integration or mapping currently exists. | Comparative institutions, implementation feedback, law revision, court review. |
| Empirical coalition size and party unity are not public opinion. | `reports/empirical-bridge.csv` proxy mappings; current caveats. | Must avoid treating legislative coalitions as public-support validation. | Representation and public-opinion measurement. |
