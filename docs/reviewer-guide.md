# Reviewer Guide

## What To Review First

1. `START_HERE.md` - shortest entry point for reviewers.
2. `PORTFOLIO.md` - one-page scope summary and implemented/not-implemented boundary.
3. `README.md` - project background, architecture, commands, and limitations.
4. `docs/assets/public-ai-safety-preview.svg` - visual preview generated from the public sample IR.
5. `docs/claims-matrix.md` - portfolio claims mapped to evidence and verification commands.
6. `docs/verification-summary.md` - verification gates and generated report locations.
7. `docs/third-party-notices.md` - third-party/source inclusion boundary.
8. `docs/demo-evidence.md` - verified public demo outputs and QA result.
9. `docs/test-evidence.md` - automated test coverage summary.
10. `case-studies/ai-safety-v3/README.md` - sanitized implementation evidence case study.

## Fast Reproduction

From the extracted `proposal-builder/` directory:

```bash
make demo
make preview
make learn
make validate-learning
make test
make docs-check
```

Expected result:

- `make demo`: generates `slides.json`, `output.pptx`, and `qa_report.md`.
- `make preview`: generates `docs/assets/public-ai-safety-preview.svg`.
- `make learn`: generates public-safe JSONL train/validation files.
- `make validate-learning`: validates dataset schema and split consistency.
- `make test`: runs the public workflow regression tests.
- `make docs-check`: validates local Markdown links in public docs.

## Full Verification

From the source repository root:

```bash
make final-check
```

This runs:

- public demo generation
- learning dataset generation and validation
- SVG preview generation
- regression tests
- documentation link checks
- portfolio zip build and verification
- direct zip audit
- package smoke test after extracting the zip into a temporary directory

## Implemented Evidence

| Evidence | Location |
|---|---|
| Public sample PRD | `examples/public-ai-safety/prd.md` |
| Demo CLI | `scripts/proposal_builder_cli.py` |
| Learning dataset builder | `scripts/build_learning_dataset.py` |
| Dataset validator | `scripts/validate_learning_dataset.py` |
| Preview generator | `scripts/build_demo_preview.py` |
| Package builder | `scripts/build_portfolio_package.py` |
| Zip audit | `scripts/audit_portfolio_package.py` |
| Zip smoke test | `scripts/smoke_portfolio_package.py` |
| Docs link checker | `scripts/check_docs_links.py` |
| Package inventory writer | `scripts/write_package_inventory.py` |
| Export consistency checker | `scripts/check_export_consistency.py` |
| Tests | `tests/test_public_workflow.py` |

## Boundaries

- No private client project files are included.
- No raw PPTX/PDF/HWP source documents are included.
- No external APIs are required for the public demo.
- No model training, fine-tuning, evaluation, or deployment is performed here.
- No web UI or API server is implemented in this repository.
- HWP generation is documented as a placeholder until a verified Windows/Hancom worker run exists.

## What Not To Infer

Do not infer production SaaS readiness, model performance, external submission completion, or private client deliverable quality from this package. The package proves the local functional core and public-safe evidence workflow only.
