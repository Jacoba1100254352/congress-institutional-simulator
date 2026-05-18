# Draft Outline

Status: outline only. Do not draft the full paper until `validation-plan.md` and `experiment-plan.md` blockers are resolved.

Final decision: NEEDS DATA/VALIDATION FIRST.

## 1. Introduction

- Legislative institutions shape proposal access, bargaining, veto opportunities, and public responsiveness.
- The paper asks when agenda control, committees, vetoes, lobbying, proposal access, and content improvement change legislative outputs under explicit assumptions.
- Contribution is institutional model behavior, not the reusable framework.
- Scope: synthetic political-science simulation with empirical boundary checks, not an empirical ranking of institutions.

## 2. Political Theory and Hypotheses

- Spatial voting and status-quo-relative preferences.
- Pivotal politics and threshold/veto structures.
- Veto-player theory and bicameral/executive/court vetoes.
- Committee gatekeeping and information.
- Agenda control and proposal access.
- Lobbying as information, access, subsidy, and private-gain pressure.
- Legislative effectiveness and throughput.
- Public-support representation and mandate failure.

Possible hypotheses:

- H1: agenda gates reduce floor load and low-support enactment at the cost of productivity.
- H2: committee information/revision can improve generated public benefit without merely blocking proposals.
- H3: veto structures suppress enactment but may not improve representation if they only block.
- H4: lobbying pressure shifts capture diagnostics unless countered by access or audit rules.
- H5: content-improvement stages outperform yes/no voting only under specific generator and budget assumptions.
- H6: public-support findings change when support and generated benefit are decoupled.

## 3. Model Summary

- Briefly describe the simulator and cite the ACM framework/appendix as methods background.
- Define mechanism families used in this paper.
- Define politically relevant metrics.
- State generator assumptions and public-benefit/support dependence.

## 4. Empirical Boundary and Calibration

- Current flow sanity checks.
- Missing validation data.
- Proxy risks.
- Planned held-out validation design.
- Clarify that public support, harm, capture, and correction are not validated yet unless new data has been added.

## 5. Experiment Design

- Baseline calibration targets.
- Benchmark fairness controls.
- Parameter sweeps.
- Paired comparisons.
- Seed robustness and uncertainty decomposition.
- Public-benefit/support correlation sensitivity.

## 6. Results

This section should be drafted only after new experiments.

Planned result subsections:

- Agenda control and committee routing.
- Veto structures and bicameralism.
- Lobbying pressure and anti-capture access.
- Content-improvement stages under fair budgets.
- Generator-sensitivity and reversal cases.
- Empirical plausibility boundary.

## 7. Discussion

- Which political mechanisms appear behaviorally distinct in the simulator.
- Which findings depend on generator assumptions.
- What benchmark fairness controls change.
- What validation gaps matter most for political-science interpretation.

## 8. Limitations

- Synthetic public benefit and public support.
- Missing district opinion and influence linkage.
- Limited strategic adaptation.
- One-dimensional baseline unless new model is implemented.
- No claim of institutional superiority.

## 9. Conclusion

- The future conclusion should emphasize political model behavior under explicit assumptions, not a framework claim or reform recommendation.
