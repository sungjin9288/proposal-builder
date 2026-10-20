#!/usr/bin/env python3
"""Fail when a tracked file contains a blocked private identifier.

Private client codes and client tone labels must never reach this public
repository. The blocked tokens are stored only as SHA-256 hashes of their
casefolded form, so this file does not republish them. A hash of a short word
can still be brute-forced; the goal is to keep the tokens out of plain text
and grep results, not to make them secret.

To block a new token, add `sha256(token.casefold())` to BLOCKED_SHA256.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BLOCKED_SHA256 = frozenset(
    {
        # internal client project code (removed 2026-10-20)
        "a3fa6b7d218ebb2f6c55d05cc10aeca653e538af74ec4d61be9966a2db10cde0",
        # client tone label (removed 2026-10-20)
        "886307ef9955bd7bf9bdf0ba461a56fbefc590e381b2aefc3d84c42195c9545a",
    }
)

WORD_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z_-]*")
# Gitignored working dirs that may hold client material; skipped when no git index exists.
LOCAL_ONLY_DIRS = {".git", "projects", "archive", "_demo_output", "_portfolio_export", "__pycache__", "ppt-master"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".pptx", ".docx", ".hwp", ".hwpx", ".zip", ".ttf", ".otf", ".woff", ".woff2"}


def token_hash(word: str) -> str:
    return hashlib.sha256(word.casefold().encode("utf-8")).hexdigest()


def tracked_files(root: Path) -> list[Path]:
    """Return git-tracked files, or every file outside local-only dirs.

    The portfolio package has no .git directory, so the fallback lets the
    same check run inside an extracted package.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
        )
    except (OSError, subprocess.CalledProcessError):
        return sorted(
            path
            for path in root.rglob("*")
            if path.is_file() and not (set(path.relative_to(root).parts) & LOCAL_ONLY_DIRS)
        )
    names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
    return [root / name for name in names]


def find_blocked(paths: list[Path], root: Path, blocked: frozenset[str]) -> list[str]:
    issues: list[str] = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        for word in WORD_RE.findall(rel):
            if token_hash(word) in blocked:
                issues.append(f"{rel}: blocked token in path (sha256 {token_hash(word)[:12]})")
        if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for word in WORD_RE.findall(line):
                if token_hash(word) in blocked:
                    issues.append(f"{rel}:{line_no}: blocked token (sha256 {token_hash(word)[:12]})")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()
    paths = tracked_files(ROOT)
    issues = find_blocked(paths, ROOT, BLOCKED_SHA256)
    if issues:
        print("Private token check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Private token check passed: {len(paths)} tracked files, {len(BLOCKED_SHA256)} blocked tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
