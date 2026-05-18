# Draft Outline

Status: outline only. Do not draft a full software paper until the reproducibility and packaging audit passes.

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

## 1. Motivation

- Researchers need inspectable tools for comparing legislative mechanisms under shared synthetic assumptions.
- Legislative simulation papers often make it difficult to separate model assumptions, mechanism modules, campaign definitions, and generated outputs.
- The simulator aims to provide a reproducible mechanism-comparison environment with documented assumptions and regenerated paper artifacts.

## 2. Software Architecture

- Java 21 core simulator.
- Makefile-first workflow.
- Package layout:
  - `behavior`;
  - `model`;
  - `simulation`;
  - `simulation/catalog`;
  - `institution/*`;
  - `experiment`;
  - `calibration`;
  - `reporting`;
  - `util`.
- Reporting and validation scripts.
- Paper-generation scripts and LaTeX assets.

## 3. Model Overview

- Entities: legislators, bills, lobby groups, institutions, environment.
- State variables: ideology, support, benefit, lobbying, harm, party, district, status quo, review state.
- Scheduling: generated world, scenario process chain, bill sequence, metrics, status quo update.
- Adaptation: proposers, lobby groups, law registries, credits, bonds, challenges.
- Submodels: voting, agenda access, committees, lobbying, chamber structures, bargaining, public input, review, law registry.
- Empirical inputs and boundaries.

## 4. Reproducibility Workflow

- `make test`.
- `make campaign`.
- `make paper-checks`.
- `make reproduce-paper-offline`.
- `make supplement-anonymous`.
- Fixed seeds.
- Generated reports and manifest checks.
- Optional network-dependent empirical refreshes.

## 5. Example Use Case

- Add a new legislative mechanism or scenario family.
- Run it against shared generated worlds.
- Compare diagnostics against existing benchmark scenarios.
- Generate reports and figures.
- Interpret results as synthetic hypotheses, not empirical rankings.

## 6. Quality Control

- Unit/invariant tests.
- Scenario catalog tests.
- Calibration screens.
- Seed robustness.
- Figure/table consistency.
- PDF rendering and manifest checks.
- Anonymous supplement builder.

## 7. Limitations

- Synthetic model assumptions.
- Empirical checks are sanity screens.
- No license/citation metadata yet.
- Clean-clone reproduction not yet documented.
- No public release archive yet.
- No software-paper claim until packaging audit passes.

## 8. Availability

This section should remain unwritten until:

- license exists;
- citation metadata exists;
- release/archive URL exists;
- clean reproduction log exists.
