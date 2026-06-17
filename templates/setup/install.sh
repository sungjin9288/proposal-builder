#!/usr/bin/env bash
# proposal-builder dependencies installer
# Run once after clone. Re-run safely (idempotent).

set -e
echo "==> proposal-builder setup"

# 1. macOS system deps
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "[1/3] checking brew deps..."
  for pkg in cairo pkg-config tesseract tesseract-lang; do
    if ! brew list $pkg &>/dev/null; then
      echo "    installing $pkg..."
      brew install $pkg || true
    fi
  done
fi

# 2. Python deps (proposal-builder + vendored ppt-master)
echo "[2/3] installing Python deps..."
pip install --user \
  python-pptx \
  Pillow \
  PyMuPDF \
  mammoth \
  markdownify \
  beautifulsoup4 \
  requests \
  openpyxl \
  numpy \
  lxml \
  PyYAML

# Optional: cairosvg + svglib (PNG fallback for legacy Office). Skip if build fails.
pip install --user cairosvg svglib reportlab 2>/dev/null || \
  echo "    [skip] cairosvg/svglib install failed (Office 2019+ native-only mode still works)"

# 3. verify
echo "[3/3] verify..."
python3 -c "from pptx import Presentation; from PIL import Image; import fitz; print('  [ok] python core deps')"
which tesseract >/dev/null && echo "  [ok] tesseract"
[[ -d vendor/ppt-master/skills/ppt-master/scripts ]] && echo "  [ok] vendor/ppt-master"

echo "==> done."
