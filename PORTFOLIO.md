# Proposal Builder Portfolio Summary

## One-line Summary

Proposal Builder is a local automation framework that turns public-sector proposal inputs into structured slide IR, PPTX output, QA reports, and learning-ready JSONL datasets without exposing private project material.

## Problem

Proposal and consulting documents often repeat the same structure work: reading requirements, drafting a PRD, shaping slide content, checking forbidden wording, and preparing review artifacts. Manual work makes quality depend on individual experience and makes repeat verification difficult.

## Implemented Scope

| Area | Implemented Evidence | Status |
|---|---|---|
| Public demo workflow | `examples/public-ai-safety/prd.md` to `slides.json`, `output.pptx`, and `qa_report.md` | Verified |
| PPTX generation | Minimal OpenXML PPTX writer in `scripts/proposal_builder_cli.py` | Verified |
| QA gate | slide count, shape count, generated file checks, forbidden token checks | Verified |
| Learning data preparation | slide-level `dataset.jsonl`, `train.jsonl`, `validation.jsonl`, manifest, report | Verified |
| Learning data validation | schema checks, split consistency, public-safe metadata checks | Verified |
| Portfolio packaging | public-safe zip with allowlist and exclusion checks | Verified |
| Release readiness | generated outputs, zip contents, overclaim scan, required file checks | Verified |
| Case study evidence | sanitized AI safety proposal evidence under `case-studies/ai-safety-v3/` | Verified as documentation evidence |

## Not Implemented Here

| Area | Boundary |
|---|---|
| Web UI | Planned for the separate DecisionDoc project |
| API server | Not included in this repository |
| Model training or fine-tuning | Not executed; this repository prepares and validates JSONL only |
| HWP generation | Placeholder scope because real HWP generation depends on a Windows/Hancom worker |
| Production deployment | Not included |
| Private client deliverables | Excluded from public package |

## Verification Commands

```bash
make demo
make learn
make validate-learning
make test
make docs-check
make package
make verify
make release-check
make package-smoke
make inventory
make upload-manifest
make export-consistency
make final-check
```

## Public Package

```text
_portfolio_export/proposal_builder_unified_portfolio_pack.zip
```

The package includes reusable framework files, public sample input, sanitized docs, tests, scripts, and case-study evidence. It excludes `projects/`, `archive/`, `_demo_output/`, raw PPTX/PDF/HWP files, credentials, dependency caches, and private client material.

## Portfolio Narrative

This project demonstrates a practical document automation workflow rather than a finished SaaS product. The useful engineering signal is the separation between generated artifacts, verification reports, and public-safe packaging. The current implementation proves the functional core up to learning data preparation; web experience and downstream model work are intentionally delegated to DecisionDoc.
