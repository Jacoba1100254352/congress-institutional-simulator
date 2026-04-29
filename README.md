# Congress Institutional Simulator

This is a small agent-based simulator for testing how legislative rules shape cooperation, compromise, productivity, and gridlock.

The first version follows the main recommendation from the research report: start with a one-dimensional spatial legislature, a scalar status quo, proposers, and comparable institutional regimes before adding a kitchen-sink set of external systems.

The current model intentionally includes only the parts needed to compare institutional structures:

- legislators with ideology, party loyalty, constituency sensitivity, lobby susceptibility, reputation sensitivity, and compromise preference
- a current policy status quo that changes when bills are enacted
- bills proposed near a selected legislator's ideal point, with public support, lobby pressure, and salience
- voting strategies that compare a bill against the current status quo before reducing pressures to a final `YAY` or `NAY`
- pluggable institutional rules such as simple majority, supermajority passage, and default passage unless a veto bloc forms
- proposal-access screens, proposal-cost screens, committee information review, and committee gatekeeping
- legislative processes such as unicameral Congress, bicameral Congress, and a basic presidential veto wrapper
- aggregate metrics over many randomized runs

## Run

```sh
make run
```

With custom parameters:

```sh
make run ARGS="--runs 1000 --legislators 151 --bills 80 --party-count 4 --polarization 0.85 --compromise 0.35 --charts --seed 42"
```

Compare only selected scenarios:

```sh
make run ARGS="--scenarios default-pass,default-pass-guarded --format csv"
```

Run tests:

```sh
make test
```

Run the current predefined simulation campaign:

```sh
make campaign
```

This writes:

- `reports/simulation-campaign-v1.csv`
- `reports/simulation-campaign-v1.md`

The earlier v0 campaign remains available:

```sh
make campaign-v0
```

You can override the campaign defaults:

```sh
make campaign ARGS="--runs 300 --seed 12345"
```

Full usage documentation lives in [docs/usage.md](docs/usage.md).

## Current Scenarios

The default CLI compares:

- `simple-majority`: unicameral simple majority
- `supermajority-60`: unicameral 60 percent passage threshold
- `default-pass`: default passage unless 2/3 vote to block
- `default-pass-access`: default passage unless 2/3 vote to block, with a proposal-access screen
- `default-pass-cost`: default passage unless 2/3 vote to block, with a proposal-cost screen
- `default-pass-cost-guarded`: default passage with proposal costs, proposal access, committee information, and committee gatekeeping
- `default-pass-committee`: default passage unless 2/3 vote to block, with a representative committee gate
- `default-pass-committee-majority`: default passage with a majority-controlled committee gate
- `default-pass-committee-polarized`: default passage with a polarized committee gate
- `default-pass-committee-captured`: default passage with a lobby-sensitive/captured committee gate
- `default-pass-info`: default passage with representative committee information review
- `default-pass-info-expert`: default passage with expert-style committee information review
- `default-pass-info-captured`: default passage with captured/lobby-sensitive committee information review
- `default-pass-guarded`: default passage unless 2/3 vote to block, with both agenda filters
- `default-pass-informed-guarded`: default passage with access screening, committee information, and committee gatekeeping
- `bicameral-majority`: bicameral simple majority
- `presidential-veto`: bicameral majority with presidential veto and 2/3 override

## Experiment Controls

Use `make run ARGS="--help"` for the current command reference.

Core controls:

- `--runs`: randomized worlds per scenario
- `--legislators`: generated chamber size
- `--bills`: bills per run
- `--party-count`: number of generated party labels
- `--polarization`: ideological clustering from 0.0 to 1.0
- `--party-loyalty`: party-pressure sensitivity from 0.0 to 1.0
- `--compromise`: compromise culture from 0.0 to 1.0
- `--constituency`: constituent-pressure sensitivity from 0.0 to 1.0
- `--lobbying`: lobby-pressure sensitivity from 0.0 to 1.0
- `--scenarios`: comma-separated scenario keys
- `--format`: `table`, `csv`, or `bars`
- `--charts`: add ASCII bar charts after the table
- `--campaign`: run a named campaign, currently `v0` or `v1`
- `--output-dir`: campaign output directory

## Architecture

The simulator is designed around small strategy interfaces:

