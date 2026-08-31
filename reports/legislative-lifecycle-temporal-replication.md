# Legislative Lifecycle Temporal Replication

No-refit transport test from the complete 117th-Congress calibration design to the complete 118th-Congress H.R./S. census.

## Frozen Protocol

- Calibration frozen in commit `c5a2a7fdf11afbbd8d91c467e74e841f6e1843c7` before the complete 118th census entered the reporting or selection path
- Frozen calendar-priority threshold: 0.68
- Fixed panel: 50 seeds, 24 runs per seed, 72,000 simulated bills
- Selection source: deterministic calibration half of the 117th-Congress census
- Test source: all 16,213 H.R. and S. bills in the 118th Congress
- No 118th rate is read by the calibration selector; this report only reads the previously selected row
- Prespecified absolute-error tolerances: 0.020 committee advancement, 0.015 floor consideration, 0.010 enactment

## Transport Results

| Metric | 117 full rate | 118 test rate (95% Wilson interval) | Frozen simulator mean | Error | Tolerance | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Committee advancement | 0.100292 | 0.113674 [0.108880, 0.118652] | 0.106278 | -0.007396 | 0.020 | pass |
| Substantive floor consideration | 0.066574 | 0.059027 [0.055502, 0.062760] | 0.061097 | +0.002070 | 0.015 | pass |
| Enactment | 0.023762 | 0.016592 [0.014737, 0.018675] | 0.027417 | +0.010825 | 0.010 | fail |

The frozen model passes 2 of 3 point-error tolerances. Committee advancement and floor consideration transport within tolerance. Enactment misses its tolerance by 0.000825: the simulator mean is 0.027417 versus the 118th-Congress rate of 0.016592.

All 3 test rates remain inside the broader 117th-derived benchmark ranges. That range result does not override the stricter enactment transport miss.

## Classifier Audit

The frozen artifact used classifier `govinfo-bill-lifecycle-v1`, builder SHA-256 `8b764e3d4577190a1da15b865911ca8191337415774a968df41662cc42c3b7fa`, and census SHA-256 `8e43e521148f113e95a2040ec592d7c5470c6303676a534f3d272497cc7bea36`. Full 118th processing exposed a context-dependent GovInfo `E30000` action: `118-s-4199` was vetoed rather than signed. Classifier v2 removes code-only enactment for `E30000` and requires positive text or an unambiguous law record/code.

The correction was applied symmetrically. It leaves every 117th aggregate lifecycle count unchanged and changes the exploratory 118th enactment classification from 270 to 269, with one vetoed non-enactment. This is a classifier correction, not a post-hoc parameter change.

## Provenance

- 117th normalized census SHA-256: `5dd533c526597944838088706980f07ac16bda5005ae57e573ed2911a99c7eba`
- 118th normalized census SHA-256: `b5d89515836e7209b6ef0d1d12b86627ebe2b2e6c8914a28a4994ae32278359b`
- Shared classifier: `govinfo-bill-lifecycle-v2`
- Source archive SHA-256 values, member counts, and timestamps are recorded in each census metadata file

## Interpretation Boundary

The result is informative in both directions: two aggregate rates transport under the frozen tolerances, while enactment is modestly overpredicted. The miss should remain visible rather than be removed by widening a tolerance or retuning on the test Congress. A second temporal cohort would be needed to distinguish a recurring model bias from Congress-specific variation.

Claim boundary: This is a no-refit transport check for three aggregate legislative-flow rates. It tests whether one stylized workflow remains close to a later completed Congress under tolerances fixed for the 117th calibration. It does not validate causal mechanisms, individual bills, public preferences, welfare, or institutional rankings.
