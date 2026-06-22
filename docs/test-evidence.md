# Test Evidence

## Command

```bash
make test
make docs-check
```

## Verified Result

```text
Ran 3 tests
OK
```

## Covered

- Public demo PRD builds into:
  - `slides.json`
  - `output.pptx`
  - `qa_report.md`
- Learning dataset export builds:
  - `dataset.jsonl`
  - `train.jsonl`
  - `validation.jsonl`
  - `learning_report.md`
  - `dataset_manifest.json`
- Learning dataset validation checks:
  - required top-level fields
  - required output fields
  - required metadata fields
  - train/validation non-overlap
  - split ids matching the full dataset
- Public SVG preview generation from demo `slides.json`
- Public documentation local Markdown link validation

## Assertions

- `slides.json` contains 5 slides.
- QA report status is `PASS`.
- Learning dataset has 5 rows.
- Train split has 4 rows.
- Validation split has 1 row.
- `model_training_executed` is `false`.
- `public_safe` is `true`.
- Preview SVG contains the public demo title and private-data boundary note.
- Docs link report status is `PASS`.

## Boundary

- Tests use temporary directories.
- Tests use only `examples/public-ai-safety/prd.md`.
- Tests do not access `projects/`, `archive/`, client notes, raw PPT/PDF files, or external APIs.
