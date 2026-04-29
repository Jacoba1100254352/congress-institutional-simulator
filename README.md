# Congress Institutional Simulator

This is a small individual-legislator simulator for testing how possible legislative systems shape compromise, productivity, public responsiveness, and gridlock.

The first version starts with a deliberately simple legislature: one-dimensional policy space, a scalar status quo, proposers, and comparable institutional regimes. Default passage is included as one stress-test family, but the project goal is broader: search across many possible legislative frameworks and measure which ones best balance compromise, productivity, and representative responsiveness.

The current model intentionally includes only the parts needed to compare institutional structures:

- legislators with ideology, party loyalty, constituency sensitivity, lobby susceptibility, reputation sensitivity, and compromise preference
- a current policy status quo that changes when bills are enacted
- bills proposed near a selected legislator's ideal point, with public support, lobby pressure, and salience
- voting strategies that compare a bill against the current status quo before reducing pressures to a final `YAY` or `NAY`
- pluggable institutional rules such as simple majority, supermajority passage, and default passage unless a veto bloc forms
- proposal-access screens, proposal-cost screens, earned proposal credits, committee information review, and committee gatekeeping
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

- `reports/simulation-campaign-v10.csv`
- `reports/simulation-campaign-v10.md`

Earlier campaigns remain available:

```sh
make campaign-v0
make campaign-v1
make campaign-v2
make campaign-v3
make campaign-v4
make campaign-v5
make campaign-v6
make campaign-v7
make campaign-v8
make campaign-v9
make campaign-v10
```

You can override the campaign defaults:

```sh
make campaign ARGS="--runs 300 --seed 12345"
```

Full usage documentation lives in [docs/usage.md](docs/usage.md).

## Current Scenarios

The default CLI compares:

- `simple-majority`: unicameral simple majority
- `simple-majority-mediation`: unicameral simple majority with a structured amendment/mediation stage
- `simple-majority-lobby-firewall`: unicameral majority with reduced direct lobby vote influence
- `supermajority-60`: unicameral 60 percent passage threshold
- `default-pass`: default passage unless 2/3 vote to block
- `default-pass-mediation`: default passage after a bounded mediation stage can move risky bills toward the median/status quo
- `default-pass-lobby-firewall`: default passage with reduced direct lobby vote influence
- `default-pass-lobby-transparency`: default passage after disclosure weakens effective lobby pressure and creates backlash against capture-risk bills
- `default-pass-public-interest-screen`: default passage with an anti-capture public-interest access screen
- `default-pass-lobby-audit`: default passage with randomized anti-capture audits and sponsor sanctions
- `default-pass-anti-capture-bundle`: transparency, public-interest screening, audit sanctions, and lower direct lobby vote influence
- `default-pass-budgeted-lobbying`: default passage after explicit lobby groups spend limited budgets by issue domain
- `default-pass-budgeted-lobbying-transparency`: budgeted lobbying followed by transparency backlash
- `default-pass-budgeted-lobbying-bundle`: budgeted lobbying with transparency, public-interest screening, audits, and lower direct lobby vote influence
- `default-pass-budgeted-lobbying-mediation`: budgeted lobbying followed by bounded amendment mediation
- `default-pass-challenge`: default passage with scarce party-held challenge vouchers that divert contested bills to active majority vote
- `default-pass-challenge-info`: default passage with committee information review before challenge-voucher decisions
- `default-pass-cross-bloc`: default passage with a cross-bloc cosponsorship agenda gate
- `default-pass-cross-bloc-strong`: stricter cross-bloc cosponsorship gate
- `default-pass-cross-bloc-challenge`: cross-bloc cosponsorship before challenge-voucher review
- `default-pass-adaptive-track`: risk-routed default pass with low-risk, middle, and high-risk procedural lanes
- `default-pass-adaptive-track-challenge`: adaptive tracks with challenge vouchers in the middle-risk lane
- `default-pass-sunset-trial`: default passage with provisional enactment and automatic sunset review for risky bills
- `default-pass-sunset-challenge`: challenge vouchers plus sunset review
- `default-pass-earned-credits`: default passage with stateful agenda credits earned or lost through proposal quality
- `default-pass-earned-credits-challenge`: earned proposal credits plus challenge vouchers
- challenge-sweep keys such as `default-pass-challenge-party-t3-s082`, `default-pass-challenge-member-t1-s082`, and `default-pass-escalation-q12-s082`
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
- `--campaign`: run a named campaign, currently `v0`, `v1`, `v2`, `v3`, `v4`, `v5`, `v6`, `v7`, `v8`, `v9`, or `v10`
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
- anti-capture: wrap a process with `LobbyTransparencyProcess`, `LobbyAuditProcess`, or a `PublicInterestScreenAccessRule`
- shame/reputation: adjust `StandardInfluences.reputation`
- committees: add a `LegislativeProcess` that filters bills before chamber votes, or improves bill-quality estimates before members vote
- courts: add a `LegislativeProcess` wrapper after enactment
- elections: run multiple worlds over time and mutate legislator incentives between sessions

