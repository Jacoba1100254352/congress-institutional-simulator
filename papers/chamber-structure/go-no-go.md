# Go/No-Go Decision

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

## Decision

No-go for a full manuscript draft.

Go for a research-plan stage focused on representation-model upgrades, validation-data planning, and targeted chamber-architecture experiments.

## Readiness Level

| Level | Meaning | Current status |
|---|---|---|
| 0 | Idea only | Complete. |
| 1 | Implemented pilot scenarios exist | Complete. Current chamber reports provide pilot sensitivity screens. |
| 2 | Stand-alone model, validation, and experiment plans exist | Complete after this folder. |
| 3 | Expanded diagnostics and sweeps implemented | Not complete. |
| 4 | Manuscript-ready evidence with uncertainty and validation boundaries | Not complete. |

## Proceed Now

- Build domain-aware status quo and representation diagnostics.
- Add population-weighted, district-level, affected-group, and chamber-coalition support outputs.
- Run malapportionment, upper-chamber power, committee-capture, selection/retention, review-body, bicameral-conflict, and support-weighting sweeps.
- Build the chamber validation inventory for apportionment, district population, chamber votes, committee assignment, bicameral disagreement, and review bodies.
- Keep current chamber reports labeled as sensitivity screens.

## Defer

- Full manuscript draft.
- Claims that chamber designs improve real-world representation.
- Institutional recommendations.
- Use of `reports/chamber-family-champions.md` or `reports/chamber-stress-screen.md` as evidence of best chamber architectures.
- Any claim about district, affected-group, or population representation until those diagnostics are implemented and reported separately.

## Full Draft Conditions

Draft only after all of the following are true:

- all seven required chamber experiments in `experiment-plan.md` have run;
- outputs distinguish national public support, district support, affected-group support, lower/upper chamber coalition support, population-weighted support, and chamber-weighted support;
- chamber metrics include domain-aware status quo movement, representation gaps, conflict/delay, committee capture, and review-body delay/intervention;
- validation inventory exists for apportionment, district population, chamber vote patterns, committee assignment/referral/markup, bicameral disagreement, and review-body data;
- results report same-world paired comparisons, seed uncertainty, and scenario variation separately;
- `make test` and the relevant chamber-report targets pass;
- every claim in `claims-ledger.md` is either supported or removed from the draft.

## Immediate Repo Tasks

```sh
env JAVA_HOME="$(/usr/libexec/java_home -v 21)" PATH="$(/usr/libexec/java_home -v 21)/bin:$PATH" make test
env JAVA_HOME="$(/usr/libexec/java_home -v 21)" PATH="$(/usr/libexec/java_home -v 21)/bin:$PATH" make chamber-structure
env JAVA_HOME="$(/usr/libexec/java_home -v 21)" PATH="$(/usr/libexec/java_home -v 21)/bin:$PATH" make chamber-structure-summary
```

Future targets to add are listed in `experiment-plan.md`.
