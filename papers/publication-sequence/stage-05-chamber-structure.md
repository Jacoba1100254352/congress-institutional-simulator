# Stage 5: Chamber-Structure Paper

## Go/No-Go Decision

No-go for drafting now. Go only after expanded chamber scenarios, district/group representation diagnostics, and validation targets are ready.

Primary workspace: `papers/chamber-structure/`.

## Repo Tasks

- Expand chamber scenarios around representation architecture rather than general mechanism bundles.
- Add or strengthen district-level support, group support, harm concentration, and chamber-conflict diagnostics.
- Isolate bicameralism, apportionment, committee information, and review architecture with paired controls.
- Use Stage 2 empirical roadmap to identify chamber-specific validation targets.
- Keep chamber work out of the ACM paper except as appendix/supporting material.

## Experiments to Run

Baseline:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make chamber-structure
make chamber-structure-summary
```

New required targets:

```make
chamber-representation-sensitivity
district-support-sensitivity
committee-information-controls
review-architecture-sensitivity
chamber-paired-report
```

Required scenario factors:

- Equal-population unicameral.
- Proportional bicameral.
- Malapportioned upper chamber.
- Conference committee with and without revision power.
- Committee expertise versus party-ratio assignment.
- Ex ante review, ex post review, law registry, and review-budget constraints.
- District heterogeneity and concentrated group harm.

## Figures and Tables to Generate

Required:

- Chamber-design hypothesis table.
- Chamber variants table.
- Chamber architecture tradeoff plot.
- Representation geometry small multiples.
- Committee information-gain plot.
- Review architecture correction plot.
- Empirical anchor table for representation and chamber metrics.

Appendix:

- Full `reports/simulation-chamber-structure.csv`.
- Chamber family champions.
- Chamber stress-screen outputs.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| The repo already has chamber-structure experiments. | `reports/simulation-chamber-structure.csv`, chamber summaries. | Current campaign is supplemental and broad. | Usable as pilot evidence. |
| Chamber architecture shifts productivity/revision tradeoffs. | Existing chamber campaign. | Needs paired controls and uncertainty summaries. | Conditional. |
| Chamber design affects representation diagnostics. | Theoretically plausible. | Current public support is too synthetic/scalar for strong claims. | Blocking. |
| Committee and review structures can be treated as information/correction mechanisms. | Source modules and chamber scenarios. | Needs information-gain and review-budget controls. | Conditional. |
| Chamber paper should follow political-science paper. | Depends on empirical roadmap and representation diagnostics. | Not enough validation now. | Use as sequencing rule. |

## Paper Outline

Do not draft until required diagnostics exist:

1. Introduction: representation architecture and collective decisions.
2. Theory: chamber design, apportionment, committees, review.
3. Simulator chamber modules and empirical boundary.
4. Experiment design.
5. Results: representation, committee, and review effects.
6. Discussion.
7. Limitations.
8. Conclusion.
