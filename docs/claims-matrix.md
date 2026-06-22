# Claims Matrix

## Purpose

This matrix maps portfolio claims to implemented evidence and verification commands. It is intended to keep the portfolio narrative grounded in what is actually present in the package.

## Verified Claims

| Claim | Evidence | Verification | Status |
|---|---|---|---|
| Public sample PRD can be converted into slide IR | `examples/public-ai-safety/prd.md`, `scripts/proposal_builder_cli.py`, generated `slides.json` | `make demo` | Verified |
| Public sample workflow generates an editable PPTX file | `scripts/proposal_builder_cli.py`, generated `output.pptx` | `make demo` | Verified |
| Demo workflow produces a QA report | generated `qa_report.md`, `docs/demo-evidence.md` | `make demo` | Verified |
| Public sample slide IR can be converted into a visual preview | `scripts/build_demo_preview.py`, `docs/assets/public-ai-safety-preview.svg` | `make preview` | Verified |
| Slide IR can be converted into learning-ready JSONL rows | `scripts/build_learning_dataset.py`, `docs/learning-dataset-schema.md` | `make learn` | Verified |
| Learning data split and metadata can be validated | `scripts/validate_learning_dataset.py`, generated `validation_report.md` | `make validate-learning` | Verified |
| Public workflow has regression test coverage | `tests/test_public_workflow.py`, `docs/test-evidence.md` | `make test` | Verified |
| Public documentation local links can be checked | `scripts/check_docs_links.py`, generated `docs_link_report.md` | `make docs-check` | Verified |
| Public portfolio package is allowlist-built | `scripts/build_portfolio_package.py` | `make package` and `make verify` | Verified |
| Zip contents are scanned for blocked paths, raw formats, and basic credential patterns | `scripts/audit_portfolio_package.py`, `_portfolio_export/package_audit.md` | `make audit` | Verified |
| Packaged zip can be extracted and rerun independently | `scripts/smoke_portfolio_package.py`, `_portfolio_export/package_smoke_report.md` | `make package-smoke` | Verified |
| Packaged zip contents can be reviewed without extraction | `scripts/write_package_inventory.py`, `_portfolio_export/package_inventory.md` | `make inventory` | Verified |
| Export metadata stays internally consistent | `scripts/check_export_consistency.py`, `_portfolio_export/export_consistency_report.md` | `make export-consistency` | Verified |
| Sanitized case-study evidence exists for the AI safety proposal workflow | `case-studies/ai-safety-v3/` | `make final-check` verifies required entries | Verified as documentation evidence |

## Claims Not Made

| Claim | Reason |
|---|---|
| Web UI is complete | Web UI is planned for DecisionDoc, not this repository |
| API server is complete | No API server is implemented here |
| Model training, fine-tuning, evaluation, or deployment is complete | This repository prepares and validates JSONL only |
| HWP generation is complete | HWP generation needs a verified Windows/Hancom worker run |
| Private client deliverables are included | Private project files and raw source documents are intentionally excluded |
| Production SaaS operation is proven | This is a local PoC / public portfolio package |

## Full Verification Command

```bash
make final-check
```

This command covers public demo generation, preview generation, learning dataset generation and validation, tests, package build, package verification, direct zip audit, and extracted-package smoke testing.
