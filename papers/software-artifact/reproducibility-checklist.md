# Reproducibility Checklist

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

## Current Verified Step

Current checkout:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
```

Observed:

```text
All simulator tests passed.
```

## Required Clean-Clone Audit

Run from outside the repository:

```sh
tmpdir=$(mktemp -d)
git clone /path/to/congress-institutional-simulator "$tmpdir/congress-institutional-simulator"
cd "$tmpdir/congress-institutional-simulator"
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
make test
make reproduce-paper-offline
make supplement-anonymous
git status --short
```

Record:

- command output;
- runtime;
- generated files;
- whether worktree is clean or expected generated artifacts changed;
- environment versions.

## Environment Checklist

- Java 21 on PATH.
- GNU Make.
- Python 3.
- LaTeX with `latexmk`.
- Required TeX packages documented in `paper/README.md`.
- No network required for core reproduction.
- Optional API-key workflows documented separately.

## Artifact Checklist

| Item | Required before software paper | Current status |
|---|---|---|
| `make test` passes | yes | pass in current checkout; clean clone not yet logged |
| `make reproduce-paper-offline` passes clean clone | yes | unverified |
| `make supplement-anonymous` passes clean clone | yes | current-checkout packager passed on 2026-07-27 after report-whitelist update; clean clone unverified |
| Fixed seeds documented | yes | pass for core Makefile campaigns and docs |
| PDF/text manifest check | yes | partial; `paper/pdf-manifest.json` exists, full check not rerun in clean clone |
| Output schema documented | yes | pass; `docs/output-schema.md` exists |
| Paired census and temporal result integrity | yes | pass in current checkout through `make govinfo-bill-census-check`; clean clone not yet logged |
| Source architecture documented | yes | pass; `docs/architecture.md` exists |
| Extension guide | yes | pass; `docs/adding-a-mechanism.md` and `docs/adding-a-campaign.md` exist |
| License | yes | fail; missing |
| Citation metadata | yes | pass; root `CITATION.cff` exists, with final DOI/version still pending release |
| Software metadata | yes | pass; root `codemeta.json` exists, with final DOI/license/version still pending release |
| Release/archive metadata | yes | partial; root `RELEASE.md` records the release checklist, but no tag, archive, DOI, or final release version exists |
| Anonymous bundle excludes notes/private files | yes | pass in current-checkout audit on 2026-07-27; archive contains newly whitelisted source-review reports and excludes identity-bearing public metadata, `papers/`, and private/planning folders; clean clone unverified |

## Reproducibility Claims Allowed Now

Allowed:

- The repository contains Makefile targets for build, test, campaign generation, paper checks, offline reproduction, and anonymous supplement creation.
- The current checkout test suite passes under Java 21.
- The root README documents no-network reproduction and optional network-dependent inputs.
- The committed paired GovInfo censuses and frozen temporal report have a deterministic integrity-check target.
- Root `CITATION.cff`, `codemeta.json`, and `RELEASE.md` now provide pre-release citation, software, and release-plan metadata.

Not allowed yet:

- The project is ready for software publication.
- A clean clone has been verified.
- The software is citable/releasable as an open-source artifact.
- The artifact has archival DOI metadata.

## Packaging Tasks

1. Choose and add `LICENSE`.
2. Add clean-clone reproduction log under a documented location.
3. Add clean-clone environment/dependency log.
4. Keep output schema documentation synchronized with report changes.
5. Keep extension documentation synchronized with catalog and process changes.
6. Run anonymous supplement audit.
7. After public release, update `CITATION.cff` and `codemeta.json` with final version, DOI/archive URL, release date, and chosen license.

## Stop Condition

Do not write a software-paper manuscript while any required checklist row is `fail` or `unverified`.
