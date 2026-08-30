# Calibration Baseline

Executable empirical-screening run for the conventional simulator baseline. This is not a claim that the model is fully fitted to Congress; it is a reproducible pass/fail check against explicit benchmark ranges derived from named empirical datasets.

## Run Configuration

- runs: 120
- legislators: 101
- bills per run: 60
- seed: 20260428
- scenarios: simple-majority, bicameral-majority, presidential-veto, current-system, default-pass-budgeted-lobbying, district-population-majority, influence-system-majority, constitutional-court-architecture-majority, law-registry-majority

## Summary

- passed checks: 15 / 15

| Check | Scenario | Metric | Range | Observed | Pass |
| --- | --- | --- | ---: | ---: | --- |
| current-system-enactment-rate | current-system | productivity | 0.010--0.070 | 0.038 | yes |
| current-system-floor-load | current-system | floor | 0.080--0.320 | 0.218 | yes |
| party-unity-support-band | current-system | averageEnactedSupport | 0.560--0.780 | 0.668 | yes |
| veto-frequency-band | presidential-veto | vetoesPerRun | 0.000--8.000 | 2.600 | yes |
| sponsor-success-concentration | current-system | proposerAccessGini | 0.050--0.550 | 0.137 | yes |
| lobbying-spend-observable | default-pass-budgeted-lobbying | lobbySpendPerBill | 0.010--1.500 | 0.092 | yes |
| topic-throughput-yield | simple-majority | welfarePerSubmittedBill | 0.050--0.450 | 0.145 | yes |
| district-public-will-alignment | district-population-majority | districtAlignment | 0.200--0.800 | 0.393 | yes |
| district-turnout-skew-proxy | district-population-majority | turnoutSkewIndex | 0.000--0.400 | 0.254 | yes |
| campaign-finance-observable-band | influence-system-majority | campaignFinanceCaptureIndex | 0.000--1.000 | 0.144 | yes |
| judicial-review-constraint | constitutional-court-architecture-majority | constitutionalInvalidationRate | 0.000--0.200 | 0.000 | yes |
| implementation-delay-proxy | law-registry-majority | implementationDelay | 0.000--100.000 | 0.486 | yes |
| implementation-capacity-proxy | law-registry-majority | implementationCapacity | 0.000--1.000 | 0.184 | yes |
| law-revision-correction-proxy | law-registry-majority | reversalRate | 0.000--0.800 | 0.420 | yes |
| bicameral-veto-burden | bicameral-majority | interChamberConflictRate | 0.050--0.600 | 0.148 | yes |

## Sources

- current-system-enactment-rate: Congress.gov bulk data and govinfo BILLSTATUS collections. Screening range tightened around the committed bill-progression raw sample while retaining abstraction margin
- current-system-floor-load: Congress.gov bulk data and govinfo BILLSTATUS collections. Tightened screen to keep the benchmark from treating every introduced bill as a floor bill
- party-unity-support-band: Voteview roll-call and party-unity data. Screens winning coalition size against the committed Voteview roll-call sample
- veto-frequency-band: Congress.gov action histories and CRS presidential veto summaries. Loose range because run length is abstract
- sponsor-success-concentration: Center for Effective Lawmaking and Congress.gov sponsor samples. Screens whether proposer access is neither perfectly equal nor fully concentrated
- lobbying-spend-observable: U.S. Senate Lobbying Disclosure Act filings. Abstract budget-unit observability check rather than dollar calibration
- topic-throughput-yield: Comparative Agendas Project topic coding. Coarse screen for generated issue-domain throughput before topic-specific calibration
- district-public-will-alignment: CES district-level survey aggregates. Abstract public-will alignment screen using district proxy data not bill-specific support validation
- district-turnout-skew-proxy: CES district-level survey aggregates. Coarse turnout-skew screen using district proxy data not a voter-file validation
- campaign-finance-observable-band: OpenFEC Schedule A and Schedule E bounded extracts. Unit-scale observability band for campaign-finance influence metrics not causal capture calibration
- judicial-review-constraint: Supreme Court Database case-centered release. Broad upper-bound screen for merits-case invalidation not emergency-order validation
- implementation-delay-proxy: Federal Register final-rule publication and effective-date extract. Abstract delay screen linked to final-to-effective-date rows not full administrative implementation validation
- implementation-capacity-proxy: Federal Register final-rule publication and effective-date extract. Abstract capacity screen derived from effective-date speed not enforcement validation
- law-revision-correction-proxy: Congress.gov public-law title and summary flags. Broad correction-rate proxy for amendment repeal reauthorization and sunset language not statutory-lineage validation
- bicameral-veto-burden: QoG DES POLCON and OWID V-Dem selected profiles. Coarse bicameral-burden screen not cross-national productivity validation
