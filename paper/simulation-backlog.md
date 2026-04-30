# Simulation Roadmap

This file tracks simulator increments that were planned for the paper and the current status after the main comparison campaign and the subsequent breadth/process cleanup.

## Implemented Through Main Comparison Campaign

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
- structured amendment mediation and package bargaining, including bounded mediation, multi-round mediation with round costs, concession limits, poison-pill risk, concentrated-harm reduction, compensation, and a multidimensional package-bargaining prototype with cross-issue trade count, implementation complexity, and affected-group mitigation
- constituent/public-will modeling, including generated district preference, district intensity, affected-group sensitivity, public-will signal revision, public signal movement, and district-alignment diagnostics
- weighted party-system sensitivity, including two-party, two-major-plus-minors, fragmented multiparty, and dominant-party legislature profiles with case likelihood weights
- initial endogenous strategy, including proposer moderation/cosponsorship/withdrawal behavior and lobby-group influence-channel learning after outcomes
- stylized timeline stress comparisons and endogenous norm-erosion stress, including rising polarization, party loyalty, lobbying pressure, proposal pressure, lower compromise culture, lower constituency responsiveness, electoral pressure, media amplification, court/delay shocks, lobbying escalation, norm recovery, and a derived contention index
- non-default institutional families added after the breadth audit: leadership agenda control, richer stylized current-Congress workflow, conference-committee revision, stylized judicial review, direct citizen initiative/referendum, and endogenous norm-erosion delay
- process hardening, including multi-seed robustness regression checks, figure-label checks, table/figure consistency checks, rendered-PDF checks, PDF text/raw-byte/metadata anonymity checks, anonymous supplement packaging, validation-readiness and empirical-validation reporting, breadth-catalog reporting, and a non-anonymous public provenance target
- diagnostic follow-ups, including an empirical validation bridge, mechanism ablation report, manipulation-stress report, and generated LaTeX diagnostics table for the paper

## Current Campaign

The main comparison campaign is the current default campaign. It runs 120 simulations per case, combines broad assumption cases, adversarial proposal-generator cases, weighted party-system cases, and six stylized timeline eras, and uses 101 legislators with 60 base bills per run. The scenario set is breadth-first: conventional affirmative systems, committee-first regular order, coalition confidence, policy tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation/package-bargaining rules, anti-capture safeguards, risk routing, reversibility, and a small default-enactment stress-test family.

Generated artifacts:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/empirical-bridge.md`
- `reports/ablation-analysis-summary.md`
- `reports/manipulation-stress-summary.md`
- `paper/main.pdf`

## Remaining Research Work

The planned roadmap layer is implemented at prototype depth. The next additions would be research-expansion work rather than cleanup of previously promised features:

- deeper endogenous strategy: proposers now adapt moderation, cosponsorship, withdrawal, proposal volume, timing, harm posture, and lobbying exposure, but they still do not learn full rule-specific strategies over many sessions
- deeper strategic lobbying response: lobby groups now reallocate capture strategy, defensive threat, and budget intensity, but they still do not run long-horizon adversarial learning against organized public-interest opponents
- richer public model: constituents should be generated as district populations with preference distributions, issue intensity, group membership, and turnout/attention differences rather than only legislator-level district signals
- richer bargaining: amendments now include several coalition, side-payment, compensation, multidimensional trade, poison-pill, and proposer-withdrawal proxies, but they still do not represent full textual omnibus bargaining, jurisdictional bargains, or explicit distributive appropriations
- empirical validation: `make validation-readiness` checks whether optional raw input files are present and schema-compatible, and `make empirical-validation` computes first-pass raw-data summaries when local Voteview-like roll-call data, Congress.gov/govinfo bill progression, LDA-style lobbying disclosures, topic throughput, or sponsor-success files are present. The project still needs curated datasets, tighter tolerances, and source-specific adapters for V-Dem, ParlGov, Comparative Agendas, and Center for Effective Lawmaking before making empirical validation claims
- agenda-control validation: add diagnostics for referral authority, jurisdictional monopoly, discharge thresholds, amendment openness, floor scheduling, and status-quo fallback so committee-power and closed-rule agenda models can be matched more directly
- social-choice stress tests: make policy tournaments vulnerable to clone alternatives, strategic sequencing, and multidimensional cycling before treating pairwise winners as robust reform candidates
- institutional realism: the newly added leadership, current-Congress workflow, conference, judicial, initiative, and norm-erosion modules are stylized family representatives, not detailed models of Congress, courts, elections, federalism, agencies, or media ecosystems

## Submission Note

The paper should continue to frame the simulator as an exploratory mechanism-search framework. The current results are useful for comparing rule bundles under shared assumptions, but they should not be presented as a validated model of the United States Congress.
