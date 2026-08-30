# Release Checklist

Status: pre-release metadata scaffold. This repository is not yet a citable archived release.

## Current Candidate

- Candidate version: `0.1.0-dev`
- Release target: first public software/artifact release after manuscript review or repository unmasking
- Repository: `https://github.com/Jacoba1100254352/congress-institutional-simulator`
- Citation metadata: `CITATION.cff`
- Software metadata: `codemeta.json`

## Required Before Public Release

1. Choose and add a project license in a root `LICENSE` file.
2. Run a clean-clone reproduction audit:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
git status --short
```

3. Save the clean-clone command log and environment versions.
4. Confirm the anonymous supplement excludes identity-bearing and planning/private files.
5. Create a version tag after the clean-clone audit passes.
6. Archive the release, record the DOI, and update `CITATION.cff` and `codemeta.json` with final release metadata.

## Public Artifact Contents

The public release should include source code, Makefile workflows, Java 21 and reproduction docs, generated validation/source-boundary reports, paper-facing figures/tables, the ACM framework manuscript, the ODD+D appendix, citation metadata, software metadata, license metadata, and release/archive metadata.

## Anonymous Review Boundary

Identity-bearing public metadata such as `CITATION.cff`, `codemeta.json`, and this release checklist should remain outside the anonymous supplement until review unmasking or public release packaging.
