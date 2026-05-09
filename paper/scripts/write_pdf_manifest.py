#!/usr/bin/env python3
"""Write or verify a deterministic manifest for the paper PDFs.

Raw PDF bytes can vary across TeX/font environments, so CI does not treat PDF
byte diffs as the canonical freshness signal. This manifest records stable
source-input and extracted-text hashes for the checked-in review PDFs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "paper" / "pdf-manifest.json"
PDF_PATHS = [
    ROOT / "paper" / "main.pdf",
    ROOT / "paper" / "appendix-odd-d.pdf",
]
INPUT_PATTERNS = [
    "Makefile",
    "data/calibration/*.csv",
    "data/validation/**/*.csv",
    "paper/*.tex",
    "paper/*.bib",
    "paper/*.bst",
    "paper/acmart.cls",
    "paper/figures/*.tex",
    "paper/scripts/*.py",
    "reports/ablation-analysis-summary.csv",
    "reports/all-scenarios-baseline.csv",
    "reports/chamber-family-champions.md",
    "reports/chamber-stress-screen.md",
    "reports/empirical-bridge.csv",
    "reports/empirical-validation-readiness.md",
    "reports/empirical-validation-summary.csv",
    "reports/family-champions.md",
    "reports/manipulation-stress-summary.csv",
    "reports/scenario-selection-manifest.md",
    "reports/seed-robustness-summary.csv",
    "reports/simulation-ablation-analysis.csv",
    "reports/simulation-campaign-v21-paper.csv",
    "reports/simulation-chamber-structure.csv",
    "reports/simulation-manipulation-stress.csv",
    "scripts/checks/*.py",
    "scripts/packaging/*.py",
    "scripts/reporting/*.py",
    "scripts/validation/*.py",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def unique_paths(patterns: Iterable[str]) -> list[Path]:
    paths: dict[str, Path] = {}
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file():
                paths[rel(path)] = path
    return [paths[key] for key in sorted(paths)]


def pdf_text(path: Path) -> str:
    completed = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    text = completed.stdout.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse whitespace so line-wrapping differences do not create false drift.
    return re.sub(r"\s+", " ", text).strip()


def pdf_pages(path: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not determine page count for {path}.")
    return int(match.group(1))


def source_manifest() -> tuple[str, list[dict[str, str]]]:
    entries = [
        {
            "path": rel(path),
            "sha256": file_sha256(path),
        }
        for path in unique_paths(INPUT_PATTERNS)
    ]
    digest_input = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(digest_input), entries


def build_manifest() -> dict[str, object]:
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext is required to write the PDF manifest.")
    if shutil.which("pdfinfo") is None:
        raise SystemExit("pdfinfo is required to write the PDF manifest.")

    source_hash, source_files = source_manifest()
    pdfs = []
    for path in PDF_PATHS:
        if not path.exists():
            raise SystemExit(f"{rel(path)} is missing; run `make paper` first.")
        text = pdf_text(path)
        pdfs.append({
            "path": rel(path),
            "pages": pdf_pages(path),
            "sizeBytes": path.stat().st_size,
            "normalizedTextSha256": sha256_bytes(text.encode()),
            "normalizedTextBytes": len(text.encode()),
        })
    return {
        "schema": 1,
        "generatedBy": "paper/scripts/write_pdf_manifest.py",
        "sourceInputSha256": source_hash,
        "sourceInputs": source_files,
        "pdfs": pdfs,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the checked-in manifest is stale")
    args = parser.parse_args(argv)

    expected = build_manifest()
    rendered = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not MANIFEST_PATH.exists():
            print(f"{rel(MANIFEST_PATH)} is missing; run `make paper`.", file=sys.stderr)
            return 1
        current = MANIFEST_PATH.read_text()
        if current != rendered:
            print(f"{rel(MANIFEST_PATH)} is stale; run `make paper` and commit the updated PDF artifacts.", file=sys.stderr)
            return 1
        print("PDF manifest check passed.")
        return 0

    MANIFEST_PATH.write_text(rendered)
    print(f"Wrote {rel(MANIFEST_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
