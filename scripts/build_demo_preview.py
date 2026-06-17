#!/usr/bin/env python3
"""Build a public-safe SVG preview from the demo slide IR."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from textwrap import shorten


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLIDES = ROOT / "_demo_output" / "public-ai-safety" / "slides.json"
DEFAULT_OUTPUT = ROOT / "docs" / "assets" / "public-ai-safety-preview.svg"

CANVAS_W = 1280
CARD_W = 368
CARD_H = 207
GAP = 32
MARGIN_X = 48
MARGIN_Y = 72
TITLE_Y = 40
NAVY = "#0d3462"
NAVY_DEEP = "#0c2042"
ORANGE = "#f16a1f"
BG = "#f6f8fb"
CARD = "#ffffff"
BORDER = "#d8dfe9"
TEXT = "#37425a"
MUTED = "#69748a"


def load_slides(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("slides"), list):
        raise ValueError("slides payload must contain a slides array")
    return payload


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def fit(value: str, width: int) -> str:
    return shorten(" ".join(value.split()), width=width, placeholder="...")


def text(x: int, y: int, value: str, size: int = 16, color: str = TEXT, weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Apple SD Gothic Neo, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(value)}</text>'
    )


def rounded_rect(x: int, y: int, w: int, h: int, fill: str, stroke: str = "none", r: int = 8) -> str:
    stroke_attr = "" if stroke == "none" else f' stroke="{stroke}" stroke-width="1"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{stroke_attr}/>'


def slide_card(slide: dict, index: int, x: int, y: int) -> str:
    title = fit(str(slide.get("title", "Untitled")), 28)
    subtitle = fit(str(slide.get("subtitle", "")), 42)
    section = fit(str(slide.get("section", "")), 18)
    layout = str(slide.get("layout_type", "content"))
    bullets = [fit(str(item), 42) for item in slide.get("bullets", [])[:3]]

    parts = [
        rounded_rect(x, y, CARD_W, CARD_H, CARD, BORDER),
        rounded_rect(x, y, CARD_W, 36, NAVY, NAVY, 8),
        text(x + 16, y + 24, f"{index:02d}", 14, "#ffffff", 700),
        text(x + 58, y + 24, section or layout, 12, "#ffffff", 400),
        text(x + 18, y + 66, title, 18, NAVY_DEEP, 700),
        text(x + 18, y + 91, subtitle, 12, MUTED, 400),
    ]

    if layout == "workflow":
        step_w = 70
        for step_idx, label in enumerate(["PRD", "IR", "PPTX", "QA"]):
            sx = x + 18 + step_idx * 84
            parts.append(rounded_rect(sx, y + 122, step_w, 40, "#eef3f8", BORDER, 6))
            parts.append(text(sx + 14, y + 147, label, 11, NAVY_DEEP, 700))
            if step_idx < 3:
                parts.append(text(sx + 72, y + 147, ">", 14, ORANGE, 700))
    else:
        for bullet_idx, bullet in enumerate(bullets):
            by = y + 126 + bullet_idx * 22
            parts.append(f'<circle cx="{x + 24}" cy="{by - 4}" r="3" fill="{ORANGE}"/>')
            parts.append(text(x + 36, by, bullet, 11, TEXT, 400))

    return "\n".join(parts)


def build_svg(payload: dict) -> str:
    slides = payload["slides"]
    rows = (len(slides) + 2) // 3
    height = MARGIN_Y + rows * CARD_H + max(0, rows - 1) * GAP + 56
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{height}" viewBox="0 0 {CANVAS_W} {height}">',
        rounded_rect(0, 0, CANVAS_W, height, BG, BG, 0),
        text(MARGIN_X, TITLE_Y, "Proposal Builder Public Demo Preview", 24, NAVY_DEEP, 700),
        text(MARGIN_X, TITLE_Y + 26, "Generated from public sample slides.json. No private project files are used.", 13, MUTED, 400),
    ]
    for idx, slide in enumerate(slides, start=1):
        col = (idx - 1) % 3
        row = (idx - 1) // 3
        x = MARGIN_X + col * (CARD_W + GAP)
        y = MARGIN_Y + row * (CARD_H + GAP)
        parts.append(slide_card(slide, idx, x, y))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a public-safe SVG preview from slides.json.")
    parser.add_argument("--slides", type=Path, default=DEFAULT_SLIDES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        payload = load_slides(args.slides)
        svg = build_svg(payload)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"RESULT FAIL demo_preview: {exc}")
        return 1

    print(f"preview={args.output}")
    print(f"slides={len(payload['slides'])}")
    print("RESULT PASS demo_preview")
    return 0


if __name__ == "__main__":
    sys.exit(main())
