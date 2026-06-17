#!/usr/bin/env python3
"""Write a categorized inventory for the built portfolio zip."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "_portfolio_export" / "proposal_builder_unified_portfolio_pack.zip"
JSON_PATH = ROOT / "_portfolio_export" / "package_inventory.json"
MD_PATH = ROOT / "_portfolio_export" / "package_inventory.md"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def category(entry: str) -> str:
    path = Path(entry)
    parts = path.parts
    if len(parts) < 3:
        return "package-root"
    rel_parts = parts[2:]
    first = rel_parts[0]
    if first in {".claude", "templates", "examples", "case-studies", "docs", "scripts", "tests", "vendor"}:
        return first
    if path.name in {"START_HERE.md", "PORTFOLIO.md", "README.md", "CLAUDE.md", "Makefile", "requirements.txt", ".gitignore"}:
        return "root-files"
    return "other"


def read_entries(zip_path: Path) -> list[str]:
    with zipfile.ZipFile(zip_path) as zf:
        return sorted(name for name in zf.namelist() if not name.endswith("/"))


def build_inventory(zip_path: Path) -> dict:
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    entries = read_entries(zip_path)
    categories: dict[str, list[str]] = {}
    for entry in entries:
        categories.setdefault(category(entry), []).append(entry)
    return {
        "generated_at": now(),
        "zip": display_path(zip_path),
        "total_entries": len(entries),
        "categories": {name: {"count": len(values), "entries": values} for name, values in sorted(categories.items())},
    }


def write_markdown(inventory: dict) -> None:
    lines = [
        "# Package Inventory",
        "",
        f"- Generated: `{inventory['generated_at']}`",
        f"- Zip: `{inventory['zip']}`",
        f"- Total entries: `{inventory['total_entries']}`",
        "",
        "## Categories",
        "",
    ]
    for name, payload in inventory["categories"].items():
        lines.extend([f"### {name}", "", f"- Count: `{payload['count']}`", ""])
        lines.extend(f"- `{entry}`" for entry in payload["entries"])
        lines.append("")
    MD_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a categorized inventory for the portfolio zip.")
    parser.add_argument("--zip", type=Path, default=ZIP_PATH)
    args = parser.parse_args()

    try:
        inventory = build_inventory(args.zip)
    except OSError as exc:
        print(f"RESULT FAIL package_inventory: {exc}")
        return 1

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(inventory)

    print(f"json={JSON_PATH}")
    print(f"markdown={MD_PATH}")
    print(f"entries={inventory['total_entries']}")
    print("RESULT PASS package_inventory")
    return 0


if __name__ == "__main__":
    sys.exit(main())
