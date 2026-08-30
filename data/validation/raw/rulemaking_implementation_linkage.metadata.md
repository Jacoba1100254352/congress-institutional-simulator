# Rulemaking Implementation Metadata Linkage

Generated: 2026-07-05T05:10:55+00:00

Source:

- Federal Register API v1 single-document endpoint.
- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api
- Input rulemaking file: `data/validation/raw/rulemaking_implementation.csv`.
- Row limit: all.

Transformation:

- Reads Federal Register final-rule rows from the cached implementation dataset.
- Fetches document-level public metadata by Federal Register document number.
- Retains docket IDs, RINs, CFR references, agency identifiers, topics, page length, significant-rule flag, and Federal Register-exposed Regulations.gov docket/comment metadata when present.
- Does not fetch full rule text, proposed-rule histories, public-law authorities, enforcement outcomes, appropriations records, or private comment submitter fields.

Rows:

- Unique final-rule document rows: 500.
- Rows with Federal Register document metadata: 495.
- Rows with Federal Register-exposed Regulations.gov document or docket IDs: 479.
- Rows with Federal Register-exposed Regulations.gov comment counts: 467.
- Rows with CFR references: 497.
- Linkage share: 0.990.

Linkage statuses:

- api_error: 5
- federal_register_document_metadata: 495

Claim boundary:

This file links bounded final-rule rows to official Federal Register document metadata and, when exposed by Federal Register, Regulations.gov docket, document, and comment-count metadata. It does not provide public-law or U.S. Code authority linkage, proposed-to-final rule histories, complete Regulations.gov comment records, enforcement outcomes, appropriations capacity, or observed nonenforcement.
