# Spec Lock — 001-dw_ai 제안서 (KALDA 발주처 톤)

> **CRITICAL**: 매 SVG 페이지 생성 전 본 파일을 재읽기. 이 안에 정의된 색·폰트·아이콘·레이아웃 외 임의 값 사용 금지.

## I. Canvas

| Property | Value |
|---|---|
| viewBox | `0 0 1280 720` |
| dimensions | 1280×720 |
| EMU target (PPTX) | 12192000×6858000 |
| margin (left/right) | 40 |
| margin (top) | 0 (헤더 없는 본문 슬라이드) / 100 (헤더 있는 슬라이드) |
| margin (bottom) | 30 (footer 페이지번호) |

## II. Colors (HEX, baseline v2 sampled)

| Variable | HEX | 용도 |
|---|---|---|
| NAVY_HEADER | `#0D3462` | 풀폭 헤더, Part divider 좌측 패널 |
| NAVY_DEEP | `#0C2042` | 카드 제목, 강조 텍스트 |
| NAVY_LIGHT | `#10366B` | 헤더 그라데이션 종점 |
| ORANGE | `#F16A1F` | 우선순위, 비용, 핵심 판단, "필수" 등급 |
| ORANGE_SOFT | `#FFEFE0` | 강조 카드 배경 |
| WHITE | `#FFFFFF` | 카드 배경 |
| GRAY_BG | `#F6F8FB` | 슬라이드 본문 배경 |
| GRAY_BG_DEEP | `#F0F4FA` | 카드 행 alternating |
| GRAY_TEXT | `#37425A` | 본문 텍스트 |
| GRAY_SOFT | `#6B7688` | 캡션, 부제, "참고" 등급 |
| GRAY_TERTIARY | `#95A5BC` | footnote, page number |
| BORDER | `#D8DFE9` | 카드 테두리 |
| GREEN_ACCENT | `#27AE60` | 긍정 지표, "권장" 등급 옵션 |

## III. Gradients

```xml
<linearGradient id="navyHeader" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#0D3462" />
  <stop offset="100%" stop-color="#10366B" />
</linearGradient>

<linearGradient id="orangeAccent" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#F16A1F" />
  <stop offset="100%" stop-color="#F58A4A" />
</linearGradient>

<radialGradient id="bgDecor" cx="85%" cy="15%" r="40%">
  <stop offset="0%" stop-color="#0D3462" stop-opacity="0.04"/>
  <stop offset="100%" stop-color="#0D3462" stop-opacity="0"/>
</radialGradient>
```

## IV. Typography

| Role | Size (viewBox unit) | Weight | Color | Family |
|---|---|---|---|---|
| TITLE (h1) | 32 | 700 | WHITE (헤더) / NAVY_DEEP (본문) | Malgun Gothic stack |
| SUBTITLE | 16 | 400 | #D0D8E5 (헤더) / GRAY_SOFT (본문) | Malgun Gothic stack |
| H2 (카드 제목) | 22 | 700 | NAVY_DEEP | Malgun Gothic stack |
| H3 (섹션 헤더) | 16 | 700 | NAVY_DEEP | Malgun Gothic stack |
| BODY | 13 | 400 | GRAY_TEXT | Malgun Gothic stack |
| CAPTION | 11 | 400 | GRAY_SOFT | Malgun Gothic stack |
| BADGE | 16 | 700 | WHITE | Malgun Gothic stack |
| FOOTNOTE | 10 | 400 | GRAY_TERTIARY | Malgun Gothic stack |

**Font stack**: `'Malgun Gothic', 'AppleGothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif`

**한국어 wrap 룰**:
- 한 `<text>` 요소에 80자 이상 넣지 말 것
- 긴 본문은 줄별로 별도 `<text>` (또는 `<tspan dy="...">`) 사용
- `text-anchor`, `x`, `y` 모두 명시

## V. Layout slots

| Slot | Value (viewBox unit) | 용도 |
|---|---|---|
| HEADER_HEIGHT | 100 | 풀폭 NAVY 헤더 |
| HEADER_HEX_OVERLAY_X | 720~1280 | hexagon 패턴 노출 영역 |
| HEADER_FADE_SOLID_END | 768 (60%) | fade 마스크 solid 종점 |
| HEADER_FADE_TRANSPARENT_START | 960 (75%) | fade 종점 |
| CARD_RADIUS | 14 | 카드 라운드 |
| CARD_BORDER_W | 1 | 카드 테두리 |
| CARD_LEFT_BAR_W | 6 | 카드 좌측 컬러바 (orange/blue/green/orange) |
| CARD_PADDING | 24 | 카드 내부 패딩 |
| CARD_GUTTER | 18 | 카드 사이 간격 |
| TABLE_HEADER_H | 38 | 표 헤더 행 높이 |
| TABLE_ROW_H | 42 | 표 데이터 행 높이 |
| FOOTER_RIBBON_H | 60 | 강조 박스 높이 (하단 핵심 판단) |
| PAGE_NUMBER_W | 38 | 우하단 페이지번호 박스 |
| PAGE_NUMBER_H | 22 | 우하단 페이지번호 박스 |

## VI. Page-rhythm tags

각 슬라이드는 다음 중 하나의 layout discipline 적용:
- **`anchor`**: 표지·divider — 큰 핵심 요소 1~2개, 빈 공간 의도적
- **`dense`**: 본문 카드형 — 정보 카드 4~8개, 한 화면에 결론
- **`breathing`**: 결론·강조 — 1~3개 강조 박스, 여백 충분

## VII. 발주처 톤 (KALDA — 영구)

- 공개 제안서 템플릿 기준을 따른다.
- 보행자/교통약자 보호 중심
- AI 판단은 운영자 보조정보
- 비용/기간/KPI는 "안", "예비 산정안", "조정 가능"으로 표현

## VIII. 금지 표현 (templates/qa/forbidden_tokens.txt)

평가기준, 평가항목, 배점, PoC, native editable, native objects, visual refinement, v1.1, v1.2, Scorecard, 가중치, 확인기준

## IX. 표지·Part Divider 페이지번호 금지 (영구)

다음 슬라이드는 페이지번호 미표시:
- p.1 (표지)
- p.5 (Part 01 divider)
- p.11 (Part 02 divider)
- p.20 (Part 03 divider)
- p.25 (Part 04 divider)

본문 슬라이드는 우하단 `(1232, 690, 38, 22)` 위치에 흰 라운드 박스 + NAVY 글자.

## X. Decoration 자산 (templates/decorations/)

- `hexagon-network-navy-full.png` — 풀폭 헤더용
- `hexagon-network-navy-corner.png` — NAVY 우상단 코너
- `hexagon-network-corner-transparent.png` — transparent 우상단 코너 (Contents)
- `hexagon-network-navy-panel.png` — Part divider 좌측 패널
- `header-fade-mask-navy.png` — 헤더 fade 마스크

SVG에서 `<image href="..." x=".." y=".." width=".." height=".." />`로 embed.
