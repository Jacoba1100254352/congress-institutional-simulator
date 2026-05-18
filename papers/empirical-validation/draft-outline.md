# Draft Outline

Status: outline only. Do not draft the full paper yet.

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY.

## 1. Introduction

- Legislative mechanism simulators need empirical boundary conditions.
- Many politically important model quantities are not directly observable.
- The paper asks what empirical signals can calibrate, sanity-check, proxy, or validate simulator quantities, and where gaps remain.
- The contribution is a benchmark construction and validation-readiness framework, not proof that a simulator is valid.

## 2. Empirical Signal Taxonomy

- Legislative flow: bill introduction, floor action, committee reporting, enactment.
- Roll-call behavior: coalition size, party unity, chamber vote patterns.
- Agenda/topic mix: topic entropy and issue throughput.
- Sponsor and legislative effectiveness.
- Lobbying and campaign finance.
- Public opinion and representation.
- Committee process.
- Court review and invalidation.
- Implementation and rulemaking.
- Law revision and correction.
- Comparative institutions.

## 3. Current Pipeline

- Current ready inputs.
- Current missing inputs.
- Current computed summaries.
- Current flow sanity checks.
- Current calibration screen.

## 4. Metric Mapping and Claim Boundaries

- Validated.
- Sanity-checkable.
- Proxy only.
- Synthetic only.
- Not currently modeled.
- Explain why current central model outputs remain unvalidated.

## 5. Data Pipeline Design

- Source registry.
- Raw fetch and cache.
- Normalization.
- Summary generation.
- Metric mapping.
- Offline reproduction.
- Held-out validation design.

## 6. Validation-Readiness Scorecard

- Raw input coverage.
- Flow checks.
- Public-support readiness.
- Influence/campaign-finance readiness.
- Committee process readiness.
- Court/review readiness.
- Implementation/correction readiness.
- Comparative-institution readiness.
- Reproducibility readiness.

## 7. Missing-Data Roadmap

- Public opinion and affected-group support.
- OpenFEC/campaign finance.
- Lobbying-to-bill linkage.
- Committee hearings/markups/discharge.
- Court review/invalidation.
- Federal Register / Unified Agenda / Regulations.gov.
- Statutory lineage.
- Cross-national party/chamber systems.

## 8. Discussion

- What can be benchmarked now.
- What remains synthetic.
- How the roadmap supports future political-science, chamber, robustness, and software papers.
- Why validation boundaries matter more than a single fit score.

## 9. Limitations

- Bounded samples.
- Missing high-priority data.
- Proxy risks.
- No held-out validation yet.
- No claim that simulator rankings are empirically validated.

## 10. Conclusion

- The future paper should close with benchmark-readiness and missing-data priorities, not a validation claim.
