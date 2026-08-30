# Adding A Mechanism

Use this guide when adding a new institutional mechanism to the simulator.

## 1. Choose The Process Boundary

Most mechanisms should be implemented as one of:

- a new `LegislativeProcess`;
- a wrapper around an existing `LegislativeProcess`;
- a small process used by an existing scenario builder;
- a voting strategy or vote influence in `congresssim.behavior`.

Keep the mechanism status-quo-relative. It should operate on generated bills,
legislators, public signals, lobbying signals, chamber decisions, or
post-enactment law state already represented in the model.

## 2. Return A Complete Outcome

Every full process should return a `BillOutcome`. Preserve:

- whether the bill was enacted;
- status quo before and after;
- gate and chamber results;
- agenda disposition;
- presidential or court action when relevant;
- `OutcomeSignals` for diagnostic metrics;
- a concise final reason.

Prefer adding signals over ad hoc report-side inference. If a metric requires a
new event, record it in the process outcome.

## 3. Compose Into A Scenario

Add the mechanism to a scenario builder under `congresssim.simulation.catalog`.
The local pattern is to keep related scenarios inside a family class such as
`BroadSystemScenarioFamily`, `DefaultPassSafeguardScenarioFamily`,
`PolicyTournamentScenarioFamily`, `DefaultPassStressScenarioFamily`, or
`ChamberCommitteeScenarioFamily`.

Add a stable scenario key through `new ScenarioEntry("scenario-key", scenario)`.
Use lowercase hyphenated keys because campaign scripts and reports rely on
stable keys.

## 4. Update Metrics Deliberately

If the mechanism changes existing outcomes, prefer existing metrics. Add a new
metric only when existing outputs cannot express the mechanism's behavior.

When adding a metric, update:

- `ScenarioReport`;
- `MetricsAccumulator`;
- `MetricDefinition`;
- any CSV writer or report script that expects the column;
- paper or appendix tables only if the metric is paper-facing.

Label new metrics as higher-is-better, lower-is-better, or diagnostic. Avoid
scoring a diagnostic metric as normatively good or bad unless the model
justifies that direction.

## 5. Add Tests

Add focused tests under `src/test/java/congresssim`. Test the smallest behavior
that could regress:

- process output for a controlled bill/world;
- scenario catalog lookup;
- campaign row serialization if a new campaign path is added;
- metric direction or bounds if a new metric is added.

Run:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
```

## 6. Preserve Claim Boundaries

New mechanisms should be described as synthetic design hypotheses unless a
validation report supports a narrower empirical boundary. Do not turn a
mechanism addition into an institutional recommendation without new validation
evidence.
