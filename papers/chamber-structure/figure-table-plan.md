# Figure and Table Plan

Final decision: NEEDS EXPANDED CHAMBER SCENARIOS AND REPRESENTATION VALIDATION FIRST.

## Required Main Tables

0. Go/no-go and evidence threshold table
   - Rows: implementation claim, pilot sensitivity claim, representation claim, empirical validation claim, institutional recommendation.
   - Columns: current status, required evidence, allowed language.

1. Chamber architecture taxonomy
   - Rows: unicameral, bicameral, upper-chamber composition, malapportionment, origin routing, second-chamber power, override, committee assignment, committee power, eligibility/selection/retention, independent review.
   - Columns: implemented scenario, model variable, expected mechanism, required validation source.

2. Representation metric definitions
   - Define population-weighted support, chamber-weighted support, district support, affected-group support, chamber coalition support, representation gap, malapportionment, committee capture, and review delay.

3. Validation-data gap table
   - Source: `validation-plan.md`.
   - Columns: data need, source family, current status, supported metric, remaining gap.

4. Review-body cost/risk table
   - Rows: ex ante advisory, legal clearance, fiscal/electoral/audit review, independent insulation, constitutional court architecture.
   - Columns: risk control, review delay, administrative cost, correction/reversal where available.

## Required Main Figures

1. Malapportionment vs public-support failure plot
   - X-axis: malapportionment or population-seat distortion.
   - Y-axis: population-weighted low-support enactment or representation gap.

2. Committee capture vs productivity plot
   - X-axis: committee capture.
   - Y-axis: productivity or floor load.
   - Point shape: committee assignment rule.

3. Bicameral conflict tradeoff plot
   - X-axis: bicameral conflict/delay.
   - Y-axis: public-support failure or risk control.
   - Labels: upper veto, amendment-only, lower override, conference, navette.

4. Population-weighted vs chamber-weighted support figure
   - Shows when chamber support diverges from population support.

5. Review delay/risk frontier
   - X-axis: review delay or administrative cost.
   - Y-axis: risk control / harm reduction.

## Required Appendix Tables

- Full chamber campaign table from `reports/simulation-chamber-structure.csv`.
- Chamber family champions from `reports/chamber-family-champions.md`.
- Chamber stress screen from `reports/chamber-stress-screen.md`.
- Full malapportionment sweep.
- Full committee capture sweep.
- Full support-weighting report.

## Presentation Rules

- Do not present current chamber stress-screen winners as institutional recommendations.
- Do not present current family champions as final evidence; label them pilot screen outputs.
- Do not use national public support as a substitute for district or affected-group support.
- Do not plot malapportionment against public-support failure until population-weighted and chamber-weighted support are separately reported.
- Mark synthetic-only representation diagnostics clearly.
- Separate chamber architecture from general mechanism-bundle comparisons.
- Use "revision moderation" rather than "compromise" in all new figures and tables.
