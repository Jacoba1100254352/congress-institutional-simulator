#!/usr/bin/env python3
"""Regression tests for deterministic generated metadata."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from reproducible_metadata import write_reproducible_metadata


class ReproducibleMetadataTests(unittest.TestCase):
    def test_timestamp_only_change_preserves_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "metadata.md"
            original = "# Metadata\n\nGenerated: 2026-01-01T00:00:00Z\n\nRows: 4\n"
            path.write_text(original)

            changed = write_reproducible_metadata(
                path,
                "# Metadata\n\nGenerated: 2026-02-01T00:00:00Z\n\nRows: 4\n",
            )

            self.assertFalse(changed)
            self.assertEqual(original, path.read_text())

    def test_substantive_change_updates_file_and_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "metadata.md"
            path.write_text(
                "# Metadata\n\n- generated_at_utc: 2026-01-01T00:00:00Z\nRows: 4\n"
            )
            replacement = (
                "# Metadata\n\n- generated_at_utc: 2026-02-01T00:00:00Z\nRows: 5\n"
            )

            changed = write_reproducible_metadata(path, replacement)

            self.assertTrue(changed)
            self.assertEqual(replacement, path.read_text())


if __name__ == "__main__":
    unittest.main()
