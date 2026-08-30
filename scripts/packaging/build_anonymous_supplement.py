#!/usr/bin/env python3
"""Build a double-blind-safe reproducibility supplement."""

from __future__ import annotations

import shutil
import sys
import zipfile
import re
import hashlib
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
PACKAGE_NAME = "congress-institutional-simulator-anonymous"
STAGING_DIR = DIST / "anonymous-supplement"
PACKAGE_DIR = STAGING_DIR / PACKAGE_NAME
ZIP_PATH = DIST / f"{PACKAGE_NAME}.zip"

TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".java",
    ".json",
    ".md",
    ".py",
    ".tex",
    ".txt",
    ".yml",
    ".yaml",
    "",
}

HASHED_BANNED_TERMS = (
    (14, "f10f60a1f978030d3278bf2c22865cda980beb926d1d0c97c3e9c85ba9252238"),
    (17, "5d394ce4d14ef833bb98c1b71d7261b96298e805ff4319d9790119fe54c67994"),
    (13, "ca035de7d1f1c65ceb1493c7147ed1f0eeba3311af52e339a1913816879ffc43"),
    (14, "ef4fab81da95ac04aba973ee1192997ad0296a18b20c8153b68975969ae6de7d"),
    (16, "5a170c01d6f4f68b0b95ac4be9c138d40a104975671b607a50d42a6409e11aa0"),
    (11, "7510bdd3e5310ec7655ac4895dc39b099b1c2f6f337abd455d73043119daf8a8"),
)
BANNED_REGEXES = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
]


def is_conflict_copy_name(name: str) -> bool:
    return Path(name).stem.endswith(" 2")


def ignore_names(directory: str, names: list[str]) -> set[str]:
    ignored = {
        ".DS_Store",
        ".git",
        ".idea",
        "build",
        "out",
        "dist",
        "no-include",
        "ACM-README",
        "notes",
        "breakout-paper-plans",
        "__pycache__",
    }
    return {name for name in names if name in ignored or is_conflict_copy_name(name)}


def copy_tree(name: str) -> None:
    source = ROOT / name
    target = PACKAGE_DIR / name
    shutil.copytree(source, target, ignore=ignore_names)


