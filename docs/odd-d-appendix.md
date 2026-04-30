# ODD+D Appendix

This appendix follows the ODD and ODD+D model-description style for the congressional institutional simulator. It is written as a submission supplement rather than a user guide.

## 1. Purpose

The model compares legislative institutional designs under shared generated political worlds. The scientific purpose is to search for institutional mechanisms that improve compromise and productivity while preserving representative responsiveness, public-benefit alignment, minority protection, and resistance to capture.

The model is not intended to forecast a specific Congress. It is a mechanism-search simulator: the same generated actors and bills are routed through many institutional systems so differences can be attributed to procedural rules and incentive structures.

## 2. Entities And State Variables

**Legislators**

Legislators have an ID, party, ideology, compromise preference, party loyalty, constituency sensitivity, lobbying susceptibility, reputation sensitivity, district preference, district intensity, and affected-group sensitivity. These variables determine how legislators weigh ideology, party pressure, public support, lobbying pressure, compromise incentives, and concentrated harm when casting a final yes-or-no vote.

**Bills**

Bills have an ID, title, proposer ID, proposer ideology, current policy position, original policy position, public support, public benefit, public-benefit uncertainty, lobby pressure, private gain, salience, issue domain, anti-lobbying reform flag, cosponsor counts, affected-group identity, affected-group support, concentrated harm, compensation cost, amendment movement, lobbying spend channels, challenge status, citizen-review signals, law-review status, and alternative-selection signals.

**Lobby Groups**

Lobby groups have an ID, primary issue domain, issue-preference map, preferred policy position, budget, influence intensity, defensive multiplier, information bias, public-campaign skill, capture strategy, and public-support mismatch tolerance. Lobby groups can spend through direct pressure, agenda access, information distortion, public campaigns, litigation/delay threats, and defensive spending against anti-lobbying reform.

**Institutions**

Institutional scenarios are composed from legislative-process modules. A process may screen proposal access, modify public signals, allocate lobbying or attention spending, route bills to different tracks, mediate amendments, evaluate affected-group harm, select among alternatives, conduct votes, apply vetoes, register enacted laws, or review laws later.

The main comparison now also includes a synthesized portfolio hybrid. It combines a low-risk fast lane, middle-risk pairwise alternatives and mediation, high-risk citizen and distributional-harm review, proposal bonds, anti-capture safeguards, and law-registry correction. It is a testable institutional hypothesis derived from earlier campaign comparisons, not an assumed optimum.

**Environment**

The environment is a one-dimensional policy space from `-1.0` to `1.0`, a scalar status quo, a generated bill stream, generated lobby groups, and party-system parameters. Most support, benefit, harm, legitimacy, and sensitivity values are ratios from `0.0` to `1.0`.

## 3. Process Overview And Scheduling

Each simulation run proceeds as follows:

1. Generate a world with legislators, parties, lobby groups, a status quo, and a bill stream.
2. Build each scenario's legislative process from that same generated world.
3. For each bill, create a deterministic vote context containing party positions, status quo, and seeded randomness.
4. Pass the bill through the scenario's process chain.
5. Record the final `BillOutcome`, including agenda disposition, votes, enactment, amendments, challenges, lobbying signals, review signals, and policy movement.
6. Update the scenario's status quo when the process enacts or rolls back policy.
7. Aggregate run-level outcomes into scenario metrics.

Campaigns repeat this over many runs and many assumption cases. Scenarios receive shared worlds but independent deterministic random streams, enabling paired comparisons among rules.

## 4. Design Concepts

**Basic Principles**

The model assumes legislative outcomes depend on proposal access, agenda scarcity, voting thresholds, committee and information structures, lobbying and capture, amendment opportunities, public review, minority harm, reversibility, and strategic actor adaptation.

**Emergence**

System-level productivity, compromise, capture, volatility, legitimacy, and gridlock emerge from many bill-by-bill interactions. No global actor optimizes these metrics directly.

**Adaptation**

Proposers adapt over repeated bills. They can reduce proposal volume, delay timing, moderate risky bills, seek outside-bloc cosponsorship, reduce lobby exposure, add compensation amendments, lower risk tolerance after bad outcomes, and withdraw weak risky bills.

Lobby groups adapt over repeated bills. They track returns by channel, reallocate among capture strategies, change issue-specific budget multipliers, adjust overall budget intensity, increase reform-threat sensitivity when anti-lobbying bills appear viable, and maintain defensive pressure against lobbying reforms.

Institutional state also adapts through proposal credits, proposal bonds, law registries, sunset reviews, challenge-token exhaustion, attention-token spending, and active-law review.

