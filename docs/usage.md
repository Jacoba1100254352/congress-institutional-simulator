# Congress Institutional Simulator Usage

This document is the project-facing guide for running and extending the simulator.

## Requirements

- Java 21 or newer
- `make`

The project has no external Java dependencies.

## Common Commands

Build the simulator:

```sh
make build
```

Run the default scenario comparison:

```sh
make run
```

Run tests:

```sh
make test
```

The same test command runs in GitHub Actions on pushes and pull requests.

Run the current campaign report:

```sh
make campaign
```

Run the earlier v0 campaign:

```sh
make campaign-v0
```

Run the v1 proposal-cost/flooding campaign:

```sh
make campaign-v1
```

Run the v2 challenge-voucher campaign:

```sh
make campaign-v2
```

Run the v3 challenge-sweep campaign:

```sh
make campaign-v3
```

Run the v4 cross-bloc campaign:

```sh
make campaign-v4
```

Run the v5 adaptive-track campaign:

```sh
make campaign-v5
```

Run the v6 sunset-trial campaign:

```sh
make campaign-v6
```

Run the v7 earned-credit campaign:

```sh
make campaign-v7
```

Run the v8 anti-capture campaign:

```sh
make campaign-v8
```

Run the v9 budgeted-lobbying campaign:

```sh
make campaign-v9
```

Run the v10 mediation campaign:

```sh
make campaign-v10
```

Run the v11 distributional-harm campaign:

```sh
make campaign-v11
```

Run the v12 law-registry campaign:

```sh
make campaign-v12
```

Run the v13 policy-tournament campaign:

```sh
make campaign-v13
```

Run the v14 lobbying-depth campaign:

```sh
make campaign-v14
```

Run the v15 citizen-mini-public campaign:

```sh
make campaign-v15
```

Run the v16 agenda-scarcity campaign:

```sh
make campaign-v16
```

Run the v17 roadmap-completion campaign:

```sh
make campaign-v17
```

Run the v18 party-system sensitivity campaign:

```sh
make campaign-v18
```

Run the v19 timeline stress campaign:

```sh
make campaign-v19
```

Run the v20 strategy/calibration campaign:

```sh
make campaign-v20
```

Run the main comparison campaign used for the current paper tables and figures:

```sh
make paper-campaign
```

Run the empirical benchmark screening report:

```sh
make calibrate
```

Run the supplemental all-catalog family screen:

```sh
make family-screen
```

Run the empirical validation bridge:

```sh
make empirical-bridge
```

Run component ablations:

```sh
make ablation-analysis
```

Run manipulation stress tests:

```sh
make manipulation-stress
```

Regenerate all paper diagnostics tables:

```sh
make mechanism-diagnostics
```

Remove generated build output:

```sh
make clean
```

## Research Documentation

- [Calibration and validation](calibration.md): tracked benchmark extract, external validation targets, and the executable calibration workflow.
- [ODD model description](odd-model.md): entities, state variables, scheduling, design concepts, initialization, and submodels.
- [Full ODD+D appendix](odd-d-appendix.md): submission-ready model documentation covering data, adaptation, submodels, assumptions, and outputs.

## CLI Examples

Run a larger comparison with reproducible randomness:

```sh
make run ARGS="--runs 1000 --legislators 151 --bills 80 --seed 42"
```

Compare selected scenarios:

```sh
make run ARGS="--scenarios current-system,simple-majority,simple-majority-alternatives-pairwise,risk-routed-majority,default-pass"
```

Write machine-readable output:

```sh
make run ARGS="--format csv"
```

Show ASCII bars:

```sh
make run ARGS="--charts"
```

Run a campaign with custom settings:

```sh
make campaign ARGS="--runs 300 --legislators 151 --bills 100 --seed 12345"
```

## CLI Options

