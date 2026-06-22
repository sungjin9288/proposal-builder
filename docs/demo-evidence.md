# Public Demo Evidence

## Purpose

This document records the verified end-to-end demo path for the public portfolio version of Proposal Builder.

## Command

```bash
make demo
make preview
make learn
```

Equivalent direct command:

```bash
python3 scripts/proposal_builder_cli.py demo
```

## Verified Result

- Status: `PASS`
- Source PRD: `examples/public-ai-safety/prd.md`
- Generated IR: `_demo_output/public-ai-safety/slides.json`
- Generated PPTX: `_demo_output/public-ai-safety/output.pptx`
- Generated QA report: `_demo_output/public-ai-safety/qa_report.md`
- Generated SVG preview: `docs/assets/public-ai-safety-preview.svg`
- Generated learning dataset: `_demo_output/public-ai-safety/learning/dataset.jsonl`
- Generated train split: `_demo_output/public-ai-safety/learning/train.jsonl`
- Generated validation split: `_demo_output/public-ai-safety/learning/validation.jsonl`
- Generated learning report: `_demo_output/public-ai-safety/learning/learning_report.md`
- Generated validation report: `_demo_output/public-ai-safety/learning/validation_report.md`

## QA Summary

The generated QA report recorded:

- PPTX exists: `True`
- slides.json exists: `True`
- Slide count: `5`
- Shape count: `69`
- Forbidden token hits: `0`
- Issues: `None`

## Learning Dataset Summary

The generated learning report recorded:

- Status: `PASS`
- Row count: `5`
- Train count: `4`
- Validation count: `1`
- Model training executed: `False`
- Issues: `None`

## Preview Summary

The generated preview command recorded:

- Status: `PASS`
- Source IR: `_demo_output/public-ai-safety/slides.json`
- Slide cards: `5`
- Generated preview: `docs/assets/public-ai-safety-preview.svg`

## Learning Validation Summary

The generated validation report recorded:

- Status: `PASS`
- Dataset rows: `5`
- Train rows: `4`
- Validation rows: `1`
- Issues: `None`
- Model training executed: not performed

## Boundary

- `_demo_output/` is a local generated output folder and is excluded from the portfolio zip.
- `docs/assets/public-ai-safety-preview.svg` is generated from public sample data and is included in the portfolio zip.
- The demo uses only `examples/public-ai-safety/prd.md`.
- The demo does not use private project data.
- The demo does not call external APIs.
- The demo does not generate HWP output.
- The demo does not claim model training or deployment.
- The learning step creates JSONL dataset rows only; model fine-tuning and evaluation are outside this project.
- DecisionDoc can consume these generated JSONL files later, but web/API/training orchestration is outside this repository.

## Packaging Verification

```bash
make package
make verify
```

Verified zip:

```text
_portfolio_export/proposal_builder_unified_portfolio_pack.zip
```

The package includes `scripts/proposal_builder_cli.py` and `examples/public-ai-safety/prd.md`, but excludes `_demo_output/` and generated PPTX files.
