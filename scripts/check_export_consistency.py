#!/usr/bin/env python3
"""Check consistency across final export metadata files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "_portfolio_export" / "proposal_builder_unified_portfolio_pack.zip"
AUDIT_REPORT = ROOT / "_portfolio_export" / "package_audit.md"
SMOKE_REPORT = ROOT / "_portfolio_export" / "package_smoke_report.md"
INVENTORY_JSON = ROOT / "_portfolio_export" / "package_inventory.json"
UPLOAD_MANIFEST_JSON = ROOT / "_portfolio_export" / "upload_manifest.json"
RELEASE_REPORT = ROOT / "_demo_output" / "release_readiness_report.md"
REPORT_PATH = ROOT / "_portfolio_export" / "export_consistency_report.md"


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


def zip_entries(path: Path) -> int:
    with zipfile.ZipFile(path) as zf:
        return len([name for name in zf.namelist() if not name.endswith("/")])


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def status_from_markdown(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^- Status: `([^`]+)`", text, re.M)
    return match.group(1) if match else "UNKNOWN"


def check() -> tuple[list[str], dict[str, int | str]]:
    issues: list[str] = []
    required = [ZIP_PATH, AUDIT_REPORT, SMOKE_REPORT, INVENTORY_JSON, UPLOAD_MANIFEST_JSON, RELEASE_REPORT]
    for path in required:
        if not path.exists():
            issues.append(f"missing:{path}")
    if issues:
        return issues, {}

    actual_size = ZIP_PATH.stat().st_size
    actual_sha = sha256(ZIP_PATH)
    actual_entries = zip_entries(ZIP_PATH)
    manifest = load_json(UPLOAD_MANIFEST_JSON)
    inventory = load_json(INVENTORY_JSON)

    package = manifest.get("package", {})
    if package.get("size_bytes") != actual_size:
        issues.append(f"manifest-size-mismatch:{package.get('size_bytes')}!={actual_size}")
    if package.get("sha256") != actual_sha:
        issues.append("manifest-sha256-mismatch")
    if package.get("file_entries") != actual_entries:
        issues.append(f"manifest-entry-count-mismatch:{package.get('file_entries')}!={actual_entries}")

    if inventory.get("total_entries") != actual_entries:
        issues.append(f"inventory-entry-count-mismatch:{inventory.get('total_entries')}!={actual_entries}")
    category_total = sum(payload.get("count", 0) for payload in inventory.get("categories", {}).values())
    if category_total != inventory.get("total_entries"):
        issues.append(f"inventory-category-total-mismatch:{category_total}!={inventory.get('total_entries')}")

    reports = manifest.get("reports", {})
    for name, payload in reports.items():
        if payload.get("status") != "PASS":
            issues.append(f"manifest-report-not-pass:{name}:{payload.get('status')}")

    for label, path in {
        "release_readiness": RELEASE_REPORT,
        "package_audit": AUDIT_REPORT,
        "package_smoke": SMOKE_REPORT,
    }.items():
        status = status_from_markdown(path)
        if status != "PASS":
            issues.append(f"report-not-pass:{label}:{status}")

    meta: dict[str, int | str] = {
        "zip_size_bytes": actual_size,
        "zip_sha256": actual_sha,
        "zip_entries": actual_entries,
        "inventory_categories": len(inventory.get("categories", {})),
    }
    return issues, meta


def write_report(issues: list[str], meta: dict[str, int | str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Export Consistency Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Zip: `{display_path(ZIP_PATH)}`",
        f"- Zip size bytes: `{meta.get('zip_size_bytes', 0)}`",
        f"- Zip SHA256: `{meta.get('zip_sha256', 'n/a')}`",
        f"- Zip entries: `{meta.get('zip_entries', 0)}`",
        f"- Inventory categories: `{meta.get('inventory_categories', 0)}`",
        "",
        "## Checks",
        "",
        "- Upload manifest size/SHA256/entry count matches zip",
        "- Package inventory entry count matches zip",
        "- Package inventory category counts sum correctly",
        "- Release, audit, and smoke reports are PASS",
        "- Upload manifest report statuses are PASS",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check final export metadata consistency.")
    parser.parse_args()

    issues, meta = check()
    write_report(issues, meta)

    print(f"report={REPORT_PATH}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} export_consistency")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
