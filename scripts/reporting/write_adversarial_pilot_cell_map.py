#!/usr/bin/env python3
"""Map first-wave adversary specs to current aggregate and executable pilot cells."""

from __future__ import annotations

import csv
from pathlib import Path


CATALOG = Path("reports/adversary-catalog.csv")
TRACE_INDEX = Path("reports/adversarial-failure-trace-index.csv")
OUT_CSV = Path("reports/adversarial-pilot-cell-map.csv")
OUT_MD = Path("reports/adversarial-pilot-cell-map.md")
EXECUTABLE_OUTPUTS = {
    "A1": (Path("reports/adversarial-stress-summary.csv"), "reports/adversarial-failure-traces.jsonl"),
    "A2": (Path("reports/adversarial-stress-a2-summary.csv"), "reports/adversarial-failure-traces-a2.jsonl"),
    "A3": (Path("reports/adversarial-stress-a3-summary.csv"), "reports/adversarial-failure-traces-a3.jsonl"),
    "A4": (Path("reports/adversarial-stress-a4-summary.csv"), "reports/adversarial-failure-traces-a4.jsonl"),
    "A5": (Path("reports/adversarial-stress-a5-summary.csv"), "reports/adversarial-failure-traces-a5.jsonl"),
    "A6": (Path("reports/adversarial-stress-a6-summary.csv"), "reports/adversarial-failure-traces-a6.jsonl"),
    "A7": (Path("reports/adversarial-stress-a7-summary.csv"), "reports/adversarial-failure-traces-a7.jsonl"),
    "A8": (Path("reports/adversarial-stress-a8-summary.csv"), "reports/adversarial-failure-traces-a8.jsonl"),
    "A9": (Path("reports/adversarial-stress-a9-summary.csv"), "reports/adversarial-failure-traces-a9.jsonl"),
}
SEED_REPLICATION_OUTPUTS = {
    "A9": Path("reports/adversarial-replication-a9-summary.csv"),
}

CLAIM_BOUNDARY = (
    "Catalog-to-pilot map only. Mapped rows identify aggregate manipulation-stress cells "
    "that can seed explicit adversary experiments and bounded executable A1-A9 pilot artifacts. "
    "They complete first-wave catalog coverage but are not mechanism-wide robustness estimates or "
    "complete recovery/correction evidence. A9 has a fixed-specification 30-base-seed replication; "
    "A1-A8 do not yet have adversarial seed replication."
)

