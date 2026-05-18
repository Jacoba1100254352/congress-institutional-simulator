# Validation Plan

Final decision: NEEDS DATA/VALIDATION FIRST.

The current empirical layer supports only flow sanity checks for the conventional benchmark. A political-science paper needs a stronger validation and calibration plan before it can make claims about institutional behavior.

## Current Empirical Status

Existing checks:

- `reports/calibration-baseline.md`: 7/7 flow sanity checks passed.
- `reports/empirical-bridge.csv`: empirical comparison signals.
- `reports/empirical-validation-gap-report.md`: missing data and synthetic-only boundaries.
- `reports/core-raw-validation-build.md`: current raw sample counts.

Current checks cover:

- bill progression;
- floor load;
- roll-call coalition size / party-unity proxy;
- veto frequency;
- sponsor access concentration;
- lobbying spend observability;
- topic throughput.

Current checks do not validate:

- public support;
- generated public benefit;
- revision moderation;
- minority or concentrated harm;
- lobbying capture;
- administrative cost;
- correction over time;
- implementation feedback.

## Missing Data Inventory

| Data need | Why it matters | Candidate source family | Current status |
|---|---|---|---|
| District-level public opinion | Needed for representation and public-support claims. | CCES/CES, MRP estimates, ACS demographics. | Missing. |
| Campaign finance / OpenFEC | Needed to separate campaign-finance influence from lobbying proxies. | FEC/OpenFEC receipts, independent expenditures, industry classifications. | Missing. |
| Lobbying-to-bill linkage | Needed to connect lobbying pressure to proposal access, committee routing, and outcomes. | LDA filings, bill subjects, client/issue matching, committee referrals. | Missing. |
| Committee hearings / markups / referrals | Needed to validate committee gatekeeping and information-gain claims. | Congress.gov, committee calendars, hearing records, markup/amendment records. | Partial/referral-ready, hearings/markups incomplete. |
| Court review / invalidation | Needed for review/veto/correction modules. | Supreme Court Database, shadow-docket/emergency-order datasets, invalidation coding. | Missing. |
| Implementation and agency enforcement | Needed for administrative burden and implementation feedback. | Federal Register, Regulations.gov, Unified Agenda, agency enforcement rows. | Missing. |
| Law revision / repeal / sunset / reauthorization | Needed for law-registry, rollback, sunset, and correction claims. | Congress.gov, GovInfo, OLRC/statutory lineage, reauthorization histories. | Missing. |
| Cross-national parliamentary or bicameral comparisons | Needed for party-system and chamber claims beyond U.S.-like flows. | ParlGov, V-Dem, IPU/chamber data, electoral systems, productivity proxies. | Missing. |

## Validation Sequence

### Phase 1: Flow Sanity Expansion

- Replace bounded samples with fuller Congress.gov/govinfo bill-progression extracts.
- Add committee referral/reporting/markup coverage.
- Add veto-frequency and sponsor-concentration checks across multiple Congresses.
- Keep pass/fail bands broad and explicit.

### Phase 2: Proxy Risk Audit

- Mark every proxy as direct, indirect, weak, or missing.
- Do not use coalition size or party unity as public opinion.
- Do not use lobbying spend observability as capture validation.
- Do not use bill throughput as public benefit.

### Phase 3: Public Representation Data

- Add district-level opinion or modeled public preference.
- Map bills or issue domains to opinion topics.
- Split national support, district support, affected-group support, and intensity.

### Phase 4: Influence Linkage

- Link LDA client/issue data to bill topics and committee referrals.
- Add OpenFEC/FEC data for campaign-finance influence.
- Split lobbying into information, access, private-gain pressure, and public persuasion where possible.

### Phase 5: Review and Correction Data

- Add court review/invalidation data.
- Add implementation and rulemaking data.
- Add law revision, reauthorization, repeal, and sunset histories.

### Phase 6: Held-Out Validation

- Define calibration periods and held-out periods.
- Report error metrics, tolerance rules, and failures.
- Only after this phase should the paper use the word validation for central model outputs.

## Required Repo Tasks

- Add `reports/empirical-data-inventory.csv`.
- Add `reports/political-validation-targets.csv`.
- Add cached no-network summaries for every empirical input used.
- Add validation scripts that separate calibration, flow sanity, proxy checks, and held-out validation.

## Proposed Make Targets

```make
empirical-data-inventory
political-validation-targets
political-flow-heldout
political-public-opinion-map
political-lobbying-linkage
political-correction-data
```