- `--runs <n>`: randomized worlds per scenario.
- `--legislators <n>`: generated chamber size.
- `--bills <n>`: potential bills per run.
- `--party-count <n>`: generated party labels.
- `--polarization <0..1>`: ideological clustering.
- `--party-loyalty <0..1>`: sensitivity to party pressure.
- `--compromise <0..1>`: compromise culture.
- `--constituency <0..1>`: sensitivity to public support.
- `--lobbying <0..1>`: sensitivity to lobby pressure.
- `--scenarios <keys>`: comma-separated scenario keys.
- `--all-scenarios`: compare every explicit scenario key in the historical catalog.
- `--format <table|csv|bars>`: output format.
- `--charts`: append ASCII charts to table output.
- `--calibrate`: run empirical benchmark screening from `data/calibration/empirical-benchmarks.csv`.
- `--campaign <name>`: run a named campaign, currently `v0` through `v20`, `paper` / `main-comparison`, `ablation-analysis`, and `manipulation-stress`; the older `v21-paper` name is still accepted.
- `--output-dir <path>`: campaign artifact directory.
- `--seed <n>`: reproducible random seed.
- `--help`: print command help.

## Scenario Keys

When `--scenarios` is omitted, the CLI now runs the same representative breadth-first set used by the main paper campaign. Default-pass systems remain available, but only three are in the default set so they function as stress tests rather than the project center.

Default breadth-first keys:

- `current-system`
- `simple-majority`
- `supermajority-60`
- `bicameral-majority`
- `presidential-veto`
- `committee-regular-order`
- `parliamentary-coalition-confidence`
- `simple-majority-alternatives-pairwise`
- `simple-majority-alternatives-strategic`
- `citizen-assembly-threshold`
- `public-interest-majority`
- `agenda-lottery-majority`
- `quadratic-attention-majority`
- `proposal-bond-majority`
- `harm-weighted-majority`
- `compensation-majority`
- `package-bargaining-majority`
- `multidimensional-package-majority`
- `law-registry-majority`
- `public-objection-majority`
- `anti-capture-majority-bundle`
- `risk-routed-majority`
- `default-pass`
- `default-pass-challenge`
- `default-pass-multiround-mediation-challenge`

Use `make run ARGS="--help"` to print the full explicit catalog. The historical catalog still includes deep default-pass side sweeps: committee gates, challenge-token grids, lobbying reforms, citizen-panel variants, adaptive tracks, law-registry variants, and other guardrail combinations.

## Campaign Reports

Campaigns write CSV and Markdown artifacts under `reports/`.

