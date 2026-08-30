# Court Review Raw Validation Dataset

Generated: 2026-07-05

Source:

- Supreme Court Database, 2025 Release 01.
- Release page: https://scdb.la.psu.edu/data/2025-release-01/
- Download URL used: https://scdb.la.psu.edu/?jet_download=ed98e2f718f46e42eddeb8d7724c77f61c84fc89
- Source CSV inside archive: `SCDB_2025_01_caseCentered_Citation.csv`.

Transformation:

- Included SCDB terms: 1946-2024.
- Unit of observation: SCDB case-centered row organized by Supreme Court citation.
- `invalidated` is `1` when `declarationUncon` is 2, 3, or 4; `declarationUncon=1` is no declaration of unconstitutionality.
- `signed_opinion` is `1` when `decisionType=1`, SCDB's signed-opinion category.
- `vote_margin` is `majVotes - minVotes` with a floor at 0.
- `emergency_order` is fixed at `0` because this SCDB case-centered release covers merits decisions, not a separately coded emergency or shadow-docket dataset.
- `law_type`, `law_supp`, and `law_minor` preserve SCDB legal-authority fields for bounded statute-linkage audits.
- `usc_sections` normalizes U.S. Code citations found in `lawMinor`; blank values mean no U.S.C. citation was parsed from the SCDB row.

Rows:

- Normalized rows: 9341
- Invalidated rows: 671
- Signed-opinion rows: 7323
- Rows with parsed U.S.C. sections: 1328
- Unique parsed U.S.C. sections: 711

Claim boundary:

This file supports a merits-case court-review bridge for invalidation, vote-margin, signed-opinion, and bounded legal-authority metadata. Parsed U.S.C. sections are not direct public-law, bill, lower-court, emergency-order, implementation-effect, welfare, or model validation evidence.
