# DecisionDoc Handoff

## Boundary

Proposal Builder prepares structured proposal-writing data. DecisionDoc is the intended downstream project for web UI, API, model orchestration, or training workflows.

This repository stops at:

- public PRD sample
- slide IR generation
- PPTX demo generation
- QA report generation
- learning JSONL export
- learning JSONL validation

This repository does not implement:

- DecisionDoc web UI
- API server
- model fine-tuning
- model evaluation
- deployment

## Handoff Files

Generated locally by:

```bash
make validate-learning
```

Files:

```text
_demo_output/public-ai-safety/learning/dataset.jsonl
_demo_output/public-ai-safety/learning/train.jsonl
_demo_output/public-ai-safety/learning/validation.jsonl
_demo_output/public-ai-safety/learning/dataset_manifest.json
_demo_output/public-ai-safety/learning/learning_report.md
_demo_output/public-ai-safety/learning/validation_report.md
```

These generated files are intentionally excluded from the portfolio zip. The reusable scripts and schema docs are included instead.

## Validation Summary

- Dataset rows: `5`
- Train rows: `4`
- Validation rows: `1`
- Schema validation: `PASS`
- Public-safe metadata validation: `PASS`
- Model training executed: `False`

## Recommended DecisionDoc Intake

DecisionDoc can consume:

- `dataset.jsonl` for full local review
- `train.jsonl` for training experiments
- `validation.jsonl` for smoke evaluation
- `dataset_manifest.json` for provenance and boundary checks

Before DecisionDoc uses this data for actual training, add more real public-safe samples and human-reviewed labels. The current 5-row demo dataset is proof of pipeline behavior, not a meaningful model-training corpus.
