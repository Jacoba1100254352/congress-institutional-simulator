# District Public Opinion Bill-Sponsor Metadata Linkage

Generated: 2026-07-05T05:34:38+00:00

Source:

- Cumulative CES district public-opinion aggregate from `district_public_opinion.csv`.
- Congress.gov bill/action metadata from `law_revision_bill_linkage.csv`.
- Congress.gov API v3 member endpoint for sponsor House district terms.
- API documentation: https://api.congress.gov/

Transformation:

- Reads public-law bill metadata rows with sponsor Bioguide IDs.
- Fetches Congress.gov member details and selects the House term matching the bill Congress.
- Joins House-sponsored public-law bills to CES district-opinion rows by congressional district ID.
- Retains public-opinion support, intensity, turnout, and affected-group-share fields as separate columns.
- Does not infer issue-specific bill support, MRP estimates, affected-group harm, member vote choice, constituent contact, or causal representation.

Rows:

- Linked district-opinion rows: 66.
- Unique district-opinion row keys: 63.
- Unique House-sponsored public-law bills linked: 22.
- Unique sponsor districts linked: 21.

Rows by issue:

- house_democratic_preference: 22
- house_representative_approval: 22
- presidential_democratic_preference: 22

Claim boundary:

This file links bounded CES district-opinion rows to House-sponsored public-law bill metadata by sponsor district. It provides district public-opinion context for bills but does not measure bill-topic support, issue-specific affected-group support or harm, representative responsiveness, welfare, or causal public-benefit validation.
