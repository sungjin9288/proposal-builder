# AI Training Readiness Runbook

## Current Gate

- Status: `PARTIAL_READY_TRAINING_BLOCKED`
- Training command allowed: `false`
- Model training: `not executed`

## Required Before Training

1. Fill pending sample packets with real source files.
2. Complete analysis/output/review documents with no TODO markers.
3. Generate reviewed sample JSONL rows.
4. Promote reviewed rows into central datasets after dry-run approval.
5. Rerun readiness until all feature blockers are cleared.

## Current Priority

- Planning Documentation AI needs more reviewed government task samples.
- Editable PPT Conversion AI has enough 002-derived evaluator rows for dry-run analysis, but needs more job diversity before model training.

## Training Guardrail

Do not run fine-tuning or model training commands until this readiness report returns `READY_FOR_PACKAGE_DRY_RUN` and the user explicitly approves training.
