# Adversary Model

## Status

Readiness level: planning complete enough to guide implementation; evidence not yet sufficient for manuscript claims.

This file defines bounded adversaries for the robustness paper. Each adversary must be implemented as an explicit actor model or campaign configuration before it can support a claim.

## Required Fields

| Field | Definition |
|---|---|
| Actor type | Institutional or outside actor represented by the attack. |
| Objective | What the actor is trying to cause. |
| Information level | What the actor can observe before choosing actions. |
| Budget | Scarce resource the actor can spend. |
| Strategy set | Discrete or parameterized actions available to the actor. |
| Success metric | Direct measure of whether the attack worked. |
| Degradation metric | Mechanism-level harm relative to a paired non-attack baseline. |
| Trace fields | Minimum data needed to audit the path from attack action to outcome. |

## Information Levels

| Level | Actor knowledge |
|---|---|
| Low | Public mechanism rules, public labels, and coarse issue/sponsor features. |
| Medium | Observable support, salience, sponsor party, issue domain, and approximate lobbying pressure. |
| High | Generated support/benefit/harm proxies, gate thresholds, and mechanism-specific scoring information. |

High information is a stress-test assumption, not a real-world knowledge claim.

## Budget Units

Budgets must use countable simulator units:

- proposal slots;
- amendment slots;
- agenda-order slots;
- objections filed;
- harm claims filed;
- challenge tokens spent or withheld;
- lobbying budget;
- proxy-sponsor count;
- panel-bias or noise intensity;
- review/attention capacity consumed.

Use at least low, medium, and high budget levels for every implemented attack. If the unit is continuous, record the exact numeric value in the output.

## First-Wave Adversaries

| ID | Actor type | Objective | Information | Budget | Strategy set | Success metric | Degradation metric |
|---|---|---|---|---|---|---|---|
| A1 Clone/decoy proposer | Proposer, party, or lobby-aligned proposer | Make content selection choose a worse alternative or dilute support for a good one. | Medium/high | Proposal or amendment slots. | Add near-duplicates, dominated variants, or support-splitting decoys. | Selected bill has lower generated support or public benefit than the best available alternative. | Max and median loss in selected-bill support/benefit; low-support enactment change. |
| A2 Poison-pill or sequencing actor | Party, proposer, committee gatekeeper, or lobby group | Block a high-benefit bill or pass it with a harmful rider. | Medium/high | Amendment slots and agenda-order slots. | Attach harmful rider, add private-gain rider, reorder substitutes, sequence polarizing amendment first. | High-benefit bill fails or passes with increased harm/capture. | High-benefit blockage rate; harm/capture increase among enacted bills. |
| A3 Public-input manipulator | Outside campaign, lobby group, or panel manipulator | Distort objection, petition, or panel signals. | Low/medium | Objections, public-attention units, panel-noise intensity. | File noisy objections, coordinate repetitive claims, bias panel inputs, increase panel noise. | Review path diverges from generated support/benefit or high-benefit bills are delayed/blocked. | Admin-cost increase; false-positive and false-negative public-input errors. |
| A4 Bad-faith harm claimant | Outside campaign, party, affected-group proxy, or lobby group | Trigger false-positive harm review or evade true harm review. | Medium | Harm-claim filings and legal attention. | Exaggerate harm, duplicate claims, target rivals, understate ally harm. | Harm review blocks a non-harmful bill or clears a harmful bill. | False-positive burden; false-negative concentrated-harm passage. |
| A5 Proposal flooder | Proposer, party, or lobby group | Exhaust agenda, floor, or review capacity. | Low/medium | Proposal slots and lobbying support. | Submit many low-value bills, clone bills, high-salience noise, or lobby-supported low-support bills. | High-benefit bills are crowded out or low-support bills enact. | Floor/review load increase; high-benefit consideration decline; low-support enactment change. |
| A6 Lobbying camouflage actor | Lobby group or proxy sponsor network | Preserve private gain while evading anti-capture screens. | Medium/high | Lobbying money, proxy sponsors, issue framing. | Split spend, route through proxies, mask private gain as technical information. | Captured bill passes an anti-capture or access screen. | Capture increase among enacted bills; visible-spend decline paired with capture persistence. |
| A7 Administrative overload coalition | Mixed coalition | Saturate layered safeguards. | Medium/high | Proposals, objections, harm claims, lobbying camouflage, review demand. | Combine flooding, claims, panel noise, and camouflage. | Routing or review capacity becomes saturated. | Admin-cost increase; queue overflow; risk-control degradation after overload. |
| A8 Public-support distortion actor | Outside campaign, lobby group, party, or proxy civic campaign | Create false consensus, suppress support for a high-benefit bill, or inflate support for a private-gain bill. | Low/medium/high | Public-campaign spend, attention capacity, salience manipulation, proxy endorsements. | Shift cheap public signals, amplify distorted salience, target generated district or affected-group support proxies when available. | Public-support signal moves away from generated benefit or affected-group burden. | Public-preference distortion, low-support enactment change, popular-fail change, admin burden if review is triggered. |
| A9 Mixed adversary portfolio | Coordinated outside and inside actors | Combine attacks so defenses that handle one stressor fail under interaction. | Medium/high | Joint budget across proposal slots, amendments, objections, claims, lobbying, public-signal distortion, and review demand. | Select 2-4 attack actions from A1-A8 under a fixed total budget. | Joint attack succeeds where the strongest single attack does not. | Interaction degradation, superadditive loss, overload, recovery failure, and residual risk after correction. |

## Deferred or Appendix Adversaries

| ID | Reason to defer | Boundary |
|---|---|---|
| D1 Strategic silence under burden-shifting rules | Useful but risks making the paper default-enactment-centered. | Include only after first-wave attacks are complete, and only as one bounded case with unused-token and objection-suppression metrics. |
| D2 Defensive anti-reform lobbying | Current pilot result improves the score profile, so the setup is not yet interpretable as an adversary result. | Treat as part of A6 only after lobbying camouflage has a clearer success metric and paired baseline. |
| D3 Fully adaptive party or media ecosystem | Too large for this breakout. | Keep parties and outside actors bounded; do not model elections, media, courts, and agencies as co-evolving adversaries in this paper. |

## Required Output Schema

Every attack output should include:

- seed;
- case key;
- scenario key;
- mechanism family;
- adversary ID;
- actor type;
- objective;
- budget unit and value;
- information level;
- attack action list;
- pre-attack bill or proposal features;
- post-attack bill or proposal features;
- gate, review, amendment, vote, and correction path;
- baseline outcome;
- attacked outcome;
- success flag;
- metric deltas;
- administrative burden under attack.

## Reporting Rules

- Pair every attack cell with a same-seed baseline.
- Report attack success rates, not just mean score deltas.
- Report worst-case and median degradation separately.
- Keep untested cells explicit.
- Treat adversary budgets as modeling assumptions, not observed real-world rates.
