#!/usr/bin/env python3
"""Public-safe Proposal Builder demo CLI.

The demo uses only Python's standard library so portfolio reviewers can run it
before installing the heavier document-processing stack. It creates:

- slides.json: structured slide IR
- output.pptx: minimal editable PPTX built with OpenXML
- qa_report.md: file, slide-count, text-shape, and forbidden-token checks
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRD = ROOT / "examples" / "public-ai-safety" / "prd.md"
DEFAULT_OUTPUT = ROOT / "_demo_output" / "public-ai-safety"
FORBIDDEN_TOKENS = ROOT / "templates" / "qa" / "forbidden_tokens.txt"

SLIDE_W = 12192000
SLIDE_H = 6858000
NAVY = "0D3462"
NAVY_DEEP = "0C2042"
ORANGE = "F16A1F"
WHITE = "FFFFFF"
GRAY_BG = "F6F8FB"
GRAY_TEXT = "37425A"
BORDER = "D8DFE9"


@dataclass
class SlideSpec:
    id: str
    title: str
    subtitle: str
    bullets: list[str]
    layout_type: str
    section: str


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def emu(inches: float) -> int:
    return int(inches * 914400)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        return {}, text
    raw = match.group(1)
    if yaml is not None:
        return yaml.safe_load(raw) or {}, match.group(2)
    return parse_minimal_frontmatter(raw), match.group(2)


def parse_minimal_frontmatter(raw: str) -> dict[str, Any]:
    def scalar(key: str, default: str = "") -> str:
        found = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw, re.M)
        return found.group(1).strip() if found else default

    def list_after(key: str) -> list[str]:
        found = re.search(rf"^\s*{re.escape(key)}:\s*\n((?:\s+- .+\n?)+)", raw, re.M)
        if not found:
            return []
        return [line.split("-", 1)[1].strip().strip("\"'") for line in found.group(1).splitlines() if "-" in line]

    return {
        "rfp": {"id": scalar("id", "public-demo"), "client": scalar("client", "확인 필요")},
        "strategy": {"win_themes": list_after("win_themes"), "risks": list_after("risks")},
    }


def section_body(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)", re.M | re.S)
    match = pattern.search(markdown)
    return " ".join(match.group(1).split()) if match else ""


def split_bullets(text: str, fallback: list[str], limit: int = 4) -> list[str]:
    if not text:
        return fallback[:limit]
    parts = re.split(r"(?<=다\.)\s+", text)
    bullets = [part.strip(" -") for part in parts if len(part.strip()) >= 8]
    return (bullets or fallback)[:limit]


def build_ir(prd_path: Path, output_dir: Path) -> list[SlideSpec]:
    meta, body = parse_frontmatter(prd_path.read_text(encoding="utf-8"))
    rfp = meta.get("rfp", {})
    strategy = meta.get("strategy", {})
    first_heading = next((line.lstrip("# ").strip() for line in body.splitlines() if line.startswith("# ")), "Proposal Builder Demo")

    slides = [
        SlideSpec("slide-01", first_heading, "PRD 기반 슬라이드 IR 및 QA 자동화 데모", [
            f"프로젝트 ID: {rfp.get('id', '확인 필요')}",
            f"대상: {rfp.get('client', '확인 필요')}",
            "민감자료 없이 실행 가능한 공개 샘플",
        ], "cover", "overview"),
        SlideSpec("slide-02", "문제정의", "반복 문서 작업을 검토 가능한 구조로 전환",
                  split_bullets(section_body(body, "Problem"), ["반복 작성 과정에서 품질 편차가 발생합니다.", "검토 누락을 줄이기 위해 구조화된 중간 산출물이 필요합니다."]), "card_grid", "problem"),
        SlideSpec("slide-03", "자동화 흐름", "PRD에서 IR, PPTX, QA 리포트까지 연결",
                  split_bullets(section_body(body, "Workflow"), ["PRD를 slides.json으로 변환합니다.", "PPTX를 생성합니다.", "QA 리포트로 검토 상태를 남깁니다."]), "workflow", "workflow"),
        SlideSpec("slide-04", "검증 게이트", "완료와 보완 필요를 분리",
                  split_bullets(section_body(body, "Verification"), ["금지어 토큰을 검사합니다.", "생성 파일 존재 여부를 확인합니다.", "검토 제한사항을 남깁니다."]), "qa", "verification"),
        SlideSpec("slide-05", "포트폴리오 활용 포인트", "실제 구현된 범위만 증거로 설명",
                  (strategy.get("win_themes") or []) + ["웹 UI, API, 모델 학습 완료는 이 데모 범위가 아닙니다."], "summary", "summary"),
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "project_id": rfp.get("id", "public-demo"),
        "generated_at": now(),
        "source_prd": str(prd_path),
        "slides": [asdict(slide) for slide in slides],
    }
    (output_dir / "slides.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return slides


def text_run(text: str, size: int, color: str, bold: bool = False) -> str:
    bold_xml = ' b="1"' if bold else ""
    return (
        f'<a:r><a:rPr lang="ko-KR" sz="{size * 100}"{bold_xml}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'</a:rPr><a:t>{html.escape(text)}</a:t></a:r>'
    )


def shape_xml(shape_id: int, x: float, y: float, w: float, h: float, text: str = "", size: int = 12,
              color: str = GRAY_TEXT, bold: bool = False, fill: str | None = None, line: str | None = None) -> str:
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    line_xml = f'<a:ln w="6350"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
    tx_xml = ""
    if text:
        tx_xml = (
            "<p:txBody><a:bodyPr wrap=\"square\"/><a:lstStyle/>"
            f"<a:p>{text_run(text, size, color, bold)}</a:p></p:txBody>"
        )
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="Shape {shape_id}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        {fill_xml}{line_xml}
      </p:spPr>
      {tx_xml}
    </p:sp>
    """


