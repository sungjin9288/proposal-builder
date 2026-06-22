# AI Training Workspace Validation Report

- Generated: `2026-06-09T14:10:12`
- AI root: `<case-study-workspace>/ai_training`
- Status: `NEEDS_INPUT`
- Training command allowed: `false`
- Current action: `DO_NOT_TRAIN_MODEL_YET`

## Summary

- jsonl_file_count: `7`
- jsonl_total_rows: `768`
- sample_count: `5`
- ready_samples: `0`
- needs_input_samples: `5`
- incomplete_samples: `0`
- broken_symlink_count: `0`

## JSONL Datasets

| Rows | Valid | Path |
|---:|---|---|
| 283 | true | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/canonical/002_editable_ppt_conversion_canonical_dataset.jsonl` |
| 15 | true | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/hold/002_editable_ppt_conversion_hold_review.jsonl` |
| 200 | true | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/preference/002_editable_ppt_conversion_preference_pairs.jsonl` |
| 199 | true | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/train/002_editable_ppt_conversion_train.jsonl` |
| 69 | true | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/validation/002_editable_ppt_conversion_validation.jsonl` |
| 1 | true | `<case-study-workspace>/ai_training/03_datasets/planning_documentation/canonical/002_planning_documentation_seed.jsonl` |
| 1 | true | `<case-study-workspace>/ai_training/03_datasets/planning_documentation/train/002_planning_documentation_sft_seed_messages.jsonl` |

## Sample Packets

| Feature | State | Sample | Status | Source files | TODO | Decision |
|---|---|---|---|---:|---:|---|
| planning_documentation | pending | `001_government_task_sample` | `NEEDS_INPUT` | 0 | 51 | `missing` |
| planning_documentation | pending | `002_next_government_task_sample` | `NEEDS_INPUT` | 0 | 50 | `missing` |
| editable_ppt_conversion | pending | `001_editable_ppt_conversion_sample` | `NEEDS_INPUT` | 0 | 10 | `missing` |
| editable_ppt_conversion | pending | `003_next_editable_ppt_job` | `NEEDS_INPUT` | 1 | 10 | `missing` |
| editable_ppt_conversion | pending | `004_next_editable_ppt_job` | `NEEDS_INPUT` | 1 | 10 | `missing` |

## Next Action

- Keep training blocked until real source files, reviewed outputs, and label decisions are complete.
- For planning samples, run `scripts/build_planning_training_row_from_sample.py` after review is complete.
