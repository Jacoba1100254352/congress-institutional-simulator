# Claims Ledger

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

| Claim | Current support | Limitation | Required evidence before draft | Status |
|---|---|---|---|---|
| The simulator implements chamber, committee, and review architecture variants. | `src/main/java/congresssim/institution/chamber`; `institution/committee`; `reports/simulation-chamber-structure.md`. | Implementation breadth is not a validated representation model. | Mechanism taxonomy and representation diagnostics. | Supported as implementation claim. |
| Chamber variants shift productivity and moderation diagnostics in the current synthetic campaign. | `reports/simulation-chamber-structure.csv`; `reports/chamber-family-champions.md`. | Current results are sensitivity screens, not stand-alone evidence. | Paired chamber experiments and uncertainty reporting. | Conditional. |
| Malapportionment affects public-support failure. | Malapportionment metric appears in chamber family reports. | Need population-weighted support, chamber-weighted support, and support-gap outputs. | Malapportionment sweep and support-weighting experiment. | Not yet supported. |
| Upper-chamber power changes productivity, delay, and representation gaps. | Existing scenarios include amendment-only, suspensive veto, absolute veto, cloture, and lower-house override variants. | Need structured power sweep and conflict/delay metrics. | Upper-chamber power sweep. | Conditional. |
| Committee assignment and committee power affect committee capture and productivity. | Committee assignment/power scenarios exist; committee capture appears in stress screen. | Need explicit committee capture sweep and empirical committee data. | Committee assignment/capture sweep and validation targets. | Conditional. |
| Eligibility, selection, and retention filters affect representation and capture. | Expertise, recusal, appointment/retention scenarios exist. | Staggered renewal and retention diagnostics need clearer implementation and validation analogues. | Selection/retention sweep. | Conditional. |
| Independent review bodies reduce risk at a procedural cost. | Ex ante review, legal clearance, independent insulation, and court architecture scenarios exist. | Need review delay, intervention, and correction outcomes. | Review-body sweep and validation plan. | Conditional. |
| Current public support metrics support representation claims. | Synthetic public support exists. | Need national/district/affected-group/chamber coalition support separation. | Representation-model upgrade. | Not yet supported. |
| The chamber paper is ready for a full draft. | No. | Expanded scenarios and representation-validation planning are incomplete. | Complete full draft gate in `experiment-plan.md`. | No-go. |
