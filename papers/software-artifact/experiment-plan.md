# Artifact Hardening Plan

This candidate needs artifact work more than scientific experiments.

## Baseline Verification

Run on the current checkout:

```sh
make test
make reproduce-paper-offline
make supplement-anonymous
```

Record:

- OS and hardware.
- Java version.
- Make version.
- Python version.
- LaTeX version.
- Runtime for each command.
- Changed files after reproduction.

## Clean-Checkout Verification

Tasks:

- Clone the repository into a temporary directory.
- Run the baseline verification commands.
- Compare generated CSV summaries and PDF manifest behavior.
- Record any dependency or path assumptions.

## Metadata Work

Add:

- `LICENSE`
- `CITATION.cff`
- optional `codemeta.json`
- release checklist
- artifact bundle checklist

## Documentation Work

Add:

- `docs/architecture.md`: major packages and data flow.
- `docs/adding-a-mechanism.md`: how to add a new institutional mechanism.
- `docs/adding-a-campaign.md`: how to add a new campaign or scenario family.
- `docs/output-schema.md`: key CSV columns and metrics.
- `docs/reproducibility.md`: deterministic seeds, output tolerances, network-dependent targets.

## Testing Work

- Add smoke tests for key command-line paths if not already covered.
- Add checks that generated reports have expected columns.
- Add a target that runs without LaTeX for reviewers who only need source/report reproduction.
- Add CI configuration only if public hosting is planned.

## Release Work

- Choose target venue and license.
- Create a tagged release.
- Archive release to a DOI-bearing service if required.
- Ensure anonymous artifact bundle excludes strategy notes, stale PDFs, and local metadata.

## Proposed Make Targets

```make
artifact-smoke
artifact-offline-check
artifact-schema-check
artifact-release-check
```