Current campaign:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/simulation-campaign-v21-paper-manifest.json`
- `reports/paper-findings-validation.md`

Calibration report:

- `reports/calibration-baseline.csv`
- `reports/calibration-baseline.md`
- `reports/calibration-baseline-manifest.json`

Diagnostic reports:

- `reports/empirical-bridge.csv`
- `reports/empirical-bridge.md`
- `reports/ablation-analysis-summary.csv`
- `reports/ablation-analysis-summary.md`
- `reports/manipulation-stress-summary.csv`
- `reports/manipulation-stress-summary.md`
- `reports/simulation-ablation-analysis.csv`
- `reports/simulation-manipulation-stress.csv`

Earlier campaigns:

- `reports/simulation-campaign-v0.csv`
- `reports/simulation-campaign-v0.md`
- `reports/simulation-campaign-v1.csv`
- `reports/simulation-campaign-v1.md`
- `reports/simulation-campaign-v2.csv`
- `reports/simulation-campaign-v2.md`
- `reports/simulation-campaign-v3.csv`
- `reports/simulation-campaign-v3.md`
- `reports/simulation-campaign-v4.csv`
- `reports/simulation-campaign-v4.md`
- `reports/simulation-campaign-v5.csv`
- `reports/simulation-campaign-v5.md`
- `reports/simulation-campaign-v6.csv`
- `reports/simulation-campaign-v6.md`
- `reports/simulation-campaign-v7.csv`
- `reports/simulation-campaign-v7.md`
- `reports/simulation-campaign-v8.csv`
- `reports/simulation-campaign-v8.md`
- `reports/simulation-campaign-v9.csv`
- `reports/simulation-campaign-v9.md`
- `reports/simulation-campaign-v10.csv`
- `reports/simulation-campaign-v10.md`
- `reports/simulation-campaign-v11.csv`
- `reports/simulation-campaign-v11.md`
- `reports/simulation-campaign-v12.csv`
- `reports/simulation-campaign-v12.md`
- `reports/simulation-campaign-v13.csv`
- `reports/simulation-campaign-v13.md`
- `reports/simulation-campaign-v14.csv`
- `reports/simulation-campaign-v14.md`
- `reports/simulation-campaign-v15.csv`
- `reports/simulation-campaign-v15.md`
- `reports/simulation-campaign-v16.csv`
- `reports/simulation-campaign-v16.md`
- `reports/simulation-campaign-v17.csv`
- `reports/simulation-campaign-v17.md`
- `reports/simulation-campaign-v18.csv`
- `reports/simulation-campaign-v18.md`
- `reports/simulation-campaign-v19.csv`
- `reports/simulation-campaign-v19.md`

Use CSV output for analysis and Markdown output for quick review.

## Metrics

The simulator reports several metrics because passage volume alone is not enough to evaluate an institution.

Direction markers are used in generated reports and paper figures:

- `↑`: higher is generally better.
- `↓`: lower is generally better.
- `diag.`: context-dependent activity or risk context.

The campaign CSV also includes `directionalScore`, `representativeQuality`, `riskControl`, and `administrativeFeasibility`. These are display scores, not proof that a system is best. `directionalScore` averages productivity, representative quality, risk control, and administrative feasibility. `representativeQuality` combines welfare, enacted support, compromise, public alignment, and legitimacy. `riskControl` inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift. `administrativeFeasibility` inverts the administrative-cost index.

- `productivity` `↑`: share of potential bills enacted.
- `caseWeight` `diag.`: likelihood weight used by sensitivity campaigns; ordinary campaigns use `1.0`.
- `floor` `diag.`: share of potential bills reaching floor consideration.
- `avgSupport` `↑`: average yes-vote share for enacted bills.
- `welfare` `↑`: average public-benefit score for enacted bills.
- `cooperation` `↑`: productivity weighted by enacted support.
- `compromise` `↑`: moderation, support, and distance from proposer advantage.
- `gridlock` `↓`: share of potential bills not enacted.
- `accessD` `diag.`: share of potential bills denied by proposal-access rules.
- `cmteRej` `diag.`: share of potential bills rejected by committee.
- `challengeRate` `diag.`: share of potential bills diverted from default enactment into active voting by challenge vouchers or q-member escalation.
- `lowSupport` `↓`: enacted bills with less than 50 percent yes support.
- `weakPublicMandatePassage` `↓`: enacted bills with generated public support below 50 percent, regardless of chamber threshold.
- `administrativeCost` `↓`: estimated procedural load from attention spending, review, challenge, amendment, and alternative-selection work.
- `popularFail` `↓`: high-public-support bills that fail.
- `policyShift` `diag.`: average movement away from the prior status quo; this can be reform or volatility depending on the scenario.
- `propGain` `↓`: enacted movement toward the proposer's ideal point.
- `lobbyCapture` `↓`: average enacted-bill capture risk from positive lobby pressure, private gain, and weak public value.
- `publicAlignment` `↑`: how closely enacted voting support tracks generated public support.
- `antiLobbyingSuccess` `↑`: share of generated anti-lobbying reform bills enacted.
- `privateGainRatio` `↓`: enacted private gain relative to generated public benefit.
- `lobbySpendPerBill` `diag.`: explicit lobby-group spend per potential bill.
- `defensiveLobbyingShare` `diag.`: share of lobby spend aimed at defeating anti-lobbying reform bills.
- `captureReturnOnSpend` `↓`: enacted capture risk per unit of explicit lobby spend.
- `publicPreferenceDistortion` `↓`: average gap between enacted yes-share and generated public support.
- `amendmentRate` `diag.`: share of potential bills whose policy position moved during mediation.
- `amendmentMovement` `diag.`: average absolute policy movement created by mediation per potential bill.
- `minorityHarm` `↓`: average enacted concentrated harm weighted by affected-group opposition.
- `concentratedHarmPassage` `↓`: share of high concentrated-harm bills that are enacted.
- `compensationRate` `diag.`: share of potential bills receiving compensation amendments.
- `legitimacy` `↑`: enacted-bill legitimacy proxy combining public support, chamber support, affected-group support, and harm penalties.
- `activeLawWelfare` `↑`: average generated public benefit among active laws at delayed review points.
- `reversalRate` `diag.`: share of delayed law reviews that repeal a provisional law.
- `timeToCorrectBadLaw` `↓`: average rounds between enactment and repeal for corrected laws.
- `lowSupportActiveLawShare` `↓`: share of active laws at review points with public support below 50 percent.
- `selectedAlternativeMedianDistance` `↓`: average distance between selected alternatives and the chamber median.
- `proposerAgendaAdvantage` `↓`: average selected-alternative movement toward the original proposer's ideal point.
- `alternativeDiversity` `diag.`: average number of alternatives/status quo options considered per tournament.
- `statusQuoWinRate` `diag.`: share of policy tournaments where the status quo blocks final ratification.
- `publicBenefitPerLobbyDollar` `↑`: enacted public benefit per unit of explicit lobby spend.
- `directLobbySpendShare`, `agendaLobbySpendShare`, `informationLobbySpendShare`, `publicCampaignSpendShare`, `litigationThreatSpendShare` `diag.`: explicit lobbying spend allocation by channel.
- `citizenReviewRate` `diag.`: share of potential bills reviewed by a synthetic citizen panel.
- `citizenCertificationRate` `↑`: share of reviewed bills receiving a positive citizen-panel certificate.
- `citizenLegitimacy` `↑`: average legitimacy estimate from citizen-panel review.
- `attentionSpendPerBill` `diag.`: quadratic attention credits spent per potential bill.
- `objectionWindowRate` `diag.`: share of potential bills triggering a public objection or repeal window.
- `repealWindowReversalRate` `diag.`: share of triggered repeal windows that reverse enactment.
- `fastLaneRate`, `middleLaneRate`, `highRiskLaneRate` `diag.`: adaptive-route shares.
- `challengeExhaustionRate` `↓`: share of potential bills where a challenge would have cleared threshold but no token was available.
- `falseNegativePassRate` `↓`: risky, low-support, or high-harm default enactments that passed unchallenged.
- `publicWillReviewRate`, `publicSignalMovement` `diag.`, `districtAlignment` `↑`: constituent/public-will review diagnostics.
- `crossBlocAdmissionRate`, `affectedGroupSponsorshipRate`, `averageCosponsors` `diag.`: richer cosponsorship diagnostics.
- `proposalBondForfeiture` `diag.`: average proposal-bond loss per potential bill.
- `strategicDecoyRate` `↓`: strategic clone/decoy alternatives introduced per tournament.
- `proposerAccessGini` `↓`: concentration of floor access across proposers.
- `welfarePerSubmittedBill` `↑`: public-benefit yield per potential proposal.
- `vetoes`: presidential veto count.
- `overrides`: veto override count.

Campaign CSV files also include absolute load metrics such as `enactedPerRun` and `floorPerRun`.

## Extending The Simulator

The main extension points are small interfaces:

- `VotingStrategy`: converts legislator incentives into `YAY` or `NAY`.
- `VoteInfluence`: models one source of voting pressure.
- `VotingRule`: converts vote totals into passage or failure.
- `ProposalAccessRule`: controls whether a bill reaches floor consideration.
- `LegislativeProcess`: wraps one or more institutional stages around a bill.
- `Scenario`: names and builds an institutional design for comparison.

Typical additions:

- Add a new voting pressure in `src/main/java/congresssim/behavior`.
- Add a new agenda screen in `src/main/java/congresssim/institution`.
- Add a new process wrapper in `src/main/java/congresssim/institution`.
- For anti-capture modeling, use `LobbyTransparencyProcess`, `LobbyAuditProcess`, or `PublicInterestScreenAccessRule`.
- For explicit lobbying actors, add `LobbyGroup` instances to `SimulationWorld` and wrap a process with `BudgetedLobbyingProcess`.
- Register the new scenario in `src/main/java/congresssim/simulation/ScenarioCatalog.java`.
- Add focused coverage in `src/test/java/congresssim/SimulatorTests.java`.

After changing behavior, run:

```sh
make test
make campaign
```
