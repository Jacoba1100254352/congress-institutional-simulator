# Comparative Institution Linkage Dataset

Generated: 2026-07-05T11:22:30+00:00

Sources:

- `data/validation/raw/comparative_institutions.csv`.
- Existing simulator scenario-family keys used as metadata anchors.

Transformation:

- Country-year rows are classified into chamber, district-magnitude, party-system, judicial-review, and legislative-constraint bands.
- Bands are mapped to a bounded set of simulator scenario keys that represent nearby institutional mechanisms.
- `legislative_constraint_proxy` carries the existing V-Dem legislative-constraints proxy; it is not observed law-output productivity.

Rows:

- Source comparative rows read: 130
- Linkage rows written: 130
- Countries represented: 130
- Unique simulator scenario anchors: 14

Linkage statuses:
- comparative_institution_metadata: 130

Chamber anchors:
- bicameral: 31
- no_effective_chamber: 10
- unicameral: 89

Claim boundary:

Bounded comparative-institution profile to simulator scenario-family metadata only; not observed law-output productivity, not bicameral disagreement evidence, not country-level institutional fit, not adoption evidence, not welfare, causal-effect, or model validation evidence.
