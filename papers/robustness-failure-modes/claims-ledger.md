# Claims Ledger

## Status

Readiness level: bounded synthetic evidence only. A1-A9 now have fixed-specification multi-seed evidence, but most substantive claims remain conditional.

Allowed language now: "the A1-A9 catalog, bounded executable pilots, and fixed 30-base-seed panels provide synthetic first-wave evidence for nine attack families; binary success and substantive degradation diverge in some A1-A8 cells, while fixed-specification A9 mixed-only failures recur even though average interaction degradation is usually subadditive relative to the strongest full-budget single attack."

Disallowed language now: "the simulator proves these mechanisms are robust," "this validates institutional design claims," or "these results show which real institutions should be adopted."

## Ledger

| ID | Proposed claim | Current support | Evidence gap | Validation gap | Allowed wording now | Status |
|---|---|---|---|---|---|---|
| C1 | The repo can support a robustness breakout distinct from the ACM framework paper. | The simulator has relevant mechanism surfaces, pilot reports, an explicit A1-A9 adversary catalog under `src/main/java/congresssim/institution/adversary/`, bounded executable stress runners for all nine entries, and fixed-specification 30-base-seed replication for every entry. | Needs broader mechanism coverage, alternative A9 and capacity specifications, stronger correction tests, and validation. | External adversarial behavior is not validated. | The breakout is feasible and now has complete bounded first-wave implementation plus fixed-specification multi-seed evidence for all nine attack families. | Planning-supported. |
| C2 | Existing manipulation-stress outputs identify candidate failure modes. | `reports/manipulation-stress-summary.md` reports seven pilot stress comparisons, `reports/adversarial-failure-trace-index.md` ranks aggregate trace candidates, and `reports/adversarial-pilot-cell-map.md` maps them to catalog entries. | Stressors are fixed scenarios, not actor models with budgets, information, or per-bill attack paths. | No real attack-rate comparison. | Pilot screens motivate targeted adversary experiments. | Supported as motivation only. |
| C3 | Clone/decoy pressure is a high-priority content-selection attack. | The bounded A1 pilot has 3,600 same-generated-world traces. Its 30-seed panel covers 108,000 evaluated rows and 54,780 successes; mean public-benefit-loss intervals are positive in all six cells, with means from 0.0108 to 0.0407. | Needs broader mechanism coverage, recovery/correction behavior, and parameter sensitivity beyond the first A1 specification. | No empirical validation of clone/decoy frequency or actor knowledge. | In the fixed A1 synthetic specification, clone/decoy pressure produces repeatable paired degradation in the pairwise policy-tournament mechanism. | Conditional. |
| C4 | Poison-pill and sequencing attacks are plausible risks for amendment/tournament systems. | The bounded A2 pilot has 1,800 same-generated-world traces. Its 30-seed panel covers 54,000 rows and 22,580 successes; mean public-benefit-loss intervals are positive in all six cells, with means from 0.0027 to 0.0441. | Needs broader amendment, tournament, and committee coverage, recovery/correction behavior, and parameter sensitivity. | No empirical rider, amendment, or agenda-order benchmark. | In the fixed A2 synthetic specification, poison-pill/sequencing pressure produces repeatable public-benefit loss in the multi-round amendment-majority path. | Conditional. |
| C5 | Public-input systems may be vulnerable to astroturf, noise, or panel manipulation. | The bounded A3 pilot has 1,800 traces and remains distinct from A8. Its 30-seed panel covers 54,000 rows and 50,410 successes; all six signed public-preference-distortion intervals are below zero, with means from -0.1459 to -0.0137. | Needs petition and challenge-token coverage, temporal recovery/correction behavior, broader mechanisms, and parameter sensitivity. | Need public-comment, panel, or objection-process data before external claims. | In the fixed A3 synthetic specification, public-input manipulation produces repeatable signed distortion in the public-objection plus citizen-panel path, distinct from A8 direct-signal manipulation. | Conditional. |
| C6 | Harm-protection systems may be vulnerable to bad-faith claims. | The bounded A4 pilot has 900 traces. Its 30-seed panel covers 27,000 rows and 21,984 successes; mean false-positive-burden intervals are positive in all three cells, with means from 0.1215 to 0.5692. | Needs compensation, affected-group consent, portfolio review paths, recovery/correction behavior, and parameter sensitivity beyond the first A4 specification. | Need claim-process, court, or review data before external claims. | In the fixed A4 synthetic specification, bad-faith claims produce repeatable false-positive burden in the harm-weighted majority path. | Conditional. |
| C7 | Proposal flooding can be studied as a capacity attack. | The bounded A5 pilot has 1,800 traces. Its 30-seed panel records 54,000 binary successes in 54,000 rows, but mean policy-yield loss is positive in five cells and crosses zero in the low-information, budget-1 cell. | Needs open-rule calendars, proposal-cost screens, committee/leadership gatekeeping, review-load pathways, recovery/correction behavior, and parameter sensitivity. | Need empirical bill-volume, agenda, committee, and floor-load anchors before external claims. | In the fixed A5 synthetic specification, the modeled flooding success condition is universal, but that does not imply a uniformly nonzero policy-yield loss. | Conditional. |
| C8 | Anti-capture systems may fail through lobbying camouflage. | The bounded A6 pilot has 1,800 traces. Its 30-seed panel covers 54,000 rows and 3,028 strict successes; mean observed-screen-risk-decline intervals are positive in all six cells, with means from 0.2168 to 0.4780. | Needs default-pass anti-capture bundles, repeated-bill audit-trust dynamics, defensive anti-reform lobbying, recovery/correction behavior, and parameter sensitivity. | Campaign-finance, proxy-sponsorship, and lobbying-disclosure validation are incomplete. | In the fixed A6 synthetic specification, visible screening risk declines repeatably even though the stricter attack-success event is uncommon. | Conditional. |
| C9 | Layered safeguards can trade robustness for administrative cost. | The bounded A7 pilot has 1,800 traces. Its 30-seed panel covers 54,000 rows and 34,051 successes; one low-budget cell has no binary success, while mean risk-control-degradation intervals are positive in all six cells. | Needs expanded-portfolio and risk-routed comparators, substantive correction after overflow enactment, and capacity-parameter sensitivity. | Administrative capacity, recovery, and cost proxies are not externally calibrated. | In the fixed A7 synthetic specification, overload exhibits a modeled binary threshold even though risk-control degradation is nonzero below that threshold. | Conditional. |
| C10 | Average-case performance can hide adversarial failure. | The A1-A9 stress summaries separate mean, median, worst-case, and trace evidence. The A1-A8 panel shows binary and primary-effect divergence in A5 and A7, while A9 distinguishes mixed-only events from average interaction. | Need broader mechanisms, parameter sweeps, and substantive correction. | No external adversarial benchmark. | The fixed A1-A9 synthetic panels provide bounded examples of why binary failures, average degradation, and worst cases must be reported separately. | Conditional. |
| C11 | Burden-shifting mechanisms have strategic-silence risks. | Burden-shifting scenarios and challenge-token concepts exist. | Strategic-silence model is not implemented. | No empirical challenge-token analogue. | Keep as deferred or appendix case. | Deferred. |
| C12 | A full manuscript is ready. | No. | Broader mechanisms, alternative A9 and capacity specifications, stronger correction evidence, and manuscript synthesis remain incomplete. | External validation remains incomplete. | No full manuscript yet. | No-go. |
| C13 | Mixed adversary portfolios can expose case-level failures that single-attack probes miss, without necessarily causing greater average degradation. | `reports/adversarial-replication-a9-summary.md` covers 30 fixed base seeds, 18 cells, and 162,000 evaluated rows. It records 2,626 strict mixed-only failures. Seed-level 95 percent intervals for mean interaction degradation are below zero in 16 cells, above zero in one, and cross zero in one. The canonical 5,400-row trace artifact retains auditable paths and same-budget controls. | Needs broader mechanism variants, alternative allocation/resource/interaction specifications, and substantive correction/replay. | No empirical benchmark for coordinated multi-actor attack frequency or resource conversion. | In the fixed A9 synthetic specification, mixed-only failures recur across seeds, while average mixed degradation is usually lower than the strongest full-budget single attack. | Conditional. |
| C14 | Public-support distortion is analytically separate from formal public-input manipulation. | The A8 pilot has 5,400 paired traces and preserves latent generated values while changing observable support and salience. Its 30-seed panel covers 162,000 rows and 97,441 successes; mean residual-signal-distortion intervals are positive in all 18 cells, with means from 0.0159 to 0.1815. | Needs additional signal-dependent mechanisms, temporal correction, parameter sensitivity, and externally grounded signal-shift magnitudes. | District opinion now includes one historical related-issue pilot, but it is not a public-campaign effect benchmark. | In the fixed A8 synthetic specification, direct public-support distortion remains analytically separate from A3, and constituent verification attenuates but does not eliminate the injected signal. | Conditional. |

## Evidence Thresholds

A claim can move from conditional to draft-ready only after it has:

- an explicit adversary ID from `adversary-model.md`;
- same-seed baseline and attack comparisons;
- low/medium/high budget results;
- attack success rates;
- worst-case and median degradation;
- seed sensitivity for core metrics;
- at least one auditable failure trace when the claim depends on path behavior;
- comparison against a same-budget single-attack baseline for mixed adversary claims;
- validation limits stated next to the claim.

## Conservative Claim Wording

Use:

- "under this bounded adversary";
- "in the implemented generator";
- "suggests a synthetic failure-mode hypothesis";
- "requires external validation before institutional interpretation."

Avoid:

- "proves";
- "validates";
- "optimal";
- "best institution";
- "real-world attack rate";
- "general legislative design-space result."
