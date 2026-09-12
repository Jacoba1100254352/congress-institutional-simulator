# House Agenda-Control Panel: Locked Source Specification

Status: locked after official-source discovery and descriptive headline-count
review, then amended during parser implementation to preserve a source-internal
117th-Congress count discrepancy. No bill-level floor-path rate had been
computed when the amendment was made.

Lock date: 2026-08-31.

## Purpose and Status

This specification fixes a source-specific House agenda-control panel for the
116th, 117th, and 118th Congresses. The panel will connect complete GovInfo
H.R. action histories to the House Committee on Rules' official classifications
of special rules and to the corresponding H. Res. action histories.

The source audit established the available files, their hashes, the official
headline category counts, and representative XML structure before this
document was locked. It did not compute H.R.-level floor-path shares, stage
transition rates, delay distributions, or simulator discrepancies. This is a
post-source-audit extraction plan, not a blinded preregistration.

The panel is descriptive procedural evidence. It does not identify why
leadership, a committee, or the House selected a floor path; estimate a causal
effect of a rule type; recover unobserved demand for floor time; or validate
the simulator's public-benefit, welfare, representation, capture, or
institutional-ranking claims.

## Frozen Official Sources

The panel uses only completed-Congress official sources.

### House Committee on Rules surveys

The amendment-structure classification comes from Table 1a, "Types of Rules
Granted (Consideration)," in the House Committee on Rules Survey of Activities
for each Congress:

| Congress | GovInfo package | Source URL | SHA-256 | Bytes |
| ---: | --- | --- | --- | ---: |
| 116 | `CRPT-116hrpt722` | `https://www.govinfo.gov/content/pkg/CRPT-116hrpt722/html/CRPT-116hrpt722.htm` | `5d65df8e35bc575d9c31b3bce10913647dd1dc59b7d8c68f9253f14490eb344a` | 552457 |
| 117 | `CRPT-117hrpt709` | `https://www.govinfo.gov/content/pkg/CRPT-117hrpt709/html/CRPT-117hrpt709.htm` | `a7777dcd7bec4ff4d00477ec8ad405226505972efbf86e6f5395af215258c969` | 532625 |
| 118 | `CRPT-118hrpt979` | `https://www.govinfo.gov/content/pkg/CRPT-118hrpt979/html/CRPT-118hrpt979.htm` | `62a7f7d70939c357c7bd7ab8bd8491ddcc6602665796382fc2c2df1ef9eb0aae` | 542453 |

The survey narrative reports these amendment-structure counts:

| Congress | Open | Modified open | Structured | Closed | Total |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 116 | 0 | 0 | 55 | 60 | 115 |
| 117 | 0 | 0 | 59 | 89 | 148 |
| 118 | 0 | 1 | 83 | 115 | 199 |

Implementation review found that the literal 117th-Congress Table 1a contains
four fewer identifiable rule-to-measure rows than its narrative says. The
extractable table counts are:

| Congress | Open | Modified open | Structured | Closed | Total |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 116 | 0 | 0 | 55 | 60 | 115 |
| 117 | 0 | 0 | 57 | 87 | 144 |
| 118 | 0 | 1 | 83 | 115 | 199 |

The parser must reproduce the literal Table 1a counts and the report must
retain the 117th-Congress narrative-to-table differences of two structured and
two closed rows. It may not invent four measure identities to force agreement.
Both sets of counts are official-source facts and neither is silently treated
as the corrected version of the other.

These counts refer to rule-to-measure grant rows, not unique resolutions or
unique measures. A resolution may cover multiple measures, and a measure may
appear under more than one rule.

### GovInfo BILLSTATUS archives

Complete H.R. records use the already pinned 116th-, 117th-, and
118th-Congress H.R. archives and committed bill-census rows.

Complete H. Res. records use these official GovInfo archives:

