# Validation Needs

## Status

Readiness level: validation gaps identified; validation not sufficient for manuscript claims beyond bounded synthetic failure hypotheses.

This robustness paper can proceed as a synthetic adversarial-stress study, but it must be explicit about what is and is not validated.

## Current Validation Assets

| Asset | Current value | Limitation for this paper |
|---|---|---|
| `reports/calibration-baseline.md` | Conventional baseline passed 7 of 7 screening checks. | Screens broad legislative-flow plausibility, not adversarial behavior. |
| `reports/empirical-validation-readiness.md` | 12 of 12 raw validation datasets are present and shaped. | Many datasets are bounded proxies rather than direct validation targets for robustness-relevant mechanisms. |
| `reports/seed-robustness-summary.md` | Main comparison campaign has multi-seed summaries. | Does not cover explicit adversary attacks; A9 now has a separate fixed-specification replication. |
| `reports/adversarial-replication-a9-summary.md` and seed-results CSV | Thirty fixed base seeds provide seed-level intervals for success, median/worst degradation, interaction, superadditive loss, recovery failure, and burden across 18 A9 cells. | Covers only the fixed A9 allocations, mechanisms, resource conversion, interaction coefficients, capacity, and recovery assumptions; it is simulation uncertainty, not empirical validation. |
| `reports/manipulation-stress-summary.md` | Seven pilot stress comparisons exist. | Not budgeted, not actor-specific, and no attack success rates. |
| `reports/adversary-catalog.md` and `reports/adversarial-stress-manifest.json` | A1-A9 adversary schema is now generated from simulator code. | The catalog is schema-only; implemented behavior and limits are documented in the separate A1-A9 runner artifacts. |
| `reports/adversarial-pilot-cell-map.md` | Maps aggregate pilot cells and executable A1-A9 artifacts to the adversary catalog. | It is a readiness map rather than result evidence; every row remains below the manuscript gate. |
| A1-A9 adversarial summaries and trace JSONL artifacts under `reports/` | Bounded executable A1-A9 pilots have budget/information cells, success rates, median/worst degradation, and same-generated-world trace rows. A7 reports queue recovery, A8 reports same-case signal correction, and A9 compares three fixed-budget mixed portfolios with full-budget and allocated-component single controls. | The pilots cover bounded mechanism paths; A1-A8 seed sensitivity, broad mechanism coverage, temporal or substantive correction beyond bounded A7-A9 evidence, and externally validated attack rates remain missing. |
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
| Seed sensitivity | A9 now exceeds the minimum with 30 fixed base seeds. A1-A8 core attack families still need at least five seeds or an explicit reason if a smaller sweep is used. |

## Empirical Validation Gaps

The current readiness report says 12 of 12 raw validation datasets are present. Incomplete proxy coverage still matters for robustness claims:

| Missing or incomplete input | Why it matters |
|---|---|
| bill-topic public opinion beyond `district_public_opinion.csv` | Needed to separate public-input manipulation from synthetic public-support assumptions; the current CES district aggregate is only a weak proxy. |
| campaign-finance and lobbying linkage beyond `campaign_finance.csv`, `campaign_finance_linkage.csv`, `reports/campaign-finance-issue-context.csv`, `reports/campaign-finance-member-context.csv`, `reports/campaign-finance-district-context.csv`, `reports/campaign-finance-sponsor-bill-context.csv`, `reports/lobbying-issue-linkage.csv`, and `reports/lobbying-bill-policy-context.csv` | Needed for lobbying camouflage, proxy sponsorship, outside spending, and defensive lobbying claims beyond bounded OpenFEC concentration summaries, FEC recipient metadata, issue-sector context, member context, House-candidate district context, candidate-to-sponsored-bill context, LDA issue taxonomy, and shared-policy-area bill context. |
| emergency-order court review beyond `court_review.csv` | Needed for emergency-review behavior; SCDB merits-case invalidation and signed-opinion summaries are ready. |
| implementation feedback beyond `rulemaking_implementation.csv`, `rulemaking_authority_linkage.csv`, `rulemaking_history_linkage.csv`, `rulemaking_comment_metadata.csv`, and `rulemaking_comment_records.csv` | Needed for enforcement, nonenforcement, high-volume comments, comment-text review, Unified Agenda stages, appropriations, and administrative-capacity claims beyond final-rule effective-date delay, authority text, proposed-rule metadata, bounded comment metadata, bounded small/zero-comment comment-record metadata, and timing metadata. |
| full statutory lineage beyond `law_revision_history.csv`, `law_revision_bill_linkage.csv`, `reports/statutory-lineage-source-scan.csv`, `reports/statutory-lineage-target-section-triage.csv`, `reports/statutory-lineage-olrc-current-scan.csv`, `reports/statutory-lineage-olrc-historical-scan.csv`, `reports/statutory-lineage-olrc-annual-text-diff.csv`, `reports/statutory-lineage-adjudication.csv`, `reports/statutory-lineage-target-review-packets.csv`, `reports/statutory-lineage-target-section-diff-review.csv`, `reports/statutory-lineage-target-lifecycle-bridge.csv`, and bounded rulemaking metadata | Needed for recovery, repeal, sunset, reauthorization, and correction claims beyond bounded Congress.gov title/summary text flags, bill/action metadata, official GovInfo public-law text scans, target-section triage, current OLRC page availability, annual OLRC availability, automated annual section-change/text-diff cues, official OLRC post-only public-law marker evidence, target-section review packets, the thirteen-public-law target-section diff-review pilot, target-section lifecycle bridge context, authority text, proposed-history metadata, comment metadata, and timing metadata. |
| comparative chamber and party-system data beyond `comparative_institutions.csv` | Needed before comparing failure modes across chamber or party-system structures externally; the current QoG/OWID/V-Dem file is a bounded profile proxy. |

Even after those datasets exist, they should validate observable flow and boundary conditions. They will not directly validate generated public benefit, generated harm, or true adversary intent.

## Modeling Weaknesses to State

- Policy space remains highly stylized and primarily one-dimensional.
- Generated public benefit, public support, concentrated harm, and capture are model signals, not observed quantities.
- Adversary budgets are assumed, not estimated from real actor resources.
- Parties, committees, courts, media, agencies, and elections do not fully co-evolve.
- Administrative cost is an index, not a measured staff-time or fiscal-cost estimate.
- Public-input manipulation is simplified and does not model communication networks.
- Lobbying camouflage is implemented only as a bounded synthetic pilot and still depends on unvalidated proxy-sponsor assumptions.
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
2. Extend adversarial seed robustness from the completed fixed-specification A9 panel to A1-A8 core attack families.
3. Extend empirical readiness for bill-topic district opinion beyond sponsor-district bill policy-area context, affected-group mapping, campaign-finance linkage beyond FEC recipient metadata, bounded issue-sector context, matched member context, bounded House-candidate district context, and bounded candidate-to-sponsored-bill context to reviewed targets, committee-action influence, and outcomes, emergency court review, fuller implementation beyond timing and bounded comment metadata, full statutory lineage beyond Congress.gov bill/action metadata, and comparative chamber/productivity sources beyond the current profile proxy.
4. Map every empirical source to only the simulator quantities it can plausibly check.
5. Add a validation-boundary table to any future manuscript.
6. Keep unvalidated constructs labeled as synthetic.
