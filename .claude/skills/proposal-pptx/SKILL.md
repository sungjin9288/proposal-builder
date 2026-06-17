# Proposal PPTX Generator (SVG-first)

`prd.md` → `design_spec.md` + `spec_lock.md` → SVG 32장 → `output.pptx` + `output.pdf` 파이프라인.

## 워크플로우 개요 (SVG-first)

```
prd.md (사용자 검토 완료)
  ↓ [Phase 0a] PDF/MD에서 baseline 텍스트 정확 추출 (필요 시)
baseline.md
  ↓ [Phase 0b] design_spec.md (인간 narrative — 톤·청중·디자인 결정)
  ↓ [Phase 0c] spec_lock.md (기계 contract — 색·폰트·아이콘·레이아웃 표준)
design_spec.md + spec_lock.md
  ↓ [Phase A~D] 슬라이드별 SVG 합성 (각 페이지마다 spec_lock 재읽기 강제)
svg_final/slide_NN_*.svg (32장)
  ↓ [Build] svg_to_pptx.py --only native
output.pptx (99%+ native editable)
  ↓ soffice headless
output.pdf
  ↓ self-QA (4 thresholds)
final 산출물 + slides.json IR + archive append
```

## 입력 / 출력

### 입력
- `projects/[id]/prd.md` — 사용자가 확정한 PRD
- `projects/[id]/reference/baseline.pdf` (선택) — 참조 디자인

### 출력
- `projects/[id]/design_spec.md` — 디자인 사양서 (인간용 narrative)
- `projects/[id]/spec_lock.md` — 디자인 contract (기계 실행용)
- `projects/[id]/svg_final/slide_NN_*.svg` — SVG 32장
- `projects/[id]/output/final.pptx` — 99%+ native editable
- `projects/[id]/output/final.pdf`
- `projects/[id]/output/slides.json` — IR 스키마

## SVG-first 빌드 룰

### 1. design_spec.md (인간용)
다음 6개 섹션 표준:
1. **I. 프로젝트 정보** — 이름, 캔버스, 페이지 수, 발주처, 청중
2. **II. 캔버스 사양** — viewBox, dimensions, margins
3. **III. 시각 테마** — 컬러 팔레트, 그라데이션 정의, 톤·정조
4. **IV. 타이포그래피** — 폰트 스택, 크기 hierarchy
5. **V. 콘텐츠 흐름** — 슬라이드 순서·rhetoric·핵심 메시지
6. **VI. 페이지별 narrative** — 각 슬라이드의 의도, 강조점

### 2. spec_lock.md (기계용)
LLM이 매 페이지 생성 전 반드시 재읽기. 다음 4개 섹션:
1. **Canvas**: viewBox, dimensions
2. **Colors**: 모든 색을 변수명 + HEX로 (NAVY, ORANGE, BORDER 등). 즉석 색 발명 금지
3. **Typography**: 폰트 스택, 사이즈 (TITLE, H2, BODY, CAPTION, BADGE 등)
4. **Layout slots**: HEADER_HEIGHT, CARD_PADDING, FOOTER_HEIGHT 등 표준 값

매 SVG 페이지 생성 시 spec_lock에 정의된 값만 사용. 새 색·폰트·간격 발명 금지.

### 3. SVG 작성 룰

#### 3.1 캔버스
- viewBox `0 0 1280 720` 표준 (16:9)
- 출력 PPTX는 12192000×6858000 EMU에 비례 매핑

#### 3.2 한국어 텍스트 처리 (중요)
SVG `<text>` → PPTX 변환 시 텍스트박스 wrap 이슈가 있다. 다음 룰 강제:

- **명시적 줄바꿈**: 긴 한국어 텍스트는 `<text>` 한 줄에 80자 이상 넣지 말 것
- **줄별 분리**: 여러 줄은 별도 `<text>` 요소로 작성 (또는 `<tspan>` + 명시적 `dy`)
- **폰트 cascade**: `font-family="'Malgun Gothic', 'AppleGothic', 'Apple SD Gothic Neo', sans-serif"`
- **text 위치**: `x` `y` 모두 명시. PPTX 변환 시 absolute positioning이 정확히 매핑됨
- **text-anchor**: `start | middle | end` 명시 — wrap 시 위치 보존

#### 3.3 표준 디자인 시스템 (기준 발주처 톤 기본)
spec_lock에 다음 변수 강제:
```
COLORS:
  NAVY_HEADER: #0D3462
  NAVY_DEEP: #0C2042
  ORANGE: #F16A1F
  WHITE: #FFFFFF
  GRAY_BG: #F6F8FB
  GRAY_TEXT: #37425A
  BORDER: #D8DFE9

LAYOUT:
  HEADER_HEIGHT: 100  (viewBox units)
  CARD_RADIUS: 14
  CARD_BORDER_W: 1
  CARD_LEFT_BAR_W: 6
  PAGE_MARGIN: 40
  FOOTER_RIBBON_H: 60

TYPO:
  H1_SIZE: 32 bold
  H2_SIZE: 22 bold
  BODY_SIZE: 13
  CAPTION_SIZE: 11
  BADGE_SIZE: 16 bold
```

