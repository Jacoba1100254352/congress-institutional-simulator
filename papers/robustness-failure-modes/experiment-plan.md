# Experiment Plan

## Status

Readiness level: adversary schema, pilot mapping, and first A1/A2/A3/A4/A5/A6/A7/A8 executable pilots implemented; full adversary program not complete.

The current `make manipulation-stress`, `make failure-trace-report`, `make adversarial-stress-manifest`, and `make ablation-analysis` outputs include pilot screens, schema artifacts, and bounded executable A1 clone/decoy through A8 public-support-distortion stress runs. They are not enough for a standalone paper because A9 does not yet have executable mixed-adversary behavior, A1-A8 still lack broader mechanism coverage and seed sensitivity, and temporal or substantive recovery/correction remains incomplete beyond bounded A7 queue recovery and A8 same-case signal correction.

## Existing Baseline Commands

Use these commands to refresh current pilot artifacts:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make ablation-analysis
make manipulation-stress
make failure-trace-report
make adversarial-stress-manifest
make mechanism-diagnostics
```

Existing outputs:

- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.md`
- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.md`
- `reports/adversary-catalog.csv`
- `reports/adversary-catalog.md`
- `reports/adversarial-stress-manifest.json`
- `reports/adversarial-stress-run-manifest.json`
- `reports/adversarial-stress-summary.csv`
- `reports/adversarial-stress-summary.md`
- `reports/adversarial-failure-traces.jsonl`
- `reports/adversarial-stress-a2-run-manifest.json`
- `reports/adversarial-stress-a2-summary.csv`
- `reports/adversarial-stress-a2-summary.md`
- `reports/adversarial-failure-traces-a2.jsonl`
- `reports/adversarial-stress-a3-run-manifest.json`
- `reports/adversarial-stress-a3-summary.csv`
- `reports/adversarial-stress-a3-summary.md`
- `reports/adversarial-failure-traces-a3.jsonl`
- `reports/adversarial-stress-a4-run-manifest.json`
- `reports/adversarial-stress-a4-summary.csv`
- `reports/adversarial-stress-a4-summary.md`
- `reports/adversarial-failure-traces-a4.jsonl`
- `reports/adversarial-stress-a5-run-manifest.json`
- `reports/adversarial-stress-a5-summary.csv`
- `reports/adversarial-stress-a5-summary.md`
- `reports/adversarial-failure-traces-a5.jsonl`
- `reports/adversarial-stress-a6-run-manifest.json`
- `reports/adversarial-stress-a6-summary.csv`
- `reports/adversarial-stress-a6-summary.md`
- `reports/adversarial-failure-traces-a6.jsonl`
- `reports/adversarial-stress-a7-run-manifest.json`
- `reports/adversarial-stress-a7-summary.csv`
- `reports/adversarial-stress-a7-summary.md`
- `reports/adversarial-failure-traces-a7.jsonl`
- `reports/adversarial-stress-a8-run-manifest.json`
- `reports/adversarial-stress-a8-summary.csv`
- `reports/adversarial-stress-a8-summary.md`
- `reports/adversarial-failure-traces-a8.jsonl`
- `reports/adversarial-failure-trace-index.csv`
- `reports/adversarial-failure-trace-index.md`
- `reports/adversarial-pilot-cell-map.csv`
- `reports/adversarial-pilot-cell-map.md`

## Required Implementation Tasks

1. Extend the new explicit adversary catalog under `src/main/java/congresssim/institution/adversary/` into executable adversary action records.
2. Add adversary configuration to campaign and scenario construction.
3. Add attack-budget and information-level parameters.
4. Add same-seed baseline pairing for every attacked cell.
5. Add trace logging for attack actions and outcome paths.
6. Add aggregation for attack success rate, worst-case degradation, median degradation, recovery/correction rate, and administrative burden under attack.
7. Add report scripts under `scripts/reporting/`.
8. Add deterministic tests for adversary configuration, seeded attack action selection, metric signs, and trace schema.

## Proposed Make Targets

```make
adversarial-stress
attack-budget-sweep
worst-case-degradation-report
failure-trace-report
defense-cost-sweep
```

The targets should write generated reports under `reports/` and intermediate traces under `out/`.

## Experiment 0: Schema and Baseline Pairing

Purpose: create the infrastructure required before substantive attacks.

Required outputs:

- `reports/adversarial-stress-manifest.json` (schema precursor exists);
- `reports/adversarial-pilot-cell-map.csv` and `.md` (aggregate pilot map exists);
- `reports/adversarial-stress-summary.csv` and `.md` (A1 executable pilot exists);
- `reports/adversarial-failure-traces.jsonl` (A1 executable pilot exists);
- `reports/adversarial-stress-a2-summary.csv` and `.md` (A2 executable pilot exists);
- `reports/adversarial-failure-traces-a2.jsonl` (A2 executable pilot exists);
- `reports/adversarial-stress-a3-summary.csv` and `.md` (A3 executable pilot exists);
- `reports/adversarial-failure-traces-a3.jsonl` (A3 executable pilot exists);
- `reports/adversarial-stress-a4-summary.csv` and `.md` (A4 executable pilot exists);
- `reports/adversarial-failure-traces-a4.jsonl` (A4 executable pilot exists);
- `reports/adversarial-stress-a5-summary.csv` and `.md` (A5 executable pilot exists);
- `reports/adversarial-failure-traces-a5.jsonl` (A5 executable pilot exists);
- `reports/adversarial-stress-a6-summary.csv` and `.md` (A6 executable pilot exists);
- `reports/adversarial-failure-traces-a6.jsonl` (A6 executable pilot exists);
- `reports/adversarial-stress-a7-summary.csv` and `.md` (A7 executable pilot exists);
- `reports/adversarial-failure-traces-a7.jsonl` (A7 executable pilot exists);
- `reports/adversarial-stress-a8-summary.csv` and `.md` (A8 executable pilot exists);
- `reports/adversarial-failure-traces-a8.jsonl` (A8 executable pilot exists).

Pilot precursor already available: `reports/adversarial-failure-trace-index.csv` and `.md` rank seven aggregate manipulation-stress comparisons as trace candidates. `reports/adversarial-pilot-cell-map.csv` joins those candidates and available executable artifacts to the A1-A9 catalog. The A1-A8 executable pilots now write same-generated-world per-bill traces and attack success summaries for clone/decoy pressure, poison-pill/sequencing pressure, public-input manipulation pressure, bad-faith harm-claim pressure, proposal-flooding pressure, lobbying-camouflage pressure, administrative overload, and public-support distortion. The full trace requirement remains incomplete for A9, broader mechanism families, seed sensitivity, and temporal or substantive recovery/correction beyond bounded A7/A8 evidence.

Acceptance checks:

- every attack row has a same-seed baseline row;
- every adversary row maps to an explicit A1-A9 catalog entry;
- signs are consistent, where positive degradation means worse attacked outcome;
- untested cells are represented as missing or explicitly `not_applicable`, never silently omitted.

## Experiment 1: Clone/Decoy Attack

Target family: content selection and alternative comparison.

Representative mechanisms:

- `simple-majority-alternatives-pairwise`;
- `pairwise-amendment-tournament-majority`;
- strategic tournament variants if retained.

Adversary: A1 clone/decoy proposer.

Required sweep:

- budgets: 1, 3, and 6 added alternatives, or equivalent low/medium/high slots;
- information: medium and high;
- seeds: at least the main paper seed plus four independent base seeds.

Required outputs:

- selected-alternative quality loss;
- low-support enactment change;
- attack success rate;
- worst-case and median degradation;
- at least one trace where a clone or decoy changes the selected outcome.

Current A1 pilot status:

- `reports/adversarial-stress-summary.csv` reports six A1 budget/information cells.
- `reports/adversarial-failure-traces.jsonl` contains 3,600 same-generated-world per-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers the pairwise policy-tournament mechanism only; it still needs broader mechanism coverage before C3 can become draft-ready.

## Experiment 2: Poison-Pill and Sequencing Attack

Target family: amendment and tournament systems.

Representative mechanisms:

- pairwise amendment tournament;
- committee amendment and revision;
- negotiated amendment variants after they exist.

Adversary: A2 poison-pill or sequencing actor.

Required outputs:

- high-benefit blockage rate;
- harm/capture increase among enacted bills;
- ordering sensitivity;
- recovery through substitute selection, review, or rollback where applicable.

Current A2 pilot status:

- `reports/adversarial-stress-a2-summary.csv` reports six A2 budget/information cells.
- `reports/adversarial-failure-traces-a2.jsonl` contains 1,800 same-generated-world per-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers the multi-round amendment-majority mechanism only; broader amendment, committee, tournament, and recovery paths remain required before C4 can become draft-ready.

## Experiment 3: Public-Input and Public-Support Manipulation

Target family: objection windows, petitions, and citizen panels.

Representative mechanisms:

- `public-objection-majority`;
- citizen-panel or citizen-assembly variants;
- challenge-token variants only if public input affects the path.

Adversaries: A3 public-input manipulator and A8 public-support distortion actor.

Required outputs:

- administrative burden increase;
- false-positive delay/blockage;
- false-negative clearance;
- public-preference distortion;
- low-support enactment caused by distorted public signals;
- review or correction rate;
- attack success rate by budget and information level.

Current A3 pilot status:

- `reports/adversarial-stress-a3-summary.csv` reports six A3 budget/information cells.
- `reports/adversarial-failure-traces-a3.jsonl` contains 1,800 same-generated-world per-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers a public-objection plus citizen-panel majority path only; petitions, challenge-token variants, broader mechanism coverage, and external public-comment or panel benchmarks remain required before C5 can become draft-ready. A8 now supplies a separate direct-signal pilot rather than extending this formal-input path.

Current A8 pilot status:

- `reports/adversarial-stress-a8-summary.csv` reports 18 mechanism/budget/information cells across signal-reliant and constituent-verified majority paths.
- `reports/adversarial-failure-traces-a8.jsonl` contains 5,400 same-world, same-bill, same-status-quo, same-vote-random trace rows.
- Generated support, public benefit, affected-group support, concentrated harm, and private gain remain latent evaluation values while observable support, salience, campaign spend, and attention spend change.
- Both A8 paths record zero objection-window and citizen-panel activity, preserving the A3/A8 analytical boundary.
- The constituent-verified path reports same-case signal correction; this is not post-enactment or temporal recovery.
- Additional signal-dependent mechanisms, seed sensitivity, externally grounded signal-shift magnitudes, and temporal correction remain required before C14 can become draft-ready.

## Experiment 4: Bad-Faith Harm Claims

Target family: harm-protection and affected-group systems.

Representative mechanisms:

- `harm-weighted-majority`;
- compensation or affected-group variants;
- portfolio harm-review path.

Adversary: A4 bad-faith harm claimant.

Required outputs:

- false-positive harm-review burden;
- false-negative concentrated-harm passage;
- administrative cost under claim pressure;
- recovery or correction after false review.

Current A4 pilot status:

- `reports/adversarial-stress-a4-summary.csv` reports three medium-information A4 harm-claim budget cells.
- `reports/adversarial-failure-traces-a4.jsonl` contains 900 same-generated-world per-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers the harm-weighted majority path only with targeted synthetic harm-claim cases; compensation, affected-group consent, portfolio review paths, broader mechanism coverage, seed sensitivity, and external claim-process benchmarks remain required before C6 can become draft-ready.

## Experiment 5: Proposal Flooding

Target family: agenda access and open-calendar systems.

Representative mechanisms:

- `open-rule-calendar-majority`;
- `agenda-lottery-majority`;
- leadership or committee gatekeeping variants where capacity can be exhausted.

Adversary: A5 proposal flooder.

Required outputs:

- floor load;
- review load;
- high-benefit bill crowdout;
- low-support enactment;
- policy-yield change.

Current A5 pilot status:

- `reports/adversarial-stress-a5-summary.csv` reports six A5 budget/information cells.
- `reports/adversarial-failure-traces-a5.jsonl` contains 1,800 same-generated-world per-original-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers a fixed-capacity weighted agenda-lottery majority path only; open-rule calendars, proposal-cost screens, committee/leadership gatekeeping, review-load pathways, broader seed sensitivity, and external agenda-load benchmarks remain required before C7 can become draft-ready.

Boundary: keep default-pass mechanisms as a small sensitivity check, not the center of this experiment.

## Experiment 6: Lobbying Camouflage

Target family: anti-capture and influence-screen systems.

Representative mechanisms:

- `anti-capture-access-majority`;
- `anti-capture-majority-bundle`;
- `influence-system-majority`.

Adversary: A6 lobbying camouflage actor.

Required outputs:

- captured bills passing access screens;
- capture increase among enacted bills;
- anti-lobby pass-rate effects;
- cases where visible spend falls but generated capture persists.
- defensive-lobbying backlash as a separate tagged cell, not a substitute for camouflage.

Current A6 pilot status:

- `reports/adversarial-stress-a6-summary.csv` reports six A6 budget/information cells.
- `reports/adversarial-failure-traces-a6.jsonl` contains 1,800 same-generated-world per-bill trace rows.
- Recovery/correction remains `not_modeled`.
- The current pilot covers a public-interest anti-capture screen plus influence-system majority path only; default-pass anti-capture bundles, audit-trust dynamics across repeated bills, defensive anti-reform lobbying, seed sensitivity, and external lobbying-disclosure or proxy-sponsorship benchmarks remain required before C8 can become draft-ready.

## Experiment 7: Administrative Overload Integration

Target family: layered portfolio systems.

Representative mechanisms:

- `portfolio-hybrid-legislature`;
- `expanded-portfolio-hybrid-legislature`;
- risk-routed systems if they are used as simpler comparators.

Adversary: A7 administrative overload coalition.

Required outputs:

- administrative cost;
- queue or capacity saturation;
- risk-control degradation;
- correction/recovery after overload;
- robustness/cost frontier inputs.

Current A7 pilot status:

- `reports/adversarial-stress-a7-summary.csv` reports six A7 budget/information cells.
- `reports/adversarial-failure-traces-a7.jsonl` contains 1,800 same-generated-world per-bill trace rows.
- The pilot reports review-capacity saturation, queue overflow, ordinary-majority fallback, latent-risk control failure, administrative burden, and no-case recovery cycles after the attack window.
- The current pilot covers the portfolio-hybrid safeguard path only with synthetic capacity and recovery assumptions; expanded-portfolio and risk-routed comparators, multi-seed sensitivity, calibration to staffing or review-load data, and substantive correction of enacted failures remain required before C9 can become draft-ready.

## Experiment 8: Mixed Adversary Case

Target family: mechanisms with multiple exposed surfaces.

Representative mechanisms:

- content selection plus amendment/tournament systems;
- public-input plus harm-review systems;
- anti-capture plus open-calendar systems;
- portfolio safeguards.

Adversary: A9 mixed adversary portfolio.

Required sweep:

- fixed total attack budget allocated across 2-4 attack types;
- medium and high information;
- at least three attack portfolios:
  - clone/decoy plus poison pill;
  - astroturf plus bad-faith harm claims;
  - proposal flooding plus lobbying camouflage plus public-support distortion.

Required outputs:

- best single-attack degradation under the same budget;
- mixed-attack degradation;
- interaction or superadditive loss;
- attack success rate;
- administrative burden under interaction;
- recovery/correction failure rate;
- at least one trace where the mixed attack succeeds although the strongest single attack does not.

## Deferred Experiment: Strategic Silence

Strategic silence under burden-shifting rules may be useful, but it is not part of the first-wave paper gate. Add it only after Experiments 1-8 are complete and only if it answers a distinct robustness question.

Required boundary if implemented:

- do not make burden-shifting or default enactment the paper's central frame;
- report unused challenge-token rate and objection-suppression success;
- compare against other attack families without giving it special priority.

## Full Draft Gate

Do not draft the paper until:

- Experiments 1-8 have generated reports;
- at least five seeds are included for core attack families;
- attack success rates are computed;
- worst-case and median degradation are reported;
- failure traces exist for at least three attack families;
- validation gaps are documented in `validation-needs.md`;
- `make test` passes after implementation.
