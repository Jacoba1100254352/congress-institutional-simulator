# Public API Adapter Fixtures

The optional fetcher in `scripts/validation/fetch_public_api_samples.py` can
populate small adapter fixtures from public APIs. These files are not raw
validation data and are not calibrated datasets.

The separate builder in `scripts/validation/build_bill_progression_dataset.py`
creates the bill-progression raw validation sample:
`data/validation/raw/bill_progression.csv`. It uses Congress.gov bill-detail and
bill-action records and writes a metadata note next to the CSV. The broader
builder in `scripts/validation/build_core_raw_validation_datasets.py` adds
Voteview roll-call rows, Congress.gov-derived topic/sponsor/committee rows, and
Senate LDA lobbying rows. These raw samples are suitable for empirical-bridge
checks, but they are not complete censuses or fitted benchmarks.

Current sources:

- Congress.gov API: bill list, law list, bill-detail, and bill-action endpoints.
  Generated files: `bill_progression.csv`, `topic_throughput.csv`, and
  `sponsor_success.csv`.
- OpenFEC API: individual receipts and independent expenditure endpoints.
  Generated file: `campaign_finance.csv`.
- Voteview static CSVs: member and vote rows. Generated file:
  `voteview_rollcalls.csv`.
- U.S. Senate LDA API: filing rows with activity issue labels and disclosed
  income/expense amounts. Generated file: `lobbying_disclosure.csv`.

Run example:

```sh
make fetch-validation-samples ARGS="--env-file /path/to/.env --bill-limit 50 --law-limit 25 --fec-limit 100"
```

The fetcher reads `CONGRESS_API_KEY` and `OPENFEC_API_KEY` from the environment
or from the provided env file. It never writes API keys to disk. The OpenFEC
normalization intentionally omits contributor names and street addresses; the
sample keeps only recipient, coarse industry/occupation text, amount, cycle, and
whether the row came from independent-expenditure data.

Limitations:

- The fixture sample is deliberately small.
- Congress.gov action text is reduced to coarse introduced, committee-reported,
  floor-considered, and enacted indicators.
- OpenFEC rows are not cleaned into a full campaign-finance ontology.
- Committee activity derived from the current Congress.gov raw sample uses
  bill-action report flags, not complete hearing or markup calendars.
- Sponsor success in the committed sample is a proposal-access concentration
  bridge. A full member-effectiveness target still requires curated Center for
  Effective Lawmaking or comparable data.
- Post-enactment implementation and law-revision validation still requires
  curated raw extracts from Federal Register, Unified Agenda, Regulations.gov,
  Congress.gov/govinfo law histories, or comparable datasets. The current
  public API fixture fetcher does not claim to build those datasets.
- These files should not be described as empirical validation of the simulator
  and should remain under `data/validation/fixtures/` unless they are replaced by
  curated, documented raw extracts.
