#!/usr/bin/env python3
"""Validate the public-safe AI Safety V3 case-study integration.

This check keeps the former local-workspace evidence attached to the
Proposal Builder portfolio as a verifiable case study. It does not re-run the
private workspace commands or require raw PPT/PDF files.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "case-studies" / "ai-safety-v3"
REPORT_PATH = ROOT / "_demo_output" / "case_study_status_report.md"

REQUIRED_FILES = [
    "README.md",
    "docs/implementation-evidence.md",
    "docs/evidence-checklist.md",
    "docs/evidence-gallery.md",
    "evidence/evidence_manifest.md",
    "evidence/architecture/current-architecture.md",
    "evidence/architecture/cli-sequence.md",
    "evidence/api-responses/not_applicable.md",
    "evidence/screenshots/not_applicable.md",
    "evidence/cli-logs/analyze_v3_proposal_editability.log",
    "evidence/cli-logs/check_ai_training_readiness.log",
    "evidence/cli-logs/check_final_fix_readiness.log",
    "evidence/cli-logs/check_visual_ppt_conversion_inputs.log",
    "evidence/cli-logs/validate_ai_training_workspace.log",
    "evidence/cli-logs/validate_revision_log.log",
    "evidence/output-artifacts/ai_training_workspace_validation.md",
    "evidence/output-artifacts/ai_training_workspace_validation.json",
    "evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.md",
    "evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.json",
    "evidence/output-artifacts/ai_training_readiness/ai_training_readiness_runbook.md",
    "evidence/output-artifacts/visual_ppt_conversion_input_check.md",
    "evidence/output-artifacts/v3_proposal_editability_report.md",
    "evidence/output-artifacts/v3_proposal_editability_inventory.json",
]

EXPECTED_TEXT = {
    "README.md": [
        "Relationship To Proposal Builder",
        "not as a separate unrelated product",
        "actual model training",
        "final external submission readiness",
    ],
    "docs/implementation-evidence.md": [
        "Visual PPT conversion input validation implemented",
        "Final submission readiness is gate-controlled",
        "actual model training not complete",
        "Web frontend",
        "API server",
    ],
    "evidence/evidence_manifest.md": [
        "Not classified as: web app, API service, deployed SaaS, production ML system",
        "Result",
        "Exclusions",
    ],
    "evidence/output-artifacts/v3_proposal_editability_report.md": [
        "PPTX_EDITABILITY_INVENTORY_READY",
        "Slide count: `31`",
        "Training command allowed: `false`",
    ],
    "evidence/output-artifacts/visual_ppt_conversion_input_check.md": [
        "Status: `VISUAL_CONVERSION_INPUTS_READY`",
        "Reference PPTX slides | `39`",
        "Training command allowed: `false`",
    ],
    "evidence/output-artifacts/ai_training_workspace_validation.md": [
        "Status: `NEEDS_INPUT`",
        "Training command allowed: `false`",
        "jsonl_total_rows: `768`",
    ],
    "evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.md": [
        "Status: `PARTIAL_READY_TRAINING_BLOCKED`",
        "Training command allowed: `false`",
        "READY_FOR_PACKAGE_DRY_RUN",
    ],
}

LOG_EXPECTATIONS = {
    "evidence/cli-logs/analyze_v3_proposal_editability.log": [
        "RESULT PASS pptx_editability_inventory",
        "exit_code=0",
        "external_submission_state=NOT_EXTERNAL_FINAL",
        "training_command_allowed=false",
    ],
    "evidence/cli-logs/check_visual_ppt_conversion_inputs.log": [
        "RESULT PASS visual_ppt_conversion_inputs",
        "exit_code=0",
        "status=VISUAL_CONVERSION_INPUTS_READY",
        "training_command_allowed=false",
    ],
    "evidence/cli-logs/validate_revision_log.log": [
        "RESULT PASS revision_log",
        "exit_code=0",
    ],
    "evidence/cli-logs/check_final_fix_readiness.log": [
        "decision=WAITING_FOR_REVIEW_INPUT",
        "external=NOT_EXTERNAL_FINAL",
        "exit_code=0",
    ],
    "evidence/cli-logs/validate_ai_training_workspace.log": [
        "RESULT NEEDS_INPUT ai_training_workspace_validation",
        "exit_code=2",
        "status=NEEDS_INPUT",
    ],
    "evidence/cli-logs/check_ai_training_readiness.log": [
        "RESULT BLOCKED ai_training_readiness",
        "exit_code=2",
        "status=PARTIAL_READY_TRAINING_BLOCKED",
        "training_command_allowed=false",
    ],
}

FORBIDDEN_CLAIMS = [
    r"\bproduction-ready\b",
    r"\benterprise\b",
    r"상용 운영",
    r"엔터프라이즈",
    r"모델 학습 완료",
    r"fine.?tuning 완료",
    r"외부 제출 완료",
]

FORBIDDEN_SENSITIVE_TOKENS = [
    "\ub2e4\uc6b8",
    "\u0044\u0041\u0057\u004f\u004f\u004c",
    "proposal" + "-v3-work",
    str(Path.home()),
]

ALLOWED_CONTEXT = [
    "not complete",
    "does not claim",
    "not classified",
    "not applicable",
    "do not claim",
    "범위가 아닙니다",
    "미완료",
    "미구현",
    "주장하지",
    "주장 금지",
    "근거는 확인되지",
    "코드 근거 없음",
    "아닙니다",
]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_case_file(relative: str) -> str:
    return (CASE_ROOT / relative).read_text(encoding="utf-8", errors="ignore")


def check_required_files() -> list[str]:
    return [f"missing case-study file: {item}" for item in REQUIRED_FILES if not (CASE_ROOT / item).exists()]


def check_expected_text() -> list[str]:
    issues: list[str] = []
    for relative, expected_values in EXPECTED_TEXT.items():
        path = CASE_ROOT / relative
        if not path.exists():
            continue
        text = read_case_file(relative)
        for expected in expected_values:
            if expected not in text:
                issues.append(f"missing expected text: {relative}: {expected}")
    for relative, expected_values in LOG_EXPECTATIONS.items():
        path = CASE_ROOT / relative
        if not path.exists():
            continue
        text = read_case_file(relative)
        for expected in expected_values:
            if expected not in text:
                issues.append(f"missing expected log marker: {relative}: {expected}")
    return issues


def check_manifest_log_coverage() -> list[str]:
    manifest = CASE_ROOT / "evidence" / "evidence_manifest.md"
    if not manifest.exists():
        return []
    text = manifest.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []
    for relative in sorted(LOG_EXPECTATIONS):
        name = Path(relative).name
        if name not in text:
            issues.append(f"manifest missing cli log entry: {name}")
    return issues


def check_forbidden_claims() -> list[str]:
    issues: list[str] = []
    targets = [
        CASE_ROOT / "README.md",
        *sorted((CASE_ROOT / "docs").rglob("*.md")),
        *sorted((CASE_ROOT / "evidence").rglob("*.md")),
    ]
    patterns = [re.compile(pattern, re.I) for pattern in FORBIDDEN_CLAIMS]
    for path in targets:
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            if not any(pattern.search(line) for pattern in patterns):
                continue
            lowered = line.lower()
            if any(context.lower() in lowered for context in ALLOWED_CONTEXT):
                continue
            issues.append(f"possible unsupported claim: {rel(path)}:{line_no}: {line.strip()}")
    return issues


def check_sensitive_tokens() -> list[str]:
    issues: list[str] = []
    targets = [
        CASE_ROOT / "README.md",
        *sorted((CASE_ROOT / "docs").rglob("*")),
        *sorted((CASE_ROOT / "evidence").rglob("*")),
    ]
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN_SENSITIVE_TOKENS:
            if token in text:
                issues.append(f"case-study sensitive token found: {rel(path)}: {token}")
    return issues


def write_report(issues: list[str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not issues else "NEEDS_FIX"
    lines = [
        "# Case Study Status Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Case study: `{rel(CASE_ROOT)}`",
        f"- Required files checked: `{len(REQUIRED_FILES)}`",
        f"- CLI logs checked: `{len(LOG_EXPECTATIONS)}`",
        "",
        "## Checks",
        "",
        "- Required sanitized case-study files exist",
        "- Evidence manifest covers the expected CLI logs",
        "- CLI logs preserve pass/blocking states",
        "- Output reports preserve non-final and no-training boundaries",
        "- Case-study docs avoid unsupported production/API/model-training claims",
        "- Case-study docs avoid private workspace paths and organization tokens",
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
            "- This validates the public-safe case-study package only.",
            "- It does not read private source decks or raw client materials.",
            "- It does not rerun model training or external submission workflows.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check AI Safety V3 case-study integration status.")
    parser.parse_args()

    issues: list[str] = []
    issues.extend(check_required_files())
    issues.extend(check_expected_text())
    issues.extend(check_manifest_log_coverage())
    issues.extend(check_forbidden_claims())
    issues.extend(check_sensitive_tokens())
    write_report(issues)

    print(f"report={REPORT_PATH}")
    print(f"case_study={CASE_ROOT}")
    print(f"RESULT {'PASS' if not issues else 'NEEDS_FIX'} case_study_status")
    if issues:
        for issue in issues:
            print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
