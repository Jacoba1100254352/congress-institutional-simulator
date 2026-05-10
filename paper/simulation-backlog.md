# Simulation Roadmap

This file tracks simulator increments that were planned for the paper and the current status after the main comparison campaign and the subsequent breadth/process cleanup.

## Implemented Through Main Comparison Campaign

The following planned increments are now represented in code, tests, campaign reports, and the LaTeX paper workflow:

- challenge-voucher sweeps, including party-held tokens, member-held tokens, q-member escalation, proportional party allocation, minority-bonus allocation, token exhaustion, false-negative pass diagnostics, and challenged paths through active vote, 60 percent vote, committee review, or committee information plus active vote
- cross-bloc and richer coalition cosponsorship, including outside-bloc admission metrics, affected-group sponsor gates, cosponsor counts, and coalition support discounts
- adaptive procedural tracks, including explicit fast/middle/high route metrics, lenient and strict thresholds, citizen-panel high-risk lanes, and supermajority high-risk lanes
- sunset and active-law review, including a real active-law registry, delayed review, reversal, partial rollback, correction delay, active-law welfare, low-support active-law share, review-period sensitivity variants, implementation delay, implementation capacity, nonenforcement risk, underfunding risk, renewal lobbying pressure, and sunset-before-implementation diagnostics
- proposal-cost and proposal-accountability variants, including scalar costs, public-value waivers, lobby-pressure surcharges, stateful member quotas, earned proposal credits, proposer-access concentration, welfare per submitted bill, and refundable proposal bonds
- distributional harm and affected groups, including concentrated harm, affected-group support, compensation amendments, affected consent, minority-harm metrics, compensation rate, and legitimacy score
- explicit budgeted lobbying actors, including issue-preference maps, capture strategies, public-support mismatch tolerance, direct pressure, agenda access, information distortion, public campaigns, litigation/delay threats, defensive spending, public financing/democracy vouchers, equal-access public advocate, blind lobby-origin review, defensive-spend caps, public benefit per lobby dollar, and channel-share metrics
- citizen mini-public review, including sampling noise, information quality, manipulation risk, panel legitimacy, certification, active routing, threshold adjustment, and agenda-priority variants
- agenda scarcity, including weighted/random agenda lotteries, quadratic attention budgets, public objection windows, repeal windows, attention spend, objection rate, and repeal reversal metrics
- competing alternatives and policy tournaments, including benefit, support, median, pairwise, obstruction-with-substitute, and strategic clone/decoy variants
- backward-to-floor agenda access, including citizen agenda petitions, default-open floor calendars, anti-capture proposal-access screens, proportional committee assignment, discharge-petition committee bypass, pairwise amendment tournaments, petition mandate strength, costly public-mandate signal, cheap signal distortion, public-mandate intensity, open-calendar delay cost, amendment openness, policy yield per submitted bill, and pre-floor blockage reliance
- structured amendment mediation and package bargaining, including bounded mediation, multi-round mediation with round costs, concession limits, poison-pill risk, amendment overload, proposer-advantage reduction, public-mandate improvement against a no-amendment counterfactual, concentrated-harm reduction, compensation, and a multidimensional package-bargaining prototype with cross-issue trade count, implementation complexity, and affected-group mitigation
- constituent/public-will modeling, including generated district preference, district intensity, affected-group sensitivity, public-will signal revision, public signal movement, and district-alignment diagnostics
- weighted party-system sensitivity, including two-party, two-major-plus-minors, fragmented multiparty, and dominant-party legislature profiles with case likelihood weights
- initial endogenous strategy, including proposer moderation/cosponsorship/withdrawal behavior and lobby-group influence-channel learning after outcomes
- stylized timeline stress comparisons and endogenous norm-erosion stress, including rising polarization, party loyalty, lobbying pressure, proposal pressure, lower compromise culture, lower constituency responsiveness, electoral pressure, media amplification, court/delay shocks, lobbying escalation, norm recovery, and a derived contention index
- non-default institutional families added after the breadth audit: leadership agenda control, richer stylized current-Congress workflow, conference-committee revision, stylized judicial review, direct citizen initiative/referendum, and endogenous norm-erosion delay
- process hardening, including multi-seed robustness regression checks, figure-label checks, table/figure consistency checks, rendered-PDF checks, PDF text/raw-byte/metadata anonymity checks, anonymous supplement packaging, validation-readiness and empirical-validation reporting, breadth-catalog reporting, and a non-anonymous public provenance target
- diagnostic follow-ups, including an empirical validation bridge, mechanism ablation report, manipulation-stress report, and generated LaTeX diagnostics table for the paper

## Current Campaign

