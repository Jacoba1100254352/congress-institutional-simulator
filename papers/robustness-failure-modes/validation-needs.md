# Validation Needs

## Status

Readiness level: validation gaps identified; validation not sufficient for manuscript claims beyond bounded synthetic failure hypotheses.

This robustness paper can proceed as a synthetic adversarial-stress study, but it must be explicit about what is and is not validated.

## Current Validation Assets

| Asset | Current value | Limitation for this paper |
|---|---|---|
| `reports/calibration-baseline.md` | Conventional baseline passed 7 of 7 screening checks. | Screens broad legislative-flow plausibility, not adversarial behavior. |
| `reports/empirical-validation-readiness.md` | 6 of 12 raw validation datasets are present and shaped. | Missing datasets cover several robustness-relevant mechanisms. |
| `reports/seed-robustness-summary.md` | Main comparison campaign has multi-seed summaries. | Does not cover new explicit adversary attacks. |
| `reports/manipulation-stress-summary.md` | Seven pilot stress comparisons exist. | Not budgeted, not actor-specific, and no attack success rates. |
| `reports/ablation-analysis-summary.md` | Mechanism component effects are summarized. | Ablations are not adversarial validation. |

## Internal Validation Required Before Drafting

| Need | Required check |
|---|---|
| Deterministic adversary behavior | Same seed, same adversary config, same attack actions and outcomes. |
| Same-seed pairing | Every attack row has a paired baseline row for the same seed, case, scenario, and generated world when possible. |
| Metric sign consistency | Positive degradation means the attacked condition is worse for the named metric. |
| Budget monotonicity audit | Larger budgets should not be assumed to worsen every outcome, but reversals must be flagged and inspected. |
| Information-level audit | Medium/high information attacks should report what additional variables were used. |
| Trace completeness | Failure traces must include actor, budget, action, path, baseline outcome, attacked outcome, and metric deltas. |
| Mixed-attack budget accounting | Mixed adversary portfolios must use a fixed total budget and be compared against the strongest same-budget single attack. |
| Regression tests | Add tests for adversary config parsing, seeded action selection, trace schema, and summary aggregation. |
| Seed sensitivity | Core attack families need at least five seeds or an explicit reason if a smaller sweep is used. |

## Empirical Validation Gaps

The current readiness report says 6 of 12 raw validation datasets are present. Missing datasets matter for robustness claims:

| Missing or incomplete input | Why it matters |
|---|---|
| `district_public_opinion.csv` | Needed to separate public-input manipulation from synthetic public-support assumptions. |
| `campaign_finance.csv` | Needed for lobbying camouflage, proxy sponsorship, outside spending, and defensive lobbying claims. |
| `court_review.csv` | Needed for claims about review, invalidation, and correction. |
| `rulemaking_implementation.csv` | Needed for post-enactment delay, enforcement, and administrative-capacity claims. |
| `law_revision_history.csv` | Needed for recovery, repeal, sunset, reauthorization, and correction claims. |
| `comparative_institutions.csv` | Needed before comparing failure modes across chamber or party-system structures externally. |

Even after those datasets exist, they should validate observable flow and boundary conditions. They will not directly validate generated public benefit, generated harm, or true adversary intent.

## Modeling Weaknesses to State

- Policy space remains highly stylized and primarily one-dimensional.
- Generated public benefit, public support, concentrated harm, and capture are model signals, not observed quantities.
- Adversary budgets are assumed, not estimated from real actor resources.
- Parties, committees, courts, media, agencies, and elections do not fully co-evolve.
- Administrative cost is an index, not a measured staff-time or fiscal-cost estimate.
- Public-input manipulation is simplified and does not model communication networks.
- Lobbying camouflage is not yet implemented and would require proxy-sponsor assumptions.
- Harm-claim behavior lacks a validated legal or administrative process model.
- Recovery/correction behavior is partial and may overstate institutional repair capacity if implemented optimistically.

## Claim Boundaries

Claims allowed after experiments:

- "Under bounded synthetic adversaries, mechanism family X shows vulnerability pattern Y."
- "Worst-case degradation differs from median degradation in these modeled attack cells."
- "Layered safeguards trade off attack resistance and administrative burden in this simulator."

Claims not allowed without further validation:

- "Real-world actors can achieve these attack rates."
- "A given real legislature is robust or fragile."
- "The model validates adoption of a reform."
- "A mechanism is generally superior across legislative institutions."
- "Observed public opinion, harm, or lobbying behavior is reproduced."

## Validation Roadmap

1. Finish internal adversary trace and summary validation.
2. Add adversarial seed robustness.
3. Extend empirical readiness for campaign finance, district opinion, review/courts, implementation, law revision, and comparative institutions.
4. Map every empirical source to only the simulator quantities it can plausibly check.
5. Add a validation-boundary table to any future manuscript.
6. Keep unvalidated constructs labeled as synthetic.
