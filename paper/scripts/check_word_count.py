#!/usr/bin/env python3
"""Check review-paper word count from a built PDF."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", nargs="?", default="paper/main.pdf")
    parser.add_argument("--max", type=int, default=6000)
    args = parser.parse_args()

    path = Path(args.pdf_path)
    if not path.exists():
        print(f"Paper PDF not found: {path}")
        return 2

    text = pdf_text(path)
    before_references = re.split(r"\n\s*References\s*\n", text, maxsplit=1)[0]
    count = len(WORD_RE.findall(before_references))
    print(f"Paper word count before references: {count} / {args.max}")
    if count > args.max:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
