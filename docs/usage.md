# Congress Institutional Simulator Usage

This document is the project-facing guide for running and extending the simulator.

## Requirements

- Java 17 or newer
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
- `--campaign <v0|v1|v2|v3|v4|v5|v6|v7>`: run a named campaign.
- `--output-dir <path>`: campaign artifact directory.
- `--seed <n>`: reproducible random seed.
- `--help`: print command help.

## Scenario Keys

The default CLI scenario set includes:

- `simple-majority`: unicameral simple majority.
- `supermajority-60`: unicameral 60 percent passage threshold.
- `default-pass`: default passage unless two-thirds vote to block.
- `default-pass-challenge`: default passage with scarce party-held challenge vouchers.
- `default-pass-challenge-info`: default passage with committee information before challenge-voucher decisions.
- `default-pass-cross-bloc`: default passage with a cross-bloc cosponsorship agenda gate.
- `default-pass-cross-bloc-strong`: default passage with a stricter cross-bloc cosponsorship gate.
- `default-pass-cross-bloc-challenge`: cross-bloc cosponsorship before challenge-voucher review.
- `default-pass-adaptive-track`: adaptive procedural routing with low-risk, middle, and high-risk lanes.
- `default-pass-adaptive-track-challenge`: adaptive routing with challenge vouchers in the middle-risk lane.
- `default-pass-sunset-trial`: provisional enactment plus automatic sunset review for risky bills.
- `default-pass-sunset-challenge`: challenge vouchers plus sunset review.
- `default-pass-earned-credits`: stateful agenda credits earned or lost through proposal quality.
- `default-pass-earned-credits-challenge`: earned proposal credits plus challenge vouchers.
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

- `reports/simulation-campaign-v7.csv`
- `reports/simulation-campaign-v7.md`

Earlier campaign:

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
- Register the new scenario in `src/main/java/congresssim/simulation/ScenarioCatalog.java`.
- Add focused coverage in `src/test/java/congresssim/SimulatorTests.java`.

After changing behavior, run:

```sh
make test
make campaign
```
