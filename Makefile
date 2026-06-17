.PHONY: audit case-study check demo docs-check export-consistency final-check inventory learn package package-smoke preview release-check test upload-manifest validate-learning verify

PYTHON ?= python3

demo:
	$(PYTHON) scripts/proposal_builder_cli.py demo

learn: demo
	$(PYTHON) scripts/build_learning_dataset.py --slides _demo_output/public-ai-safety/slides.json --output _demo_output/public-ai-safety/learning

validate-learning: learn
	$(PYTHON) scripts/validate_learning_dataset.py

preview: demo
	$(PYTHON) scripts/build_demo_preview.py

test:
	$(PYTHON) -m unittest discover -s tests

docs-check:
	$(PYTHON) scripts/check_docs_links.py

case-study:
	$(PYTHON) scripts/check_case_study_status.py

release-check: check
	$(PYTHON) scripts/check_release_readiness.py

audit: package
	$(PYTHON) scripts/audit_portfolio_package.py

package-smoke: audit
	$(PYTHON) scripts/smoke_portfolio_package.py

inventory: package
	$(PYTHON) scripts/write_package_inventory.py

upload-manifest: release-check package-smoke inventory
	$(PYTHON) scripts/write_upload_manifest.py

export-consistency: upload-manifest
	$(PYTHON) scripts/check_export_consistency.py

final-check: export-consistency

check: validate-learning preview test docs-check case-study package verify

package: preview
	$(PYTHON) scripts/build_portfolio_package.py

verify:
	$(PYTHON) scripts/build_portfolio_package.py --verify-only
