# Stage 4: Political Science Simulation Paper

## Go/No-Go Decision

No-go for drafting now. Go only after Stage 2 produces a stronger validation/data roadmap and Stage 3 or related work strengthens fairness and sensitivity controls.

Primary workspace: `papers/political-science-simulation/`.

## Repo Tasks

- Add cost-budgeted fairness controls before comparing content-selection systems to conventional or simple-majority systems.
- Add a two-dimensional policy-space sensitivity model or narrow claims about amendment, alternatives, compromise, and package bargaining.
- Add paired-difference reporting against `CUR` and `SM`.
- Separate seed uncertainty from scenario variation.
- Keep PAIR/AMT merged as `SEL` in main narrative unless a new test demonstrates meaningful divergence.
- Use empirical roadmap outputs from Stage 2 to define what is and is not validated.

## Experiments to Run

Baseline:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make campaign
make seed-robustness
make findings-validation
make calibration-check
```

New required targets:

```make
cost-budget-fairness
two-dimensional-sensitivity
generator-correlation-worlds
paired-difference-report
political-science-campaign
```

Required cases:

- Moderation-friendly baseline.
- Reform-friendly high-distance proposals.
- Public-support-lags-benefit world.
- Lobbying-information world.
- Majority-support-with-minority-harm world.
- Cost-constrained content selection and conventional revision.

## Figures and Tables to Generate

Required:

- Institutional hypotheses table.
- Mechanism-family table with `SEL` as combined content selection.
- Generator-world sensitivity plot.
- Cost-budget fairness table.
- Paired-difference plot versus `CUR` and `SM`.
- Two-dimensional policy-space stress plot.
- Empirical-boundary table imported from Stage 2.

Appendix:

- Full scenario averages from `reports/simulation-campaign-v21-paper.csv`.
- Seed robustness from `reports/seed-robustness-summary.csv`.
- Full scenario manifest.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| The current simulator can support synthetic political-science hypotheses. | Main campaign and source modules. | Framework claim belongs to ACM paper. | Usable as method. |
| Content selection changes output diagnostics under the baseline generator. | Current campaign and findings reports. | Moderation-friendly generator may bake in part of the result. | Conditional. |
| Content selection is superior to conventional systems. | Not sufficiently supported. | Requires cost-budget fairness and validation boundaries. | Exclude for now. |
| Burden-shifting systems show high-throughput stress behavior. | Current `DP`/`DPM` results. | Stress cases, not reform recommendation. | Usable with caveat. |
| Political-science claims require stronger empirical framing. | Stage 2 roadmap and current gap reports. | Validation not yet implemented. | Blocking. |

## Paper Outline

Do not draft until required experiments complete:

1. Introduction: institutional mechanism hypotheses, not framework novelty.
2. Theory: thresholds, agenda access, proposal transformation, review, lobbying.
3. Simulator summary and empirical boundary.
4. Experiment design.
5. Fairness and generator-sensitivity controls.
6. Results.
7. Discussion: mechanism behavior under synthetic assumptions.
8. Limitations.
9. Conclusion.
