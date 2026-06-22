# Verification Summary

## Purpose

This document summarizes the verification gates used for the public Proposal Builder portfolio package. It is included inside the zip so reviewers can understand the validation story before running commands.

## Primary Command

```bash
make final-check
```

## Published Release Check

- Release URL: `https://github.com/sungjin9288/proposal-builder/releases/tag/portfolio-v0.1.1`
- Asset URL: `https://github.com/sungjin9288/proposal-builder/releases/download/portfolio-v0.1.1/proposal_builder_unified_portfolio_pack.zip`
- Expected SHA256: `f917b489ffc38d45653ddd4389f25e322271e81a8f1d9f87c5d74ef23b00443f`

Post-publish verification downloaded the GitHub release asset, checked the SHA256, extracted the package, ran `make check` inside the extracted package, and scanned the release zip for blocked private/raw file patterns.

## Gates Covered

| Gate | Command | What It Verifies |
|---|---|---|
| Public demo build | `make demo` | Public sample PRD generates `slides.json`, `output.pptx`, and `qa_report.md` |
| SVG preview | `make preview` | Public slide IR generates `docs/assets/public-ai-safety-preview.svg` |
| Learning data export | `make learn` | Slide IR generates public-safe JSONL dataset and train/validation split |
| Learning data validation | `make validate-learning` | Dataset schema, metadata, split overlap, and public-safe flags |
| Regression tests | `make test` | Public workflow unit tests continue to pass |
| Docs links | `make docs-check` | Local Markdown links in public docs resolve |
| Package build | `make package` | Allowlisted files are copied into the public zip |
| Package verification | `make verify` | Required zip entries exist and blocked paths/formats are excluded |
| Release readiness | `make release-check` | Generated reports, required files, zip contents, and overclaim scan pass |
| Zip audit | `make audit` | Built zip is scanned for blocked paths, raw formats, and basic credential patterns |
| Package smoke test | `make package-smoke` | Built zip is extracted into a temp directory and public commands rerun |
| Package inventory | `make inventory` | Built zip contents are listed by category |
| Upload manifest | `make upload-manifest` | Zip size, SHA256, report statuses, and reproduction commands are recorded |
| Export consistency | `make export-consistency` | Zip metadata is checked against audit, inventory, and upload manifest |

## Expected Reports

| Report | Location |
|---|---|
| Demo QA | `_demo_output/public-ai-safety/qa_report.md` |
| Learning report | `_demo_output/public-ai-safety/learning/learning_report.md` |
| Learning validation report | `_demo_output/public-ai-safety/learning/validation_report.md` |
| Docs link report | `_demo_output/docs_link_report.md` |
| Release readiness report | `_demo_output/release_readiness_report.md` |
| Package audit report | `_portfolio_export/package_audit.md` |
| Package smoke report | `_portfolio_export/package_smoke_report.md` |
| Package inventory | `_portfolio_export/package_inventory.md` |
| Upload manifest | `_portfolio_export/upload_manifest.md` |
| Export consistency report | `_portfolio_export/export_consistency_report.md` |

## Boundary

- Generated `_demo_output/` and `_portfolio_export/` reports are local verification artifacts, not source material.
- The public zip includes the scripts and documentation needed to reproduce the checks.
- The public zip excludes private project folders, raw document formats, generated JSONL/CSV datasets, and credentials.
- The package build sanitizes local absolute user paths in staged public text files before writing the zip.
- Passing verification does not imply web UI, API server, model training, HWP generation, deployment, or production SaaS readiness.
