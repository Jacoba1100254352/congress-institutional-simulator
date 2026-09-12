# House Agenda-Control Calibration: Locked Pre-Fit Specification

Status: locked after official-source panel construction and descriptive source
audit, before route-state implementation, parameter probing, or simulator fit.

Lock date: 2026-08-31.

## Purpose and Status

This specification fixes a narrow aggregate calibration and temporal transport
study for the stylized current-Congress workflow. The study asks whether a
separately identified simulator scenario can reproduce four observed House
agenda-control surfaces:

1. committee advancement among introduced H.R. measures;
2. substantive House floor consideration among introduced H.R. measures;
3. the mixture of adopted-special-rule, suspension, mixed, and other observed
   routes among floor-considered H.R. measures; and
4. the restrictive share among H.R. measures considered under an adopted
   special rule.

This is not a blinded or prospective preregistration. The complete source
panel and its 116th-, 117th-, and 118th-Congress descriptive results were
inspected before this document was locked. The 118th Congress is a frozen
no-refit temporal test, but not an outcome-blind test. No route-state code,
candidate-grid probe, parameter fit, or simulator-to-source route comparison
has been implemented or run before this lock.

The study calibrates aggregate synthetic route frequencies. It does not
recover leadership demand, estimate the causal effect of a floor route,
identify why a real bill received a route, validate bill-level predictions,
or validate public benefit, welfare, representation, capture, or institutional
rankings.

## Frozen Source Population

The source population and classifications are fixed by
`house-agenda-control-panel-specification.md` and these committed artifacts:

- `data/validation/raw/house_agenda_control.csv`;
- `data/validation/raw/house_special_rule_grants.csv`; and
- `reports/house-agenda-control-metrics.csv`.

The unit used for lifecycle and route metrics is one H.R. measure. The
development cohort pools all 18,771 H.R. measures introduced in the 116th and
117th Congresses. The primary temporal test contains all 10,564 H.R. measures
introduced in the 118th Congress.

The study must fail before simulation if the source inputs do not reproduce
all of these locked values:

| Metric | 116th-117th development | 118th test |
| --- | ---: | ---: |
| H.R. measures | 18,771 | 10,564 |
| Committee advanced | 1,912 / 18,771 = 0.101859250972 | 1,202 / 10,564 = 0.113782658084 |
| Floor considered | 1,500 / 18,771 = 0.079910500240 | 676 / 10,564 = 0.063990912533 |
| Adopted special rule only | 155 / 1,500 = 0.103333333333 | 127 / 676 = 0.187869822485 |
| Suspension only | 1,248 / 1,500 = 0.832000000000 | 544 / 676 = 0.804733727811 |
| Mixed special rule and suspension | 38 / 1,500 = 0.025333333333 | 4 / 676 = 0.005917159763 |
| Other detected route | 59 / 1,500 = 0.039333333333 | 1 / 676 = 0.001479289941 |
| Restrictive adopted-rule H.R. measures | 198 / 198 = 1.000000000000 | 134 / 135 = 0.992592592593 |

The source route categories are mutually exclusive as specified in the source
panel. The restrictive numerator is a unique-H.R.-measure quantity. It is not
the number of rule grants or resolutions.

## Frozen Simulator Baseline

The existing `current-congress-workflow` scenario and its lifecycle
calibration remain a separate, previously frozen baseline. This study may not
overwrite or silently reinterpret its selected calendar threshold, source
cohort, tolerances, or committed result. Before route fitting, the baseline
must still report from `reports/legislative-lifecycle-calibration.csv`:

- calendar-priority threshold 0.680;
- 50 seeds, 24 runs per seed, and 72,000 simulated bills;
- committee advancement 0.106278;
- floor consideration 0.061097; and
- enactment 0.027417.

The new selected parameters belong to a separately named House
agenda-calibration scenario. A passing result does not retroactively convert
the earlier lifecycle workflow into a route-calibrated model.

## Frozen Structural Change

The simulator currently assigns `closedRuleRate` and `openRuleRate` before
calendar denial. Those legacy diagnostics therefore describe latent rule
posture on committee-advanced bills, not observed routes among floor-considered
bills. They are not calibration targets in this study.

