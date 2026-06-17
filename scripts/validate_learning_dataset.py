#!/usr/bin/env python3
"""Validate Proposal Builder learning JSONL outputs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "_demo_output" / "public-ai-safety" / "learning" / "dataset.jsonl"
DEFAULT_TRAIN = ROOT / "_demo_output" / "public-ai-safety" / "learning" / "train.jsonl"
DEFAULT_VALIDATION = ROOT / "_demo_output" / "public-ai-safety" / "learning" / "validation.jsonl"
DEFAULT_REPORT = ROOT / "_demo_output" / "public-ai-safety" / "learning" / "validation_report.md"

TOP_LEVEL_FIELDS = {"record_id", "project_id", "source", "source_file", "task", "input", "output", "metadata"}
OUTPUT_FIELDS = {"title", "subtitle", "bullets", "layout_type", "section"}
METADATA_FIELDS = {"slide_index", "slide_id", "layout_type", "section", "public_safe", "contains_private_project_data"}


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows, [f"missing file: {path}"]
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"{path.name}:{line_no}: invalid json: {exc}")
            continue
        if not isinstance(row, dict):
            issues.append(f"{path.name}:{line_no}: row is not object")
            continue
        rows.append(row)
    return rows, issues


def validate_row(row: dict[str, Any], row_no: int, source_name: str) -> list[str]:
    issues: list[str] = []
    missing = TOP_LEVEL_FIELDS - set(row)
    if missing:
        issues.append(f"{source_name}:{row_no}: missing top-level fields: {', '.join(sorted(missing))}")
        return issues

    for field in ["record_id", "project_id", "source", "source_file", "task", "input"]:
        if not isinstance(row.get(field), str) or not row[field].strip():
            issues.append(f"{source_name}:{row_no}: {field} must be non-empty string")

    output = row.get("output")
    if not isinstance(output, dict):
        issues.append(f"{source_name}:{row_no}: output must be object")
    else:
        missing_output = OUTPUT_FIELDS - set(output)
        if missing_output:
            issues.append(f"{source_name}:{row_no}: missing output fields: {', '.join(sorted(missing_output))}")
        if not isinstance(output.get("bullets"), list) or not output.get("bullets"):
            issues.append(f"{source_name}:{row_no}: output.bullets must be non-empty array")

    metadata = row.get("metadata")
    if not isinstance(metadata, dict):
        issues.append(f"{source_name}:{row_no}: metadata must be object")
    else:
        missing_metadata = METADATA_FIELDS - set(metadata)
        if missing_metadata:
            issues.append(f"{source_name}:{row_no}: missing metadata fields: {', '.join(sorted(missing_metadata))}")
        if metadata.get("public_safe") is not True:
            issues.append(f"{source_name}:{row_no}: metadata.public_safe must be true")
        if metadata.get("contains_private_project_data") is not False:
            issues.append(f"{source_name}:{row_no}: metadata.contains_private_project_data must be false")

    return issues


def validate_file(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows, issues = read_jsonl(path)
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        issues.extend(validate_row(row, index, path.name))
        record_id = row.get("record_id")
        if isinstance(record_id, str):
            if record_id in seen:
                issues.append(f"{path.name}:{index}: duplicate record_id: {record_id}")
            seen.add(record_id)
    return rows, issues


def write_report(report: Path, status: str, dataset: Path, train: Path, validation: Path, counts: dict[str, int], issues: list[str]) -> None:
    lines = [
        "# Learning Dataset Validation Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{status}`",
        f"- Dataset: `{dataset}`",
        f"- Train: `{train}`",
        f"- Validation: `{validation}`",
        f"- Dataset rows: `{counts.get('dataset', 0)}`",
        f"- Train rows: `{counts.get('train', 0)}`",
        f"- Validation rows: `{counts.get('validation', 0)}`",
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
            "- This validation checks JSONL schema and public-safety metadata.",
            "- It does not train, fine-tune, evaluate, or deploy a model.",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Proposal Builder learning JSONL files.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--train", default=str(DEFAULT_TRAIN))
    parser.add_argument("--validation", default=str(DEFAULT_VALIDATION))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    dataset = Path(args.dataset).expanduser().resolve()
    train = Path(args.train).expanduser().resolve()
    validation = Path(args.validation).expanduser().resolve()
    report = Path(args.report).expanduser().resolve()

    dataset_rows, dataset_issues = validate_file(dataset)
    train_rows, train_issues = validate_file(train)
    validation_rows, validation_issues = validate_file(validation)
    issues = dataset_issues + train_issues + validation_issues

    dataset_ids = {row.get("record_id") for row in dataset_rows}
    split_ids = {row.get("record_id") for row in train_rows + validation_rows}
    if dataset_ids != split_ids:
        issues.append("train+validation record ids do not match dataset record ids")
    if set(row.get("record_id") for row in train_rows) & set(row.get("record_id") for row in validation_rows):
        issues.append("train and validation splits overlap")

    counts = {"dataset": len(dataset_rows), "train": len(train_rows), "validation": len(validation_rows)}
    status = "PASS" if not issues else "NEEDS_FIX"
    write_report(report, status, dataset, train, validation, counts, issues)

    print(f"report={report}")
    print(f"dataset_rows={counts['dataset']}")
    print(f"train_rows={counts['train']}")
    print(f"validation_rows={counts['validation']}")
    print(f"RESULT {status} learning_dataset_validation")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