def slide_xml(spec: SlideSpec, index: int) -> str:
    shapes: list[str] = []
    sid = 2
    shapes.append(shape_xml(sid, 0, 0, 13.333, 7.5, fill=GRAY_BG)); sid += 1

    if index == 1:
        shapes.append(shape_xml(sid, 7.45, 0, 5.88, 7.5, fill=NAVY)); sid += 1
        shapes.append(shape_xml(sid, 0.75, 1.25, 6.0, 0.58, spec.title, 28, NAVY_DEEP, True)); sid += 1
        shapes.append(shape_xml(sid, 0.78, 2.0, 5.8, 0.34, spec.subtitle, 13, GRAY_TEXT)); sid += 1
        for i, bullet in enumerate(spec.bullets):
            shapes.append(shape_xml(sid, 0.8, 3.0 + i * 0.72, 5.35, 0.52, fill=WHITE, line=BORDER)); sid += 1
            shapes.append(shape_xml(sid, 0.98, 3.13 + i * 0.72, 4.95, 0.2, bullet, 9, GRAY_TEXT)); sid += 1
    else:
        shapes.append(shape_xml(sid, 0, 0, 13.333, 0.86, fill=NAVY)); sid += 1
        shapes.append(shape_xml(sid, 0.48, 0.16, 7.2, 0.32, spec.title, 18, WHITE, True)); sid += 1
        shapes.append(shape_xml(sid, 0.50, 0.51, 8.2, 0.2, spec.subtitle, 8, WHITE)); sid += 1
        if spec.layout_type == "workflow":
            labels = ["PRD", "slides.json", "PPTX", "QA"]
            for i, label in enumerate(labels):
                x = 0.78 + i * 3.05
                shapes.append(shape_xml(sid, x, 1.72, 2.42, 1.28, fill=WHITE, line=BORDER)); sid += 1
                shapes.append(shape_xml(sid, x + 0.18, 1.90, 1.8, 0.22, label, 12, NAVY_DEEP, True)); sid += 1
                body = spec.bullets[min(i, len(spec.bullets) - 1)]
                shapes.append(shape_xml(sid, x + 0.18, 2.25, 2.0, 0.46, body, 8, GRAY_TEXT)); sid += 1
                if i < len(labels) - 1:
                    shapes.append(shape_xml(sid, 3.05 + i * 3.05, 2.18, 0.36, 0.2, "->", 16, ORANGE, True)); sid += 1
        else:
            for i, bullet in enumerate(spec.bullets[:4]):
                x = 0.75 + (i % 2) * 6.05
                y = 1.38 + (i // 2) * 2.25
                shapes.append(shape_xml(sid, x, y, 5.58, 1.65, fill=WHITE, line=BORDER)); sid += 1
                shapes.append(shape_xml(sid, x + 0.2, y + 0.18, 4.9, 0.22, f"{i + 1}. 핵심", 11, NAVY_DEEP, True)); sid += 1
                shapes.append(shape_xml(sid, x + 0.2, y + 0.58, 5.05, 0.58, bullet, 9, GRAY_TEXT)); sid += 1
        shapes.append(shape_xml(sid, 11.9, 7.02, 0.72, 0.18, f"{index:02d}", 8, NAVY, True)); sid += 1

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def static_parts(slide_count: int) -> dict[str, str]:
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    slide_ids = "\n".join(f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1))
    rels = "\n".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, slide_count + 1)
    )
    rels += f'\n<Relationship Id="rId{slide_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'

    return {
        "[Content_Types].xml": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slide_overrides}
</Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>""",
        "ppt/presentation.xml": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{slide_count + 1}"/></p:sldMasterIdLst>
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>""",
        "ppt/_rels/presentation.xml.rels": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>""",
        "ppt/slideMasters/slideMaster1.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>""",
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>""",
        "ppt/slideLayouts/slideLayout1.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
</p:sldLayout>""",
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>""",
        "ppt/theme/theme1.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Proposal Builder">
  <a:themeElements><a:clrScheme name="Office"><a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="0D3462"/></a:dk2><a:lt2><a:srgbClr val="F6F8FB"/></a:lt2><a:accent1><a:srgbClr val="F16A1F"/></a:accent1><a:accent2><a:srgbClr val="0D3462"/></a:accent2><a:accent3><a:srgbClr val="37425A"/></a:accent3><a:accent4><a:srgbClr val="D8DFE9"/></a:accent4><a:accent5><a:srgbClr val="FFFFFF"/></a:accent5><a:accent6><a:srgbClr val="0C2042"/></a:accent6><a:hlink><a:srgbClr val="0563C1"/></a:hlink><a:folHlink><a:srgbClr val="954F72"/></a:folHlink></a:clrScheme><a:fontScheme name="Office"><a:majorFont><a:latin typeface="Arial"/><a:ea typeface="Malgun Gothic"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:ea typeface="Malgun Gothic"/></a:minorFont></a:fontScheme><a:fmtScheme name="Office"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements>
</a:theme>""",
    }


