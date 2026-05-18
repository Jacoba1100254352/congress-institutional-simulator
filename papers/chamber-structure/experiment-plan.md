# Experiment Plan

## Baseline Commands

```sh
make chamber-structure
make chamber-structure-summary
```

Baseline files:

- `reports/simulation-chamber-structure.csv`
- `reports/chamber-family-champions.md`
- `reports/chamber-stress-screen.md`
- `paper/figures/chamber_productivity_compromise.tex`
- `paper/figures/chamber_family_table.tex`

## Required New Experiment 1: Representation Geometry

Purpose: test how district heterogeneity and geographic/party clustering affect chamber outcomes.

Factors:

- Uniform districts versus polarized districts.
- Party geography concentrated versus dispersed.
- Group harm concentrated versus diffuse.
- Issue domains localized versus national.

Outputs:

- District alignment.
- Public support by district or group.
- Low-support enactment.
- Risk-control and harm diagnostics.

## Required New Experiment 2: Bicameral and Apportionment Controls

Purpose: isolate bicameralism, upper-chamber composition, and malapportionment.

Controls:

- Equal-population unicameral.
- Proportional bicameral.
- Malapportioned upper chamber.
- Upper chamber with different term/selection assumptions.
- Conference committee with and without content revision.

Outputs:

- Paired differences versus equal-population unicameral.
- Chamber conflict rate.
- Policy delay and blockage reliance.
- Group/district alignment.

## Required New Experiment 3: Committee Information Gain

Purpose: test committee design as an information/routing mechanism rather than only a gate.

Factors:

- Random committee assignment.
- Expertise-based assignment.
- Party-ratio assignment.
- Committee amendment power.
- Committee reporting threshold.
- Information gain level.

Outputs:

- Enacted public benefit.
- Revision moderation.
- Floor load.
- Committee reporting rate.
- Administrative cost.

## Required New Experiment 4: Review Architecture

Purpose: separate review/correction from chamber structure.

Factors:

- No review.
- Ex ante advisory review.
- Ex post rollback.
- Law registry.
- Independent review insulation.
- Review budget constraints.

Outputs:

- Active-law quality.
- Reversal/correction rate.
- Harm reduction.
- Administrative cost.

## New Code or Data Tasks

- Add district-level public support output if not already sufficient.
- Add chamber conflict and committee reporting diagnostics.
- Add empirical comparison samples for apportionment and committee reporting.
- Add reporting scripts for chamber paired differences.

## Proposed Make Targets

```make
chamber-representation-sensitivity
committee-information-controls
review-architecture-sensitivity
chamber-paired-report
```
