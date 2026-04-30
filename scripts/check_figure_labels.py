#!/usr/bin/env python3
"""Basic sanity checks for generated LaTeX figure label placement."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FIGURES = [
    Path("paper/figures/productivity_low_support.tex"),
    Path("paper/figures/compromise_productivity.tex"),
    Path("paper/figures/timeline_contention.tex"),
]

PICTURE_RE = re.compile(r"\\begin\{picture\}\(([-0-9.]+),([-0-9.]+)\)")
POINT_LABEL_RE = re.compile(r"% point-label label=(.*?) x=([-0-9.]+) y=([-0-9.]+)")
PUT_RE = re.compile(r"\\put\(([-0-9.]+),([-0-9.]+)\)")


def label_width(label: str) -> float:
    visible = re.sub(r"\\[A-Za-z]+|[{}$]", "", label)
    return max(3.2, len(visible) * 1.05)


def check_file(path: Path) -> list[str]:
    text = path.read_text()
    picture = PICTURE_RE.search(text)
    if not picture:
        return [f"{path}: missing picture bounds"]
    width = float(picture.group(1))
    height = float(picture.group(2))
    failures: list[str] = []

    for match in PUT_RE.finditer(text):
        x = float(match.group(1))
        y = float(match.group(2))
        if x < -10.0 or x > width + 12.0 or y < -8.0 or y > height + 8.0:
            failures.append(f"{path}: put coordinate outside generous bounds ({x:.1f}, {y:.1f})")

    labels = [
        (match.group(1), float(match.group(2)), float(match.group(3)))
        for match in POINT_LABEL_RE.finditer(text)
    ]
    for label, x, y in labels:
        if x < 0.0 or x > width or y < 0.0 or y > height:
            failures.append(f"{path}: label {label!r} outside picture bounds ({x:.1f}, {y:.1f})")

    for index, (label_a, x_a, y_a) in enumerate(labels):
        width_a = label_width(label_a)
        for label_b, x_b, y_b in labels[index + 1:]:
            width_b = label_width(label_b)
            x_overlap = abs(x_a - x_b) < ((width_a + width_b) / 2.0)
            y_overlap = abs(y_a - y_b) < 3.4
            if x_overlap and y_overlap:
                failures.append(
                    f"{path}: point labels {label_a!r} and {label_b!r} are too close "
                    f"(({x_a:.1f}, {y_a:.1f}) vs ({x_b:.1f}, {y_b:.1f}))"
                )
    return failures


def main(argv: list[str]) -> int:
    figures = [Path(argument) for argument in argv] if argv else FIGURES
    failures: list[str] = []
    for figure in figures:
        if not figure.exists():
            failures.append(f"{figure}: missing")
            continue
        failures.extend(check_file(figure))

    if failures:
        print("Figure label check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("Figure label check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
