# Calibration And Validation

The simulator is still a mechanism-search model, not a fitted forecast of Congress. It now includes an executable empirical-screening pass so conventional baselines can be checked against named real-world data sources before counterfactual systems are interpreted.

The tracked benchmark extract lives at:

```text
data/calibration/empirical-benchmarks.csv
```

The code-level benchmark loader lives in `congresssim.calibration.CalibrationTargetCatalog`.

Run the validation pass with:

```sh
make calibrate
```

This writes:

- `reports/calibration-baseline.csv`
- `reports/calibration-baseline.md`

## Standard Targets

The broader target list documents what should be calibrated as richer empirical extracts are added.

| Target | Dataset | Simulator Metrics | Use |
| --- | --- | --- | --- |
| Voteview party unity | Voteview roll-call votes | average support, coalition size, party-position spread | Tune party loyalty and polarization in conventional baselines. |
| Bill attrition | Congress.gov and govinfo bill histories | floor consideration, access denial, committee rejection, productivity, vetoes | Check ordinary procedural baselines before testing counterfactual rules. |
| Topic throughput | Comparative Agendas Project | issue-domain shares, enacted diversity, welfare per submitted bill | Keep generated issue domains from becoming arbitrary noise. |
| Party systems | ParlGov | party-system profile, case weight, seat shares | Ground weighted two-party, two-major-plus-minors, fragmented, and dominant-party cases. |
| Lobbying spend | U.S. lobbying disclosure data | spend per bill, defensive share, channel shares, capture return | Constrain budgeted lobby actors and anti-capture scenarios. |
| Sponsor success | Center for Effective Lawmaking | proposer access Gini, welfare per submitted bill, enacted bills by proposer | Interpret proposal credits, bonds, and agenda concentration. |
| Institutional context | V-Dem | case weights, veto frequency, legitimacy, public alignment | Support broader sensitivity analysis without pretending the model is U.S.-validated. |

## Executable Benchmarks

The current benchmark extract maps named empirical quantities to simulator metrics and pass/fail ranges:

| Check | Source Data | Scenario | Metric | Purpose |
| --- | --- | --- | --- | --- |
| current-system-enactment-rate | Congress.gov and govinfo bill histories | `current-system` | `productivity` | Screen whether stylized U.S.-like conventional bill attrition stays plausible. |
| current-system-floor-load | Congress.gov and govinfo bill histories | `current-system` | `floor` | Prevent the benchmark from treating every introduced bill as a floor bill. |
| party-unity-support-band | Voteview roll-call votes | `current-system` | `averageEnactedSupport` | Check generated winning coalition support under polarization. |
| veto-frequency-band | Congress.gov veto actions and CRS summaries | `presidential-veto` | `vetoesPerRun` | Catch implausible executive-veto behavior. |
| sponsor-success-concentration | Center for Effective Lawmaking | `current-system` | `proposerAccessGini` | Check whether proposer access is neither perfectly equal nor fully concentrated. |
| lobbying-spend-observable | U.S. Senate LDA filings | `default-pass-budgeted-lobbying` | `lobbySpendPerBill` | Confirm explicit lobbying actors generate visible budgeted influence. |
| topic-throughput-yield | Comparative Agendas Project | `simple-majority` | `welfarePerSubmittedBill` | Prevent generated issue throughput from collapsing to zero. |

## Calibration Workflow

1. Load benchmark ranges from `data/calibration/empirical-benchmarks.csv`.
2. Run conventional scenarios: simple majority, bicameral majority, presidential veto, the stylized U.S.-like benchmark, and explicit budgeted lobbying.
3. Compute the mapped simulator metric for each benchmark range.
4. Write a CSV and Markdown report with observed values and pass/fail status.
5. Use failures as calibration prompts before drawing paper-level conclusions from counterfactual mechanisms.

The current pass is deliberately a benchmark screen. It does not yet fit parameters automatically or ingest raw Voteview/Congress.gov/LDA rows during the run. The next validation increment should add raw-data adapters that produce the benchmark extract directly.

## Non-Goals

Calibration should not turn the simulator into a Congress replica. The goal is to make ordinary baselines plausible enough that comparisons among institutional mechanisms are harder to dismiss as artifacts of arbitrary generation settings.
