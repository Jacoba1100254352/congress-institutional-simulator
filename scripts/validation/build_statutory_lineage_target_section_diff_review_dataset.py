#!/usr/bin/env python3
"""Synchronize curated target-section diff reviews with refreshed packet ranks."""

from __future__ import annotations

import csv
from pathlib import Path


RAW_REVIEW = Path("data/validation/raw/statutory_lineage_target_section_diff_review.csv")
PACKETS_RAW = Path("data/validation/raw/statutory_lineage_target_review_packets.csv")
OUT_METADATA = Path("data/validation/raw/statutory_lineage_target_section_diff_review.metadata.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"{path} is missing.")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def packet_key(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        row.get("bill_id", "").strip(),
        row.get("public_law_number", "").strip(),
        row.get("target_reference", "").strip(),
        row.get("pre_olrc_url", "").strip(),
        row.get("post_olrc_url", "").strip(),
    )


def packet_rows_by_key(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = packet_key(row)
        if not all(key):
            continue
        if key in result:
            raise SystemExit(f"{PACKETS_RAW}: duplicate packet key {key}")
        result[key] = row
    return result


def synchronized_rows(review_rows: list[dict[str, str]], packet_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    packet_by_key = packet_rows_by_key(packet_rows)
    rows: list[dict[str, str]] = []
    missing: list[str] = []
    for row in review_rows:
        packet = packet_by_key.get(packet_key(row))
        if not packet:
            missing.append(
                f"review_rank={row.get('review_rank', '').strip()} "
                f"bill_id={row.get('bill_id', '').strip()} "
                f"target_reference={row.get('target_reference', '').strip()}"
            )
            continue
        updated = dict(row)
        updated["target_review_packet_rank"] = packet.get("target_review_packet_rank", "").strip()
        rows.append(updated)
    if missing:
        raise SystemExit(
            f"{RAW_REVIEW}: {len(missing)} curated review row(s) lack refreshed packet matches: "
            + "; ".join(missing[:10])
        )
    return rows


def write_metadata(rows: list[dict[str, str]]) -> None:
    OUT_METADATA.write_text(
        "\n".join([
            "# Statutory Lineage Target-Section Diff Review Metadata",
            "",
            "Curated target-section diff review rows synchronized against refreshed target-review packet ranks.",
            "",
            f"- Raw review rows: {len(rows)}",
            f"- Packet source: `{PACKETS_RAW}`",
            "",
            "Claim boundary: source-reviewed target-section diff disposition only; synchronization updates packet ranks but does not establish public-law causal attribution, implementation outcomes, court review, welfare, causal effects, or model validation.",
        ])
        + "\n"
    )


def main() -> int:
    review_rows = read_csv(RAW_REVIEW)
    if not review_rows:
        raise SystemExit(f"{RAW_REVIEW} is empty.")
    packet_rows = read_csv(PACKETS_RAW)
    if not packet_rows:
        raise SystemExit(f"{PACKETS_RAW} is empty.")
    rows = synchronized_rows(review_rows, packet_rows)
    write_csv(RAW_REVIEW, rows, list(review_rows[0]))
    write_metadata(rows)
    print(f"Wrote {RAW_REVIEW}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
