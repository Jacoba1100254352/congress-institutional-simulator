# Public API Validation Samples

The optional fetcher in `scripts/validation/fetch_public_api_samples.py` can
populate small raw validation samples from public APIs. These files are adapter
smoke tests, not calibrated datasets.

Current sources:

- Congress.gov API: bill list, law list, bill-detail, and bill-action endpoints.
  Generated files: `bill_progression.csv`, `topic_throughput.csv`, and
  `sponsor_success.csv`.
- OpenFEC API: individual receipts and independent expenditure endpoints.
  Generated file: `campaign_finance.csv`.

Run example:

```sh
make fetch-validation-samples ARGS="--env-file /path/to/.env --bill-limit 50 --law-limit 25 --fec-limit 100"
make validation-readiness
make empirical-validation
```

The fetcher reads `CONGRESS_API_KEY` and `OPENFEC_API_KEY` from the environment
or from the provided env file. It never writes API keys to disk. The OpenFEC
normalization intentionally omits contributor names and street addresses; the
sample keeps only recipient, coarse industry/occupation text, amount, cycle, and
whether the row came from independent-expenditure data.

Limitations:

- The sample is deliberately small.
- Congress.gov action text is reduced to coarse introduced, committee-reported,
  floor-considered, and enacted indicators.
- OpenFEC rows are not cleaned into a full campaign-finance ontology.
- These files should not be described as empirical validation of the simulator.
