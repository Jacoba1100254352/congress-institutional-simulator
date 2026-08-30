# Claims Ledger

## Status

Readiness level: claim planning only. Most substantive claims are conditional until explicit adversary experiments exist.

Allowed language now: "the A1-A9 catalog defines planned adversary tests, and the A1 clone/decoy through A8 public-support-distortion pilots provide bounded synthetic evidence for eight attack families."

Disallowed language now: "the simulator proves these mechanisms are robust," "this validates institutional design claims," or "these results show which real institutions should be adopted."

## Ledger

| ID | Proposed claim | Current support | Evidence gap | Validation gap | Allowed wording now | Status |
|---|---|---|---|---|---|---|
| C1 | The repo can support a robustness breakout distinct from the ACM framework paper. | The simulator has relevant mechanism surfaces, pilot reports, an explicit A1-A9 adversary catalog under `src/main/java/congresssim/institution/adversary/`, and executable A1-A8 stress runners. | Needs an executable A9 mixed-adversary action and report plus broader A1-A8 coverage. | External adversarial behavior is not validated. | The breakout is feasible as a planned extension. | Planning-supported. |
| C2 | Existing manipulation-stress outputs identify candidate failure modes. | `reports/manipulation-stress-summary.md` reports seven pilot stress comparisons, `reports/adversarial-failure-trace-index.md` ranks aggregate trace candidates, and `reports/adversarial-pilot-cell-map.md` maps them to catalog entries. | Stressors are fixed scenarios, not actor models with budgets, information, or per-bill attack paths. | No real attack-rate comparison. | Pilot screens motivate targeted adversary experiments. | Supported as motivation only. |
| C3 | Clone/decoy pressure is a high-priority content-selection attack. | Current aggregate summary reports material vulnerability for policy tournament clone/decoy stress: directional loss 0.087 and revision-moderation loss 0.046. `reports/adversarial-stress-summary.md` now adds a bounded A1 budget/information pilot with attack success rates, median/worst degradation, and 3,600 same-generated-world per-bill trace rows. | Needs broader mechanism coverage, recovery/correction behavior, and sensitivity beyond the first A1 pilot. | No empirical validation of clone/decoy frequency or actor knowledge. | In the current A1 synthetic pilot, clone/decoy pressure produces measurable paired degradation in the pairwise policy-tournament mechanism. | Conditional. |
| C4 | Poison-pill and sequencing attacks are plausible risks for amendment/tournament systems. | Amendment and bargaining mechanisms exist in the simulator. `reports/adversarial-stress-a2-summary.md` now adds a bounded A2 budget/information pilot with attack success rates, median/worst degradation, and 1,800 same-generated-world per-bill trace rows. | Needs broader amendment/tournament/committee coverage, recovery/correction behavior, and sensitivity beyond the first A2 pilot. | No empirical rider, amendment, or agenda-order benchmark. | In the current A2 synthetic pilot, poison-pill/sequencing pressure can be reported only as a bounded multi-round amendment-majority stress result. | Conditional. |
| C5 | Public-input systems may be vulnerable to astroturf, noise, or panel manipulation. | Current aggregate pilot includes citizen-panel manipulation and astroturf objection pressure. `reports/adversarial-stress-a3-summary.md` adds a bounded A3 budget/information pilot with attack success rates, false-positive blockage, false-negative clearance, low-support enactment, administrative-burden deltas, and 1,800 same-generated-world per-bill trace rows. The A8 runner now supplies a separate direct-signal path with zero objection-window and citizen-panel activity. | Needs petition and challenge-token coverage, temporal recovery/correction behavior, broader mechanism coverage, and seed sensitivity. | Need public-comment, panel, or objection-process data before external claims. | In the current A3 synthetic pilot, public-input manipulation can be reported only as a bounded public-objection plus citizen-panel stress result distinct from the A8 direct-signal pilot. | Conditional. |
| C6 | Harm-protection systems may be vulnerable to bad-faith claims. | Current loose-claims stress exists. `reports/adversarial-stress-a4-summary.md` now adds a bounded A4 medium-information harm-claim pilot with false-positive burden, false-negative clearance, concentrated-harm passage, administrative-burden deltas, and 900 same-generated-world per-bill trace rows. | Needs compensation, affected-group consent, portfolio review paths, recovery/correction behavior, seed sensitivity, and sensitivity beyond the first A4 pilot. | Need claim-process, court, or review data before external claims. | In the current A4 synthetic pilot, bad-faith harm claims can be reported only as a bounded harm-weighted majority stress result. | Conditional. |
| C7 | Proposal flooding can be studied as a capacity attack. | Current agenda-flooding pilot exists. `reports/adversarial-stress-a5-summary.md` now adds a bounded A5 budget/information pilot with high-benefit crowdout, high-benefit blockage, low-support flood enactment, proposal-load, flood-floor-slot, policy-yield, administrative-burden, and 1,800 same-generated-world per-original-bill trace rows. | Needs open-rule calendars, proposal-cost screens, committee/leadership gatekeeping, review-load pathways, recovery/correction behavior, seed sensitivity, and sensitivity beyond the first A5 pilot. | Need empirical bill-volume, agenda, committee, and floor-load anchors before external claims. | In the current A5 synthetic pilot, proposal flooding can be reported only as a bounded fixed-capacity weighted agenda-lottery stress result. | Conditional. |
| C8 | Anti-capture systems may fail through lobbying camouflage. | Lobbying, influence-system, and anti-capture modules exist. `reports/adversarial-stress-a6-summary.md` now adds a bounded A6 budget/information pilot with anti-capture bypass, capture enactment added, shadow-share movement, watchdog-detection decline, observed screen-risk decline, visible-spend decline with capture persistence, administrative-burden deltas, and 1,800 same-generated-world per-bill trace rows. | Needs default-pass anti-capture bundles, repeated-bill audit-trust dynamics, defensive anti-reform lobbying, recovery/correction behavior, seed sensitivity, and sensitivity beyond the first A6 pilot. | Campaign-finance, proxy-sponsorship, and lobbying-disclosure validation are incomplete. | In the current A6 synthetic pilot, lobbying camouflage can be reported only as a bounded public-interest screen plus influence-system stress result. | Conditional. |
| C9 | Layered safeguards can trade robustness for administrative cost. | Ablation and portfolio outputs track administrative cost. `reports/adversarial-stress-a7-summary.md` adds a bounded A7 portfolio-hybrid pilot with capacity saturation, queue overflow, ordinary-majority fallback, latent-risk control failure, administrative burden, and post-attack queue-recovery cycles across six budget/information cells and 1,800 same-generated-world traces. | Needs expanded-portfolio and risk-routed comparators, substantive correction after overflow enactment, multi-seed sensitivity, and capacity-parameter sensitivity. | Administrative capacity, recovery, and cost proxies are not externally calibrated. | In the current A7 synthetic pilot, layered safeguards can be reported only as exhibiting modeled overload thresholds and recovery times under the named capacity assumptions. | Conditional. |
| C10 | Average-case performance can hide adversarial failure. | The ACM framework, pilot reports, aggregate trace index, and A1-A8 stress summaries separate mean, median, worst-case, and per-bill trace evidence for eight attack families. | Need the same reporting for A9, broader mechanisms, and multi-seed runs. | No external adversarial benchmark. | The current A1-A8 pilots can be used as bounded examples of why average stress summaries are not enough. | Conditional. |
| C11 | Burden-shifting mechanisms have strategic-silence risks. | Burden-shifting scenarios and challenge-token concepts exist. | Strategic-silence model is not implemented. | No empirical challenge-token analogue. | Keep as deferred or appendix case. | Deferred. |
| C12 | A full manuscript is ready. | No. | Experiments, traces, and validation gates are missing. | External validation remains incomplete. | No full manuscript yet. | No-go. |
| C13 | Mixed adversary portfolios can expose interactions that single-attack probes miss. | No direct evidence yet; the simulator has enough mechanism surfaces to plan this test. | Need fixed-budget mixed attacks, single-attack baselines, interaction metrics, and traces. | No empirical benchmark for coordinated multi-actor attack frequency. | Mixed attacks are required experiments, not current findings. | Unsupported. |
| C14 | Public-support distortion is analytically separate from formal public-input manipulation. | `reports/adversarial-stress-a8-summary.md` reports 18 A8 mechanism/budget/information cells and `reports/adversarial-failure-traces-a8.jsonl` provides 5,400 paired traces. The runner changes observable support and salience while preserving generated support, benefit, affected-group support, harm, and private gain; both A8 paths record zero objection-window and citizen-panel activity. The constituent-verified path reports same-case correction separately from the signal-reliant path. | Needs additional signal-dependent mechanisms, multi-seed sensitivity, temporal correction, and externally grounded signal-shift magnitudes. | Current district-opinion sources remain proxy-only and no public-campaign effect validation exists. | In the bounded A8 synthetic pilot, direct public-support distortion can be analyzed separately from A3 formal public-input manipulation, and constituent verification attenuates the injected signal under the stated assumptions. | Conditional. |

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
