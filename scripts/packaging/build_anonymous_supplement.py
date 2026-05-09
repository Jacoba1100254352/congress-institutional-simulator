#!/usr/bin/env python3
"""Build a double-blind-safe reproducibility supplement."""

from __future__ import annotations

import shutil
import sys
import zipfile
import re
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
PACKAGE_NAME = "congress-institutional-simulator-anonymous"
PACKAGE_DIR = DIST / "anonymous-supplement" / PACKAGE_NAME
ZIP_PATH = DIST / f"{PACKAGE_NAME}.zip"

TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".java",
    ".json",
    ".md",
    ".py",
    ".tex",
    ".txt",
    ".yml",
    ".yaml",
    "",
}

HASHED_BANNED_TERMS = (
    (14, "f10f60a1f978030d3278bf2c22865cda980beb926d1d0c97c3e9c85ba9252238"),
    (17, "5d394ce4d14ef833bb98c1b71d7261b96298e805ff4319d9790119fe54c67994"),
    (13, "ca035de7d1f1c65ceb1493c7147ed1f0eeba3311af52e339a1913816879ffc43"),
    (14, "ef4fab81da95ac04aba973ee1192997ad0296a18b20c8153b68975969ae6de7d"),
    (16, "5a170c01d6f4f68b0b95ac4be9c138d40a104975671b607a50d42a6409e11aa0"),
    (11, "7510bdd3e5310ec7655ac4895dc39b099b1c2f6f337abd455d73043119daf8a8"),
)
BANNED_REGEXES = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
]


def ignore_names(directory: str, names: list[str]) -> set[str]:
    ignored = {
        ".DS_Store",
        ".git",
        ".idea",
        "build",
        "out",
        "dist",
        "no-include",
        "ACM-README",
    }
    return {name for name in names if name in ignored}


def copy_tree(name: str) -> None:
    source = ROOT / name
    target = PACKAGE_DIR / name
    shutil.copytree(source, target, ignore=ignore_names)


def copy_reports() -> None:
    source = ROOT / "reports"
    target = PACKAGE_DIR / "reports"
    target.mkdir(parents=True, exist_ok=True)
    for pattern in (
        "calibration-baseline.*",
        "simulation-campaign-v21-paper.*",
        "seed-robustness-summary.*",
        "paper-findings-validation.*",
        "all-scenarios-baseline.*",
        "family-champions.*",
        "representative-vs-family-champions.*",
        "ablation-analysis-summary.*",
        "manipulation-stress-summary.*",
        "empirical-bridge.*",
        "simulation-ablation-analysis.*",
        "simulation-manipulation-stress.*",
        "simulation-chamber-structure.*",
        "chamber-family-champions.*",
        "chamber-stress-screen.*",
        "catalog-breadth.*",
        "scenario-selection-manifest.*",
        "core-raw-validation-build.*",
        "empirical-validation-readiness.*",
        "empirical-validation-summary.*",
    ):
        for path in source.glob(pattern):
            if path.is_file():
                shutil.copy2(path, target / path.name)


def write_readme() -> None:
    (PACKAGE_DIR / "README.md").write_text(
        "# Anonymous Reproducibility Supplement\n\n"
        "This double-blind supplement contains source code, generated reports, LaTeX paper sources, "
        "paper PDFs, and scripts for the legislative mechanism-search simulator.\n\n"
        "Useful commands:\n\n"
        "```sh\n"
        "make test\n"
        "make calibration-check\n"
        "make seed-robustness\n"
        "make findings-validation\n"
        "make family-screen\n"
        "make catalog-breadth\n"
        "make chamber-structure\n"
        "make build-core-raw-validation ARGS=\"--derive-congress-from-bill-progression\"\n"
        "make empirical-validation\n"
        "make paper\n"
        "```\n\n"
        "The main evidence artifact is the generated main comparison campaign under `reports/`. "
        "Calibration screening output is in `reports/calibration-baseline.csv`, the "
        "generated findings audit is in `reports/paper-findings-validation.md`, and the "
        "supplemental breadth-catalog screen is in `reports/family-champions.md`, "
        "representative selection audit is in `reports/representative-vs-family-champions.md`, "
        "scenario-selection rationale is in `reports/scenario-selection-manifest.md`, "
        "the chamber-structure supplement is in `reports/chamber-family-champions.md`, "
        "and the raw-validation build summary is in `reports/core-raw-validation-build.md`.\n"
    )


def copy_files() -> None:
    for file_name in ("Makefile", ".gitignore", ".gitattributes"):
        source = ROOT / file_name
        if source.exists():
            shutil.copy2(source, PACKAGE_DIR / file_name)


def contains_hashed_banned_term(text: str) -> tuple[int, str] | None:
    normalized = text.lower()
    for length, expected_hash in HASHED_BANNED_TERMS:
        if len(normalized) < length:
            continue
        for index in range(0, len(normalized) - length + 1):
            candidate = normalized[index:index + length]
            digest = hashlib.sha256(candidate.encode()).hexdigest()
            if digest == expected_hash:
                return length, expected_hash[:12]
    return None


def scan_identity() -> list[str]:
    failures: list[str] = []
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="ignore")
        except UnicodeDecodeError:
            continue
        hashed_match = contains_hashed_banned_term(text)
        if hashed_match:
            length, digest_prefix = hashed_match
            failures.append(
                f"{path.relative_to(PACKAGE_DIR)} contains hashed banned identity term "
                f"(length={length}, hash={digest_prefix}...)"
            )
        for pattern in BANNED_REGEXES:
            if pattern.search(text):
                failures.append(f"{path.relative_to(PACKAGE_DIR)} matches {pattern.pattern!r}")
    return failures


def zip_package() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_DIR.parent))


def main() -> int:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    for directory in ("src", "data", "paper", "scripts", ".github"):
        copy_tree(directory)
    copy_reports()
    copy_files()
    write_readme()

    failures = scan_identity()
    if failures:
        print("Anonymous supplement identity scan failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    zip_package()
    print(f"Wrote {ZIP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
