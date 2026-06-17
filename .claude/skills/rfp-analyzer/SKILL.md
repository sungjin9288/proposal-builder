# RFP Analyzer

RFP(제안요청서) PDF를 분석하여 `prd.md` 초안을 생성하는 스킬.

## 입력

- `projects/[프로젝트명]/rfp.pdf` — 발주기관의 제안요청서 PDF

## 출력

- `projects/[프로젝트명]/prd.md` — PRD 초안 (frontmatter + 본문 마크다운)

## 실행 절차

1. RFP PDF를 읽고 핵심 정보를 추출한다:
   - 사업명, 발주기관, 예산, 납기
   - 제출 형식 요구사항 (PPTX, PDF, HWP 등)
   - 평가 기준 및 배점표
   - 필수 포함 항목
   - 기술적 요구사항

2. 추출한 정보를 PRD frontmatter 스키마에 맞게 구조화한다:
   ```yaml
   ---
   rfp:
     id: "프로젝트 ID (폴더명 기반)"
     client: "발주기관명"
     budget_krw: 예산(원)
     deadline: "YYYY-MM-DD"
     format_required: ["pptx", "pdf"]
   strategy:
     win_themes: ["핵심 차별화 포인트"]
     competitor_gaps: ["경쟁사 약점 추정"]
     risks: ["리스크 요인"]
   sections:
     - id: "section-id"
       pages: 예상 페이지 수
       must_include: ["필수 포함 항목"]
       sources: ["근거 자료"]
       score_weight: 배점 비중
   templates:
     pptx: "templates/default.pptx"
     hwp: "templates/default.hwp"
   ---
   ```

3. 본문 마크다운 초안을 작성한다:
   - 각 섹션별 개요와 핵심 메시지
   - 평가위원 관점에서의 득점 포인트 표시
   - 추가 조사가 필요한 부분에 `<!-- TODO: ... -->` 마커 삽입

## 한국어 톤

- 격식체, 단정적 어미
- 평가 기준 분석 시 원문 인용은 최소화하고 핵심 요약 중심
- 전략 제안은 근거 기반으로 작성

## 주의사항

- RFP 원문을 그대로 복사하지 않는다
- 근거 없는 수치를 생성하지 않는다
- 예산 항목에 임의 금액을 기재하지 않는다
- 확인이 필요한 사항은 TODO로 명시한다
