#!/usr/bin/env python3
"""Basic sanity checks for generated LaTeX figure label placement."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
import sys
from pathlib import Path


FIGURES = [
    Path("paper/figures/productivity_low_support.tex"),
    Path("paper/figures/compromise_productivity.tex"),
    Path("paper/figures/chamber_productivity_compromise.tex"),
    Path("paper/figures/timeline_contention.tex"),
]
MIN_LABELS = {
    Path("paper/figures/productivity_low_support.tex"): 11,
    Path("paper/figures/compromise_productivity.tex"): 11,
    Path("paper/figures/chamber_productivity_compromise.tex"): 8,
    Path("paper/figures/timeline_contention.tex"): 6,
}

PICTURE_RE = re.compile(r"\\begin\{picture\}\(([-0-9.]+),([-0-9.]+)\)")
FIGURE_BOUNDS_RE = re.compile(r"% figure-bounds width=([-0-9.]+) height=([-0-9.]+)")
POINT_LABEL_RE = re.compile(
    r"% point-label label=(.*?) pointX=([-0-9.]+) pointY=([-0-9.]+) "
    r"labelX=([-0-9.]+) labelY=([-0-9.]+) anchor=([lrc]) leader=([01])"
)
LEGACY_LABEL_RE = re.compile(r"% (point|legend)-label label=(.*?) x=([-0-9.]+) y=([-0-9.]+)")
PUT_RE = re.compile(r"\\put\(([-0-9.]+),([-0-9.]+)\)")
POINT_RULE_RE = re.compile(r"\\rule\{([0-9.]+)mm\}\{\1mm\}")
LABEL_HEIGHT = 4.5
LABEL_MARGIN = 0.6
MAX_LABEL_DISTANCE = 42.0
LEADER_DISTANCE = 7.5


@dataclass(frozen=True)
class FigureLabel:
    label: str
    label_x: float
    label_y: float
    anchor: str
    point_x: float | None = None
    point_y: float | None = None
    leader: bool = False
    kind: str = "point"


def label_width(label: str) -> float:
    visible = re.sub(r"\\[A-Za-z]+|[{}$]", "", label)
    return max(4.2, len(visible) * 1.22)


def label_box(label: FigureLabel) -> tuple[float, float, float, float]:
    width = label_width(label.label)
    if label.anchor == "l":
        left = label.label_x
        right = label.label_x + width
    elif label.anchor == "r":
        left = label.label_x - width
        right = label.label_x
    else:
        left = label.label_x - width / 2.0
        right = label.label_x + width / 2.0
    return left, right, label.label_y - LABEL_HEIGHT / 2.0, label.label_y + LABEL_HEIGHT / 2.0


def expanded_box(box: tuple[float, float, float, float], padding_x: float = 0.45,
                 padding_y: float = 0.45) -> tuple[float, float, float, float]:
    left, right, bottom, top = box
    return left - padding_x, right + padding_x, bottom - padding_y, top + padding_y


def point_box(x: float, y: float) -> tuple[float, float, float, float]:
    return x - 1.7, x + 1.7, y - 1.7, y + 1.7


def boxes_overlap(left_a: float, right_a: float, bottom_a: float, top_a: float,
                  left_b: float, right_b: float, bottom_b: float, top_b: float) -> bool:
    return left_a < right_b and right_a > left_b and bottom_a < top_b and top_a > bottom_b


def parse_labels(text: str) -> list[FigureLabel]:
    labels = [
        FigureLabel(
            label=match.group(1).strip(),
            point_x=float(match.group(2)),
            point_y=float(match.group(3)),
            label_x=float(match.group(4)),
            label_y=float(match.group(5)),
            anchor=match.group(6),
            leader=match.group(7) == "1",
            kind="point",
        )
        for match in POINT_LABEL_RE.finditer(text)
    ]
    if labels:
        for match in LEGACY_LABEL_RE.finditer(text):
            if match.group(1) == "legend":
                labels.append(
                    FigureLabel(
                        label=match.group(2).strip(),
                        label_x=float(match.group(3)),
                        label_y=float(match.group(4)),
                        anchor="l",
                        kind="legend",
                    )
                )
        return labels
    return [
        FigureLabel(
            label=match.group(2).strip(),
            label_x=float(match.group(3)),
            label_y=float(match.group(4)),
            anchor="c" if match.group(1) == "point" else "l",
            kind=match.group(1),
        )
        for match in LEGACY_LABEL_RE.finditer(text)
    ]


def check_file(path: Path) -> list[str]:
    text = path.read_text()
    bounds = PICTURE_RE.search(text) or FIGURE_BOUNDS_RE.search(text)
    if not bounds:
        return [f"{path}: missing figure bounds"]
    width = float(bounds.group(1))
    height = float(bounds.group(2))
    failures: list[str] = []

    for match in PUT_RE.finditer(text):
        x = float(match.group(1))
        y = float(match.group(2))
        if x < -10.0 or x > width + 12.0 or y < -8.0 or y > height + 8.0:
            failures.append(f"{path}: put coordinate outside generous bounds ({x:.1f}, {y:.1f})")

    labels = parse_labels(text)
    minimum = MIN_LABELS.get(path)
    if minimum is not None and len(labels) < minimum:
        failures.append(f"{path}: expected at least {minimum} point labels, found {len(labels)}")
    seen_labels: set[str] = set()
    for label in labels:
        if label.label in seen_labels:
            failures.append(f"{path}: duplicate point label {label.label!r}")
        seen_labels.add(label.label)
    for label in labels:
        box = label_box(label)
        if (
            box[0] < LABEL_MARGIN
            or box[1] > width - LABEL_MARGIN
            or box[2] < LABEL_MARGIN
            or box[3] > height - LABEL_MARGIN
        ):
            failures.append(
                f"{path}: label {label.label!r} not fully visible "
                f"(box {box[0]:.1f}, {box[1]:.1f}, {box[2]:.1f}, {box[3]:.1f})"
            )

    rich_point_labels = [label for label in labels if label.kind == "point" and label.point_x is not None]
    if rich_point_labels:
        square_count = len(POINT_RULE_RE.findall(text))
        if square_count != len(rich_point_labels):
            failures.append(
                f"{path}: found {square_count} plotted point squares but "
                f"{len(rich_point_labels)} point labels"
            )
        point_boxes = [point_box(label.point_x or 0.0, label.point_y or 0.0) for label in rich_point_labels]
        for label in rich_point_labels:
            distance = math.hypot(label.label_x - (label.point_x or 0.0), label.label_y - (label.point_y or 0.0))
            if distance > MAX_LABEL_DISTANCE:
                failures.append(
                    f"{path}: label {label.label!r} is too far from its point ({distance:.1f}mm)"
                )
            if distance > LEADER_DISTANCE and not label.leader:
                failures.append(
                    f"{path}: label {label.label!r} needs a leader line at {distance:.1f}mm from its point"
                )
            label_bounds = expanded_box(label_box(label), padding_x=0.25, padding_y=0.25)
            for point in point_boxes:
                if boxes_overlap(*label_bounds, *point):
                    failures.append(f"{path}: label {label.label!r} overlaps a plotted point")
                    break

    for index, label_a in enumerate(labels):
        box_a = expanded_box(label_box(label_a))
        for label_b in labels[index + 1:]:
            box_b = expanded_box(label_box(label_b))
            if boxes_overlap(*box_a, *box_b):
                failures.append(
                    f"{path}: point labels {label_a.label!r} and {label_b.label!r} overlap "
                    f"(({label_a.label_x:.1f}, {label_a.label_y:.1f}) vs "
                    f"({label_b.label_x:.1f}, {label_b.label_y:.1f}))"
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
