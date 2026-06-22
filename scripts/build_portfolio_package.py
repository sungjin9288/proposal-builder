#!/usr/bin/env python3
"""Build a public-safe Proposal Builder portfolio package.

The package intentionally includes only reusable framework files and sanitized
case-study evidence. Raw project data, decks, PDFs, archives, and vendored
third-party source trees are excluded by construction.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = ROOT / "_portfolio_export"
PACKAGE_NAME = "proposal_builder_unified_portfolio_pack"
STAGING_ROOT = EXPORT_ROOT / PACKAGE_NAME
STAGING_PROJECT = STAGING_ROOT / "proposal-builder"
ZIP_PATH = EXPORT_ROOT / f"{PACKAGE_NAME}.zip"

INCLUDE_FILES = [
    "START_HERE.md",
    "PORTFOLIO.md",
    "README.md",
    "CLAUDE.md",
    ".gitignore",
    "requirements.txt",
    "Makefile",
]

INCLUDE_DIRS = [
    ".claude",
    "examples",
    "templates",
    "docs",
    "case-studies",
    "scripts",
    "tests",
]

INCLUDE_VENDOR_FILES = [
    "vendor/README.md",
]

REQUIRED_IN_ZIP = [
    f"{PACKAGE_NAME}/proposal-builder/START_HERE.md",
    f"{PACKAGE_NAME}/proposal-builder/PORTFOLIO.md",
    f"{PACKAGE_NAME}/proposal-builder/README.md",
    f"{PACKAGE_NAME}/proposal-builder/CLAUDE.md",
    f"{PACKAGE_NAME}/proposal-builder/requirements.txt",
    f"{PACKAGE_NAME}/proposal-builder/Makefile",
    f"{PACKAGE_NAME}/proposal-builder/scripts/build_portfolio_package.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/proposal_builder_cli.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/build_learning_dataset.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/validate_learning_dataset.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/build_demo_preview.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/audit_portfolio_package.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/smoke_portfolio_package.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/write_upload_manifest.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/write_package_inventory.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/check_docs_links.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/check_case_study_status.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/check_export_consistency.py",
    f"{PACKAGE_NAME}/proposal-builder/scripts/check_release_readiness.py",
    f"{PACKAGE_NAME}/proposal-builder/examples/public-ai-safety/prd.md",
    f"{PACKAGE_NAME}/proposal-builder/tests/test_public_workflow.py",
    f"{PACKAGE_NAME}/proposal-builder/.claude/skills/rfp-analyzer/SKILL.md",
    f"{PACKAGE_NAME}/proposal-builder/.claude/skills/proposal-pptx/SKILL.md",
    f"{PACKAGE_NAME}/proposal-builder/.claude/skills/proposal-hwp/SKILL.md",
    f"{PACKAGE_NAME}/proposal-builder/templates/qa/forbidden_tokens.txt",
    f"{PACKAGE_NAME}/proposal-builder/docs/claims-matrix.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/portfolio-merge-map.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/publication-checklist.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/release-note.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/reviewer-guide.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/third-party-notices.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/unified-portfolio-manifest.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/verification-summary.md",
    f"{PACKAGE_NAME}/proposal-builder/docs/assets/public-ai-safety-preview.svg",
    f"{PACKAGE_NAME}/proposal-builder/case-studies/ai-safety-v3/README.md",
    f"{PACKAGE_NAME}/proposal-builder/case-studies/ai-safety-v3/docs/implementation-evidence.md",
    f"{PACKAGE_NAME}/proposal-builder/case-studies/ai-safety-v3/evidence/evidence_manifest.md",
]

BLOCKED_PARTS = {
    ".git",
    ".DS_Store",
    "projects",
    "archive",
    "ppt-master",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    ".next",
    "out",
    "target",
    "coverage",
    "_demo_output",
    "_portfolio_export",
}

BLOCKED_SUFFIXES = {
    ".pptx",
    ".pdf",
    ".hwp",
    ".hwpx",
    ".jsonl",
    ".csv",
    ".pem",
    ".key",
    ".crt",
    ".zip",
}

BLOCKED_FILENAMES = {
    ".env",
    "id_rsa",
    "id_rsa.pub",
    "Thumbs.db",
}

SECRET_PATTERNS = [
    re.compile(r"BEGIN (RSA|OPENSSH|PRIVATE) KEY"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*="),
    re.compile("/" + "Users" + r"/[^/\\s`\"']+"),
    re.compile("sung" + "jin", re.I),
    re.compile("\uc81c\uccad\uc11c"),
]

TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".log", ".py", ".sh", ".svg", ".gitignore", ""}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & BLOCKED_PARTS:
        return True
    if path.name in BLOCKED_FILENAMES or path.name.startswith(".env."):
        return True
    return path.suffix.lower() in BLOCKED_SUFFIXES


def copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, ignore=copy_ignore)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_ignore(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    base = Path(directory)
    for name in names:
        if should_skip(base / name):
            ignored.add(name)
    return ignored


def build_staging() -> None:
    if STAGING_ROOT.exists():
        shutil.rmtree(STAGING_ROOT)
    STAGING_PROJECT.mkdir(parents=True)

    for item in INCLUDE_FILES:
        source = ROOT / item
        if source.exists():
            copy_path(source, STAGING_PROJECT / item)

    for item in INCLUDE_DIRS:
        source = ROOT / item
        if source.exists():
            copy_path(source, STAGING_PROJECT / item)

    for item in INCLUDE_VENDOR_FILES:
        source = ROOT / item
        if source.exists():
            copy_path(source, STAGING_PROJECT / item)
    sanitize_staged_text()


def iter_staged_files() -> list[Path]:
    if not STAGING_ROOT.exists():
        return []
    return sorted(path for path in STAGING_ROOT.rglob("*") if path.is_file())


def is_text_file(path: Path) -> bool:
    if path.name == ".gitignore":
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def sanitize_staged_text() -> None:
    replacements = [
        (str(ROOT), "<proposal-builder-root>"),
        (str(Path.home() / "local-workspace"), "<case-study-workspace>"),
        (str(Path.home() / "Downloads"), "<local-downloads>"),
        (str(Path.home()), "<local-home>"),
        ("github.com/" + "sung" + "jin9288/proposal-builder", "github.com/<github-owner>/proposal-builder"),
        ("sung" + "jin9288", "<github-owner>"),
        ("㈜" + "\ub2e4\uc6b8", "㈜샘플기관"),
        ("\ub2e4\uc6b8", "샘플기관"),
        ("\u0044\u0041\u0057\u004f\u004f\u004c Co., Ltd.", "Sample Org Co., Ltd."),
        ("\u0044\u0041\u0057\u004f\u004f\u004c", "SAMPLEORG"),
        ("\uc81c\uccad\uc11c", "제안서"),
    ]
    for path in iter_staged_files():
        if not is_text_file(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def scan_file_for_secrets(path: Path) -> list[str]:
    if not is_text_file(path):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return [f"unreadable:{path}"]
    hits: list[str] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            hits.append(f"secret-pattern:{path}:{pattern.pattern}")
    return hits


def verify_staging() -> list[str]:
    issues: list[str] = []
    for path in iter_staged_files():
        staged_rel = path.relative_to(STAGING_ROOT)
        if should_skip(staged_rel):
            issues.append(f"blocked-path:{staged_rel.as_posix()}")
        issues.extend(scan_file_for_secrets(path))
    return issues


def write_zip() -> None:
    EXPORT_ROOT.mkdir(exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_staged_files():
            arcname = path.relative_to(EXPORT_ROOT).as_posix()
            zf.write(path, arcname)


def verify_zip() -> list[str]:
    issues: list[str] = []
    if not ZIP_PATH.exists():
        return ["zip-missing"]
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
    top = {name.split("/", 1)[0] for name in names if name}
    if top != {PACKAGE_NAME}:
        issues.append(f"bad-top-level:{sorted(top)}")
    missing = sorted(set(REQUIRED_IN_ZIP) - set(names))
    for name in missing:
        issues.append(f"required-missing:{name}")
    for name in names:
        path = Path(name)
        if should_skip(path):
            issues.append(f"blocked-in-zip:{name}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and verify the public-safe portfolio package.")
    parser.add_argument("--verify-only", action="store_true", help="verify current staging/zip without rebuilding")
    args = parser.parse_args()

    if not args.verify_only:
        build_staging()
        staging_issues = verify_staging()
        if staging_issues:
            print("RESULT FAIL staging")
            for issue in staging_issues:
                print(issue)
            return 1
        write_zip()

    staging_issues = verify_staging()
    zip_issues = verify_zip()
    if staging_issues or zip_issues:
        print("RESULT FAIL portfolio_package")
        for issue in staging_issues + zip_issues:
            print(issue)
        return 1

    file_count = len(iter_staged_files())
    size = ZIP_PATH.stat().st_size if ZIP_PATH.exists() else 0
    print("RESULT PASS portfolio_package")
    print(f"root={ROOT}")
    print(f"staging={STAGING_ROOT}")
    print(f"zip={ZIP_PATH}")
    print(f"files={file_count}")
    print(f"zip_size_bytes={size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
