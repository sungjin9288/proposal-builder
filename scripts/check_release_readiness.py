#!/usr/bin/env python3
"""Check whether Proposal Builder is ready for portfolio submission."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "_portfolio_export" / "proposal_builder_unified_portfolio_pack.zip"
REPORT_PATH = ROOT / "_demo_output" / "release_readiness_report.md"

REQUIRED_LOCAL_FILES = [
    "START_HERE.md",
    "PORTFOLIO.md",
    "README.md",
    "CLAUDE.md",
    "requirements.txt",
    "Makefile",
    "scripts/proposal_builder_cli.py",
    "scripts/build_learning_dataset.py",
    "scripts/validate_learning_dataset.py",
    "scripts/build_demo_preview.py",
    "scripts/audit_portfolio_package.py",
    "scripts/smoke_portfolio_package.py",
    "scripts/write_upload_manifest.py",
    "scripts/write_package_inventory.py",
    "scripts/check_docs_links.py",
    "scripts/check_case_study_status.py",
    "scripts/check_export_consistency.py",
    "scripts/build_portfolio_package.py",
    "tests/test_public_workflow.py",
    "examples/public-ai-safety/prd.md",
    "docs/claims-matrix.md",
    "docs/demo-evidence.md",
    "docs/test-evidence.md",
    "docs/learning-dataset-schema.md",
    "docs/decisiondoc-handoff.md",
    "docs/publication-checklist.md",
    "docs/release-note.md",
    "docs/reviewer-guide.md",
    "docs/third-party-notices.md",
    "docs/unified-portfolio-manifest.md",
    "docs/verification-summary.md",
    "docs/assets/public-ai-safety-preview.svg",
    "case-studies/ai-safety-v3/README.md",
]

REQUIRED_GENERATED_FILES = [
    "_demo_output/public-ai-safety/slides.json",
    "_demo_output/public-ai-safety/output.pptx",
    "_demo_output/public-ai-safety/qa_report.md",
    "_demo_output/public-ai-safety/learning/dataset.jsonl",
    "_demo_output/public-ai-safety/learning/train.jsonl",
    "_demo_output/public-ai-safety/learning/validation.jsonl",
    "_demo_output/public-ai-safety/learning/learning_report.md",
    "_demo_output/public-ai-safety/learning/validation_report.md",
    "_demo_output/docs_link_report.md",
    "_demo_output/case_study_status_report.md",
]

REQUIRED_ZIP_FILES = [
    "proposal_builder_unified_portfolio_pack/proposal-builder/START_HERE.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/PORTFOLIO.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/README.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/Makefile",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/proposal_builder_cli.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/build_learning_dataset.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/validate_learning_dataset.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/build_demo_preview.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/audit_portfolio_package.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/smoke_portfolio_package.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/write_upload_manifest.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/write_package_inventory.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/check_docs_links.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/check_case_study_status.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/scripts/check_export_consistency.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/tests/test_public_workflow.py",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/claims-matrix.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/decisiondoc-handoff.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/publication-checklist.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/learning-dataset-schema.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/release-note.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/reviewer-guide.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/third-party-notices.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/verification-summary.md",
    "proposal_builder_unified_portfolio_pack/proposal-builder/docs/assets/public-ai-safety-preview.svg",
    "proposal_builder_unified_portfolio_pack/proposal-builder/case-studies/ai-safety-v3/README.md",
]

BLOCKED_ZIP_RE = re.compile(
    r"(^|/)(\.env|\.env\.|.*\.pem$|.*\.key$|.*\.crt$|id_rsa$|id_rsa\.pub$|"
    r"secrets\.|credentials\.|token\.|node_modules|venv|\.venv|__pycache__|"
    r"\.pytest_cache|\.mypy_cache|dist|build|\.next|out|target|\.git|\.idea|"
    r"\.vscode|coverage|\.DS_Store|Thumbs\.db|projects|archive|ppt-master|"
    r"_demo_output|.*\.pptx$|.*\.pdf$|.*\.hwp$|.*\.hwpx$|.*\.jsonl$|.*\.csv$)(/|$)"
)

OVERCLAIM_RE = re.compile(
    r"99\.8|94\.2|95%|production-ready|enterprise|상용 운영|엔터프라이즈|"
    r"모델 학습 완료|fine.?tuning 완료",
    re.I,
)

ALLOWED_OVERCLAIM_CONTEXT = [
    "주장하지 않습니다",
    "범위가 아닙니다",
    "근거는 확인되지 않습니다",
    "보류",
    "미구현",
    "주장 금지",
    "아직 할 수 없는",
]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def check_required_files(paths: list[str], label: str) -> list[str]:
    issues: list[str] = []
    for item in paths:
        if not (ROOT / item).exists():
            issues.append(f"missing {label}: {item}")
    return issues


def check_generated_reports() -> list[str]:
    issues: list[str] = []
    report_expectations = {
        "_demo_output/public-ai-safety/qa_report.md": "Status: `PASS`",
        "_demo_output/public-ai-safety/learning/learning_report.md": "Status: `PASS`",
        "_demo_output/public-ai-safety/learning/validation_report.md": "Status: `PASS`",
        "_demo_output/docs_link_report.md": "Status: `PASS`",
        "_demo_output/case_study_status_report.md": "Status: `PASS`",
    }
    for item, expected in report_expectations.items():
        path = ROOT / item
        if not path.exists():
            issues.append(f"missing generated report: {item}")
            continue
        if expected not in read(path):
            issues.append(f"generated report not PASS: {item}")
    return issues


def check_zip() -> list[str]:
    issues: list[str] = []
    if not ZIP_PATH.exists():
        return [f"missing zip: {ZIP_PATH}"]
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = set(zf.namelist())
    top = {name.split("/", 1)[0] for name in names if name}
    if top != {"proposal_builder_unified_portfolio_pack"}:
        issues.append(f"zip top-level folder mismatch: {sorted(top)}")
    for item in REQUIRED_ZIP_FILES:
        if item not in names:
            issues.append(f"missing zip file: {item}")
    for name in names:
        if BLOCKED_ZIP_RE.search(name):
            issues.append(f"blocked zip entry: {name}")
    return issues


def check_overclaims() -> list[str]:
    issues: list[str] = []
    targets = [
        ROOT / "README.md",
        *sorted((ROOT / "docs").glob("*.md")),
        *sorted((ROOT / "case-studies").rglob("*.md")),
        *sorted((ROOT / "examples").rglob("*.md")),
        *sorted((ROOT / "scripts").glob("*.py")),
        *sorted((ROOT / "tests").glob("*.py")),
    ]
    for path in targets:
        if not path.exists():
            continue
        if path.name in {"check_release_readiness.py", "check_case_study_status.py"}:
            continue
        for line_no, line in enumerate(read(path).splitlines(), start=1):
            if not OVERCLAIM_RE.search(line):
                continue
            if any(allowed in line for allowed in ALLOWED_OVERCLAIM_CONTEXT):
                continue
            issues.append(f"possible overclaim: {path.relative_to(ROOT)}:{line_no}: {line.strip()}")
    return issues


def write_report(issues: list[str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Release Readiness Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Zip: `{display_path(ZIP_PATH)}`",
        "",
        "## Checks",
        "",
        "- Required local files",
        "- Required generated demo/learning outputs",
        "- Generated report PASS status",
        "- Portfolio zip required entries",
        "- Portfolio zip exclusion patterns",
        "- README/docs overclaim scan",
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
            "- This release check validates portfolio packaging readiness only.",
            "- It does not publish to GitHub.",
            "- It does not train or evaluate a model.",
            "- It does not include generated demo outputs in the zip.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check portfolio release readiness.")
    parser.parse_args()

    issues: list[str] = []
    issues.extend(check_required_files(REQUIRED_LOCAL_FILES, "local file"))
    issues.extend(check_required_files(REQUIRED_GENERATED_FILES, "generated file"))
    issues.extend(check_generated_reports())
    issues.extend(check_zip())
    issues.extend(check_overclaims())
    write_report(issues)

    print(f"report={REPORT_PATH}")
    print(f"zip={ZIP_PATH}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} release_readiness")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
