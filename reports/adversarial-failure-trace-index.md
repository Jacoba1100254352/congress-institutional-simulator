# Adversarial Failure Trace Index

This report converts the existing manipulation-stress aggregate comparisons into pilot trace candidates for the robustness/failure-mode breakout. It is an index of where to collect full traces next, not a substitute for explicit adversary experiments.

- Pilot trace candidates: 7
- Pilot success flags: 3
- Material pilot degradation rows: 2
- Budget coverage: pilot_not_budgeted
- Information coverage: pilot_not_modeled

Claim boundary: Aggregate pilot failure-trace index only; rows compare bounded manipulation-stress aggregate cells against reference cells from the same campaign. This is not a per-bill action log, not a budget sweep, not an attack success rate, not recovery evidence, not empirical adversary validation, and not evidence for real-world institutional ranking.

Trace candidates:

| Rank | Adversary | Test | Reference | Stressed | Leading metric | Directional loss | Weak mandate added | Severity |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- |
| 1 | A1 | Policy tournament clone/decoy attack | `clone-decoy-pressure / simple-majority-alternatives-pairwise` | `clone-decoy-pressure / simple-majority-alternatives-strategic` | productivity_loss | 0.087 | 0.010 | material_pilot_degradation |
| 2 | A9/deferred | Open burden-shifting capture stress | `baseline / default-pass` | `capture-flooding / default-pass` | weak_mandate_added | 0.021 | 0.063 | material_pilot_degradation |
| 3 | A3/A8 | Astroturf objection pressure | `capture-flooding / public-objection-majority` | `capture-flooding / public-objection-astroturf-majority` | productivity_loss | 0.012 | 0.003 | bounded_pilot_degradation |
| 4 | A5 | Agenda flooding | `baseline / agenda-lottery-majority` | `proposal-flooding / agenda-lottery-majority` | productivity_loss | 0.008 | 0.007 | limited_or_no_observed_degradation |
| 5 | A3 | Citizen-panel manipulation | `capture-flooding / citizen-assembly-threshold` | `capture-flooding / citizen-assembly-manipulation-stress` | revision_moderation_loss | -0.002 | -0.005 | limited_or_no_observed_degradation |
| 6 | A4 | Bad-faith harm claims | `rights-harm-pressure / harm-weighted-majority` | `rights-harm-pressure / harm-weighted-loose-claims-majority` | public_support_loss | -0.002 | -0.018 | limited_or_no_observed_degradation |
| 7 | A6 | Anti-capture defensive backlash | `baseline / anti-capture-majority-bundle` | `anti-lobbying-backlash / anti-capture-majority-bundle` | public_support_loss | -0.066 | -0.065 | stress_variant_improves_aggregate_profile |

Missing before manuscript-grade traces:

- explicit budget; information level; same-seed per-run baseline pairing; per-bill attack action log; recovery/correction event log; attack success rate; seed sensitivity
