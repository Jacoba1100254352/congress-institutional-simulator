# Experiment Plan

Final decision: NEEDS ADVERSARY EXPERIMENTS FIRST.

The current manipulation-stress campaign is a pilot. A full paper needs explicit adversaries, budget/information sweeps, worst-case reporting, attack success rates, and trace examples.

## Baseline Commands

Run current pilot artifacts:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
```

Current outputs:

- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.md`
- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.md`

## Required Code Tasks

1. Add an adversary model package or equivalent records, for example `src/main/java/congresssim/institution/adversary`.
2. Add adversary configuration to campaign/scenario construction.
3. Add attack-budget and information-level parameters.
4. Add attack action logging for failure traces.
5. Add metric aggregation for:
   - worst-case degradation;
   - median degradation;
   - attack success rate;
   - mechanism-specific vulnerability;
   - recovery/correction behavior;
   - administrative burden under attack.
6. Add reporting scripts under `scripts/reporting/`.
7. Add tests for attack configuration, deterministic seeding, and trace schema.

## Required Experiment 1: Clone/Decoy Attack

Target: content-selection family.

Mechanisms:

- `simple-majority-alternatives-pairwise`;
- `pairwise-amendment-tournament-majority`;
- strategic tournament variants if retained.

Adversary:

- actor type: proposer, party, or lobby-aligned proposer;
- objective: cause selection of lower-benefit or lower-support alternative;
- budget: number of clone/decoy proposals;
- information: medium/high.

Outputs:

- selected-alternative quality loss;
- low-support enactment increase;
- attack success rate;
- failure traces for selected runs.

## Required Experiment 2: Poison-Pill Amendment Attack

Target: amendment/tournament systems.

Mechanisms:

- pairwise amendment tournament;
- committee amendment and revision;
- negotiated amendment variants after they exist.

Adversary:

- actor type: party, proposer, lobby group;
- objective: block high-benefit bill or pass it with harmful/captured rider;
- budget: amendment slots.

Outputs:

- high-benefit blockage rate;
- harm/capture increase among enacted bills;
- recovery through review or substitute selection.

## Required Experiment 3: Astroturf Objection Attack

Target: objection-window systems.

Mechanisms:

- `public-objection-majority`;
- burden-shifting challenge variants where objections/challenges matter.

Adversary:

- actor type: outside campaign or lobby group;
- objective: raise admin burden or block high-benefit bills;
- budget: objection capacity and public attention.

Outputs:

- admin burden increase;
- false-negative blockage;
- objection queue saturation;
- correction/recovery rate.

## Required Experiment 4: Bad-Faith Harm-Claim Attack

Target: harm-weighted systems.

Mechanisms:

- `harm-weighted-majority`;
- compensation/affected-group variants;
- portfolio harm-review path.

Adversary:

- actor type: outside campaign, party, or affected-group proxy;
- objective: trigger false-positive review or evade true harm screen;
- budget: harm-claim filings and legal attention.

Outputs:

- false-positive review burden;
- false-negative concentrated-harm enactment;
- admin cost under claim pressure.

## Required Experiment 5: Proposal Flooding

Target: open-calendar and burden-shifting systems.

Mechanisms:

- `open-rule-calendar-majority`;
- `agenda-lottery-majority`;
- `default-pass`;
- `default-pass-challenge`;
- `default-pass-multiround-mediation-challenge`.

Adversary:

- actor type: proposer, party, lobby group;
- objective: exhaust floor/review capacity or enact low-support bills;
- budget: proposal slots and lobbying support.

Outputs:

- floor load;
- review load;
- high-benefit bill crowdout;
- low-support enactment;
- policy shift.

## Required Experiment 6: Lobbying Camouflage

Target: anti-capture access systems.

Mechanisms:

- `anti-capture-access-majority`;
- `anti-capture-majority-bundle`;
- `influence-system-majority`.

Adversary:

- actor type: lobby group;
- objective: preserve private gain while evading anti-capture screens;
- budget: money, proxy sponsors, issue framing.

Outputs:

- captured bills passing access screens;
- lobby capture increase;
- anti-lobby pass-rate effects;
- false reassurance where visible spend falls but capture persists.

## Required Experiment 7: Administrative Overload

Target: portfolio systems.

Mechanisms:

- `portfolio-hybrid-legislature`;
- `expanded-portfolio-hybrid-legislature`;
- risk-routed systems if used as comparison.

Adversary:

- actor type: mixed coalition;
- objective: exhaust layered safeguards;
- budget: proposals, objections, harm claims, lobbying camouflage, review demand.

Outputs:

- admin cost;
- queue saturation;
- risk-control degradation;
- recovery/correction after overload.

## Required Experiment 8: Mixed Adversary Case

Target: all major mechanism families.

Adversary:

- actor type: mixed coalition with proposer, lobby, outside campaign, and gatekeeper components;
- objective: enact low-support/private-gain bills while blocking high-benefit reform.

Outputs:

- family-level vulnerability ranking;
- worst-case degradation by mechanism;
- attack success rate by family;
- failure traces for 2-3 mechanisms.

## Required Experiment 9: Strategic Silence Under Burden-Shifting

Target: burden-shifting passage rules.

Mechanisms:

- `default-pass`;
- `default-pass-challenge`;
- `default-pass-multiround-mediation-challenge`.

Adversary:

- actor type: party, lobby group, committee gatekeeper;
- objective: allow low-support/private-gain bill to enact by suppressing objection or hoarding challenge tokens;
- budget: coordination capacity and challenge-token withholding.

Outputs:

- low-support default enactment;
- unused challenge-token rate;
- objection suppression success;
- recovery through review/rollback.

## Proposed Make Targets

```make
adversarial-stress
attack-budget-sweep
worst-case-degradation-report
failure-trace-report
defense-cost-sweep
```

## Full Draft Gate

Only draft the paper after:

- all eight required experiments plus strategic-silence case have outputs;
- reporting includes worst-case and median degradation;
- attack success rates are computed;
- failure traces exist for at least 2-3 mechanisms;
- `make test` passes.
