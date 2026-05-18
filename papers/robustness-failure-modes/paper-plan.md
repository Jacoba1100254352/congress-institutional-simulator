# Paper Plan

## Final Decision

NEEDS ADVERSARY EXPERIMENTS FIRST.

The paper is promising as an independent technical breakout, but current evidence is still a pilot stress screen. It lacks explicit adversary models, budget sweeps, worst-case degradation, attack success rates, and correction/recovery metrics.

## Working Title

Adversarial Failure Modes in Legislative Collective-Decision Mechanisms

## Target Venue Category

Computational social science, social simulation, mechanism design, adversarial social systems, governance technology, or collective-decision systems.

## One-Sentence Contribution

The future paper will identify which legislative mechanism families are robust or fragile when bounded adversaries manipulate proposal content, agenda sequencing, public-input channels, harm claims, lobbying signals, and administrative capacity.

## Why This Is Not Redundant With the ACM CI Paper

The ACM CI paper contributes the reusable simulation framework and uses robustness probes only as boundary evidence. This paper would make adversarial failure itself the central object: actor models, goals, budgets, information levels, attack strategies, worst-case degradation, and recovery behavior.

## Current Evidence

Existing pilot artifacts:

- `reports/simulation-manipulation-stress.csv`: 91 rows, 212 columns.
- `reports/manipulation-stress-summary.md`: pilot stress summary.
- `reports/simulation-ablation-analysis.csv`: 405 rows, 212 columns.
- `reports/ablation-analysis-summary.md`: mechanism ablation summary.
- `reports/scenario-selection-manifest.md`: mechanism labels and stress-case context.
- `reports/simulation-manipulation-stress.md`: stress-campaign configuration and scenario averages.
- source modules under `institution/bargaining`, `agenda`, `publicinput`, `distribution`, `lobbying`, `accountability`, `review`, and `strategy`.

Pilot findings that can be used only as motivation:

- Policy tournament clone/decoy attack shows material vulnerability in the current summary.
- Open burden-shifting capture stress shows material vulnerability.
- Citizen-panel manipulation, loose harm claims, astroturf pressure, and proposal flooding show limited observed degradation under current bounded probes.
- Anti-capture defensive backlash improves the current score profile in the pilot, which signals that the stress design is not yet a general adversary model.

## Core Failure Modes to Study

- clone/decoy alternatives in policy tournaments;
- agenda sequencing manipulation;
- poison-pill amendments;
- astroturf objection windows;
- noisy or biased citizen panels;
- bad-faith harm claims;
- proposal flooding;
- lobbying camouflage;
- public-support distortion;
- defensive lobbying against anti-capture reform;
- administrative overload attacks;
- strategic silence under burden-shifting passage rules.

## Mechanism Families

| Family | Current representative(s) | Attack surface |
|---|---|---|
| Content selection / policy tournaments | `simple-majority-alternatives-pairwise`, `pairwise-amendment-tournament-majority`, strategic tournament rows | clones, decoys, sequencing, poison-pill amendments |
| Agenda access / open calendars | `open-rule-calendar-majority`, `agenda-lottery-majority`, `leadership-cartel-majority` | proposal flooding, agenda sequencing, gatekeeper manipulation |
| Objection and public-input systems | `public-objection-majority`, citizen panels, petitions | astroturf, noise, framing, challenge exhaustion |
| Harm-protection systems | `harm-weighted-majority`, compensation/affected-group variants | bad-faith harm claims, false positives, false negatives |
| Anti-capture systems | `anti-capture-access-majority`, `anti-capture-majority-bundle`, `influence-system-majority` | lobbying camouflage, proxy sponsors, defensive lobbying |
| Portfolio systems | `portfolio-hybrid-legislature`, `expanded-portfolio-hybrid-legislature` | administrative overload, routing exhaustion, review-budget exhaustion |
| Burden-shifting systems | `default-pass`, `default-pass-challenge`, `default-pass-multiround-mediation-challenge` | proposal flooding, strategic silence, challenge-token exhaustion |

## Go/No-Go

No-go for full draft.

Go for code/model upgrade and expanded adversarial campaign.

## Required Next Repo Tasks

1. Add explicit adversary model classes or records.
2. Add adversarial campaign definitions and attack-intensity sweeps.
3. Add reporting for worst-case degradation, median degradation, attack success rate, mechanism-specific vulnerability, recovery/correction, and administrative burden under attack.
4. Split ablation reporting from adversarial-stress reporting.
5. Add failure trace logging for selected runs.
6. Re-run tests and new campaigns before any full paper drafting.
