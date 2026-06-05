# Experiment Plan

## Status

Readiness level: experiments specified, implementation not complete.

The current `make manipulation-stress` and `make ablation-analysis` outputs are pilot screens. They are not enough for a standalone paper because they do not yet specify adversary actors, budgets, information levels, attack success rates, worst-case degradation, or failure traces.

## Existing Baseline Commands

Use these commands to refresh current pilot artifacts:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
```

Existing outputs:

- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.md`
- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.md`

## Required Implementation Tasks

1. Add explicit adversary records or classes, for example under `src/main/java/congresssim/institution/adversary/`.
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

- `reports/adversarial-stress-manifest.json`;
- `reports/adversarial-stress-summary.csv`;
- `reports/adversarial-stress-summary.md`;
- `reports/adversarial-failure-traces.jsonl` or equivalent trace artifact.

Acceptance checks:

- every attack row has a same-seed baseline row;
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