- `VotingStrategy`: how a legislator turns weighted pressures into `YAY` or `NAY`
- `VoteInfluence`: one source of pressure, such as ideology, party, constituency, lobbying, or compromise preference
- `VotingRule`: how chamber vote totals become pass/fail outcomes
- `ProposalAccessRule`: whether a potential bill can reach formal floor consideration
- `LegislativeProcess`: how one or more institutions consider a bill
- `Scenario`: a named institutional design to compare
- `PolicyState`: the current scalar status quo for the simulated policy space

To add a new system, implement one of those interfaces rather than rewriting the simulator engine.

Examples:

- proposal access: add a `ProposalAccessRule` and wrap a process with `ProposalAccessProcess`
- proposal costs: add a `ProposalAccessRule` that prices floor access by expected policy value, public credit, lobby support, or institutional scarcity
- committee gatekeeping: wrap a floor process with `CommitteeGatekeepingProcess`
- lobbying: add or replace a `VoteInfluence`
- shame/reputation: adjust `StandardInfluences.reputation`
- committees: add a `LegislativeProcess` that filters bills before chamber votes, or improves bill-quality estimates before members vote
- courts: add a `LegislativeProcess` wrapper after enactment
- elections: run multiple worlds over time and mutate legislator incentives between sessions

## Metrics

The first metric set is deliberately simple, but it separates throughput from legitimacy-oriented signals:

- `productivity`: share of introduced bills enacted
- `floor`: share of potential bills that reached floor consideration
- campaign reports also track `enactedPerRun` and `floorPerRun` so proposal flooding is visible as institutional load, not only as percentages
- `avgSupport`: average yay share for enacted bills
- `welfare`: average public-benefit score for enacted bills
- `cooperation`: productivity multiplied by enacted support
- `compromise`: rewards enacted bills that are moderate, broadly supported, and do not simply hand the proposer their ideal point
- `gridlock`: share of introduced bills that fail
- `accessD`: share of potential bills blocked by proposal-access rules
- `cmteRej`: share of potential bills rejected by a committee gate
- `lowSupport`: share of enacted bills with less than 50 percent yay support
- `popularFail`: share of high-public-support bills that fail
- `policyShift`: average absolute movement from the prior status quo
- `propGain`: average enacted movement toward the proposer's ideal point

These are not claims about real-world validity. They are hooks for comparing rule sets under shared assumptions.

## Research Direction

The research report found that the proposed default-pass rule has analogues in negative parliamentarism, WTO reverse consensus, EU reverse qualified majority rules, tacit-acceptance treaty procedures, silence procedures, and U.S. review-and-disapproval structures such as the Congressional Review Act and BRAC. It did not find a close mainstream analogue where ordinary statutes generally pass unless a two-thirds blocking coalition forms.

The main design warning is that default passage shifts power from affirmative majority formation to blocking coalition formation. That makes agenda access, proposal screening, proposer power, committees, and legitimacy metrics central. The first modeling layers therefore focus on agenda access, committee gatekeeping, committee information, and proposal costs before media, lobbying, elections, or richer behavioral systems.

That agenda layer is now represented in three comparison scenarios:

- `Default pass + proposal access screen`: denies floor access to bills with low public support or very large jumps away from the status quo.
- `Default pass + representative committee gate`: requires approval by a representative committee before the default-pass floor rule applies.
- `Default pass + access + committee`: applies both filters before the floor vote.

The committee-information layer adds committee composition and information:

- Committee presets can select representative, majority-controlled, polarized, expert-style, or captured/lobby-sensitive committees.
- `CommitteeInformationProcess` moves the noisy public-support signal toward a bill's generated public-benefit score before floor consideration.
- Information review can be tested independently or combined with access screening and committee gatekeeping.

The current v1 campaign adds proposal flooding and proposal costs:

- `default-pass-cost` screens floor access by comparing a proposal's expected proposer policy gain, public credit, and lobby credit against a fixed cost threshold.
- The flooding cases increase potential bills per run by 3x or 5x, with variants for high lobbying and low compromise.
- The first finding is mixed: proposal costs substantially reduce floor load and enactment volume, but the current cost formula also selects for high proposer gain and positive lobby pressure. That makes cost design itself a modeling target.
