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
| veto-frequency-band | Congress.gov veto actions and CRS summaries | `presidential-veto` | `vetoesPerRun` | Legacy broad count screen; not a conditional presidential-action calibration. |
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

The three-census temporal and mechanism-diagnostic workflow is:

```sh
make govinfo-bill-census
make govinfo-bill-census-116
make govinfo-bill-census-118
make legislative-lifecycle-calibration
make legislative-executive-action-diagnostic
make legislative-lifecycle-temporal-replication
make govinfo-bill-census-check
```

The 117th census remains the only selection source. The temporal report reads the already-selected 0.68 threshold and compares its fixed 50-seed means with all 14,148 H.R. and S. bills in the 116th Congress and all 16,213 in the 118th. The 116th backcast passes all three existing tolerances. The 118th forecast passes committee advancement and substantive floor consideration; enactment is 0.027417 in the simulator and 0.016592 in the census, an error of 0.010825 that misses the 0.010 tolerance by 0.000825. Five of six external cohort-metric cells pass. No tolerance is widened and no parameter is refit on either test Congress.

Full 118th processing exposed a context-dependent GovInfo `E30000` presidential-action code. Classifier v2 requires positive signature/enactment text or an unambiguous law record/code rather than treating that code alone as enactment. Classifier v3 adds successful override classification only when both chambers affirmatively override. It identifies the veto override and enactment of 116th-Congress H.R.6395 without changing any established funnel count.

The separate executive-action diagnostic aligns empirical presentments with simulator executive decisions, defined as enactments plus vetoes minus overrides. A compact panel parses all 126,760 H.R./S. records in the pinned 108th-118th-Congress GovInfo archives and retains 4,021 presidential decisions, including 21 vetoes and six successful overrides. Its pooled conditional veto rate is 0.005223, compared with 647 vetoes in 2,621 frozen simulator decisions, or 0.246852. The nonoverlapping Wilson intervals and exact-count 47.266-fold rate difference expose a mechanism discrepancy that the legacy `veto-frequency-band` did not catch. Because no veto-specific tolerance was prespecified, the comparison is descriptive rather than a post-hoc pass/fail rule. Government-control and sponsor-party strata are selected after congressional passage and are not causal estimates. A separately locked low-event presidential-choice model passes its 118th-Congress log-loss and aggregate-calibration gate, but 12 of 13 test vetoes occur among only 17 joint resolutions. That predictor does not calibrate the elevated-propensity simulator mechanism.

## House Agenda-Control Mechanism Test

The calendar threshold controls admission. The special-rule and suspension
thresholds add diagnostic labels to admitted bills; they do not change the
inner voting rule, enforce the House's two-thirds suspension requirement, or
change amendment rights. Their fitted shares are not evidence that those
procedural mechanisms have been implemented or validated.

The frozen v1 panel has one known chamber-attribution defect: the suspension
evidence for 118th-Congress H.R. 4366 is a Senate action. The separate
`reports/house-agenda-control-source-audit.md` rechecks all 29,335 pinned bill
histories and retains 7,397 matching actions. House screening changes one
route and raises the fixed-model test distance to 0.111950, without changing
the original fit or failed gate. Retained House Clerk and engrossed-resolution
sources independently establish the H. Res. 1061-mediated suspension path for
this bill; the direct-only screen is not a complete procedural correction.
History-wide source routes are not equivalent to the model's single-decision
overlap, and panel-wide resolution-mediated coverage remains incomplete.
Reproduce this audit with
`make house-procedure-source-audit-check`.

The source workflow builds a complete H.R. panel for the 116th-118th
Congresses and joins direct bill and rule-resolution actions to literal Table
1a entries in the official House Rules Committee activity surveys:

```sh
make house-agenda-control-panel
make house-agenda-control-study
make house-agenda-control-study-check
```

The panel contains 29,335 H.R. rows, 458 literal grant rows, and four mutually
exclusive observed floor routes. It is descriptive procedure evidence. It
does not identify leadership demand, causal gatekeeping, or the counterfactual
status quo for bills that receive no floor action.

The separate locked simulator test is:

```sh
make house-agenda-control-calibration
make house-agenda-control-calibration-check
```

The specification fixes 1,445 calendar, special-rule, and suspension
threshold triples. The 116th and 117th Congresses form the development cohort;
the unchanged 118th-Congress test uses fresh simulation seeds. The selected
triple is 0.680 / 0.475 / 0.750 and is reselected in 16 of 20
leave-one-seed-out panels. Committee advancement, floor consideration, and
restrictive special-rule share pass their test tolerances. Four-route total
variation is 0.110470 against the locked 0.100 tolerance, so the primary gate
fails. The suspension threshold is at the upper grid boundary. The grid is not
expanded and the test cohort is not used for retuning. This result falsifies
the current aggregate route construction and does not overwrite the separate
lifecycle threshold or validate House agenda control.

## Non-Goals

Flow screening should not turn the simulator into a Congress replica. The goal is to make ordinary baselines plausible enough that comparisons among institutional mechanisms are harder to dismiss as artifacts of arbitrary generation settings.
