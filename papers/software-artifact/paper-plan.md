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

The repository has strong reproduction infrastructure plus root `CITATION.cff`, `codemeta.json`, and `RELEASE.md` metadata scaffolding. It still has no chosen license, no clean-checkout reproduction log, and no public archival release or DOI metadata.

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
- `docs/architecture.md`, `docs/output-schema.md`, `docs/adding-a-mechanism.md`, `docs/adding-a-campaign.md`, and `docs/reproducibility.md`: software-facing artifact docs.

## Missing Experiments or Validation Needed Before Submission

This is mostly artifact work, not new scientific experiments:

- Add an explicit open-source license if the project will be submitted as reusable software.
- Update `CITATION.cff` and `codemeta.json` with final version, license, release date, and DOI/archive fields after release.
- Complete a public archival release, such as Zenodo or an equivalent DOI-bearing archive, if required by the target venue.
- Keep command-line usage examples and software-facing docs synchronized with Makefile and scenario-catalog changes.
- Confirm offline reproduction on a clean checkout.
- Confirm that anonymous-submission artifacts do not include strategy notes or stale drafts.

## Go/No-Go Recommendation

No-go for immediate software-paper submission. Go for artifact hardening.

After license choice, final citation/release metadata, archival release, and clean-checkout reproduction are complete, this could become the strongest breakout candidate.

See `go-no-go.md` for the strict full-draft conditions.

## Next Concrete Commands or Repo Tasks

Baseline verification:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
```

Artifact hardening tasks:

1. Choose and add `LICENSE`.
2. Add a clean-checkout reproduction log.
3. Archive a tagged release after clean-checkout reproduction passes.
4. Update `CITATION.cff` and `codemeta.json` with final release fields.
5. Audit the public and anonymous artifact bundles for stale/private files.
