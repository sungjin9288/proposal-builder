# Public Portfolio Publication Checklist

## Before Upload

- Run `make final-check`.
- Confirm `_portfolio_export/proposal_builder_unified_portfolio_pack.zip` exists.
- Confirm `_portfolio_export/package_audit.md` status is `PASS`.
- Confirm `_portfolio_export/package_smoke_report.md` status is `PASS`.
- Confirm `_demo_output/docs_link_report.md` status is `PASS`.
- Confirm `_portfolio_export/upload_manifest.json` exists.
- Confirm `_portfolio_export/upload_manifest.md` exists.
- Confirm `_portfolio_export/package_inventory.json` exists.
- Confirm `_portfolio_export/package_inventory.md` exists.
- Confirm `_portfolio_export/export_consistency_report.md` status is `PASS`.
- Confirm `_demo_output/release_readiness_report.md` status is `PASS`.
- Review `PORTFOLIO.md` and `README.md` for scope wording.
- Do not upload local `projects/`, `archive/`, `_demo_output/`, or raw PPTX/PDF/HWP files.

## Upload File

```text
_portfolio_export/proposal_builder_unified_portfolio_pack.zip
```

## Reviewer Entry Points

- `PORTFOLIO.md`
- `START_HERE.md`
- `README.md`
- `docs/reviewer-guide.md`
- `docs/claims-matrix.md`
- `docs/verification-summary.md`
- `docs/third-party-notices.md`
- `docs/release-note.md`
- `docs/demo-evidence.md`
- `docs/test-evidence.md`
- `docs/assets/public-ai-safety-preview.svg`
- `case-studies/ai-safety-v3/README.md`

## Claims To Avoid

- Do not claim web UI or API server completion in this repository.
- Do not claim model training, fine-tuning, evaluation, or deployment completion.
- Do not claim HWP generation is complete without a verified Windows/Hancom worker run.
- Do not claim production SaaS readiness.
- Do not describe private client deliverables as included in this package.

## Verified Positioning

This package demonstrates the functional core of a local proposal automation workflow: public sample PRD ingestion, slide IR creation, editable PPTX generation, QA report generation, learning dataset preparation, public preview generation, and public-safe packaging.
