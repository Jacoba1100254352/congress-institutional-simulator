# Stage 1: Finish and Freeze the ACM CI Framework Paper

## Go/No-Go Decision

Go for final polish and freeze. Do not broaden the ACM paper, do not add new breakout claims, and do not convert it back into an umbrella manuscript.

Freeze criteria:

- `make paper-checks` passes.
- `make reproduce-paper-offline` passes.
- Anonymous supplement builds cleanly.
- No stale `main.pdf`-style drafts or strategy notes are included in the anonymous artifact package.
- The paper keeps the framework contribution central: reusable architecture, diagnostic dashboard, generator assumptions, and synthetic design hypotheses.

## Repo Tasks

- Audit `paper/acm-ci-framework/acm-ci-framework.tex` for scope drift.
- Audit `paper/technical-appendix/odd-d-appendix.tex` for appendix roadmap clarity and artifact pointers.
- Verify `README.md` remains reproduction-focused.
- Keep `paper/notes/breakout-paper-plan.md` out of anonymous submission bundles unless explicitly allowed.
- Confirm generated PDFs use descriptive names:
  - `paper/acm-ci-framework/acm-ci-framework.pdf`
  - `paper/technical-appendix/odd-d-appendix.pdf`
- Run anonymity, figure-label, table-consistency, PDF-render, and manifest checks.

## Experiments to Run

This stage should not add new experiments unless a check fails. It should rerun only the canonical artifact workflow:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
make reproduce-paper-offline
make supplement-anonymous
```

Optional if outputs are stale:

```sh
make campaign
make mechanism-diagnostics
make paper-checks
```

## Figures and Tables to Generate

Use the existing ACM set only:

- Modular simulation pipeline.
- Key generator and vote-kernel assumptions.
- Main metrics and interpretation.
- Empirical flow sanity checks.
- Mechanism-family table.
- Productivity/risk/revision-moderation tradeoff figure.
- Selected metric profiles.
- Robustness/failure-mode summary.

No new breakout-specific figures belong in this paper.

## Claims Ledger

| Claim | Support | Limitation | Status |
|---|---|---|---|
| The project contributes a reusable simulation framework. | ACM paper, ODD+D appendix, Java source, Make workflow. | Framework is synthetic and not a validated Congress model. | Keep. |
| The framework makes tradeoffs inspectable under shared synthetic worlds. | Main campaign, figures, metric dashboard. | Tradeoffs depend on generator assumptions. | Keep with caveat. |
| The empirical layer is a flow sanity check. | `reports/calibration-baseline.*`, `reports/empirical-bridge.*`. | Does not validate welfare, harm, capture, support, or revision moderation. | Keep. |
| Particular legislative designs are generally superior. | Not supported. | Would overclaim beyond synthetic evidence. | Exclude. |
| Breakout papers are submission-ready. | Current plans only. | Most require new experiments or validation. | Exclude from ACM paper. |

## Paper Outline

The ACM paper outline should remain:

1. Introduction and collective-intelligence framing.
2. Simulator architecture and generator assumptions.
3. Metrics and campaign design.
4. Results as framework demonstration.
5. Empirical flow sanity checks.
6. Limitations.
7. Reproducibility and AI disclosure.
8. Conclusion focused on reusable architecture.
