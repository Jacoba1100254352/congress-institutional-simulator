# ODD Model Description

This is an ODD-style model description for the congressional institutional simulator. It is intentionally concise so it can become an appendix for the paper.

## Purpose

The model compares legislative institutional designs by running shared generated worlds through different procedural mechanisms. The goal is to study tradeoffs among compromise, productivity, representative responsiveness, minority protection, and resistance to agenda capture.

## Entities, State Variables, And Scales

**Legislators** have an ID, party label, ideology, compromise preference, party loyalty, constituency sensitivity, lobby sensitivity, reputation sensitivity, district preference, district intensity, and affected-group sensitivity.

**Bills** have a proposer, proposer ideology, policy position, public support, public benefit, public-benefit uncertainty, lobby pressure, private gain, salience, issue domain, affected group, affected-group support, concentrated harm, and compensation cost. Later institutional processes may add lobbying spend, cosponsors, amendments, citizen-panel certification, attention spend, or compensation.

**Lobby groups** have an ID, issue preferences, preferred policy position, budget, capture strategy, defensive multiplier, information bias, public-campaign skill, and public-support mismatch tolerance.

**Institutional processes** are composable rule modules. A process can screen proposals, alter bill signals, mediate content, route bills to review lanes, spend lobbying or attention resources, conduct votes, record active laws, or produce final outcomes.

The policy scale is one-dimensional from `-1.0` to `1.0`. Support, benefit, harm, legitimacy, and most sensitivities are ratios from `0.0` to `1.0`.

## Process Overview And Scheduling

Each simulation run generates a world, then evaluates every bill in sequence under each scenario. For a scenario:

1. Build the scenario's legislative process from the generated world.
2. Start from the generated status quo.
3. For each bill, create a vote context with party positions, the current status quo, and a deterministic random stream.
4. Let the process consider the bill through its configured stages.
5. Record metrics from the outcome.
6. Update the status quo to the outcome's post-bill policy position.

Scenarios share generated worlds but receive independent deterministic random streams. This supports paired comparison across institutional rules.

## Design Concepts

**Basic principles:** Legislative outcomes are shaped by agenda access, voting thresholds, information, lobbying, amendment, public review, reversibility, and strategic proposal selection.

**Emergence:** Aggregate productivity, compromise, capture, and volatility emerge from bill-by-bill interactions with institutional rules.

**Adaptation:** The current baseline has limited adaptation. Proposal credits, proposal bonds, and law review carry state across bills. The next layer adds explicit proposer adaptation and lobby channel learning across sessions.

**Objectives:** Legislators vote according to weighted ideological, party, constituency, lobbying, reputational, and compromise influences. Institutions do not optimize one global objective; they produce measurable tradeoffs.

**Stochasticity:** Worlds, bills, panels, committees, and some routing decisions use seeded randomness. Identical seeds produce identical results.

**Observation:** Campaign reports aggregate outcomes into productivity, floor load, welfare, compromise, low-support passage, public alignment, minority harm, legitimacy, capture, lobbying spend, amendment, law-review, citizen-review, attention, and agenda-concentration metrics.

## Initialization

`WorldGenerator` creates legislators from a party-system profile, generates lobby groups by issue domain, chooses an initial status quo, and generates bills around proposer ideal points. Generated values are bounded by model-level validation checks.

Party-system profiles currently include ideological bins, two major parties with minor parties, fragmented multiparty, and dominant-party systems.

## Input Data

The exploratory model does not yet consume external datasets. Calibration targets are listed in `docs/calibration.md`; future calibrated runs should use those targets to fit baseline generation parameters.

## Submodels

Major submodels include:

- weighted voting strategy
- proposal access and proposal cost screens
- committee gatekeeping and committee information
- challenge vouchers and q-member escalation
- adaptive procedural tracks
- sunset trial and active-law registry review
- budgeted lobbying and anti-capture processes
- structured and multi-round mediation
- citizen mini-public review
- distributional harm and compensation
- competing alternatives and policy tournaments
- agenda lotteries, quadratic attention budgets, and public objection windows

Each submodel returns a `BillOutcome`, allowing metrics to be accumulated consistently across scenario families.