| Congress | Archive | SHA-256 | XML members |
| ---: | --- | --- | ---: |
| 116 | `BILLSTATUS-116-hres.zip` | `dc79a72dea6c2ad6ff4e4065a2f44b9f954e0f3880ad9e86e1740ef69d71772a` | 1273 |
| 117 | `BILLSTATUS-117-hres.zip` | `2a915021d570e1de5592d5126be42ce3f02251a9252961c7ac98eb51d6796e72` | 1532 |
| 118 | `BILLSTATUS-118-hres.zip` | `b71a85e04d980fde4c4ad95919f214c4154575ddb874afb365b547e82b634e43` | 1627 |

The archive URL pattern is
`https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/hres/BILLSTATUS-{congress}-hres.zip`.
Only direct `bill/actions/item` records may supply action evidence. Text nested
inside related bills, amendments, summaries, or other descendants must not be
treated as an action of the current measure.

## Units of Observation

The build must produce two linked panels.

### Rule-to-measure grant panel

One row represents one Table 1a rule-to-measure grant. Required fields are:

- Congress;
- H. Res. rule identifier;
- covered measure type, number, and normalized ID;
- official amendment-structure category in `{open, modified_open, structured,
  closed}`;
- title as printed in the survey;
- source package, URL, SHA-256, and table name;
- H. Res. source URL and source XML SHA-256;
- whether the rule resolution passed the House;
- first reported date, first House disposition date, and disposition basis;
- whether the covered measure maps to the complete H.R. census; and
- explicit linkage or source-integrity status.

Continuation lines belong only to the immediately preceding title. Category
labels may occur on their own line or at the end of a preceding title line, as
in the 118th-Congress transition from `Modified-Open` to `Structured`. The
parser must reject an unrecognized nonblank line inside Table 1a rather than
silently dropping it.

### H.R. agenda-control panel

One row represents one H.R. measure in each complete GovInfo H.R. census. It
must retain the existing lifecycle and provenance fields and add:

- first House or Union Calendar placement, calendar name/number, date, and
  direct-action basis;
- direct-action evidence for consideration under suspension of the rules;
- all adopted Table 1a special-rule links and their categories;
- all nonadopted Table 1a grant links separately;
- direct-action H. Res. identifiers used for consideration, when present;
- counts of direct House floor amendment offer and disposition actions;
- introduction-to-referral, referral-to-committee-advance,
  committee-advance-to-floor, and introduction-to-floor elapsed days when
  both dates exist; and
- a conservative floor-path classification.

The floor-path classification applies only to a measure with substantive floor
consideration and uses these mutually exclusive values:

1. `adopted_special_rule` when at least one linked Table 1a H. Res. passed the
   House and no direct suspension action is present;
2. `suspension` when direct suspension action evidence is present and no
   adopted special-rule link is present;
3. `mixed_special_rule_and_suspension` when both forms of evidence are
   present;
4. `other_detected_floor_path` when another direct procedural action identifies
   a path that is neither an adopted special rule nor suspension; and
5. `floor_path_not_identified` when substantive floor consideration is present
   but no allowed direct-action path evidence is found.

A measure without substantive floor consideration receives
`not_floor_considered`. Absence of floor consideration by the end of a Congress
is an observed endpoint, not proof that leadership rejected the measure, that
the status quo was preferred, or that agenda capacity caused the endpoint.

For a measure with multiple adopted special rules, the panel must preserve the
complete category set and counts. It may report a most-restrictive summary in
the fixed order `closed > structured > modified_open > open`, but it must not
discard the underlying rows or relabel a mixed category set as a single source
classification.

## Frozen Temporal Comparison

The source study uses:

- development cohorts: 116th and 117th Congresses; and
- primary temporal test cohort: 118th Congress.

The 118th Congress is not outcome blind because the official headline rule
counts were inspected during source discovery. No H.R.-level route share,
transition rate, delay distribution, or simulator fit may be used to change
the extraction definitions after this lock.

The report must present each Congress separately and the pooled 116th-117th
development cohort. At minimum it must report:

1. introduced, referred, committee-advanced, calendar-placed,
   floor-considered, House-passed, and enacted counts and rates;
