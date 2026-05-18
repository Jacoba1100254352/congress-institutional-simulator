# Metric Mapping

Final decision: BENCHMARK/DATA PIPELINE PLAN ONLY. DO NOT DRAFT FULL PAPER YET.

This file maps empirical signals to simulator metrics and states the claim boundary for each mapping.

## Boundary Categories

- Validated: empirical target directly validates a simulator quantity under a held-out design. Current status: none for central simulator outputs.
- Sanity-checkable: empirical signal can screen a broad simulator flow or scale.
- Proxy only: empirical signal is related but cannot validate the target construct.
- Synthetic only: simulator metric exists but no empirical input currently supports it.
- Not currently modeled: empirical signal is important but the simulator/reporting layer does not yet represent it clearly.

## Mapping Table

| Empirical signal | Source family | Simulator metric/proxy | Boundary category | Why |
|---|---|---|---|---|
| Bill enactment rate | Congress.gov / govinfo | `current-system` productivity | sanity-checkable | Broad flow target; current calibration screens rate but does not validate mechanism behavior. |
| Floor consideration rate | Congress.gov / govinfo | floor load / floor consideration | sanity-checkable | Screens agenda/floor volume, not support or quality. |
| Committee reporting rate | Congress.gov / committee activity | committee gatekeeping / floor proxy | sanity-checkable | Basic reporting signal available; hearings/markups remain thin. |
| Roll-call coalition size | Voteview | average enacted coalition support proxy | proxy only | Legislative coalition size is not public opinion. |
| Party unity | Voteview | party-pressure / enacted support proxy | proxy only | Useful for party behavior screens, not public support. |
| Veto frequency | Congress.gov / CRS-style veto records | vetoes per run | sanity-checkable | Screens executive-veto scale under stylized run length. |
| Sponsor proposal concentration | Congress.gov / CEL-style sponsor data | proposer access Gini | sanity-checkable/proxy | Screens sponsor concentration, not legislative effectiveness as a full construct. |
| Sponsor enacted-success concentration | sponsor success sample | proposer access Gini / sponsor success | proxy only | Current sample is rough and success rate is sparse. |
| Topic agenda entropy | Comparative Agendas Project / Congress subjects | issue-domain diversity | sanity-checkable/proxy | Screens topic mix, not public value. |
| Topic enactment rate | CAP / Congress subjects | topic throughput / welfare-per-submitted proxy | proxy only | Does not validate generated public benefit. |
| Lobby spending concentration | Senate LDA | lobby spend / capture proxy | proxy only | Spending concentration is not bill-level capture. |
| Lobby issue entropy | Senate LDA | issue-pressure diversity | proxy only | Shows pressure distribution, not influence effect. |
| Campaign finance concentration | OpenFEC/FEC | campaign-finance influence | synthetic only | Dataset missing. |
| District public opinion | MRP / CCES-style sources | public support, district support, representative responsiveness | synthetic only | Dataset missing; central support metrics are unvalidated. |
| Affected-group support/harm | district/group data plus issue mapping | minority harm, affected-group legitimacy | synthetic only | Dataset and mapping missing. |
| Committee hearings/markups | committee records | committee information gain, amendment/revision | proxy only / partial | Basic activity file ready, but hearing/markup signals are missing or zero. |
| Committee discharge records | committee/discharge records | discharge-petition behavior | proxy only / partial | Needs fuller committee dataset. |
| Court invalidation | SCDB / invalidation datasets | judicial review / correction | synthetic only | Dataset missing. |
| Emergency court posture | shadow-docket/emergency-order datasets | emergency review / court behavior | synthetic only | Dataset missing. |
| Rulemaking delay | Federal Register / Unified Agenda / Regulations.gov | implementation delay / administrative burden | synthetic only | Dataset missing. |
| Enforcement/nonenforcement | agency enforcement data | implementation feedback | synthetic only | Dataset missing. |
| Statutory amendment/repeal/sunset | OLRC/GovInfo/Congress.gov lineage | law registry, correction over time | synthetic only | Dataset missing. |
| Cross-national chamber/party structure | ParlGov / V-Dem / IPU | party-system and chamber sensitivity | synthetic only | Dataset missing; current chamber breadth is sensitivity, not fit. |
| Revision moderation | no direct empirical signal yet | moderating revision score | synthetic only | Needs operational definition and empirical target. |
| Generated public benefit | no direct empirical signal yet | welfare / policy yield | synthetic only | Internal generator quantity. |
| Administrative cost | possible future process/load proxies | admin cost | synthetic only / proxy only | Current metric is procedural-load proxy, not observed administrative cost. |

## Current Validation Claim

No central simulator outcome should be labeled validated. Current evidence supports benchmark construction and sanity checking for observable legislative flow only.
