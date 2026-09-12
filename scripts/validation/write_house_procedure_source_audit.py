#!/usr/bin/env python3
"""Audit chamber attribution without modifying the frozen House study or fit.

The optional --rebuild-actions path reads pinned local archives only. Normal
report generation uses the committed, provenance-linked action extract.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from math import fsum
from pathlib import Path

from build_govinfo_bill_census_dataset import (
    KNOWN_ARCHIVE_PINS, at, canonical_actions_sha256, parse_actions, text_at,
)
from build_house_agenda_control_panel import OTHER_PATH_PHRASES, SUSPENSION_PHRASES
from write_house_resolution_link_reference import evidence as resolution_link_evidence
from write_house_resolution_link_reference import REPORT as RESOLUTION_LINK_REPORT

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "data/validation/raw/house_agenda_control.csv"
ACTIONS = ROOT / "data/validation/raw/house_procedure_audit_actions.csv"
PROVENANCE = ROOT / "data/validation/raw/house_procedure_audit_actions.metadata.json"
METRICS = ROOT / "reports/house-agenda-control-calibration-metrics.csv"
PREFIX = ROOT / "reports/house-agenda-control-source-audit"
FIELDS = (
    "bill_id", "action_index", "action_date", "action_time", "action_type",
    "action_code", "source_code", "source_name", "text", "evidence_kind",
    "source_url", "source_xml_sha256", "actions_sha256",
)
ROUTES = {
    "adopted_special_rule": "specialRuleOnlyRouteShare",
    "suspension": "suspensionOnlyRouteShare",
    "mixed_special_rule_and_suspension": "mixedSpecialRuleAndSuspensionRouteShare",
    "other_detected_floor_path": "otherFloorRouteShare",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_text(rows, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def chamber(row):
    """Require positive House evidence; explicit Senate attribution wins."""
    name = row["source_name"].casefold()
    if "senate" in name:
        return "senate"
    if row["source_code"] == "2" or "house" in name or row["action_code"].startswith("H"):
        return "house"
    if row.get("text", "").casefold().startswith((
        "passed/agreed to in house:", "failed of passage/not agreed to in house:",
        "failed of passage/not agreed to in house ",
    )):
        return "house"
    return "unresolved"


def harvest(panel, archive_dir):
    expected = {r["bill_id"]: r for r in panel}
    result, seen = [], set()
    archive_provenance = []
    for congress in (116, 117, 118):
        path = archive_dir / f"BILLSTATUS-{congress}-hr.zip"
        archive_hash, expected_members = KNOWN_ARCHIVE_PINS[(congress, "hr")]
        if digest(path) != archive_hash:
            raise ValueError(f"Archive pin mismatch: {path.name}")
        with zipfile.ZipFile(path) as archive:
            members = sorted(n for n in archive.namelist() if n.endswith(".xml"))
            if len(members) != expected_members:
                raise ValueError(f"Archive member count mismatch: {path.name}")
            for name in members:
                raw = archive.read(name)
                bill = at(ET.fromstring(raw), "bill")
                number = text_at(bill, "number") or text_at(bill, "billNumber")
                bill_type = (text_at(bill, "type") or text_at(bill, "billType")).casefold()
                if text_at(bill, "congress") != str(congress) or bill_type != "hr":
                    raise ValueError(f"Unexpected XML identity: {name}")
                bill_id = f"{congress}-hr-{number}"
                if bill_id in seen or bill_id not in expected:
                    raise ValueError(f"Unexpected or duplicate bill: {bill_id}")
                seen.add(bill_id)
                source = expected[bill_id]
                actions = parse_actions(bill)
                if hashlib.sha256(raw).hexdigest() != source["source_xml_sha256"]:
                    raise ValueError(f"XML pin mismatch: {bill_id}")
                if canonical_actions_sha256(actions) != source["actions_sha256"]:
                    raise ValueError(f"Action history mismatch: {bill_id}")
                for index, action in enumerate(actions):
                    if action.action_type.casefold() != "floor":
                        continue
                    text = action.text.casefold()
                    for kind, phrases in (("suspension", SUSPENSION_PHRASES), ("other", OTHER_PATH_PHRASES)):
                        if not any(phrase in text for phrase in phrases):
                            continue
                        result.append(dict(zip(FIELDS, (
                            bill_id, str(index), action.date, action.time,
                            action.action_type, action.code, action.source_code,
                            action.source_name, action.text, kind,
                            source["source_url"], source["source_xml_sha256"], source["actions_sha256"],
                        ))))
        archive_provenance.append({"filename": path.name, "sha256": archive_hash, "xmlMembers": len(members)})
    if seen != set(expected):
        raise ValueError("Archive-to-panel coverage is incomplete")
    result.sort(key=lambda r: (tuple(map(int, r["bill_id"].replace("-hr-", "-").split("-"))), int(r["action_index"]), r["evidence_kind"]))
    ACTIONS.write_bytes(csv_text(result, FIELDS).encode())
    PROVENANCE.write_text(json.dumps({
        "schema": 1,
        "claimBoundary": "Complete lexical suspension/other-path candidate extraction, not a complete House procedural history.",
        "panelSha256": digest(PANEL), "actionExtractSha256": digest(ACTIONS),
        "builderSha256": digest(Path(__file__)),
        "reviewedBillXmlRecords": len(seen), "candidateActionRows": len(result),
        "archives": archive_provenance,
    }, indent=2) + "\n", encoding="utf-8")


def verify_extract(panel, actions, provenance):
    if provenance["builderSha256"] != digest(Path(__file__)):
        raise ValueError("Source audit builder hash mismatch; rebuild the action extract")
    if provenance["panelSha256"] != digest(PANEL) or provenance["actionExtractSha256"] != digest(ACTIONS):
        raise ValueError("Source audit input hash mismatch")
    if provenance["reviewedBillXmlRecords"] != len(panel) or provenance["candidateActionRows"] != len(actions):
        raise ValueError("Source audit coverage count mismatch")
    archives = provenance["archives"]
    if len(archives) != 3:
        raise ValueError("Expected three pinned H.R. archives")
    for congress, archive in zip((116, 117, 118), archives):
        expected_hash, expected_count = KNOWN_ARCHIVE_PINS[(congress, "hr")]
        if archive != {"filename": f"BILLSTATUS-{congress}-hr.zip", "sha256": expected_hash, "xmlMembers": expected_count}:
            raise ValueError("Source audit archive provenance mismatch")
    index = {r["bill_id"]: r for r in panel}
    seen = set()
    for row in actions:
        key = row["bill_id"], row["action_index"], row["evidence_kind"]
        if key in seen or row["bill_id"] not in index:
            raise ValueError("Duplicate or orphan action evidence")
        seen.add(key)
        source = index[row["bill_id"]]
        if any(row[k] != source[k] for k in ("source_url", "source_xml_sha256", "actions_sha256")):
            raise ValueError(f"Bill provenance mismatch: {row['bill_id']}")


def audit(panel, actions):
    by_bill = defaultdict(list)
    for action in actions:
        by_bill[action["bill_id"]].append(action)
    corrected, changes = [], []
    for row in panel:
        candidates = by_bill[row["bill_id"]]
        # Reconstruct the frozen flags first, before applying chamber screening.
        for kind, flag in (("suspension", "suspension_path_evidence"), ("other", "other_floor_path_evidence")):
            if bool(int(row[flag])) != any(a["evidence_kind"] == kind for a in candidates):
                raise ValueError(f"Extract does not reconstruct {row['bill_id']} {flag}")
        suspension = any(a["evidence_kind"] == "suspension" and chamber(a) == "house" for a in candidates)
        new = dict(row)
        if row["floor_considered"] == "1" and row["suspension_path_evidence"] == "1" and not suspension:
            if int(row["adopted_rule_count"]):
                new["floor_path"] = "adopted_special_rule"
            else:
                # Do not silently manufacture an alternative route.
                new["floor_path"] = "floor_path_not_identified"
            excluded = [a for a in candidates if a["evidence_kind"] == "suspension"]
            changes.append({
                "bill_id": row["bill_id"], "original_route": row["floor_path"],
                "house_screened_route": new["floor_path"],
                "excluded_action_count": str(len(excluded)),
                "excluded_chambers": ";".join(sorted({chamber(a) for a in excluded})),
                "source_url": row["source_url"],
            })
        corrected.append(new)
    return corrected, changes


def sensitivity(original, corrected, metrics):
    rows = []
    for role, congresses in (("development", {"116", "117"}), ("test", {"118"})):
        old = Counter(r["floor_path"] for r in original if r["congress"] in congresses and r["floor_considered"] == "1")
        new = Counter(r["floor_path"] for r in corrected if r["congress"] in congresses and r["floor_considered"] == "1")
        denominator = sum(old.values())
        metric_role = "primary_temporal_test" if role == "test" else role
        simulation = {r["metric"]: float(r["simulatorValue"]) for r in metrics if r["cohortRole"] == metric_role}
        if set(new) - set(ROUTES):
            raise ValueError("Unresolved corrected route prevents a four-route comparison")
        distance = fsum(abs(new[route] / denominator - simulation[metric]) for route, metric in ROUTES.items()) / 2
        for route, metric in ROUTES.items():
            rows.append({"cohort": role, "metric": metric, "original_count": str(old[route]),
                         "house_screened_count": str(new[route]), "denominator": str(denominator),
                         "fixed_simulator_value": f"{simulation[metric]:.12f}",
                         "original_source_value": f"{old[route] / denominator:.12f}",
                         "house_screened_source_value": f"{new[route] / denominator:.12f}",
                         "original_total_variation": "", "house_screened_total_variation": ""})
        rows.append({"cohort": role, "metric": "routeTotalVariation", "original_count": "",
                     "house_screened_count": "", "denominator": str(denominator),
                     "fixed_simulator_value": "", "original_source_value": "",
                     "house_screened_source_value": "",
                     "original_total_variation": f"{simulation['routeTotalVariation']:.12f}",
                     "house_screened_total_variation": f"{distance:.12f}"})
    return rows


def outputs(panel, actions):
    resolution_link = resolution_link_evidence()
    if json.loads(RESOLUTION_LINK_REPORT.read_text()) != resolution_link:
        raise ValueError("Resolution linkage reference is stale")
    corrected, changes = audit(panel, actions)
    metrics = sensitivity(panel, corrected, read_rows(METRICS))
    non_house = Counter((a["evidence_kind"], chamber(a)) for a in actions if chamber(a) != "house")
    test_distance = next(r["house_screened_total_variation"] for r in metrics if r["cohort"] == "test" and r["metric"] == "routeTotalVariation")
    lines = [
        "# House Procedure Source Audit: Chamber Attribution", "",
        "Assessment: **share with caveats**. Post-fit source audit; no retuning or replacement of the frozen study.", "",
        f"All {len(panel):,} H.R. XML histories from the pinned 116th-118th archives were checked against their frozen XML and action hashes. The committed extract retains {len(actions):,} direct Floor actions matching the existing suspension/other-path phrases, including non-House actions. It reconstructs every original lexical evidence flag.", "",
        "## Chamber finding", "",
        f"House screening changes {len(changes)} bill route(s). Candidate actions lacking positive House attribution: " + "; ".join(f"{kind}, {source}: {count:,}" for (kind, source), count in sorted(non_house.items())) + ". Library of Congress summaries explicitly naming House passage or failure are recognized as House evidence; duplicate summaries do not multiply bill counts.", "",
        "| Bill | Frozen route | House-screened direct-action route | Excluded chamber |",
        "| --- | --- | --- | --- |",
        *[f"| {r['bill_id']} | {r['original_route']} | {r['house_screened_route']} | {r['excluded_chambers']} |" for r in changes],
        "", "The v1 phrase matcher did not require House attribution. H.R. 4366's cited 2023-11-01 suspension motion is explicitly a Senate action. The direct-action screen below deliberately excludes resolution-mediated actions; it is not a complete corrected procedural classification.", "",
        "## Verified resolution-mediated path", "",
        resolution_link["finding"], "",
        f"The [House Clerk's roll call 64](https://clerk.house.gov/Votes/202464) records {resolution_link['yeas']} yeas and {resolution_link['nays']} nays on March 6, 2024. The [engrossed resolution](https://www.govinfo.gov/content/pkg/BILLS-118hres1061eh/html/BILLS-118hres1061eh.htm) explicitly provides for that concurrence. Both complete source documents are retained with pinned hashes; [the linkage reference](house-agenda-control-resolution-linkage.json) records the exact operative clause.", "",
        "This closes the named H. Res. 1061-to-H.R. 4366 linkage gap. Including this indirect path alongside the earlier special-rule history supports a mixed-history label for this bill, but does not repair the original Senate-action attribution. The direct-only sensitivity is therefore not an estimate of a fully recoded distribution. Cross-measure coverage for the full panel remains unverified.", "",
        "## Fixed-model sensitivity", "",
        f"Screening the direct evidence moves the 118th counts from 127/544/4/1 to 128/544/3/1 (special-only/suspension-only/mixed/other), on the same 676-bill denominator. Total variation becomes {test_distance} instead of 0.110470441680. Both exceed the unchanged 0.100 tolerance. The development counts and fitted simulator values are unchanged. This is a post-fit data-quality sensitivity, not a new acceptance gate or independent validation.", "",
        "The original panel, candidate table, selected thresholds, test predictions, and failed metric table are preserved byte-for-byte. The chamber error does not account for the route failure; screening it slightly increases the discrepancy. The broader gap remains descriptive, not a causal explanation of leadership behavior.", "",
        "## Definition and linkage limitations", "",
        "- The source panel records routes observed anywhere in a bill's history, whereas the simulator's mixed label means two scores overlap in one scheduling decision. These are not equivalent procedural sequences.",
        "- CRS R48650 reports 545 H.R. measures initially considered under suspension. That initial-route denominator must not be equated with the panel's 548 ever-matched lexical suspension rows, or the 547 House-screened direct-action rows. H.R. 2670 and H.R. 3935 have special-rule consideration before later suspension actions; H.R. 9495 has failed suspension before a later special rule.",
        "- H. Res. 1061 is now explicitly linked, but other resolution-mediated or deemed actions still require a systematic cross-measure audit. This screen does not constitute a complete corrected procedural census, nor a measure of amendment opportunities, calendar demand, welfare, representation, capture, or causal institutional rankings.",
        "- The 118th distribution was already inspected. Neither this sensitivity nor subsequent modeling on it is an outcome-blind test.", "",
        "Official sources: [CRS R48650](https://www.congress.gov/crs-product/R48650), [H.R. 4366 actions](https://www.congress.gov/bill/118th-congress/house-bill/4366/all-actions), and the per-row pinned GovInfo XML links in the action extract.", "",
        "## Reproduction", "",
        "`make house-procedure-source-audit` reproduces this report and both tables from committed data. `make house-procedure-source-audit-check` verifies them without writing. `make build-house-procedure-audit-actions` re-extracts the evidence from all three pinned local H.R. archives, without network access. No simulator fit is run by these targets.", "",
        "`make house-resolution-link-reference` reconstructs the reviewed indirect link from complete retained source documents. Only the optional `make build-house-resolution-link-reference` uses the network, and it refuses changed source hashes.", "",
        f"Frozen panel SHA-256: `{digest(PANEL)}`. Action extract SHA-256: `{digest(ACTIONS)}`. Fixed-model metrics SHA-256: `{digest(METRICS)}`.", "",
    ]
    return {
        PREFIX.with_suffix(".md"): "\n".join(lines),
        PREFIX.with_suffix(".csv"): csv_text(changes, ("bill_id", "original_route", "house_screened_route", "excluded_action_count", "excluded_chambers", "source_url")),
        PREFIX.with_name(PREFIX.name + "-sensitivity.csv"): csv_text(metrics, ("cohort", "metric", "original_count", "house_screened_count", "denominator", "fixed_simulator_value", "original_source_value", "house_screened_source_value", "original_total_variation", "house_screened_total_variation")),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild-actions", action="store_true")
    parser.add_argument("--archive-dir", type=Path, default=ROOT / "out/validation-cache/govinfo-billstatus")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and args.rebuild_actions:
        parser.error("--check cannot be combined with --rebuild-actions")
    panel = read_rows(PANEL)
    if args.rebuild_actions:
        harvest(panel, args.archive_dir)
    actions = read_rows(ACTIONS)
    verify_extract(panel, actions, json.loads(PROVENANCE.read_text()))
    for path, content in outputs(panel, actions).items():
        if args.check:
            if not path.exists() or path.read_bytes() != content.encode():
                raise ValueError(f"Source audit output differs: {path.name}")
        else:
            path.write_bytes(content.encode())
    print("House procedure source audit checks passed." if args.check else "Wrote House procedure source audit.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(str(error))