The main comparison campaign is the current default campaign. It runs 120 simulations per case, combines broad assumption cases, adversarial proposal-generator cases, weighted party-system cases, and six stylized timeline eras, and uses 101 legislators with 60 base bills per run. The scenario set is breadth-first: conventional affirmative systems, committee-first regular order, proportional committee assignment, discharge-petition bypass, open floor calendars, citizen agenda petitions, coalition confidence, policy and amendment tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation/package-bargaining rules, anti-capture safeguards, risk routing, reversibility, and a small default-enactment stress-test family.

Generated artifacts:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/empirical-bridge.md`
- `reports/empirical-validation-gap-report.md`
- `reports/ablation-analysis-summary.md`
- `reports/manipulation-stress-summary.md`
- `paper/main.pdf`

## Remaining Research Work

The planned roadmap layer is implemented at prototype depth. The next additions would be research-expansion work rather than cleanup of previously promised features:

- deeper endogenous strategy: proposers now adapt moderation, cosponsorship, withdrawal, proposal volume, timing, harm posture, and lobbying exposure, and `LongHorizonStrategyProcess` adds bounded rule-learning diagnostics. Remaining work is full multi-session reinforcement-style learning against changing opponents.
- deeper strategic lobbying response: lobby groups now reallocate capture strategy, defensive threat, and budget intensity, and `InfluenceSystemProcess` adds shadow-lobbying, campaign-finance, watchdog, enforcement, and public-matching proxies. Remaining work is a separate high-fidelity lobbying/campaign-finance simulator with adversarial public-interest opponents.
- richer public model: `DistrictPopulationProcess` now adds district-level preference variance, turnout skew, affected-group representation gaps, attention, and public-will polarization. Remaining work is calibrated constituent microdata and district election feedback rather than only bill-level signal adjustment.
- richer bargaining: amendment, package, multidimensional, and `OmnibusBargainingProcess` modules now include side-payment, delay, jurisdictional-trade, distributive-load, compensation, poison-pill, and proposer-withdrawal proxies. Remaining work is textual omnibus modeling, appropriations line items, and explicit high-dimensional coalition formation.
- empirical validation: `make validation-readiness` checks whether optional raw input files are present and schema-compatible, and `make empirical-validation` computes first-pass raw-data summaries when local Voteview-like roll-call data, Congress.gov/govinfo bill progression, LDA-style lobbying disclosures, topic throughput, sponsor-success, district-opinion, committee-activity, campaign-finance, court-review, rulemaking/implementation, law-revision, or comparative-institutions files are present. Six of twelve raw validation inputs are now present: Voteview roll calls, Congress.gov bill progression, LDA lobbying disclosures, topic throughput, sponsor success, and committee activity. The project still needs curated district-opinion, campaign-finance, court-review, implementation, law-lineage, comparative-institution, V-Dem, ParlGov, Comparative Agendas, Center for Effective Lawmaking, Federal Register, Unified Agenda, and Regulations.gov extracts before making empirical validation claims
- empirical priority: small adapter samples remain fixtures under `data/validation/fixtures/`; the next serious paper-strengthening step is replacing the remaining missing inputs with curated raw extracts under `data/validation/raw/`, with documented source transformations and tighter target ranges. `make validation-gap-report` now makes this boundary explicit by separating empirical bridge rows from synthetic-only rows. The current sponsor and committee raw summaries are usable bridge signals but remain sampled and action-derived rather than full committee-calendar or member-history datasets
- agenda-control validation: referral authority, discharge-petition bypass, amendment openness, floor scheduling, and pre-floor blockage diagnostics now exist at prototype depth. The 118th Congress bill-progression raw sample and Congress.gov-derived committee activity now give a first empirical bridge for floor load, committee reporting, and enactment. Remaining work is source-specific validation of referral jurisdictions, closed/open rules, calendar control, and status-quo fallback against fuller empirical data.
- post-enactment validation: implementation delay, enforcement capacity, nonenforcement, underfunding, renewal lobbying, and law-revision diagnostics now exist at prototype depth. Remaining work is to replace proxy state transitions with curated rulemaking, oversight, renewal, repeal, and invalidation histories.
- social-choice stress tests: clone and decoy variants exist. Remaining work is strategic sequencing and explicit multidimensional cycling before treating pairwise winners as robust reform candidates.
- institutional realism: the newly added leadership, current-Congress workflow, conference, court-architecture, initiative, district-public, influence-system, and norm-erosion modules are stylized family representatives, not detailed models of Congress, courts, elections, federalism, agencies, or media ecosystems

## Submission Note

The paper should continue to frame the simulator as an exploratory mechanism-search framework. The current results are useful for comparing rule bundles under shared assumptions, but they should not be presented as a validated model of the United States Congress. Feature work should stay frozen for this paper unless it closes a validation or reproducibility gap; new synthetic institutional families are better saved for a follow-up version or separate paper.
