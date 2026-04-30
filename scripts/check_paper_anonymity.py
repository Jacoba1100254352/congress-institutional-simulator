#!/usr/bin/env python3
"""Fail if generated review PDFs expose obvious local or author identity."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


DEFAULT_PDFS = [
    Path("paper/main.pdf"),
    Path("paper/appendix-odd-d.pdf"),
]

_FIRST = "Jac" + "ob"
_LAST = "And" + "erson"
_LOCAL_USER = "jacob" + "anderson"
_DOMAIN = "github" + ".com/"
_REPO_USER = "Jacoba" + "1100254352"

BANNED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        _FIRST + r"\s+D\.?\s+" + _LAST,
        _FIRST + r"\s+" + _LAST,
        _LOCAL_USER,
        "jacob" + "danderson",
        _REPO_USER,
        re.escape(_DOMAIN),
        r"/Users/[A-Za-z0-9._-]+",
    )
]


def pdf_text(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", str(path), "-"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exception:
        raise SystemExit("pdftotext is required for paper anonymity checks.") from exception
    except subprocess.CalledProcessError as exception:
        raise SystemExit(f"Could not extract text from {path}: {exception.stderr}") from exception
    return completed.stdout


def main(argv: list[str]) -> int:
    pdfs = [Path(argument) for argument in argv] if argv else DEFAULT_PDFS
    failures: list[str] = []
    for pdf in pdfs:
        if not pdf.exists():
            failures.append(f"{pdf}: missing")
            continue
        text = pdf_text(pdf)
        for pattern in BANNED_PATTERNS:
            if pattern.search(text):
                failures.append(f"{pdf}: matched banned identity pattern {pattern.pattern!r}")

    if failures:
        print("Paper anonymity check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("Paper anonymity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
