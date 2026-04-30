# Congress Institutional Simulator

This is a small individual-legislator simulator for testing how possible legislative systems shape compromise, productivity, public responsiveness, and gridlock.

The first version starts with a deliberately simple legislature: one-dimensional policy space, a scalar status quo, proposers, and comparable institutional regimes. Default passage is included as one stress-test family, but the project goal is broader: search across many possible legislative frameworks and measure which ones best balance compromise, productivity, and representative responsiveness.

The current model intentionally includes only the parts needed to compare institutional structures:

- legislators with ideology, party loyalty, district/public-will signals, constituency sensitivity, lobby susceptibility, reputation sensitivity, and compromise preference
- a current policy status quo that changes when bills are enacted
- bills proposed near a selected legislator's ideal point, with public support, public-benefit uncertainty, affected-group harm, lobby pressure, and salience
- voting strategies that compare a bill against the current status quo before reducing pressures to a final `YAY` or `NAY`
- pluggable institutional rules such as simple majority, supermajority passage, and default passage unless a veto bloc forms
- proposal-access screens, proposal-cost screens, refundable proposal bonds, earned proposal credits, committee information review, and committee gatekeeping
- legislative processes such as unicameral Congress, bicameral Congress, and a basic presidential veto wrapper
- explicit proposer and lobby-group adaptation over repeated bills, including proposal pacing, timing delay, risk tolerance, amendment posture, channel learning, issue-specific budget adaptation, and defensive anti-reform lobbying
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
make run ARGS="--scenarios current-system,simple-majority,simple-majority-alternatives-pairwise,risk-routed-majority,default-pass --format csv"
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

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/simulation-campaign-v21-paper-manifest.json`

Run empirical benchmark screening:

```sh
make calibrate
```

This writes:

- `reports/calibration-baseline.csv`
- `reports/calibration-baseline.md`
- `reports/calibration-baseline-manifest.json`

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
make campaign-v11
make campaign-v12
make campaign-v13
make campaign-v14
make campaign-v15
make campaign-v16
make campaign-v17
make campaign-v18
make campaign-v19
make campaign-v20
make campaign-v21-paper
```

You can override the campaign defaults:

```sh
make campaign ARGS="--runs 300 --seed 12345"
```

Full usage documentation lives in [docs/usage.md](docs/usage.md).
Calibration and validation details live in [docs/calibration.md](docs/calibration.md), the concise ODD-style model description lives in [docs/odd-model.md](docs/odd-model.md), and the full ODD+D appendix lives in [docs/odd-d-appendix.md](docs/odd-d-appendix.md).

## Current Scenarios

The default CLI and v21 paper campaign now use a representative breadth-first set. Default passage is deliberately kept to three stress-test variants rather than treated as the main family:

- `current-system`: stylized current U.S. benchmark
- `simple-majority`: unicameral simple majority
- `supermajority-60`: unicameral 60 percent passage threshold
- `bicameral-majority`: bicameral simple majority
- `presidential-veto`: bicameral majority with presidential veto and 2/3 override
- `committee-regular-order`: committee-first regular order under affirmative majority rule
- `parliamentary-coalition-confidence`: cross-bloc confidence/access discipline
- `simple-majority-alternatives-pairwise`: pairwise policy tournament before majority ratification
- `simple-majority-alternatives-strategic`: policy tournament with strategic clones and decoys
- `citizen-assembly-threshold`: mini-public review changes the burden of proof
- `public-interest-majority`: affirmative majority with public-interest agenda screening
- `agenda-lottery-majority`: weighted agenda lottery with majority ratification
- `quadratic-attention-majority`: quadratic attention budget with majority ratification
- `proposal-bond-majority`: refundable proposal accountability bond
- `harm-weighted-majority`: concentrated-harm thresholds
- `compensation-majority`: compensation amendments for concentrated harm
- `law-registry-majority`: active-law review and correction
- `public-objection-majority`: public objection window before majority ratification
- `anti-capture-majority-bundle`: lobbying transparency, public advocate, audit, and screen bundle
- `risk-routed-majority`: adaptive risk lanes under majority rule
- `default-pass`: default passage unless 2/3 vote to block
- `default-pass-challenge`: default passage with scarce challenge vouchers
- `default-pass-multiround-mediation-challenge`: default passage with mediation plus challenge vouchers