## Metrics

The first metric set is deliberately simple, but it separates throughput from legitimacy-oriented signals:

- `productivity`: share of introduced bills enacted
- `floor`: share of potential bills that reached floor consideration
- campaign reports also track `enactedPerRun` and `floorPerRun` so proposal flooding is visible as institutional load, not only as percentages
- `challengeRate`: share of potential bills diverted from default enactment into active voting by challenge vouchers or q-member challenge escalation
- `avgSupport`: average yay share for enacted bills
- `welfare`: average public-benefit score for enacted bills
- `cooperation`: a legacy throughput-support metric, not a unity score
- `compromise`: the more important target metric; it rewards enacted bills that are moderate, broadly supported, and do not simply hand the proposer their ideal point
- `gridlock`: share of introduced bills that fail
- `accessD`: share of potential bills blocked by proposal-access rules
- `cmteRej`: share of potential bills rejected by a committee gate
- `lowSupport`: share of enacted bills with less than 50 percent yay support
- `popularFail`: share of high-public-support bills that fail
- `policyShift`: average absolute movement from the prior status quo
- `propGain`: average enacted movement toward the proposer's ideal point
- `lobbyCapture`: average enacted-bill capture risk from positive lobby pressure, private gain, and weak public value
- `publicAlignment`: how closely enacted voting support tracks generated public support
- `antiLobbyingSuccess`: share of generated anti-lobbying reform bills enacted
- `privateGainRatio`: enacted private gain relative to generated public benefit
- `lobbySpendPerBill`: explicit lobby-group spend per potential bill
- `defensiveLobbyingShare`: share of lobby spend aimed at defeating anti-lobbying reform bills
- `captureReturnOnSpend`: enacted capture risk per unit of explicit lobby spend
- `publicPreferenceDistortion`: average gap between enacted yes-share and generated public support
- `amendmentRate`: share of potential bills whose policy position moved during mediation
- `amendmentMovement`: average absolute policy movement created by mediation per potential bill

These are not claims about real-world validity. They are hooks for comparing rule sets under shared assumptions.

## Research Direction

The research direction is comparative institutional search. The simulator should be able to test ordinary legislative systems, default-pass systems, cross-bloc systems, challenge-token systems, adaptive-track systems, sunset/review systems, and more radical future proposals under shared assumptions.

Default passage remains useful as an early stress test because it sharply shifts power from affirmative majority formation to blocking coalition formation. The broader design warning is that every legislative structure depends on agenda access, proposal screening, proposer power, information, challenge rights, reversibility, and legitimacy metrics. The first modeling layers therefore focus on those institutional mechanics before media, elections, or richer behavioral systems.

The early agenda layer is represented in three comparison scenarios:

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

The v2 campaign adds challenge vouchers:

- `default-pass-challenge` gives each party a scarce challenge-token budget; unchallenged bills default enact, while challenged bills go to active majority vote.
- `default-pass-challenge-info` first lets a representative committee improve the public-support signal, then applies the same challenge-voucher mechanism.
- This tests whether default-pass can keep some throughput advantage while forcing the most contested bills into a stronger affirmative-vote path.

The v3 campaign sweeps challenge mechanics:

- party token budgets: 3, 6, 10, 15, and 25 tokens per party at the baseline challenge threshold
- challenge thresholds: 0.50, 0.65, 0.82, 1.00, and 1.25 with 10 party tokens
- member token budgets: 1, 2, and 3 tokens per legislator
- tokenless escalation: q-member challenge thresholds at q=6, q=12, and q=20
- The finding is a throughput/safety frontier: low token budgets preserve or even increase throughput but barely reduce low-support passage, while member-token and q-member escalation variants cut low-support passage and policy shift much more at a large productivity cost.