#### 3.4 표지·Part Divider 페이지번호 금지 (영구 룰)
- p.1 표지, 모든 Part divider: 페이지번호 미표시
- 본문 슬라이드: 우하단 `12192000-padding` 위치에 작은 흰 라운드 박스 + NAVY 글자

#### 3.5 헤더 hexagon overlay + fade-mask (옵션)
풀폭 hexagon 헤더 사용 시:
- z-order: header rect → hexagon overlay → fade-mask → 텍스트
- 자산: `templates/decorations/hexagon-network-navy-full.svg` (또는 PNG embed)
- fade 곡선: 0~60% solid → 60~75% ease-out (1-t)^1.6 → 75~100% transparent

## 빌드 명령

```bash
# SVG → PPTX 변환
python3 vendor/ppt-master/skills/ppt-master/scripts/svg_to_pptx.py \
  projects/[id] \
  --only native \
  -s svg_final \
  -o projects/[id]/output/final.pptx

# PDF 변환
soffice --headless --convert-to pdf projects/[id]/output/final.pptx \
  --outdir projects/[id]/output/

# Self-QA
python3 .claude/skills/proposal-pptx/scripts/self_qa.py projects/[id]
```

## 정제 작업 룰 (image-locked baseline 기반 작업 시)

본 SKILL은 baseline PPTX가 image-locked일 때 "기준본 보존형 디밸롭" 방식으로 작업한다. 다음 룰은 기준 제안서 작업에서 발견·검증되어 일반화되었다.

### 1. 정성 등급 매핑 (제안서 톤)
평가 뉘앙스를 환기하는 수치(% / 점수 / 가중치)는 정성 등급으로 변환한다.
- 3단계: 필수(상위 ≈40%, ORANGE) / 권장(중위 ≈40%, NAVY) / 참고(하위 ≈20%, GRAY)
- 컬럼 헤더 권장: "선정 요소 / 고려 관점 / 확인 기준" (b안 표준)

### 2. 검사 토큰 자가 확장
OCR 금지어 검사 시 명시 토큰 + 동일 뉘앙스 토큰을 누적 관리한다.
- 사전 위치: `templates/qa/forbidden_tokens.txt`
- 매 작업마다 검출된 신규 토큰을 누적

### 3. 가운데 native + 좌·우 baseline 충돌 회피
가운데 영역에 native 카드를 올릴 때, 같은 행의 좌·우 baseline 카드까지 함께 마스킹·재작성한다.

### 4. native 재작성 카드 밀도 ±15%
새로 만든 native 카드의 빈 여백 비율이 baseline 카드 ±15%를 벗어나면 안 된다.
임계값: `templates/qa/quality_thresholds.yaml::card_density_tolerance`

### 5. 헤더 hexagon overlay + fade-mask 동시 적용
풀폭 hexagon 헤더를 사용할 때 좌측 텍스트 가독성 보호를 위해 fade-mask를 함께 적용한다.

### 6. 점진적 native화 (레이어 4단계)
image-locked baseline에서 100% native로 점진 이행:
1. **레이어 1 (BG)**: baseline 슬라이드를 SVG 안에 `<image>`로 배경 배치 (참조용)
2. **레이어 2 (텍스트)**: 모든 텍스트를 SVG `<text>`로 native 작성
3. **레이어 3 (도형)**: 카드/뱃지/표/도식을 SVG 도형으로 native 작성
4. **레이어 4 (확정)**: 시각 검수 통과한 슬라이드에서 baseline BG 제거 → 100% native

각 슬라이드는 layer 1~4를 순차 통과해야 final 산출물 자격.

## 정량 검증 (final 단계 자동)

`templates/qa/quality_thresholds.yaml`의 4개 임계값을 PPTX → PDF → PNG 렌더 후 자동 측정한다.
- header_navy_ratio_min: 0.90
- tone_delta_rgb_max: 5
- card_density_tolerance: 0.15
- ocr_forbidden_count_max: 0

추가 SVG-first 검증:
- **native_shape_ratio_min: 0.95** (전체 shape 중 native 비율 ≥95%)
- **picture_count_max: slide_count × 0.5** (picture는 의도된 사진/일러스트만)

## 주의사항

- 근거 없는 수치나 차트 데이터를 생성하지 않는다
- 템플릿 미제공 시 `templates/decorations/` 자산을 우선 검색
- slides.json은 반드시 IR 스키마를 준수한다
- spec_lock.md는 매 SVG 페이지 생성 전 재읽기 (LLM 컨텍스트 압축 drift 방지)