The full catalog still exposes the earlier default-pass sweeps for side analysis, including challenge-token sweeps, committee variants, lobbying variants, citizen-panel variants, and default-pass law-registry variants. Use `make run ARGS="--help"` to list all explicit keys, or pass keys with `--scenarios` to recreate those historical comparisons.

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
- `--calibrate`: run empirical benchmark screening from `data/calibration/empirical-benchmarks.csv`
- `--campaign`: run a named campaign, currently `v0` through `v21-paper`
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

Metric direction is explicit:

- `↑` higher is generally better.
- `↓` lower is generally better; directional comparisons invert these before combining them.
- `diag.` means the value is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.
- `directionalScore` is a reader aid that averages `productivity`, `representativeQuality`, and `riskControl`. `representativeQuality` averages welfare, enacted support, compromise, public alignment, and legitimacy. `riskControl` inverts low-support passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.

- `productivity` `↑`: share of introduced bills enacted
- `floor` `diag.`: share of potential bills that reached floor consideration
- `caseWeight` `diag.`: likelihood weight used by sensitivity campaigns; ordinary campaigns use `1.0`
- campaign reports also track `enactedPerRun` and `floorPerRun` `diag.` so proposal flooding is visible as institutional load, not only as percentages
- `directionalScore` `↑`, `representativeQuality` `↑`, and `riskControl` `↑`: derived display scores that orient mixed-sign metrics in the same direction
- `challengeRate` `diag.`: share of potential bills diverted from default enactment into active voting by challenge vouchers or q-member challenge escalation
- `avgSupport` `↑`: average yay share for enacted bills
- `welfare` `↑`: average public-benefit score for enacted bills
- `cooperation` `↑`: a legacy throughput-support metric, not a unity score
- `compromise` `↑`: the more important target metric; it rewards enacted bills that are moderate, broadly supported, and do not simply hand the proposer their ideal point
- `gridlock` `↓`: share of introduced bills that fail
- `accessD` `diag.`: share of potential bills blocked by proposal-access rules
- `cmteRej` `diag.`: share of potential bills rejected by a committee gate
- `lowSupport` `↓`: share of enacted bills with less than 50 percent yay support
- `popularFail` `↓`: share of high-public-support bills that fail
- `policyShift` `diag.`: average absolute movement from the prior status quo; high values may mean useful reform or uncontrolled volatility depending on context
- `propGain` `↓`: average enacted movement toward the proposer's ideal point
- `lobbyCapture` `↓`: average enacted-bill capture risk from positive lobby pressure, private gain, and weak public value
- `publicAlignment` `↑`: how closely enacted voting support tracks generated public support
- `antiLobbyingSuccess` `↑`: share of generated anti-lobbying reform bills enacted
- `privateGainRatio` `↓`: enacted private gain relative to generated public benefit
- `lobbySpendPerBill` `diag.`: explicit lobby-group spend per potential bill
- `defensiveLobbyingShare` `diag.`: share of lobby spend aimed at defeating anti-lobbying reform bills
- `captureReturnOnSpend` `↓`: enacted capture risk per unit of explicit lobby spend
- `publicPreferenceDistortion` `↓`: average gap between enacted yes-share and generated public support
- `amendmentRate` `diag.`: share of potential bills whose policy position moved during mediation
- `amendmentMovement` `diag.`: average absolute policy movement created by mediation per potential bill
- `selectedAlternativeMedianDistance` `↓`: average distance between selected alternatives and the chamber median
- `proposerAgendaAdvantage` `↓`: average selected-alternative movement toward the original proposer's ideal point
- `alternativeDiversity` `diag.`: average number of alternatives/status quo options considered per tournament
- `statusQuoWinRate` `diag.`: share of policy tournaments where the status quo blocks final ratification
- `citizenReviewRate` `diag.`: share of potential bills reviewed by a synthetic citizen panel
- `citizenCertificationRate` `↑`: share of reviewed bills receiving a positive citizen-panel certificate
- `citizenLegitimacy` `↑`: average legitimacy estimate from citizen-panel review
- `attentionSpendPerBill` `diag.`: quadratic attention credits spent per potential bill
- `objectionWindowRate` `diag.`: share of potential bills triggering a public objection or repeal window
- `repealWindowReversalRate` `diag.`: share of triggered repeal windows that reverse enactment
- `fastLaneRate`, `middleLaneRate`, `highRiskLaneRate` `diag.`: adaptive-route shares
- `challengeExhaustionRate` `↓`: share of potential bills where a challenge would have cleared threshold but no token was available
- `falseNegativePassRate` `↓`: risky, low-support, or high-harm default enactments that passed unchallenged
- `publicWillReviewRate`, `publicSignalMovement` `diag.`, `districtAlignment` `↑`: constituent/public-will review diagnostics
- `crossBlocAdmissionRate`, `affectedGroupSponsorshipRate`, `averageCosponsors` `diag.`: richer cosponsorship diagnostics
- `proposalBondForfeiture` `diag.`: average proposal-bond loss per potential bill
- `strategicDecoyRate` `↓`: strategic clone/decoy alternatives introduced per tournament
- `proposerAccessGini` `↓`: concentration of floor access across proposers
- `welfarePerSubmittedBill` `↑`: public-benefit yield per potential proposal

