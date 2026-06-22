# CLI Evidence Sequence

```mermaid
sequenceDiagram
  participant User
  participant CLI as Python CLI scripts
  participant Input as input/projects/output files
  participant Evidence as evidence folder
  participant Gate as readiness and review gates

  User->>CLI: run validation/check commands
  CLI->>Input: inspect PPTX/PDF/spec/dataset files
  CLI->>Evidence: write logs and reports
  CLI->>Gate: classify pass, needs-input, blocked
  Gate-->>Evidence: record status and next action
  Evidence-->>User: implementation evidence package
```

## Commands Captured

- `validate_ai_training_workspace.py`
- `check_ai_training_readiness.py`
- `check_visual_ppt_conversion_inputs.py`
- `analyze_pptx_editability_inventory.py`
- `validate_revision_log.py`
- `check_final_fix_readiness.py`
