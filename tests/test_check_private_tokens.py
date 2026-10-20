from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_private_tokens.py"

spec = importlib.util.spec_from_file_location("check_private_tokens", SCRIPT)
check_private_tokens = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(check_private_tokens)


class CheckPrivateTokensTest(unittest.TestCase):
    def test_finds_blocked_token_in_text_and_path_case_insensitively(self) -> None:
        blocked = frozenset({check_private_tokens.token_hash("sample-secret")})
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.md").write_text("ok line\nsee projects/SAMPLE-Secret/assets\n", encoding="utf-8")
            (root / "sample-secret.md").write_text("clean\n", encoding="utf-8")
            (root / "clean.md").write_text("sample secret secret-sample\n", encoding="utf-8")
            paths = [root / "notes.md", root / "sample-secret.md", root / "clean.md"]

            issues = check_private_tokens.find_blocked(paths, root, blocked)

        self.assertEqual(len(issues), 2)
        self.assertTrue(issues[0].startswith("notes.md:2: blocked token"))
        self.assertTrue(issues[1].startswith("sample-secret.md: blocked token in path"))
        # The report names only a hash prefix, never the blocked word itself.
        self.assertNotIn("secret", issues[0].casefold())

    def test_repository_has_no_blocked_tokens(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=ROOT, check=False, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