These are not claims about real-world validity. They are hooks for comparing rule sets under shared assumptions.

## Research Direction

The research direction is comparative institutional search. The simulator should be able to test ordinary legislative systems, default-pass systems, cross-bloc systems, challenge-token systems, adaptive-track systems, sunset/review systems, and more radical future proposals under shared assumptions.

Default passage remains useful as an early stress test because it sharply shifts power from affirmative majority formation to blocking coalition formation. The broader design warning is that every legislative structure depends on agenda access, proposal screening, proposer power, information, challenge rights, reversibility, and legitimacy metrics. The first modeling layers therefore focus on those institutional mechanics before media, elections, or richer behavioral systems.

The following campaign notes are historical side logs. They explain how earlier default-pass-heavy iterations were developed, but the current paper campaign is the breadth-first v21 comparison above.

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

The v10 campaign adds structured amendment mediation:

- `AmendmentMediationProcess` wraps a floor process and, when bills are risky or weakly supported, moves the bill toward a weighted target based on the chamber median, current status quo, and proposer position.
- Mediation variants test simple majority, open default-pass, and budgeted-lobbying default-pass against their non-mediated counterparts.
- Campaign reports now include amendment rate and amendment movement so compromise can be measured as pre-vote content change, not only final yes/no support.

The v11 campaign adds distributional harm and affected groups:

- Bills now include an affected group, affected-group support, concentrated-harm score, and compensation cost.
- `default-pass-harm-threshold` routes concentrated-harm bills to a higher affirmative threshold.
- `default-pass-compensation` lets high-harm bills receive compensation amendments that reduce concentrated harm at some public-benefit cost.
- `default-pass-affected-consent` adds an affected-group support requirement after compensation.
- Campaign reports now include minority harm, concentrated-harm passage, compensation rate, and legitimacy.

The v12 campaign adds a multi-session law registry:

- `LawRegistryProcess` records risky enacted laws as active provisional laws with a later review date.
- Due laws are renewed or repealed based on public benefit, public support, affected-group support, and risk.
- Repealed laws roll back part of their status-quo movement, making correction and instability measurable.
- Campaign reports now include active-law welfare, reversal rate, time to correction, and low-support active-law share.

The v13 campaign adds competing alternatives and policy tournaments:

- `CompetingAlternativesProcess` generates same-domain alternatives before final yes/no ratification.
- Selection variants choose alternatives by public benefit, public support, chamber-median distance, or pairwise majority performance.
- `default-pass-obstruction-substitute` models a limited constructive opposition right: opposition can force a substitute into the comparison instead of only blocking.
- Campaign reports now include selected-alternative median distance, proposer agenda advantage, alternative diversity, and status-quo win rate.

The v14 campaign deepens lobbying:

- `LobbyGroup` actors now have richer issue-preference maps, capture strategies, and public-support mismatch tolerance.
- `BudgetedLobbyingProcess` allocates spending across direct pressure, agenda access, information distortion, public campaigns, litigation/delay threats, and defensive anti-reform pressure.
- New scenarios test democracy vouchers/public financing, equal-access public advocates, blind sponsor/lobby-origin review, defensive lobbying caps, and a combined channel anti-capture bundle.
- Campaign reports now include public benefit per lobby dollar and channel-specific spend shares.

