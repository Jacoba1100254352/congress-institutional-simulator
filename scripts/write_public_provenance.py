#!/usr/bin/env python3
"""Write a non-anonymous provenance manifest for public releases."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "public-provenance-manifest.json"
ARTIFACTS = [
    "reports/simulation-campaign-v21-paper.csv",
    "reports/calibration-baseline.csv",
    "reports/seed-robustness-summary.csv",
    "reports/paper-findings-validation.md",
    "reports/family-champions.md",
    "paper/main.pdf",
    "paper/appendix-odd-d.pdf",
]


def run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def run_command(*args: str) -> str:
    try:
        completed = subprocess.run(
            list(args),
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return (completed.stdout + completed.stderr).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_hashes() -> dict[str, dict[str, object]]:
    hashes: dict[str, dict[str, object]] = {}
    for relative in ARTIFACTS:
        path = ROOT / relative
        if path.exists():
            hashes[relative] = {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
    return hashes


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "git": {
            "commit": run_git("rev-parse", "HEAD"),
            "branch": run_git("rev-parse", "--abbrev-ref", "HEAD"),
            "describe": run_command("git", "describe", "--tags", "--always", "--dirty"),
            "dirty": bool(run_git("status", "--porcelain")),
        },
        "runtime": {
            "java": run_command("java", "-version"),
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "commands": {
            "campaign": "make paper-campaign",
            "calibration": "make calibration-check",
            "seedRobustness": "make seed-robustness-check",
            "paper": "make paper-checks",
        },
        "artifacts": artifact_hashes(),
        "note": "This manifest is for public, non-anonymous release packages and is intentionally excluded from the double-blind supplement.",
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
