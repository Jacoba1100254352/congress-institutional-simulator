# Empirical Flow Screening And Temporal Transport

The simulator is a mechanism-comparison model, not a fitted forecast of Congress. It includes an executable empirical-flow screening pass so conventional baselines can be checked against named real-world data sources before counterfactual systems are interpreted.

The tracked benchmark extract lives at:

```text
data/calibration/empirical-benchmarks.csv
```

The code-level benchmark loader lives in `congresssim.calibration.CalibrationTargetCatalog`.

Run the flow-screen pass with:

```sh
make calibrate
```

This writes:

- `reports/calibration-baseline.csv`
- `reports/calibration-baseline.md`

## Standard Targets

The broader target list documents what should be screened as richer empirical extracts are added.

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
| current-congress-committee-advance-rate | GovInfo 117th-Congress H.R./S. census | `current-congress-workflow` | `committeeAdvanceRate` | Screen the share of introduced bills ordered reported, reported, or discharged. |
| current-congress-floor-consideration-rate | GovInfo 117th-Congress H.R./S. census | `current-congress-workflow` | `floor` | Screen substantive floor consideration after committee advancement. |
| current-congress-enactment-rate | GovInfo 117th-Congress H.R./S. census | `current-congress-workflow` | `productivity` | Screen final enactment attrition in the lifecycle workflow. |
| party-unity-support-band | Voteview roll-call votes | `current-system` | `averageEnactedSupport` | Check generated winning coalition support under polarization. |
| veto-frequency-band | Congress.gov veto actions and CRS summaries | `presidential-veto` | `vetoesPerRun` | Catch implausible executive-veto behavior. |
| sponsor-success-concentration | Center for Effective Lawmaking | `current-system` | `proposerAccessGini` | Check whether proposer access is neither perfectly equal nor fully concentrated. |
| lobbying-spend-observable | U.S. Senate LDA filings | `default-pass-budgeted-lobbying` | `lobbySpendPerBill` | Confirm explicit lobbying actors generate visible budgeted influence. |
| topic-throughput-yield | Comparative Agendas Project | `simple-majority` | `welfarePerSubmittedBill` | Prevent generated issue throughput from collapsing to zero. |

## Flow-Screen Workflow

1. Load benchmark ranges from `data/calibration/empirical-benchmarks.csv`.
2. Run conventional scenarios: simple majority, bicameral majority, presidential veto, the compact U.S.-like comparator, the census-calibrated current-Congress workflow, and explicit budgeted lobbying.
3. Compute the mapped simulator metric for each benchmark range.
4. Write a CSV and Markdown report with observed values and pass/fail status.
5. Use failures as flow-screen prompts before drawing paper-level conclusions from counterfactual mechanisms.

The lifecycle calendar threshold is selected by `make legislative-lifecycle-calibration` from the calibration half of the GovInfo census across a fixed 50-seed simulator panel. Floor consideration and enactment enter threshold selection; committee advancement is an upstream workflow check. The held-out half is reported only after selection, and leave-one-seed-out reselection checks panel stability. Other benchmark rows remain screening ranges rather than fitted parameters.

The paired temporal workflow is:

```sh
make govinfo-bill-census
make govinfo-bill-census-118
make legislative-lifecycle-calibration
make legislative-lifecycle-temporal-replication
make govinfo-bill-census-check
```

The 117th census remains the only selection source. The temporal report reads the already-selected 0.68 threshold and compares its fixed 50-seed means with all 16,213 H.R. and S. bills in the 118th Congress. Committee advancement and substantive floor consideration pass the existing 0.020 and 0.015 absolute-error tolerances. Enactment is 0.027417 in the simulator and 0.016592 in the 118th census, an error of 0.010825 that misses the existing 0.010 tolerance by 0.000825. No tolerance is widened and no parameter is refit on the test Congress.

Full 118th processing also exposed a context-dependent GovInfo `E30000` presidential-action code. Classifier v2 requires positive signature/enactment text or an unambiguous law record/code rather than treating that code alone as enactment. The correction leaves every 117th aggregate lifecycle count unchanged and classifies the 118th as 269 enactments plus one vetoed non-enactment.

## Non-Goals

Flow screening should not turn the simulator into a Congress replica. The goal is to make ordinary baselines plausible enough that comparisons among institutional mechanisms are harder to dismiss as artifacts of arbitrary generation settings.
