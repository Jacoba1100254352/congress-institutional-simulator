# Experiment Plan

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

## Baseline Commands

Run current chamber artifacts:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make chamber-structure
make chamber-structure-summary
```

Current outputs:

- `reports/simulation-chamber-structure.csv`
- `reports/simulation-chamber-structure.md`
- `reports/chamber-family-champions.md`
- `reports/chamber-stress-screen.md`

## Required Code Tasks

1. Make status quo domain-aware for chamber/representation diagnostics.
2. Add district/population support distributions.
3. Split public support into national, district, affected-group, and chamber coalition support.
4. Add population-weighted and chamber-weighted support diagnostics.
5. Add committee capture outputs by committee assignment and power configuration.
6. Add review delay and intervention metrics for independent review bodies.
7. Add paired chamber-architecture reporting scripts.

## Required Experiment 1: Malapportionment Sweep

Purpose: test how population-seat distortion changes representation and legislative outcomes.

Sweep:

- equal-population unicameral;
- proportional lower chamber;
- territorial upper chamber;
- malapportioned upper chamber;
- increasing upper-chamber malapportionment levels;
- district magnitude variation.

Metrics:

- productivity;
- moderation;
- population-weighted support;
- chamber-weighted support;
- representation gap;
- low-public-support enactment;
- minority harm;
- malapportionment index.

## Required Experiment 2: Upper-Chamber Power Sweep

Purpose: separate upper-chamber composition from upper-chamber power.

Sweep:

- advisory review only;
- amendment-only power;
- suspensive veto;
- absolute veto;
- cloture-like upper threshold;
- territorial veto threshold;
- lower-house override thresholds.

Metrics:

- productivity;
- bicameral conflict;
- upper veto/amendment rate;
- lower-house override rate;
- delay;
- public-support failure;
- minority harm.

## Required Experiment 3: Committee Assignment and Capture Sweep

Purpose: test how committee composition and power affect productivity, capture, and support.

Sweep:

- proportional committee assignment;
- forced-balanced committee;
- random-lottery committee;
- expertise-qualified lottery committee;
- opposition-chaired scrutiny committee;
- minority-veto committee seat;
- mixed legislator-citizen committee;
- captured committee condition;
- committee amendment/revision power.

Metrics:

- committee reporting rate;
- committee capture;
- floor load;
- productivity;
- public-support failure;
- generated public benefit;
- administrative cost.

## Required Experiment 4: Eligibility and Selection Filter Sweep

Purpose: test appointment, election, eligibility, retention, and renewal rules.

Sweep:

- expertise eligibility filter;
- recusal/cooling-off filter;
- appointment and retention eligibility filter;
- elected selection baseline;
- appointed upper chamber;
- staggered renewal if implemented;
- retention filter strength.

Metrics:

- productivity;
- moderation;
- capture;
- representation gap;
- support diagnostics;
- turnover/retention diagnostics if implemented.

## Required Experiment 5: Independent Review Body Sweep

Purpose: test ex ante review and independent bodies as representation/risk/cost mechanisms.

Sweep:

- ex ante advisory review;
- mandatory legal clearance;
- fiscal review;
- electoral review;
- audit/ethics review;
- independent insulation bundle;
- constitutional court architecture;
- review budget constraints.

Metrics:

- risk control;
- minority harm;
- capture;
- review delay;
- administrative cost;
- correction/reversal if available.

## Required Experiment 6: Bicameral Conflict and Override Scenarios

Purpose: study chamber disagreement and resolution pathways.

Sweep:

- house-origin-only routing;
- senate/upper-origin-only routing;
- proposer-chamber origin routing;
- leadership-routed origin;
- limited navette;
- conference compromise;
- mediation committee;
- principles resolution before second-chamber drafting;
- lower-house override after disagreement;
- joint sitting fallback.

Metrics:

- bicameral conflict rate;
- amendment/revision rate;
- conference/navette rounds;
- delay;
- productivity;
- representation gap;
- low-support enactment.

## Required Experiment 7: Population-Weighted vs Chamber-Weighted Support

Purpose: test whether chamber-weighted support masks population-weighted public-support failure.

Conditions:

- equal population/seat distribution;
- mild malapportionment;
- severe malapportionment;
- district support aligned with population;
- district support polarized by geography;
- affected-group concentrated harm.

Metrics:

- population-weighted support;
- chamber-weighted support;
- lower-chamber support;
- upper-chamber support;
- affected-group support;
- support gap;
- minority harm.

## Proposed Make Targets

```make
chamber-representation-sensitivity
chamber-malapportionment-sweep
chamber-upper-power-sweep
committee-capture-sweep
selection-retention-sweep
review-body-sweep
chamber-conflict-override-sweep
chamber-support-weighting-report
```

## Full Draft Gate

Only draft the paper after:

- all seven required experiments have run;
- representation diagnostics are domain-aware;
- support diagnostics distinguish national, district, affected-group, and chamber coalition support;
- validation plan has source inventories and at least initial apportionment/committee/chamber-vote targets;
- `make test` passes.