**Objectives**

Legislators seek voting outcomes that fit their weighted incentives. Proposers seek agenda access and enactment while learning to avoid reputational or procedural failure. Lobby groups seek policy movement toward their issue preferences and private benefits while resisting anti-lobbying reforms. Institutions do not have a single objective function; they impose rule constraints that shape actor incentives.

**Learning**

Learning is deterministic and lightweight. It uses bounded state updates rather than full reinforcement learning. Proposer state includes trust, proposal pace, risk tolerance, concession rate, lobby exposure, cooldown, and streak counters. Lobby state includes learned channel returns, issue multipliers, budget multipliers, and reform-threat multipliers.

**Prediction**

Actors do not forecast the entire chamber. Proposers and lobby groups use local outcome signals: enactment, public support, public benefit, capture risk, concentrated harm, salience, private gain, and prior success.

**Sensing**

Actors sense bill-level public support, public benefit, salience, lobby pressure, policy position, affected-group support, and concentrated harm. Some institutions simulate imperfect information through committee-information noise, citizen-panel sampling noise, public-will signal movement, and lobbying information distortion.

**Interaction**

Interaction occurs through voting, proposal access, cosponsorship, challenge tokens, amendment mediation, lobbying influence, public review, affected-group consent, alternative selection, and law-review correction.

**Stochasticity**

World generation, committee composition, citizen panels, bill values, party-system profiles, and some routing decisions use seeded randomness. Runs are reproducible with the same seed.

**Collectives**

Parties and blocs are modeled through party labels, party positions, party loyalty, challenge-token allocation, outside-bloc cosponsorship, and party-system profiles. Lobby groups are collective actors with issue maps and budgets.

**Observation**

The model reports productivity, floor load, enacted support, public-benefit proxy, cooperation, compromise, gridlock, access denial, committee rejection, challenge rate, chamber low-support passage, weak public-mandate passage, administrative cost, policy shift, proposer gain, lobby capture, public alignment, anti-lobbying success, private-gain ratio, lobbying spend by channel, public benefit per lobby dollar, amendment rate, amendment movement, minority harm, concentrated-harm passage, compensation rate, legitimacy, law-review metrics, alternative-selection metrics, citizen-review metrics, agenda-scarcity metrics, adaptive-track route rates, false-negative default passage, public-will review, district alignment, cosponsorship, bond forfeiture, strategic decoys, proposer-access Gini, welfare per submitted bill, vetoes, and overrides.

## 5. Initialization

`WorldGenerator` creates:

- legislators from party-system profile and ideological distribution parameters;
- party positions derived from generated legislator ideologies;
- lobby groups by issue domain with issue preference maps and capture strategies;
- a status quo in the one-dimensional policy space;
- bills around proposer ideal points with public-support, public-benefit, salience, lobbying, affected-group, harm, uncertainty, and private-gain signals.

Party-system profiles include ideological bins, two major parties with minor parties, fragmented multiparty systems, dominant-party systems, and weighted campaign profiles. The party-system sensitivity campaign assigns likelihood weights to party-system profiles.

The main comparison campaign also supports adversarial proposal-generator profiles: high-benefit extreme reform, popular harmful bills, low-benefit moderate capture, delayed-benefit reform, concentrated rights-like harm, and anti-lobbying backlash. These cases are stress tests for the generator's own normative assumptions, not empirical claims about real proposal distributions.

## 6. Input Data

Scenario runs use synthetic generated worlds. Calibration screening reads `data/calibration/empirical-benchmarks.csv`, a tracked extract that maps empirical sources to simulator metrics and benchmark ranges.

Current empirical sources named by the benchmark layer include Voteview roll-call data, Congress.gov and govinfo bill histories, Comparative Agendas Project topic data, ParlGov party-system data, U.S. Lobbying Disclosure Act filings, Center for Effective Lawmaking scores, and V-Dem institutional indicators.

The calibration runner executes conventional scenarios and writes pass/fail reports to `reports/calibration-baseline.csv` and `reports/calibration-baseline.md`. It is an empirical screen, not an automatic parameter fitter.

## 7. Submodels

**Voting**

Legislators cast `YAY` or `NAY` through weighted influences: ideology, party, constituency/public support, lobbying, compromise preference, reputation, and affected-group sensitivity.

**Proposal Access**

Access rules include open access, viability screens, scalar proposal costs, public-value waivers, lobby surcharges, member quotas, public-interest screens, cross-bloc cosponsorship gates, affected-group sponsor gates, proposal bonds, and earned proposal credits.

