# Voteview Member Context

This report derives a bounded actor-metadata join from cached Voteview roll-call rows and cached Voteview member metadata. It is a member-context inventory, not bill-level roll-call validation.

- Voteview member-context rows: 541
- Roll-call member-vote rows represented: 83636
- Member-context rows with Bioguide IDs: 541
- Roll-call member-vote rows with Bioguide member metadata: 83636
- Member-context rows with district metadata: 433

Claim boundary: this context attaches public Voteview member identifiers, Bioguide IDs, state/district metadata, and ideal-point fields to current roll-call rows. It does not join roll calls to bills, public laws, statutory sections, issue-specific public opinion, sponsor-effectiveness rows, or legislative outcomes, and it does not validate representation, welfare, public benefit, or model behavior.

Linkage statuses:
- voteview_member_metadata: 541

Chambers:
- House: 439
- Senate: 102

Parties:
- D: 264
- I: 3
- R: 274

| Member | Bioguide | Party | District | Roll-call rows | Missing links |
| --- | --- | --- | --- | ---: | --- |
| AGUILAR, Peter Rey | `A000371` | D | `CA-33` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| ALFORD, Mark | `A000379` | R | `MO-04` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| ALLEN, Rick W. | `A000372` | R | `GA-12` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| AMODEI, Mark E. | `A000369` | R | `NV-02` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| AUCHINCLOSS, Jake | `A000148` | D | `MA-04` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BALDERSON, Troy | `B001306` | R | `OH-12` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BALDWIN, Tammy | `B001230` | D | `WI` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BANKS, James E. | `B001299` | R | `IN-03` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BENTZ, Cliff | `B000668` | R | `OR-02` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BERA, Ami | `B001287` | D | `CA-06` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BICE, Stephanie I. | `B000740` | R | `OK-05` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BISHOP, Sanford Dixon, Jr. | `B000490` | D | `GA-02` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BLUMENTHAL, Richard | `B001277` | D | `CT` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BOOZMAN, John | `B001236` | R | `AR` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BOST, Mike | `B001295` | R | `IL-12` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BOWMAN, Jamaal | `B001223` | D | `NY-16` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BROWNLEY, Julia | `B001285` | D | `CA-26` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BUDZINSKI, Nikki | `B001315` | D | `IL-13` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BURCHETT, Timothy | `B001309` | R | `TN-02` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
| BURLISON, Eric | `B001316` | R | `MO-07` | 160 | roll_call_to_bill_or_action; public_law_or_statute; district_public_opinion_issue; sponsor_success_or_member_effectiveness; model_validation |
