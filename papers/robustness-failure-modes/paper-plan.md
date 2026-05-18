# Paper Plan: Robustness and Failure Modes

## Working Title

Failure Modes in Synthetic Legislative Mechanism Design: Bounded Attacks, Ablations, and Adversarial Stress Tests

## Target Venue Category

Computational social science, mechanism design, adversarial social systems, governance technology, or social simulation.

## One-Sentence Contribution

The paper would identify which legislative mechanism components fail under clone proposals, noisy public input, loose harm claims, astroturf objections, proposal flooding, and lobbying camouflage.

## Why This Is Not Redundant With the ACM CI Paper

The ACM paper uses stress probes mainly to bound the framework's demonstration results. This breakout would make failure modes the central object: adversary objectives, attack budgets, worst-case degradation, and mechanism-specific vulnerabilities.

## Current Readiness Decision

Ready for an extended outline plus experiment plan. Not ready for a full manuscript draft.

Existing stress artifacts are useful, but they do not yet include adaptive adversaries, systematic attack budgets, or worst-case reporting.

## Existing Artifacts and Results It Can Use

- `reports/simulation-ablation-analysis.csv`: 405 rows, 212 columns.
- `reports/ablation-analysis-summary.md` and `.csv`: ablation summaries.
- `reports/simulation-manipulation-stress.csv`: 91 rows, 212 columns.
- `reports/manipulation-stress-summary.md` and `.csv`: stress summaries.
- `reports/scenario-selection-manifest.md`: adversarial bill-stream cases and rationales.
- `reports/paper-findings-validation.md`: current warnings about PAIR/AMT redundancy, portfolio risks, and burden-shift stress cases.
- Appendix robustness tables in `paper/technical-appendix/odd-d-appendix.pdf`.
- Source packages under `congresssim/institution/strategy`, `publicinput`, `lobbying`, `agenda`, `bargaining`, and `review`.

Current stress categories include clone/decoy pressure, noisy panels, loose harm claims, astroturf/noise, and proposal flooding. These are diagnostic probes, not full adversarial optimization.

## Missing Experiments or Validation Needed Before Submission

- Explicit adversary model with objectives, information, action set, and budget.
- Worst-case degradation reporting rather than mean-only stress summaries.
- Attack-intensity sweeps for each mechanism family.
- Repeated-round adaptation by proposers, lobby groups, parties, or organized objectors.
- Mechanism-specific attack libraries: clone/decoy attacks for alternatives, poison-pill amendments for tournaments, bad-faith harm claims, astroturf objections, lobbying camouflage, and queue flooding.
- Controls showing whether defensive modules create new administrative overload or false-negative blockage.

## Go/No-Go Recommendation

No-go for a full failure-mode paper now. Go for an adversarial-protocol implementation and expanded stress campaign.

## Next Concrete Commands or Repo Tasks

Current reproducible baseline:

```sh
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
make paper-checks
```

Needed new targets:

```make
adversarial-stress
attack-budget-sweep
worst-case-degradation-report
```
