# Experiment Plan

Final decision: NEEDS DATA/VALIDATION FIRST. These experiments are the second blocker after the validation roadmap: the paper cannot be drafted until both empirical boundaries and benchmark fairness controls improve.

## Baseline Commands

Run the current paper-facing and model-facing baselines:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make campaign
make seed-robustness
make calibration-check
make validation-gap-report
```

Core current outputs:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/scenario-selection-manifest.md`
- `reports/calibration-baseline.csv`
- `reports/seed-robustness-summary.csv`
- `reports/empirical-validation-gap-report.csv`

## Experiment 1: Baseline Calibration Targets

Purpose: keep the stylized U.S.-like benchmark within plausible observable ranges before comparing alternatives.

Targets:

- enactment rate;
- floor load;
- committee reporting and referral rate;
- roll-call coalition size;
- party unity;
- veto frequency;
- sponsor access/success concentration;
- lobbying spending concentration;
- topic throughput.

Required output:

- `reports/political-baseline-calibration.csv`
- `reports/political-baseline-calibration.md`

Do not treat this as validation of public support, welfare, harm, capture, or correction.

## Experiment 2: Stronger Benchmark Fairness Controls

Purpose: test whether content-improvement mechanisms perform well because they receive proposal-revision capacity that conventional systems lack.

Required controls:

- conventional benchmark + committee information gain;
- conventional benchmark + negotiated amendment;
- conventional benchmark + conference compromise;
- simple majority + mediation;
- simple majority + committee revision;
- cost-constrained comparison where each system receives the same review, amendment, information, and attention budget.

Required outputs:

- paired differences versus `CUR` and `SM`;
- administrative-budget table;
- tradeoff plot under equal budgets;
- failure cases where conventional controls catch up or reverse the pattern.

Proposed target:

```make
political-fairness-controls
```

## Experiment 3: Parameter Sweeps

Purpose: align experiments with political theory rather than an all-purpose mechanism catalog.

Sweep dimensions:

- polarization;
- party loyalty;
- proposal pressure;
- lobbying pressure;
- constituency responsiveness;
- committee information quality;
- veto strictness and override threshold;
- agenda gate selectivity;
- amendment/revision capacity;
- public-benefit/support correlation.

Required output:

- `reports/political-parameter-sweeps.csv`
- `reports/political-parameter-sweeps.md`

## Experiment 4: Paired Comparisons

Purpose: compare mechanisms within the same generated worlds rather than relying only on aggregate averages.

Pairs:

- `CUR` vs `CUR + committee information gain`;
- `CUR` vs `CUR + negotiated amendment`;
- `SM` vs `SM + mediation`;
- `SM` vs `SM + committee revision`;
- `COMM` vs `DIS`;
- `VETO` vs `BIC`;
- `ACG` vs `SM`;
- `SEL` vs cost-constrained `SM` and cost-constrained `CUR`.

Metrics:

- productivity;
- floor load;
- revision moderation;
- enacted support;
- low-public-support enactment;
- capture;
- minority/concentrated harm;
- administrative cost;
- generated public benefit per submitted bill.

## Experiment 5: Seed Robustness and Uncertainty Separation

Purpose: separate stochastic uncertainty from scenario variation.

Tasks:

- report seed variance within fixed scenario cases;
- report scenario distribution separately;
- add paired confidence/interval summaries only where the sampling interpretation is valid;
- avoid mean plus case half-range as the main uncertainty display.

Required outputs:

- seed-variance table;
- scenario-variation table;
- paired-difference distribution plot.

## Experiment 6: Public-Benefit / Public-Support Correlation Sensitivity

Purpose: address the central generator-dependence critique.

Required worlds:

- moderation-friendly baseline;
- reform-friendly high-distance proposals;
- public support lags generated benefit;
- lobbying sometimes provides useful information;
- majority support correlates with concentrated harm;
- compromise/revision can dilute benefit;
- public opinion error and noisy support.

Required outputs:

- generator-world matrix;
- reversal table;
- plot of mechanism-family sensitivity to support/benefit correlation.

## Experiment 7: Historical Plausibility Checks

Purpose: improve political-science credibility without overclaiming validation.

Checks:

- Congress.gov/govinfo bill progression;
- Voteview coalition size and party unity;
- LDA lobbying concentration;
- committee referral/reporting/markup data;
- veto frequency;
- sponsor concentration;
- CAP/topic throughput;
- optional cross-national benchmark if data is added.

Required output:

- updated empirical-boundary table that distinguishes flow sanity, proxy checks, and missing validation.

## Proposed Make Targets

```make
political-baseline-calibration
political-fairness-controls
political-parameter-sweeps
political-paired-comparisons
political-generator-sensitivity
political-uncertainty-report
```
