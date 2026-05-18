# Breakout Work Sequence

This is a sequencing roadmap, not a manuscript and not another umbrella paper. It orders the breakout-paper work to maximize reusable value and minimize duplication with the ACM CI framework paper.

## Recommended Order

1. `stage-01-acm-ci-framework-freeze.md`: finish and freeze the ACM CI framework paper and artifact package.
2. `stage-02-empirical-validation-roadmap.md`: build the empirical-validation/data roadmap that supports later papers.
3. `stage-03-robustness-failure-modes.md`: implement adversary experiments and then draft the robustness/failure-mode paper if evidence is strong enough.
4. `stage-04-political-science-simulation.md`: defer the political-science simulation paper until validation and fairness controls are stronger.
5. `stage-05-chamber-structure.md`: defer the chamber-structure paper until expanded chamber scenarios and representation diagnostics are ready.
6. `stage-06-software-artifact.md`: consider a software/artifact paper only after clean reproducibility and packaging audit.
7. `stage-07-normative-institutional-design.md`: do not draft a normative institutional-design paper until empirical and robustness evidence is stronger.

## Duplication Control

- The ACM CI paper owns the framework contribution.
- The empirical-validation work owns data boundaries and validation design.
- The robustness paper owns adversarial failure modes.
- The political-science paper owns institutional hypotheses only after validation and fairness controls improve.
- The chamber paper owns representation architecture only after chamber-specific diagnostics improve.
- The software paper owns packaging, reproducibility, and reuse, not scientific mechanism rankings.
- The normative paper is blocked until the project can support stronger claims.

## Existing Candidate Folders

- `papers/empirical-validation/`
- `papers/robustness-failure-modes/`
- `papers/political-science-simulation/`
- `papers/chamber-structure/`
- `papers/software-artifact/`

Use the stage files here as the execution order and the candidate folders as the paper-specific workspaces.