The implementation must add four mutually exclusive route indicators only
after a bill clears the existing calendar-capacity and status-quo-fallback
gates:

- `specialRuleOnlyRouteRate`;
- `suspensionOnlyRouteRate`;
- `mixedSpecialRuleAndSuspensionRouteRate`; and
- `otherFloorRouteRate`.

Each indicator is one for its selected route and zero for the other three. A
bill denied before the floor emits zero for all four. The sum of the four
indicators must equal one for every modeled floor-considered bill and zero for
every other submitted bill. Scenario-level raw rates remain divided by all
submitted bills; the study probe must convert them to route shares by dividing
each route rate by their sum.

The route assignment is deterministic conditional on the generated bill and
current policy context. It uses existing model quantities without adding a
Congress label, empirical bill identifier, source outcome, or post-floor
variable.

Define ideological distance as:

```text
distance = abs(bill ideology - current policy position) / 2
```

using the existing bounded bill and policy positions. Define the two route
scores as:

```text
special score = clamp(
    0.42 * closure score
  + 0.23 * scheduling risk
  + 0.20 * bill salience
  + 0.15 * distance
)

suspension score = clamp(
    0.42 * mandate score
  + 0.24 * (1 - scheduling risk)
  + 0.18 * (1 - capture risk)
  + 0.10 * (1 - distance)
  + 0.06 * (1 - public-benefit uncertainty)
)
```

`mandate score`, `scheduling risk`, `capture risk`, and `closure score` retain
their existing formulas. `clamp` bounds a value to `[0, 1]`.

For a floor-considered bill:

1. if both scores meet their candidate thresholds, assign mixed;
2. otherwise, if only the special score meets its threshold, assign adopted
   special rule only;
3. otherwise, if only the suspension score meets its threshold, assign
   suspension only; and
4. otherwise assign other detected route.

This fixed overlap rule is the only modeled mixed-route mechanism. No random
route draw or target-share quota is permitted.

For special-rule-only and mixed bills, define a restrictive rule when the
existing closure score is at least `max(0.34, openRuleNorm)`. The probe must
report `restrictiveSpecialRuleRouteRate` and calculate the restrictive share
using special-rule-only plus mixed bills as the denominator. This is a modeled
structured-or-closed analogue. It does not distinguish structured from closed
rules and may not be described as a literal House Rules Committee category.

The route indicators are diagnostic in this study. The route assignment may
not alter the existing calendar decision, chamber thresholds, amendment
process, status-quo update, or enactment path. This preserves the previously
frozen lifecycle baseline while exposing the missing route state. Any later
study that gives routes distinct behavioral effects requires a new lock and
new outcome validation.

## Frozen Simulator Population

Every candidate uses the existing deterministic simulator with this fixed
world specification:

- 101 legislators;
- 60 submitted bills per run;
- two parties;
- polarization 0.76;
- party loyalty 0.74;
- lobbying susceptibility 0.48;
- constituency sensitivity 0.62; and
- compromise culture 0.46.

All institutional parameters outside the three candidate values remain those
of `stylizedCurrentCongressWorkflow` at the lock date. Generated bills are the
unit corresponding to introduced H.R. measures. This is an aggregate analogy,
not a claim that the generator reproduces the real H.R. covariate distribution.

## Frozen Candidate Grid

Exactly three parameters may vary:

1. minimum calendar priority in `{0.62, 0.64, 0.66, 0.68, 0.70}`;
2. special-rule threshold from 0.350 through 0.750 in increments of 0.025; and
3. suspension threshold from 0.350 through 0.750 in increments of 0.025.

The complete Cartesian product contains 1,445 candidates. No candidate may be
added, removed, or refined after probe results are observed. A boundary
selection must be retained and reported as a stability warning rather than
used to justify expanding the grid in this study.

The development probe uses 20 seeds defined by:

```text
1,161,170,001 + 104,729 * index, for index 0 through 19
```

with 12 runs per seed. Each candidate therefore uses 14,400 generated bills.
All candidates use the same worlds and seeds.

## Frozen Selection Rule

