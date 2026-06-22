# Evidence Gallery

## CLI Logs

| Evidence | Link | What it proves |
|---|---|---|
| AI training workspace validation log | `../evidence/cli-logs/validate_ai_training_workspace.log` | Workspace validation command runs and records `NEEDS_INPUT` honestly |
| AI training readiness log | `../evidence/cli-logs/check_ai_training_readiness.log` | Training readiness gate runs and blocks training |
| Visual PPT conversion input log | `../evidence/cli-logs/check_visual_ppt_conversion_inputs.log` | Conversion input check passes |
| PPTX editability analysis log | `../evidence/cli-logs/analyze_v3_proposal_editability.log` | PPTX inventory command runs successfully |
| Revision log validation log | `../evidence/cli-logs/validate_revision_log.log` | Revision log validation passes |
| Final fix readiness log | `../evidence/cli-logs/check_final_fix_readiness.log` | Final package remains review-waiting, not external-final |

## Generated Reports

| Evidence | Link | What it proves |
|---|---|---|
| AI training workspace validation | `../evidence/output-artifacts/ai_training_workspace_validation.md` | JSONL counts, sample packet status, training blocked state |
| AI training readiness report | `../evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.md` | Editable PPT conversion dry-run readiness and planning documentation blockers |
| Visual PPT conversion input check | `../evidence/output-artifacts/visual_ppt_conversion_input_check.md` | Source PDF/reference PPTX metadata and readiness |
| V3 proposal editability report | `../evidence/output-artifacts/v3_proposal_editability_report.md` | 31-slide PPTX structure and editable-shape inventory |

## Architecture

| Evidence | Link | What it shows |
|---|---|---|
| Current architecture | `../evidence/architecture/current-architecture.md` | File-based local automation flow |
| CLI sequence | `../evidence/architecture/cli-sequence.md` | Command execution and evidence capture flow |

## Not Applicable Evidence

| Area | Link | Reason |
|---|---|---|
| Screenshots | `../evidence/screenshots/not_applicable.md` | No confirmed web app |
| API responses | `../evidence/api-responses/not_applicable.md` | No confirmed API server |
