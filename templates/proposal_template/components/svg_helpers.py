"""
재사용 가능한 SVG 헬퍼 라이브러리 — baseline 수준의 도식·아이콘 정밀 재현용.
모든 함수는 SVG 문자열 반환.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _build_svg import S, escape


# ============================================================
# 공통 헤더 / 푸터 / 페이지번호
# ============================================================
def codex_header(title: str, subtitle: str) -> str:
    """codex 톤 풀폭 NAVY 헤더 + 우상단 5 stripe."""
    out = [f'<rect x="0" y="0" width="1280" height="100" fill="{S.NAVY_HEADER}"/>']
    for i, x in enumerate([1043, 1090, 1130, 1156, 1198]):
        col = S.ORANGE if i in [0, 4] else S.NAVY_LIGHT
        op = 0.85 if col == S.ORANGE else 0.6
        out.append(f'<rect x="{x}" y="-20" width="22" height="150" fill="{col}" opacity="{op}"/>')
    out.append(f'<text x="40" y="58" font-family="{S.FONT}" font-size="28" font-weight="700" fill="{S.WHITE}">{escape(title)}</text>')
    out.append(f'<text x="40" y="86" font-family="{S.FONT}" font-size="13" fill="#D0D8E5">{escape(subtitle)}</text>')
    return '\n'.join(out)


def page_number(num: int) -> str:
    return (f'<rect x="1232" y="690" width="38" height="22" rx="4" fill="{S.WHITE}" stroke="{S.BORDER}"/>'
            f'<text x="1251" y="705" font-family="{S.FONT}" font-size="10" fill="{S.NAVY_DEEP}" text-anchor="middle">{num:02d}</text>')


def source_footer(text: str) -> str:
    return (f'<rect x="40" y="660" width="1200" height="38" rx="6" fill="{S.GRAY_BG_DEEP}"/>'
            f'<text x="640" y="683" font-family="{S.FONT}" font-size="10" fill="{S.GRAY_SOFT}" text-anchor="middle">{escape(text)}</text>')


def card(x: int, y: int, w: int, h: int, *, color: str = S.ORANGE, label: str | None = None,
         label_color: str = S.NAVY_HEADER, radius: int = 14) -> str:
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{S.WHITE}" stroke="{S.BORDER}"/>',
           f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{color}"/>']
    if label:
        out.append(f'<rect x="{x+18}" y="{y+18}" width="80" height="22" rx="11" fill="{label_color}"/>')
        out.append(f'<text x="{x+58}" y="{y+33}" font-family="{S.FONT}" font-size="10" font-weight="700" fill="{S.WHITE}" text-anchor="middle">{escape(label)}</text>')
    return '\n'.join(out)


def small_card(x: int, y: int, w: int, h: int, *, color: str = S.NAVY_LIGHT, radius: int = 10) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{S.WHITE}" stroke="{S.BORDER}"/>'
            f'<rect x="{x}" y="{y}" width="4" height="{h}" fill="{color}"/>')


# ============================================================
# 사람 아이콘 (남성/여성/어린이/노인)
# ============================================================
def person(cx: int, cy: int, scale: float = 1.0, color: str = S.NAVY_HEADER, kind: str = 'adult') -> str:
    """단순 사람 아이콘 (top-down view 또는 side view)."""
    s = scale
    if kind == 'adult':
        head_r = 4 * s
        body_h = 12 * s
        leg_h = 6 * s
    elif kind == 'child':
        head_r = 3 * s
        body_h = 8 * s
        leg_h = 4 * s
    elif kind == 'elderly':
        head_r = 4 * s
        body_h = 12 * s
        leg_h = 6 * s
    else:
        head_r, body_h, leg_h = 4*s, 12*s, 6*s

    head_y = cy
    body_y_top = cy + head_r + 1
    body_y_bot = body_y_top + body_h
    leg_y_bot = body_y_bot + leg_h
    half_w = body_h * 0.4

    out = [f'<circle cx="{cx}" cy="{head_y}" r="{head_r}" fill="{color}"/>',
           f'<polygon points="{cx-half_w*0.6},{body_y_top} {cx+half_w*0.6},{body_y_top} {cx+half_w},{body_y_bot} {cx-half_w},{body_y_bot}" fill="{color}"/>',
           f'<rect x="{cx-half_w*0.6}" y="{body_y_bot}" width="{half_w*0.5}" height="{leg_h}" fill="{color}"/>',
           f'<rect x="{cx+half_w*0.1}" y="{body_y_bot}" width="{half_w*0.5}" height="{leg_h}" fill="{color}"/>']
    if kind == 'elderly':
        # 지팡이
        out.append(f'<line x1="{cx+half_w+2}" y1="{body_y_top}" x2="{cx+half_w+2}" y2="{leg_y_bot}" stroke="{S.GRAY_SOFT}" stroke-width="1.2"/>')
    return '\n'.join(out)


# ============================================================
# 자동차 (top-down)
# ============================================================
def car_topdown(cx: int, cy: int, color: str = '#F4C534', orientation: str = 'down', scale: float = 1.0) -> str:
    """top-down 자동차. orientation: 'down' 'up' 'left' 'right'."""
    w = 24 * scale
    h = 40 * scale
    if orientation in ('left', 'right'):
        w, h = h, w
    x = cx - w/2
    y = cy - h/2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{color}" stroke="#A0801F" stroke-width="1"/>']
    if orientation == 'down':
        # 앞 유리 위쪽
        out.append(f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="9" rx="2" fill="#1A2A4A" opacity="0.7"/>')
        out.append(f'<rect x="{x+3}" y="{y+h-12}" width="{w-6}" height="9" rx="2" fill="#1A2A4A" opacity="0.7"/>')
    elif orientation == 'up':
        out.append(f'<rect x="{x+3}" y="{y+h-12}" width="{w-6}" height="9" rx="2" fill="#1A2A4A" opacity="0.7"/>')
        out.append(f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="9" rx="2" fill="#1A2A4A" opacity="0.7"/>')
    elif orientation == 'right':
        out.append(f'<rect x="{x+w-12}" y="{y+3}" width="9" height="{h-6}" rx="2" fill="#1A2A4A" opacity="0.7"/>')
    elif orientation == 'left':
        out.append(f'<rect x="{x+3}" y="{y+3}" width="9" height="{h-6}" rx="2" fill="#1A2A4A" opacity="0.7"/>')
    return '\n'.join(out)


# ============================================================
# 도로 (top-down)
# ============================================================
def horizontal_road(x: int, y: int, w: int, h: int = 80, *, lane_dash: bool = True, edges: bool = True) -> str:
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#7A8290"/>']
    if edges:
        out.append(f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="#F2C94C" stroke-width="2"/>')
        out.append(f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="#F2C94C" stroke-width="2"/>')
    if lane_dash:
        out.append(f'<line x1="{x}" y1="{y+h/2}" x2="{x+w}" y2="{y+h/2}" stroke="{S.WHITE}" stroke-dasharray="10 8" stroke-width="2"/>')
    return '\n'.join(out)


def vertical_road(x: int, y: int, w: int = 80, h: int = 200, *, lane_dash: bool = True, edges: bool = True) -> str:
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#7A8290"/>']
    if edges:
        out.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+h}" stroke="#F2C94C" stroke-width="2"/>')
        out.append(f'<line x1="{x+w}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="#F2C94C" stroke-width="2"/>')
    if lane_dash:
        out.append(f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="{S.WHITE}" stroke-dasharray="10 8" stroke-width="2"/>')
    return '\n'.join(out)


def crosswalk(x: int, y: int, w: int, h: int = 14, vertical: bool = False) -> str:
    """횡단보도 줄무늬."""
    out = []
    if vertical:
        n = int(h / 10)
        for i in range(n):
            out.append(f'<rect x="{x}" y="{y + i*10}" width="{w}" height="6" fill="{S.WHITE}"/>')
    else:
        n = int(w / 10)
        for i in range(n):
            out.append(f'<rect x="{x + i*10}" y="{y}" width="6" height="{h}" fill="{S.WHITE}"/>')
    return '\n'.join(out)


# ============================================================
# 아이콘 (작은 path-based)
# ============================================================
def icon_camera(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<rect x="{cx-9*s}" y="{cy-6*s}" width="{18*s}" height="{12*s}" rx="2" fill="none" stroke="{color}" stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{3*s}" fill="none" stroke="{color}" stroke-width="1.5"/>'
            f'<rect x="{cx-3*s}" y="{cy-9*s}" width="{6*s}" height="{3*s}" fill="{color}"/>')


def icon_brain(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<circle cx="{cx}" cy="{cy}" r="{8*s}" fill="none" stroke="{color}" stroke-width="1.5"/>'
            f'<path d="M {cx-4*s} {cy} L {cx+4*s} {cy}" stroke="{color}" stroke-width="1.5"/>'
            f'<path d="M {cx} {cy-4*s} L {cx} {cy+4*s}" stroke="{color}" stroke-width="1.5"/>')


def icon_speaker(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<polygon points="{cx-7*s},{cy-3*s} {cx-2*s},{cy-3*s} {cx+3*s},{cy-7*s} {cx+3*s},{cy+7*s} {cx-2*s},{cy+3*s} {cx-7*s},{cy+3*s}" fill="none" stroke="{color}" stroke-width="1.5"/>'
            f'<path d="M {cx+5*s} {cy-3*s} Q {cx+9*s} {cy} {cx+5*s} {cy+3*s}" fill="none" stroke="{color}" stroke-width="1.5"/>')


def icon_doc(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<rect x="{cx-7*s}" y="{cy-9*s}" width="{14*s}" height="{16*s}" fill="none" stroke="{color}" stroke-width="1.5"/>'
            f'<line x1="{cx-4*s}" y1="{cy-5*s}" x2="{cx+4*s}" y2="{cy-5*s}" stroke="{color}"/>'
            f'<line x1="{cx-4*s}" y1="{cy-1*s}" x2="{cx+4*s}" y2="{cy-1*s}" stroke="{color}"/>'
            f'<line x1="{cx-4*s}" y1="{cy+3*s}" x2="{cx+4*s}" y2="{cy+3*s}" stroke="{color}"/>')


def icon_warning(cx: int, cy: int, color: str = S.ORANGE, scale: float = 1.0) -> str:
    s = scale
    return (f'<polygon points="{cx},{cy-9*s} {cx+9*s},{cy+7*s} {cx-9*s},{cy+7*s}" fill="{color}"/>'
            f'<text x="{cx}" y="{cy+5*s}" font-family="{S.FONT}" font-size="{12*s}" font-weight="700" fill="{S.WHITE}" text-anchor="middle">!</text>')


def icon_octagon(cx: int, cy: int, color: str = '#C0392B', scale: float = 1.0, label: str = '') -> str:
    """정지 표지 (8각형)."""
    s = scale * 9
    pts = f'{cx-s/2},{cy-s} {cx+s/2},{cy-s} {cx+s},{cy-s/2} {cx+s},{cy+s/2} {cx+s/2},{cy+s} {cx-s/2},{cy+s} {cx-s},{cy+s/2} {cx-s},{cy-s/2}'
    out = [f'<polygon points="{pts}" fill="{color}"/>']
    if label:
        out.append(f'<text x="{cx}" y="{cy+4}" font-family="{S.FONT}" font-size="{8*scale}" font-weight="700" fill="{S.WHITE}" text-anchor="middle">{escape(label)}</text>')
    return '\n'.join(out)


def icon_speedometer(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<path d="M {cx-8*s} {cy+4*s} A {8*s} {8*s} 0 0 1 {cx+8*s} {cy+4*s}" fill="none" stroke="{color}" stroke-width="1.8"/>'
            f'<line x1="{cx}" y1="{cy+4*s}" x2="{cx+5*s}" y2="{cy-3*s}" stroke="{color}" stroke-width="1.8"/>'
            f'<circle cx="{cx}" cy="{cy+4*s}" r="{1.5*s}" fill="{color}"/>')


def icon_signal(cx: int, cy: int, scale: float = 1.0) -> str:
    """신호기 아이콘."""
    s = scale
    return (f'<rect x="{cx-5*s}" y="{cy-12*s}" width="{10*s}" height="{24*s}" rx="2" fill="#2A2A2A"/>'
            f'<circle cx="{cx}" cy="{cy-7*s}" r="{2.5*s}" fill="#E74C3C"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{2.5*s}" fill="#F1C40F"/>'
            f'<circle cx="{cx}" cy="{cy+7*s}" r="{2.5*s}" fill="#27AE60"/>')


def icon_school(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    """학교 건물 아이콘."""
    s = scale
    return (f'<rect x="{cx-12*s}" y="{cy-8*s}" width="{24*s}" height="{16*s}" fill="{color}"/>'
            f'<polygon points="{cx-12*s},{cy-8*s} {cx},{cy-14*s} {cx+12*s},{cy-8*s}" fill="{S.ORANGE}"/>'
            f'<rect x="{cx-2*s}" y="{cy-2*s}" width="{4*s}" height="{8*s}" fill="{S.WHITE}"/>'
            f'<text x="{cx}" y="{cy-4*s}" font-family="{S.FONT}" font-size="{6*s}" font-weight="700" fill="{S.WHITE}" text-anchor="middle">학교</text>')


def icon_check_circle(cx: int, cy: int, color: str = S.GREEN, scale: float = 1.0) -> str:
    s = scale
    return (f'<circle cx="{cx}" cy="{cy}" r="{8*s}" fill="{color}"/>'
            f'<path d="M {cx-4*s} {cy} L {cx-1*s} {cy+3*s} L {cx+4*s} {cy-3*s}" fill="none" stroke="{S.WHITE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')


def icon_cctv(cx: int, cy: int, color: str = S.NAVY_HEADER, scale: float = 1.0) -> str:
    s = scale
    return (f'<rect x="{cx-9*s}" y="{cy-4*s}" width="{14*s}" height="{8*s}" rx="2" fill="{color}"/>'
            f'<polygon points="{cx-9*s},{cy-4*s} {cx-13*s},{cy-7*s} {cx-13*s},{cy+7*s} {cx-9*s},{cy+4*s}" fill="{color}"/>'
            f'<rect x="{cx-1*s}" y="{cy+4*s}" width="{2*s}" height="{4*s}" fill="{color}"/>')


def icon_edge_box(cx: int, cy: int, color: str = S.NAVY_LIGHT, scale: float = 1.0) -> str:
    """Edge 장치 (작은 box with antenna)."""
    s = scale
    return (f'<rect x="{cx-8*s}" y="{cy-5*s}" width="{16*s}" height="{10*s}" rx="2" fill="{color}"/>'
            f'<circle cx="{cx-3*s}" cy="{cy}" r="{1*s}" fill="{S.GREEN}"/>'
            f'<circle cx="{cx+3*s}" cy="{cy}" r="{1*s}" fill="{S.WHITE}"/>'
            f'<line x1="{cx}" y1="{cy-5*s}" x2="{cx}" y2="{cy-10*s}" stroke="{color}" stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{cy-11*s}" r="{1*s}" fill="{S.ORANGE}"/>')


def icon_shield(cx: int, cy: int, color: str = S.GREEN, scale: float = 1.0) -> str:
    s = scale
    return (f'<path d="M {cx} {cy-10*s} L {cx+9*s} {cy-7*s} L {cx+9*s} {cy+3*s} Q {cx+9*s} {cy+8*s} {cx} {cy+11*s} Q {cx-9*s} {cy+8*s} {cx-9*s} {cy+3*s} L {cx-9*s} {cy-7*s} Z" fill="{color}"/>'
            f'<path d="M {cx-3*s} {cy} L {cx-1*s} {cy+3*s} L {cx+4*s} {cy-3*s}" stroke="{S.WHITE}" stroke-width="1.8" fill="none"/>')


# ============================================================
# 차트
# ============================================================
def bar_chart(ox: int, oy: int, w: int, h: int, data: list[tuple[str, float, str]],
              max_val: float | None = None, *, label_fmt: str = '{:.0f}') -> str:
    """간단 막대 차트. data = [(label, value, color), ...]."""
    if not max_val:
        max_val = max(d[1] for d in data) * 1.15
    out = [f'<line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{S.BORDER}"/>',
           f'<line x1="{ox}" y1="{oy-h}" x2="{ox}" y2="{oy}" stroke="{S.BORDER}"/>']
    n = len(data)
    bw = (w - 20) / n * 0.6
    step = (w - 20) / n
    for i, (label, val, color) in enumerate(data):
        bx = ox + 10 + i*step + (step - bw)/2
        bh = val / max_val * h
        out.append(f'<rect x="{bx}" y="{oy-bh}" width="{bw}" height="{bh}" fill="{color}"/>')
        out.append(f'<text x="{bx+bw/2}" y="{oy-bh-4}" font-family="{S.FONT}" font-size="9" font-weight="700" fill="{S.NAVY_DEEP}" text-anchor="middle">{label_fmt.format(val)}</text>')
        out.append(f'<text x="{bx+bw/2}" y="{oy+14}" font-family="{S.FONT}" font-size="9" fill="{S.GRAY_TEXT}" text-anchor="middle">{escape(label)}</text>')
    return '\n'.join(out)


def stat_circle(cx: int, cy: int, r: int, big_text: str, label: str, color: str = S.ORANGE) -> str:
    """원형 큰 숫자 강조."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{S.WHITE}" stroke="{color}" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy+2}" font-family="{S.FONT}" font-size="{int(r*0.55)}" font-weight="700" fill="{color}" text-anchor="middle">{escape(big_text)}</text>'
            f'<text x="{cx}" y="{cy+r-12}" font-family="{S.FONT}" font-size="9" fill="{S.GRAY_TEXT}" text-anchor="middle">{escape(label)}</text>')


