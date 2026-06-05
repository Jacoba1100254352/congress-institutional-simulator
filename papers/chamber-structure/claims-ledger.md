# Claims Ledger

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

## Claim Rules

- Current chamber reports may support implementation and pilot-sensitivity claims.
- Current chamber reports do not support empirical representation claims.
- Avoid winner language. Use "highest displayed profile in this pilot screen" only when needed, and explain the limitation.
- Any claim about representation requires population-weighted, chamber-weighted, district, affected-group, and chamber coalition support diagnostics.

## Claim Ledger

| ID | Claim | Supporting evidence | Limitation | Citation/data needed | Status |
|---|---|---|---|---|---|
| C1 | The simulator implements chamber, committee, and review architecture variants. | `src/main/java/congresssim/institution/chamber`; `src/main/java/congresssim/institution/committee`; `reports/simulation-chamber-structure.md`. | Implementation breadth is not evidence of empirical representation behavior. | Mechanism taxonomy with source-code anchors. | Supported as implementation claim. |
| C2 | Current chamber scenarios can identify candidate representation-architecture patterns for deeper testing. | `reports/simulation-chamber-structure.csv`; `reports/chamber-family-champions.md`; `reports/chamber-stress-screen.md`. | Pilot screens use current synthetic metrics and do not separate all representation diagnostics. | Paired chamber sweeps with uncertainty. | Supported only as pilot-sensitivity claim. |
| C3 | Chamber variants shift productivity and revision-moderation diagnostics in the current synthetic campaign. | Current chamber campaign reports productivity and moderation-like outputs. | The metric is still synthetic and not a political-theory measure of negotiated settlement. | Same-world paired comparisons and seed uncertainty. | Conditional. |
| C4 | Malapportionment affects public-support failure. | Malapportionment metric appears in chamber reports. | Current support outputs do not yet separate population-weighted, chamber-weighted, district, and affected-group support. | Malapportionment sweep plus support-weighting report. | Not yet supported. |
| C5 | Upper-chamber power changes productivity, delay, and representation gaps. | Scenarios include amendment-only, suspensive veto, absolute veto, cloture-like, and lower-house override variants. | Need structured power sweep and conflict/delay outputs. | Upper-chamber power sweep; chamber vote/conflict validation targets. | Conditional. |
| C6 | Committee assignment and committee power affect committee capture and productivity. | Committee assignment/power scenarios exist; committee capture appears in stress reports. | Need explicit committee-capture sweep and committee roster/referral/markup validation plan. | Committee assignment/capture sweep; committee data inventory. | Conditional. |
| C7 | Eligibility, selection, retention, and staggered renewal filters affect representation and capture. | Expertise, recusal, appointment/retention scenarios exist. | Retention and staggered-renewal diagnostics need clearer implementation and empirical analogues. | Selection/retention sweep; selection-rule data inventory. | Conditional. |
| C8 | Independent review bodies reduce risk at a procedural cost. | Ex ante review, legal clearance, fiscal/electoral/audit insulation, and court architecture scenarios exist. | Need review delay, intervention, correction, and invalidation analogues. | Review-body sweep; judicial/audit/ethics data inventory. | Conditional. |
| C9 | Current public-support diagnostics support representation claims. | Synthetic public support exists. | National scalar support is not enough for representation architecture. | National/district/affected/chamber support split. | Not supported. |
| C10 | The chamber paper is ready for a full draft. | No. | Expanded scenarios and representation-validation planning are incomplete. | Complete full draft gate in `go-no-go.md`. | No-go. |

## Safe Claim Language

- "The current chamber campaign is a pilot sensitivity screen."
- "The simulator contains implemented surfaces for chamber, committee, and review variants."
- "A stand-alone chamber paper requires representation diagnostics that are not yet fully separated."
- "Future experiments should test whether population-weighted and chamber-weighted support diverge under malapportionment and bicameral power changes."

## Unsafe Claim Language

- "The simulator validates chamber architecture effects."
- "Malapportioned chambers improve or worsen representation" without population-weighted and chamber-weighted support outputs.
- "Committee assignment rules reduce capture" without a committee-capture sweep and empirical committee data plan.
- "Review bodies are better safeguards" without delay, cost, intervention, and correction metrics.
- "The current chamber-family champions identify designs to recommend."
