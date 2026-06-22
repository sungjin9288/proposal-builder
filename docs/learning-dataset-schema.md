# Learning Dataset Schema

## Purpose

Proposal Builder exports slide-level JSONL rows from `slides.json` so a downstream project such as DecisionDoc can consume proposal-writing examples without requiring raw client files.

This repository prepares and validates the dataset. It does not train, fine-tune, evaluate, host, or deploy a model.

## JSONL Row

Each line in `dataset.jsonl`, `train.jsonl`, and `validation.jsonl` is one JSON object.

```json
{
  "record_id": "public-ai-safety-demo:slide-01",
  "project_id": "public-ai-safety-demo",
  "source": "proposal-builder-public-demo",
  "source_file": ".../slides.json",
  "task": "slide_outline_generation",
  "input": "Create a Korean proposal slide draft...",
  "output": {
    "title": "공공 문서 자동화 데모",
    "subtitle": "PRD 기반 슬라이드 IR 및 QA 자동화 데모",
    "bullets": ["..."],
    "layout_type": "cover",
    "section": "overview"
  },
  "metadata": {
    "slide_index": 1,
    "slide_id": "slide-01",
    "layout_type": "cover",
    "section": "overview",
    "public_safe": true,
    "contains_private_project_data": false
  }
}
```

## Required Top-Level Fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `record_id` | string | yes | Stable row id |
| `project_id` | string | yes | Source project id |
| `source` | string | yes | Dataset source label |
| `source_file` | string | yes | Origin `slides.json` path |
| `task` | string | yes | Currently `slide_outline_generation` |
| `input` | string | yes | Prompt/input text |
| `output` | object | yes | Slide output payload |
| `metadata` | object | yes | Safety and trace metadata |

## Required Output Fields

| Field | Type | Required |
|---|---|---:|
| `title` | string | yes |
| `subtitle` | string | yes |
| `bullets` | string array | yes |
| `layout_type` | string | yes |
| `section` | string | yes |

## Required Metadata Fields

| Field | Type | Required | Expected |
|---|---|---:|---|
| `slide_index` | integer | yes | 1-based index |
| `slide_id` | string | yes | Source slide id |
| `layout_type` | string | yes | Mirrors output layout |
| `section` | string | yes | Mirrors output section |
| `public_safe` | boolean | yes | Must be `true` for public demo |
| `contains_private_project_data` | boolean | yes | Must be `false` for public demo |

## Local Commands

```bash
make learn
make validate-learning
```

Generated local files:

```text
_demo_output/public-ai-safety/learning/dataset.jsonl
_demo_output/public-ai-safety/learning/train.jsonl
_demo_output/public-ai-safety/learning/validation.jsonl
_demo_output/public-ai-safety/learning/dataset_manifest.json
_demo_output/public-ai-safety/learning/learning_report.md
_demo_output/public-ai-safety/learning/validation_report.md
```

`_demo_output/` is excluded from the portfolio zip.
