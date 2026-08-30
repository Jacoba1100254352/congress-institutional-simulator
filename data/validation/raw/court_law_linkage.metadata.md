# Court-Law Linkage Raw Dataset

Generated: 2026-07-05

Inputs:

- `data/validation/raw/court_review.csv`
- `data/validation/raw/rulemaking_authority_linkage.csv`

Transformation:

- Parses U.S.C. title-section citations from SCDB `law_minor` / `usc_sections` fields.
- Parses U.S.C. title-section citations from Federal Register authority-search `usc_citations` fields.
- Marks a court row as `usc_section_authority_overlap` only when a normalized U.S.C. section appears in both places.
- Keeps unmatched SCDB rows in the output so the denominator remains explicit.

Rows:

- SCDB court rows checked: 9341
- Court rows with parsed U.S.C. sections: 1328
- Court rows with authority-section overlaps: 26
- Public-law rows overlapped by at least one court U.S.C. section: 9
- Bill IDs overlapped by at least one court U.S.C. section: 9
- Unique matched U.S.C. sections: 12

Claim boundary:

Bounded metadata overlap between SCDB lawMinor U.S.C. citations and Federal Register authority U.S.C. citations attached to cached public-law rows; not proof that the case challenged or invalidated the listed public law, bill, agency implementation chain, or rule, and not emergency-order, lower-court, welfare, causal-effect, or model validation evidence.
