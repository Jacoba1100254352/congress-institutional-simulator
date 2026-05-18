# Paper Plan: Political Science Simulation

## Working Title

Mechanism Bundles, Agenda Control, and Legislative Output in a Synthetic Institutional Simulator

## Target Venue Category

Computational social science, political methodology, public choice, political simulation, or social simulation.

## One-Sentence Contribution

The paper would test how agenda access, proposal transformation, veto points, lobbying safeguards, and threshold rules shift productivity, revision moderation, public-support diagnostics, risk, and procedural cost in a shared synthetic legislative environment.

## Why This Is Not Redundant With the ACM CI Paper

The ACM paper contributes the reusable framework and frames legislatures as collective-intelligence architectures. This breakout would instead evaluate political-science hypotheses about institutional mechanisms, benchmark fairness, generator assumptions, and legislative-output tradeoffs. It should not repeat the ACM architecture argument except as methods background.

## Current Readiness Decision

Ready for an extended outline plus experiment plan. Not ready for a full manuscript draft.

The existing evidence is broad enough to justify a paper plan, but not strong enough for submission as a political-science simulation paper. The current results are synthetic design hypotheses, not empirical institutional rankings.

## Existing Artifacts and Results It Can Use

- `reports/simulation-campaign-v21-paper.csv`: 1628 rows, 212 columns from the canonical main campaign.
- `reports/simulation-campaign-v21-paper.md`: run configuration, case list, scenario families, and mechanism labels.
- `reports/scenario-selection-manifest.md`: broad, adversarial, generator-sensitivity, party-system, contention, and fairness-control case rationales.
- `reports/paper-findings-validation.md`: focus-system summaries and directional/compromise/risk/yield checks.
- `reports/seed-robustness-summary.csv` and `.md`: deterministic seed sweep summaries.
- `reports/family-champions.md` and `reports/representative-vs-family-champions.csv`: family-level champion checks.
- `reports/calibration-baseline.md` and `.csv`: flow sanity screens for the conventional benchmark.
- `paper/technical-appendix/odd-d-appendix.pdf`: exact generator, vote-kernel, and scenario documentation.
- Source packages under `src/main/java/congresssim/institution/agenda`, `bargaining`, `committee`, `lobbying`, `publicinput`, `review`, `strategy`, and `voting`.

Known descriptive findings from current reports:

- Burden-shifting mechanisms can produce high productivity but worse low-support and risk diagnostics.
- Content-selection mechanisms such as PAIR/AMT are nearly indistinguishable in the current generator and should be treated as one family in the main narrative.
- Portfolio variants reduce some capture and risk diagnostics but add process complexity and do not dominate simpler selection mechanisms.
- Several patterns depend on the moderation-friendly public-benefit generator.

## Missing Experiments or Validation Needed Before Submission

- A two-dimensional policy-space sensitivity model with explicit issue dimensions and multidimensional ideal points.
- Cost-normalized fairness controls that give conventional, simple-majority, PAIR/AMT, and portfolio systems comparable amendment, information, review, and administrative budgets.
- Stronger calibration or validation against held-out observable legislative-flow metrics.
- Separate stochastic uncertainty from scenario variation; report seed variance, scenario distribution, and paired within-world differences.
- Explicit alternative generator worlds for public-benefit/support correlation, lobbying as information, minority-rights harm, and reform-friendly high-distance proposals.
- Statistical summaries that do not rely on mean plus case half-range as the main uncertainty display.
- Institutional theory that distinguishes proposal filtering from proposal transformation.

## Go/No-Go Recommendation

No-go for a full paper submission now. Go for a focused experiment sweep and extended outline.

## Next Concrete Commands or Repo Tasks

1. Add an experiment mode for a two-dimensional policy space.
2. Add a cost-budgeted fairness-control campaign.
3. Add paired-difference reporting against `CUR` and `SM`.
4. Re-run:

```sh
make campaign
make seed-robustness
make calibration-check
make paper-checks
```

5. Create a political-science results notebook or script that generates distribution plots from `reports/simulation-campaign-v21-paper.csv`.
