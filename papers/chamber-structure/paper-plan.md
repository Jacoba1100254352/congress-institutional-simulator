# Paper Plan

## Final Decision

NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

The current chamber campaign is useful pilot evidence, but it does not yet support a stand-alone representation-architecture paper. The next work must improve the model's representation diagnostics and add targeted chamber sweeps.

## Working Title

Representation Architecture in Synthetic Legislatures: Chamber Design, Apportionment, Committees, and Review Bodies

## Target Venue Category

Political methodology, legislative studies, public choice, computational social science, social simulation, or comparative institutions.

## One-Sentence Contribution

The future paper will test how chamber architecture, apportionment, committee assignment, selection/retention filters, and independent review bodies change representation diagnostics and legislative tradeoffs under controlled synthetic conditions.

## Why This Is Not Redundant With the ACM CI Paper

The ACM CI paper owns the reusable framework contribution. This paper would instead study representation architecture: how institutional structure changes population-weighted support, chamber-weighted support, district support, affected-group support, malapportionment, committee capture, bicameral conflict, review delay, and productivity.

## Core Mechanisms

| Mechanism area | Existing implemented surface | Needed before paper |
|---|---|---|
| Unicameral vs bicameral structure | `UnicameralProcess`, `BicameralProcess`, `BicameralRoutingProcess` | Paired controls isolating chamber count from routing and revision. |
| Upper-chamber composition | chamber campaign rows for appointed, territorial, proportional, and PR-like variants | Explicit composition parameters and validation targets. |
| Malapportionment | `SeatAllocationProfile`, malapportioned upper scenarios, malapportionment metric in chamber reports | Malapportionment sweep and public-support failure diagnostics. |
| District magnitude | `RepresentationUnit`, chamber/district abstractions | Add district magnitude and district support distributions. |
| Population-seat distortion | seat allocation metrics and malapportionment outputs | Population-weighted versus chamber-weighted diagnostics. |
| Chamber-origin routing | `BicameralOriginRule`, origin-routing scenarios | Conflict and delay outputs by origination rule. |
| Second-chamber amendment/veto powers | upper amendment, suspensive veto, absolute veto, cloture-like scenarios | Power sweep with lower-house override controls. |
| Lower-house override | lower-house override scenarios | Override threshold sweep and conflict resolution metrics. |
| Committee assignment | `CommitteeFactory`, `CommitteeSelectionConfig`, assignment scenarios | Committee assignment/capture sweep and empirical assignment data. |
| Committee power | `CommitteePowerProcess`, `CommitteeInformationProcess`, amendment/revision scenarios | Information-gain and capture controls. |
| Committee capture | committee capture diagnostics in stress reports | Explicit committee-capture adversary or capture parameter. |
| Eligibility filters | expertise, appointment/retention, recusal/cooling-off scenarios | Selection/retention sweep and validation analogues. |
| Appointment/election selection filters | selection/retention scenario family | Explicit selector and retention parameters. |
| Retention/staggered renewal | retention scenario names exist | Add staggered renewal model and turnover outputs if not implemented. |
| Independent review bodies | ex ante advisory, legal clearance, fiscal/electoral/audit insulation, constitutional court architecture | Review-body sweep with delay/cost/risk outputs. |

## Existing Artifacts

- `reports/simulation-chamber-structure.csv`: focused chamber campaign.
- `reports/simulation-chamber-structure.md`: run configuration and scenario averages.
- `reports/chamber-family-champions.md`: fixed-rule family champions.
- `reports/chamber-stress-screen.md`: stress-case chamber winners.
- `paper/figures/chamber_family_table.tex`: existing chamber table asset.
- `paper/figures/chamber_productivity_compromise.tex`: existing chamber plot asset.
- Source packages:
  - `src/main/java/congresssim/institution/chamber`
  - `src/main/java/congresssim/institution/committee`
  - `src/main/java/congresssim/simulation/ChamberSpec.java`
  - `src/main/java/congresssim/simulation/SeatAllocationProfile.java`
  - `src/main/java/congresssim/simulation/RepresentationUnit.java`
  - `src/main/java/congresssim/simulation/ChamberArchitectureMetrics.java`
  - `src/main/java/congresssim/simulation/catalog/ChamberCommitteeScenarioBuilders.java`

## Current Pilot Findings

Use cautiously:

- The chamber campaign reports 51 scenarios across 37 cases with 80 runs per case.
- Existing reports show chamber and committee variants shift productivity, risk, public-support failure, and review metrics.
- Family champion and stress-screen reports are sensitivity screens, not validation.
- Current public-support diagnostics are not yet sufficient for strong representation claims.

## Required Modeling Improvements

1. Make status quo and representation diagnostics clearly domain-aware.
2. Add district/population support distributions rather than only a national public-support scalar.
3. Distinguish public support, district support, affected-group support, and chamber coalition support.
4. Add validation planning for apportionment, population distributions, chamber voting, committee assignment, referrals/markups, bicameral disagreement, and review bodies.

## Go/No-Go

No-go for full draft.

Go for representation-model upgrades, validation planning, and targeted chamber experiments.
