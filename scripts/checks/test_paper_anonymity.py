#!/usr/bin/env python3
"""Regression checks for narrowly allowing an official source citation."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/checks"))
sys.path.insert(0, str(ROOT / "scripts/packaging"))

from check_paper_anonymity import OFFICIAL_SOURCE_URL, contains_hashed_banned_term
from build_anonymous_supplement import contains_hashed_banned_term as package_match
import build_anonymous_supplement as builder
import check_presidential_choice_study as presidential_checker


class AnonymousReadmeTests(unittest.TestCase):
    def test_current_readme_passes_publication_claim_checks(self):
        # Also runs inside the extracted supplement, before long campaigns.
        presidential_checker.check_publication_claims()

    def test_generated_readme_preserves_claim_checks_and_anonymity(self):
        original = (ROOT / "README.md").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            with patch.object(builder, "PACKAGE_DIR", target):
                builder.write_readme()
            readme = target / "README.md"
            with patch.object(presidential_checker, "README", readme):
                presidential_checker.check_publication_claims()
            text = readme.read_text()
            self.assertIsNone(package_match(text))
            self.assertFalse(any(pattern.search(text) for pattern in builder.BANNED_REGEXES))
        self.assertEqual((ROOT / "README.md").read_bytes(), original)

    def test_missing_test_concentration_caveat_remains_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            with patch.object(builder, "PACKAGE_DIR", target):
                builder.write_readme()
            readme = target / "README.md"
            readme.write_text(readme.read_text().replace(
                "Twelve of the 13 test vetoes occur among only 17 joint resolutions. ", ""))
            with patch.object(presidential_checker, "README", readme):
                with self.assertRaisesRegex(SystemExit, "Publication integration text drifted"):
                    presidential_checker.check_publication_claims()


class OfficialCitationTests(unittest.TestCase):
    def test_exact_government_citation_is_allowed(self):
        for check in (contains_hashed_banned_term, package_match):
            for text in (OFFICIAL_SOURCE_URL, f"[GPO]({OFFICIAL_SOURCE_URL})", f'"{OFFICIAL_SOURCE_URL}"'):
                with self.subTest(check=check.__module__, text=text):
                    self.assertIsNone(check(text))

    def test_other_hosting_links_and_lookalikes_remain_blocked(self):
        private_url = "https://" + "github" + ".com/example/author-repository"
        for check in (contains_hashed_banned_term, package_match):
            for text in (
                private_url,
                OFFICIAL_SOURCE_URL + "/extra",
                OFFICIAL_SOURCE_URL + "?author=example",
                OFFICIAL_SOURCE_URL + ".different",
                OFFICIAL_SOURCE_URL + " " + private_url,
            ):
                with self.subTest(check=check.__module__, text=text):
                    self.assertIsNotNone(check(text))

    def test_regression_source_is_safe_to_package(self):
        self.assertIsNone(package_match(Path(__file__).read_text()))

    def test_other_identity_terms_remain_checked(self):
        # A synthetic term tests the unchanged hash scan without embedding
        # private identity data in the anonymous supplement itself.
        import hashlib
        import check_paper_anonymity as checker
        from unittest.mock import patch

        token = "synthetic-private-identity"
        terms = ((len(token), hashlib.sha256(token.encode()).hexdigest()),)
        with patch.object(checker, "HASHED_BANNED_TERMS", terms):
            self.assertIsNotNone(checker.contains_hashed_banned_term(OFFICIAL_SOURCE_URL + " " + token))


if __name__ == "__main__":
    unittest.main()
