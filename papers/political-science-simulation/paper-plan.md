# Paper Plan

## Final Decision

NEEDS DATA/VALIDATION FIRST.

The paper also needs benchmark-fairness experiments before drafting, but the strict first blocker is data/validation. Without stronger empirical boundaries, the paper would look like a synthetic mechanism-ranking paper with political-science vocabulary layered on top.

## Working Title

Agenda Control, Veto Points, and Proposal Transformation in a Synthetic Legislative Simulator

## Target Venue Category

Computational social science, political methodology, public choice, legislative studies, or social simulation.

## One-Sentence Contribution

The future paper would evaluate how politically meaningful mechanisms--agenda control, committee routing, vetoes, lobbying pressure, proposal access, and content-improvement stages--shift productivity, representative responsiveness, capture risk, and public-support failure under explicit synthetic and empirically screened benchmark conditions.

## Non-Redundancy With the ACM CI Paper

The ACM CI paper contributes the reusable simulation framework, diagnostic dashboard, and artifact workflow. This paper must contribute institutional theory and model behavior under politically meaningful benchmark conditions. It should cite the ACM paper or appendix only as a methods/source artifact and should not re-argue the framework contribution.

## Implemented Mechanism Inventory

| Political-science construct | Implemented representative(s) | Existing artifacts | Current readiness |
|---|---|---|---|
| Stylized U.S.-like benchmark | `current-system` / `CUR` | `CurrentSystemAgendaAccessRule`, `reports/simulation-campaign-v21-paper.csv`, `reports/calibration-baseline.md` | Usable as stylized benchmark, not calibrated Congress. |
| Simple majority | `simple-majority` / `SM` | `AffirmativeThresholdRule`, manifest row `SM` | Usable baseline. |
| Committee regular order | `committee-regular-order` / `COMM` | `CommitteeGatekeepingProcess`, manifest row `COMM` | Usable but needs committee empirical targets. |
| Discharge petition | `committee-discharge-target-majority` / `DIS` | committee/discharge scenario, manifest row `DIS` | Usable as committee-bypass prototype. |
| Open floor calendar | `open-rule-calendar-majority` / `OPEN` | `OpenFloorCalendarProcess`, manifest row `OPEN` | Usable agenda-access contrast. |
| Veto/override systems | `presidential-veto`, `cloture-conference-review` | `PresidentialVetoProcess`, `ConferenceCommitteeProcess`, manifest rows `VETO`, `PROC` | Needs clearer veto-player framing and calibration. |
| Bicameral systems | `bicameral-majority`, chamber campaign | `BicameralProcess`, `BicameralRoutingProcess`, `reports/simulation-chamber-structure.csv` | Use only selectively; chamber paper owns deeper treatment. |
| Lobbying/capture mechanisms | `default-pass-budgeted-lobbying`, `influence-system-majority`, capture metrics | `BudgetedLobbyingProcess`, `InfluenceSystemProcess`, `LobbyCaptureScoring` | Needs lobbying-to-bill and campaign-finance validation. |
| Anti-capture access | `anti-capture-access-majority` / `ACG`; `anti-capture-majority-bundle` / `CAP` | `LobbySurchargeProposalAccessRule`, `LobbyAuditProcess`, transparency/audit modules | Usable as synthetic anti-capture scenarios; not empirically validated. |
| Content-selection mechanisms | `simple-majority-alternatives-pairwise`, `pairwise-amendment-tournament-majority` | `CompetingAlternativesProcess`, `AlternativeSelectionRule`, manifest rows `PAIR`, `AMT` | Must be merged as `SEL` unless new divergence is shown. |
| Portfolio hybrid | `portfolio-hybrid-legislature` / `PORT` | manifest row `PORT`, source modules across routing/review/access | Include only if theoretically justified as bundled safeguards; do not make it a favored design. |

## Political-Theory Framing

This paper should frame implemented modules through political science concepts:

- spatial voting: status-quo-relative utility and legislator ideal points;
- pivotal politics: thresholds, vetoes, blocking coalitions, override rules;
- veto-player theory: bicameralism, executive veto, court/review layers, supermajority rules;
- committee gatekeeping: committee-first routing, reporting, discharge, amendment power, information gain;
- agenda control: leadership cartel, open calendar, proposal access screens, lobbying surcharges, floor scheduling;
- lobbying as information/access/subsidy: separate technical information, access pressure, private-gain pressure, and campaign-finance influence;
- legislative effectiveness: throughput, floor load, sponsor access, enactment rates, policy yield;
- public-support representation: national support, district support, affected-group support, and public-support failure.

## Existing Artifacts It Can Use

- `reports/simulation-campaign-v21-paper.csv`: canonical main campaign.
- `reports/simulation-campaign-v21-paper.md`: run configuration and scenario averages.
- `reports/scenario-selection-manifest.md`: mechanism labels and selection rationale.
- `reports/calibration-baseline.md`: current flow sanity checks.
- `reports/empirical-validation-gap-report.md`: empirical boundary and missing data.
- `reports/seed-robustness-summary.csv`: seed robustness.
- `reports/family-champions.md` and `reports/representative-vs-family-champions.csv`: family-level checks.
- `reports/simulation-chamber-structure.csv`: only for limited bicameral/chamber references.
- `paper/technical-appendix/odd-d-appendix.pdf`: model and generator details.
- Source packages under `institution/agenda`, `committee`, `chamber`, `lobbying`, `bargaining`, `voting`, `review`, and `accountability`.

## Missing Validation Data

- District-level public opinion.
- Campaign finance / OpenFEC.
- Lobbying-to-bill linkage.
- Committee hearings, markups, referrals, amendments, and discharge petitions.
- Court review and invalidation.
- Implementation and agency enforcement.
- Law revision, repeal, sunset, and reauthorization.
- Cross-national parliamentary or bicameral comparisons.

## Required Benchmark Fairness Controls

- Conventional benchmark + committee information gain.
- Conventional benchmark + negotiated amendment.
- Conventional benchmark + conference compromise.
- Simple majority + mediation.
- Simple majority + committee revision.
- Cost-constrained comparison where each system gets the same review, amendment, information, and attention budget.

## Required New Code Or Data Work

Before drafting, add or extend:

1. Political fairness-control scenarios that isolate process capacity from institutional label.
2. A political paired-comparison report that uses matched seeds/worlds and reports differences versus `CUR` and `SM`.
3. A cost-budget accounting layer for review, amendment, information, and attention resources.
4. A public-benefit/public-support sensitivity report that includes decoupled support-benefit worlds.
5. Empirical source upgrades identified in `../empirical-validation/go-no-go.md`, especially public opinion, campaign finance, and correction/implementation data.

## Next Concrete Commands

Current evidence refresh:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make campaign
make seed-robustness
make calibration-check
make validation-gap-report
```

Future targets to add:

```make
political-fairness-controls
political-paired-comparisons
political-uncertainty-report
political-generator-sensitivity
political-validation-targets
```

## Go/No-Go

No-go for full draft.

Proceed with data/validation and fairness-control work. Reassess only after validation-plan and experiment-plan milestones are complete.
