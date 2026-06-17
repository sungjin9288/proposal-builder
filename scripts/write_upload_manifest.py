#!/usr/bin/env python3
"""Write upload metadata for the verified portfolio package."""

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
RELEASE_REPORT = ROOT / "_demo_output" / "release_readiness_report.md"
INVENTORY_JSON = ROOT / "_portfolio_export" / "package_inventory.json"
INVENTORY_MD = ROOT / "_portfolio_export" / "package_inventory.md"
JSON_PATH = ROOT / "_portfolio_export" / "upload_manifest.json"
MD_PATH = ROOT / "_portfolio_export" / "upload_manifest.md"


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


def report_status(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^- Status: `([^`]+)`", text, re.M)
    return match.group(1) if match else "UNKNOWN"


def zip_entries(path: Path) -> int:
    with zipfile.ZipFile(path) as zf:
        return len([name for name in zf.namelist() if not name.endswith("/")])


def build_manifest(zip_path: Path) -> dict:
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    return {
        "generated_at": now(),
        "package": {
            "name": zip_path.name,
            "path": display_path(zip_path),
            "size_bytes": zip_path.stat().st_size,
            "sha256": sha256(zip_path),
            "file_entries": zip_entries(zip_path),
        },
        "reports": {
            "release_readiness": {
                "path": display_path(RELEASE_REPORT),
                "status": report_status(RELEASE_REPORT),
            },
            "package_audit": {
                "path": display_path(AUDIT_REPORT),
                "status": report_status(AUDIT_REPORT),
            },
            "package_smoke": {
                "path": display_path(SMOKE_REPORT),
                "status": report_status(SMOKE_REPORT),
            },
            "package_inventory": {
                "path": display_path(INVENTORY_MD),
                "status": "PASS" if INVENTORY_JSON.exists() and INVENTORY_MD.exists() else "MISSING",
            },
        },
        "reproduction_commands": [
            "make demo",
            "make preview",
            "make learn",
            "make validate-learning",
            "make test",
            "make docs-check",
            "make inventory",
            "make final-check",
        ],
        "boundaries": [
            "No private client material is included.",
            "No raw PPTX/PDF/HWP source documents are included.",
            "No external APIs are required for the public demo.",
            "No model training, fine-tuning, evaluation, or deployment is performed.",
            "No web UI or API server is implemented in this repository.",
        ],
    }


def write_markdown(manifest: dict) -> None:
    package = manifest["package"]
    reports = manifest["reports"]
    lines = [
        "# Upload Manifest",
        "",
        f"- Generated: `{manifest['generated_at']}`",
        f"- Package: `{package['path']}`",
        f"- Size bytes: `{package['size_bytes']}`",
        f"- SHA256: `{package['sha256']}`",
        f"- File entries: `{package['file_entries']}`",
        "",
        "## Report Status",
        "",
    ]
    for label, info in reports.items():
        lines.append(f"- {label}: `{info['status']}` ({info['path']})")
    lines.extend(["", "## Reproduction Commands", ""])
    lines.extend(f"- `{command}`" for command in manifest["reproduction_commands"])
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["boundaries"])
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write upload manifest for the portfolio zip.")
    parser.add_argument("--zip", type=Path, default=ZIP_PATH)
    args = parser.parse_args()

    try:
        manifest = build_manifest(args.zip)
    except OSError as exc:
        print(f"RESULT FAIL upload_manifest: {exc}")
        return 1

    statuses = [info["status"] for info in manifest["reports"].values()]
    if any(status != "PASS" for status in statuses):
        print(f"RESULT FAIL upload_manifest: report statuses are {statuses}")
        return 1

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(manifest)

    print(f"json={JSON_PATH}")
    print(f"markdown={MD_PATH}")
    print(f"zip={args.zip}")
    print(f"sha256={manifest['package']['sha256']}")
    print("RESULT PASS upload_manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
