# AI 이미지 생성 프롬프트 종합 가이드 — 기준 제안서

> 본 문서는 v7 final_native.pptx의 일부 슬라이드(증빙 영역)에서 native 도형으로 재현이 어려운 사진/스크린샷을 외부 AI 이미지 생성 도구로 생성할 때 사용할 프롬프트 모음입니다.
>
> 호환 도구: Midjourney v6 / DALL-E 3 / Imagen 3 / Stable Diffusion XL
> 한국어 텍스트 포함 이미지는 Imagen 3 또는 한국어 친화 모델 권장.

---

## 사용 위치 안내

| 슬라이드 | 영역 | 현재 상태 | 권장 |
|---|---|---|---|
| **p.1 표지** | ㈜샘플기관 로고 영역 | 텍스트 placeholder | **사용자 제공 (실제 로고 PNG/SVG)** |
| **p.28 4-3 공공·AI 실적** | 사업 결과 화면 2장 | placeholder + 라벨 | AI 생성 또는 실제 캡처 |
| **p.29 4-4 디지털트윈** | 모니터링 화면 3장 | placeholder + 라벨 | AI 생성 (시각화·관제·What-if) |
| **p.30 4-5 인증** | 인증서 logo 2장 | placeholder | **공식 인증기관 로고 (위조 금지)** |
| **p.32 제청기관 정보** | ㈜샘플기관 로고 | 텍스트 placeholder | **사용자 제공** |

---

## 🎨 AI 생성 프롬프트 (8종)

### Prompt 01 — p.28 좌: 공공 AI 사업 실적 화면 1 (관제센터 메인)

```
Korean public traffic control center main monitoring screen,
wide curved display showing 12 CCTV grid feeds of urban intersections,
real-time vehicle and pedestrian detection with bounding boxes in orange,
left sidebar with event timeline and risk level indicators,
top status bar with KPI metrics in blue cards,
modern professional government command center aesthetic,
dark navy blue (#0D3462) UI theme with orange (#F16A1F) accent,
clean Korean text labels, ultra detailed, 4K, photorealistic,
--ar 16:10 --v 6 --style raw --quality 2
```

**대안 도구별**:
- **DALL-E 3**: "A Korean public traffic control center monitoring dashboard with multiple CCTV feeds in a grid layout, AI detecting pedestrians and vehicles with orange bounding boxes, real-time event timeline on the left sidebar, KPI metrics at the top, dark navy blue and orange professional UI, photorealistic, 16:10 aspect ratio"
- **Imagen 3**: 동일 영문 + "한국어 라벨 포함, 정부 관제센터 스타일"

---

### Prompt 02 — p.28 우: 공공 AI 사업 실적 화면 2 (Before/After 분석)

```
Korean traffic safety improvement project portfolio screenshot,
before/after comparison of 3 dangerous intersections,
left side shows previous accident heatmap with red dots dense,
right side shows post-intervention reduced accidents in green,
percentage reduction labels prominently displayed (-32%, -45%, -28%),
KPI achievement summary cards at bottom in navy blue,
official government project report style, clean Korean UI,
navy blue and white tone with orange highlights for key numbers,
photorealistic dashboard mockup, 4K detail,
--ar 4:3 --v 6 --style raw
```

---

### Prompt 03 — p.29 좌: 3D 디지털트윈 화면

```
Isometric 3D digital twin visualization of Korean urban intersection,
realistic city block with 4-way intersection, traffic signals, crosswalks,
3D rendered cars at various positions, pedestrians on sidewalks,
CCTV cameras visible at corners with cone-of-view indicators in semi-transparent blue,
AI-detected pedestrian risk zones highlighted in transparent orange overlays,
red collision risk markers at right-turn conflict points,
data overlay panels floating on right side with live metrics,
modern technical visualization aesthetic, navy blue base + orange + white,
dramatic lighting, ultra detailed, 4K,
--ar 16:9 --v 6 --style raw --quality 2
```

---

### Prompt 04 — p.29 가운데: 실시간 모니터링 화면

