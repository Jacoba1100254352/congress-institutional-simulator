# Representation Model

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

The current chamber campaign can screen structural variants, but a stand-alone representation-architecture paper needs a clearer representation model. This file defines the required model upgrades.

## Current Problem

The simulator reports productivity, revision-moderation, public-support diagnostics, low-public-support enactment, minority harm, malapportionment, committee capture, inter-chamber conflict, and ex ante review. For a chamber-structure paper, these diagnostics need a stronger representation base:

- status quo should be domain-aware, not only a single abstract baseline;
- public support should be distributed across districts, groups, and chambers;
- chamber coalition support should be separated from population support;
- affected-group support should be separated from majority support;
- malapportionment should affect whose support counts in each chamber;
- committee assignment should affect agenda flow and capture risk through explicit member, party, district, expertise, and sponsor channels.

## Required State Variables

| Component | Required variable | Purpose |
|---|---|---|
| Issue domain | `domain` or `issueDomain` | Allows status quo, support, harm, and committee jurisdiction to vary by policy area. |
| Domain status quo | `q_domain,t` | Prevents unrelated issue domains from sharing one abstract status quo. |
| District population | `population_d` | Enables population-weighted representation diagnostics. |
| District support | `support_b,d` | Distinguishes district support from national support. |
| Affected-group support | `support_b,g` | Distinguishes group harm/accommodation from majority support. |
| Chamber coalition support | `support_b,chamber` | Measures support among voting members in each chamber. |
| Seat-population weight | `seatShare_d - populationShare_d` | Measures malapportionment and seat distortion. |
| Committee jurisdiction | `jurisdiction_c,domain` | Links committees to issue domains. |
| Committee capture | `capture_c` | Measures whether committee routing/revision favors private gain or lobby pressure. |
| Review delay | `delay_review` | Separates risk control from procedural cost. |
| Bicameral conflict | `conflict_chambers` | Records disagreement, navette, amendment conflict, override, or deadlock. |

## Support Diagnostics to Separate

| Diagnostic | Definition needed | Why it matters |
|---|---|---|
| National public support | Population-weighted support across all represented people. | Basic public-support benchmark. |
| District support | Distribution of support across districts. | Detects geographically uneven representation. |
| Affected-group support | Support or harm among directly affected groups. | Detects majority-supported concentrated harm. |
| Lower-chamber coalition support | Support among lower-house voting coalition. | Separates chamber voting from population support. |
| Upper-chamber coalition support | Support among upper-house voting coalition. | Detects malapportioned or territorially weighted support. |
| Committee coalition support | Support within committee or reporting coalition. | Detects committee gatekeeping/capture. |
| Population-weighted enactment support | Support weighted by population, not seat count. | Needed for representation claims. |
| Chamber-weighted enactment support | Support weighted by seats/chamber votes. | Shows institutional aggregation. |
| Representation gap | Difference between chamber-weighted and population-weighted support. | Core malapportionment metric. |

## Domain-Aware Status Quo

Required model change:

- Replace or supplement scalar status quo with domain-specific status quo values.
- Bills should update the status quo for their own issue domain.
- Cross-domain packages should update multiple domain states only when explicitly modeled.
- Metrics should report whether a bill's apparent revision moderation is domain-specific or an artifact of scalar compression.

Minimum implementation target:

```text
q[domain][t] -> q[domain][t+1] after enactment/revision/review
```

## Chamber Architecture Metrics

Required metrics:

- malapportionment index;
- population-seat distortion;
- district magnitude;
- lower/upper chamber support gap;
- bicameral conflict rate;
- upper-chamber amendment rate;
- upper-chamber veto rate;
- lower-house override rate;
- navette/conference rounds;
- review delay;
- committee reporting rate;
- committee capture;
- review-body intervention rate.

## Minimum Paper-Ready Model Gate

Before drafting, the simulator should output:

- population-weighted support;
- chamber-weighted support;
- district support distribution summaries;
- affected-group support summaries;
- chamber coalition support;
- malapportionment and population-seat distortion;
- domain-aware status quo movement;
- committee capture by assignment/power condition;
- review delay and correction outcomes.
