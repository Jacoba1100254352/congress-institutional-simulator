# Claims Ledger

Final decision: NEEDS DATA/VALIDATION FIRST.

Allowed language now: "the implemented simulator contains politically meaningful mechanism surfaces" and "planned experiments can test political mechanism behavior under explicit assumptions."

Disallowed language now: "the model validates a political theory," "this identifies better institutions," or "current synthetic public-support results are empirical representation findings."

| ID | Proposed claim | Supporting evidence | Limitation | Citation/data needed | Current status |
|---|---|---|---|---|---|
| C1 | The simulator implements politically meaningful legislative mechanisms, including agenda access, committees, bicameralism, vetoes, lobbying, thresholds, and content selection. | Source packages under `src/main/java/congresssim/institution`; `reports/scenario-selection-manifest.md`. | Implementation breadth is not the same as political-science validation. | Cite literature for each mechanism family. | Supported as implementation claim. |
| C2 | The stylized U.S.-like benchmark is useful as a synthetic comparison baseline. | `current-system` rows in `reports/simulation-campaign-v21-paper.csv`; `reports/calibration-baseline.md`. | It is not calibrated Congress and currently passes only flow sanity screens. | Congress.gov/govinfo, Voteview, veto data, sponsor data. | Supported with caveat. |
| C3 | Agenda gates, committee routing, and open floor access affect productivity and floor load in the simulator. | Scenario rows `CUR`, `COMM`, `DIS`, `OPEN`, and `SM` in main campaign. | Needs paired comparisons and benchmark fairness controls. | Agenda control and committee gatekeeping literature; committee data. | Conditional. |
| C4 | Veto structures and bicameralism shift enactment and risk diagnostics in the simulator. | Scenario rows `BIC`, `VETO`, `PROC`; chamber campaign. | Chamber paper owns deeper representation architecture; veto calibration is thin. | Veto-player theory; bicameral and veto datasets. | Conditional. |
| C5 | Lobbying pressure and anti-capture access alter capture-risk diagnostics in the simulator. | `BudgetedLobbyingProcess`, `InfluenceSystemProcess`, `LobbyCaptureScoring`; `ACG`, `CAP`, `INFL` rows where available. | Lobbying-to-bill and campaign-finance linkage are missing. | LDA, OpenFEC/FEC, issue-topic linkage. | Needs data. |
| C6 | Content-improvement stages can change productivity/support/risk tradeoffs under the implemented generator. | `PAIR`, `AMT`, `SMED`, `CAMD`, `PROC`, `PORT` rows in campaign/manifest. | PAIR and AMT are nearly duplicate; generator is moderation-friendly; cost-constrained controls are incomplete. | Amendment/agenda manipulation and bargaining literature; fairness controls. | Conditional. |
| C7 | Portfolio hybrid is a theoretically justified political-science object. | `PORT` exists and combines safeguards. | It is a bundle, not a clean political mechanism; risks becoming a pet design. | Institutional layering and oversight literature if retained. | Optional, use sparingly. |
| C8 | Public-support representation can be evaluated empirically with current data. | Current simulator reports synthetic public support and enacted support. | District-level public opinion and affected-group data are missing. | CCES/CES/MRP, ACS, affected-population mapping. | Not supported. |
| C9 | Current results support empirical validation of welfare, public support, harm, capture, or correction. | No sufficient support. | Current empirical checks are flow smoke tests only. | New validation workflow and held-out data. | Exclude. |
| C10 | A political-science full draft is ready now. | No. | Validation and benchmark fairness controls are not strong enough. | Complete `validation-plan.md`, `experiment-plan.md`, and `go-no-go.md`. | No-go. |

## Evidence Thresholds

A claim can move from conditional to draft-ready only after it has:

- a named mechanism family and scenario key;
- same-seed paired comparison against `CUR`, `SM`, or another justified benchmark;
- uncertainty separation between seed variance and scenario variation;
- cost/fairness accounting when comparing content-improvement systems with threshold-only baselines;
- empirical-boundary language tied to `reports/empirical-validation-gap-report.md`;
- citation targets for the political theory being tested.
