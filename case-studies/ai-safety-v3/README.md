# AI Safety V3 Case Study

This case study consolidates the public-safe evidence collected from `<case-study-workspace>` into the main `proposal-builder` portfolio root.

## Relationship To Proposal Builder

`proposal-builder` is the reusable local workflow for proposal document automation:

```text
RFP / source context
-> PRD / slide specification
-> PPTX / PDF generation
-> OCR, editability, and readiness QA
-> reviewer handoff
```

The AI Safety V3 work is a concrete application of that workflow to a public-sector pedestrian-safety proposal deck. It demonstrates:

- V3 proposal direction and slide specification management
- PPTX/PDF artifact inspection
- design-preserving PPT conversion input checks
- revision-log and final-fix readiness gates
- AI-training dataset readiness gates without claiming completed model training

## Included Evidence

- `docs/implementation-evidence.md`
- `docs/evidence-checklist.md`
- `docs/evidence-gallery.md`
- `evidence/evidence_manifest.md`
- `evidence/cli-logs/*.log`
- `evidence/output-artifacts/*.md`
- `evidence/output-artifacts/*.json`
- `evidence/architecture/*.md`

## Excluded By Design

- raw client or institution materials
- original PPTX/PDF files
- generated proposal decks
- `.env`, API keys, passwords, tokens, private keys
- source folders that may include internal project-specific material

## Current Status

- Project type: local CLI/agent/tool workflow evidence
- Verified: visual PPT input validation, PPTX editability inventory, revision-log validation, final-fix readiness gate
- Blocked/needs input: actual model training, final external submission readiness
- Not applicable: web UI screenshots, API responses

Use this case study as implementation evidence for the reusable `proposal-builder` workflow, not as a separate unrelated product.
