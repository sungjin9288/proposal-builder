#!/usr/bin/env python3
"""Build a public-safe learning dataset from Proposal Builder slide IR.

This script does not train a model. It converts `slides.json` into JSONL rows
that can be handed to a downstream learning system such as DecisionDoc.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLIDES = ROOT / "_demo_output" / "public-ai-safety" / "slides.json"
DEFAULT_OUTPUT = ROOT / "_demo_output" / "public-ai-safety" / "learning"
REQUIRED_SLIDE_FIELDS = {"id", "title", "subtitle", "bullets", "layout_type", "section"}


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def json_line(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def validate_ir(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not payload.get("project_id"):
        issues.append("missing project_id")
    slides = payload.get("slides")
    if not isinstance(slides, list) or not slides:
        issues.append("missing slides list")
        return issues
    for index, slide in enumerate(slides, start=1):
        missing = REQUIRED_SLIDE_FIELDS - set(slide)
        if missing:
            issues.append(f"slide {index} missing fields: {', '.join(sorted(missing))}")
        if not isinstance(slide.get("bullets"), list) or not slide.get("bullets"):
            issues.append(f"slide {index} missing bullet list")
    return issues


def slide_to_learning_row(project_id: str, slide: dict[str, Any], index: int, source_slides: Path) -> dict[str, Any]:
    bullets = [str(item).strip() for item in slide.get("bullets", []) if str(item).strip()]
    prompt = (
        "Create a Korean proposal slide draft from the structured slide intent. "
        f"Section: {slide.get('section')}. Layout: {slide.get('layout_type')}. "
        f"Title: {slide.get('title')}. Subtitle: {slide.get('subtitle')}."
    )
    completion = {
        "title": slide.get("title"),
        "subtitle": slide.get("subtitle"),
        "bullets": bullets,
        "layout_type": slide.get("layout_type"),
        "section": slide.get("section"),
    }
    return {
        "record_id": f"{project_id}:{slide.get('id', f'slide-{index:02d}')}",
        "project_id": project_id,
        "source": "proposal-builder-public-demo",
        "source_file": str(source_slides),
        "task": "slide_outline_generation",
        "input": prompt,
        "output": completion,
        "metadata": {
            "slide_index": index,
            "slide_id": slide.get("id"),
            "layout_type": slide.get("layout_type"),
            "section": slide.get("section"),
            "public_safe": True,
            "contains_private_project_data": False,
        },
    }


def split_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(rows) <= 1:
        return rows, []
    validation_count = max(1, round(len(rows) * 0.2))
    train_count = max(1, len(rows) - validation_count)
    return rows[:train_count], rows[train_count:]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json_line(row) for row in rows) + ("\n" if rows else ""), encoding="utf-8")


def build_dataset(slides_path: Path, output_dir: Path) -> tuple[bool, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = read_json(slides_path)
    issues = validate_ir(payload)
    rows: list[dict[str, Any]] = []
    if not issues:
        project_id = str(payload.get("project_id"))
        rows = [
            slide_to_learning_row(project_id, slide, index, slides_path)
            for index, slide in enumerate(payload["slides"], start=1)
        ]

    train_rows, validation_rows = split_rows(rows)
    all_path = output_dir / "dataset.jsonl"
    train_path = output_dir / "train.jsonl"
    validation_path = output_dir / "validation.jsonl"
    manifest_path = output_dir / "dataset_manifest.json"
    report_path = output_dir / "learning_report.md"

    write_jsonl(all_path, rows)
    write_jsonl(train_path, train_rows)
    write_jsonl(validation_path, validation_rows)

    manifest = {
        "generated_at": now(),
        "status": "PASS" if not issues else "NEEDS_FIX",
        "source_slides": str(slides_path),
        "output_dir": str(output_dir),
        "dataset": str(all_path),
        "train": str(train_path),
        "validation": str(validation_path),
        "row_count": len(rows),
        "train_count": len(train_rows),
        "validation_count": len(validation_rows),
        "task": "slide_outline_generation",
        "model_training_executed": False,
        "public_safe": True,
        "issues": issues,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Learning Dataset Report",
        "",
        f"- Generated: `{manifest['generated_at']}`",
        f"- Status: `{manifest['status']}`",
        f"- Source slides: `{slides_path}`",
        f"- Dataset: `{all_path}`",
        f"- Train split: `{train_path}`",
        f"- Validation split: `{validation_path}`",
        f"- Row count: `{len(rows)}`",
        f"- Train count: `{len(train_rows)}`",
        f"- Validation count: `{len(validation_rows)}`",
        f"- Model training executed: `False`",
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
            "- This step creates learning dataset rows only.",
            "- It does not fine-tune or train a model.",
            "- It does not call external APIs.",
            "- It uses the public demo IR, not private project files.",
            "- `_demo_output/` and JSONL outputs are excluded from the portfolio zip.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return not issues, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build learning JSONL rows from Proposal Builder slides.json.")
    parser.add_argument("--slides", default=str(DEFAULT_SLIDES), help="path to slides.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="output directory for JSONL and reports")
    args = parser.parse_args()

    slides_path = Path(args.slides).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()
    if not slides_path.exists():
        print(f"missing slides.json: {slides_path}", file=sys.stderr)
        return 2

    ok, manifest = build_dataset(slides_path, output_dir)
    print(f"dataset={manifest['dataset']}")
    print(f"train={manifest['train']}")
    print(f"validation={manifest['validation']}")
    print(f"report={output_dir / 'learning_report.md'}")
    print(f"rows={manifest['row_count']}")
    print(f"RESULT {'PASS' if ok else 'NEEDS_FIX'} learning_dataset")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
