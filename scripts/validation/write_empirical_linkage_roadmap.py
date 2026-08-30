#!/usr/bin/env python3
"""Write a roadmap for upgrading empirical source-family linkages."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REGISTRY = Path("data/validation/source-registry.csv")
LINKAGE = Path("reports/empirical-linkage-report.csv")
OUT_CSV = Path("reports/empirical-linkage-roadmap.csv")
OUT_MD = Path("reports/empirical-linkage-roadmap.md")

FULLY_LINKED = {"linked"}

ROADMAP: dict[str, dict[str, str]] = {
    "govinfo bill and action records": {
        "blockingGap": "The 117th-Congress H.R./S. census is source-backed and linked, but its deterministic held-out split remains within one Congress and the operational action classifier still needs temporal replication.",
        "requiredJoinKeys": "congress,bill_type,bill_number,bill_id,action_date,source_xml_sha256,actions_sha256",
        "targetSourceFamilies": "Congress.gov bill histories; later GovInfo BILLSTATUS Congresses",
        "minimumViableDataset": "The pinned 117th-Congress census plus at least one later completed-Congress census produced by the same reviewed classifier.",
        "acceptanceGate": "A later completed Congress reproduces the lifecycle schema with archive pins, record/action hashes, integrity checks, and reviewed action-text or source-date differences before any temporal fit claim is made.",
        "futureTarget": "make build-govinfo-bill-census-raw ARGS='--congress <completed Congress> --allow-unpinned-source'",
        "claimUpgradeBoundary": "Supports descriptive census-backed legislative-flow and within-Congress held-out checks; temporal replication would still not validate public welfare, representation, implementation outcomes, or causal model fit.",
    },
    "Voteview roll-call data": {
        "blockingGap": "Roll-call rows now carry Voteview member metadata and a bounded Voteview bill-number crosswalk, but coverage is incomplete and still does not connect roll calls to topic, district public-opinion, public-law, implementation, court, or outcome evidence.",
        "requiredJoinKeys": "congress,chamber,roll_call_id,bill_id,member_id",
        "targetSourceFamilies": "Congress.gov bill histories; District public opinion and affected groups; Center for Effective Lawmaking and sponsor histories",
        "minimumViableDataset": "The current Voteview member metadata and bounded Voteview bill-number crosswalk plus broader roll-call-to-bill/action coverage across chambers and Congresses.",
        "acceptanceGate": "Roll-call rows join to bill IDs beyond the current bounded overlap and preserve enough member identifiers for sponsor, district, topic, public-law, implementation, or court joins.",
        "futureTarget": "make build-voteview-bill-linkage-raw",
        "claimUpgradeBoundary": "Would link coalition behavior to bills; it would still not make roll-call support equivalent to public opinion.",
    },
    "QoG and V-Dem comparative institutions": {
        "blockingGap": "Country-year institutional rows can now map to bounded simulator scenario-family metadata when the local comparative-institution linkage cache is present, but they are still not joined to observed chamber-level legislative output, bicameral disagreement, IPU/ParlGov chamber identifiers, or country-specific law-output records.",
        "requiredJoinKeys": "iso3,year,chamber_id,institution_family",
        "targetSourceFamilies": "Comparative Agendas topic throughput; Congress.gov bill histories",
        "minimumViableDataset": "The current bounded simulator scenario-family metadata bridge plus country-year chamber metadata and observed legislative-output rows that can join to the comparative institution profile.",
        "acceptanceGate": "Comparative institution rows join beyond the current simulator metadata anchors to observed country-year legislative output, IPU/ParlGov chamber identifiers, bicameral disagreement records, or reviewed chamber-level law-output rows for a documented set of countries.",
        "futureTarget": "make build-comparative-institution-linkage-raw",
        "claimUpgradeBoundary": "Supports bounded comparative context and simulator-scenario anchoring only; not cross-national institutional-fit, law-output productivity, adoption, welfare, or model validation by itself.",
    },
    "Senate LDA lobbying disclosures": {
        "blockingGap": (
            "LDA rows now carry a bounded issue-to-policy-area crosswalk, cached bill/action metadata by shared policy area, exact official filing-text bill identifiers for a bounded public-law subset, cached Congress.gov bill/action, sponsor, and enacted-outcome metadata for those exact bill IDs, bounded stored activity-text position-signal review, a disposition/target source-review queue, source-reviewed high-priority rows plus medium-priority directional and position/activity packets, a local bill-finance/lobbying review confirming no current-bill exact match in the current same-policy local context for the remaining queued rows, an external LDA current-bill search finding 55 exact activity-text bill-reference rows across 2 queued public-law bills, an external LDA mention review classifying 19 filing packets with no explicit support/opposition text, no named target, and no committee-action, roll-call, or outcome-causality evidence, a campaign-finance target-scope review covering 4 queued public-law rows, 5 candidate/recipient context attachments, 5 transaction attachments, 2 unique public FEC candidate recipients, and 2 unique raw OpenFEC transactions with no current-bill ID, sponsor/candidate overlap, committee-action, or outcome-influence link, a committee/action context report joining 10 queued public-law rows to cached public bill-action metadata with 8 committee-reported flags, 10 floor-considered flags, 0 committee-action influence rows, 0 roll-call influence rows, and 0 outcome-causality rows, a govinfo BILLSTATUS committee/action source review fetching 10 source rows with 9 committee-name rows across 12 unique committee/subcommittee names, 1 official no-direct-committee row, 9 direct committee-action record rows, 10 floor-action rows, 8 roll-call-reference rows, and 10 public-law outcome metadata rows, a House Clerk roll-call source review fetching 8 official roll-call XML rows with bill-ID matches, classifying 2 floor-action rows without numbered roll-call references, and representing 3,435 member-vote rows as source context, a member-vote target-scope review joining 3,435 official House Clerk member-vote rows across 8 numbered roll calls to reviewed public FEC/OpenFEC candidate/member context with 0 same-bill campaign target Bioguide overlaps and 40 broad public FEC member-context overlaps, and a source-acquisition queue recording 9 official govinfo committee-name rows, 1 official no-direct-committee source-reviewed row, 8 official House Clerk roll-call source rows, 8 official member-vote target-scope review rows, 2 no-numbered-roll-call floor-action rows, 0 remaining committee-name follow-up rows, 0 remaining roll-call source-acquisition rows, and 0 local Voteview roll-call context rows. Full activity-text refetch has removed the local truncation gap for cached exact-match rows, but the reviewed packet, local-context, external-search, external mention-review, campaign-finance target-scope, committee/action context, official source review, roll-call source review, member-vote target-scope review, and source-acquisition queue layers still do not create sponsor/member targets beyond activity-text references or public target-scope overlaps, direct member target documents, committee-action influence, roll-call influence, legislative-outcome causality, external campaign-finance target/source documents, or causal influence joins."
        ),
        "requiredJoinKeys": "filing_uuid,client,issue,issue_topic,policy_area,bill_id,committee,roll_call_id",
        "targetSourceFamilies": "Congress.gov bill histories; Comparative Agendas topic throughput; Committee hearing markup referral and discharge records",
        "minimumViableDataset": "The current documented LDA issue-to-policy-area crosswalk, policy-area bill/action context, exact filing-text bill-mention cache, exact bill/action metadata context, bounded stored activity-text position-signal review, high-priority manual review, medium-priority directional packet review, medium-priority position/activity packet review, disposition/target source-review queue, local no-current-match review, external LDA current-bill search review, external LDA mention review, campaign-finance target-scope review, committee/action context report, official govinfo committee/no-direct-committee source review, House Clerk roll-call source review, member-vote target-scope review, and source-acquisition queue plus sponsor/member, direct member target, external campaign-finance target/source, or outcome-causality dispositions where source evidence exists.",
        "acceptanceGate": "Support/opposition and position dispositions are manually confirmed where they affect claims, and any sponsor/member target, committee action, roll-call exposure, or legislative-outcome disposition is recorded only when the filing or public record supports it.",
        "futureTarget": "Use reports/bill-finance-lobbying-source-acquisition-queue.csv, reports/bill-finance-lobbying-member-vote-target-review.csv, reports/bill-finance-lobbying-roll-call-source-review.csv, reports/bill-finance-lobbying-committee-action-source-review.csv, reports/bill-finance-lobbying-external-lda-mention-review.csv, reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv, and reports/bill-finance-lobbying-committee-action-context.csv to pursue independent contact, target, direct member target documents, outcome-causality, and external campaign-finance source documents where source evidence exists",
        "claimUpgradeBoundary": "Supports bounded issue, policy-area bill exposure, exact filing-text bill-identifier context, stored activity-text position signals, source-reviewed activity-text dispositions, cached bill/action metadata context, source-review queue context, local no-current-match review, external LDA bill-reference search, external LDA mention review, public FEC/OpenFEC target-scope review, cached bill-action committee/floor flags, official govinfo committee/no-direct-committee source context, official House Clerk roll-call source context, and source-acquisition targets only; not client-to-bill lobbying influence, campaign-finance influence, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, or causal capture validation.",
    },
    "OpenFEC campaign finance": {
        "blockingGap": (
            "Rows now join to public FEC recipient metadata, a bounded transaction-label subset maps to broad policy-area issue context, a bounded candidate subset joins to Voteview member context when name/chamber/state/district evidence agrees, a bounded House-candidate subset joins to district public-opinion context, a bounded candidate/member subset joins by Bioguide ID to cached govinfo sponsored-bill metadata, the local bill-finance/lobbying review confirms no current-bill exact match in current same-policy local context for the remaining queued public-law rows, the campaign-finance target-scope review covers 4 queued public-law rows, 5 candidate/recipient context attachments, 5 transaction attachments, 2 unique public FEC candidate recipients, and 2 unique raw OpenFEC transactions while recording 0 public FEC/OpenFEC current-bill ID matches, 0 reviewed bill sponsor/candidate overlaps, 0 committee-action links, and 0 legislative-outcome or influence links, the committee/action context report joins 10 queued public-law rows to cached public bill-action metadata with 8 committee-reported flags, 10 floor-considered flags, 0 committee-action influence rows, 0 roll-call influence rows, and 0 outcome-causality rows, a govinfo BILLSTATUS committee/action source review fetches 10 source rows with 9 committee-name rows across 12 unique committee/subcommittee names, 1 official no-direct-committee row, 9 direct committee-action record rows, 10 floor-action rows, 8 roll-call-reference rows, and 10 public-law outcome metadata rows, a House Clerk roll-call source review fetches 8 official roll-call XML rows with bill-ID matches, classifies 2 floor-action rows without numbered roll-call references, and represents 3,435 member-vote rows as source context, a member-vote target-scope review joins 3,435 official House Clerk member-vote rows across 8 numbered roll calls to reviewed public FEC/OpenFEC candidate/member context with 0 same-bill campaign target Bioguide overlaps and 40 broad public FEC member-context overlaps, and the source-acquisition queue records 9 official govinfo committee-name rows, 1 official no-direct-committee source-reviewed row, 8 official House Clerk roll-call source rows, 8 official member-vote target-scope review rows, 2 no-numbered-roll-call floor-action rows, 0 remaining committee-name follow-up rows, 0 remaining roll-call source-acquisition rows, and 0 local Voteview roll-call context rows. There is still no reviewed external campaign target/source document, reviewed outside-spending target beyond public candidate IDs, bill-specific campaign-finance target/source evidence, direct member target document, committee-action influence, roll-call influence, legislative-outcome causality, private-contributor disclosure, or causal influence linkage."
        ),
        "requiredJoinKeys": "cycle,committee_id,candidate_id,member_id,bioguide_id,sponsor_bioguide_id,issue_topic,bill_id,committee",
        "targetSourceFamilies": "Congress.gov bill histories; Center for Effective Lawmaking and sponsor histories; Comparative Agendas topic throughput",
        "minimumViableDataset": "The current FEC recipient metadata, bounded issue-topic context, bounded Voteview member context, House-candidate district context, bounded candidate-to-sponsored-bill context, FEC/OpenFEC source-scope triage, campaign-finance target-scope review, committee/action context report, official govinfo committee/no-direct-committee source review, House Clerk roll-call source review, member-vote target-scope review, and source-acquisition queue plus broader bill, reviewed outside-spending target, direct member target, or outcome-causality metadata.",
        "acceptanceGate": "Scale the current candidate-to-sponsored-bill context beyond the bounded govinfo overlap and add reviewed outside-spending targets, direct member target documents, or legislative-outcome causality evidence without exposing private contributor information.",
        "futureTarget": "Use reports/bill-finance-lobbying-source-acquisition-queue.csv, reports/bill-finance-lobbying-member-vote-target-review.csv, reports/bill-finance-lobbying-roll-call-source-review.csv, reports/bill-finance-lobbying-committee-action-source-review.csv, reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv, and reports/bill-finance-lobbying-committee-action-context.csv to pursue external campaign target/source documents, direct member target documents, and outcome-causality evidence before making any bill-specific campaign-finance influence claim",
        "claimUpgradeBoundary": "Supports bounded recipient, issue-sector, member, district, candidate-to-sponsored-bill context, local no-current-match review, FEC/OpenFEC source-scope triage, public FEC/OpenFEC target-scope review, cached bill-action committee/floor flags, official govinfo committee/no-direct-committee source context, official House Clerk roll-call source context, and source-acquisition targets only; these joins are not causal influence, capture, bill-specific campaign-finance influence, committee-action influence, roll-call influence, public-benefit, or model validation.",
    },
    "Center for Effective Lawmaking and sponsor histories": {
        "blockingGap": "Sponsor aggregate rows now join by Bioguide ID to bounded govinfo BILLSTATUS sponsor metadata when the local sponsor-bill linkage cache is present, but the result is still a bounded sponsor aggregate rather than licensed CEL-style effectiveness data or complete member bill histories.",
        "requiredJoinKeys": "sponsor_id,member_id,bill_id,congress,chamber,party",
        "targetSourceFamilies": "Congress.gov bill histories; OpenFEC campaign finance; Voteview roll-call data",
        "minimumViableDataset": "The current bounded sponsor-bill metadata cache plus complete sponsor histories or a member-to-bill crosswalk that preserves sponsor IDs, bill IDs, chamber, committee, and outcome fields.",
        "acceptanceGate": "Sponsor rows join beyond the current bounded bill metadata to complete sponsor histories, licensed CEL-style effectiveness scores, roll-call outcomes, committee records, issue topics, district opinion, finance, lobbying, or legislative-quality outcomes.",
        "futureTarget": "make build-sponsor-bill-linkage-raw",
        "claimUpgradeBoundary": "Would support member proposal-access and sponsor-exposure checks; not full legislative-effectiveness validation without complete histories and reviewed outcome definitions.",
    },
    "District public opinion and affected groups": {
        "blockingGap": "The district-opinion pipeline now covers 22 official bill-text reviews, retains one directionally aligned historical CES issue item, preserves 21 negative dispositions against forced policy-area matches, and joins that item to annual CCES geography and validated-voter weights for two privacy-thresholded NY-10 estimates from 2012 and 2016. The estimates predate enactment, do not use the bill wording, omit design-based uncertainty, do not validate district-boundary equivalence with shape files, and do not provide MRP, contemporaneous support, bill-text-specific affected-population definitions, or issue-specific affected-group support and harm.",
        "requiredJoinKeys": "district_id,bill_id,survey_item_id,survey_year,policy_area,affected_group",
        "targetSourceFamilies": "Cumulative CES/CCES or ANES item-level public opinion; contemporaneous bill-topic surveys; Census TIGERweb; Census/ACS; congressional district boundary crosswalks; affected-group data",
        "minimumViableDataset": "The current sponsor-district metadata and context layers, source packets, Census/ACS context, official CES item/codebook reviews, official GovInfo bill-text context, source-reviewed bill-item dispositions, and privacy-thresholded annual district estimates plus an exact or closer contemporaneous bill-topic item, validated district geography, design-based uncertainty or MRP where needed, and bill-text-specific affected-population joins.",
        "acceptanceGate": "At least one exact or closer contemporaneous bill-topic question joins to a validated district estimate with an uncertainty treatment appropriate to the survey design, or to issue-specific affected-group support or harm data, while historical related-issue context remains separately labeled.",
        "futureTarget": "Use reports/district-public-opinion-bill-item-alignment-review.csv and reports/district-public-opinion-bill-topic-support.csv with the existing source packets, Census/ACS context, survey crosswalk, candidate-item, response-distribution, and codebook-direction reports to extend beyond the current historical related-issue pilot without weakening its exact-question, timing, geography, privacy, and uncertainty boundaries.",
        "claimUpgradeBoundary": "Supports a bounded source-reviewed historical related-issue district pilot with two direct-weighted annual estimates and explicit negative alignment dispositions. It is not exact or contemporaneous bill support, MRP, design-based uncertainty, validated district-boundary equivalence, bill-text-specific affected-population detail, issue-specific affected-group harm, public-benefit validation, causal representation, or model validation.",
    },
    "Court review and invalidation": {
        "blockingGap": "SCDB rows now preserve lawMinor U.S.C. sections and a bounded court-law linkage cache overlaps some of those sections with Federal Register authority citations attached to cached public-law rows, but there is still no direct case-to-public-law, bill, agency docket, lower-court, emergency-order, or implementation-record identifier.",
        "requiredJoinKeys": "case_id,public_law_number,usc_section,bill_id,agency,docket_id",
        "targetSourceFamilies": "Statutory revision and law lineage; Rulemaking implementation and enforcement; Congress.gov bill histories",
        "minimumViableDataset": "The current U.S.C.-section authority-overlap cache plus a direct case-to-statute or case-to-public-law crosswalk and emergency-order or lower-court identifiers where relevant.",
        "acceptanceGate": "At least one court-review row joins directly to a public law, bill ID, agency docket, implementation record, or reviewed challenged-statute identifier rather than only overlapping a U.S.C. section with Federal Register authority metadata.",
        "futureTarget": "make build-court-law-linkage-raw",
        "claimUpgradeBoundary": "Would link judicial review to statutes only after direct identifiers are added; the current U.S.C.-section overlap is not direct invalidation, emergency-review, lower-court, implementation-effect, welfare, or model validation evidence.",
    },
    "Rulemaking implementation and enforcement": {
        "blockingGap": "Final-rule rows can now join to Federal Register document metadata, a bounded public-law authority-search cache links some cached public-law rows to Federal Register rule text, and a bounded proposed-history cache links some authority-matched final rules to proposed-rule metadata. This still does not provide complete comment records, Unified Agenda stages, enforcement outcomes, appropriations capacity, or exhaustive implementation coverage.",
        "requiredJoinKeys": "document_number,public_law_number,usc_section,docket_id,rin,agency",
        "targetSourceFamilies": "Statutory revision and law lineage; Congress.gov bill histories; Court review and invalidation",
        "minimumViableDataset": "The current Federal Register document metadata, authority-search cache, proposed-history cache, bounded complete and partial Regulations.gov comment-record metadata, sanitized public comment-detail review for complete retrieved-comment rows and explicit partial-docket samples, plus higher-volume comment retrieval, Unified Agenda stages, agency enforcement identifiers, and appropriations-capacity rows for at least one reviewed rulemaking chain.",
        "acceptanceGate": "At least one public-law authority match is reviewed beyond proposed-rule metadata into complete bounded Regulations.gov comment-record metadata and sanitized public comment-detail text-availability/hash metadata, at least one partial high-volume retrieved-comment row is sampled with explicit incomplete-coverage flags, and the remaining high-volume comment, Unified Agenda, enforcement, or appropriations gaps stay explicit while preserving the authority/proposed-history-only claim boundary for unreviewed matches.",
        "futureTarget": "make build-rulemaking-history-linkage-raw",
        "claimUpgradeBoundary": "Would support implementation-feedback exposure checks only after authority/proposed-history matches are linked to complete comment, stage, enforcement, or appropriations evidence; Federal Register metadata, authority text, and proposed-rule metadata alone are not full enforcement or administrative-burden validation.",
    },
    "Statutory revision and law lineage": {
        "blockingGap": "Public-law rows now join to Congress.gov bill/action metadata, a bounded Federal Register authority-search cache links some public laws to rule text, a bounded proposed-history cache links some authority-matched final rules to proposed-rule metadata, a bounded SCDB/Federal Register U.S.C.-section overlap links some court rows to authority sections, a multi-public-law source-reviewed target-section diff pilot exists, effective-text and bounded public-law attribution reviews cover the positive pilot rows, a complete-lineage expansion queue ranks the remaining source-candidate, triage-to-packet, final-audit, and reviewed no-structured-target work, a target-packet expansion queue decomposes the triage-to-packet gap into row-level concrete U.S.C. note-review tasks with 0 current title-only manual-target tasks and 0 incomplete-fragment manual-review tasks, a target-packet source-gap queue classifies those blockers as current OLRC pages without public-law markers, current pages with public-law markers but no downstream packet, and manual source-gap review rows, a source-gap disposition review records curated official-source no-packet classifications for reviewed current-OLRC no-marker blockers, and a target-reference resolution candidate report records whether any ambiguous blockers still need bounded concrete U.S.C. candidates or no-candidate manual review. Full codified-text lineage, implementation/enforcement outcomes, welfare evidence, causal effects, and direct target-section court-review disposition remain absent.",
        "requiredJoinKeys": "public_law_number,bill_id,usc_section,amended_section,revision_date",
        "targetSourceFamilies": "Rulemaking implementation and enforcement; Court review and invalidation; Congress.gov bill histories",
        "minimumViableDataset": "The current Congress.gov bill-action metadata, Federal Register authority-search cache, proposed-history cache, U.S.C.-section court-overlap cache, bounded target-section diff/effective-text/public-law attribution pilot, complete-lineage expansion queue, target-packet expansion queue, target-packet source-gap queue, source-gap disposition review, and target-reference resolution candidate report plus broader OLRC or govinfo statutory-lineage rows with public law numbers, U.S. Code sections, amendment targets, related notes/subsections, and bill IDs.",
        "acceptanceGate": "Use the target-reference resolution candidate report to confirm whether any ambiguous rows need suggested concrete U.S.C. candidates or no-candidate manual review; use the target-packet source-gap queue and source-gap disposition review to resolve current OLRC pages without public-law markers and current pages with public-law markers but no downstream packet before building OLRC pre/post packets for direct U.S.C. note-review tasks; then use the complete-lineage expansion queue to expand source-scan candidates, audit related notes/subsections/amendments/repeals/redesignations/cross-references, and only then connect reviewed target sections to implementation, direct court-review rows, or reviewed enforcement outcomes before stronger correction-over-time claims are made.",
        "futureTarget": "make statutory-lineage-target-reference-resolution-candidates",
        "claimUpgradeBoundary": "Would support correction-over-time exposure checks after target-reference candidates are source-confirmed, no-candidate blockers are manually resolved, current-page source-gap blockers are resolved or disposition-reviewed, queued target packets are source-reviewed, and complete-lineage rows are expanded; the current target-section diff/effective-text/public-law attribution pilot, complete-lineage expansion queue, target-packet expansion queue, target-packet source-gap queue, source-gap disposition review, and target-reference resolution candidate report are not observed welfare, expiration outcome, complete codified lineage, enforcement, direct invalidation, causal public-law attribution, or model validation.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def by_field(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in rows if row.get(field)}


def build_rows(registry: list[dict[str, str]], linkage: list[dict[str, str]]) -> list[dict[str, str]]:
    registry_by_family = by_field(registry, "source_family")
    rows: list[dict[str, str]] = []
    for linkage_row in linkage:
        family = linkage_row["sourceFamily"]
        if linkage_row["linkageStatus"] in FULLY_LINKED:
            continue
        source = registry_by_family.get(family, {})
        spec = ROADMAP.get(family)
        if spec is None:
            spec = {
                "blockingGap": linkage_row.get("linkageBoundary", ""),
                "requiredJoinKeys": "not specified",
                "targetSourceFamilies": linkage_row.get("linkedTo", ""),
                "minimumViableDataset": source.get("next_step", ""),
                "acceptanceGate": "Add an explicit linkage rule and joinable source rows for this source family.",
                "futureTarget": "not specified",
                "claimUpgradeBoundary": source.get("claim_boundary", ""),
            }
        rows.append({
            "sourceFamily": family,
            "dataset": linkage_row["dataset"],
            "priority": linkage_row["priority"],
            "currentLinkageStatus": linkage_row["linkageStatus"],
            "linkedRows": linkage_row["linkedRows"],
            "totalRows": linkage_row["totalRows"],
            "blockingGap": spec["blockingGap"],
            "requiredJoinKeys": spec["requiredJoinKeys"],
            "targetSourceFamilies": spec["targetSourceFamilies"],
            "minimumViableDataset": spec["minimumViableDataset"],
            "acceptanceGate": spec["acceptanceGate"],
            "futureTarget": spec["futureTarget"],
            "claimUpgradeBoundary": spec["claimUpgradeBoundary"],
        })
    return rows


def write_markdown(rows: list[dict[str, str]], total_families: int) -> None:
    status_counts = Counter(row["currentLinkageStatus"] for row in rows)
    high_priority_rows = [row for row in rows if row["priority"] == "high"]
    lines = [
        "# Empirical Linkage Roadmap",
        "",
        "This roadmap turns the current linkage audit into source-family-specific upgrade gates. It is not validation evidence; it records the minimum joins needed before stronger empirical claims can be considered.",
        "",
        f"- Source families needing linkage upgrades: {len(rows)} / {total_families}",
        f"- High-priority linkage upgrades: {len(high_priority_rows)} / {len(rows)}",
        "",
        "Current linkage statuses among roadmap rows:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend([
        "",
        "| Source family | Current status | Required join keys | Minimum viable dataset | Acceptance gate |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['sourceFamily']} | {row['currentLinkageStatus']} "
            f"({row['linkedRows']} / {row['totalRows']}) | `{row['requiredJoinKeys']}` | "
            f"{row['minimumViableDataset']} | {row['acceptanceGate']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    registry = read_csv(REGISTRY)
    linkage = read_csv(LINKAGE)
    if not registry:
        raise SystemExit(f"{REGISTRY} is missing or empty.")
    if not linkage:
        raise SystemExit(f"{LINKAGE} is missing or empty; run make empirical-linkage-report first.")
    rows = build_rows(registry, linkage)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_markdown(rows, len(registry))
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
