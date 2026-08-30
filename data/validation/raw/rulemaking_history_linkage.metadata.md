# Rulemaking History Linkage

Generated: 2026-07-05T09:40:58+00:00

Source:

- Federal Register API v1 search and single-document endpoints.
- API documentation: https://www.federalregister.gov/reader-aids/developer-resources/rest-api
- Input authority linkage file: `data/validation/raw/rulemaking_authority_linkage.csv`.
- Row limit: all authority-matched final rules.

Transformation:

- Starts from final-rule documents already text-verified as citing cached public laws in the rulemaking authority linkage cache.
- Fetches each final rule's Federal Register detail record.
- Searches proposed-rule documents by the final rule's RIN and docket identifiers.
- Keeps proposed-rule candidates only when their Federal Register metadata shares a normalized RIN or docket identifier with the final rule and the proposed-rule publication date is not later than the final rule publication date.
- Does not fetch complete Regulations.gov comment records, Unified Agenda stages, enforcement outcomes, appropriations data, or nonpublic submitter information.

Rows:

- Authority-matched final-rule rows checked: 51.
- Unique final-rule documents checked: 50.
- Final-rule rows with proposed-rule history matches: 23.
- Candidate proposed-rule documents inspected: 176.
- Matched proposed-rule links: 36.
- Unique matched proposed-rule documents: 36.

History statuses:

- no_proposed_rule_history_match: 28
- proposed_rule_history_match: 23

Claim boundary:

Bounded Federal Register proposed-rule search for final rules already text-verified as citing cached public laws; matches require shared RIN or docket identifiers and do not prove complete public-comment records, Unified Agenda stage coverage, enforcement outcomes, appropriations capacity, exhaustive implementation coverage, public benefit, welfare, causal effects, or model validation.
