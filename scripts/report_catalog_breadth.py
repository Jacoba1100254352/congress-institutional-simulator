#!/usr/bin/env python3
"""Report breadth-first versus historical scenario catalog composition."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "src/main/java/congresssim/simulation/ScenarioCatalog.java"
REPORT = ROOT / "reports/catalog-breadth.md"


def historical_keys() -> list[str]:
    text = CATALOG.read_text()
    return re.findall(r'new ScenarioEntry\("([^"]+)"', text)


def breadth_keys() -> list[str]:
    text = CATALOG.read_text()
    match = re.search(r"DEFAULT_SCENARIO_KEYS\s*=\s*List\.of\((.*?)\);", text, re.DOTALL)
    default_keys = set(re.findall(r'"([^"]+)"', match.group(1))) if match else set()
    return [key for key in historical_keys() if not key.startswith("default-pass") or key in default_keys]


def family(key: str) -> str:
    if key.startswith("default-pass"):
        return "Default-pass archived/stress"
    if key in {"current-system", "current-congress-workflow", "simple-majority", "supermajority-60", "bicameral-majority", "presidential-veto"}:
        return "Conventional benchmark"
    if any(token in key for token in ["equal-population", "proportional-house", "malapportioned-upper", "appointed-upper", "chamber-incongruence"]):
        return "Chamber apportionment"
    if any(token in key for token in ["origin-routing", "preclearance", "navette", "joint-sitting", "upper-", "last-offer", "lower-override", "routing"]):
        return "Chamber routing/conflict"
    if any(token in key for token in ["eligibility", "appointment-retention", "recusal-cooling"]):
        return "Selection/retention"
    if any(token in key for token in ["exante", "insulation"]):
        return "Independent review"
    if "leadership" in key or "cloture" in key or "committee" in key:
        return "Leadership/procedure"
    if "initiative" in key:
        return "Direct democracy"
    if "parliamentary" in key or "coalition" in key:
        return "Coalition/parliamentary"
    if "alternative" in key:
        return "Policy tournament"
    if "citizen" in key or "public-interest" in key:
        return "Citizen/public review"
    if "lottery" in key or "attention" in key or "bond" in key or "credit" in key:
        return "Attention scarcity"
    if "harm" in key or "compensation" in key or "affected" in key:
        return "Distributional justice"
    if "package" in key or "mediation" in key:
        return "Bargaining/amendment"
    if "registry" in key or "objection" in key or "sunset" in key or "repeal" in key:
        return "Reversibility"
    if "lobby" in key or "capture" in key:
        return "Anti-capture"
    if "portfolio" in key or "hybrid" in key:
        return "Portfolio hybrid"
    if "adaptive" in key or "risk" in key or "norm" in key or "strategy" in key or "deterioration" in key:
        return "Adaptive/stress"
    return "Other"


def write_report(historical: list[str], breadth: list[str]) -> None:
    archived_default = [key for key in historical if key.startswith("default-pass") and key not in set(breadth)]
    lines = [
        "# Scenario Catalog Breadth",
        "",
        "The Java catalog preserves historical default-pass parameter sweeps as addressable scenario keys, but `--all-scenarios` now runs a breadth-first screen: every non-default explicit key plus the small default-pass stress-test family used by the paper.",
        "",
        f"- Historical explicit keys: {len(historical)}",
        f"- Breadth-screen keys run by `--all-scenarios`: {len(breadth)}",
        f"- Archived default-pass keys excluded from `--all-scenarios`: {len(archived_default)}",
        "",
        "| Breadth family | Count |",
        "| --- | ---: |",
    ]
    counts = Counter(family(key) for key in breadth)
    for name, count in sorted(counts.items()):
        lines.append(f"| {name} | {count} |")
    lines.extend([
        "",
        "Archived default-pass variants remain reproducible through `--scenarios <key>` and the historical v0--v20 campaign targets, but they no longer dominate the catalog-level breadth screen.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> int:
    historical = historical_keys()
    breadth = breadth_keys()
    write_report(historical, breadth)
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