The committee-advancement rate is reported as an upstream check and does not
enter parameter selection because none of the three candidate parameters acts
before the committee layer. The restrictive-rule share also does not enter
selection because its rule is structurally fixed rather than tuned.

For each candidate, calculate the development floor-consideration error and
the four conditional route-share errors. The selection loss is:

```text
(floor error / 0.015)^2
+ (special-only share error / 0.040)^2
+ (suspension-only share error / 0.050)^2
+ (mixed share error / 0.020)^2
+ (other share error / 0.030)^2
```

The selected candidate minimizes this loss using full-precision values. Ties
are broken by, in order:

1. lower maximum absolute standardized error across the five fitted metrics;
2. lower minimum-calendar-priority value;
3. lower special-rule threshold; and
4. lower suspension threshold.

The implementation must also recompute the selected triple after omitting each
development seed in turn. These 20 leave-one-seed-out selections are stability
diagnostics only and may not change the selected full-panel candidate.

All 1,445 candidate rows must be retained, including poor fits. The selected
candidate must be retained even if its fit is poor or it lies on a grid
boundary.

## Frozen Temporal Test

After selection, the unchanged selected candidate is run on an independent
Monte Carlo panel of 30 seeds defined by:

```text
1,180,000,001 + 130,363 * index, for index 0 through 29
```

with 20 runs per seed, for 36,000 generated bills. The 118th-Congress source
targets may not alter the route formulas, grid, selected parameters, world
specification, simulator seeds, run count, or loss.

The primary temporal gate passes only if all four conditions hold using
full-precision values:

1. absolute committee-advancement error is at most 0.020;
2. absolute floor-consideration error is at most 0.020;
3. total-variation distance between the four modeled and 118th-Congress route
   shares is at most 0.100, where total variation is one half of the sum of
   absolute category-share differences; and
4. absolute restrictive special-rule share error is at most 0.020.

The route tolerance was fixed after the empirical development-to-test route
shift was known. This limits the force of a passing result and must be stated
in the report. Development fit, route-category errors, advancement-to-floor
ratio, enactment, legacy closed/open diagnostics, and Monte Carlo variation
must be reported but do not create additional post hoc gates.

All test results must be retained whether the gate passes or fails. A failed
condition may not be tuned away within this locked study.

## Explicitly Noncomparable Source Metrics

The following source-panel outputs may be described alongside the study but
may not enter fitting or gate decisions:

- calendar-placement coverage, because simulator calendar admission is a
  latent gate rather than an official House, Union, or Private Calendar action;
- median and 90th-percentile stage durations, because the simulator has no
  calendar-day time scale;
- amendment offer and disposition action counts, because the current route
  layer does not emit action records; and
- House passage or enactment rates, because the source panel is H.R.-specific
  while the simulator's downstream path includes a stylized Senate,
  conference, President, and court.

## Required Outputs and Integrity

The implementation must write, at minimum:

- a machine-readable row for every grid candidate;
- a machine-readable development and test metric table;
- a human-readable report stating the selected parameters and every gate;
- metadata with SHA-256 hashes for this specification, both source CSVs, the
  source metric table, the probe implementation, and the simulator JAR;
- focused Java and Python tests for route exclusivity, denial behavior,
  conditional denominators, selection, tie-breaking, and temporal gates; and
- a hard checker that pins the source targets, candidate count, seeds, selected
  row, report claims, and failure retention.

The Makefile must provide an offline build and checker. Repeated builds from
unchanged source and code must be byte-identical. The existing lifecycle
calibration and temporal-replication checks must still pass after the route
state is added.

After fitting, any correction to this specification requires a visibly
versioned amendment that preserves the original lock, identifies the reason,
and reports the original result. Source-integrity or implementation bugs may
be corrected, but an affected original result may not be silently replaced.

## Claim Boundary

A passing result would show only that one fixed synthetic workflow reproduces
selected aggregate development targets and remains within four broad,
post-source-audit temporal tolerances in one later Congress. A failure would
show that the fixed route construction does not transport under those rules.
Neither result validates bill-level agenda decisions, causal gatekeeping,
leadership motives, amendment opportunities, calendar timing, downstream
outcomes, welfare, representation, capture, or institutional-design
recommendations.