**Committees And Information**

Committee gatekeeping can reject proposals before the floor. Committee information processes move public-signal estimates toward generated public benefit with composition-dependent accuracy.

**Challenge And Objection**

Challenge vouchers allocate scarce blocking rights to parties or members. Q-member escalation lets a sufficient number of legislators trigger active review. Public objection windows route contested default-pass bills to active voting or repeal review.

**Lobbying**

Budgeted lobbying modifies bill pressure and public signals through channel-specific spending. Anti-capture variants include transparency, public financing, public advocates, blind review, audits, sanctions, and defensive-spend caps. Adaptive lobbying learns from channel returns and reform threats.

**Amendment And Mediation**

Structured mediation moves risky proposals toward weighted institutional targets. Multi-round mediation models repeated amendments, costs, concession limits, poison-pill risk, and compensation for concentrated harm.

**Distributional Harm**

Harm-weighted thresholds, compensation amendments, and affected-group consent mechanisms distinguish broad aggregate benefit from concentrated minority loss.

**Citizen Mini-Publics**

Citizen panels simulate sampling noise, information quality, manipulation risk, informed support, benefit estimates, and legitimacy. Panel output can affect default-pass eligibility, active-vote routing, final threshold, or agenda priority.

**Alternatives And Tournaments**

Competing-alternative processes generate same-domain alternatives and select by public benefit, public support, chamber median proximity, or pairwise majority before a final yes-or-no ratification.

**Package Bargaining**

Package bargaining approximates side payments, implementation delays, policy concessions, and harm-reducing trades. It is intentionally a proxy: it can test whether compromise-by-packaging changes the productivity/legitimacy tradeoff, but it does not yet model true multidimensional omnibus bargaining or jurisdictional trades.

**Law Registry**

Enacted laws can persist across later bills, receive review dates, produce realized welfare/support estimates, and be renewed, repealed, or partially rolled back.

**Agenda Scarcity**

Agenda lotteries, quadratic attention budgets, proposal credits, and challenge tokens represent scarcity in formal legislative attention.

## 8. Experimental Design

The main campaigns are:

- roadmap-completion campaign across broad assumption cases.
- weighted party-system sensitivity campaign.
- stylized rising-contention timeline.
- focused strategy and calibration campaign comparing the stylized U.S.-like benchmark, adaptive proposers, strategic lobbying, combined deep strategy, mediation, citizen panels, alternatives, objection windows, and law registry.
- main paper campaign joining broad assumption cases, adversarial generator cases, party-system sensitivity cases, and rising-contention timeline cases in one CSV artifact for all submitted tables and figures; the campaign includes the portfolio hybrid as a synthesized candidate alongside family representatives.
- family screen: supplemental all-catalog screen that runs every explicit scenario key and reports the highest-scoring scenario within each family under a fixed rule.
- mechanism diagnostics: ablation comparisons for nearby mechanism removals plus manipulation-stress comparisons for clone proposals, panel manipulation, astroturf objection, bad-faith harm claims, agenda flooding, and capture pressure.
- empirical bridge: optional raw empirical summaries mapped to the simulator proxy metrics currently used for calibration screening.

All campaign rows include scenario labels, case weights, and a stable metric schema.

## 9. Assumptions And Limitations

The policy space is one-dimensional. Public benefit is generated rather than empirically estimated. Legislators are synthetic and do not represent named real officials. Lobby groups are abstract collective actors. The calibration layer screens plausible ranges but does not yet fit raw datasets directly. Institutional mechanisms are simplified so they can be compared in bundles without modeling the full legal, administrative, judicial, media, and electoral environment. Several mechanisms are optimistic prototypes: citizen panels, objection windows, tournaments, audits, challenge tokens, package bargaining, and law review include diagnostics for procedural cost and strain, but not full real-world implementation cost or strategic manipulation cost.

These limitations are intentional at this stage. The model is meant to identify which institutional mechanisms deserve deeper modeling, not to prove that one constitutional design would work in the real world.

## 10. Reproducibility

Run tests:

```sh
make test
```

Run current campaign:

```sh
make campaign
```

Run calibration:

```sh
make calibrate
```

Build paper and appendix PDFs:

```sh
make paper
```

Run multi-seed robustness checks for the paper scenarios:

```sh
make seed-robustness
```

Run the all-catalog family screen:

```sh
make family-screen
```

Run the empirical bridge and mechanism diagnostics:

```sh
make empirical-bridge
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
```

Build the anonymous supplement package:

```sh
make supplement-anonymous
```
