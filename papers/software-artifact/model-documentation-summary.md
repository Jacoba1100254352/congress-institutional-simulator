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
- topic throughput;
- sponsor success;
- committee activity;
- tracked calibration benchmarks.

Missing or incomplete empirical areas include district public opinion, campaign finance, court review, implementation feedback, law revision, and comparative institutions.

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
- Not yet packaged as public reusable software with license/citation/release metadata.
