# Paper Findings Validation

This report is generated from `reports/simulation-campaign-v21-paper.csv` and, when present, `reports/seed-robustness-summary.csv`. It is a validation aid for the paper tables and figures, not a separate empirical result.

## Data Integrity Checks

- Campaign rows: 1628
- Broad/adversarial scenarios with averages: 44
- Broad/adversarial cases per scenario: [27]
- Portfolio hybrid present: yes
- Seed directional intervals present for focus scenarios: 8 / 8

## Focus Scenario Averages

| Key | Scenario | Dir. | Prod. | Comp. | Risk ctrl. | Rep. quality | Low public support | Welfare | Lobby capture | Seed dir. mean [min,max] |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `current-system` | Stylized U.S.-like conventional benchmark | 0.610 | 0.052 | 0.356 | 0.930 | 0.475 | 0.007 | 0.657 | 0.202 | 0.612 [0.611, 0.614] |
| `simple-majority-alternatives-pairwise` | Unicameral majority + pairwise alternatives | 0.701 | 0.558 | 0.505 | 0.936 | 0.598 | 0.002 | 0.636 | 0.229 | 0.696 [0.696, 0.697] |
| `portfolio-hybrid-legislature` | Portfolio hybrid legislature | 0.700 | 0.532 | 0.426 | 0.931 | 0.580 | 0.028 | 0.631 | 0.148 | 0.693 [0.692, 0.693] |
| `risk-routed-majority` | Risk-routed majority legislature | 0.680 | 0.552 | 0.262 | 0.838 | 0.502 | 0.230 | 0.521 | 0.286 | 0.674 [0.674, 0.675] |
| `anti-capture-majority-bundle` | Majority + anti-capture bundle | 0.658 | 0.317 | 0.244 | 0.881 | 0.498 | 0.152 | 0.654 | 0.137 | 0.656 [0.655, 0.656] |
| `law-registry-majority` | Active-law registry + majority review | 0.636 | 0.354 | 0.232 | 0.830 | 0.473 | 0.256 | 0.599 | 0.258 | 0.636 [0.636, 0.637] |
| `default-pass` | Default pass unless 2/3 block | 0.734 | 0.873 | 0.136 | 0.630 | 0.501 | 0.470 | 0.519 | 0.275 | 0.729 [0.728, 0.730] |
| `default-pass-multiround-mediation-challenge` | Default pass + multi-round mediation + challenge | 0.708 | 0.806 | 0.243 | 0.727 | 0.507 | 0.363 | 0.479 | 0.283 | 0.705 [0.704, 0.707] |

## Ranking Cross-Checks

- Top directional scores: `default-pass` (0.734), `default-pass-multiround-mediation-challenge` (0.708), `simple-majority-alternatives-pairwise` (0.701), `portfolio-hybrid-legislature` (0.700), `pairwise-amendment-tournament-majority` (0.699), `expanded-portfolio-hybrid-legislature` (0.684), `risk-routed-majority` (0.680), `citizen-initiative-referendum` (0.677).
- Top compromise scores under party-system sensitivity cases: `simple-majority-alternatives-pairwise` (0.518), `pairwise-amendment-tournament-majority` (0.517), `expanded-portfolio-hybrid-legislature` (0.464), `portfolio-hybrid-legislature` (0.410), `current-system` (0.377).
- Top productivity scores: `default-pass` (0.873), `default-pass-multiround-mediation-challenge` (0.806), `expanded-portfolio-hybrid-legislature` (0.803), `default-pass-challenge` (0.646), `long-horizon-learning-majority` (0.610).
- Lowest low-public-support enactment: `simple-majority-alternatives-pairwise` (0.002), `pairwise-amendment-tournament-majority` (0.002), `expanded-portfolio-hybrid-legislature` (0.002), `current-system` (0.007), `committee-amendment-majority` (0.015).
- Highest generated welfare: `committee-amendment-majority` (0.713), `citizen-assembly-threshold` (0.690), `committee-discharge-target-majority` (0.685), `cloture-conference-review` (0.680), `random-public-review-panel-majority` (0.675).

## Hybrid Interpretation

- Versus pairwise alternatives, `portfolio-hybrid-legislature` changes productivity by -0.025, compromise by -0.079, risk control by -0.005, low-public-support enactment by +0.026, and lobbying capture by -0.081.
- Versus risk-routed majority, `portfolio-hybrid-legislature` changes productivity by -0.020, compromise by +0.164, risk control by +0.093, low-public-support enactment by -0.202, and lobbying capture by -0.138.
- Versus anti-capture bundle, `portfolio-hybrid-legislature` changes productivity by +0.215, compromise by +0.182, risk control by +0.050, low-public-support enactment by -0.124, and lobbying capture by +0.012.
- Versus open default pass, `portfolio-hybrid-legislature` changes productivity by -0.341, compromise by +0.290, risk control by +0.301, low-public-support enactment by -0.443, and lobbying capture by -0.127.

The portfolio variants illustrate the tradeoff between combining safeguards and increasing administrative load. Pairwise alternatives remain the cleanest alternative-selection productivity/compromise result; the hybrid preserves much of that productivity while adding lower lobbying capture and stronger low-public-support controls, but it pays in administrative load and loses some compromise because not every bill enters the pairwise route.

A portfolio legislature remains one testable mechanism bundle: low-risk bills move quickly; medium-risk bills face alternative comparison and mediation; high-risk or high-harm bills face public/harm review; proposers internalize some outcome risk; organized-interest pressure is visible and audited; enacted high-uncertainty laws are reviewed later.
