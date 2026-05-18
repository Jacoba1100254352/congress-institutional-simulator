#!/usr/bin/env python3
"""Fail if generated review PDFs expose obvious local or author identity."""

from __future__ import annotations

import re
import subprocess
import sys
import hashlib
from pathlib import Path


DEFAULT_PDFS = [
    Path("paper/acm-ci-framework/acm-ci-framework.pdf"),
    Path("paper/technical-appendix/odd-d-appendix.pdf"),
]

HASHED_BANNED_TERMS = (
    (14, "f10f60a1f978030d3278bf2c22865cda980beb926d1d0c97c3e9c85ba9252238"),
    (17, "5d394ce4d14ef833bb98c1b71d7261b96298e805ff4319d9790119fe54c67994"),
    (13, "ca035de7d1f1c65ceb1493c7147ed1f0eeba3311af52e339a1913816879ffc43"),
    (14, "ef4fab81da95ac04aba973ee1192997ad0296a18b20c8153b68975969ae6de7d"),
    (16, "5a170c01d6f4f68b0b95ac4be9c138d40a104975671b607a50d42a6409e11aa0"),
    (11, "7510bdd3e5310ec7655ac4895dc39b099b1c2f6f337abd455d73043119daf8a8"),
)

BANNED_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+", re.IGNORECASE),
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


def pdf_metadata(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exception:
        raise SystemExit("pdfinfo is required for paper anonymity metadata checks.") from exception
    except subprocess.CalledProcessError as exception:
        raise SystemExit(f"Could not extract metadata from {path}: {exception.stderr}") from exception
    return completed.stdout


def pdf_raw_text(path: Path) -> str:
    return path.read_bytes().decode("latin-1", errors="ignore")


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


def main(argv: list[str]) -> int:
    pdfs = [Path(argument) for argument in argv] if argv else DEFAULT_PDFS
    failures: list[str] = []
    for pdf in pdfs:
        if not pdf.exists():
            failures.append(f"{pdf}: missing")
            continue
        text = pdf_text(pdf)
        metadata = pdf_metadata(pdf)
        raw_text = pdf_raw_text(pdf)
        for source_name, source_text in (
            ("text", text),
            ("metadata", metadata),
            ("raw PDF bytes", raw_text),
        ):
            hashed_match = contains_hashed_banned_term(source_text)
            if hashed_match:
                length, digest_prefix = hashed_match
                failures.append(
                    f"{pdf}: {source_name} matched hashed banned identity term "
                    f"(length={length}, hash={digest_prefix}...)"
                )
        for pattern in BANNED_PATTERNS:
            if pattern.search(text):
                failures.append(f"{pdf}: matched banned identity pattern {pattern.pattern!r}")
            if pattern.search(metadata):
                failures.append(f"{pdf}: metadata matched banned identity pattern {pattern.pattern!r}")
            if pattern.search(raw_text):
                failures.append(f"{pdf}: raw PDF bytes matched banned identity pattern {pattern.pattern!r}")

    if failures:
        print("Paper anonymity check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("Paper anonymity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
