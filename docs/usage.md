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

Remove generated build output:

```sh
make clean
```

## CLI Examples

Run a larger comparison with reproducible randomness:

```sh
make run ARGS="--runs 1000 --legislators 151 --bills 80 --seed 42"
```

Compare selected scenarios:

```sh
make run ARGS="--scenarios simple-majority,default-pass,default-pass-informed-guarded"
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
- `--format <table|csv|bars>`: output format.
- `--charts`: append ASCII charts to table output.
- `--campaign <v0..v17>`: run a named campaign.
- `--output-dir <path>`: campaign artifact directory.
- `--seed <n>`: reproducible random seed.
- `--help`: print command help.

## Scenario Keys

The default CLI scenario set includes:

- `simple-majority`: unicameral simple majority.
- `simple-majority-mediation`: unicameral simple majority with a structured amendment/mediation stage.
- `simple-majority-lobby-firewall`: unicameral simple majority with reduced direct lobby vote influence.
- `supermajority-60`: unicameral 60 percent passage threshold.
- `default-pass`: default passage unless two-thirds vote to block.
- `default-pass-mediation`: default passage after a bounded mediation stage can move risky bills toward the median/status quo.
- `default-pass-lobby-firewall`: default passage with reduced direct lobby vote influence.
- `default-pass-lobby-transparency`: default passage after disclosure weakens effective lobby pressure and creates backlash against capture-risk bills.
- `default-pass-public-interest-screen`: default passage with an anti-capture public-interest access screen.
- `default-pass-lobby-audit`: default passage with randomized anti-capture audits and sponsor sanctions.
- `default-pass-anti-capture-bundle`: transparency, public-interest screening, audit sanctions, and lower direct lobby vote influence.
- `default-pass-budgeted-lobbying`: default passage after explicit lobby groups spend limited budgets by issue domain.
- `default-pass-budgeted-lobbying-transparency`: budgeted lobbying followed by transparency backlash.
- `default-pass-budgeted-lobbying-bundle`: budgeted lobbying with transparency, public-interest screening, audits, and lower direct lobby vote influence.
- `default-pass-budgeted-lobbying-mediation`: budgeted lobbying followed by bounded amendment mediation.
- `default-pass-democracy-vouchers`: budgeted lobbying with a public-financing counterweight.
- `default-pass-public-advocate`: budgeted lobbying with an equal-access public advocate.
- `default-pass-blind-lobby-review`: budgeted lobbying with reduced agenda and information influence before sponsor/lobby origin is visible.
- `default-pass-defensive-lobby-cap`: budgeted lobbying with an explicit cap on anti-reform defensive spend.
- `default-pass-lobby-channel-bundle`: public financing, public advocate access, blind review, and defensive caps together.
- `default-pass-citizen-certificate`: default passage only for bills certified by a synthetic citizen panel.
- `default-pass-citizen-active-routing`: uncertified citizen-panel bills route to active majority voting.
- `default-pass-citizen-threshold`: uncertified citizen-panel bills require a stronger affirmative threshold.
- `default-pass-citizen-agenda`: citizen-panel results adjust agenda priority/public signals without changing the final lane.
- `default-pass-weighted-agenda-lottery`: default passage after a weighted lottery rations floor slots.
- `default-pass-random-agenda-lottery`: default passage after a random lottery rations floor slots.
- `default-pass-quadratic-attention`: default passage with quadratic agenda-attention credits.
- `default-pass-public-objection`: high-contestation bills are routed to active voting after a public objection window.
- `default-pass-repeal-window`: high-contestation default enactments can be reversed after a public repeal window.
- `default-pass-harm-threshold`: default passage for ordinary bills, but concentrated-harm bills require affirmative supermajority support.
- `default-pass-compensation`: default passage with compensation amendments for high concentrated-harm bills.
- `default-pass-affected-consent`: default passage with compensation plus affected-group consent screening.
- `simple-majority-alternatives-pairwise`: simple majority after a pairwise competing-alternatives stage.
- `default-pass-alternatives-benefit`: default passage after choosing the highest-public-benefit alternative.
- `default-pass-alternatives-support`: default passage after choosing the highest-public-support alternative.
- `default-pass-alternatives-median`: default passage after choosing the alternative closest to the chamber median.
- `default-pass-alternatives-pairwise`: default passage after a pairwise policy tournament.
- `default-pass-obstruction-substitute`: default passage after opponents can force a same-domain substitute into the tournament.
- `default-pass-challenge`: default passage with scarce party-held challenge vouchers.
- `default-pass-challenge-info`: default passage with committee information before challenge-voucher decisions.
- `default-pass-cross-bloc`: default passage with a cross-bloc cosponsorship agenda gate.
- `default-pass-cross-bloc-strong`: default passage with a stricter cross-bloc cosponsorship gate.
- `default-pass-cross-bloc-challenge`: cross-bloc cosponsorship before challenge-voucher review.
- `default-pass-adaptive-track`: adaptive procedural routing with low-risk, middle, and high-risk lanes.
- `default-pass-adaptive-track-challenge`: adaptive routing with challenge vouchers in the middle-risk lane.
- `default-pass-sunset-trial`: provisional enactment plus automatic sunset review for risky bills.
- `default-pass-sunset-challenge`: challenge vouchers plus sunset review.
- `default-pass-law-registry`: delayed active-law review, renewal, and repeal across the run.
- `default-pass-law-registry-challenge`: challenge vouchers plus delayed active-law review.
- `default-pass-earned-credits`: stateful agenda credits earned or lost through proposal quality.
- `default-pass-earned-credits-challenge`: earned proposal credits plus challenge vouchers.
- `default-pass-constituent-public-will`: district-weighted constituent/public-will signal revision.
- `default-pass-constituent-citizen-panel`: constituent public-will revision followed by citizen-panel active routing.
- `default-pass-proposal-bonds`: refundable public-benefit proposal bonds.
- `default-pass-proposal-bonds-challenge`: proposal bonds plus challenge vouchers.
- `default-pass-cross-bloc-credit-discount`: richer cross-bloc cosponsorship with coalition support discounts.
- `default-pass-affected-sponsor-gate`: cross-bloc cosponsorship requiring affected-group sponsor participation.
- `default-pass-multiround-mediation`: multi-round amendment mediation with costs, concession limits, poison-pill risk, and compensation.
- `default-pass-multiround-mediation-challenge`: multi-round mediation plus challenge vouchers.
- `default-pass-alternatives-strategic`: policy tournament with strategic clones and decoys.
- `default-pass-challenge-party-proportional`: challenge vouchers allocated proportionally by party size.
- `default-pass-challenge-minority-bonus`: challenge vouchers with a minority-party allocation bonus.
- `default-pass-challenge-supermajority`: challenged bills route to a 60 percent affirmative vote.
- `default-pass-challenge-committee`: challenged bills route to committee review.
- `default-pass-challenge-info-active`: challenged bills receive committee information before active voting.
- `default-pass-adaptive-track-lenient`: adaptive routing with wider fast-lane eligibility.
- `default-pass-adaptive-track-strict`: adaptive routing with stricter high-risk review.
- `default-pass-adaptive-track-citizen-high-risk`: adaptive routing with citizen-panel review for high-risk bills.
- `default-pass-adaptive-track-supermajority-high-risk`: adaptive routing with supermajority review for high-risk bills.
- `default-pass-law-registry-fast-review`: active-law registry with faster review.
- `default-pass-law-registry-slow-review`: active-law registry with slower partial rollback.
- `default-pass-cost-public-waiver`: proposal costs discounted by public value.
- `default-pass-cost-lobby-surcharge`: proposal costs increased by positive lobby pressure.
- `default-pass-member-quota`: stateful per-member proposal quota.
- `default-pass-challenge-party-t3-s082`: party-held challenge voucher sweep point with 3 tokens per party and challenge threshold 0.82.
- `default-pass-challenge-party-t25-s082`: party-held challenge voucher sweep point with 25 tokens per party and challenge threshold 0.82.
- `default-pass-challenge-party-t10-s050`: party-held challenge voucher sweep point with 10 tokens per party and challenge threshold 0.50.
- `default-pass-challenge-party-t10-s125`: party-held challenge voucher sweep point with 10 tokens per party and challenge threshold 1.25.
- `default-pass-challenge-member-t1-s082`: legislator-held challenge voucher sweep point with 1 token per legislator.
- `default-pass-challenge-member-t3-s082`: legislator-held challenge voucher sweep point with 3 tokens per legislator.
- `default-pass-escalation-q6-s082`: tokenless q-member challenge escalation with 6 challengers required.
- `default-pass-escalation-q12-s082`: tokenless q-member challenge escalation with 12 challengers required.
- `default-pass-escalation-q20-s082`: tokenless q-member challenge escalation with 20 challengers required.
- `default-pass-access`: default passage with a proposal-access screen.
- `default-pass-cost`: default passage with a proposal-cost screen.
- `default-pass-cost-guarded`: default passage with proposal costs, proposal access, committee information, and committee gatekeeping.
- `default-pass-committee`: default passage with a representative committee gate.
- `default-pass-committee-majority`: default passage with a majority-controlled committee gate.
- `default-pass-committee-polarized`: default passage with a polarized committee gate.
- `default-pass-committee-captured`: default passage with a lobby-sensitive committee gate.
- `default-pass-info`: default passage with representative committee information review.
- `default-pass-info-expert`: default passage with expert-style committee information review.
- `default-pass-info-captured`: default passage with captured committee information review.
- `default-pass-guarded`: default passage with proposal access and committee gatekeeping.
- `default-pass-informed-guarded`: default passage with access screening, committee information, and committee gatekeeping.
- `bicameral-majority`: bicameral simple majority.
- `presidential-veto`: bicameral majority with presidential veto and two-thirds override.

## Campaign Reports

Campaigns write CSV and Markdown artifacts under `reports/`.

Current campaign:

- `reports/simulation-campaign-v17.csv`
- `reports/simulation-campaign-v17.md`

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

Use CSV output for analysis and Markdown output for quick review.

## Metrics

The simulator reports several metrics because passage volume alone is not enough to evaluate an institution.

- `productivity`: share of potential bills enacted.
- `floor`: share of potential bills reaching floor consideration.
- `avgSupport`: average yes-vote share for enacted bills.
- `welfare`: average public-benefit score for enacted bills.
- `cooperation`: productivity weighted by enacted support.
- `compromise`: moderation, support, and distance from proposer advantage.
- `gridlock`: share of potential bills not enacted.
- `accessD`: share of potential bills denied by proposal-access rules.
- `cmteRej`: share of potential bills rejected by committee.
- `challengeRate`: share of potential bills diverted from default enactment into active voting by challenge vouchers or q-member escalation.
- `lowSupport`: enacted bills with less than 50 percent yes support.
- `popularFail`: high-public-support bills that fail.
- `policyShift`: average movement away from the prior status quo.
- `propGain`: enacted movement toward the proposer's ideal point.
- `lobbyCapture`: average enacted-bill capture risk from positive lobby pressure, private gain, and weak public value.
- `publicAlignment`: how closely enacted voting support tracks generated public support.
- `antiLobbyingSuccess`: share of generated anti-lobbying reform bills enacted.
- `privateGainRatio`: enacted private gain relative to generated public benefit.
- `lobbySpendPerBill`: explicit lobby-group spend per potential bill.
- `defensiveLobbyingShare`: share of lobby spend aimed at defeating anti-lobbying reform bills.
- `captureReturnOnSpend`: enacted capture risk per unit of explicit lobby spend.
- `publicPreferenceDistortion`: average gap between enacted yes-share and generated public support.
- `amendmentRate`: share of potential bills whose policy position moved during mediation.
- `amendmentMovement`: average absolute policy movement created by mediation per potential bill.
- `minorityHarm`: average enacted concentrated harm weighted by affected-group opposition.
- `concentratedHarmPassage`: share of high concentrated-harm bills that are enacted.
- `compensationRate`: share of potential bills receiving compensation amendments.
- `legitimacy`: enacted-bill legitimacy proxy combining public support, chamber support, affected-group support, and harm penalties.
- `activeLawWelfare`: average generated public benefit among active laws at delayed review points.
- `reversalRate`: share of delayed law reviews that repeal a provisional law.
- `timeToCorrectBadLaw`: average rounds between enactment and repeal for corrected laws.
- `lowSupportActiveLawShare`: share of active laws at review points with public support below 50 percent.
- `selectedAlternativeMedianDistance`: average distance between selected alternatives and the chamber median.
- `proposerAgendaAdvantage`: average selected-alternative movement toward the original proposer's ideal point.
- `alternativeDiversity`: average number of alternatives/status quo options considered per tournament.
- `statusQuoWinRate`: share of policy tournaments where the status quo blocks final ratification.
- `publicBenefitPerLobbyDollar`: enacted public benefit per unit of explicit lobby spend.
- `directLobbySpendShare`: share of explicit lobbying spent on direct pressure.
- `agendaLobbySpendShare`: share of explicit lobbying spent on agenda access.
- `informationLobbySpendShare`: share of explicit lobbying spent on information distortion.
- `publicCampaignSpendShare`: share of explicit lobbying spent on public campaigns.
- `litigationThreatSpendShare`: share of explicit lobbying spent on litigation or delay threats.
- `citizenReviewRate`: share of potential bills reviewed by a synthetic citizen panel.
- `citizenCertificationRate`: share of reviewed bills receiving a positive citizen-panel certificate.
- `citizenLegitimacy`: average legitimacy estimate from citizen-panel review.
- `attentionSpendPerBill`: quadratic attention credits spent per potential bill.
- `objectionWindowRate`: share of potential bills triggering a public objection or repeal window.
- `repealWindowReversalRate`: share of triggered repeal windows that reverse enactment.
- `fastLaneRate`, `middleLaneRate`, `highRiskLaneRate`: adaptive-route shares.
- `challengeExhaustionRate`: share of potential bills where a challenge would have cleared threshold but no token was available.
- `falseNegativePassRate`: risky, low-support, or high-harm default enactments that passed unchallenged.
- `publicWillReviewRate`, `publicSignalMovement`, `districtAlignment`: constituent/public-will review diagnostics.
- `crossBlocAdmissionRate`, `affectedGroupSponsorshipRate`, `averageCosponsors`: richer cosponsorship diagnostics.
- `proposalBondForfeiture`: average proposal-bond loss per potential bill.
- `strategicDecoyRate`: strategic clone/decoy alternatives introduced per tournament.
- `proposerAccessGini`: concentration of floor access across proposers.
- `welfarePerSubmittedBill`: public-benefit yield per potential proposal.
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