```
Real-time traffic safety monitoring dashboard interface,
top header bar with KPI cards (12 active alerts, 3 critical, 87% detection rate),
center area split into 3 panels:
  left: live CCTV feed of school zone with pedestrian detection boxes,
  center: event timeline graph with color-coded risk levels (1-5),
  right: geographic heatmap of city with risk hotspots in red/orange,
bottom panel: scrollable event log table with timestamp/location/type/action,
clean professional Korean government enterprise UI,
dark theme with navy (#0D3462) header, white cards, orange (#F16A1F) accents for alerts,
photorealistic UI mockup, ultra detailed 4K,
--ar 16:9 --v 6 --style raw
```

---

### Prompt 05 — p.29 우: What-if 시뮬레이션 / 운영 대시보드

```
Operations management dashboard for pedestrian safety service simulation,
"What-if Analysis" header with scenario controls,
left side: simulation parameter sliders (signal timing, speed limit, lighting),
center: 3D top-down map view of intersection with predicted safety improvement zones,
right side: comparative bar chart showing baseline vs simulated risk reduction (45% improvement),
bottom: monthly trend line chart with seasonal patterns,
KPI indicator cards showing projected outcomes,
Korean text labels, navy blue + green + orange enterprise UI,
clean professional aesthetic, ultra detailed 4K dashboard mockup,
--ar 16:9 --v 6 --style raw
```

---

### Prompt 06 — p.30 좌: CMMI / ISMS 인증서 (placeholder 대안)

> ⚠️ **인증서 logo는 위조 금지**. 다음 중 한 가지 선택:
> 1. **공식 logo 다운로드 (권장)**: 발행기관 공식 사이트에서 logo 사용 라이선스 확인 후 사용
>    - CMMI Institute: https://cmmiinstitute.com/
>    - 한국인터넷진흥원 (ISMS): https://isms.kisa.or.kr/
> 2. **실제 보유 인증서 스캔**: 사용자가 보유한 인증서 사본을 PDF/이미지로 첨부
> 3. **AI 생성은 부적합** — 실제 인증서 위조로 오인될 수 있음

대신 placeholder를 디자인 친화 형태로 유지:
```
Professional certification badge mockup placeholder,
generic shield-and-checkmark logo design (NOT mimicking any real certification),
"Certification Pending" or "별도 첨부" Korean label clearly visible,
clean minimalist design, navy blue and silver gradient,
white background, ultra clean, --ar 1:1 --v 6
```

---

### Prompt 07 — p.30 우: ISO 9001 / 27001 인증서 (placeholder 대안)

> 동일하게 **공식 logo 다운로드 권장**. ISO logo 사용은 ISO 9001:2015 / ISO 27001:2013 라이선스 정책 확인 필수.

---

### Prompt 08 — p.1 표지: ㈜샘플기관 로고 영역 (사용자 제공 권장)

> ⚠️ **로고는 사용자 제공 필수** (회사 공식 자산).
>
> 만약 임시 placeholder가 필요하다면:

```
Modern corporate logo placeholder for "㈜샘플기관 (Sample Org Co., Ltd.)",
clean geometric design with stylized "D" letter,
navy blue (#0D3462) and orange (#F16A1F) corporate colors,
minimalist sans-serif typography, professional Korean tech company aesthetic,
white background, vector-clean style, --ar 1:1 --v 6
```

→ 이는 임시 placeholder이며 **실제 로고가 들어가야** 합니다.

---

## 📐 통일 디자인 가이드 (모든 AI 이미지에 적용)

생성된 모든 이미지가 본 제안서의 디자인 시스템과 일관되도록:

### 컬러 팔레트
- **NAVY_HEADER**: `#0D3462` (헤더, 메인 UI)
- **NAVY_LIGHT**: `#10366B` (그라데이션 종점)
- **NAVY_DEEP**: `#0C2042` (강조 텍스트)
- **ORANGE**: `#F16A1F` (포인트, 경고, 핵심 데이터)
- **GREEN**: `#27AE60` (긍정 지표, 안전 지표)
- **WHITE**: `#FFFFFF` (카드, 배경)
- **GRAY_BG**: `#F6F8FB` (본문 배경)

