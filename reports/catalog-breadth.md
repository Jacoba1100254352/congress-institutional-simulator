# Scenario Catalog Breadth

The Java catalog preserves historical default-pass parameter sweeps as addressable scenario keys, but `--all-scenarios` now runs a breadth-first screen: every non-default explicit key plus the small default-pass stress-test family used by the paper.

- Historical explicit keys: 138
- Breadth-screen keys run by `--all-scenarios`: 42
- Archived default-pass keys excluded from `--all-scenarios`: 96

| Breadth family | Count |
| --- | ---: |
| Adaptive/stress | 3 |
| Anti-capture | 2 |
| Attention scarcity | 3 |
| Bargaining/amendment | 3 |
| Citizen/public review | 4 |
| Coalition/parliamentary | 1 |
| Conventional benchmark | 6 |
| Default-pass archived/stress | 3 |
| Direct democracy | 1 |
| Distributional justice | 4 |
| Leadership/procedure | 3 |
| Policy tournament | 5 |
| Portfolio hybrid | 1 |
| Reversibility | 3 |

Archived default-pass variants remain reproducible through `--scenarios <key>` and the historical v0--v20 campaign targets, but they no longer dominate the catalog-level breadth screen.
