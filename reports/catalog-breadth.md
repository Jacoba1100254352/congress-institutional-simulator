# Scenario Catalog Coverage

The Java catalog preserves historical burden-shifting parameter sweeps as addressable scenario keys, but `--all-scenarios` runs a representative coverage screen: every non-default explicit key plus the small burden-shifting stress-test family used by the paper.

- Historical explicit keys: 196
- Coverage-screen keys run by `--all-scenarios`: 100
- Archived burden-shifting keys excluded from `--all-scenarios`: 96

| Breadth family | Count |
| --- | ---: |
| Adaptive/stress | 4 |
| Anti-capture | 3 |
| Attention scarcity | 3 |
| Bargaining/amendment | 4 |
| Chamber apportionment | 6 |
| Chamber routing/conflict | 13 |
| Citizen/public review | 5 |
| Coalition/parliamentary | 1 |
| Constituent population | 1 |
| Constitutional court architecture | 1 |
| Conventional benchmark | 6 |
| Default-pass archived/stress | 3 |
| Direct democracy | 1 |
| Distributional justice | 4 |
| Independent review | 3 |
| Influence/campaign finance | 1 |
| Leadership/procedure | 23 |
| Other | 5 |
| Policy tournament | 5 |
| Portfolio hybrid | 2 |
| Reversibility | 3 |
| Selection/retention | 3 |

Archived default-pass variants remain reproducible through `--scenarios <key>` and the historical v0--v20 campaign targets, but they no longer dominate the catalog-level breadth screen.
