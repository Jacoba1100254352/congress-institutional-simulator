# Empirical Boundary Report

This report separates what the paper can inspect empirically from what remains a synthetic or speculative model component. It is generated from the validation-readiness and empirical-check artifacts.

- Raw validation inputs available: 6 / 12
- Raw validation inputs missing or incomplete: 6 / 12
- Highest-priority missing areas: Public support, Campaign finance, Implementation feedback, Law revision

| Area | Dataset | Input status | Paper status | Priority | Boundary for claims | Next source family |
| --- | --- | --- | --- | --- | --- | --- |
| Roll-call behavior | `voteview_rollcalls.csv` | ready | empirical check | available | Party-unity and coalition-size proxies are inspectable. | Extend Voteview coverage across more Congresses and chambers. |
| Bill progression | `bill_progression.csv` | ready | empirical check | available | Floor load, committee reporting, and enactment-rate proxies are inspectable. | Replace the bounded sample with a full Congress.gov/govinfo bill census. |
| Lobbying disclosure | `lobbying_disclosure.csv` | ready | empirical check | available | Lobby-spend concentration is inspectable, but not yet tied to bill-level outcomes. | Link LDA clients/issues to bill topics and committee referrals. |
| Topic throughput | `topic_throughput.csv` | ready | empirical check | available | Agenda diversity and topic enactment proxies are inspectable. | Map topics to CAP/congressional subject taxonomies across sessions. |
| Sponsor access | `sponsor_success.csv` | ready | empirical check | available | Proposal-access concentration is inspectable with a rough sponsor sample. | Replace with CEL-style sponsor effectiveness or complete sponsor histories. |
| Public support | `district_public_opinion.csv` | missing | synthetic only | high | District public-will and affected-group legitimacy remain synthetic. | Add district-level MRP/CCES-style opinion, turnout, and affected-population estimates. |
| Committee gatekeeping | `committee_activity.csv` | ready | empirical check | available | Reporting and referral proxies are inspectable; hearings remain rough. | Add committee hearing calendars, markup records, amendments, and discharge petitions. |
| Campaign finance | `campaign_finance.csv` | missing | synthetic only | high | Money-in-politics effects remain represented by lobbying proxies. | Add FEC/OpenFEC receipts, independent expenditures, and industry classifications. |
| Court review | `court_review.csv` | missing | synthetic only | medium | Judicial-review and emergency-docket behavior remain speculative prototypes. | Add Supreme Court Database/emergency-order coding and invalidation outcomes. |
| Implementation feedback | `rulemaking_implementation.csv` | missing | synthetic only | high | Implementation delay, nonenforcement, and capacity feedback remain synthetic. | Add Federal Register, Unified Agenda, Regulations.gov, and agency enforcement rows. |
| Law revision | `law_revision_history.csv` | missing | synthetic only | high | Law-registry correction and sunset dynamics remain synthetic. | Add statutory lineage for amendment, reauthorization, repeal, expiration, and invalidation. |
| Comparative institutions | `comparative_institutions.csv` | missing | synthetic only | medium | Chamber and party-system breadth is a sensitivity analysis, not cross-national fit. | Add ParlGov, V-Dem, IPU/chamber data, electoral systems, and productivity proxies. |