### 톤 키워드 (모든 프롬프트에 추가)
```
clean professional Korean government UI, modern enterprise aesthetic,
navy blue + white + orange accent color scheme,
high-contrast readable typography
```

### 회피 키워드 (negative prompts)
```
--no cartoon, sticker, low quality, blurry, watermark, signature,
text overlay errors, distorted Korean characters, fake certification logos
```

---

## 🛠️ PPT 삽입 워크플로우

AI로 이미지 생성 후 v7 final_native.pptx에 삽입하는 절차:

### 방법 1: PowerPoint에서 직접 삽입 (권장)
1. 생성된 이미지를 `projects/<project-id>/assets/p28_screen1.png` 등으로 저장
2. PowerPoint로 `output/final_native.pptx` 열기
3. p.28/29/30 슬라이드 이동
4. 기존 placeholder 회색 박스 선택 → 우클릭 → "그림으로 채우기" 또는 박스 위에 사진 삽입
5. 기존 placeholder 텍스트("※ 별도 첨부 자료 참조") 제거
6. 다른 이름으로 저장

### 방법 2: 자동화 스크립트 (배치 처리)

```python
# projects/<project-id>/output/_inject_ai_images.py
from pptx import Presentation
from pptx.util import Emu

prs = Presentation('final_native.pptx')

INJECTIONS = {
    # (slide_idx, placeholder_idx_in_slide): 'asset_path'
    (27, 0): '../assets/p28_screen1.png',     # p.28 좌
    (27, 1): '../assets/p28_screen2.png',     # p.28 우
    (28, 0): '../assets/p29_3d_twin.png',     # p.29 좌
    (28, 1): '../assets/p29_realtime.png',    # p.29 가운데
    (28, 2): '../assets/p29_whatif.png',      # p.29 우
    (29, 0): '../assets/p30_cert1.png',       # p.30 좌
    (29, 1): '../assets/p30_cert2.png',       # p.30 우
}

for (sl_idx, ph_idx), path in INJECTIONS.items():
    sl = prs.slides[sl_idx]
    placeholders = [s for s in sl.shapes
                    if s.shape_type in (1, 5) and s.fill.type and s.width > Emu(2000000)]
    if ph_idx >= len(placeholders): continue
    ph = placeholders[ph_idx]
    # placeholder 위치/크기로 picture 삽입
    sl.shapes.add_picture(path, ph.left, ph.top, ph.width, ph.height)
    # placeholder 제거
    ph._element.getparent().remove(ph._element)

prs.save('final_native_with_images.pptx')
```

---

## 🚦 우선순위 권장

1. **즉시 필요 (제출 직전)**:
   - 샘플기관 로고 PNG/SVG → p.1, p.32
   - CMMI/ISMS/ISO 인증 logo (공식) → p.30

2. **품질 향상 (선택)**:
   - p.29 디지털트윈/모니터링 화면 3장 → AI 생성으로 자체 시각화 가능
   - p.28 공공 AI 실적 화면 2장 → 실제 사업 캡처가 있으면 그것 우선

3. **현재 placeholder 유지 가능**:
   - "별도 첨부 자료 참조" 라벨로 남겨두고 제출 시 별도 첨부 문서로 대체 가능

---

## 검증 체크리스트

AI 생성 이미지를 PPT에 삽입한 후:

- [ ] 이미지 해상도 ≥ 1920×1080 (4K 권장)
- [ ] 한국어 텍스트가 깨지지 않음 (또는 영문만)
- [ ] 본 제안서 디자인 시스템 컬러 톤 일치 (NAVY/ORANGE/WHITE)
- [ ] 워터마크 없음
- [ ] 위조 인증서 로고 없음 (실제 로고 또는 placeholder만)
- [ ] 슬라이드 placeholder 영역과 비율 일치
- [ ] PPT → PDF 변환 후에도 이미지 깨끗하게 보존

---

## 참고

본 가이드는 v7 final_native.pptx (32장 100% native + 5장 baseline-grade 도식)의 보조 문서입니다.
도식·표·차트는 모두 native SVG로 재현 완료. 본 가이드의 AI 이미지는 **선택적 보조 자산**입니다.
