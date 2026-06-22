# Third-Party And Source Notices

## Public Package Boundary

The public portfolio zip is built from an allowlist. It includes reusable framework files, sanitized case-study evidence, public sample input, tests, scripts, templates, and documentation.

It does not include private project folders, raw source documents, generated demo datasets, credentials, dependency caches, or vendored third-party source trees.

## Third-Party Runtime Dependencies

The repository lists Python dependencies in `requirements.txt`:

```text
python-pptx
Pillow
PyMuPDF
mammoth
markdownify
beautifulsoup4
requests
openpyxl
numpy
lxml
PyYAML
reportlab
```

These packages are not vendored into the portfolio zip. Reviewers can install them in their local Python environment when needed.

## Vendor Directory

The local workspace may use `vendor/ppt-master/` as an external integration reference. The public portfolio package does not include that source tree. It includes only `vendor/README.md` so reviewers can see the intended integration boundary.

Any future distribution that includes third-party source code should preserve the upstream license files and notices from that project.

## Template And Asset Notes

- `templates/decorations/` contains reusable visual assets and metadata files used by the proposal template workflow.
- `docs/assets/public-ai-safety-preview.svg` is generated from the public sample slide IR.
- Public demo output under `_demo_output/` is generated locally and excluded from the zip.

## Source Material Exclusions

The portfolio zip intentionally excludes:

- `projects/`
- `archive/`
- raw `*.pptx`, `*.pdf`, `*.hwp`, `*.hwpx`
- generated `*.jsonl`, `*.csv`
- `.env`, keys, tokens, certificates, and private credentials
- `vendor/ppt-master/`
- dependency/cache folders

## Local Path Sanitization

During package build, public text files copied into the staging directory are sanitized so local absolute paths such as macOS home-directory paths are replaced with placeholders like `<proposal-builder-root>`, `<case-study-workspace>`, or `<local-home>`.

The package audit fails if local macOS home-directory paths remain in text entries inside the generated zip.

## Claim Boundary

This package does not claim ownership of third-party libraries or upstream tools. It demonstrates local workflow integration, public-safe packaging, and verification around the Proposal Builder framework.
