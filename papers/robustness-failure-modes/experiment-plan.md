# Experiment Plan

## Baseline Commands

```sh
make ablation-analysis
make manipulation-stress
make mechanism-diagnostics
```

Baseline files:

- `reports/simulation-ablation-analysis.csv`
- `reports/ablation-analysis-summary.csv`
- `reports/simulation-manipulation-stress.csv`
- `reports/manipulation-stress-summary.csv`

## Required New Experiment 1: Formal Adversary Model

Define adversaries by:

- Objective: enact low-support bills, block high-benefit bills, increase administrative burden, raise capture, or reduce revision moderation.
- Information: none, noisy proxy, full generator access, or mechanism-specific knowledge.
- Budget: number of proposal clones, objection filings, harm claims, lobbying camouflage actions, or amendment poison pills.
- Action set: clone, decoy, salience manipulation, harm exaggeration, proposal flooding, lobbying camouflage, public-input noise, agenda sequencing.

Output:

- A table of adversary profiles.
- Worst-case and median degradation by mechanism family.
- Attack success rates by budget and information level.

## Required New Experiment 2: Attack-Intensity Sweeps

Run each stressor at multiple intensities:

- Low: mild perturbation similar to current stress tests.
- Medium: organized group behavior.
- High: concentrated adversary with mechanism knowledge.

Metrics:

- Productivity loss or inflation.
- Low-support enactment increase.
- Risk-control degradation.
- Administrative-cost increase.
- False-negative burden for high-benefit bills.

## Required New Experiment 3: Mechanism-Specific Failure Modes

Mechanism families and attacks:

- Content selection: clones, decoys, agenda sequencing, poison-pill alternatives.
- Harm rules: loose harm claims, strategic minority-claim inflation.
- Citizen panels and objections: noisy panels, framing manipulation, astroturf overload.
- Anti-capture access: lobbying camouflage and proxy sponsors.
- Portfolio systems: routing overload and review exhaustion.
- Burden-shifting systems: objection-window flooding and default-path gaming.

## Required New Experiment 4: Defense and Cost Tradeoffs

For each attack, add a defensive module and measure cost:

- Bond or filing cost.
- Random audit.
- Adversary detection.
- Challenge voucher limits.
- Harm-claim evidence threshold.
- Proposal deduplication or clone filtering.

Report whether the defense reduces attack success and whether it creates unacceptable administrative burden or false blockage.

## New Code Tasks

- Add attack generators under `src/main/java/congresssim/institution/strategy` or a new `adversary` package.
- Add attack-budget parameters to campaign configuration.
- Add worst-case reporting scripts under `scripts/reporting/`.
- Split ablation and manipulation summaries into separate, consistent-sign outputs.

## Proposed Make Targets

```make
adversarial-stress
attack-budget-sweep
worst-case-degradation-report
```
