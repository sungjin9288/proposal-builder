# Proposal Builder

> 공공·컨설팅 제안서와 발표자료(PPTX/PDF/HWP) 작성을 **RFP 분석 → PRD → 슬라이드 IR → 산출물 → QA**의 재현 가능한 워크플로로 자동화하는 로컬 워크스페이스.

LLM 스킬과 템플릿, OCR 기반 QA를 결합해 "문서 품질을 작성자 숙련도가 아니라 구조로" 만드는 데 초점을 둔 도구입니다.

> ⚠️ 상태: **PoC / 외부 공개용 경량 버전**. 실제 발주처 제안서 원본·클라이언트 자료는 이 저장소에 포함되지 않습니다([Scope & Limitations](#scope--limitations) 참고). 운영 SaaS가 아니며, 검증되지 않은 성과 수치는 사용하지 않습니다.

처음 검토하는 경우 [`START_HERE.md`](./START_HERE.md)부터 보면 됩니다.

---

## Why I Built This

컨설팅·공공 제안 업무를 직접 하면서 제안서·발표자료의 반복 형식 작업이 시간을 잡아먹고, 품질이 작성자마다 달라지는 문제를 겪었습니다. 도메인(공공·컨설팅)을 아는 사람이 만들었기에 **어디까지 자동화하고 어디부터 사람이 검토해야 하는지**를 구분해 설계할 수 있었습니다.

핵심 문제는 **문서 작성 업무를 수작업이 아니라 재현 가능한 workflow로 관리하는 것**입니다.

---

## Features

| Feature | 설명 |
|---------|------|
| RFP 분석 (`rfp-analyzer`) | RFP 문서 → `prd.md` 초안 (요구사항·평가배점·win theme 구조화) |
| 슬라이드 생성 (`proposal-pptx`) | `prd.md` → `slides.json`(IR) → `output.pptx` + `output.pdf` |
| HWP 생성 (`proposal-hwp`) | `prd.md` → HWP (한컴 COM, Windows 워커 — placeholder) |
| 디자인 자산 카탈로그 | `templates/decorations/` — PNG + `.meta.md`(출처·색상·권장 크기) |
| OCR 기반 QA | baseline 이미지 슬라이드를 `tesseract -l kor`로 검사, `forbidden_tokens.txt` 토큰 hit 0% 보장 |
| editability / QA 리포트 | 자동 변환이 PPT 디자인을 깨뜨렸는지 before/after·blocker로 검토 게이트화 |

---

## Portfolio Case Study

이 저장소는 프레임워크와 합성 공개 샘플뿐 아니라, 공개 가능한 구현 증거를 `case-studies/` 아래에 분리해 둡니다.

빠른 포트폴리오 요약은 [`PORTFOLIO.md`](./PORTFOLIO.md), 리뷰 순서는 [`docs/reviewer-guide.md`](./docs/reviewer-guide.md), 주장별 증거는 [`docs/claims-matrix.md`](./docs/claims-matrix.md), 검증 요약은 [`docs/verification-summary.md`](./docs/verification-summary.md), 외부자료 경계는 [`docs/third-party-notices.md`](./docs/third-party-notices.md), 공개 릴리스 범위는 [`docs/release-note.md`](./docs/release-note.md)에 정리했습니다.

| Case Study | 설명 | 상태 |
|---|---|---|
| [`case-studies/ai-safety-v3`](./case-studies/ai-safety-v3/README.md) | 공공 AI 보행자 안전서비스 제안서 V3 작업을 대상으로 PPTX 구조 검사, visual PPT 입력 검증, revision/fix readiness gate, AI training readiness gate를 수집한 사례 | evidence 수집 완료, 모델 학습·외부 제출은 미완료 |

병합 기준과 제외 범위는 [`docs/portfolio-merge-map.md`](./docs/portfolio-merge-map.md)에 정리했습니다.

---

## Tech Stack

| Area | Stack |
|------|-------|
| Automation | Python, python-pptx |
| Document Processing | lxml, Pillow |
| OCR QA | tesseract (kor) |
| Data / Config | YAML, Markdown, JSON, JSONL |
| Output | PPTX, PDF, (HWP — Windows) |
| Skill Runtime | Claude skills (`rfp-analyzer`, `proposal-pptx`, `proposal-hwp`) |

---

## Architecture

```text
RFP 문서
 → [rfp-analyzer]  → prd.md (요구사항·배점·win theme)
 → 사용자 검토·수정
 → [proposal-pptx] → slides.json (IR) → output.pptx + output.pdf
 → OCR / editability QA → qa_report.md (forbidden token hits, blocker)
 → (HWP는 Windows 워커에서 별도 처리)
```

설계 핵심: `input → template → output`을 분리해 **같은 입력이면 같은 결과**가 나오도록 하고, 자동화의 한계(디자인 깨짐)는 QA 리포트로 검토 게이트를 남김.

저장소 구조:

```text
proposal-builder/
 → .claude/skills/        # 재사용 워크플로 스킬 (rfp-analyzer / proposal-pptx / proposal-hwp)
 → templates/             # 재사용 디자인·QA 자산 (decorations / qa / proposal_template)
 → examples/              # 합성 공개 샘플 (public-ai-safety)
 → case-studies/          # 정제된 구현 증거
 → docs/                  # 포트폴리오 검토·검증 문서
 → projects/  · archive/  # 작업물·완료 IR (비공개, .gitignore 처리)
```

---

## Key Design Decisions

- **재현 가능한 workflow로 만든 이유** — 제안서를 매번 처음부터 만들면 시간·품질이 사람에 종속된다. input/template/output을 분리해 결정론적으로 구성.
- **자동화와 사람 검토를 분리한 이유** — 자동 PPT 변환은 디자인을 깨뜨릴 수 있다. 무조건 자동화 대신 editability·QA 리포트로 검토 게이트를 남겨 자동화의 한계를 설계에 명시.
- **OCR 검증을 강제한 이유** — baseline 이미지에 평가위원 대상 금지 표현이 남는 사고를 사람 눈검사로는 못 잡는다. `tesseract` + `forbidden_tokens.txt`로 기계 검증.
- **발주처 특수 사항을 코드에서 분리** — 일반 규칙은 `CLAUDE.md`, 발주처별 톤·금지표현은 프로젝트별 `client_notes.md`로 분리(공개 저장소에는 미포함).

---

## Getting Started

```bash
# 1. 의존성
pip install -r requirements.txt
# OCR QA를 쓰려면 tesseract(한국어 데이터 포함) 설치 필요

# 2. 새 프로젝트 디렉터리 생성 후 RFP 배치
mkdir -p projects/<project-id>
#   projects/<project-id>/ 에 RFP 문서 배치  (projects/ 는 .gitignore 처리됨)

# 3. 스킬 워크플로 (Claude skills)
#   /rfp-analyzer   → prd.md 초안
#   /proposal-pptx  → slides.json + output.pptx + output.pdf
```

### 공개 데모 (민감자료 없음)

`examples/public-ai-safety/prd.md`(합성 샘플)만 사용하는 공개 데모를 제공합니다. 외부 API·비공개 자료·모델 학습을 실행하지 않습니다.

```bash
make demo       # 공개 샘플 → slides.json / output.pptx / qa_report.md (금지어·슬라이드 수 점검)
make check      # demo / preview / test / docs link / case-study / package verify 검증
```

---

## Testing / Verification

이 워크스페이스는 단위 테스트 대신 **산출물 검증(QA) 게이트**로 품질을 보장합니다.

- **공개 데모 QA**: `make demo`로 공개 PRD 샘플에서 산출물을 생성하고 금지어/슬라이드 수/파일 생성 여부를 점검.
- **공개 미리보기**: `make preview`로 공개 샘플 slide IR 기반 SVG contact sheet를 생성합니다.
- **학습 데이터 준비·검증**: `make learn`과 `make validate-learning`으로 slide-level JSONL과 split/report를 생성·검증합니다. 실제 모델 학습은 수행하지 않습니다.
- **회귀 테스트**: `make test`로 공개 샘플 데모, 학습 데이터 split, 케이스스터디 상태 검증이 계속 통과하는지 확인합니다.
- **문서·케이스스터디 검증**: `make docs-check`와 `make case-study`로 로컬 Markdown 링크와 정제된 evidence 경계를 점검합니다.
- **릴리즈·패키지 검증**: `make release-check`, `make package-smoke`, `make final-check`로 공개 zip 포함/제외 규칙과 재현성을 확인합니다.
- **OCR forbidden-token 검사**: baseline 이미지 슬라이드를 `tesseract <png> -l kor`로 추출, `templates/qa/forbidden_tokens.txt` 토큰 hit를 `qa_report.md`에 기록 (사람 눈검사 의존 금지).
- **editability 리포트**: 자동 변환 후 텍스트/도형 편집 가능성 점검.
- **의미 단위 마스킹 규칙**: baseline 표/카드는 셀 단위가 아니라 표·카드 전체 단위로만 교체.

---

## Scope & Limitations

- **클라이언트 자료 미포함**: 실제 발주처 제안서 원본, `client_notes.md`, 완료 산출물(`projects/`, `archive/`)은 공개 저장소에서 제외됩니다(`.gitignore` 처리). 이 저장소는 **프레임워크(스킬·템플릿·QA) + 합성 공개 샘플 + 정제된 case-study evidence만** 담은 경량 공개판입니다.
- **Case study는 정제본만 포함**: `case-studies/`에는 원본 PPTX/PDF, 회사자료, 내부 메모가 아니라 Markdown evidence, CLI log, generated report, architecture diagram만 포함합니다.
- **Public demo output은 로컬 생성물**: `_demo_output/`은 실행 확인용이며 공개 패키지에는 포함하지 않습니다.
- 상용 제안서 자동화 **SaaS가 아닙니다.** 웹 UI·API 서버·인증·DB·배포는 포함하지 않습니다.
- HWP 생성은 한컴 COM 의존으로 **Windows 전용 / placeholder** 단계입니다.
- `vendor/ppt-master/`는 외부 오픈소스(별도 라이선스)로, 저장소에 포함하지 않고 필요 시 재클론합니다.
- 실제 모델 학습 완료·운영 KPI를 주장하지 않습니다.

---

## Links

- GitHub: (private 생성 후 추가)
- 빌드 규칙 상세: [`CLAUDE.md`](./CLAUDE.md)
