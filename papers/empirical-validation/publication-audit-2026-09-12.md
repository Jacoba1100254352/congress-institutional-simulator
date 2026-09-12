# Publication and Evidence Audit, 2026-09-12

## Scope and assessment

Review the current uncommitted implementation and manuscript, investigate the
failed House-procedure comparison without retuning against held-out data,
strengthen the highest-priority evidence links, and deliver reproducible
results with precise data-dependent limitations.

Assessment: **local checks passed; package and hosted CI verification in progress**. The empirical result is suitable
only with the qualifications below. Passing artifact checks does not turn
the synthetic simulator into an empirically validated model of Congress.
This audit does not authorize a second-generation fit, loosen tolerances,
choose a license, or establish an archived software release.

## Evidence and corrections

1. The frozen House source panel has 29,335 H.R. measures and 458 literal
   Table 1a grant rows. The original study retains 1,445 candidates, the
   selected 0.680 / 0.475 / 0.750 thresholds, and all 18 comparison metrics.
   Its 118th-Congress gate remains failed, with three of four conditions
   passing. The source distribution was known; a separate pre-fit protocol
   commit cannot be established. See the preserved protocol and
   [provenance amendment](house-agenda-control-provenance-amendment.md).
2. The new [chamber-attribution audit](../../reports/house-agenda-control-source-audit.md)
   reopens all three pinned H.R. archives, verifies every bill's XML and
   canonical-action hashes, and retains 7,397 candidate action records.
   The original phrase matcher incorrectly uses a Senate action on H.R.
   4366 as House suspension evidence. A separate House-screened comparison
   changes one bill, leaves the development population and fit unchanged,
   and raises test total variation from 0.110470441680 to 0.111949731621.
   Both exceed the unchanged 0.100 tolerance. No fitted results are replaced.
   A further primary-source check closes the named indirect-action gap:
   House roll call 64 adopted H. Res. 1061 under suspension by 339-85 on
   March 6, 2024, and the engrossed resolution deemed concurrence in the
   Senate amendment to H.R. 4366 with an amendment. Both complete source
   documents are retained with pinned hashes in
   `data/validation/reference/house-procedure-resolution-sources/`.
   The linkage supports a mixed-history label if indirect actions are
   included, but does not repair the original Senate-action provenance.
   The direct-only sensitivity must not be described as a complete correction.
3. The source's history-wide mixed route and the simulator's single-decision
   overlap are different quantities. H.R. 2670 and H.R. 3935 have later
   suspension actions after special-rule consideration; H.R. 9495 has the
   reverse sequence. The source audit records this structural limitation
   rather than claiming that the chamber correction explains the failure.
4. Manuscript prose now reports underproduction of special-only routes,
   unverified House pre-fit chronology, conditional Monte Carlo uncertainty,
   and the separate source-attribution sensitivity. Source-report status
   distinguishes frozen-artifact integrity from a known attribution caveat.
5. Census metadata was rebuilt from all six pinned local H.R./S. archives
   after the shared builder changed. The three source CSVs are unchanged;
   the full Census/executive/final-vote checker passes.
6. The anonymity check had treated GPO's official format-guide URL as an
   author link. The checker now permits that exact citation, with regression
   checks that other hosting links and suffix/query lookalikes remain
   blocked. Source URLs and hashes are not removed.
7. The reviewer packager now includes the required study protocols, new
   calibration and source-audit results, and campaign provenance manifests.
   It continues excluding surrounding planning notes and identity-bearing
   root release metadata. Actual archive validation is still required.
8. The implementation review confirms that special-rule and suspension
   thresholds only assign diagnostic labels. They do not alter the inner
   voting threshold or amendment rights. The manuscript and calibration
   documentation now state that boundary explicitly. Full-reproduction
   runtime guidance now accounts for the 1,445-candidate grid.
9. Every pre-existing value in all 4,646 rows of the five campaign tables
   matches the prior source commit, `1c15c493046ec895f22a12416b609069561db3c5`.
   Only eight diagnostic columns were added. A clean Java 21 rebuild retains
   JAR SHA-256 `c27e9827c717bb2e7f0080cfe7b3bd2e34df5360d3a3c5393b82bfefa913704b`.
10. The staged-change redacted secret scan reports no leaks. A broader local
    scan also encountered two credentials in the ignored `.env` and 5,445
    generated `scenarioKey` identifiers, including test outputs; those are
    not staged secrets. Only `.env.example` is tracked. The exact pinned
    GovInfo HTML snapshot retains publisher trailing spaces, with a
    file-specific whitespace-check exception rather than content alteration.
11. The baseline regeneration retained all 16 numerical screens and tolerances
    but exposed an outdated veto-count caveat. The CSV, Markdown, and provenance
    manifest now call it a legacy broad count screen, not a calibration of
    conditional veto probability. Seed robustness and catalog checks pass.
12. Two untracked numbered source copies appeared during local verification.
    Each matched its original byte for byte and was moved to recoverable local
    audit storage without changing the original. Six new regression tests
    protect the PDF source manifest: identical numbered copies do not alter
    its input digest, unpaired numbered inputs are retained, and differing
    copies stop for review. The full native suite and paper checks pass after
    this change; both PDF byte hashes are unchanged.