def copy_reports() -> None:
    source = ROOT / "reports"
    target = PACKAGE_DIR / "reports"
    target.mkdir(parents=True, exist_ok=True)
    for pattern in (
        "calibration-baseline.*",
        "simulation-campaign-v21-paper.*",
        "seed-robustness-summary.*",
        "paper-findings-validation.*",
        "all-scenarios-baseline.*",
        "family-champions.*",
        "representative-vs-family-champions.*",
        "ablation-analysis-summary.*",
        "manipulation-stress-summary.*",
        "adversary-catalog.*",
        "adversarial-stress-manifest.*",
        "adversarial-stress-run-manifest.*",
        "adversarial-stress-summary.*",
        "adversarial-stress-a2-run-manifest.*",
        "adversarial-stress-a2-summary.*",
        "adversarial-stress-a3-run-manifest.*",
        "adversarial-stress-a3-summary.*",
        "adversarial-stress-a4-run-manifest.*",
        "adversarial-stress-a4-summary.*",
        "adversarial-stress-a5-run-manifest.*",
        "adversarial-stress-a5-summary.*",
        "adversarial-stress-a6-run-manifest.*",
        "adversarial-stress-a6-summary.*",
        "adversarial-stress-a7-run-manifest.*",
        "adversarial-stress-a7-summary.*",
        "adversarial-stress-a8-run-manifest.*",
        "adversarial-stress-a8-summary.*",
        "adversarial-failure-trace-index.*",
        "adversarial-failure-traces.*",
        "adversarial-failure-traces-a2.*",
        "adversarial-failure-traces-a3.*",
        "adversarial-failure-traces-a4.*",
        "adversarial-failure-traces-a5.*",
        "adversarial-failure-traces-a6.*",
        "adversarial-failure-traces-a7.*",
        "adversarial-failure-traces-a8.*",
        "adversarial-pilot-cell-map.*",
        "empirical-bridge.*",
        "empirical-data-inventory.*",
        "empirical-flow-heldout.*",
        "empirical-linkage-report.*",
        "empirical-linkage-roadmap.*",
        "govinfo-billstatus-linkage.*",
        "sponsor-bill-linkage.*",
        "comparative-institution-linkage.*",
        "court-law-linkage.*",
        "rulemaking-authority-linkage.*",
        "rulemaking-history-linkage.*",
        "rulemaking-comment-metadata.*",
        "rulemaking-comment-records.*",
        "rulemaking-comment-text-review.*",
        "bill-law-evidence-spine.*",
        "bill-law-lifecycle-readiness.*",
        "bill-law-lifecycle-next-actions.*",
        "bill-law-lifecycle-corpus.*",
        "bill-finance-lobbying-review-queue.*",
        "bill-finance-lobbying-local-context-review.*",
        "bill-finance-lobbying-external-search-review.*",
        "bill-finance-lobbying-external-lda-mention-review.*",
        "bill-finance-lobbying-campaign-finance-target-scope-review.*",
        "bill-finance-lobbying-committee-action-context.*",
        "bill-finance-lobbying-committee-action-source-review.*",
        "bill-finance-lobbying-roll-call-source-review.*",
        "bill-finance-lobbying-member-vote-target-review.*",
        "bill-finance-lobbying-source-acquisition-queue.*",
        "statutory-lineage-review-queue.*",
        "statutory-lineage-source-scan.*",
        "statutory-lineage-target-section-triage.*",
        "statutory-lineage-olrc-current-scan.*",
        "statutory-lineage-olrc-historical-scan.*",
        "statutory-lineage-olrc-annual-text-diff.*",
        "statutory-lineage-adjudication.*",
        "statutory-lineage-target-review-packets.*",
        "statutory-lineage-target-section-diff-review.*",
        "statutory-lineage-no-target-review.*",
        "statutory-lineage-target-lifecycle-bridge.*",
        "statutory-lineage-codified-progress.*",
        "statutory-lineage-effective-text-review.*",
        "statutory-lineage-public-law-attribution-review.*",
        "statutory-lineage-completion-queue.*",
        "statutory-lineage-complete-lineage-expansion-queue.*",
        "statutory-lineage-target-packet-expansion-queue.*",
        "statutory-lineage-target-packet-source-gap-queue.*",
        "statutory-lineage-target-packet-source-gap-review.*",
        "statutory-lineage-target-reference-resolution-candidates.*",
        "court-public-law-review-queue.*",
        "court-public-law-temporal-triage.*",
        "court-public-law-direct-review.*",
        "campaign-finance-district-context.*",
        "campaign-finance-member-context.*",
        "campaign-finance-issue-context.*",
        "campaign-finance-sponsor-bill-context.*",
        "district-public-opinion-policy-context.*",
        "district-public-opinion-bill-topic-readiness.*",
        "district-public-opinion-source-packets.*",
        "district-public-opinion-census-denominators.*",
        "district-public-opinion-acs-context.*",
        "district-public-opinion-survey-source-crosswalk.*",
        "district-public-opinion-survey-item-proxy-review.*",
        "district-public-opinion-ces-source-freshness.*",
        "voteview-member-context.*",
        "voteview-bill-linkage.*",
        "lobbying-issue-linkage.*",
        "lobbying-bill-policy-context.*",
        "raw-source-manifest.*",
        "empirical-validation-gap-report.*",
        "simulation-ablation-analysis.*",
        "simulation-manipulation-stress.*",
        "validation-boundary-matrix.*",
        "simulation-chamber-structure.*",
        "chamber-family-champions.*",
        "chamber-stress-screen.*",
        "catalog-breadth.*",
        "scenario-selection-manifest.*",
        "core-raw-validation-build.*",
        "empirical-validation-readiness.*",
        "empirical-validation-summary.*",
    ):
        for path in source.glob(pattern):
            if path.is_file() and not is_conflict_copy_name(path.name):
                shutil.copy2(path, target / path.name)