2. referral-to-advance and advance-to-floor transition rates using explicit
   denominators;
3. floor-path counts and shares among floor-considered H.R. measures;
4. special-rule category counts by grant row, unique resolution, and unique
   covered H.R. measure;
5. the restrictive share, defined as `structured + closed`, among adopted
   special-rule grant rows and among unique H.R. measures with an adopted
   special rule;
6. median and 90th-percentile elapsed days for each available stage interval;
7. floor-amendment action coverage by floor path; and
8. source-linkage conflicts, unresolved floor paths, and mixed-path rows.

Percentiles use sorted observed integer day values with the nearest-rank rule:
rank `ceil(p * n)`, bounded to `[1, n]`. No missing interval may be imputed as
zero or as the end of the Congress.

## Integrity Gates

The build and hard checker must fail if any of these conditions occurs:

1. A survey file or archive does not match its frozen SHA-256 hash.
2. Literal Table 1a category counts differ from the extractable totals above,
   or the recorded narrative counts or 117th-Congress discrepancies change.
3. A parsed Table 1a row lacks a valid H. Res. identifier, measure identifier,
   category, or source title.
4. A Table 1a H.R. row does not map to exactly one complete H.R. census row.
5. A Table 1a rule identifier does not map to exactly one complete H. Res.
   record.
6. A passed-House flag conflicts with the direct H. Res. action evidence used
   to derive it.
7. Nested related-bill or amendment text contaminates a direct-action field.
8. Stage dates run backward for an interval that is reported.
9. A floor-path category violates the frozen precedence rules.
10. Rebuilding offline from pinned cached sources changes a committed output.

## Required Outputs

The implementation must write, at minimum:

- a committed raw rule-to-measure grant CSV and reproducible metadata;
- a committed raw H.R. agenda-control CSV and reproducible metadata;
- a machine-readable metric table;
- a human-readable source and temporal-comparison report;
- an explicit reconciliation table preserving the 117th-Congress narrative
  and literal Table 1a count discrepancy;
- tests for table parsing, category transitions, direct-action isolation,
  path precedence, elapsed-day calculations, and source failures; and
- a hard checker for exact source counts, hashes, joins, report claims, and
  manuscript claim boundaries.

The Makefile must provide online raw-source build targets and an offline
publication target. Publication checks may use committed outputs or matching
pinned caches, but they may not silently accept an upstream source change.

## Simulator Follow-On Gate

No simulator parameter or floor-rule behavior changes are authorized by this
source specification alone. After the source panels pass all integrity gates,
a separate pre-fit calibration specification must freeze:

- the empirical quantities that are genuinely comparable to simulator
  metrics;
- any revised floor-path states and metric definitions;
- development-only parameter selection using the 116th-117th cohorts;
- the fixed simulation seeds, runs, candidate grid, loss function, and
  tie-breaking rule; and
- the 118th-Congress no-refit acceptance tolerances.

The baseline simulator result must be preserved even if it fails. A later
candidate may not be tuned to the 118th-Congress result in the same study.

## Amendment 1: 117th-Congress Narrative/Table Count Conflict

During the first parser run on 2026-08-31, the literal 117th-Congress Table 1a
yielded 57 structured and 87 closed rule-to-measure rows. Direct line review
confirmed those counts. The narrative immediately preceding the table reports
59 and 89. This amendment changes the extraction gate from forced agreement
with the narrative to exact preservation of both official-source results. It
does not change any row classification, floor-path definition, temporal split,
simulator parameter, or downstream acceptance rule, and it was made before the
H.R.-level agenda panel or its metrics were produced.

## Claim Boundary

Passing this source build would establish a reproducible official-source panel
of House procedural routes and stage timing for three completed Congresses. A
later passing temporal calibration would establish only that a fixed stylized
floor-path mechanism matches selected aggregate procedural rates within fixed
tolerances. Neither result would identify causal agenda power, prove that a
specific bill was blocked for a particular reason, validate unobserved public
preferences, or support real-world institutional-design recommendations.
