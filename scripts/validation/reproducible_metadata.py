#!/usr/bin/env python3
"""Write metadata without changing files for timestamp-only rebuilds."""

from __future__ import annotations

from pathlib import Path


TIMESTAMP_PREFIXES = (
    "Generated:",
    "- generated_at_utc:",
)


def write_reproducible_metadata(path: Path, content: str) -> bool:
    """Write metadata unless only its generated timestamp changed.

    Returns ``True`` when the file was created or substantively updated. If an
    existing file differs only in a generated-time line, its original bytes are
    retained so clean-checkout regeneration remains deterministic.
    """

    if path.exists():
        existing = path.read_text()
        if normalized_metadata(existing) == normalized_metadata(content):
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def normalized_metadata(content: str) -> str:
    return "\n".join(
        "<generated-timestamp>"
        if line.startswith(TIMESTAMP_PREFIXES)
        else line
        for line in content.splitlines()
    )
