# Adversarial Pilot Cell Map

This report maps the Java first-wave adversary catalog to the current aggregate manipulation-stress evidence and bounded executable pilot artifacts. It is a planning and readiness artifact, not a complete adversary experiment result.

- First-wave adversaries: 9
- Adversaries with at least one aggregate pilot cell: 7
- Adversaries without a current pilot cell: 2
- Adversaries with partial executable pilots: 7
- Manuscript-ready adversary rows: 0

Claim boundary: Catalog-to-pilot map only. Mapped rows identify aggregate manipulation-stress cells that can seed explicit adversary experiments and bounded executable A1/A2/A3/A4/A5/A6/A7 pilot artifacts where present. They are not a complete A1-A9 sweep, not mechanism-wide robustness estimates, and not complete recovery/correction evidence beyond the bounded A7 queue-recovery pilot.

| ID | Name | Aggregate cells | Aggregate status | Executable status | Executable rows | Trace artifact | Next required artifact |
| --- | --- | ---: | --- | --- | ---: | --- | --- |
| A1 | Clone/decoy proposer | 1 | aggregate_pilot_cell_mapped | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A2 | Poison-pill or sequencing actor | 0 | no_current_pilot_cell | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces-a2.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A3 | Public-input manipulator | 2 | aggregate_pilot_cell_mapped | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces-a3.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A4 | Bad-faith harm claimant | 1 | aggregate_pilot_cell_mapped | partial_executable_pilot_available | 3 | reports/adversarial-failure-traces-a4.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A5 | Proposal flooder | 1 | aggregate_pilot_cell_mapped | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces-a5.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A6 | Lobbying camouflage actor | 1 | boundary_pilot_cell_not_camouflage | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces-a6.jsonl | extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces |
| A7 | Administrative overload coalition | 0 | no_current_pilot_cell | partial_executable_pilot_available | 6 | reports/adversarial-failure-traces-a7.jsonl | extend to expanded/risk-routed mechanisms, seed and capacity sensitivity, and substantive correction |
| A8 | Public-support distortion actor | 1 | aggregate_pilot_cell_mapped | not_available | 0 | none | run low/medium/high budget same-seed attack sweep with per-bill trace log |
| A9 | Mixed adversary portfolio | 1 | deferred_or_boundary_pilot_cell | not_available | 0 | none | replace open burden-shifting stress proxy with fixed-budget mixed-attack portfolio |

Gate status: every row remains `not_ready`. A1 through A7 now have bounded executable pilot artifacts, but the mapped evidence still lacks A8-A9 executable pilots, broader mechanism coverage, recovery metrics beyond A7 queue recovery, seed sensitivity, and external validation.
