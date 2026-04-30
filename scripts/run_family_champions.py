#!/usr/bin/env python3
"""Run a supplemental breadth-catalog screen and summarize top family scenarios."""

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
        clamp01(float(row.get("legitimacy", 0.0))),
    ])
    risk = mean([
        inverse01(float(row["lowSupport"])),
        inverse01(float(row.get("weakPublicMandatePassage", 0.0))),
        inverse01(float(row.get("minorityHarm", 0.0))),
        inverse01(float(row["lobbyCapture"])),
        inverse01(float(row["publicPreferenceDistortion"])),
        inverse01(float(row.get("concentratedHarmPassage", 0.0))),
        inverse_range(float(row["proposerGain"])),
        inverse_range(float(row["policyShift"])),
    ])
    administrative_feasibility = inverse01(float(row.get("administrativeCost", 0.0)))
    return mean([productivity, representative, risk, administrative_feasibility])


def family_for(name: str) -> str:
    lower = name.lower()
    if "default pass" in lower:
        return "Default-pass side family"
    if "current" in lower or "u.s.-like" in lower or "congress" in lower or "bicameral" in lower or "veto" in lower:
        return "Conventional benchmark"
    if "leadership" in lower or "cloture" in lower or "conference" in lower or "judicial" in lower:
        return "Leadership and procedural veto points"
    if "initiative" in lower or "referendum" in lower:
        return "Direct democracy"
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
    if "portfolio" in lower or "hybrid" in lower:
        return "Portfolio hybrid"
    if "adaptive" in lower or "risk-routed" in lower or "strategy" in lower or "norm erosion" in lower or "deterioration" in lower:
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
        "# Family Scenario Screen",
        "",
        "Supplemental breadth-catalog screen over the runnable --all-scenarios set. Long default-pass parameter sweeps remain archived as explicit --scenarios keys, but are not included in this breadth screen.",
        "",
        "- Runs per scenario: 48",
        "- Legislators: 101",
        "- Bills per run: 60",
        "- Seed: 20260428",
        "- Selection rule: within each scenario family, the reported scenario has the highest directional score in this fixed baseline screen.",
        "",
        "| Family | Top scenario | Directional | Productivity | Compromise | Weak mandate | Admin cost | Welfare |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family in sorted(by_family):
        champion = max(by_family[family], key=lambda row: float(row["directionalScore"]))
        lines.append(
            f"| {family} | {champion['scenario']} | {float(champion['directionalScore']):.3f} | "
            f"{float(champion['productivity']):.3f} | {float(champion['compromise']):.3f} | "
            f"{float(champion.get('weakPublicMandatePassage', '0')):.3f} | "
            f"{float(champion.get('administrativeCost', '0')):.3f} | {float(champion['welfare']):.3f} |"
        )
    lines.extend([
        "",
        "The screen exists to reduce cherry-picking risk: the main paper reports a compact breadth-first campaign, while this supplement shows which breadth-catalog variants score highest under a fixed within-family rule.",
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
