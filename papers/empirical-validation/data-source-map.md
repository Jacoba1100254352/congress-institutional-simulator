# Data Source Map

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

This map inventories empirical signals that can calibrate, sanity-check, or eventually validate legislative simulation models. Status reflects current repository artifacts, especially `reports/empirical-validation-readiness.md`, `reports/empirical-validation-summary.md`, `reports/empirical-bridge.md`, and `reports/empirical-validation-gap-report.md`.

## Source Inventory

| Source family | Empirical signal | Current repo dataset or report | Current status | Simulator metric/proxy | Boundary |
|---|---|---|---|---|---|
| Congress.gov bill histories | introduction, floor action, committee reporting, enactment, sponsor/action histories | `bill_progression.csv`; `reports/core-raw-validation-build.md`; `reports/empirical-bridge.md` | ready as bounded sample | productivity, floor load, committee reporting, enactment rate | sanity-checkable flow only |
| govinfo bill/action records | BILLSTATUS/action histories and bill progression | referenced in `reports/calibration-baseline.md` | partial/bounded | productivity, floor load, veto/action checks | sanity-checkable flow only |
| Voteview roll-call data | party unity, coalition size, chamber voting behavior | `voteview_rollcalls.csv`; `reports/empirical-validation-summary.md` | ready as raw summary | average enacted coalition support proxy | proxy only; not public opinion |
| Comparative Agendas Project topics | topic throughput, agenda diversity, topic enactment | `topic_throughput.csv`; `reports/empirical-validation-summary.md` | ready as raw summary | agenda diversity, topic throughput, welfare-per-submitted proxy | proxy only for issue mix, not benefit validation |
| ParlGov / cross-national party-system data | party-system profiles, coalition structure, bicameral/comparative productivity | `comparative_institutions.csv` | missing | party-system and chamber sensitivity anchors | not currently available |
| Senate LDA lobbying disclosures | spending concentration, issue diversity, client pressure | `lobbying_disclosure.csv`; `reports/empirical-validation-summary.md` | ready as raw summary | lobby spend, issue-pressure, capture proxy | proxy only; not bill-linked capture validation |
| OpenFEC campaign finance | receipts, independent expenditures, industry/committee pressure | `campaign_finance.csv` | missing | campaign-finance influence, private-spending concentration | synthetic only until added |
| Center for Effective Lawmaking / sponsor effectiveness | sponsor success, legislative effectiveness, proposal access | `sponsor_success.csv`; `reports/empirical-validation-summary.md` | ready as rough sponsor sample | proposer access Gini, sponsor success concentration | sanity-check/proxy; needs fuller sample |
| District-level public opinion / MRP / CCES-style sources | district support, issue intensity, turnout skew, affected-group representation | `district_public_opinion.csv` | missing | public support, district public will, representative responsiveness | synthetic only until added |
| Committee hearing / markup / referral / discharge records | referral, hearing, markup, amendment, discharge, reporting | `committee_activity.csv` | ready for basic committee activity; hearings/amendments currently zero in summary | committee gatekeeping, committee reporting, floor load | partial sanity check; hearings/markups thin |
| Court review / invalidation data | emergency orders, signed opinions, invalidation, constitutional review | `court_review.csv` | missing | judicial review, legal clearance, invalidation/correction | synthetic only until added |
| Federal Register / Unified Agenda / Regulations.gov | rulemaking delay, comments, implementation, enforcement, nonenforcement | `rulemaking_implementation.csv` | missing | implementation delay, administrative burden, correction feedback | synthetic only until added |
| Statutory amendment / repeal / sunset / reauthorization / expiration data | post-enactment amendment, reauthorization, repeal, sunset, expiration, invalidation lineage | `law_revision_history.csv` | missing | law registry, sunset, rollback, correction over time | synthetic only until added |

## Current Computed Signals

From `reports/empirical-validation-summary.md`:

- Voteview: `partyUnity = 0.946078`, `coalitionSize = 0.604453`.
- Bill progression: `floorLoad = 0.122222`, `committeeReportRate = 0.083333`, `enactmentRate = 0.016667`.
- Lobbying disclosure: `clientSpendGini = 0.976526`, `issueEntropy = 0.891519`.
- Topic throughput: `topicAgendaEntropy = 0.885219`, `topicFloorRate = 0.122222`, `topicEnactmentRate = 0.016667`.
- Sponsor success: `sponsorIntroductionGini = 0.388636`, `sponsorSuccessGini = 0.000000`.
- Committee activity: `committeeReportRate = 0.083333`, `hearingPerReferral = 0.000000`, `amendmentPerReferral = 0.000000`, `dischargeRate = 0.000000`.

These are benchmark signals. They are not proof that the simulator is valid.

## Priority Additions

1. District public opinion and affected-group support.
2. Campaign finance / OpenFEC.
3. Lobbying-to-bill linkage.
4. Implementation feedback from rulemaking/enforcement sources.
5. Statutory lineage for amendment, repeal, sunset, reauthorization, and expiration.
6. Court review and invalidation.
7. Cross-national institutions and party systems.
