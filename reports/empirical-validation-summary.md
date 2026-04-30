# Empirical Validation Summary

This report computes validation summaries when optional raw datasets are present under `data/validation/raw/`. Missing rows indicate absent local data, not a simulator failure.

| Dataset | Metric | Value | Status | Note |
| --- | --- | ---: | --- | --- |
| `voteview_rollcalls.csv` | missing | --- | missing | Add Voteview-like member vote rows to compute party unity and coalition size. |
| `bill_progression.csv` | missing | --- | missing | Add Congress.gov/govinfo-style bill history rows to compute attrition. |
| `lobbying_disclosure.csv` | missing | --- | missing | Add LDA-style client issue spending rows to compute spend concentration. |
| `topic_throughput.csv` | missing | --- | missing | Add topic-level bill counts to compute agenda diversity and throughput. |
| `sponsor_success.csv` | missing | --- | missing | Add sponsor-level introduced/enacted counts to compute sponsor success concentration. |
