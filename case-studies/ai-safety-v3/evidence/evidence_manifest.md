# Evidence Manifest

## Project Classification

- Project type: CLI/agent/tool-oriented local automation workspace
- Domain: public-sector AI safety-service proposal deck and design-preserving PPT workflow
- Not classified as: web app, API service, deployed SaaS, production ML system
- Career framing note: no direct management-evaluation application feature was found, so this evidence package does not frame the project as a management-evaluation product.

## Evidence Collection Date

- Date: 2026-06-09
- Workspace: `<case-study-workspace>`

## CLI Logs

| File | Command | Result |
|---|---|---|
| `evidence/cli-logs/validate_ai_training_workspace.log` | `python3 scripts/validate_ai_training_workspace.py --report-md evidence/output-artifacts/ai_training_workspace_validation.md --report-json evidence/output-artifacts/ai_training_workspace_validation.json` | `NEEDS_INPUT`, exit code 2 |
| `evidence/cli-logs/check_ai_training_readiness.log` | `python3 scripts/check_ai_training_readiness.py --output-dir evidence/output-artifacts/ai_training_readiness` | `PARTIAL_READY_TRAINING_BLOCKED`, exit code 2 |
| `evidence/cli-logs/check_visual_ppt_conversion_inputs.log` | `python3 scripts/check_visual_ppt_conversion_inputs.py --input-dir input/visual_ppt_conversion --report evidence/output-artifacts/visual_ppt_conversion_input_check.md --skip-export-tool` | `PASS`, exit code 0 |
| `evidence/cli-logs/analyze_v3_proposal_editability.log` | `python3 scripts/analyze_pptx_editability_inventory.py --pptx output/v3_proposal.pptx --inventory evidence/output-artifacts/v3_proposal_editability_inventory.json --report evidence/output-artifacts/v3_proposal_editability_report.md` | `PASS`, exit code 0 |
| `evidence/cli-logs/validate_revision_log.log` | `python3 scripts/validate_revision_log.py --revision-log output/revision_log.md` | `PASS`, exit code 0 |
| `evidence/cli-logs/check_final_fix_readiness.log` | `python3 scripts/check_final_fix_readiness.py` | `WAITING_FOR_REVIEW_INPUT`, exit code 0 |

## Output Artifacts

| File | Description |
|---|---|
| `evidence/output-artifacts/ai_training_workspace_validation.md` | AI training workspace structure, JSONL, and sample readiness report |
| `evidence/output-artifacts/ai_training_workspace_validation.json` | Machine-readable AI training workspace validation report |
| `evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.md` | Training readiness report |
| `evidence/output-artifacts/ai_training_readiness/ai_training_readiness_report.json` | Machine-readable training readiness report |
| `evidence/output-artifacts/ai_training_readiness/ai_training_readiness_runbook.md` | Generated runbook for next actions |
| `evidence/output-artifacts/visual_ppt_conversion_input_check.md` | Visual PPT conversion input status report |
| `evidence/output-artifacts/v3_proposal_editability_report.md` | PPTX editability inventory report |
| `evidence/output-artifacts/v3_proposal_editability_inventory.json` | Machine-readable PPTX editability inventory |

## Architecture Evidence

| File | Description |
|---|---|
| `evidence/architecture/current-architecture.md` | Mermaid flowchart of current local workflow architecture |
| `evidence/architecture/cli-sequence.md` | Mermaid sequence diagram for evidence-producing CLI checks |

## Exclusions

- No `.env`, API keys, passwords, tokens, private keys, `.git`, dependency folders, raw source-code package, large PPT/PDF files, or customer/internal raw materials were intentionally added to this evidence package.
- Web screenshots and API responses are marked not applicable because no web/API application was confirmed.
