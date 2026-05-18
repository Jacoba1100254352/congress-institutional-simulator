# Adversary Model

Final decision: NEEDS ADVERSARY EXPERIMENTS FIRST.

The current simulator has stress scenarios, but this paper requires explicit adversary models. Each adversary must specify actor type, objective, information level, budget, strategy set, success metric, and worst-case degradation metric.

## Common Adversary Fields

| Field | Definition |
|---|---|
| Actor type | Proposer, lobby group, party, committee gatekeeper, outside campaign, citizen-panel manipulator, objector network, or mixed coalition. |
| Objective | Enact a low-support bill, block a high-benefit bill, increase administrative burden, preserve private gain, create false consensus, exhaust challenge tokens, or distort public-support signals. |
| Information level | Low: only public mechanism rules; medium: observable bill features and rough support/capture proxies; high: mechanism-specific signals and near-generator-level feature knowledge. |
| Budget | Attention, money, proposal slots, amendment slots, objection capacity, challenge tokens, panel-manipulation capacity, lobbying camouflage, or committee agenda capacity. |
| Strategy set | Discrete actions available to the adversary. |
| Success metric | Binary or continuous attack success measure. |
| Worst-case degradation metric | Largest observed loss or burden increase across budget/information/scenario cells. |

## Proposed Adversary Taxonomy

| ID | Actor type | Objective | Information | Budget | Strategy set | Success metric | Worst-case degradation metric |
|---|---|---|---|---|---|---|---|
| A1 Clone/decoy proposer | Proposer or party | Make content-selection pick a worse alternative or dilute a good one | Medium/high | Proposal slots, amendment slots | Add near-duplicate clones, decoy alternatives, dominated variants, split-support alternatives | Selected bill has lower generated public benefit or lower support than best available alternative | Max decline in selected-bill benefit/support; max increase in low-support enactment |
| A2 Agenda sequencer | Party or committee gatekeeper | Change outcome by controlling order of alternatives/amendments | High | Agenda order slots, floor time | Reorder alternatives, delay strong substitute, sequence polarizing amendment first | Final selected proposal differs from Condorcet-like or best-benefit alternative | Max benefit/support loss from ordering |
| A3 Poison-pill amender | Party, proposer, or lobby group | Block or taint high-benefit bill | Medium/high | Amendment slots | Attach harmful rider, private-gain rider, concentrated-harm provision, salience-raising poison pill | High-benefit proposal fails or passes with material harm/capture increase | Max high-benefit blockage; max harm/capture increase |
| A4 Astroturf objector | Outside campaign or lobby group | Overload objection window or falsely signal public opposition | Low/medium | Objection capacity, money, public attention | File noisy objections, coordinate repetitive claims, target challenge threshold | Admin cost rises or high-benefit bills are delayed/blocked | Max admin-cost increase; max false-negative blockage |
| A5 Panel manipulator | Citizen-panel manipulator or outside campaign | Bias citizen review toward false consensus or false rejection | Medium | Framing budget, panel-noise capacity | Bias information packet, target panel composition, increase noise | Panel certification diverges from generated benefit/support | Max certification error; max low-support enactment or high-benefit blockage |
| A6 Bad-faith harm claimant | Outside campaign, party, or affected-group proxy | Trigger harm review to delay/block rivals or exempt allies | Medium | Harm-claim filings, legal attention | Exaggerate harm, duplicate claims, strategically target high-benefit bills | False-positive review or false-negative harm clearance | Max false-positive admin burden; max harm-screen error |
| A7 Proposal flooder | Proposer, party, or lobby group | Exhaust agenda capacity and review capacity | Low/medium | Proposal slots, lobbying money | Submit many low-value bills, clone bills, high-salience noise | Floor/review load rises or high-benefit bills are crowded out | Max admin burden; max decline in high-benefit consideration |
| A8 Lobby camouflage actor | Lobby group | Preserve private gain while evading anti-capture screens | High | Money, proxy sponsors, issue framing | Split spend, use proxy sponsors, mask private gain as technical information | Captured bill passes anti-capture gate | Max capture increase among enacted bills |
| A9 Defensive anti-reform lobby | Lobby group or outside campaign | Block anti-capture reform or weaken safeguards | Medium/high | Lobbying money, public persuasion | Attack reform legitimacy, raise uncertainty, sponsor decoys | Anti-capture reforms fail or pass weakened | Max reduction in anti-lobby pass rate; max capture persistence |
| A10 Burden-shift silence actor | Party, lobby group, or committee gatekeeper | Let default enactment happen by suppressing objections | Medium/high | Coordination capacity, challenge tokens withheld | Strategic silence, challenge-token hoarding, obstruction of objection coordination | Low-support or captured bill enacts by default | Max low-support enactment increase; max unused challenge-token rate |
| A11 Portfolio overload actor | Mixed adversary | Exhaust layered safeguards | Medium/high | Proposal slots, objections, harm claims, lobbying camouflage | Combine flooding, claims, panel noise, and camouflage | Routing/review capacity saturates | Max admin cost; max review queue overflow; max risk-control degradation |

## Budget Levels

Use at least three levels for each attack:

- Low: mild perturbation comparable to current manipulation-stress probes.
- Medium: organized actor with targeted budget.
- High: concentrated adversary with mechanism knowledge and repeated attempts.

Budgets should be stated in units the simulator can count:

- proposal slots;
- amendment slots;
- objections filed;
- harm claims filed;
- challenge tokens spent or withheld;
- lobbying budget;
- panel-bias/noise amount;
- review/attention capacity consumed.

## Information Levels

- Low: mechanism rules and public bill labels only.
- Medium: observed support, salience, sponsor party, issue domain, and approximate lobbying pressure.
- High: generated support/benefit/harm proxies, gate thresholds, and mechanism-specific scoring information.

## Required Attack Outputs

For every adversary x mechanism family x budget x information cell, report:

- worst-case degradation;
- median degradation;
- attack success rate;
- administrative burden under attack;
- recovery/correction rate;
- low-support enactment change;
- high-benefit blockage change;
- capture/harm change where relevant.

## Failure Trace Schema

Each trace should record:

- seed;
- scenario/case;
- mechanism;
- adversary ID;
- budget;
- information level;
- bill ID or proposal family;
- attack actions;
- pre-attack bill features;
- post-attack bill features;
- gate/review/vote path;
- outcome;
- metric deltas.
