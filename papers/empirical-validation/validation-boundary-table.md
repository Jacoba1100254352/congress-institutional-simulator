# Validation Boundary Table

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

## Claim Boundary Table

| Claim area | Current category | Current evidence | What would upgrade it |
|---|---|---|---|
| Bill attrition / enactment rate | sanity-checkable | `reports/calibration-baseline.md`; `reports/empirical-bridge.md` | Fuller Congress.gov/govinfo bill census and held-out checks. |
| Floor consideration | sanity-checkable | bill progression summary and calibration range | Full floor-action histories and held-out checks. |
| Committee reporting | sanity-checkable / proxy only | `committee_activity.csv` and bill progression report rate | Hearing, markup, amendment, referral, discharge records. |
| Roll-call coalition behavior | proxy only | Voteview coalition size and party unity | Chamber/party behavior calibration separated from public support. |
| Sponsor access concentration | sanity-checkable / proxy only | sponsor introduction Gini and proposer access Gini | Complete sponsor histories and CEL-style effectiveness measures. |
| Lobby spending observability | proxy only | LDA summary, mean spend, client Gini, issue entropy | Bill-linked LDA/topic/committee matching and influence design. |
| Topic throughput | proxy only | CAP/topic summary and topic enactment rate | Stable topic mapping across sessions and issue-domain calibration. |
| Public support | synthetic only | no district public opinion input | District-level public opinion and issue mapping. |
| Affected-group harm/support | synthetic only | no affected-group empirical input | Affected-population estimates and issue-domain harm mapping. |
| Campaign finance influence | synthetic only | no OpenFEC/FEC input | Candidate/committee/outside-spending linkage to bills, sponsors, and issues. |
| Court review / invalidation | synthetic only | no court-review input | SCDB/invalidation/emergency-order data. |
| Implementation feedback | synthetic only | no rulemaking/enforcement input | Federal Register, Unified Agenda, Regulations.gov, and enforcement data. |
| Law revision / correction over time | synthetic only | no statutory lineage input | amendment, reauthorization, repeal, sunset, expiration, and invalidation lineage. |
| Comparative party/chamber systems | synthetic only | no comparative-institution input | ParlGov/V-Dem/IPU/chamber productivity data. |
| Generated public benefit / welfare | synthetic only | internal generator quantity | No simple direct validation; needs proxy design and strong caveats. |
| Revision moderation | synthetic only | simulator diagnostic | Operationalize against observed amendment/bargaining data before validation. |
| Administrative cost | synthetic/proxy only | procedural-load index | Process-time, staff/load, delay, review, and implementation burden proxies. |

## Validation-Readiness Scorecard

| Dimension | Current status | Score | Reason |
|---|---|---:|---|
| Raw input coverage | partial | 2 / 5 | 6 / 12 optional raw inputs are ready. |
| Flow sanity checks | usable | 3 / 5 | 7 / 7 current calibration checks pass, but ranges are broad. |
| Public support data | missing | 0 / 5 | District opinion and affected-group support are absent. |
| Lobbying/campaign finance linkage | weak | 1 / 5 | LDA summaries exist; OpenFEC and bill linkage are missing. |
| Committee process data | partial | 2 / 5 | Reporting/referral proxies exist; hearings/markups/amendments are thin. |
| Court/review data | missing | 0 / 5 | Court review and invalidation inputs are absent. |
| Implementation/correction data | missing | 0 / 5 | Rulemaking, enforcement, law revision, sunset, and repeal inputs are absent. |
| Comparative institution data | missing | 0 / 5 | Cross-national party/chamber data is absent. |
| Reproducible offline summaries | partial | 3 / 5 | Current summaries exist; future source caches and manifests need expansion. |
| Held-out validation design | not implemented | 0 / 5 | Current checks are calibration/sanity screens, not held-out validation. |

Overall readiness: benchmark-readiness pilot, not validation paper.

## Missing-Data Roadmap

Priority 1:

- district-level public opinion / MRP / CCES-style sources;
- campaign finance / OpenFEC;
- lobbying-to-bill/topic/committee linkage;
- implementation feedback from Federal Register, Unified Agenda, Regulations.gov, and enforcement sources;
- statutory amendment, repeal, sunset, reauthorization, and expiration lineage.

Priority 2:

- court review, emergency docket, and invalidation data;
- committee hearings, markups, amendments, discharge petitions;
- complete sponsor effectiveness and sponsor history data;
- broader Congress.gov/govinfo bill/action census.

Priority 3:

- ParlGov or cross-national party-system data;
- V-Dem/IPU/chamber structure data;
- comparative legislative productivity and bicameral disagreement signals.

## Prohibited Claims Until Upgraded

- The simulator is empirically validated.
- The simulator validates public support or public benefit.
- Lobby spending validates capture.
- Voteview coalition size validates public opinion.
- Flow sanity checks validate mechanism rankings.
- Synthetic welfare or harm metrics are empirical.
