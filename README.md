# Reproducing the ACM CI Framework Paper

This repository contains the Congress Institutional Simulator, a Java 21
comparative institutional-design simulator, plus the ACM Collective
Intelligence framework manuscript and ODD+D appendix generated from it.

The submitted paper is a framework and stress-test artifact. It compares
selected legislative mechanism bundles under shared synthetic worlds and reports
diagnostics for productivity, revision moderation, generated public support,
risk, administrative cost, and generated public benefit. The results are
synthetic design hypotheses, not empirical rankings of real legislatures.

## Requirements

- Java 21 on `PATH`
- GNU Make
- Python 3 for report and figure-generation scripts
- LaTeX with `latexmk` for rebuilding the PDFs

On macOS, set Java 21 explicitly when needed:

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```

The paper workspace vendors the ACM class files used by the review build. With a
minimal TeX Live Basic install, see [paper/README.md](paper/README.md) for the
extra LaTeX packages that may be needed.

## Quick Smoke Test

```sh
make test
```

Expected runtime: under one minute on the authoring workstation.

Expected result: Java sources compile and the simulator test suite passes.

## Full Offline Reproduction

```sh
make reproduce-paper-offline
```

Expected runtime: several minutes on the authoring workstation.

This no-network target regenerates:

- `reports/simulation-campaign-v21-paper.csv`
- `reports/simulation-campaign-v21-paper.md`
- `reports/simulation-campaign-v21-paper-manifest.json`
- generated diagnostic reports under `reports/`
- generated LaTeX tables and figures under `paper/figures/`
- `paper/acm-ci-framework/acm-ci-framework.pdf`
- `paper/technical-appendix/odd-d-appendix.pdf`
- `paper/pdf-manifest.json`

The workflow uses fixed seeds. Reproduced CSV values and PDF extracted-text
hashes should match `paper/pdf-manifest.json` within the tracked manifest
checks.

## Paper Checks

Before treating paper-facing output as ready, run:

```sh
make paper-checks
```

This runs the paper workflow plus word-count, anonymity, figure-label,
table/figure-consistency, PDF-render, and PDF-manifest checks.

GitHub Actions uses:

```sh
make github-ci
```

Local full CI uses:

```sh
make ci
```

## Optional Network-Dependent Inputs

The offline reproduction path does not require API keys or live network access.
Optional empirical sample rebuilds are separate:

```sh
make fetch-validation-samples
make build-bill-progression-raw
make build-core-raw-validation
```

Some optional rebuilds may require public data access or API credentials. They
are useful for refreshing empirical flow sanity checks, but they are not part of
the no-network artifact reproduction path.

## Main Paper Files

- Main ACM manuscript: [paper/acm-ci-framework/acm-ci-framework.tex](paper/acm-ci-framework/acm-ci-framework.tex)
- Main ACM PDF: [paper/acm-ci-framework/acm-ci-framework.pdf](paper/acm-ci-framework/acm-ci-framework.pdf)
- ODD+D appendix source: [paper/technical-appendix/odd-d-appendix.tex](paper/technical-appendix/odd-d-appendix.tex)
- ODD+D appendix PDF: [paper/technical-appendix/odd-d-appendix.pdf](paper/technical-appendix/odd-d-appendix.pdf)
- Paper build notes: [paper/README.md](paper/README.md)
- Simulator usage reference: [docs/usage.md](docs/usage.md)
- Empirical-boundary notes: [docs/calibration.md](docs/calibration.md)

Publication-strategy notes are kept under `paper/notes/` for project planning
and are excluded from the anonymous supplement.

## Anonymous Supplement

Build the double-blind artifact bundle with:

```sh
make supplement-anonymous
```

This writes:

- `dist/anonymous-supplement/congress-institutional-simulator-anonymous/`
- `dist/congress-institutional-simulator-anonymous.zip`

The supplement builder excludes local build products, private local files,
project-planning notes, and identity-bearing paths. It writes its own
reviewer-facing README inside the supplement.

## Extended Documentation

Use [docs/usage.md](docs/usage.md) for the full simulator command reference,
historical campaign targets, scenario keys, and metric glossary.