def callout_label(x: int, y: int, w: int, text: str, target_x: int, target_y: int, *,
                   color: str = S.NAVY_HEADER, fill: str = S.WHITE, text_color: str | None = None) -> str:
    tc = text_color or color
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="3" fill="{fill}" stroke="{color}"/>',
           f'<text x="{x+w/2}" y="{y+15}" font-family="{S.FONT}" font-size="10" font-weight="700" fill="{tc}" text-anchor="middle">{escape(text)}</text>',
           f'<line x1="{x}" y1="{y+11}" x2="{target_x}" y2="{target_y}" stroke="{color}"/>',
           f'<circle cx="{target_x}" cy="{target_y}" r="2" fill="{color}"/>']
    return '\n'.join(out)


def numbered_step(x: int, y: int, w: int, num: str, title: str, desc: str,
                   color: str = S.ORANGE, icon_fn=None) -> str:
    """번호 + 제목 + 설명 + 우측 아이콘 (대응 절차용)."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="74" rx="10" fill="{S.GRAY_BG}" stroke="{S.BORDER}"/>',
           f'<circle cx="{x+22}" cy="{y+37}" r="14" fill="{color}"/>',
           f'<text x="{x+22}" y="{y+42}" font-family="{S.FONT}" font-size="13" font-weight="700" fill="{S.WHITE}" text-anchor="middle">{num}</text>',
           f'<text x="{x+44}" y="{y+30}" font-family="{S.FONT}" font-size="13" font-weight="700" fill="{S.NAVY_DEEP}">{escape(title)}</text>']
    for i in range(0, len(desc), 22):
        out.append(f'<text x="{x+44}" y="{y+50+(i//22)*14}" font-family="{S.FONT}" font-size="10" fill="{S.GRAY_TEXT}">{escape(desc[i:i+22])}</text>')
    if icon_fn:
        out.append(f'<rect x="{x+w-50}" y="{y+18}" width="38" height="38" rx="6" fill="{S.WHITE}" stroke="{color}"/>')
        out.append(icon_fn(x+w-31, y+37, color=color, scale=1.0))
    return '\n'.join(out)


def svg_wrap(body: str, bg: str = S.GRAY_BG) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
<rect x="0" y="0" width="1280" height="720" fill="{bg}"/>
{body}
</svg>'''
