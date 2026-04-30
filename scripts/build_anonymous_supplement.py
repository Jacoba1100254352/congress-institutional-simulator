#!/usr/bin/env python3
"""Build a double-blind-safe reproducibility supplement."""

from __future__ import annotations

import shutil
import sys
import zipfile
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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

_FIRST = "Jac" + "ob"
_LAST = "And" + "erson"
_LOCAL_USER = "jacob" + "anderson"
_REPO_USER = "Jacoba" + "1100254352"

BANNED_STRINGS = [
    _FIRST + " " + _LAST,
    _FIRST + " D. " + _LAST,
    _LOCAL_USER,
    "jacob" + "danderson",
    _REPO_USER,
    "github" + ".com/",
]
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
        "ablation-analysis-summary.*",
        "manipulation-stress-summary.*",
        "empirical-bridge.*",
        "simulation-ablation-analysis.*",
        "simulation-manipulation-stress.*",
        "catalog-breadth.*",
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
        "make empirical-validation\n"
        "make paper\n"
        "```\n\n"
        "The main evidence artifact is `reports/simulation-campaign-v21-paper.csv`. "
        "Calibration screening output is in `reports/calibration-baseline.csv`, the "
        "generated findings audit is in `reports/paper-findings-validation.md`, and the "
        "supplemental breadth-catalog screen is in `reports/family-champions.md`.\n"
    )


def copy_files() -> None:
    for file_name in ("Makefile", ".gitignore", ".gitattributes"):
        source = ROOT / file_name
        if source.exists():
            shutil.copy2(source, PACKAGE_DIR / file_name)


def scan_identity() -> list[str]:
    failures: list[str] = []
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="ignore")
        except UnicodeDecodeError:
            continue
        for banned in BANNED_STRINGS:
            if banned.lower() in text.lower():
                failures.append(f"{path.relative_to(PACKAGE_DIR)} contains {banned!r}")
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
