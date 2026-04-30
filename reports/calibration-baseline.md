# Calibration Baseline

Executable empirical-screening run for the conventional simulator baseline. This is not a claim that the model is fully fitted to Congress; it is a reproducible pass/fail check against explicit benchmark ranges derived from named empirical datasets.

## Run Configuration

- runs: 120
- legislators: 101
- bills per run: 60
- seed: 20260428
- scenarios: simple-majority, bicameral-majority, presidential-veto, current-system, default-pass-budgeted-lobbying

## Summary

- passed checks: 7 / 7

| Check | Scenario | Metric | Range | Observed | Pass |
| --- | --- | --- | ---: | ---: | --- |
| current-system-enactment-rate | current-system | productivity | 0.010--0.120 | 0.036 | yes |
| current-system-floor-load | current-system | floor | 0.050--0.450 | 0.203 | yes |
| party-unity-support-band | current-system | averageEnactedSupport | 0.500--0.820 | 0.673 | yes |
| veto-frequency-band | presidential-veto | vetoesPerRun | 0.000--8.000 | 2.600 | yes |
| sponsor-success-concentration | current-system | proposerAccessGini | 0.050--0.750 | 0.147 | yes |
| lobbying-spend-observable | default-pass-budgeted-lobbying | lobbySpendPerBill | 0.010--1.500 | 0.092 | yes |
| topic-throughput-yield | simple-majority | welfarePerSubmittedBill | 0.050--0.450 | 0.145 | yes |

## Sources

- current-system-enactment-rate: Congress.gov bulk data and govinfo BILLSTATUS collections. Broad screening range for ordinary U.S.-style bill attrition
- current-system-floor-load: Congress.gov bulk data and govinfo BILLSTATUS collections. Keeps the benchmark from treating every introduced bill as a floor bill
- party-unity-support-band: Voteview roll-call and party-unity data. Screens whether party loyalty and polarization generate plausible winning coalition support
- veto-frequency-band: Congress.gov action histories and CRS presidential veto summaries. Loose range because run length is abstract
- sponsor-success-concentration: Center for Effective Lawmaking member-level effectiveness scores. Screens whether proposer access is neither perfectly equal nor fully concentrated
- lobbying-spend-observable: U.S. Senate Lobbying Disclosure Act filings. Abstract budget-unit observability check rather than dollar calibration
- topic-throughput-yield: Comparative Agendas Project topic coding. Coarse screen for generated issue-domain throughput before topic-specific calibration
