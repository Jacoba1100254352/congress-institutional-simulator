# Stage 3: Robustness and Failure-Mode Work

## Go/No-Go Decision

Go for adversary experiments and an expanded paper plan. Conditional go for a full draft only after budgeted adversarial results exist.

This is the cleanest independent technical breakout because it can focus on failure modes rather than validating real institutions or ranking reforms.

Primary workspace: `papers/robustness-failure-modes/`.

## Repo Tasks

- Formalize adversary profiles with objective, information, budget, action set, and success criterion.
- Split ablation and manipulation outputs into separate, consistent-sign reports.
- Add worst-case reporting in addition to mean degradation.
- Add attack-budget sweeps and mechanism-specific attacks.
- Keep PAIR/AMT as one content-selection family in main reporting unless a stress case makes them diverge.
- Make every stress result synthetic and bounded; do not imply observed real-world attack rates.

## Experiments to Run

Current baseline:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
```

New experiment targets to implement:

```make
adversarial-stress
attack-budget-sweep
worst-case-degradation-report
defense-cost-sweep
```

Attack families:

- Clone/decoy attacks against content selection.
- Poison-pill and sequencing attacks against amendment/tournament systems.
- Bad-faith harm claims against harm-protection rules.
- Astroturf/noise against objection and citizen-input paths.
- Proposal flooding against agenda systems.
- Lobbying camouflage against anti-capture screens.
- Routing overload against portfolio systems.

## Figures and Tables to Generate

Required:

- Adversary model table.
- Attack library table.
- Attack-budget degradation curves.
- Mechanism failure-mode matrix.
- Worst-case degradation table.
- Defense cost-benefit plot.
- Ablation waterfall or component-removal table.

Appendix:

- Full ablation outputs from `reports/simulation-ablation-analysis.csv`.
- Full manipulation-stress outputs from `reports/simulation-manipulation-stress.csv`.
- Seed robustness for selected attack cases.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| Current repo has ablation and manipulation-stress pilots. | `reports/simulation-ablation-analysis.csv`, `reports/simulation-manipulation-stress.csv`. | Current stressors are bounded and not adaptive. | Usable as pilot evidence. |
| Failure modes differ by mechanism family. | Plausible from current stress categories and mechanism designs. | Needs budgeted attack sweeps and worst-case results. | Conditional. |
| Content-selection mechanisms can be attacked by clones/decoys. | Existing clone/decoy stress category. | Needs mechanism-specific attack success criteria. | Conditional. |
| Harm and objection systems can be overloaded by bad-faith use. | Current loose-harm and astroturf/noise probes. | Need false-positive and admin-burden sweeps. | Conditional. |
| A robustness paper can stand apart from the ACM framework paper. | Failure modes are a distinct technical object. | Requires new experiments. | Usable after implementation. |

## Paper Outline

Draft only after the new adversary experiments:

1. Introduction: average performance is not robustness.
2. Mechanism families and failure-mode theory.
3. Simulator and baseline stress probes.
4. Adversary model.
5. Attack-budget and worst-case experiment design.
6. Results by attack family.
7. Defensive modules and administrative cost.
8. Discussion: robust design hypotheses.
9. Limitations: synthetic bounded adversaries.
10. Conclusion.