def build_pptx(slides: list[SlideSpec], output_dir: Path) -> Path:
    output = output_dir / "output.pptx"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, xml in static_parts(len(slides)).items():
            zf.writestr(name, xml)
        for index, spec in enumerate(slides, start=1):
            zf.writestr(f"ppt/slides/slide{index}.xml", slide_xml(spec, index))
            zf.writestr(
                f"ppt/slides/_rels/slide{index}.xml.rels",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>""",
            )
    return output


def load_forbidden_tokens() -> list[str]:
    if not FORBIDDEN_TOKENS.exists():
        return []
    return [
        line.strip()
        for line in FORBIDDEN_TOKENS.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def pptx_slide_text(path: Path) -> list[tuple[int, str, int]]:
    rows: list[tuple[int, str, int]] = []
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=lambda value: int(re.search(r"slide(\d+)\.xml", value).group(1)),
        )
        for name in slide_names:
            slide_no = int(re.search(r"slide(\d+)\.xml", name).group(1))
            xml = zf.read(name).decode("utf-8", errors="ignore")
            texts = [html.unescape(value) for value in re.findall(r"<a:t>(.*?)</a:t>", xml)]
            shape_count = len(re.findall(r"<p:sp>", xml))
            rows.append((slide_no, "\n".join(texts), shape_count))
    return rows


def run_qa(output_dir: Path) -> tuple[bool, Path]:
    pptx = output_dir / "output.pptx"
    slides_json = output_dir / "slides.json"
    report = output_dir / "qa_report.md"
    issues: list[str] = []
    token_hits: list[str] = []
    shape_count = 0
    slide_count = 0

    if not pptx.exists():
        issues.append("missing output.pptx")
    if not slides_json.exists():
        issues.append("missing slides.json")
    if pptx.exists():
        rows = pptx_slide_text(pptx)
        slide_count = len(rows)
        for slide_no, text, slide_shapes in rows:
            shape_count += slide_shapes
            for token in load_forbidden_tokens():
                if token in text:
                    token_hits.append(f"slide {slide_no}: {token}")
    if slide_count != 5:
        issues.append(f"unexpected slide count: {slide_count}")
    issues.extend(f"forbidden token hit: {hit}" for hit in token_hits)

    ok = not issues
    lines = [
        "# Proposal Builder Demo QA Report",
        "",
        f"- Generated: `{now()}`",
        f"- Status: `{'PASS' if ok else 'NEEDS_FIX'}`",
        f"- Output dir: `{output_dir}`",
        f"- PPTX exists: `{pptx.exists()}`",
        f"- slides.json exists: `{slides_json.exists()}`",
        f"- Slide count: `{slide_count}`",
        f"- Shape count: `{shape_count}`",
        f"- Forbidden token hits: `{len(token_hits)}`",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This demo does not use private project data.",
        "- This demo does not call external APIs.",
        "- This demo does not generate HWP output.",
        "- This demo does not claim model training or deployment.",
    ])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ok, report


def command_build(args: argparse.Namespace) -> int:
    prd = Path(args.prd).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not prd.exists():
        print(f"missing prd: {prd}", file=sys.stderr)
        return 2
    slides = build_ir(prd, output)
    pptx = build_pptx(slides, output)
    ok, report = run_qa(output)
    print(f"slides_json={output / 'slides.json'}")
    print(f"pptx={pptx}")
    print(f"qa_report={report}")
    print(f"RESULT {'PASS' if ok else 'NEEDS_FIX'} demo_build")
    return 0 if ok else 1


def command_qa(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    ok, report = run_qa(output)
    print(f"qa_report={report}")
    print(f"RESULT {'PASS' if ok else 'NEEDS_FIX'} demo_qa")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run public-safe Proposal Builder demo workflows.")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="build the bundled public-safe sample")
    demo.add_argument("--prd", default=str(DEFAULT_PRD))
    demo.add_argument("--output", default=str(DEFAULT_OUTPUT))
    demo.set_defaults(func=command_build)

    build = sub.add_parser("build", help="build slides.json, output.pptx, and qa_report.md from a PRD")
    build.add_argument("--prd", required=True)
    build.add_argument("--output", required=True)
    build.set_defaults(func=command_build)

    qa = sub.add_parser("qa", help="run QA for an existing output folder")
    qa.add_argument("--output", required=True)
    qa.set_defaults(func=command_qa)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
