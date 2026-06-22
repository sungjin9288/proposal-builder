# Current Architecture

```mermaid
flowchart TD
  U["User / reviewer"] --> I["input/ PPTX and PDF files"]
  U --> S["projects/ai_safety_v3 specs and policies"]
  I --> C["scripts/ CLI automation"]
  S --> C
  C --> O["output/ generated PPT, PDF, QA reports"]
  C --> J["jobs/visual_ppt_conversion job packages"]
  C --> A["ai_training datasets and readiness gates"]
  C --> E["evidence logs and artifacts"]
  A --> G["training blocked or dry-run gate"]
  O --> R["reviewer decision / evidence follow-up"]
  J --> R
  G --> R
```

## Notes

- This is a local file-based automation workspace, not a deployed web service.
- No API server, frontend app, authentication layer, or production database was found.
- Model training is intentionally blocked by readiness gates.
