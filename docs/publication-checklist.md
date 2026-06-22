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

## Published Release

- Release tag: `portfolio-v0.1.0`
- Release URL: `https://github.com/sungjin9288/proposal-builder/releases/tag/portfolio-v0.1.0`
- Asset URL: `https://github.com/sungjin9288/proposal-builder/releases/download/portfolio-v0.1.0/proposal_builder_unified_portfolio_pack.zip`
- Asset SHA256: `4a46f765e7fe07a3cc26dfc816b974fa0e1414153496a64449919648dafc05b8`

## After Upload

- Confirm the GitHub release is published, not draft.
- Download the release asset from GitHub.
- Verify the downloaded asset SHA256 matches the upload manifest.
- Extract the downloaded asset and run `make check` inside the package.
- Scan the original release zip entries for blocked paths and raw/private file patterns.

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