The v4 campaign adds cross-bloc cosponsorship gates:

- `default-pass-cross-bloc` requires credible support from at least two legislators outside the proposer bloc before a bill reaches default-pass consideration.
- `default-pass-cross-bloc-strong` raises the cosponsorship burden to test a stricter coalition-breadth screen.
- `default-pass-cross-bloc-challenge` combines the cross-bloc agenda gate with challenge vouchers.
- The finding is that coalition breadth is a strong upstream filter: it improves enacted-bill welfare and sharply reduces policy shift and proposer gain, but it also cuts floor access enough that adaptive routing became the next important model feature.

The v5 campaign adds adaptive procedural tracks:

- `default-pass-adaptive-track` sends low-risk bills to default pass, middle-risk bills to active simple-majority review, and high-risk bills to informed guardrails.
- `default-pass-adaptive-track-challenge` keeps the same fast and high-risk lanes, but sends middle-risk bills through challenge-voucher review.
- The finding is that adaptive routing provides a middle path: it preserves far more floor access than cross-bloc or informed guardrails while reducing low-support passage, policy shift, and proposer gain relative to open default-pass.

The v6 campaign adds sunset trial legislation:

- `default-pass-sunset-trial` provisionally enacts risky default-pass bills, then automatically renews or expires them using generated public support, public benefit, lobby risk, and risk score.
- `default-pass-sunset-challenge` combines the same sunset review with challenge vouchers.
- The current finding is that reversibility improves enacted-bill welfare and sharply reduces policy shift without using a front-end agenda gate, but it still reduces productivity because failed review rolls the status quo back.

The v7 campaign adds earned proposal credits:

- `default-pass-earned-credits` gives proposers stateful agenda credits. A proposal spends credits according to risk, lobby pressure, salience, and public value; after consideration, the proposer earns or loses credits based on generated public benefit, public support, lobby risk, and outcome quality.
- `default-pass-earned-credits-challenge` combines the same credit budget with challenge-voucher review.
- The current finding is that earned credits reduce floor load and policy shift more gently than cross-bloc or committee gates. The base credit scenario denies about 20 percent of potential proposals, improves welfare by 0.015, reduces policy shift by 0.159, and reduces proposer gain by 0.032 relative to open default-pass. Combining credits with challenge vouchers is stricter: productivity falls by 0.398, but policy shift falls by 0.416 and proposer gain by 0.191.

The v8 campaign adds anti-capture stress tests:

- Bill generation now includes ordinary private-gain bills and explicit anti-lobbying reform bills that face negative lobby pressure.
- `simple-majority-lobby-firewall` and `default-pass-lobby-firewall` reduce direct lobby influence in legislator voting while increasing public/reputation pressure.
- `default-pass-lobby-transparency` exposes lobbying pressure before consideration, reducing effective lobby pressure and creating public backlash against high-capture proposals.
- `default-pass-public-interest-screen` denies high-capture, low-public-interest proposals while allowing public-benefit anti-lobbying reforms through the agenda gate.
- `default-pass-lobby-audit` randomly audits enacted high-capture bills, can reverse failed audits, and sanctions repeat sponsors.
- `default-pass-anti-capture-bundle` combines transparency, public-interest screening, audit sanctions, and a lower-lobby voting strategy.

The v9 campaign adds explicit lobbying actors:

- `LobbyGroup` actors have issue domains, budgets, preferred policy positions, influence intensity, defensive multipliers, information bias, and public-campaign skill.
- `BudgetedLobbyingProcess` lets groups spend limited budgets to boost favored private-gain bills and spend defensively against anti-lobbying reform.
- Campaign reports now distinguish ordinary capture pressure from explicit spending, defensive spending, capture return on spend, and public-preference distortion.

The current v10 campaign adds structured amendment mediation:

- `AmendmentMediationProcess` wraps a floor process and, when bills are risky or weakly supported, moves the bill toward a weighted target based on the chamber median, current status quo, and proposer position.
- Mediation variants test simple majority, open default-pass, and budgeted-lobbying default-pass against their non-mediated counterparts.
- Campaign reports now include amendment rate and amendment movement so compromise can be measured as pre-vote content change, not only final yes/no support.
