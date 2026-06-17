# Proposal Builder — 컨설팅 제안서 자동화

## 프로젝트 개요

공공기관 컨설팅 / AI 컨설팅 제안서·제정서 작성 자동화 도구.
산출물: PPTX, PDF, HWP. 모든 작업물의 구조화 JSON(IR)을 `archive/`에 누적하여
추후 DecisionDoc 프로젝트의 AI 학습 데이터로 활용한다.

## 워크플로우

1. `projects/[프로젝트명]/`에 RFP PDF 배치
2. `/rfp-analyzer` 스킬로 RFP 분석 → `prd.md` 초안 생성
3. 사용자가 `prd.md` 검토·수정
4. `/proposal-pptx` 스킬로 `prd.md` → `slides.json` (IR) → `output.pptx` + `output.pdf` 생성
5. HWP는 Windows 워커에서 별도 처리 (추후)
6. 완료 프로젝트는 `archive/`로 이동, `slides.json`을 `archive/slides.jsonl`에 append

## Plan-First 원칙

큰 변경(새 스킬 추가, IR 스키마 변경, 템플릿 구조 변경 등)은 반드시 사용자 승인을 받은 뒤 진행한다.
구현 전에 변경 범위와 영향을 먼저 설명하고, 사용자가 동의한 뒤 코드를 작성한다.

## 한국어 톤 가이드

- **격식체** 사용: 단정적 어미("~합니다", "~입니다"), 수동태 최소화
- 슬라이드 제목에 **결론을 노출**: 평가위원이 5초 안에 핵심을 파악할 수 있도록
- 표/도식 캡션: "무엇을 보여주는가"가 아니라 **"무엇을 의미하는가"**로 작성
- 불필요한 수식어 배제, 데이터와 근거 중심 서술

## 금지 사항

- RFP 원문을 그대로 복사하여 제안서에 붙여넣지 않는다
- 근거 없는 수치나 통계를 생성하지 않는다
- 경쟁사를 직접 비방하는 표현을 사용하지 않는다
- 비용 항목에 임의의 금액을 기재하지 않는다
- `archive/`의 기존 데이터를 삭제하거나 덮어쓰지 않는다 (append-only)
- baseline 표/카드의 한 셀만 덮는 단어 단위 패치 금지 (의미 단위 마스킹만 허용)

## 표지·Part Divider 페이지번호 금지 (영구 규칙)

표지와 모든 Part divider 슬라이드는 페이지번호 표시 금지.
SKILL의 PPTX 렌더링 단계에서 자동 적용 (페이지번호 박스 자체를 미생성).
본문 슬라이드는 페이지번호 유지.

## baseline 이미지 슬라이드 OCR 검증 필수

baseline 이미지가 사용된 슬라이드는 `tesseract <png> -l kor`로 자동 검증한다.
검사 토큰: `templates/qa/forbidden_tokens.txt` 전체.
결과는 `qa_report.md`에 슬라이드별 hits로 기록.
사람 눈검사 의존 금지.

## 의미 단위 마스킹

baseline 표/카드의 한 셀만 덮는 단어 단위 패치는 금지.
인접 셀의 평가 뉘앙스 텍스트가 baseline 픽셀에 남기 때문.
**최소 단위**: 표 전체 또는 카드 전체.

## 장식 자산 우선 검색

새 슬라이드 디자인 보강 시 `templates/decorations/`를 **우선 검색**한다.
- 자산 카탈로그: `templates/decorations/README.md`
- 매 자산은 PNG + 동명 `.meta.md` (출처/색상/권장 크기/사용처)
- 자산이 없으면 baseline에서 텍스트 없는 영역만 캡처 후 등록
- OCR 검증으로 텍스트 0% 보장

## 기준본 디자인 시스템 4축 (재사용 톤 판단 기준)

새 제안서 작업 시 발주처 기준본의 다음 4축을 추출해 분석한다.

- **헤더**: 풀폭 NAVY + 우상단 hexagon/네트워크 장식 (텍스트 없음)
- **카드**: 화이트 라운드 + 좌측 컬러 바, BORDER 라이트 그레이
- **포인트**: ORANGE는 우선순위/비용/핵심 판단에만 한정
- **밀도**: "한 화면에 결론이 보이는" 카드 밀도 — 빈 여백 ±15%

발주처 톤이 다르면 자산을 신규 캡처·합성하여 재사용 가능 형태로 등록한다.

## 발주처 특수 사항

