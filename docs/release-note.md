# Portfolio Release Note

## Release

- Package: `proposal_builder_unified_portfolio_pack.zip`
- Root: `<proposal-builder-root>`
- Audience: portfolio review / implementation evidence review
- Scope: public-safe framework and sanitized evidence package

## Latest Published Artifact

- Release tag: `portfolio-v0.1.1`
- Release URL: `https://github.com/sungjin9288/proposal-builder/releases/tag/portfolio-v0.1.1`
- Asset URL: `https://github.com/sungjin9288/proposal-builder/releases/download/portfolio-v0.1.1/proposal_builder_unified_portfolio_pack.zip`
- Asset size bytes: `198571`
- Asset SHA256: `a12292435da94bf2bde1a00b2072e6d9e3b5d64ec432b3c61f85b5360cab809e`
- Release commit: `ed9d79b2cdfa5938b8d464740f4a926e459198e3`

## Release History

| Tag | Purpose | SHA256 |
|---|---|---|
| `portfolio-v0.1.1` | Adds post-release evidence docs and package URL sanitization | `a12292435da94bf2bde1a00b2072e6d9e3b5d64ec432b3c61f85b5360cab809e` |
| `portfolio-v0.1.0` | Initial public-safe portfolio package | `fa204745711c60dbe0534c59eb011c17683082b89d40b7b633de5f4c0e827fb1` |

## Reissue — 2026-10-20

Internal client identifiers were removed from every commit, and the history was rewritten, so all commit SHAs changed. Both release assets were rebuilt from the rewritten tags and replaced in place. The checksums and release commit above refer to the rebuilt assets. Each rebuilt zip has the same 88 entries, passes `make check` after extraction, and contains none of the removed identifiers.

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