The v15 campaign adds citizen mini-public review:

- `CitizenPanelReviewProcess` inserts a synthetic deliberative citizen panel before final routing.
- Panel review models sampling noise, information quality, manipulation risk, public support, public benefit, affected-group support, and concentrated harm.
- New scenarios test certificate-gated default passage, active-vote routing for uncertified bills, threshold adjustment, and softer agenda-priority review.
- Campaign reports now include citizen review rate, certification rate, and panel legitimacy.

The v16 campaign adds agenda-scarcity variants:

- `AgendaLotteryProcess` admits a bounded share of bills by weighted or random draw.
- `QuadraticAttentionBudgetProcess` makes proposal access consume scarce credits with increasing marginal cost.
- `PublicObjectionWindowProcess` routes contested bills to active voting or rolls back contested default enactments.
- Campaign reports now include attention spend, objection-window rate, and repeal-window reversal rate.

The v17 campaign completes the planned roadmap layer:

- `ConstituentPublicWillProcess` grounds public signals in generated district preferences, intensity, and affected-group sensitivity.
- `ProposalBondProcess` adds refundable public-benefit proposer bonds and records forfeiture.
- `CoalitionCosponsorshipProcess` records cosponsor counts, outside-bloc admissions, affected-group sponsors, and coalition support discounts.
- `MultiRoundAmendmentProcess` adds multi-round mediation with round costs, concession limits, poison-pill risk, and compensation.
- `ProposerStrategyProcess` lets proposers moderate risky bills, seek outside-bloc cosponsorship, and withdraw repeated low-trust proposals.
- Strategic budgeted lobbying lets lobby groups reallocate influence strategies across direct pressure, agenda access, information distortion, public campaigns, and litigation/delay threats after observing outcomes.
- Challenge vouchers now include proportional and minority-bonus party allocation plus supermajority, committee, and information-active challenged paths.
- Adaptive tracks now report fast/middle/high route rates and include lenient, strict, citizen high-risk, and supermajority high-risk variants.
- Proposal-cost variants include public-value waivers, lobby-pressure surcharges, and stateful member quotas.

The v18 campaign adds weighted party-system sensitivity:

- `PartySystemProfile` lets generated worlds use ideological bins, two major parties with minor parties, dominant-party legislatures, or fragmented multiparty legislatures.
- `WorldGenerator` assigns profile-specific party seat shares before sorting parties along the ideological range.
- Campaign rows include `caseWeight`, and scenario averages are weighted when the campaign defines non-unit case likelihoods.
- The tracked v18 sensitivity mix is 0.25 two-party, 0.40 two-major-plus-minors, 0.20 fragmented multiparty, and 0.15 dominant party.

The v19 campaign adds timeline stress comparisons:

- Six stylized eras raise polarization, party loyalty, lobbying pressure, and proposal pressure while lowering compromise culture and constituency responsiveness.
- The campaign includes the current U.S.-style benchmark alongside conventional affirmative systems, open default-pass, challenge vouchers, public panels, adaptive tracks, policy tournaments, public objection, and law-registry review.
- The generated report includes a contention path using `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * lowSupport`.
- The timeline is a stress test, not a historical calibration; it asks which institutional systems degrade gracefully as background politics become more contentious.

The v20 campaign adds focused strategy and calibration comparisons:

- It carries forward the current-system benchmark and conventional affirmative baselines.
- It compares strategic lobbying, adaptive proposers, adaptive proposers with strategic lobbying, and the combined deep strategy bundle.
- The deep strategy bundle combines proposer pacing/risk adaptation, lobby-channel learning, issue-budget adaptation, defensive anti-reform behavior, and multi-round mediation.
- Use it with `make campaign-v20`.

The current v21-paper campaign is the canonical paper evidence base:

- It combines broad assumption cases, weighted party-system sensitivity cases, and rising-contention timeline cases in one CSV.
- It is breadth-first: current-system and conventional affirmative baselines, committee regular order, coalition confidence, policy tournaments, citizen review, public-interest screening, agenda lotteries, quadratic attention, proposal bonds, harm and compensation rules, public objection, law-registry review, anti-capture safeguards, risk routing, and a small default-pass stress-test family.
- Use it with `make campaign` or `make campaign-v21-paper`.
