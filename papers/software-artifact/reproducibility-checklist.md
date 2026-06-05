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
git clone /Users/jacobanderson/Documents/simulators/Congress\ Institutional\ Simulator "$tmpdir/congress-institutional-simulator"
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
| `make supplement-anonymous` passes clean clone | yes | unverified |
| Fixed seeds documented | yes | pass for core Makefile campaigns and docs |
| PDF/text manifest check | yes | partial; `paper/pdf-manifest.json` exists, full check not rerun in clean clone |
| Output schema documented | yes | fail; missing dedicated `docs/output-schema.md` |
| Source architecture documented | yes | partial; ODD docs exist, missing `docs/architecture.md` |
| Extension guide | yes | fail; missing adding-mechanism/campaign docs |
| License | yes | fail; missing |
| Citation metadata | yes | fail; missing |
| Release/archive metadata | yes | fail; missing |
| Anonymous bundle excludes notes/private files | yes | unverified; builder exists but bundle needs audit |

## Reproducibility Claims Allowed Now

Allowed:

- The repository contains Makefile targets for build, test, campaign generation, paper checks, offline reproduction, and anonymous supplement creation.
- The current checkout test suite passes under Java 21.
- The root README documents no-network reproduction and optional network-dependent inputs.

Not allowed yet:

- The project is ready for software publication.
- A clean clone has been verified.
- The software is citable/releasable as an open-source artifact.
- The artifact has archival DOI metadata.

## Packaging Tasks

1. Add `LICENSE`.
2. Add `CITATION.cff`.
3. Add optional `codemeta.json`.
4. Add clean-clone reproduction log under a documented location.
5. Add environment/dependency manifest.
6. Add output schema documentation.
7. Add extension documentation.
8. Run anonymous supplement audit.

## Stop Condition

Do not write a software-paper manuscript while any required checklist row is `fail` or `unverified`.
