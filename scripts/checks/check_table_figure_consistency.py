#!/usr/bin/env python3
"""Check that generated paper tables and scatter figures describe the same scenarios."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TABLE = Path("paper/figures/scenario_averages_table.tex")
SCATTERS = [
    Path("paper/figures/productivity_low_support.tex"),
    Path("paper/figures/compromise_productivity.tex"),
]


LABEL_RE = re.compile(r"% point-label label=(.*?) x=([-0-9.]+) y=([-0-9.]+)")
ROW_RE = re.compile(r"^\s*(.*?)\s*&\s*(.*?)\s*&")


def normalize_label(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\\textcolor\{[^}]+\}\{\\textbf\{([^}]*)\}\}", r"\1", value)
    value = re.sub(r"\\textbf\{([^}]*)\}", r"\1", value)
    value = re.sub(r"\\[A-Za-z]+\{([^}]*)\}", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def table_labels() -> set[str]:
    if not TABLE.exists():
        raise FileNotFoundError(TABLE)
    labels: set[str] = set()
    for line in TABLE.read_text().splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        label = normalize_label(match.group(1))
        if not label or label in {"Label", "\\toprule", "\\midrule", "\\bottomrule"}:
            continue
        labels.add(label)
    return labels


def scatter_labels(path: Path) -> set[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    return {match.group(1).strip() for match in LABEL_RE.finditer(path.read_text())}


def count_point_squares(path: Path) -> int:
    text = path.read_text()
    return len(re.findall(r"\\rule\{(?:1\.5|1\.7|1\.9|2\.0)mm\}\{(?:1\.5|1\.7|1\.9|2\.0)mm\}", text))


def main() -> int:
    failures: list[str] = []
    try:
        labels = table_labels()
    except FileNotFoundError:
        failures.append(f"{TABLE}: missing")
        labels = set()

    if "CUR" not in labels:
        failures.append("scenario table is missing CUR benchmark label")
    table_text = TABLE.read_text() if TABLE.exists() else ""
    if "textcolor{red}" not in table_text or "CUR" not in table_text:
        failures.append("scenario table does not visibly mark CUR in red")

    for scatter in SCATTERS:
        try:
            figure_labels = scatter_labels(scatter)
        except FileNotFoundError:
            failures.append(f"{scatter}: missing")
            continue
        missing = labels - figure_labels
        extra = figure_labels - labels
        if missing:
            failures.append(f"{scatter}: labels missing from figure: {', '.join(sorted(missing))}")
        if extra:
            failures.append(f"{scatter}: figure labels missing from table: {', '.join(sorted(extra))}")
        square_count = count_point_squares(scatter)
        if square_count != len(figure_labels):
            failures.append(f"{scatter}: found {square_count} plotted squares but {len(figure_labels)} point labels")
        text = scatter.read_text()
        if "\\color{red}" not in text or "label=CUR" not in text:
            failures.append(f"{scatter}: CUR benchmark is not visibly marked in red")

    if failures:
        print("Table/figure consistency check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print("Table/figure consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
