#!/usr/bin/env python3
"""Fail when an executable calibration report contains failing checks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?", default="reports/calibration-baseline.csv")
    args = parser.parse_args()

    path = Path(args.csv_path)
    if not path.exists():
        print(f"Calibration report not found: {path}")
        return 2

    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    failing = [row for row in rows if row.get("passed", "").lower() != "true"]
    if failing:
        print(f"Calibration failed: {len(failing)} / {len(rows)} checks did not pass.")
        for row in failing:
            print(
                f"- {row.get('key', '<unknown>')}: observed {row.get('observed')} "
                f"outside {row.get('minimum')}--{row.get('maximum')}"
            )
        return 1

    print(f"Calibration passed: {len(rows)} / {len(rows)} checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
