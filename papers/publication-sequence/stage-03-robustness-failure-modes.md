# Stage 3: Robustness and Failure-Mode Work

## Go/No-Go Decision

Go for expansion and replication beyond the fixed-specification A9 seed panel. Conditional go for a full draft only after the remaining mechanism, A1-A8 seed, correction, and validation gates are satisfied.

This is the cleanest independent technical breakout because it can focus on failure modes rather than validating real institutions or ranking reforms.

Primary workspace: `papers/robustness-failure-modes/`.

Current executable state: A1 clone/decoy through A9 mixed portfolios have bounded budget/information pilots and per-bill traces. A7 includes queue recovery, A8 includes same-case signal correction, and A9 compares three exact-budget portfolios against full-budget and allocated-component single controls. A9 additionally has 30-base-seed fixed-specification replication covering 162,000 evaluated rows. A1-A8 seed replication, broader mechanisms, alternative A9 specifications, temporal or substantive correction, and external attack validation remain missing.

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
make adversarial-replication-a9
```

New experiment targets to implement:

```make
adversarial-stress
adversarial-replication-a9
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
- Public-support distortion against signal-reliant and constituent-verification paths.
- Mixed fixed-budget portfolios across two to four A1-A8 attack actions.

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
| Current repo has ablation, manipulation-stress, bounded A1-A9 explicit adversary pilots, and fixed-specification A9 seed replication. | `reports/simulation-ablation-analysis.csv`, `reports/simulation-manipulation-stress.csv`, A1-A9 adversarial summaries/traces, and `reports/adversarial-replication-a9-summary.csv`. | Current attacks cover bounded mechanism paths and are not externally validated; A1-A8 remain single-seed. | Usable as bounded synthetic evidence only. |
| Failure modes differ by mechanism family. | Plausible from current stress categories and mechanism designs. | Needs budgeted attack sweeps and worst-case results. | Conditional. |
| Content-selection mechanisms can be attacked by clones/decoys. | Existing clone/decoy stress category. | Needs mechanism-specific attack success criteria. | Conditional. |
| Harm and objection systems can be overloaded by bad-faith use. | Current loose-harm and astroturf/noise probes. | Need false-positive and admin-burden sweeps. | Conditional. |
| A robustness paper can stand apart from the ACM framework paper. | Failure modes are a distinct technical object; A1-A9 provide bounded explicit examples and A9 now demonstrates a scalable seed-replication path. | Requires broader mechanisms, A1-A8 seed sweeps, alternative A9 specifications, correction evidence, and validation before drafting. | Conditional. |

## Paper Outline

Draft only after the remaining go/no-go gates:

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