13. Hosted CI on `62bb85a` independently passed the native, empirical, paper,
    and package checks, then failed clean regeneration on the stale baseline
    caveat and last-bit presidential metadata differences. The baseline was
    already corrected in `e2cc614`. Metadata schema 2 now records explicitly
    labeled 12-decimal-place results, matching the existing CSV precision;
    it no longer calls these persisted values full precision. Fitting,
    unrounded gate evaluation, and all protocol constants are unchanged.
    Three regression tests cover observed cross-environment differences,
    preservation of the pre-rounding gate, and invalid numeric values. The
    metrics, coefficients, predictions, and substantive report remain
    byte-identical; the hard checker reconciles metadata with all eight CSV
    result rows. Metadata is byte-identical under local Python 3.9 and 3.14;
    all native and paper checks pass. Final hosted confirmation is still
    required.

## Verification ledger

| Requirement | Authoritative evidence | Current status |
| --- | --- | --- |
| No retuning or erased failure | Frozen panel, candidate and metric hashes; calibration hard checker | Full grid rerun retains candidate, metric, seed, and Monte Carlo hashes; hard checks pass under Python 3.9 and 3.14 |
| Source-linkage investigation | 29,335 XML/action hash matches; 7,397-row extract; full resolution and vote snapshots | Nine tests pass; source-audit regeneration checks pass under Python 3.9 and 3.14; pinned resolution-link check passes |
| Native regression coverage | `make test` with a clean Java 21 build | Java suite and 125 Python tests pass; final extracted-copy checks still pending |
| Isolated offline reproduction | Network-denied `make test` followed by `make reproduce-paper-offline`, outside the source checkout, using the `7981110` package snapshot | Isolated Java suite and 122 Python tests pass; rebuilt JAR matches the pinned hash. Full campaign reproduction is running. The subsequent metadata-only correction is checked separately. |
| Manuscript/output alignment | Full campaign/grid run, followed by `make -o paper-assets paper-checks` for the reconciled prose | All paper checks pass; 5,815 / 6,000 words; visual review passes for main pages 6, 7, 13 and appendix pages 6, 7, 8, 17; all 30 pages pass automated rendering |
| Anonymous reviewer reproducibility | Built ZIP, member/CRC/privacy checks, extracted-copy tests | Pending |
| Publication synchronization | Reviewed diff, redacted staged secret scan, commit/push, final CI result | Diff and secret scan pass; publication and hosted CI verification pending |

## Remaining data-dependent limitations

| Area | Evidence presently available | What is still required; claim not supported |
| --- | --- | --- |
| House procedure | Complete frozen bill/action panel, official Table 1a grants, chamber-screened direct-action sensitivity, and verified H. Res. 1061-to-H.R. 4366 linkage | Systematic resolution-mediated/deemed-action coverage beyond the reviewed link, full route-event sequences, referral-jurisdiction behavior, calendar demand and status-quo fallback evidence. No causal agenda-control, timing, or amendment-opportunity validation; diagnostic route labels do not enforce real House voting rules. |
| District opinion | One retained historical related-issue alignment out of 22 reviewed bill packets; two separate NY-10 estimates (2012 and 2016), with 92 and 280 responses | Exact or closer contemporaneous bill wording, validated district-boundary correspondence, survey-design uncertainty or a justified small-area model, and bill-specific affected-population links. No contemporaneous bill-support or representation validation. |
| Campaign finance and lobbying | Public recipient/member context, exact activity-text bill mentions, bounded position reviews, and official committee/roll-call context | Direct target/contact or outside-spending evidence connected to a specific bill, exposure timing, and a defensible outcome/influence design. Metadata overlap and contributions are not evidence of causal influence or capture. |
| Implementation feedback | Federal Register authority/history links; 48 public-law/docket rows with 19 complete and 29 partial/skipped/blocked metadata dispositions; 2,501 retrieved comment metadata records | Complete bounded high-volume comments where required, Unified Agenda stages, enforcement/nonenforcement, appropriations capacity, and observed implementation outcomes. A zero-comment or completed metadata retrieval is not successful implementation. |
| Statutory revision | 73 reviewed target-section differences across 13 public laws, with effective-text and bounded public-law attribution review; two no-structured-target dispositions | Complete codified lineage including notes, exceptions, redesignations and cross-references; implementation and outcome links. Reviewed attribution of text changes is not a causal policy-effect estimate. |
| Court review | 34 court/public-law queue dispositions: 33 temporally excluded, one reviewed not-direct, zero direct public-law reviews | Positive direct case-to-public-law or target-section identifiers, lower-court/emergency coverage, and disposition/effect evidence. Shared U.S.C. references do not establish direct review or invalidation of the named law. |
| Transport and institutional comparisons | Lifecycle tests pass 5 of 6 external cohort-metric tolerances; presidential predictor passes one primary gate, but 12 of 13 test vetoes occur among 17 joint resolutions | Unchanged replication on another completed cohort not used for model development; measure-class-specific tests; observed comparable institutional outputs. Synthetic welfare, harm, capture, and institution rankings remain unvalidated. |

Source reports: [district opinion](../../reports/district-public-opinion-bill-topic-support.md),
[finance/lobbying scope](../../reports/bill-finance-lobbying-member-vote-target-review.md),
[comments](../../reports/rulemaking-comment-records.md),
[statutory lineage](../../reports/statutory-lineage-completion-queue.md),
[court review](../../reports/court-public-law-direct-review.md), and
[linkage roadmap](../../reports/empirical-linkage-roadmap.md).

## Separate release prerequisites

The missing root license, final archived version/DOI, and completed clean-clone
release audit are release prerequisites, not empirical findings. They remain
distinct from the data-dependent limitations and from the current audit goal.