FIELDNAMES = [
    "adversary_id",
    "name",
    "actor_type",
    "pilot_cell_count",
    "pilot_trace_ranks",
    "pilot_tests",
    "pilot_status",
    "pilot_success_flags",
    "material_pilot_degradation_count",
    "executable_pilot_status",
    "executable_summary_rows",
    "executable_trace_artifact",
    "baseline_pairing_level",
    "budget_status",
    "information_status",
    "attack_success_rate_status",
    "worst_case_status",
    "median_status",
    "seed_replication_status",
    "seed_replication_artifact",
    "recovery_status",
    "per_bill_trace_status",
    "manuscript_gate",
    "next_required_artifact",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_trace_ids(raw: str) -> list[str]:
    if raw == "A3/A8":
        return ["A3", "A8"]
    if raw == "A9/deferred":
        return ["A9"]
    return [raw]


def traces_by_adversary(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    mapped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        for adversary_id in normalized_trace_ids(row["adversary_id"]):
            mapped.setdefault(adversary_id, []).append(row)
    return mapped


def pilot_status(adversary_id: str, traces: list[dict[str, str]]) -> str:
    if not traces:
        return "no_current_pilot_cell"
    if adversary_id == "A6":
        return "boundary_pilot_cell_not_camouflage"
    if adversary_id == "A9":
        return "aggregate_boundary_cell_mapped"
    return "aggregate_pilot_cell_mapped"


def executable_status(adversary_id: str) -> tuple[str, str, str]:
    executable = EXECUTABLE_OUTPUTS.get(adversary_id)
    if executable is None:
        return ("not_available", "0", "none")
    summary_path, trace_artifact = executable
    if not summary_path.exists():
        return ("not_available", "0", "none")
    return ("partial_executable_pilot_available", str(count_data_rows(summary_path)), trace_artifact)


def information_status(adversary_id: str, has_executable_pilot: bool) -> str:
    if not has_executable_pilot:
        return "not_modeled"
    if adversary_id == "A8":
        return "low_medium_high_information_cells_available"
    if adversary_id in {"A3", "A5"}:
        return "low_medium_information_cells_available"
    if adversary_id == "A4":
        return "medium_information_cells_available"
    return "medium_high_information_cells_available"


def recovery_status(adversary_id: str, has_executable_pilot: bool) -> str:
    if adversary_id == "A7" and has_executable_pilot:
        return "queue_recovery_computed_for_executable_pilot"
    if adversary_id == "A8" and has_executable_pilot:
        return "same_case_signal_correction_computed_for_executable_pilot"
    if adversary_id == "A9" and has_executable_pilot:
        return "same_case_review_and_queue_recovery_controls_computed_for_executable_pilot"
    return "not_computed"


def seed_replication_status(adversary_id: str) -> tuple[str, str]:
    artifact = SEED_REPLICATION_OUTPUTS.get(adversary_id)
    if artifact is None or not artifact.exists():
        return ("not_available", "none")
    return ("fixed_specification_base_seed_replication_available", artifact.as_posix())


def count_data_rows(path: Path) -> int:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def next_required_artifact(adversary_id: str, traces: list[dict[str, str]]) -> str:
    status, _, _ = executable_status(adversary_id)
    if status == "partial_executable_pilot_available":
        if adversary_id == "A7":
            return "extend to expanded/risk-routed mechanisms, seed and capacity sensitivity, and substantive correction"
        if adversary_id == "A8":
            return "extend to additional signal-dependent mechanisms, seed sensitivity, temporal correction, and external district-opinion validation"
        if adversary_id == "A9":
            return "vary allocation/resource/interaction specifications, broaden mechanisms, add substantive replay, and externally anchor assumptions"
        return "extend executable pilot to broader mechanisms, seed sensitivity, and recovery traces"
    if not traces:
        return "implement first explicit attacked cell with paired baseline"
    if adversary_id == "A6":
        return "replace defensive-backlash proxy with lobbying-camouflage adversary sweep"
    if adversary_id == "A9":
        return "replace open burden-shifting stress proxy with fixed-budget mixed-attack portfolio"
    return "run low/medium/high budget same-seed attack sweep with per-bill trace log"


def map_rows(catalog: list[dict[str, str]], traces: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = traces_by_adversary(traces)
    rows: list[dict[str, str]] = []
    for spec in catalog:
        adversary_id = spec["adversaryId"]
        mapped_traces = sorted(by_id.get(adversary_id, []), key=lambda row: int(row["trace_rank"]))
        pilot_success_flags = sum(row["pilot_success_flag"] == "yes" for row in mapped_traces)
        material_count = sum(row["severity"] == "material_pilot_degradation" for row in mapped_traces)
        executable_pilot_status, executable_summary_rows, executable_trace_artifact = executable_status(adversary_id)
        has_executable_pilot = executable_pilot_status == "partial_executable_pilot_available"
        replication_status, replication_artifact = seed_replication_status(adversary_id)
        rows.append({
            "adversary_id": adversary_id,
            "name": spec["name"],
            "actor_type": spec["actorType"],
            "pilot_cell_count": str(len(mapped_traces)),
            "pilot_trace_ranks": "; ".join(row["trace_rank"] for row in mapped_traces) or "none",
            "pilot_tests": "; ".join(row["test"] for row in mapped_traces) or "none",
            "pilot_status": pilot_status(adversary_id, mapped_traces),
            "pilot_success_flags": str(pilot_success_flags),
            "material_pilot_degradation_count": str(material_count),
            "executable_pilot_status": executable_pilot_status,
            "executable_summary_rows": executable_summary_rows,
            "executable_trace_artifact": executable_trace_artifact,
            "baseline_pairing_level": "same_generated_world_paired_trace_available" if has_executable_pilot else "aggregate_case_or_scenario_pair_only" if mapped_traces else "not_available",
            "budget_status": "low_medium_high_budget_cells_available" if has_executable_pilot else "not_budgeted",
            "information_status": information_status(adversary_id, has_executable_pilot),
            "attack_success_rate_status": "computed_for_executable_pilot" if has_executable_pilot else "not_computed",
            "worst_case_status": "computed_for_executable_pilot" if has_executable_pilot else "not_computed",
            "median_status": "computed_for_executable_pilot" if has_executable_pilot else "not_computed",
            "seed_replication_status": replication_status,
            "seed_replication_artifact": replication_artifact,
            "recovery_status": recovery_status(adversary_id, has_executable_pilot),
            "per_bill_trace_status": "available_for_executable_pilot" if has_executable_pilot else "not_available",
            "manuscript_gate": "not_ready",
            "next_required_artifact": next_required_artifact(adversary_id, mapped_traces),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    mapped_count = sum(row["pilot_cell_count"] != "0" for row in rows)
    executable_count = sum(row["executable_pilot_status"] == "partial_executable_pilot_available" for row in rows)
    lines = [
        "# Adversarial Pilot Cell Map",
        "",
        "This report maps the Java first-wave adversary catalog to the current aggregate manipulation-stress evidence and bounded executable pilot artifacts. It is a planning and readiness artifact, not a complete adversary experiment result.",
        "",
        f"- First-wave adversaries: {len(rows)}",
        f"- Adversaries with at least one aggregate pilot cell: {mapped_count}",
        f"- Adversaries without a current pilot cell: {len(rows) - mapped_count}",
        f"- Adversaries with partial executable pilots: {executable_count}",
        "- Manuscript-ready adversary rows: 0",
        "",
        f"Claim boundary: {CLAIM_BOUNDARY}",
        "",
        "| ID | Name | Aggregate cells | Executable status | Executable rows | Seed replication | Trace artifact | Next required artifact |",
        "| --- | --- | ---: | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['adversary_id']} | {escape(row['name'])} | {row['pilot_cell_count']} | "
            f"{row['executable_pilot_status']} | {row['executable_summary_rows']} | "
            f"{row['seed_replication_status']} | {escape(row['executable_trace_artifact'])} | "
            f"{escape(row['next_required_artifact'])} |"
        )
    lines.extend([
        "",
        "Gate status: every row remains `not_ready`. A1 through A9 have bounded executable pilots and A9 has fixed-specification 30-base-seed replication, but A1-A8 replication, broader mechanism coverage, alternative A9 specifications, temporal or substantive correction, and external validation remain incomplete.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n")


def escape(value: str) -> str:
    return value.replace("|", "\\|")


def main() -> int:
    catalog = read_csv(CATALOG)
    traces = read_csv(TRACE_INDEX)
    rows = map_rows(catalog, traces)
    if len(rows) != 9:
        raise SystemExit(f"Expected 9 first-wave adversary rows, got {len(rows)}.")
    write_outputs(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
