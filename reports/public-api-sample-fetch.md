# Public API Validation Sample Fetch

This report records the shape of locally fetched public API samples. It does not contain API keys and does not claim empirical validation.

| Source | Output | Rows/groups |
| --- | --- | ---: |
| Congress.gov | `bill_progression.csv` | 75 |
| Congress.gov | `topic_throughput.csv` | 23 |
| Congress.gov | `sponsor_success.csv` | 42 |
| OpenFEC | `campaign_finance.csv` | 200 |

Interpretation: these files are adapter smoke-test samples for bill attrition, topic throughput, sponsor success, and campaign-finance concentration. They are too small and too lightly cleaned to validate the simulator.
