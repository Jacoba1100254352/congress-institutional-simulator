# Model Documentation Summary

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

This summary condenses the existing ODD/ODD+D documentation for a future software or model-description paper. It draws on `docs/odd-model.md`, `docs/odd-d-appendix.md`, and `paper/technical-appendix/odd-d-appendix.pdf`.

## Purpose

The simulator compares legislative institutional designs by running shared generated worlds through different procedural mechanisms. Its scientific purpose is to stress-test how rules alter productivity, revision/moderation, representative responsiveness, generated public-benefit alignment, minority protection, capture resistance, and administrative burden.

It is a mechanism-comparison simulator, not a forecast of a specific Congress.

## Entities

- Legislators: synthetic actors with party, ideology, compromise preference, party loyalty, constituency sensitivity, lobbying susceptibility, reputation sensitivity, district preference, district intensity, and affected-group sensitivity.
- Bills: proposals with proposer, policy position, public support, public benefit, uncertainty, lobby pressure, private gain, salience, issue domain, affected group, concentrated harm, compensation cost, amendment movement, lobbying signals, challenges, citizen review, and law review status.
- Lobby groups: collective actors with issue preferences, budget, influence intensity, defensive multiplier, information bias, public-campaign skill, capture strategy, and public-support mismatch tolerance.
- Institutions: composable process modules that screen, route, amend, review, vote on, register, or reverse bills.
- Environment: generated legislature, lobby groups, bill stream, party-system profile, and status quo.

## State Variables

Core state includes:

- legislator ideal points and sensitivities;
- party positions and party-system profile;
- bill policy position and original position;
- public support and generated public benefit;
- lobbying pressure, private gain, salience, and uncertainty;
- issue domain and affected group;
- concentrated harm and compensation cost;
- agenda access state;
- committee composition and reporting state;
- challenge-token and attention-budget state;
- law registry and active-law review state;
- proposal credits, bonds, and eligibility filters;
- status quo updated through enacted outcomes.

## Scheduling

Each run:

1. Generates a world with legislators, parties, lobby groups, status quo, and bill stream.
2. Builds each scenario's legislative process from the same generated world.
3. Processes each bill in sequence through the scenario's process chain.
4. Records agenda, vote, amendment, lobbying, review, and enactment outcomes.
5. Updates scenario status quo after enacted or reviewed policy changes.
6. Aggregates run metrics into campaign reports.

Scenarios share generated worlds but receive deterministic random streams, supporting paired comparison.

## Adaptation

Adaptation is bounded and deterministic rather than full reinforcement learning.

Examples:

- proposal credits and proposal bonds carry proposer state;
- law registries and sunset review carry active-law state;
- challenge-token exhaustion affects later capacity;
- proposer strategies can moderate, delay, seek cosponsors, reduce lobby exposure, or withdraw weak proposals;
- lobbying strategies can reallocate channel effort, escalate defensive spending, or change issue multipliers.

## Submodels

Major submodels include:

- weighted voting;
- proposal access and agenda gates;
- committee gatekeeping and information;
- challenge vouchers and public objection;
- lobbying and anti-capture;
- amendment mediation and package bargaining;
- competing alternatives and policy tournaments;
- chamber/bicameral/veto structures;
- distributional harm and compensation;
- citizen panels and public-input systems;
- law registry, sunset, eligibility, proposal bonds, and credits;
- review and independent institution bundles;
- empirical flow screening and campaign reporting.

## Empirical Inputs

Normal scenario runs are synthetic. Empirical inputs currently support benchmark readiness and flow sanity checks:

- Voteview roll calls;
- Congress.gov/govinfo bill progression;
- Senate LDA lobbying disclosures;
- OpenFEC campaign-finance receipts and independent-expenditure summaries;
- Cumulative CES district public-opinion aggregates;
- Supreme Court Database merits-case court-review summaries and bounded court-law U.S.C.-section authority-overlap metadata;
- Federal Register final-rule effective-date, authority-search, proposed-history, proposed-rule comment-portal, bounded small/zero-comment comment-record, and timing metadata;
- Congress.gov law-revision text flags and bounded bill/action linkage;
- topic throughput;
- sponsor success and bounded sponsor-bill metadata by Bioguide ID;
- committee activity;
- tracked calibration benchmarks.

Missing or incomplete empirical areas include bill-topic district public opinion and affected-group mapping beyond the bounded CES proxy and sponsor-district bill policy-area context, campaign-finance linkage beyond FEC recipient metadata, bounded issue-sector context, matched member context, bounded House-candidate district context, and bounded candidate-to-sponsored-bill context to reviewed targets, committee-action influence, and outcomes, complete sponsor histories or CEL-style effectiveness data beyond bounded sponsor-bill metadata, direct case-to-statute/public-law and emergency-order court review beyond U.S.C.-section overlaps, implementation feedback beyond final-rule effective dates, authority-search matches, proposed-history/comment-portal metadata, bounded small/zero-comment comment-record metadata, and timing metadata, full statutory lineage beyond the bounded Congress.gov revision-text proxy, bill/action metadata, authority-search matches, proposed-history/comment-portal/comment-record metadata, timing metadata, and court-overlap metadata, and comparative chamber/productivity evidence beyond the bounded QoG/OWID/V-Dem profile proxy.

## Outputs

Outputs include:

- campaign CSVs;
- Markdown reports;
- calibration and empirical-boundary reports;
- seed robustness reports;
- ablation and manipulation stress reports;
- chamber-structure reports;
- generated LaTeX figures/tables;
- main ACM manuscript PDF;
- ODD+D appendix PDF;
- anonymous supplement archive.

## Limitations

- Synthetic public benefit and public support.
- One-dimensional baseline policy space in current framework.
- Simplified strategic behavior.
- Empirical inputs are sanity checks, not validation of central model outputs.
- Administrative cost is a procedural proxy.
- No claim of real-world institutional ranking.
- Not yet packaged as public reusable software with a chosen license, clean-clone evidence, final citation/CodeMeta release fields, and archive/DOI metadata.
