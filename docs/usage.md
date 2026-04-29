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
- `--campaign <v0|v1|v2>`: run a named campaign.
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

- `reports/simulation-campaign-v2.csv`
- `reports/simulation-campaign-v2.md`

Earlier campaign:

- `reports/simulation-campaign-v0.csv`
- `reports/simulation-campaign-v0.md`
- `reports/simulation-campaign-v1.csv`
- `reports/simulation-campaign-v1.md`

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
- `challengeRate`: share of potential bills diverted from default enactment into active voting by challenge vouchers.
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
