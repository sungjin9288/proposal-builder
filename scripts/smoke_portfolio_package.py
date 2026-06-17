#!/usr/bin/env python3
"""Smoke-test the generated portfolio zip in a clean temporary directory."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "_portfolio_export" / "proposal_builder_unified_portfolio_pack.zip"
REPORT_PATH = ROOT / "_portfolio_export" / "package_smoke_report.md"
PACKAGE_ROOT_NAME = "proposal_builder_unified_portfolio_pack"
PROJECT_ROOT = Path(PACKAGE_ROOT_NAME) / "proposal-builder"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def run(command: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout


def write_report(zip_path: Path, checks: list[tuple[str, int, str]], issues: list[str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Portfolio Package Smoke Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Zip: `{display_path(zip_path)}`",
        "",
        "## Checks",
        "",
    ]
    for label, code, output in checks:
        result = "PASS" if code == 0 else "FAIL"
        lines.append(f"- `{label}`: `{result}`")
        if code != 0:
            snippet = "\n".join(output.splitlines()[-20:])
            lines.extend(["", "```text", snippet, "```", ""])
    lines.extend(["", "## Issues", ""])
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This smoke test extracts the generated zip into a temporary directory.",
            "- It runs only the public sample workflow inside the extracted package.",
            "- It does not call external APIs, publish files, or train a model.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def smoke(zip_path: Path) -> tuple[list[tuple[str, int, str]], list[str]]:
    checks: list[tuple[str, int, str]] = []
    issues: list[str] = []
    if not zip_path.exists():
        return checks, [f"zip-missing:{zip_path}"]

    with tempfile.TemporaryDirectory(prefix="proposal-builder-smoke-") as tmp:
        tmp_root = Path(tmp)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_root)
        project = tmp_root / PROJECT_ROOT
        if not project.exists():
            return checks, [f"extracted-project-missing:{project}"]

        commands = [
            ("make demo", ["make", "demo"]),
            ("make preview", ["make", "preview"]),
            ("make learn", ["make", "learn"]),
            ("make validate-learning", ["make", "validate-learning"]),
            ("make test", ["make", "test"]),
            ("make docs-check", ["make", "docs-check"]),
        ]
        for label, command in commands:
            code, output = run(command, project)
            checks.append((label, code, output))
            if code != 0:
                issues.append(f"command-failed:{label}")

        expected_outputs = [
            "_demo_output/public-ai-safety/slides.json",
            "_demo_output/public-ai-safety/output.pptx",
            "_demo_output/public-ai-safety/qa_report.md",
            "docs/assets/public-ai-safety-preview.svg",
            "_demo_output/public-ai-safety/learning/dataset.jsonl",
            "_demo_output/public-ai-safety/learning/train.jsonl",
            "_demo_output/public-ai-safety/learning/validation.jsonl",
            "_demo_output/public-ai-safety/learning/validation_report.md",
            "_demo_output/docs_link_report.md",
        ]
        for item in expected_outputs:
            if not (project / item).exists():
                issues.append(f"expected-output-missing:{item}")

    return checks, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test the generated portfolio zip.")
    parser.add_argument("--zip", type=Path, default=ZIP_PATH)
    args = parser.parse_args()

    checks, issues = smoke(args.zip)
    write_report(args.zip, checks, issues)

    print(f"report={REPORT_PATH}")
    print(f"zip={args.zip}")
    print(f"checks={len(checks)}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} package_smoke")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
