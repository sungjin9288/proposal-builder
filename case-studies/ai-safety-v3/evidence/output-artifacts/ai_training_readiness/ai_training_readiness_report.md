# AI Training Readiness Report

- Generated: `2026-06-09T14:10:12`
- AI root: `<case-study-workspace>/ai_training`
- Status: `PARTIAL_READY_TRAINING_BLOCKED`
- Training command allowed: `false`
- Current action: `DO_NOT_TRAIN_MODEL_YET`

## Summary

- ready_features: `1`
- blocked_features: `1`
- training_blocked_reason: `planning_documentation_insufficient_samples`

## planning_documentation

- Description: Government/public-sector planning documentation AI
- Status: `BLOCKED`

### Split Counts

| Split | Rows | Minimum |
|---|---:|---:|
| `canonical` | 1 | 20 |
| `hold` | 0 | 0 |
| `train` | 1 | 10 |
| `validation` | 0 | 3 |

### Blockers

- `validation_dataset_missing`
- `canonical_rows_below_min:1/20`
- `train_rows_below_min:1/10`
- `validation_rows_below_min:0/3`

### Warnings

- `job_diversity_low:1_unique_jobs`
- `planning_ai_needs_more_real_government_task_samples`

### Dataset Files

| Split | Rows | Valid | Jobs | Path |
|---|---:|---|---:|---|
| `canonical` | 1 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/planning_documentation/canonical/002_planning_documentation_seed.jsonl` |
| `train` | 1 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/planning_documentation/train/002_planning_documentation_sft_seed_messages.jsonl` |

## editable_ppt_conversion

- Description: Design-preserving editable PPT conversion evaluator AI
- Status: `READY_FOR_PACKAGE_DRY_RUN`

### Split Counts

| Split | Rows | Minimum |
|---|---:|---:|
| `canonical` | 283 | 100 |
| `hold` | 15 | 0 |
| `preference` | 200 | 50 |
| `train` | 199 | 100 |
| `validation` | 69 | 20 |

### Warnings

- `job_diversity_low:1_unique_jobs`
- `editable_evaluator_ready_for_dry_run_not_full_model_training`

### Dataset Files

| Split | Rows | Valid | Jobs | Path |
|---|---:|---|---:|---|
| `canonical` | 283 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/canonical/002_editable_ppt_conversion_canonical_dataset.jsonl` |
| `train` | 199 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/train/002_editable_ppt_conversion_train.jsonl` |
| `validation` | 69 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/validation/002_editable_ppt_conversion_validation.jsonl` |
| `hold` | 15 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/hold/002_editable_ppt_conversion_hold_review.jsonl` |
| `preference` | 200 | true | 1 | `<case-study-workspace>/ai_training/03_datasets/editable_ppt_conversion/preference/002_editable_ppt_conversion_preference_pairs.jsonl` |

## Next Action

- Do not train a model yet.
- Add real reviewed planning documentation samples until planning canonical/train/validation thresholds are met.
- Keep editable PPT conversion as evaluator dry-run data until more job diversity is collected.
