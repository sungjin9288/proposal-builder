# Start Here

This package is a public-safe portfolio version of Proposal Builder.

## Quick Read Order

1. `PORTFOLIO.md` - one-page project summary.
2. `docs/reviewer-guide.md` - review path and reproduction commands.
3. `docs/claims-matrix.md` - claims mapped to evidence and verification.
4. `README.md` - full project context, architecture, and limitations.
5. `docs/verification-summary.md` - verification gates and generated reports.
6. `docs/third-party-notices.md` - third-party/source inclusion boundary.
7. `docs/assets/public-ai-safety-preview.svg` - generated visual preview.

## Quick Reproduction

From this `proposal-builder/` directory:

```bash
make demo
make preview
make learn
make validate-learning
make test
make docs-check
```

For the full local verification gate:

```bash
make final-check
```

After `make final-check`, upload metadata is written to:

```text
_portfolio_export/upload_manifest.json
_portfolio_export/upload_manifest.md
_portfolio_export/package_inventory.json
_portfolio_export/package_inventory.md
_portfolio_export/export_consistency_report.md
```

## What This Proves

- Public sample PRD to slide IR generation.
- Editable PPTX generation from public sample data.
- QA report generation.
- Public-safe learning JSONL preparation and validation.
- SVG preview generation from slide IR.
- Public-safe zip packaging, direct zip audit, and extracted-package smoke testing.

## What This Does Not Claim

- No web UI or API server is implemented here.
- No model training, fine-tuning, evaluation, or deployment is performed here.
- No private client deliverables or raw source documents are included.
- No HWP generation is claimed complete without a verified Windows/Hancom worker run.
- No production SaaS readiness is claimed.

## Upload Artifact

```text
_portfolio_export/proposal_builder_unified_portfolio_pack.zip
```
