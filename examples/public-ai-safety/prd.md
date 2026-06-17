---
rfp:
  id: "public-ai-safety-demo"
  client: "공개 샘플 기관"
  budget_krw: 0
  deadline: "확인 필요"
  format_required: ["pptx"]
strategy:
  win_themes:
    - "반복 문서 작업을 구조화된 워크플로로 전환"
    - "자동화 결과를 사람 검토 게이트로 통제"
    - "민감자료와 공개용 산출물을 분리"
  competitor_gaps:
    - "수작업 중심 문서 작성은 검토 누락 위험이 큼"
  risks:
    - "원본 자료와 공개 패키지의 분리 필요"
sections:
  - id: "problem"
    pages: 1
    must_include: ["문제정의", "반복 작업", "검토 누락"]
    sources: ["공개 샘플"]
    score_weight: 0
  - id: "workflow"
    pages: 1
    must_include: ["입력", "구조화", "산출", "QA"]
    sources: ["공개 샘플"]
    score_weight: 0
  - id: "verification"
    pages: 1
    must_include: ["금지어 검사", "산출물 기록", "검토 게이트"]
    sources: ["공개 샘플"]
    score_weight: 0
templates:
  pptx: "templates/proposal_template"
  hwp: "미구현"
---

# 공공 문서 자동화 데모

## Problem

반복적인 발표자료 작성과 검토 작업은 담당자 숙련도에 따라 품질 편차가 커질 수 있습니다.
이 데모는 원본 자료와 공개 산출물을 분리하고, 구조화된 중간 표현과 QA 리포트를 남기는 흐름을 보여줍니다.

## Workflow

입력 문서를 PRD로 정리한 뒤, 슬라이드 IR인 `slides.json`으로 변환하고, 다시 PPTX 산출물과 QA 리포트를 생성합니다.
자동화 결과는 최종 확정이 아니라 검토자가 확인할 수 있는 초안 산출물로 취급합니다.

## Verification

QA 단계에서는 금지어 토큰, 슬라이드 수, 텍스트 도형 수, 파일 생성 여부를 확인합니다.
통과하지 못한 항목은 완료 기능이 아니라 보완 필요 항목으로 남깁니다.
