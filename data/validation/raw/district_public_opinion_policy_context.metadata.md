# District Public-Opinion Policy Context

Generated: 2026-07-05T12:33:21+00:00

Sources:

- District public-opinion bill-sponsor linkage: `data/validation/raw/district_public_opinion_linkage.csv`.
- Local Congress.gov policy-area topic throughput: `data/validation/raw/topic_throughput.csv`.

Transformation:

- Preserves one output row per cached sponsor-district public-law bill metadata row.
- Adds local topic-throughput counts when the linked bill policy area is present in the topic sample.
- Keeps support, turnout, intensity, and affected-group-share proxy fields separate from bill policy area.
- Does not infer issue-specific bill support, MRP estimates, affected-group harm, constituent contact, member vote choice, or causal representation.

Rows:

- Policy-context rows: 66.
- Rows with mapped policy-area topic context: 66.
- Unique district-opinion row keys: 63.
- Unique public-law bills: 22.
- Unique sponsor districts: 21.
- Unique policy areas: 11.

Rows by survey proxy:

- house_democratic_preference: 22
- house_representative_approval: 22
- presidential_democratic_preference: 22

Rows by policy area:

- Crime and Law Enforcement: 12
- Armed Forces and National Security: 9
- Economics and Public Finance: 9
- Commerce: 6
- Government Operations and Politics: 6
- International Affairs: 6
- Science, Technology, Communications: 6
- Civil Rights and Liberties, Minority Issues: 3
- Finance and Financial Sector: 3
- Immigration: 3
- Public Lands and Natural Resources: 3

Claim boundary:

Bounded Cumulative CES district aggregate to sponsor-district public-law bill policy-area context only; not bill-topic support, MRP or small-area estimation, issue-specific affected-group mapping or harm, representative responsiveness, public benefit, welfare, causal effect, or model validation.
