# House Procedure Source Audit: Chamber Attribution

Assessment: **share with caveats**. Post-fit source audit; no retuning or replacement of the frozen study.

All 29,335 H.R. XML histories from the pinned 116th-118th archives were checked against their frozen XML and action hashes. The committed extract retains 7,397 direct Floor actions matching the existing suspension/other-path phrases, including non-House actions. It reconstructs every original lexical evidence flag.

## Chamber finding

House screening changes 1 bill route(s). Candidate actions lacking positive House attribution: suspension, senate: 1. Library of Congress summaries explicitly naming House passage or failure are recognized as House evidence; duplicate summaries do not multiply bill counts.

| Bill | Frozen route | House-screened direct-action route | Excluded chamber |
| --- | --- | --- | --- |
| 118-hr-4366 | mixed_special_rule_and_suspension | adopted_special_rule | senate |

The v1 phrase matcher did not require House attribution. H.R. 4366's cited 2023-11-01 suspension motion is explicitly a Senate action. The direct-action screen below deliberately excludes resolution-mediated actions; it is not a complete corrected procedural classification.

## Verified resolution-mediated path

The House adopted H. Res. 1061 under suspension; that resolution deemed concurrence in the Senate amendment to H.R. 4366 with an amendment.

The [House Clerk's roll call 64](https://clerk.house.gov/Votes/202464) records 339 yeas and 85 nays on March 6, 2024. The [engrossed resolution](https://www.govinfo.gov/content/pkg/BILLS-118hres1061eh/html/BILLS-118hres1061eh.htm) explicitly provides for that concurrence. Both complete source documents are retained with pinned hashes; [the linkage reference](house-agenda-control-resolution-linkage.json) records the exact operative clause.

This closes the named H. Res. 1061-to-H.R. 4366 linkage gap. Including this indirect path alongside the earlier special-rule history supports a mixed-history label for this bill, but does not repair the original Senate-action attribution. The direct-only sensitivity is therefore not an estimate of a fully recoded distribution. Cross-measure coverage for the full panel remains unverified.

## Fixed-model sensitivity

Screening the direct evidence moves the 118th counts from 127/544/4/1 to 128/544/3/1 (special-only/suspension-only/mixed/other), on the same 676-bill denominator. Total variation becomes 0.111949731621 instead of 0.110470441680. Both exceed the unchanged 0.100 tolerance. The development counts and fitted simulator values are unchanged. This is a post-fit data-quality sensitivity, not a new acceptance gate or independent validation.

The original panel, candidate table, selected thresholds, test predictions, and failed metric table are preserved byte-for-byte. The chamber error does not account for the route failure; screening it slightly increases the discrepancy. The broader gap remains descriptive, not a causal explanation of leadership behavior.

## Definition and linkage limitations

- The source panel records routes observed anywhere in a bill's history, whereas the simulator's mixed label means two scores overlap in one scheduling decision. These are not equivalent procedural sequences.
- CRS R48650 reports 545 H.R. measures initially considered under suspension. That initial-route denominator must not be equated with the panel's 548 ever-matched lexical suspension rows, or the 547 House-screened direct-action rows. H.R. 2670 and H.R. 3935 have special-rule consideration before later suspension actions; H.R. 9495 has failed suspension before a later special rule.
- H. Res. 1061 is now explicitly linked, but other resolution-mediated or deemed actions still require a systematic cross-measure audit. This screen does not constitute a complete corrected procedural census, nor a measure of amendment opportunities, calendar demand, welfare, representation, capture, or causal institutional rankings.
- The 118th distribution was already inspected. Neither this sensitivity nor subsequent modeling on it is an outcome-blind test.

Official sources: [CRS R48650](https://www.congress.gov/crs-product/R48650), [H.R. 4366 actions](https://www.congress.gov/bill/118th-congress/house-bill/4366/all-actions), and the per-row pinned GovInfo XML links in the action extract.

## Reproduction

`make house-procedure-source-audit` reproduces this report and both tables from committed data. `make house-procedure-source-audit-check` verifies them without writing. `make build-house-procedure-audit-actions` re-extracts the evidence from all three pinned local H.R. archives, without network access. No simulator fit is run by these targets.

`make house-resolution-link-reference` reconstructs the reviewed indirect link from complete retained source documents. Only the optional `make build-house-resolution-link-reference` uses the network, and it refuses changed source hashes.

Frozen panel SHA-256: `d801a86290d2eb7127736ef259a44847fe5d19acff2c4dd738d2f00ba0556f7b`. Action extract SHA-256: `64963ee1708bb3331de031a8f94fa22a30ff932b278ee640012150add5d74487`. Fixed-model metrics SHA-256: `09084f95ce1331be4c776669b31fd58d2da5650e22b53f6b65d336d308750b5c`.
