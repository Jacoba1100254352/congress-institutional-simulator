# Legislative Lifecycle Temporal Replication

No-refit backcast and forecast of the complete 117th-Congress calibration design against complete 116th- and 118th-Congress H.R./S. censuses.

## Frozen Protocol

- Calibration frozen in commit `c5a2a7fdf11afbbd8d91c467e74e841f6e1843c7` before either external cohort entered the reporting or selection path
- Frozen calendar-priority threshold: 0.68
- Fixed panel: 50 seeds, 24 runs per seed, 72,000 simulated bills
- Selection source: deterministic calibration half of the 117th-Congress census
- Backcast source: all 14,148 H.R. and S. bills in the 116th Congress
- Forecast source: all 16,213 H.R. and S. bills in the 118th Congress
- No 116th or 118th rate is read by the calibration selector; this report only reads the previously selected row
- Prespecified absolute-error tolerances: 0.020 committee advancement, 0.015 floor consideration, 0.010 enactment

## Transport Results

| Test Congress | Metric | 117 full rate | Test rate (95% Wilson interval) | Frozen simulator mean | Error | Tolerance | Result |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 116 | Committee advancement | 0.100292 | 0.105174 [0.100226, 0.110337] | 0.106278 | +0.001104 | 0.020 | pass |
| 116 | Substantive floor consideration | 0.066574 | 0.074074 [0.069873, 0.078506] | 0.061097 | -0.012977 | 0.015 | pass |
| 116 | Enactment | 0.023762 | 0.023537 [0.021165, 0.026167] | 0.027417 | +0.003880 | 0.010 | pass |
| 118 | Committee advancement | 0.100292 | 0.113674 [0.108880, 0.118652] | 0.106278 | -0.007396 | 0.020 | pass |
| 118 | Substantive floor consideration | 0.066574 | 0.059027 [0.055502, 0.062760] | 0.061097 | +0.002070 | 0.015 | pass |
| 118 | Enactment | 0.023762 | 0.016592 [0.014737, 0.018675] | 0.027417 | +0.010825 | 0.010 | fail |

The frozen model passes all 3 of 3 backcast tolerances for the 116th Congress and 2 of 3 forecast tolerances for the 118th Congress, or 5 of 6 external cohort-metric cells overall. The 118th-Congress enactment rate remains the only miss. It exceeds its tolerance by 0.000825: the simulator mean is 0.027417 versus the observed rate of 0.016592.

All 6 external cohort-metric cells remain inside the broader 117th-derived benchmark ranges. That range result does not override the stricter 118th enactment miss.

## Classifier Audit

The frozen artifact used classifier `govinfo-bill-lifecycle-v1`, builder SHA-256 `8b764e3d4577190a1da15b865911ca8191337415774a968df41662cc42c3b7fa`, and census SHA-256 `8e43e521148f113e95a2040ec592d7c5470c6303676a534f3d272497cc7bea36`. Full 118th processing exposed a context-dependent GovInfo `E30000` action: `118-s-4199` was vetoed rather than signed. Classifier v2 removed code-only enactment for `E30000` and required positive text or an unambiguous law record/code.

Classifier v3 adds successful veto-override classification only when affirmative House and Senate override evidence is present. It identifies the override and enactment of `116-hr-6395`; it changes no established committee, floor, completion, presentment, veto, or enactment count in any cohort. Both classifier revisions are source corrections, not post-hoc parameter changes.

## Provenance

- 116th normalized census SHA-256: `422265c48bd344ebd132815f7d711bda9b76ffda7b2d2182d8682ef7fa05e374`
- 117th normalized census SHA-256: `74f5270b7bd70f6b041fc100e18976a4626eb6aaa20ef1a7deedbf3a1aace747`
- 118th normalized census SHA-256: `a1d9fee85eb84c8f59bd99bb0c6f71f25fb55c9af10e54415553d851e29edc1b`
- Shared classifier: `govinfo-bill-lifecycle-v3`
- Source archive SHA-256 values, member counts, and timestamps are recorded in each census metadata file

## Interpretation Boundary

The earlier cohort passes all three frozen tolerances, while the later cohort preserves a narrow enactment miss. That pattern does not support treating the 118th result as a recurring directional bias across both external Congresses. It also does not establish general transport from only two external cohorts. The separate executive-action diagnostic shows that aggregate flow proximity can coexist with a large veto-mechanism discrepancy.

Claim boundary: This is a no-refit transport check for three aggregate legislative-flow rates. It tests whether one stylized workflow remains close to one earlier and one later completed Congress under tolerances fixed for the 117th calibration. It does not validate causal mechanisms, individual bills, public preferences, welfare, or institutional rankings.
