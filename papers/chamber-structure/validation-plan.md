# Validation Plan

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

The chamber paper cannot claim empirical representation behavior until it has validation targets for apportionment, district population, chamber votes, committee assignment, referrals/markups, bicameral disagreement, and review bodies.

## Validation Data Needs

| Area | Why it matters | Candidate data source family | Current status |
|---|---|---|---|
| Apportionment data | Needed for population-seat distortion and malapportionment metrics. | Census apportionment, state/district population data, IPU/chamber data for comparative cases. | Missing or not integrated. |
| District population distributions | Needed for population-weighted support and district magnitude. | ACS, Census, district shapefiles or district-level population tables. | Missing. |
| District-level public opinion | Needed for district support and representation gaps. | CCES/CES, MRP estimates, issue-level district opinion. | Missing. |
| Upper/lower chamber vote patterns | Needed for chamber coalition support and bicameral disagreement. | Voteview, chamber roll-call records, comparative parliamentary roll calls where available. | Partially adjacent through Voteview, not chamber-structure-specific. |
| Committee assignment records | Needed for committee assignment/capture tests. | Congressional committee rosters, party ratios, chair assignments, seniority/expertise proxies. | Missing or incomplete. |
| Referral and markup data | Needed for gatekeeping and committee power. | Congress.gov, committee calendars, hearing/markup records, amendment data. | Referral partially inspectable; markup/hearing incomplete. |
| Bicameral disagreement data | Needed for navette, conference, override, upper veto, and conflict-rate validation. | Bill histories, conference reports, Senate/House action sequences, comparative bicameral datasets. | Missing. |
| Judicial/audit/ethics review data | Needed for independent review body models. | Supreme Court Database, inspector general/audit datasets, ethics committee records, fiscal scoring/review records. | Missing. |
| Selection/retention filters | Needed for appointment/election/retention claims. | Chamber tenure, appointment/election method, staggered renewal, eligibility rules, comparative chamber data. | Missing. |

## Validation Sequence

### Phase 1: Representation Data Inventory

Create a machine-readable inventory:

- source;
- unit of observation;
- years/chambers covered;
- license/access status;
- offline cache status;
- simulator metric supported;
- unsupported claims.

Proposed output:

- `reports/chamber-validation-data-inventory.csv`
- `reports/chamber-validation-data-inventory.md`

This inventory should reuse the empirical-validation breakout's source registry where possible, but it must add chamber-specific fields for population-seat distortion, chamber vote patterns, committee assignment, bicameral disagreement, and review-body actions.

### Phase 2: Apportionment and Population Diagnostics

Add or validate:

- population share by district/state/territory;
- seat share by chamber;
- malapportionment index;
- district magnitude;
- population-seat distortion.

### Phase 3: Chamber Vote and Conflict Diagnostics

Add or validate:

- lower-chamber coalition support;
- upper-chamber coalition support;
- chamber disagreement rate;
- conference/navette frequency;
- override frequency;
- chamber-origin effects.

### Phase 4: Committee Assignment and Routing

Add or validate:

- committee assignment composition;
- committee reporting rate;
- hearing/markup activity;
- amendment/revision rate;
- committee capture proxies.

### Phase 5: Review Body Diagnostics

Add or validate:

- ex ante fiscal/electoral/audit/legal review frequency;
- judicial review/invalidation;
- ethics/audit intervention;
- review delay;
- correction outcomes.

### Phase 6: Held-Out Checks

Only after phases 1-5:

- define calibration and held-out periods;
- report error/tolerance metrics;
- mark synthetic-only metrics separately;
- avoid calling support/harm/capture validated without direct targets.

## Current Boundary

Current chamber outputs should be described as sensitivity screens. They do not validate representation architecture because district population distributions, district public opinion, chamber coalition support, committee assignment records, and review-body data are not yet integrated.

Do not use the words validated, calibrated, representative, or empirically supported for chamber-structure effects unless the relevant source family has been integrated and the claim appears in `claims-ledger.md` as supported.

## Proposed Make Targets

```make
chamber-validation-data-inventory
chamber-apportionment-check
chamber-vote-conflict-check
committee-assignment-check
review-body-validation-check
```
