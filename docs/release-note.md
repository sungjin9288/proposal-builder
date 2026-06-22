# Portfolio Release Note

## Release

- Package: `proposal_builder_unified_portfolio_pack.zip`
- Root: `<proposal-builder-root>`
- Audience: portfolio review / implementation evidence review
- Scope: public-safe framework and sanitized evidence package

## Published Artifact

- Release tag: `portfolio-v0.1.0`
- Release URL: `https://github.com/sungjin9288/proposal-builder/releases/tag/portfolio-v0.1.0`
- Asset URL: `https://github.com/sungjin9288/proposal-builder/releases/download/portfolio-v0.1.0/proposal_builder_unified_portfolio_pack.zip`
- Asset size bytes: `197459`
- Asset SHA256: `4a46f765e7fe07a3cc26dfc816b974fa0e1414153496a64449919648dafc05b8`
- Release commit: `5a3ce04421a640129cabda54fd9ea062edaf67e1`

## Post-Publish Verification

- GitHub release state: published, not draft
- Release asset was downloaded from GitHub and SHA256 matched the upload manifest.
- Downloaded release zip was extracted and `make check` passed inside the package.
- Downloaded release zip was scanned for blocked paths and raw/private file patterns.
- Downloaded release package was scanned for private organization and local workspace tokens.

## Included Capabilities

| Capability | Evidence |
|---|---|
| Public demo build | `make demo` generates `slides.json`, `output.pptx`, and `qa_report.md` from `examples/public-ai-safety/prd.md` |
| Public preview asset | `make preview` generates `docs/assets/public-ai-safety-preview.svg` from public demo slide IR |
| Learning dataset preparation | `make learn` generates slide-level JSONL, train/validation splits, manifest, and learning report |
| Dataset validation | `make validate-learning` checks required fields, metadata, split consistency, and public-safe flags |
| Regression tests | `make test` runs the public workflow tests |
| Documentation link check | `make docs-check` validates local Markdown links in public docs |
| Public-safe packaging | `make package` creates the zip with allowlisted files only |
| Package verification | `make verify` checks required entries and exclusion rules |
| Release readiness | `make release-check` validates generated reports, package contents, and overclaim boundaries |
| Upload audit | `make final-check` runs release readiness and direct zip content audit |
| Package smoke test | `make package-smoke` extracts the zip and reruns the public workflow inside the extracted package |
| Package inventory | `make inventory` records zip contents as categorized JSON and Markdown |
| Upload manifest | `make upload-manifest` records zip metadata, report statuses, and reproduction commands |
| Export consistency | `make export-consistency` verifies zip metadata is consistent across generated reports |

## Excluded From Package

- Private project folders: `projects/`, `archive/`
- Generated demo outputs: `_demo_output/`
- Raw document formats: `*.pptx`, `*.pdf`, `*.hwp`, `*.hwpx`
- Dataset exports: `*.jsonl`, `*.csv`
- Credentials and environment files: `.env`, `.env.*`, key/token/certificate files
- Dependency and cache folders
- Vendored third-party source trees

## Verified Boundaries

- No external API calls are required for the public demo.
- No private client material is used by the public demo.
- No model training or fine-tuning is performed in this repository.
- No web UI or API server is claimed as implemented here.
- HWP generation remains a placeholder until a Windows/Hancom worker is connected.

## Reviewer Path

```bash
make release-check
```

Then inspect:

```text
PORTFOLIO.md
START_HERE.md
README.md
docs/demo-evidence.md
docs/test-evidence.md
docs/reviewer-guide.md
docs/claims-matrix.md
docs/verification-summary.md
docs/third-party-notices.md
docs/decisiondoc-handoff.md
docs/publication-checklist.md
docs/assets/public-ai-safety-preview.svg
case-studies/ai-safety-v3/
_portfolio_export/proposal_builder_unified_portfolio_pack.zip
```
