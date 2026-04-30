# Paper Findings Validation

This report is generated from `reports/simulation-campaign-v21-paper.csv` and, when present, `reports/seed-robustness-summary.csv`. It is a validation aid for the paper tables and figures, not a separate empirical result.

## Data Integrity Checks

- Campaign rows: 986
- Broad/adversarial scenarios with averages: 29
- Broad/adversarial cases per scenario: [24]
- Portfolio hybrid present: yes
- Seed directional intervals present for focus scenarios: 8 / 8

## Focus Scenario Averages

| Key | Scenario | Dir. | Prod. | Comp. | Risk ctrl. | Rep. quality | Weak mandate | Welfare | Lobby capture | Seed dir. mean [min,max] |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `current-system` | Stylized U.S.-like conventional benchmark | 0.653 | 0.052 | 0.368 | 0.929 | 0.648 | 0.007 | 0.697 | 0.205 | 0.650 [0.647, 0.653] |
| `simple-majority-alternatives-pairwise` | Unicameral majority + pairwise alternatives | 0.712 | 0.542 | 0.502 | 0.937 | 0.654 | 0.002 | 0.627 | 0.229 | 0.712 [0.712, 0.713] |
| `portfolio-hybrid-legislature` | Portfolio hybrid legislature | 0.705 | 0.504 | 0.421 | 0.932 | 0.625 | 0.031 | 0.618 | 0.150 | 0.706 [0.705, 0.706] |
| `risk-routed-majority` | Risk-routed majority legislature | 0.687 | 0.531 | 0.264 | 0.842 | 0.544 | 0.234 | 0.508 | 0.290 | 0.686 [0.686, 0.687] |
| `anti-capture-majority-bundle` | Majority + anti-capture bundle | 0.676 | 0.307 | 0.248 | 0.884 | 0.578 | 0.154 | 0.648 | 0.138 | 0.676 [0.675, 0.677] |
| `law-registry-majority` | Active-law registry + majority review | 0.654 | 0.345 | 0.237 | 0.836 | 0.555 | 0.244 | 0.594 | 0.259 | 0.655 [0.654, 0.655] |
| `default-pass` | Default pass unless 2/3 block | 0.725 | 0.866 | 0.136 | 0.629 | 0.476 | 0.472 | 0.500 | 0.278 | 0.725 [0.724, 0.726] |
| `default-pass-multiround-mediation-challenge` | Default pass + multi-round mediation + challenge | 0.708 | 0.803 | 0.243 | 0.727 | 0.509 | 0.375 | 0.459 | 0.288 | 0.708 [0.706, 0.710] |

## Ranking Cross-Checks

- Top directional scores: `default-pass` (0.725), `simple-majority-alternatives-pairwise` (0.712), `default-pass-multiround-mediation-challenge` (0.708), `portfolio-hybrid-legislature` (0.705), `citizen-initiative-referendum` (0.693), `risk-routed-majority` (0.687), `default-pass-challenge` (0.683), `anti-capture-majority-bundle` (0.676).
- Top compromise scores under party-system sensitivity cases: `simple-majority-alternatives-pairwise` (0.518), `portfolio-hybrid-legislature` (0.411), `current-system` (0.377), `supermajority-60` (0.360), `cloture-conference-review` (0.348).
- Top productivity scores: `default-pass` (0.866), `default-pass-multiround-mediation-challenge` (0.803), `default-pass-challenge` (0.659), `simple-majority-alternatives-pairwise` (0.542), `risk-routed-majority` (0.531).
- Lowest weak public-mandate passage: `simple-majority-alternatives-pairwise` (0.002), `current-system` (0.007), `portfolio-hybrid-legislature` (0.031), `cloture-conference-review` (0.032), `citizen-assembly-threshold` (0.061).
- Highest generated welfare: `current-system` (0.697), `citizen-assembly-threshold` (0.686), `cloture-conference-review` (0.685), `supermajority-60` (0.662), `leadership-cartel-majority` (0.652).

## Hybrid Interpretation

- Versus pairwise alternatives, `portfolio-hybrid-legislature` changes productivity by -0.037, compromise by -0.082, risk control by -0.005, weak-mandate passage by +0.029, and lobbying capture by -0.079.
- Versus risk-routed majority, `portfolio-hybrid-legislature` changes productivity by -0.026, compromise by +0.157, risk control by +0.090, weak-mandate passage by -0.202, and lobbying capture by -0.140.
- Versus anti-capture bundle, `portfolio-hybrid-legislature` changes productivity by +0.198, compromise by +0.173, risk control by +0.048, weak-mandate passage by -0.122, and lobbying capture by +0.013.
- Versus open default pass, `portfolio-hybrid-legislature` changes productivity by -0.362, compromise by +0.285, risk control by +0.303, weak-mandate passage by -0.441, and lobbying capture by -0.128.

The hybrid is best read as a synthesized candidate rather than a final winner. Pairwise alternatives remain the cleanest non-default productivity/compromise result. The hybrid preserves much of that productivity while adding lower lobbying capture and stronger weak-mandate control, but it pays in administrative load and loses some compromise because not every bill enters the pairwise route.

The design hypothesis to carry forward is a portfolio legislature: low-risk bills should move quickly; medium-risk bills should face alternative comparison and mediation; high-risk or high-harm bills should face public/harm review; proposers should internalize some outcome risk; organized-interest pressure should be visible and audited; enacted high-uncertainty laws should be reviewed later.
