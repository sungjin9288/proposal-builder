# README Improvement Plan

## 1. 현재 README의 문제점

- 루트 `README.md`가 없어 프로젝트 진입점과 실행 방법이 즉시 보이지 않습니다.
- Python 의존성 파일이 없어 새 환경에서 재현하기 어렵습니다.
- 스크립트 수가 많지만 대표 workflow command가 정리되어 있지 않습니다.
- 구현 완료, 개발 중, 검증 필요 상태가 산출물별로 분산되어 있습니다.
- 포트폴리오 관점에서 사용 대상, 문제, 결과, 제한사항이 한 문서에 모여 있지 않습니다.

## 2. README에 추가해야 할 섹션

# 프로젝트명

## 1. 프로젝트 개요

- 공공 AI 안전서비스 제안서 V3 개정과 디자인 보존 PPT 변환/QA를 위한 로컬 자동화 워크스페이스입니다.

## 2. 개발 배경

- 기존 PPT 템플릿 보존, 문구 리스크 검토, 근거 상태 관리, PowerPoint 렌더 검증을 반복 가능하게 만들기 위해 시작했습니다.

## 3. 주요 기능

- 구현 완료
  - V3 제안서 방향과 슬라이드 사양 문서화
  - PPTX/PDF 산출물 생성 일부
  - 디자인 보존 PPT conversion job 검증 기록
  - AI training readiness report 생성
- 개발 중
  - V3 full review deck generation workflow
  - evaluator dry-run package 검토
  - evidence/reviewer feedback gate 보완
- 향후 개선
  - 통합 CLI
  - 재현 가능한 dependency setup
  - 웹 UI 또는 dashboard

## 4. 기술 스택

- Python
- python-pptx
- lxml
- Pillow
- YAML/Markdown/JSON/CSV/JSONL
- Microsoft PowerPoint PDF export 기반 visual QA

## 5. 시스템 구조

```text
input/
-> projects/ai_safety_v3/
-> scripts/
-> output/
-> jobs/visual_ppt_conversion/
-> ai_training/
```

## 6. 핵심 구현 내용

- `scripts/generate_v3_full_review_deck.py`: V3 full review deck 생성과 QA 보조
- `scripts/run_visual_ppt_conversion.py`: visual PPT conversion workflow runner
- `scripts/analyze_pptx_editability_inventory.py`: PPTX 구조와 media/editability inventory 분석
- `scripts/validate_ai_training_workspace.py`: AI training workspace 상태 검증
- `scripts/check_ai_training_readiness.py`: dataset split, row count, gate 상태 확인

## 7. 실행 방법

```bash
python3 scripts/validate_ai_training_workspace.py
python3 scripts/check_ai_training_readiness.py
python3 scripts/run_visual_ppt_conversion.py
```

주의: 현재 repo에는 의존성 파일이 확인되지 않아 새 환경에서는 패키지 설치 목록을 먼저 정리해야 합니다.

## 8. 환경변수

- 현재 확인된 필수 환경변수 없음
- 실제 외부 API key 사용 근거 없음
- 민감정보 파일은 repo 및 export package에 포함하지 않아야 함

## 9. 화면 예시

- 추가 필요: PPT before/after contact sheet
- 추가 필요: QA report screenshot
- 추가 필요: training readiness report screenshot

## 10. 개발 과정에서 해결한 문제

- PowerPoint와 다른 renderer 간 시각 차이를 PowerPoint PDF export 기준으로 관리
- 디자인 보존과 native editability 사이의 tradeoff를 lock status와 limitation으로 명확히 기록
- 학습 데이터 준비 상태를 row count, split, blocker 기준으로 정리

## 11. 비즈니스/사용자 관점의 적용 가능성

- 제안서, 보고서, PPT 산출물의 반복 검토를 자동화하는 내부 생산성 도구로 확장 가능
- 공공 문서 작업에서 요구되는 근거 상태, 문구 리스크, 산출물 검증 흐름을 구조화할 수 있음

## 12. 향후 개선 계획

- dependency pinning
- 대표 workflow CLI 통합
- reviewer feedback 자동 반영
- sample diversity 확충
- 포트폴리오용 demo package 작성

## 3. README 초안

# 공공 AI 안전서비스 제안서 PPT 자동화 워크스페이스

이 저장소는 공공 AI 안전서비스 제안서 V3 개정, 디자인 보존형 PPT 변환, QA 리포트 작성, AI 학습 데이터 준비 상태 점검을 위한 로컬 자동화 워크스페이스입니다.

## 현재 상태

- V3 제안서 개정 방향과 슬라이드 사양이 문서화되어 있습니다.
- Python 스크립트로 PPTX/PDF 생성, PPTX 구조 분석, QA 리포트, training readiness report를 생성합니다.
- 디자인 보존형 PPT conversion 작업은 PowerPoint 기준 검증 기록이 있습니다.
- 실제 모델 학습과 서비스 배포는 아직 완료되지 않았습니다.

## 주요 폴더

| 경로 | 설명 |
|---|---|
| `input/` | 원본 PPTX/PDF 입력 |
| `projects/ai_safety_v3/` | V3 제안서 사양, 스타일, QA 기준 |
| `scripts/` | 생성, 변환, 검증, smoke 자동화 스크립트 |
| `output/` | 제안서 산출물과 QA/검토 리포트 |
| `jobs/visual_ppt_conversion/` | 디자인 보존 PPT conversion job 기록 |
| `ai_training/` | 학습 데이터셋, readiness gate, dry-run package 준비 |

## 대표 명령

```bash
python3 scripts/validate_ai_training_workspace.py
python3 scripts/check_ai_training_readiness.py
```

visual PPT conversion 입력 파일이 준비된 경우:

```bash
python3 scripts/run_visual_ppt_conversion.py
```

## 제한사항

- 루트 dependency 파일이 아직 없습니다.
- 웹 UI, API 서버, 인증, DB, 배포는 미구현입니다.
- 실제 모델 학습은 repo 문서상 차단 상태입니다.
- 공식 증빙, 비용/KPI 전제, Windows PowerPoint 검토 등은 추가 확인이 필요합니다.
