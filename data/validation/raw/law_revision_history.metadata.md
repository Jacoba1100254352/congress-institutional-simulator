# Law Revision History Raw Validation Dataset

Generated: 2026-07-02T19:53:45+00:00

Source:

- Congress.gov API v3 law-list, bill-summary, and bill-title endpoints.
- API documentation: https://api.congress.gov/
- Congresses sampled: 117,118.
- Maximum public laws per Congress: 60.
- API key: provided key, not recorded.

Transformation:

- Unit of observation is an enacted public law.
- `law_id` and `public_law_number` use the Congress.gov public-law number when available.
- `enacted_date` is the public-law action date from the Congress.gov law-list endpoint.
- `policy_area` is currently `Unclassified` because the builder avoids per-bill detail calls to keep the source refresh bounded.
- Revision flags are text-derived indicators from enacted-law titles and CRS summaries: amendment, reauthorization or extension, repeal, and sunset/expiration language.
- `invalidated` is fixed at `0` because Congress.gov law titles and summaries are not a judicial-invalidation source; the SCDB court-review extract is the current invalidation proxy.

Rows:

- Normalized rows: 120
- Amendment-text rows: 36
- Reauthorization/extension-text rows: 20
- Repeal-text rows: 8
- Sunset/expiration-text rows: 6
- Invalidation-text rows: 0

Claim boundary:

This file supports a bounded statutory revision-activity proxy for public laws whose titles or summaries mention amendment, reauthorization, repeal, or sunset/expiration language. It does not provide longitudinal lineage for every target statute, observed expiration outcomes, codified-text diffs, OLRC notes, or later judicial invalidation.