def write_readme() -> None:
    (PACKAGE_DIR / "README.md").write_text(
        "# Anonymous Reproducibility Supplement\n\n"
        "This double-blind supplement contains source code, generated reports, LaTeX paper sources, "
        "paper PDFs, and scripts for the legislative mechanism-comparison simulator. The offline "
        "paper path is deterministic and does not require network access.\n\n"
        "Requirements: Java 21, GNU Make, Python 3, and LaTeX with `latexmk` for PDF rebuilding.\n\n"
        "Recommended reproduction commands:\n\n"
        "```sh\n"
        "make test\n"
        "make reproduce-paper-offline\n"
        "make paper-checks\n"
        "```\n\n"
        "`make test` is the quick smoke test. `make reproduce-paper-offline` regenerates the "
        "main campaign, diagnostics, figures, PDFs, and PDF manifest from fixed seeds. "
        "`make paper-checks` adds word-count, anonymity, figure-label, table/figure consistency, "
        "PDF-render, and manifest checks.\n\n"
        "Expected runtime: `make test` usually runs in under one minute on the authoring workstation. "
        "`make reproduce-paper-offline` and `make paper-checks` usually take several minutes because "
        "they rerun the fixed-seed campaign and rebuild PDFs.\n\n"
        "Main outputs:\n\n"
        "- `paper/acm-ci-framework/acm-ci-framework.pdf`\n"
        "- `paper/technical-appendix/odd-d-appendix.pdf`\n"
        "- `paper/pdf-manifest.json`\n"
        "- `reports/simulation-campaign-v21-paper.csv`\n"
        "- `reports/raw-source-manifest.csv`\n"
        "- `reports/empirical-linkage-report.csv`\n"
        "- `reports/empirical-linkage-roadmap.csv`\n"
        "- `reports/govinfo-billstatus-linkage.csv`\n"
        "- `reports/sponsor-bill-linkage.csv`\n"
        "- `reports/comparative-institution-linkage.csv`\n"
        "- `reports/court-law-linkage.csv`\n"
        "- `reports/rulemaking-authority-linkage.csv`\n"
        "- `reports/rulemaking-history-linkage.csv`\n"
        "- `reports/rulemaking-comment-metadata.csv`\n"
        "- `reports/rulemaking-comment-records.csv`\n"
        "- `reports/rulemaking-comment-text-review.csv`\n"
        "- `reports/bill-law-evidence-spine.csv`\n"
        "- `reports/bill-law-lifecycle-readiness.csv`\n"
        "- `reports/bill-law-lifecycle-next-actions.csv`\n"
        "- `reports/bill-law-lifecycle-corpus.csv`\n"
        "- `reports/bill-finance-lobbying-review-queue.csv`\n"
        "- `reports/bill-finance-lobbying-local-context-review.csv`\n"
        "- `reports/bill-finance-lobbying-external-search-review.csv`\n"
        "- `reports/bill-finance-lobbying-external-lda-mention-review.csv`\n"
        "- `reports/bill-finance-lobbying-campaign-finance-target-scope-review.csv`\n"
        "- `reports/bill-finance-lobbying-committee-action-context.csv`\n"
        "- `reports/bill-finance-lobbying-committee-action-source-review.csv`\n"
        "- `reports/bill-finance-lobbying-roll-call-source-review.csv`\n"
        "- `reports/bill-finance-lobbying-member-vote-target-review.csv`\n"
        "- `reports/bill-finance-lobbying-source-acquisition-queue.csv`\n"
        "- `reports/statutory-lineage-review-queue.csv`\n"
        "- `reports/statutory-lineage-source-scan.csv`\n"
        "- `reports/statutory-lineage-target-section-triage.csv`\n"
        "- `reports/statutory-lineage-olrc-current-scan.csv`\n"
        "- `reports/statutory-lineage-olrc-historical-scan.csv`\n"
        "- `reports/statutory-lineage-olrc-annual-text-diff.csv`\n"
        "- `reports/statutory-lineage-adjudication.csv`\n"
        "- `reports/statutory-lineage-target-review-packets.csv`\n"
        "- `reports/statutory-lineage-target-section-diff-review.csv`\n"
        "- `reports/statutory-lineage-no-target-review.csv`\n"
        "- `reports/statutory-lineage-target-lifecycle-bridge.csv`\n"
        "- `reports/statutory-lineage-codified-progress.csv`\n"
        "- `reports/statutory-lineage-effective-text-review.csv`\n"
        "- `reports/statutory-lineage-public-law-attribution-review.csv`\n"
        "- `reports/statutory-lineage-completion-queue.csv`\n"
        "- `reports/statutory-lineage-complete-lineage-expansion-queue.csv`\n"
        "- `reports/statutory-lineage-target-packet-expansion-queue.csv`\n"
        "- `reports/statutory-lineage-target-packet-source-gap-queue.csv`\n"
        "- `reports/statutory-lineage-target-packet-source-gap-review.csv`\n"
        "- `reports/statutory-lineage-target-reference-resolution-candidates.csv`\n"
        "- `reports/court-public-law-review-queue.csv`\n"
        "- `reports/court-public-law-temporal-triage.csv`\n"
        "- `reports/court-public-law-direct-review.csv`\n"
        "- `reports/campaign-finance-district-context.csv`\n"
        "- `reports/campaign-finance-member-context.csv`\n"
        "- `reports/campaign-finance-issue-context.csv`\n"
        "- `reports/campaign-finance-sponsor-bill-context.csv`\n"
        "- `reports/district-public-opinion-policy-context.csv`\n"
        "- `reports/district-public-opinion-bill-topic-readiness.csv`\n"
        "- `reports/district-public-opinion-source-packets.csv`\n"
        "- `reports/district-public-opinion-census-denominators.csv`\n"
        "- `reports/district-public-opinion-acs-context.csv`\n"
        "- `reports/district-public-opinion-survey-source-crosswalk.csv`\n"
        "- `reports/district-public-opinion-survey-item-proxy-review.csv`\n"
        "- `reports/district-public-opinion-ces-source-freshness.csv`\n"
        "- `reports/voteview-member-context.csv`\n"
        "- `reports/voteview-bill-linkage.csv`\n"
        "- `reports/lobbying-issue-linkage.csv`\n"
        "- `reports/lobbying-bill-policy-context.csv`\n"
        "- `reports/adversary-catalog.csv`\n"
        "- `reports/adversarial-stress-manifest.json`\n"
        "- `reports/adversarial-stress-run-manifest.json`\n"
        "- `reports/adversarial-stress-summary.csv`\n"
        "- `reports/adversarial-failure-traces.jsonl`\n"
        "- `reports/adversarial-stress-a2-run-manifest.json`\n"
        "- `reports/adversarial-stress-a2-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a2.jsonl`\n"
        "- `reports/adversarial-stress-a3-run-manifest.json`\n"
        "- `reports/adversarial-stress-a3-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a3.jsonl`\n"
        "- `reports/adversarial-stress-a4-run-manifest.json`\n"
        "- `reports/adversarial-stress-a4-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a4.jsonl`\n"
        "- `reports/adversarial-stress-a5-run-manifest.json`\n"
        "- `reports/adversarial-stress-a5-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a5.jsonl`\n"
        "- `reports/adversarial-stress-a6-run-manifest.json`\n"
        "- `reports/adversarial-stress-a6-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a6.jsonl`\n"
        "- `reports/adversarial-stress-a7-run-manifest.json`\n"
        "- `reports/adversarial-stress-a7-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a7.jsonl`\n"
        "- `reports/adversarial-stress-a8-run-manifest.json`\n"
        "- `reports/adversarial-stress-a8-summary.csv`\n"
        "- `reports/adversarial-failure-traces-a8.jsonl`\n"
        "- `reports/adversarial-failure-trace-index.csv`\n"
        "- `reports/adversarial-pilot-cell-map.csv`\n"
        "- generated diagnostic reports under `reports/`\n\n"
        "Optional live-data refresh targets include `make fetch-validation-samples`, "
        "`make build-bill-progression-raw`, `make build-core-raw-validation`, "
        "`make build-govinfo-billstatus-linkage-raw`, "
        "`make build-sponsor-bill-linkage-raw`, "
        "`make build-comparative-institution-linkage-raw`, "
        "`make build-voteview-member-context-raw`, `make build-voteview-bill-linkage-raw`, "
        "`make build-lobbying-issue-linkage-raw`, "
        "`make build-campaign-finance-raw`, `make build-campaign-finance-linkage-raw`, "
        "`make build-campaign-finance-member-context-raw`, "
        "`make build-campaign-finance-issue-context-raw`, "
        "`make build-district-public-opinion-raw`, "
        "`make build-district-public-opinion-linkage-raw`, "
        "`make build-district-public-opinion-policy-context-raw`, "
        "`make build-court-review-raw`, "
        "`make build-court-law-linkage-raw`, "
        "`make build-rulemaking-implementation-raw`, "
        "`make build-rulemaking-implementation-linkage-raw`, "
        "`make build-rulemaking-authority-linkage-raw`, "
        "`make build-rulemaking-history-linkage-raw`, "
        "`make build-rulemaking-comment-metadata-raw`, "
        "`make build-rulemaking-comment-records-raw`, "
        "`make build-rulemaking-comment-text-review-raw`, "
        "`make build-law-revision-raw`, "
        "`make build-law-revision-bill-linkage-raw`, "
        "`make build-statutory-lineage-source-scan-raw`, "
        "`make build-statutory-lineage-olrc-current-scan-raw`, "
        "`make build-statutory-lineage-olrc-historical-scan-raw`, "
        "`make build-statutory-lineage-olrc-annual-text-diff-raw`, "
        "`make build-statutory-lineage-adjudication-raw`, "
        "`make build-statutory-lineage-target-review-packets-raw`, and "
        "`make build-comparative-institutions-raw`; they are intentionally outside the "
        "no-network reproduction path.\n"
    )


