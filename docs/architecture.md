# Architecture

This document summarizes the software architecture for readers who want to run,
audit, or extend the simulator. The scientific model details remain in
`docs/odd-model.md` and `docs/odd-d-appendix.md`.

## Runtime Flow

The main command path is:

1. `congresssim.Main` parses command-line options.
2. `WorldSpec` defines the generated legislature and bill stream.
3. `ScenarioCatalog` resolves scenario keys into `Scenario` objects.
4. Each `Scenario` builds a `LegislativeProcess` for a generated
   `SimulationWorld`.
5. `Simulator` runs bills through each process across fixed-seed repeated runs.
6. `MetricsAccumulator` produces a `ScenarioReport`.
7. `CampaignRunner` writes campaign CSV, Markdown, and manifest outputs under
   `reports/`.
8. Python reporting scripts summarize campaign outputs and generate paper
   tables under `paper/figures/`.

## Java Packages

| Package | Role |
|---|---|
| `congresssim` | CLI entrypoint and top-level option dispatch. |
| `congresssim.model` | Core domain records such as bills, legislators, worlds, votes, policy state, and lobby groups. |
| `congresssim.behavior` | Voting strategies and vote influence composition. |
| `congresssim.institution.core` | Common process interface and `BillOutcome` structure. |
| `congresssim.institution.agenda` | Proposal access, floor scheduling, challenge tokens, and agenda routing. |
| `congresssim.institution.voting` | Affirmative thresholds and default-pass voting rules. |
| `congresssim.institution.chamber` | Unicameral, bicameral, presidential, conference, court, and chamber-routing processes. |
| `congresssim.institution.committee` | Committee gatekeeping, information, power, hearing, and amendment processes. |
| `congresssim.institution.bargaining` | Amendment, alternative, package, omnibus, mediation, and coalition processes. |
| `congresssim.institution.distribution` | Harm, compensation, consent, and affected-group scoring processes. |
| `congresssim.institution.lobbying` | Lobbying pressure, capture, audit, transparency, and influence-system processes. |
| `congresssim.institution.publicinput` | Citizen panels, initiatives, objection windows, petitions, and public-will processes. |
| `congresssim.institution.accountability` | Law registry, proposal bonds, eligibility, credits, sunset, and attention-budget processes. |
| `congresssim.institution.review` | Ex ante review, judicial review, and independent institution bundles. |
| `congresssim.institution.strategy` | Strategic proposer behavior, norm erosion, long-horizon learning, and deterioration. |
| `congresssim.simulation` | Scenario interface, simulator loop, world generation, metrics, reports, and chamber specs. |
| `congresssim.simulation.catalog` | Scenario families and scenario-key catalog. |
| `congresssim.experiment` | Campaign definitions and report serialization. |
| `congresssim.calibration` | Conventional-baseline calibration screens. |
| `congresssim.reporting` | Report provenance helpers. |

## Extension Points

Use these stable seams for extension work:

- Add a mechanism by implementing or composing a `LegislativeProcess`.
- Add a scenario by creating a `ScenarioEntry` in a scenario-family class and
  ensuring `ScenarioCatalog.entries()` includes that family.
- Add a campaign by selecting scenario keys and cases in `CampaignRunner`, then
  wiring a command name in `Main` and a Makefile target.
- Add a metric by extending `ScenarioReport`, `MetricsAccumulator`, and
  `MetricDefinition`, then updating downstream report scripts and table checks.
- Add empirical validation support under `data/validation/` and
  `scripts/validation/`, keeping raw inputs separate from adapter fixtures.

## Evidence Boundaries

The simulator is designed for comparative synthetic stress tests. Generated
metrics should be described as model outputs unless an empirical report
explicitly supports a narrower boundary such as flow sanity check, calibration
proxy, or held-out benchmark. The current registry-backed empirical boundary
reports are the authority for those labels.