프로젝트별 발주처 특수 사항은 `projects/[id]/client_notes.md`를 참조한다.
CLAUDE.md에는 일반화 규칙만 보관하며, 발주처 톤·금지표현·핵심 메시지 등은 client_notes에서 관리한다.

## PRD 스키마 (`prd.md` 상단 frontmatter)

```yaml
---
rfp:
  id: "project-id"
  client: "발주기관명"
  budget_krw: 0
  deadline: "YYYY-MM-DD"
  format_required: ["pptx", "pdf"]
strategy:
  win_themes: []
  competitor_gaps: []
  risks: []
sections:
  - id: "section-id"
    pages: 0
    must_include: []
    sources: []
    score_weight: 0
templates:
  pptx: "templates/default.pptx"
  hwp: "templates/default.hwp"
---
# 본문 초안 (마크다운)
```

## IR 스키마 (`slides.json`)

```json
{
  "project_id": "...",
  "slides": [
    {
      "id": "slide-01",
      "section": "1.사업개요",
      "rhetoric": "problem-statement | solution | evidence | conclusion",
      "elements": [
        {"type": "text", "role": "title|body|caption", "content": "..."},
        {"type": "chart", "data": {}, "purpose": "evidence"},
        {"type": "shape", "subtype": "...", "semantic": "..."}
      ]
    }
  ]
}
```

## 기술 스택

- **PPTX 생성**: python-pptx
- **PDF 생성**: pypdf 또는 weasyprint
- **HWP 생성**: pywin32 + 한컴 한글 COM (Windows 전용, 추후)

## 폴더 구조

```
proposal-builder/
├── CLAUDE.md              # 이 파일
├── .claude/skills/
│   ├── rfp-analyzer/      # RFP PDF → prd.md
│   ├── proposal-pptx/     # prd.md → slides.json + PPTX + PDF
│   └── proposal-hwp/      # prd.md → HWP (placeholder)
├── templates/             # PPTX/HWP 템플릿
├── projects/              # 진행 중 프로젝트
└── archive/               # 완료 프로젝트 + slides.jsonl
```

---

## README 정직성 규칙 (포트폴리오 공개용 — 반드시 준수)

이 repo의 README는 채용 담당자·외부 방문자가 본다. README를 생성·수정할 때 아래를 **절대 규칙**으로 지킨다. 규칙을 어기면 작업을 멈추고 보고한다.

### 금지

- **측정 근거를 한 줄로 댈 수 없는 수치는 쓰지 않는다.** (예: "99.8% 비용 절감", "94.2% 자동화", "정확도 95%", "요청당 €0.0005")
  - 숫자를 쓰려면 **어떻게 쟀는지**(측정 커맨드·로그·방법)를 같은 자리에 표기한다. 못 대면 **삭제**한다.
- **과장 표현 금지**: "production-ready", "enterprise", "상용 운영", "엔터프라이즈". 실제가 PoC/MVP면 그대로 표기한다.
- 코드에 **없는** 기능·엔드포인트·성과를 적지 않는다. 추측 금지.

### 필수

- **테스트 수는 실제 코드로 카운트**해서 적고, 카운트 커맨드를 함께 둔다.
  - 예: `grep -rE "def test_" tests | wc -l`, `grep -rE "\b(test|it)\(" --include="*.test.*" | wc -l`
  - "정의된 함수 수"와 "통과 수"를 구분한다. 실제로 돌리지 않았으면 **"정의 기준 카운트, pass 여부는 별도 확인"**으로 표기.
- **엔드포인트·환경변수·디렉터리 구조는 코드/`.env.example`에서 직접 추출**한다. 손으로 지어내지 않는다.
- **`## Scope & Limitations` 섹션을 반드시 둔다.** 미구현·미검증·외부 의존·범위 밖 항목을 명시한다.
- **Demo·운영 URL은 접근 검증된 것만 링크**한다. 미검증이면 "(접근 검증 필요)"로 표기한다.

### 표준 구조

제목 → 한 줄 소개 → Why I Built This → Features → Tech Stack → Architecture → Key Design Decisions → Getting Started → (API/Usage) → Testing → Scope & Limitations → Links

### 갱신 절차

1. README를 고치기 전에 위 규칙을 먼저 적용한다.
2. 수정 후 **측정 근거 없는 새 수치가 들어가지 않았는지** 스스로 검사한다 (`99.8`, `production-ready` 등 grep).
3. 큰 변경은 "어디를 왜 바꿨는지"를 커밋 메시지/PR에 남긴다.
