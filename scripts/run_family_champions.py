#!/usr/bin/env python3
"""Run a supplemental all-catalog screen and summarize family champions."""

from __future__ import annotations

import csv
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_CSV = ROOT / "reports" / "all-scenarios-baseline.csv"
REPORT_MD = ROOT / "reports" / "family-champions.md"


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def inverse01(value: float) -> float:
    return 1.0 - clamp01(value)


def inverse_range(value: float, max_value: float = 2.0) -> float:
    return 1.0 - clamp01(value / max_value)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def directional_score(row: dict[str, str]) -> float:
    productivity = float(row["productivity"])
    representative = mean([
        clamp01(float(row["welfare"])),
        clamp01(float(row["avgSupport"])),
        clamp01(float(row["compromise"])),
        clamp01(float(row["publicAlignment"])),
    ])
    risk = mean([
        inverse01(float(row["lowSupport"])),
        inverse01(float(row["lobbyCapture"])),
        inverse01(float(row["publicPreferenceDistortion"])),
        inverse_range(float(row["proposerGain"])),
        inverse_range(float(row["policyShift"])),
    ])
    return mean([productivity, representative, risk])


def family_for(name: str) -> str:
    lower = name.lower()
    if "default pass" in lower:
        return "Default-pass side family"
    if "current" in lower or "u.s.-like" in lower or "bicameral" in lower or "veto" in lower:
        return "Conventional benchmark"
    if "supermajority" in lower or "60 percent" in lower or "simple majority" in lower or "unicameral simple" in lower:
        return "Conventional threshold"
    if "committee" in lower or "public-interest" in lower or "lottery" in lower:
        return "Agenda gate"
    if "coalition" in lower or "cross-bloc" in lower or "parliamentary" in lower:
        return "Coalition access"
    if "alternative" in lower or "tournament" in lower or "substitute" in lower:
        return "Policy tournament"
    if "citizen" in lower or "panel" in lower or "assembly" in lower:
        return "Citizen deliberation"
    if "attention" in lower or "credit" in lower or "bond" in lower or "quota" in lower:
        return "Agenda scarcity and accountability"
    if "harm" in lower or "compensation" in lower or "affected" in lower:
        return "Distributional justice"
    if "package" in lower or "mediation" in lower or "amendment" in lower:
        return "Content bargaining"
    if "registry" in lower or "sunset" in lower or "objection" in lower or "repeal" in lower:
        return "Reversibility and objection"
    if "lobby" in lower or "capture" in lower or "advocate" in lower or "voucher" in lower or "blind" in lower:
        return "Anti-capture"
    if "adaptive" in lower or "risk-routed" in lower or "strategy" in lower:
        return "Adaptive strategy"
    return "Other"


def run_all_scenarios() -> list[dict[str, str]]:
    java_props = os.environ.get("JAVA_PROPS", "-Dcongresssim.javaRelease=21").split()
    command = [
        "java",
        *java_props,
        "-cp",
        "out/main",
        "congresssim.Main",
        "--all-scenarios",
        "--runs",
        "48",
        "--legislators",
        "101",
        "--bills",
        "60",
        "--seed",
        "20260428",
        "--format",
        "csv",
    ]
    completed = subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
    rows = list(csv.DictReader(completed.stdout.splitlines()))
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", newline="") as handle:
        fieldnames = ["family", "directionalScore", *rows[0].keys()]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["family"] = family_for(row["scenario"])
            output["directionalScore"] = f"{directional_score(row):.6f}"
            writer.writerow(output)
    return rows


def write_summary(rows: list[dict[str, str]]) -> None:
    by_family: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        row = dict(row)
        row["family"] = family_for(row["scenario"])
        row["directionalScore"] = f"{directional_score(row):.6f}"
        by_family.setdefault(row["family"], []).append(row)

    lines = [
        "# Family Champion Screen",
        "",
        "Supplemental all-catalog screen over every explicit scenario key. This is a baseline screening run, not the paper's main evidence base.",
        "",
        "- Runs per scenario: 48",
        "- Legislators: 101",
        "- Bills per run: 60",
        "- Seed: 20260428",
        "- Selection rule: within each scenario family, the champion is the highest directional score in this fixed baseline screen.",
        "",
        "| Family | Champion | Directional | Productivity | Compromise | Low-support | Welfare |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family in sorted(by_family):
        champion = max(by_family[family], key=lambda row: float(row["directionalScore"]))
        lines.append(
            f"| {family} | {champion['scenario']} | {float(champion['directionalScore']):.3f} | "
            f"{float(champion['productivity']):.3f} | {float(champion['compromise']):.3f} | "
            f"{float(champion['lowSupport']):.3f} | {float(champion['welfare']):.3f} |"
        )
    lines.extend([
        "",
        "The screen exists to reduce cherry-picking risk: the main paper reports a compact breadth-first campaign, while this supplement shows which variants would win under a fixed within-family rule.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = run_all_scenarios()
    write_summary(rows)
    print(f"Wrote {REPORT_CSV}")
    print(f"Wrote {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
