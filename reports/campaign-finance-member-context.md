# Campaign-Finance Member Context

This report derives a bounded candidate-to-member context join from cached public FEC recipient metadata and cached Voteview member metadata. It is an evidence inventory, not bill-level influence validation.

- FEC recipient metadata rows inspected: 32
- Candidate metadata rows inspected: 24
- Candidate rows with Voteview member context: 15
- Campaign-finance transaction rows with Voteview member context: 30
- Unique Voteview/Bioguide members linked: 15

Claim boundary: the joined candidate subset adds public Voteview member context to public FEC recipient metadata when candidate name, chamber, state, and district evidence agree. It does not identify bill-level influence, sponsor effectiveness, committee of jurisdiction, issue targeting, legislative outcome, causal influence, capture, public benefit, private contributor details, or model validation.

Member-context statuses:
- candidate_metadata_noncongressional_office: 4
- candidate_voteview_member_context: 15
- candidate_without_voteview_member_match: 5
- recipient_without_candidate_metadata: 8

| Recipient | Candidate | Member | Chamber | District/state | Transactions | Match basis | Missing links |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `H0IL15129` | MILLER, MARY | MILLER, Mary E. (`M001211`) | House | `IL-15` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2IL02172` | KELLY, ROBIN | KELLY, Robin L. (`K000385`) | House | `IL-02` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2IL10068` | SCHNEIDER, BRADLEY S. | SCHNEIDER, Brad (`S001190`) | House | `IL-10` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H2PA17103` | DELUZIO, CHRISTOPHER | DELUZIO, Chris (`D000530`) | House | `PA-17` | 7 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H4IL12060` | BOST, MICHAEL | BOST, Mike (`B001295`) | House | `IL-12` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `H8PA15229` | WILD, SUSAN | WILD, Susan (`W000826`) | House | `PA-07` | 5 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S0AL00230` | TUBERVILLE, THOMAS H | TUBERVILLE, Thomas Hawley (Tommy) (`T000278`) | Senate | `AL` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S0KY00156` | PAUL, RAND | PAUL, Rand (`P000603`) | Senate | `KY` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S0UT00165` | LEE, MIKE | LEE, Mike (`L000577`) | Senate | `UT` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S0WI00197` | JOHNSON, RON HAROLD MR. | JOHNSON, Ron (`J000293`) | Senate | `WI` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S2MO00544` | SCHMITT, ERIC | SCHMITT, Eric Stephen (`S001227`) | Senate | `MO` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S2OH00436` | VANCE, J D | VANCE, James David (`V000137`) | Senate | `OH` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S2TX00312` | CRUZ, RAFAEL EDWARD TED | CRUZ, Rafael Edward (Ted) (`C001098`) | Senate | `TX` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S6PA00217` | CASEY, ROBERT P. JR. | CASEY, Robert (Bob), Jr. (`C001070`) | Senate | `PA` | 6 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
| `S8FL00273` | SCOTT, RICK SEN | SCOTT, Richard Lynn (Rick) (`S001217`) | Senate | `FL` | 1 | candidate_name_state_district_voteview_member_match | bill_id_or_issue_topic; committee_of_jurisdiction; outside_spending_target; legislative_outcome_or_public_law; causal_influence_or_capture_validation |
