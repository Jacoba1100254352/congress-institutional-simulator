# Simulation Roadmap

This file tracks simulator increments that were planned for the paper and the current status after `simulation-campaign-v19`.

## Implemented Through v19

The following planned increments are now represented in code, tests, campaign reports, and the LaTeX paper workflow:

- challenge-voucher sweeps, including party-held tokens, member-held tokens, q-member escalation, proportional party allocation, minority-bonus allocation, token exhaustion, false-negative pass diagnostics, and challenged paths through active vote, 60 percent vote, committee review, or committee information plus active vote
- cross-bloc and richer coalition cosponsorship, including outside-bloc admission metrics, affected-group sponsor gates, cosponsor counts, and coalition support discounts
- adaptive procedural tracks, including explicit fast/middle/high route metrics, lenient and strict thresholds, citizen-panel high-risk lanes, and supermajority high-risk lanes
- sunset and active-law review, including a real active-law registry, delayed review, reversal, partial rollback, correction delay, active-law welfare, low-support active-law share, and review-period sensitivity variants
- proposal-cost and proposal-accountability variants, including scalar costs, public-value waivers, lobby-pressure surcharges, stateful member quotas, earned proposal credits, proposer-access concentration, welfare per submitted bill, and refundable proposal bonds
- distributional harm and affected groups, including concentrated harm, affected-group support, compensation amendments, affected consent, minority-harm metrics, compensation rate, and legitimacy score
- explicit budgeted lobbying actors, including issue-preference maps, capture strategies, public-support mismatch tolerance, direct pressure, agenda access, information distortion, public campaigns, litigation/delay threats, defensive spending, public financing/democracy vouchers, equal-access public advocate, blind lobby-origin review, defensive-spend caps, public benefit per lobby dollar, and channel-share metrics
- citizen mini-public review, including sampling noise, information quality, manipulation risk, panel legitimacy, certification, active routing, threshold adjustment, and agenda-priority variants
- agenda scarcity, including weighted/random agenda lotteries, quadratic attention budgets, public objection windows, repeal windows, attention spend, objection rate, and repeal reversal metrics
- competing alternatives and policy tournaments, including benefit, support, median, pairwise, obstruction-with-substitute, and strategic clone/decoy variants
- structured amendment mediation, including bounded mediation and multi-round mediation with round costs, concession limits, poison-pill risk, concentrated-harm reduction, and compensation
- constituent/public-will modeling, including generated district preference, district intensity, affected-group sensitivity, public-will signal revision, public signal movement, and district-alignment diagnostics
- weighted party-system sensitivity, including two-party, two-major-plus-minors, fragmented multiparty, and dominant-party legislature profiles with case likelihood weights
- initial endogenous strategy, including proposer moderation/cosponsorship/withdrawal behavior and lobby-group influence-channel learning after outcomes
- stylized timeline stress comparisons, including rising polarization, party loyalty, lobbying pressure, proposal pressure, lower compromise culture, lower constituency responsiveness, and a derived contention index

## Current Campaign

`simulation-campaign-v19` is the current default campaign. It runs 120 simulations per case, six stylized timeline eras, 101 legislators, 60 base bills per run, and a selected broad scenario set. It uses rising-contention assumptions to compare how conventional affirmative systems, default-pass variants, guardrails, public-review systems, policy tournaments, and the current U.S.-style benchmark degrade over time.

Generated artifacts:

- `reports/simulation-campaign-v19.csv`
- `reports/simulation-campaign-v19.md`
- `paper/main.pdf`

## Remaining Research Work

The planned roadmap layer is now implemented. The next additions would be research-expansion work rather than cleanup of previously promised features:

- deeper endogenous strategy: proposers currently adapt moderation, cosponsorship, and withdrawal; next they should adapt proposal volume, timing, lobbying exposure, and amendment demands to each institutional rule set
- deeper strategic lobbying response: lobby groups currently reallocate capture strategy after outcomes; next they should learn channel returns over longer sessions and adapt budgets by issue, reform threat, and opponent behavior
- richer public model: constituents should be generated as district populations with preference distributions, issue intensity, group membership, and turnout/attention differences rather than only legislator-level district signals
- richer bargaining: amendments should support coalitions, side payments or compensation packages, poison-pill amendments from opponents, and proposer withdrawal
- calibration: compare rough simulator outputs to Voteview roll-call ideology and party-unity patterns, Congress.gov/govinfo bill progression, lobbying disclosure spending and client patterns, Comparative Agendas topic throughput, V-Dem institutional measures, ParlGov party-system structure, and Center for Effective Lawmaking sponsor-success benchmarks before making empirical claims
- agenda-control validation: add diagnostics for referral authority, jurisdictional monopoly, discharge thresholds, amendment openness, floor scheduling, and status-quo fallback so committee-power and closed-rule agenda models can be matched more directly
- social-choice stress tests: make policy tournaments vulnerable to clone alternatives, strategic sequencing, and multidimensional cycling before treating pairwise winners as robust reform candidates
- documentation: expand the ODD/ODD+D description into a submission appendix if the project moves toward submission

## Submission Note

The paper should continue to frame the simulator as an exploratory mechanism-search framework. The current results are useful for comparing rule bundles under shared assumptions, but they should not be presented as a validated model of the United States Congress.
