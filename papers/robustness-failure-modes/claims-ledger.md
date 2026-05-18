# Claims Ledger

Final decision: NEEDS ADVERSARY EXPERIMENTS FIRST.

| Claim | Current support | Limitation | Required evidence before draft | Status |
|---|---|---|---|---|
| The repo has pilot manipulation-stress diagnostics. | `reports/simulation-manipulation-stress.csv`; `reports/manipulation-stress-summary.md`. | Pilot stressors are not explicit adversary models. | Keep as motivation only. | Supported as pilot. |
| Policy tournaments are vulnerable to clone/decoy alternatives. | Pilot summary reports material vulnerability for policy tournament clone/decoy attack. | Needs attack budget, information level, success rate, and worst-case degradation. | Clone/decoy experiment with traces. | Conditional. |
| Amendment/tournament systems are vulnerable to poison-pill attacks. | Mechanisms exist in `institution/bargaining`; no explicit poison-pill experiment yet. | Not tested directly. | Poison-pill amendment experiment. | Not yet supported. |
| Objection windows can be overloaded by astroturf activity. | Pilot astroturf objection pressure shows limited observed degradation. | Current result is mild and may under-model adversary budget. | Attack-budget sweep and admin overload metrics. | Conditional. |
| Citizen panels are vulnerable to noisy or biased manipulation. | Pilot citizen-panel manipulation exists. | Limited observed degradation; no panel-manipulator adversary model. | Panel manipulation budget/information sweep. | Conditional. |
| Harm-weighted systems are vulnerable to bad-faith harm claims. | Pilot loose harm claim stress exists. | Limited observed degradation; no false-positive/false-negative claim model. | Harm-claim adversary experiment. | Conditional. |
| Open-calendar and burden-shifting systems are vulnerable to proposal flooding. | Proposal flooding and burden-shifting stress reports exist. | Need explicit flooder budgets and high-benefit crowdout metrics. | Proposal flooding experiment. | Conditional. |
| Anti-capture access systems are vulnerable to lobbying camouflage. | Lobbying/capture modules exist; anti-capture defensive backlash pilot exists. | No camouflage actor or proxy-sponsor model yet. | Lobby camouflage experiment. | Not yet supported. |
| Portfolio systems can fail through administrative overload. | Portfolio mechanisms and admin-cost metrics exist. | No overload attacker or queue saturation report yet. | Portfolio overload experiment. | Not yet supported. |
| Burden-shifting systems can fail through strategic silence. | Burden-shifting and challenge-token systems exist. | No strategic-silence model or unused-token metric. | Strategic silence experiment. | Not yet supported. |
| The future paper can report robustness by mechanism family. | Mechanism families exist. | Must avoid general mechanism rankings; only report vulnerability under specified attacks. | Vulnerability matrix and attack success rates. | Conditional. |
| A full manuscript is ready now. | No. | Required adversary experiments have not been run. | Complete full draft gate in `experiment-plan.md`. | No-go. |
