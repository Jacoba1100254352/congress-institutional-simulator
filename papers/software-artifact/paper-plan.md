# Paper Plan: Software Artifact

## Working Title

Congress Institutional Simulator: A Reproducible Java Toolkit for Legislative Mechanism Stress Tests

## Target Venue Category

Software artifact track, JOSS-style software paper, SoftwareX-style article, or ACM artifact companion.

## One-Sentence Contribution

The artifact paper would document a reproducible Java 21 toolkit for running synthetic legislative mechanism campaigns, generating diagnostic reports, and rebuilding the ACM framework paper's figures and appendix offline.

## Why This Is Not Redundant With the ACM CI Paper

The ACM paper argues for a framework and reports demonstration campaigns. This breakout would focus on the software artifact itself: installation, command-line workflow, reproducibility guarantees, package structure, outputs, tests, and reuse boundaries.

## Current Readiness Decision

Ready for an artifact-hardening plan and extended outline. Not ready for a full software paper submission.

The repository has strong reproduction infrastructure, but no license, no `CITATION.cff`, no `codemeta.json`, and no public archival release metadata were found in the repository root.

## Existing Artifacts and Results It Can Use

- `README.md`: artifact reproduction guide for the ACM CI framework paper.
- `Makefile`: build, run, campaign, validation, paper, and package targets.
- `src/main/java/congresssim`: Java 21 simulator source.
- `src/test/java`: Java test source.
- `reports/`: generated campaigns, diagnostics, validation screens, and summaries.
- `paper/acm-ci-framework/acm-ci-framework.pdf`: current main paper.
- `paper/technical-appendix/odd-d-appendix.pdf`: technical appendix and ODD+D documentation.
- `paper/pdf-manifest.json`: PDF freshness manifest.
- `scripts/checks`, `scripts/reporting`, `scripts/validation`, `paper/scripts`: checks, reports, validation, and figure generation scripts.
- `make test`, `make reproduce-paper-offline`, `make paper-checks`, `make supplement-anonymous`.

## Missing Experiments or Validation Needed Before Submission

This is mostly artifact work, not new scientific experiments:

- Add an explicit open-source license if the project will be submitted as reusable software.
- Add `CITATION.cff` and optionally `codemeta.json`.
- Add a public archival release plan, such as Zenodo or an equivalent DOI-bearing archive, if required by the target venue.
- Add command-line usage examples beyond paper reproduction.
- Add a short architecture/API guide for adding a new mechanism, metric, or campaign.
- Add deterministic-output tolerance notes for generated CSV/PDF artifacts.
- Confirm offline reproduction on a clean checkout.
- Confirm that anonymous-submission artifacts do not include strategy notes or stale drafts.

## Go/No-Go Recommendation

No-go for immediate software-paper submission. Go for artifact hardening.

After license/citation/release metadata and clean-checkout reproduction are complete, this could become the strongest breakout candidate.

## Next Concrete Commands or Repo Tasks

Baseline verification:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
```

Artifact hardening tasks:

1. Add `LICENSE`.
2. Add `CITATION.cff`.
3. Add optional `codemeta.json`.
4. Add `docs/architecture.md`.
5. Add `docs/adding-a-mechanism.md`.
6. Add a clean-checkout reproduction log.
7. Add release checklist for the chosen venue.
