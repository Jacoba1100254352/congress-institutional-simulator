#!/usr/bin/env python3
"""Source-manifest regressions for duplicate-named local files."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import write_pdf_manifest as manifest


class SourceInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        root_patch = patch.object(manifest, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def write(self, name, content):
        path = self.root / name
        path.write_bytes(content)
        return path

    def test_identical_copy_ignored_without_mutating_either_file(self):
        original = self.write("panel.csv", b"bill,value\na,1\n")
        duplicate = self.write("panel 2.csv", original.read_bytes())
        self.assertEqual(manifest.unique_paths(["*.csv"]), [original])
        self.assertEqual(original.read_bytes(), b"bill,value\na,1\n")
        self.assertEqual(duplicate.read_bytes(), original.read_bytes())

    def test_different_copy_blocks_even_when_the_size_matches(self):
        original = self.write("panel.csv", b"a,1\n")
        duplicate = self.write("panel 2.csv", b"a,2\n")
        with self.assertRaisesRegex(RuntimeError, "Conflicting source copies.*contents differ"):
            manifest.unique_paths(["*.csv"])
        self.assertEqual(original.read_bytes(), b"a,1\n")
        self.assertEqual(duplicate.read_bytes(), b"a,2\n")

    def test_unpaired_numbered_file_is_retained(self):
        path = self.write("panel 2.csv", b"a,1\n")
        self.assertEqual(manifest.unique_paths(["*.csv"]), [path])

    def test_original_outside_selected_patterns_does_not_drop_only_input(self):
        self.write("panel.csv", b"a,1\n")
        duplicate = self.write("panel 2.csv", b"a,1\n")
        self.assertEqual(manifest.unique_paths(["* 2.csv"]), [duplicate])

    def test_other_inputs_are_sorted_and_overlapping_globs_deduplicated(self):
        second = self.write("z.csv", b"z,1\n")
        first = self.write("a.csv", b"a,1\n")
        numbered = self.write("a 3.csv", first.read_bytes())
        self.assertEqual(manifest.unique_paths(["*.csv", "a.csv"]), [numbered, first, second])

    def test_duplicate_does_not_change_source_digest(self):
        original = self.write("panel.csv", b"a,1\n")
        with patch.object(manifest, "INPUT_PATTERNS", ["*.csv"]):
            expected = manifest.source_manifest()
            self.write("panel 2.csv", original.read_bytes())
            self.assertEqual(manifest.source_manifest(), expected)


if __name__ == "__main__":
    unittest.main()
