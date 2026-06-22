# Portfolio Merge Map

## Decision

Use `<proposal-builder-root>` as the unified portfolio root.

The previous `<case-study-workspace>` folder is treated as a concrete case-study/evidence workspace for the reusable Proposal Builder workflow, not as a separate portfolio project.

## Why This Merge Is Non-Destructive

- No source project folders were moved or deleted.
- No raw PPTX/PDF files were copied into the public case-study folder.
- No client notes, company profile files, `projects/`, `archive/`, or `vendor/` contents were copied.
- Only sanitized Markdown, JSON reports, CLI logs, and architecture diagrams were copied.

## Unified Structure

```text
proposal-builder/
├── README.md
├── CLAUDE.md
├── .claude/skills/
├── templates/
├── docs/
│   └── portfolio-merge-map.md
└── case-studies/
    └── ai-safety-v3/
        ├── README.md
        ├── docs/
        └── evidence/
```

## Source Mapping

| Original root | Unified location | Purpose |
|---|---|---|
| `<proposal-builder-root>` | root | reusable proposal automation framework |
| `<case-study-workspace>/docs` | `case-studies/ai-safety-v3/docs` | implementation and portfolio evidence docs |
| `<case-study-workspace>/evidence` | `case-studies/ai-safety-v3/evidence` | CLI logs, generated reports, architecture diagrams |

## Portfolio Interpretation

Safe explanation:

> Proposal Builder is a local workflow framework for turning proposal/RFP work into structured PRD, slide IR, generated PPT/PDF outputs, and QA gates. The AI Safety V3 case study shows the framework applied to a public-sector pedestrian-safety proposal workflow, with implementation evidence collected through local CLI validation and artifact inspection.

Do not claim:

- deployed SaaS
- public API service
- completed AI model training
- final external submission approval
- raw client-material disclosure

## Remaining Work

- Confirm which scripts and skills were directly authored by the portfolio owner.
- Add safe screenshots only after confirming they contain no internal/client material.
- Add a GitHub URL only after the public repository is created and checked.
