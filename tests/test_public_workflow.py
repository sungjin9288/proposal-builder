from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_CLI = ROOT / "scripts" / "proposal_builder_cli.py"
LEARNING_CLI = ROOT / "scripts" / "build_learning_dataset.py"
PREVIEW_CLI = ROOT / "scripts" / "build_demo_preview.py"
CASE_STUDY_CLI = ROOT / "scripts" / "check_case_study_status.py"
SAMPLE_PRD = ROOT / "examples" / "public-ai-safety" / "prd.md"


class PublicWorkflowTest(unittest.TestCase):
    def run_cmd(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def test_demo_builds_pptx_ir_and_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "demo"
            result = self.run_cmd([str(DEMO_CLI), "build", "--prd", str(SAMPLE_PRD), "--output", str(output)])
            self.assertEqual(result.returncode, 0, result.stdout)

            slides_json = output / "slides.json"
            pptx = output / "output.pptx"
            qa_report = output / "qa_report.md"
            self.assertTrue(slides_json.exists())
            self.assertTrue(pptx.exists())
            self.assertTrue(qa_report.exists())

            payload = json.loads(slides_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["project_id"], "public-ai-safety-demo")
            self.assertEqual(len(payload["slides"]), 5)
            self.assertIn("Status: `PASS`", qa_report.read_text(encoding="utf-8"))

    def test_learning_dataset_splits_from_demo_ir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            demo_output = Path(tmp) / "demo"
            learning_output = Path(tmp) / "learning"

            demo = self.run_cmd([str(DEMO_CLI), "build", "--prd", str(SAMPLE_PRD), "--output", str(demo_output)])
            self.assertEqual(demo.returncode, 0, demo.stdout)

            learn = self.run_cmd([
                str(LEARNING_CLI),
                "--slides",
                str(demo_output / "slides.json"),
                "--output",
                str(learning_output),
            ])
            self.assertEqual(learn.returncode, 0, learn.stdout)

            dataset = learning_output / "dataset.jsonl"
            train = learning_output / "train.jsonl"
            validation = learning_output / "validation.jsonl"
            report = learning_output / "learning_report.md"
            manifest = learning_output / "dataset_manifest.json"

            self.assertEqual(len(dataset.read_text(encoding="utf-8").splitlines()), 5)
            self.assertEqual(len(train.read_text(encoding="utf-8").splitlines()), 4)
            self.assertEqual(len(validation.read_text(encoding="utf-8").splitlines()), 1)
            self.assertIn("Status: `PASS`", report.read_text(encoding="utf-8"))

            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertFalse(manifest_payload["model_training_executed"])
            self.assertTrue(manifest_payload["public_safe"])

    def test_demo_preview_builds_public_svg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            demo_output = Path(tmp) / "demo"
            preview = Path(tmp) / "preview.svg"

            demo = self.run_cmd([str(DEMO_CLI), "build", "--prd", str(SAMPLE_PRD), "--output", str(demo_output)])
            self.assertEqual(demo.returncode, 0, demo.stdout)

            result = self.run_cmd([
                str(PREVIEW_CLI),
                "--slides",
                str(demo_output / "slides.json"),
                "--output",
                str(preview),
            ])
            self.assertEqual(result.returncode, 0, result.stdout)
            content = preview.read_text(encoding="utf-8")
            self.assertIn("<svg", content)
            self.assertIn("Proposal Builder Public Demo Preview", content)
            self.assertIn("No private project files are used", content)

    def test_case_study_status_validates_merged_evidence(self) -> None:
        result = self.run_cmd([str(CASE_STUDY_CLI)])
        self.assertEqual(result.returncode, 0, result.stdout)

        report = ROOT / "_demo_output" / "case_study_status_report.md"
        content = report.read_text(encoding="utf-8")
        self.assertIn("Status: `PASS`", content)
        self.assertIn("Output reports preserve non-final and no-training boundaries", content)


if __name__ == "__main__":
    unittest.main()
