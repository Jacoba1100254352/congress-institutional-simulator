#!/usr/bin/env python3
"""Render review PDFs and fail on obviously blank or malformed pages."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_PDFS = [
    Path("paper/main.pdf"),
    Path("paper/appendix-odd-d.pdf"),
]
OUT_DIR = Path("out/pdf-render-check")


def pdf_page_count(path: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not find page count for {path}.")
    return int(match.group(1))


def parse_ppm(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    index = 0

    def token() -> bytes:
        nonlocal index
        while index < len(data) and data[index:index + 1].isspace():
            index += 1
        if index < len(data) and data[index:index + 1] == b"#":
            while index < len(data) and data[index:index + 1] not in b"\r\n":
                index += 1
            return token()
        start = index
        while index < len(data) and not data[index:index + 1].isspace():
            index += 1
        return data[start:index]

    magic = token()
    if magic != b"P6":
        raise RuntimeError(f"{path}: expected binary PPM P6, found {magic!r}.")
    width = int(token())
    height = int(token())
    max_value = int(token())
    if max_value != 255:
        raise RuntimeError(f"{path}: expected max value 255, found {max_value}.")
    while index < len(data) and data[index:index + 1].isspace():
        index += 1
    pixels = data[index:]
    expected = width * height * 3
    if len(pixels) != expected:
        raise RuntimeError(f"{path}: expected {expected} bytes of pixels, found {len(pixels)}.")
    return width, height, pixels


def page_stats(path: Path) -> tuple[int, int, float, float, float]:
    width, height, pixels = parse_ppm(path)
    sample_count = len(pixels)
    mean = sum(pixels) / sample_count
    variance = sum((byte - mean) ** 2 for byte in pixels) / sample_count
    dark_ratio = sum(1 for byte in pixels if byte < 80) / sample_count
    return width, height, mean, variance, dark_ratio


def check_pdf(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"{path}: missing"]
    page_count = pdf_page_count(path)
    pages_to_check = min(page_count, 3)
    for page in range(1, pages_to_check + 1):
        output_base = OUT_DIR / f"{path.stem}-page-{page}"
        subprocess.run(
            [
                "pdftoppm",
                "-r",
                "72",
                "-f",
                str(page),
                "-l",
                str(page),
                "-singlefile",
                str(path),
                str(output_base),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        width, height, mean, variance, dark_ratio = page_stats(output_base.with_suffix(".ppm"))
        if width < 400 or height < 500:
            failures.append(f"{path}: page {page} rendered too small ({width}x{height}).")
        if mean > 253.8 or variance < 12.0 or dark_ratio < 0.00015:
            failures.append(
                f"{path}: page {page} appears blank or unreadable "
                f"(mean={mean:.2f}, variance={variance:.2f}, darkRatio={dark_ratio:.5f})."
            )
    return failures


def main(argv: list[str]) -> int:
    if shutil.which("pdftoppm") is None:
        raise SystemExit("pdftoppm is required for PDF render checks.")
    if shutil.which("pdfinfo") is None:
        raise SystemExit("pdfinfo is required for PDF render checks.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = [Path(argument) for argument in argv] if argv else DEFAULT_PDFS
    failures: list[str] = []
    for pdf in pdfs:
        failures.extend(check_pdf(pdf))
    if failures:
        print("PDF render check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("PDF render check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
