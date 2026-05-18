# Software Paper Plan

Final decision: NEEDS REPRODUCIBILITY AND PACKAGING AUDIT FIRST.

## Working Title

Congress Institutional Simulator: A Reproducible Java Toolkit for Legislative Mechanism Stress Tests

## Target Venue Category

Software paper, model-description paper, software artifact track, JOSS-style software note, SoftwareX-style software article, or computational social science model-documentation venue.

## Software Contribution Statement

The Congress Institutional Simulator is a Java 21, Makefile-driven simulation toolkit for comparing synthetic legislative mechanism bundles under shared generated political worlds. It lets researchers route the same legislator, lobby, bill, and status-quo environment through alternative agenda, committee, chamber, voting, lobbying, review, bargaining, public-input, and accountability modules, then reports reproducible diagnostics about productivity, support, risk, administrative cost, revision, capture, harm, and correction.

## Who Can Use It

Potential users:

- computational social scientists studying institutional mechanisms;
- political methodologists prototyping legislative simulation designs;
- collective-intelligence researchers comparing group decision architectures;
- governance researchers needing reproducible mechanism stress tests;
- instructors or students studying agenda control, voting thresholds, committees, lobbying, and institutional tradeoffs.

## Supported Mechanism Families

The codebase currently includes modules for:

- voting thresholds and default passage;
- proposal access and agenda gates;
- leadership, open floor, lottery, attention, and challenge processes;
- committee gatekeeping, information, assignment, and power;
- unicameral, bicameral, veto, conference, and chamber-routing structures;
- lobbying, influence, audit, transparency, and anti-capture processes;
- mediation, package bargaining, alternatives, and amendment tournaments;
- distributional harm, compensation, affected-group scoring;
- citizen panels, petitions, initiatives, and objection windows;
- law registry, sunset, proposal bonds, credits, and eligibility filters;
- review bodies, ex ante review, judicial review, and independent institution bundles;
- proposer/lobby adaptation and strategy wrappers.

## Outputs Produced

The artifact produces:

- campaign CSVs and Markdown summaries under `reports/`;
- empirical-readiness and calibration reports;
- ablation and manipulation-stress summaries;
- chamber-structure reports;
- seed-robustness summaries;
- LaTeX tables and figures under `paper/figures/`;
- ACM manuscript and ODD+D appendix PDFs;
- PDF freshness manifest;
- anonymous supplement bundle.

## What It Does Not Claim

- It does not validate a model of Congress.
- It does not forecast real legislative outcomes.
- It does not prove any mechanism is generally superior.
- It does not turn synthetic public benefit, harm, support, or capture metrics into empirical facts.
- It does not yet provide a packaged public software release with license, citation metadata, and archived DOI.

## Current Go/No-Go

No-go for full software paper draft.

Go for artifact hardening:

- license and citation metadata;
- clean-clone reproduction;
- package/module documentation;
- output schema documentation;
- extension guides;
- public release checklist.

## Required New Documentation Before Draft

- `docs/architecture.md`
- `docs/adding-a-mechanism.md`
- `docs/adding-a-campaign.md`
- `docs/output-schema.md`
- `docs/reproducibility.md`
- `LICENSE`
- `CITATION.cff`
- optional `codemeta.json`

## Paper Draft Gate

Only draft after:

- clean clone passes `make test`;
- clean clone passes `make reproduce-paper-offline`;
- anonymous supplement builds and excludes planning/private files;
- license/citation metadata exist;
- architecture and extension docs exist;
- dependency/environment requirements are documented;
- stale drafts and local generated artifacts are absent from release bundle.
