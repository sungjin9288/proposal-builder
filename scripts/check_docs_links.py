#!/usr/bin/env python3
"""Check local Markdown links in public portfolio documentation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "_demo_output" / "docs_link_report.md"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_DOC_ROOTS = [
    ROOT / "START_HERE.md",
    ROOT / "PORTFOLIO.md",
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "docs",
    ROOT / "case-studies",
    ROOT / "examples",
    ROOT / "templates",
    ROOT / "vendor" / "README.md",
]


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "tel:"))


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in LOCAL_DOC_ROOTS:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".md":
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*.md") if "ppt-master" not in path.parts)
    return sorted(set(files))


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target.split("#", 1)[0])


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in MARKDOWN_LINK_RE.finditer(line):
            raw_target = match.group(1)
            if is_external(raw_target):
                continue
            target = normalize_target(raw_target)
            if not target:
                continue
            if target.startswith("/"):
                issues.append(f"absolute-local-link:{path.relative_to(ROOT)}:{line_no}:{raw_target}")
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                issues.append(f"outside-root-link:{path.relative_to(ROOT)}:{line_no}:{raw_target}")
                continue
            if not resolved.exists():
                issues.append(f"missing-link-target:{path.relative_to(ROOT)}:{line_no}:{raw_target}")
    return issues


def write_report(files: list[Path], issues: list[str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Docs Link Report",
        "",
        f"- Status: `{status}`",
        f"- Markdown files scanned: `{len(files)}`",
        "",
        "## Scope",
        "",
        "- START_HERE.md, PORTFOLIO.md, README.md, CLAUDE.md",
        "- docs/",
        "- case-studies/",
        "- examples/",
        "- templates/",
        "- vendor/README.md only",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local Markdown links in public docs.")
    parser.parse_args()

    files = iter_markdown_files()
    issues: list[str] = []
    for path in files:
        issues.extend(check_file(path))
    write_report(files, issues)

    print(f"report={REPORT_PATH}")
    print(f"files={len(files)}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} docs_links")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
