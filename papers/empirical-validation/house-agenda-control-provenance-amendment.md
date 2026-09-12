# House Agenda-Control Study: Provenance and Numerical Amendment 1

Date: 2026-09-12. Status: post-fit audit amendment; no model refit.

## Protocol chronology

The original `house-agenda-control-calibration-specification.md` records a
2026-08-31 pre-fit lock. Its SHA-256 remains
`d7fdb1b7cd6131077479ed7bacf2c5404706e671e9cf12c200b7580ae99ccc72`.
The publication audit found that the specification, source panels, and fit
outputs were still untracked together. No separate pre-fit commit for the
specification exists in the available Git history. Consequently the public
artifact cannot independently establish the asserted pre-fit chronology.

The original document is preserved as the recorded protocol. This amendment
supersedes its claims of committed source artifacts and independently
established pre-fit timing. The study can be reproduced as a fixed,
post-source-audit development fit followed by an unchanged 118th-Congress
comparison. It must not be represented as a verified pre-fit registration or
as an outcome-blind test. The 118th source distribution was already known
when the recorded tolerances were chosen. A later publication commit does
not retroactively establish a pre-fit lock.

The calibration metadata therefore uses
`post-source-audit-prefit-chronology-unverified` as its current lock status
and hashes both the original specification and this amendment.

## Numerical reproducibility

Using the same Microsoft OpenJDK 21.0.11 executable, the original floating-point
aggregation produced different candidate-table bytes under Python 3.9 and
3.14. The cause was Python's changed built-in floating-point summation, not
an established change in Java's seeded world generation.

| Candidate-table version | SHA-256 |
| --- | --- |
| Original, Python 3.9 | `2ddc82e0ad4f7bc9ade38d1fb854f118d647e2c41fe16b2a319608a25fdc9e03` |
| Original, Python 3.14 | `faa3591f52d6b5e6efd2bec52aa728465f85363f3a342afcb02478944c617ff3` |
| Corrected, both interpreters | `8574e596907390c5e6991ae81e0b17724912f685034f13c69868d8d5a5047797` |

The original tables differed in 119 of 1,445 candidate rows, principally in
the last printed digits of selection loss. The largest absolute serialized
difference was approximately 3.2e-12. Explicit `math.fsum` aggregation
removed the interpreter dependence in the verified runs. This check covers
the calibration writer, not Python 3.9 compatibility of the entire project.

The selected triple remains 0.680 / 0.475 / 0.750, with 16 of 20
leave-one-seed-out reselections. The 18-row metric table is byte-identical
to the original result, with SHA-256
`09084f95ce1331be4c776669b31fd58d2da5650e22b53f6b65d336d308750b5c`.
The route total variation remains 0.110470441680 against 0.100, and the
primary gate still fails with three of four conditions passing. The model,
candidate grid, seeds, source targets, and tolerances were not changed.

## Interpretation correction

The main manuscript and two planning summaries incorrectly described
special-rule-only routes as overproduced. The source and simulator metric
tables were correct: the test share is 0.187869822485 observed versus
0.077399380805 simulated. Special-rule-only routes are underproduced;
mixed and other routes are overproduced. The prose is corrected to match
those tables. This correction does not change the retained failed gate.

## Missing diagnostics and portable provenance

The initial report omitted the protocol's required Monte Carlo variation
summary. The amended writer retains the selected candidate's 20 development
and 30 test seed rows and reports sample standard deviations, standard
errors, ranges, and seed means. These diagnostics do not alter the pooled
acceptance gate. Seed means of conditional shares and total variation need
not equal the corresponding pooled metrics. Development variation remains
conditional on the same seeds used for selection.

The House panel builder also now emits repository-relative source paths,
or just filenames for externally located caches. Source URLs and hashes
continue to identify the original records. This removes machine-specific
directory names from the public metadata without changing normalized data.

The JAR's default manifest embedded `Created-By: 21.0.11 (Microsoft)`, which
made the archive hash depend on the local Java distribution even with a
fixed entry date. The build now omits that unused manifest. All compiled
class bytes are preserved; the simulator uses an explicit classpath and
main class. The archive hash is repinned for this packaging correction.
