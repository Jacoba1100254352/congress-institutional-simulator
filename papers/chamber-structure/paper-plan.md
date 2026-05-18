# Paper Plan: Chamber Structure

## Working Title

Representation Architecture in Synthetic Legislatures: Chamber Design, Committees, and Review Structures

## Target Venue Category

Political methodology, legislative studies, public choice, computational social science, or representation-focused social simulation.

## One-Sentence Contribution

The paper would isolate how chamber architecture, apportionment, committee assignment, review institutions, and bicameral conflict shift productivity, revision moderation, support, risk, and representation diagnostics in a synthetic legislative simulator.

## Why This Is Not Redundant With the ACM CI Paper

The ACM paper presents the general framework and a small mechanism-family comparison. This breakout would focus narrowly on representation architecture and chamber design, using the existing chamber-structure campaign as the starting point.

## Current Readiness Decision

Ready for an extended outline plus experiment plan. Not ready for a full manuscript draft.

The chamber campaign is large enough to justify planning, but it needs clearer hypotheses, better controls, and an empirical comparison strategy before it can stand alone.

## Existing Artifacts and Results It Can Use

- `reports/simulation-chamber-structure.csv`: 2346 rows, 212 columns.
- `reports/simulation-chamber-structure.md`: chamber campaign run details.
- `reports/chamber-family-champions.md`: family champion summaries.
- `reports/chamber-stress-screen.md`: chamber stress-screen summary.
- `paper/figures/chamber_family_table.tex` and `paper/figures/chamber_productivity_compromise.tex`: existing LaTeX figure/table assets.
- `reports/scenario-selection-manifest.md`: scenario context.
- Source packages under `src/main/java/congresssim/institution/chamber`, `committee`, `distribution`, and `review`.

Observed current signal:

- Chamber and review variants shift productivity and revision-moderation surfaces, but do not currently dominate the main mechanism-level comparison.
- Some chamber-family champions appear under adversarial moderate-capture and other stress cases.
- The current ACM paper properly treats chamber structure as supplemental rather than central.

## Missing Experiments or Validation Needed Before Submission

- Explicit chamber-design hypotheses: representation equality, malapportionment, bicameral conflict, committee specialization, independent review, and selection/retention.
- Controls that isolate chamber structure from proposal-transformation mechanisms.
- District-level or group-level support distributions rather than only scalar public support.
- Empirical anchors for apportionment, bicameralism, committee reporting, upper-chamber composition, and review institutions.
- Sensitivity to district heterogeneity, party geography, turnout, and issue-domain concentration.
- Clear separation between representation diagnostics and generated public benefit.

## Go/No-Go Recommendation

No-go for a full chamber-structure paper now. Go for a focused chamber-design campaign and validation plan.

## Next Concrete Commands or Repo Tasks

Current baseline:

```sh
make chamber-structure
make chamber-structure-summary
make paper-checks
```

Needed new targets:

```make
chamber-representation-sensitivity
district-support-sensitivity
committee-information-controls
```
