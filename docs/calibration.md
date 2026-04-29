# Calibration Plan

The simulator is currently an exploratory mechanism-search model, not an empirical model of Congress. Calibration should happen before the project makes stronger empirical claims.

## Standard Targets

The code-level target list lives in `congresssim.calibration.CalibrationTargetCatalog`.

| Target | Dataset | Simulator Metrics | Use |
| --- | --- | --- | --- |
| Voteview party unity | Voteview roll-call votes | average support, coalition size, party-position spread | Tune party loyalty and polarization in conventional baselines. |
| Bill attrition | Congress.gov and govinfo bill histories | floor consideration, access denial, committee rejection, productivity, vetoes | Check ordinary procedural baselines before testing counterfactual rules. |
| Topic throughput | Comparative Agendas Project | issue-domain shares, enacted diversity, welfare per submitted bill | Keep generated issue domains from becoming arbitrary noise. |
| Party systems | ParlGov | party-system profile, case weight, seat shares | Ground weighted two-party, two-major-plus-minors, fragmented, and dominant-party cases. |
| Lobbying spend | U.S. lobbying disclosure data | spend per bill, defensive share, channel shares, capture return | Constrain budgeted lobby actors and anti-capture scenarios. |
| Sponsor success | Center for Effective Lawmaking | proposer access Gini, welfare per submitted bill, enacted bills by proposer | Interpret proposal credits, bonds, and agenda concentration. |
| Institutional context | V-Dem | case weights, veto frequency, legitimacy, public alignment | Support broader sensitivity analysis without pretending the model is U.S.-validated. |

## Calibration Workflow

1. Run a conventional baseline campaign with simple majority, bicameral majority, presidential veto, committee gatekeeping, and ordinary proposal access.
2. Compute simulator distributions for the metrics above rather than relying on one aggregate average.
3. Fit generation parameters only on conventional institutional baselines.
4. Freeze calibrated parameters before evaluating counterfactual scenarios.
5. Report whether each counterfactual result is robust across calibrated and deliberately misspecified assumption cases.

## Non-Goals

Calibration should not turn the simulator into a Congress replica. The goal is to make ordinary baselines plausible enough that comparisons among institutional mechanisms are harder to dismiss as artifacts of arbitrary generation settings.