def copy_files() -> None:
    for file_name in ("Makefile", ".gitignore", ".gitattributes", ".java-version"):
        source = ROOT / file_name
        if source.exists():
            shutil.copy2(source, PACKAGE_DIR / file_name)


def reset_staging_dir() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)


def leave_clean_staging_marker() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    (STAGING_DIR / "README.md").write_text(
        "Temporary staging directory for the anonymous supplement builder.\n\n"
        "The reviewable artifact is ../congress-institutional-simulator-anonymous.zip.\n"
    )


def remove_conflict_copies(settle: bool = False) -> None:
    attempts = 4 if settle else 1
    for attempt in range(attempts):
        for path in STAGING_DIR.rglob("*"):
            if path.is_file() and is_conflict_copy_name(path.name):
                path.unlink()
        if attempt < attempts - 1:
            time.sleep(0.5)


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


def scan_identity() -> list[str]:
    failures: list[str] = []
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="ignore")
        except UnicodeDecodeError:
            continue
        hashed_match = contains_hashed_banned_term(text)
        if hashed_match:
            length, digest_prefix = hashed_match
            failures.append(
                f"{path.relative_to(PACKAGE_DIR)} contains hashed banned identity term "
                f"(length={length}, hash={digest_prefix}...)"
            )
        for pattern in BANNED_REGEXES:
            if pattern.search(text):
                failures.append(f"{path.relative_to(PACKAGE_DIR)} matches {pattern.pattern!r}")
    return failures


def zip_package() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file() and not any(is_conflict_copy_name(part) for part in path.parts):
                archive.write(path, path.relative_to(PACKAGE_DIR.parent))


def main() -> int:
    reset_staging_dir()

    for directory in ("src", "data", "docs", "paper", "scripts", ".github"):
        copy_tree(directory)
    copy_reports()
    copy_files()
    write_readme()
    remove_conflict_copies()

    failures = scan_identity()
    if failures:
        print("Anonymous supplement identity scan failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    remove_conflict_copies()
    zip_package()
    remove_conflict_copies(settle=True)
    leave_clean_staging_marker()
    print(f"Wrote {ZIP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
