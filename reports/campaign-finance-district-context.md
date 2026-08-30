# Campaign-Finance District Context

This report derives a bounded district-context join from cached OpenFEC recipient metadata and cached district public-opinion aggregates. It is an evidence inventory, not bill-level influence validation.

- FEC recipient metadata rows inspected: 32
- Candidate metadata rows inspected: 24
- Campaign-finance transaction rows represented: 194
- House candidate-recipient rows with district public-opinion context: 7
- Campaign-finance transaction rows with House district context: 23
- District public-opinion context rows attached: 21
- Sponsor-district public-law metadata rows sharing those House districts: 0

Claim boundary: the joined House-candidate subset adds district-level public-opinion context to public FEC recipient metadata. It does not identify a sitting sponsor, bill, committee of jurisdiction, issue topic, legislative outcome, causal influence, capture, public benefit, or model validation.

Context statuses:
- candidate_metadata_without_house_district_context: 17
- committee_metadata_without_house_district_context: 8
- house_candidate_district_public_opinion_context: 7

| Recipient | Candidate | District | Transactions | Outside amount | District opinion rows | Sponsor-law rows | Missing links |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `H0IL15129` | MILLER, MARY | `IL-15` | 1 | 60.39 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2IL02172` | KELLY, ROBIN | `IL-02` | 1 | 60.35 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2IL10068` | SCHNEIDER, BRADLEY S. | `IL-10` | 1 | 60.39 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2PA01099` | EHASZ, ASHLEY | `PA-01` | 7 | 326.56 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2PA17103` | DELUZIO, CHRISTOPHER | `PA-17` | 7 | 398.78 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H4IL12060` | BOST, MICHAEL | `IL-12` | 1 | 60.39 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H8PA15229` | WILD, SUSAN | `PA-07` | 5 | 415.22 | 3 | 0 | candidate_to_sitting_member_or_sponsor; bill_id_or_issue_topic; committee_of_jurisdiction; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
