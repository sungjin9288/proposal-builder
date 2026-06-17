#!/usr/bin/env python3
"""Audit the built portfolio zip before upload."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "_portfolio_export" / "proposal_builder_unified_portfolio_pack.zip"
REPORT_PATH = ROOT / "_portfolio_export" / "package_audit.md"

BLOCKED_ENTRY_RE = re.compile(
    r"(^|/)(\.env|\.env\.|.*\.pem$|.*\.key$|.*\.crt$|id_rsa$|id_rsa\.pub$|"
    r"secrets\.|credentials\.|token\.|node_modules|venv|\.venv|__pycache__|"
    r"\.pytest_cache|\.mypy_cache|dist|build|\.next|out|target|\.git|\.idea|"
    r"\.vscode|coverage|\.DS_Store|Thumbs\.db|projects|archive|ppt-master|"
    r"_demo_output|_portfolio_export|.*\.pptx$|.*\.pdf$|.*\.hwp$|.*\.hwpx$|"
    r".*\.jsonl$|.*\.csv$)(/|$)"
)

TEXT_SUFFIXES = {
    "",
    ".gitignore",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".svg",
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


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_text_entry(name: str) -> bool:
    path = Path(name)
    if path.name == ".gitignore":
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def scan_text(name: str, data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8", errors="ignore")
    except UnicodeDecodeError:
        return [f"unreadable-text-entry:{name}"]

    issues: list[str] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"secret-pattern:{name}:{pattern.pattern}")
    return issues


def audit_zip(zip_path: Path) -> tuple[list[str], dict[str, int | str]]:
    issues: list[str] = []
    if not zip_path.exists():
        return [f"zip-missing:{zip_path}"], {"entries": 0, "size_bytes": 0, "text_entries_scanned": 0}

    text_entries_scanned = 0
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        top = {name.split("/", 1)[0] for name in names if name}
        if top != {"proposal_builder_unified_portfolio_pack"}:
            issues.append(f"bad-top-level:{sorted(top)}")

        for name in names:
            if name.endswith("/"):
                continue
            if BLOCKED_ENTRY_RE.search(name):
                issues.append(f"blocked-entry:{name}")
            if is_text_entry(name):
                text_entries_scanned += 1
                issues.extend(scan_text(name, zf.read(name)))

    meta: dict[str, int | str] = {
        "entries": len([name for name in names if not name.endswith("/")]),
        "size_bytes": zip_path.stat().st_size,
        "sha256": sha256(zip_path),
        "text_entries_scanned": text_entries_scanned,
    }
    return issues, meta


def write_report(zip_path: Path, issues: list[str], meta: dict[str, int | str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Portfolio Package Audit",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Zip: `{display_path(zip_path)}`",
        f"- Zip size bytes: `{meta.get('size_bytes', 0)}`",
        f"- Zip SHA256: `{meta.get('sha256', 'n/a')}`",
        f"- File entries: `{meta.get('entries', 0)}`",
        f"- Text entries scanned: `{meta.get('text_entries_scanned', 0)}`",
        "",
        "## Checks",
        "",
        "- Top-level folder",
        "- Blocked filename and folder patterns",
        "- Blocked raw document/data formats",
        "- Basic credential/key/token regex patterns in text entries",
        "- Local absolute user-path patterns in text entries",
        "- Local username patterns in text entries",
        "- Legacy incorrect document-name token patterns in text entries",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This audit checks the generated zip only.",
            "- It does not publish the package.",
            "- It does not inspect files outside the zip.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the generated public portfolio package.")
    parser.add_argument("--zip", type=Path, default=ZIP_PATH)
    args = parser.parse_args()

    issues, meta = audit_zip(args.zip)
    write_report(args.zip, issues, meta)

    print(f"report={REPORT_PATH}")
    print(f"zip={args.zip}")
    print(f"entries={meta.get('entries', 0)}")
    print(f"zip_size_bytes={meta.get('size_bytes', 0)}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} package_audit")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
