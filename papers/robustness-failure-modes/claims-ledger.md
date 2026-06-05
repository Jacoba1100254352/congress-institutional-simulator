# Claims Ledger

## Status

Readiness level: claim planning only. Most substantive claims are conditional until explicit adversary experiments exist.

Allowed language now: "pilot stress screens suggest attack surfaces worth testing."

Disallowed language now: "the simulator proves these mechanisms are robust," "this validates institutional design claims," or "these results show which real institutions should be adopted."

## Ledger

| ID | Proposed claim | Current support | Evidence gap | Validation gap | Allowed wording now | Status |
|---|---|---|---|---|---|---|
| C1 | The repo can support a robustness breakout distinct from the ACM framework paper. | The simulator has relevant mechanism surfaces and pilot reports. | Needs explicit adversary implementation and reports. | External adversarial behavior is not validated. | The breakout is feasible as a planned extension. | Planning-supported. |
| C2 | Existing manipulation-stress outputs identify candidate failure modes. | `reports/manipulation-stress-summary.md` reports seven pilot stress comparisons. | Stressors are fixed scenarios, not actor models with budgets and information. | No real attack-rate comparison. | Pilot screens motivate targeted adversary experiments. | Supported as motivation only. |
| C3 | Clone/decoy pressure is a high-priority content-selection attack. | Current summary reports material vulnerability for policy tournament clone/decoy stress: directional loss 0.087 and revision-moderation loss 0.046. | Needs budget sweep, success rate, same-seed baselines, and traces. | No empirical validation of clone/decoy frequency or actor knowledge. | Clone/decoy stress is the strongest current pilot signal. | Conditional. |
| C4 | Poison-pill and sequencing attacks are plausible risks for amendment/tournament systems. | Amendment and bargaining mechanisms exist in the simulator. | No direct poison-pill or sequencing experiment has been run. | No empirical rider, amendment, or agenda-order benchmark. | This is a required experiment, not a result. | Unsupported. |
| C5 | Public-input systems may be vulnerable to astroturf, noise, or panel manipulation. | Current pilot includes citizen-panel manipulation and astroturf objection pressure. | Current observed degradation is limited and not budgeted. | Need public-comment, panel, or objection-process data before external claims. | Current tests show only limited pilot degradation under bounded probes. | Conditional. |
| C6 | Harm-protection systems may be vulnerable to bad-faith claims. | Current loose-claims stress exists. | Need false-positive and false-negative claim model with administrative burden. | Need claim-process, court, or review data. | Bad-faith harm claims remain an unproven attack surface. | Conditional. |
| C7 | Proposal flooding can be studied as a capacity attack. | Current agenda-flooding pilot exists. | Current degradation is limited and lacks capacity/queue metrics. | Need empirical bill-volume, agenda, committee, and floor-load anchors. | Proposal flooding is a planned capacity stress test. | Conditional. |
| C8 | Anti-capture systems may fail through lobbying camouflage. | Lobbying and anti-capture modules exist; defensive backlash pilot exists. | No camouflage/proxy-sponsor adversary is implemented. | Campaign-finance and lobbying-disclosure validation are incomplete. | Camouflage is a required experiment, not a finding. | Unsupported. |
| C9 | Layered safeguards can trade robustness for administrative cost. | Ablation and portfolio outputs already track administrative cost. | Need overload actor, queue saturation, and recovery metrics. | Administrative cost proxy is not externally calibrated. | Current outputs justify testing overload, not claiming real overload thresholds. | Conditional. |
| C10 | Average-case performance can hide adversarial failure. | The ACM framework and pilot reports separate baseline metrics from stress probes. | Need median versus worst-case adversary reporting. | No external adversarial benchmark. | The planned paper will test whether averages hide failure cases. | Conditional. |
| C11 | Burden-shifting mechanisms have strategic-silence risks. | Burden-shifting scenarios and challenge-token concepts exist. | Strategic-silence model is not implemented. | No empirical challenge-token analogue. | Keep as deferred or appendix case. | Deferred. |
| C12 | A full manuscript is ready. | No. | Experiments, traces, and validation gates are missing. | External validation remains incomplete. | No full manuscript yet. | No-go. |
| C13 | Mixed adversary portfolios can expose interactions that single-attack probes miss. | No direct evidence yet; the simulator has enough mechanism surfaces to plan this test. | Need fixed-budget mixed attacks, single-attack baselines, interaction metrics, and traces. | No empirical benchmark for coordinated multi-actor attack frequency. | Mixed attacks are required experiments, not current findings. | Unsupported. |
| C14 | Public-support distortion is analytically separate from formal public-input manipulation. | The simulator tracks public-preference distortion and public signal movement in current reports. | Need an explicit actor that changes public signals while preserving generated support/benefit for evaluation. | No district opinion or public campaign validation yet. | Public-support distortion is a planned attack surface. | Conditional. |

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
