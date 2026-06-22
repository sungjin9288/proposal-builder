# Project Card

## 1. Snapshot

- 프로젝트명: 공공 AI 안전서비스 제안서 V3 및 디자인 보존 PPT 자동화 워크스페이스
- 프로젝트 유형: 개인 / PoC
- 기간: 확인 필요
- 현재 상태: MVP 구현 및 고도화 중
- 내 역할: 확인 필요
- GitHub 링크: 추가 필요
- Demo 링크: 추가 필요
- 핵심 기술스택: Python 스크립트, python-pptx, lxml, Pillow, YAML/JSON/CSV/JSONL, PowerPoint PDF export 기반 QA
- 이력서 반영 가능 여부: 조건부 가능
- 판단 이유: 파일 기반 자동화, 산출물 검증, QA 문서, 학습 데이터 준비 게이트가 코드와 문서로 확인되지만, 배포형 서비스·사용자 UI·실제 모델 학습 완료 근거는 확인되지 않습니다.

## 2. One-liner

공공 제안서 작업자의 디자인 보존형 PPT 수정·검증 문제를 해결하기 위해 Python 기반 PPTX/PDF 생성, QA, 학습 데이터 준비 워크플로를 개발 중인 문서 자동화 PoC입니다.

## 3. Problem

- 이 프로젝트가 해결하려는 사용자 문제: 기존 제안서 PPT 템플릿을 유지하면서 V3 내용으로 개정하고, 디자인 손상·문구 리스크·근거 부족 상태를 반복 검증해야 하는 문제
- 기존 방식의 불편함 또는 한계: 수작업 PPT 수정은 페이지 수가 많을수록 레이아웃 편차, 문구 누락, 렌더러 차이, 증빙 상태 추적 누락이 발생하기 쉽습니다.
- 이 프로젝트에서 가장 중요한 문제정의: 제안서의 시각 템플릿을 보존하면서 내용 개정, PPTX/PDF 산출, QA, 근거 상태 관리, 학습 데이터 준비를 재현 가능한 파일 기반 워크플로로 만드는 것
- 컨설팅 경험과 자연스럽게 연결되는 부분:
  - 문제정의: 공공 제안서 요구사항을 산출물·검증 조건·차단 조건으로 분해
  - 요구사항 정리: `AGENTS.md`, `V3_REVISION_BRIEF.md`, `projects/ai_safety_v3/*.md`에 방향성과 제약 정리
  - 사용자 관점: 최종 검토자가 확인해야 할 파일, 게이트, 보완 질문을 분리
  - 문서화: QA 체크리스트, 준비 요약, readiness report, runbook 형태로 기록
  - 기대효과 정리: 반복 검증 가능한 제안서 개정·PPT 변환 워크플로 구축

## 4. Solution

- 제공하려는 핵심 기능: V2 제안서 기반 V3 개정, 디자인 보존형 PPT 변환, PPTX 구조/시각 검증, 산출물 QA, 학습 데이터 준비 상태 점검
- 현재 실제로 제공 가능한 기능:
  - V3 개정 방향과 슬라이드 사양 관리: `V3_REVISION_BRIEF.md`, `projects/ai_safety_v3/V3_FULL_REVIEW_DECK_SPEC.yaml`
  - PPTX/PDF 산출 스크립트: `scripts/generate_v3_full_review_deck.py`, `scripts/build_visual_ppt_from_pdf.py`, `scripts/run_visual_ppt_conversion.py`
  - PPTX editability 분석: `scripts/analyze_pptx_editability_inventory.py`
  - AI 학습 워크스페이스 검증: `scripts/validate_ai_training_workspace.py`, `scripts/check_ai_training_readiness.py`
  - 증빙·QA 산출물 기록: `output/*.md`, `ai_training/06_training_packages/central_readiness/*.md`
- 개발 중인 기능: 계획 문서화 AI 샘플 확충, editable PPT conversion evaluator dry-run 패키지 검토, Windows PowerPoint 검토 입력 반영
- 아직 할 수 없는 기능: 배포형 웹 서비스, 인증/사용자 관리, DB 기반 프로젝트 관리, 실제 모델 학습 완료(미구현), 자동 외부 제출
- 사용자 흐름: 원본 PDF/PPTX 입력 -> 스크립트 실행 -> PPTX/PDF 및 QA 리포트 생성 -> 검토 게이트 확인 -> 보완 요청 또는 내부 검토 패키지 전달
- AI/IT 기술을 적용한 방식: 현재는 모델 실행보다 학습 데이터 준비와 evaluator용 데이터셋 구성에 초점이 있으며, 실제 학습 실행은 repo 문서상 차단 상태입니다.

## 5. Tech Stack

| 영역 | 사용 기술 | 현재 사용 여부 | 근거 파일 |
|---|---|---|---|
| Language | Python | 사용 중 | `scripts/*.py` |
| Frontend | 없음 | 미구현 | 관련 app/frontend 디렉터리 없음 |
| Backend | 없음 | 미구현 | API 서버 엔드포인트 근거 없음 |
| AI/LLM | 학습 데이터/패키지 준비 워크플로 | 예정/검증 중 | `ai_training/README.md`, `ai_training/06_training_packages/central_readiness/ai_training_readiness_report.md` |
| Database | 파일 기반 JSON/CSV/JSONL/Markdown | 사용 중 | `ai_training/03_datasets/**`, `output/*.md` |
| Infra/Deploy | 없음 | 미구현 | Docker/compose/배포 설정 없음 |
| Tools | PowerPoint PDF export, python-pptx, lxml, Pillow, YAML | 사용 중 | `scripts/generate_v3_full_review_deck.py`, `jobs/visual_ppt_conversion/README.md` |
| Test | validation/smoke/check scripts | 사용 중 | `scripts/validate_*`, `scripts/smoke_*`, `scripts/check_*` |

## 6. Architecture

### 현재 아키텍처

```text
User / Reviewer
-> input/ 원본 PPTX/PDF
-> projects/ai_safety_v3/ 사양, 정책, runbook
-> scripts/ 생성/분석/검증 자동화
-> output/ 및 jobs/ 산출물, QA, 검토 리포트
-> ai_training/ 데이터셋, readiness gate, dry-run package
-> Reviewer decision / 보완 요청
```

### 목표 아키텍처

```text
User / Reviewer
-> 표준 입력 패킷
-> 자동 사양 검증
-> 디자인 보존 PPT 변환 및 QA
-> 근거/문구 리스크 게이트
-> 학습 데이터 큐 및 evaluator dry-run
-> 검토자 승인 후 산출물 전달
```

### 설명

- 주요 데이터 흐름: 입력 파일과 YAML/Markdown 사양을 Python 스크립트가 읽고 PPTX/PDF/QA Markdown/JSON/CSV 산출물로 변환합니다.
- 주요 모듈 구성: `scripts/`는 생성, 변환, 검증, smoke, 학습 패키지 준비 스크립트로 구성됩니다.
- API 구조: 확인된 HTTP API 엔드포인트 없음.
- AI/LLM 처리 흐름: 현재는 `ai_training/`에서 JSONL 데이터셋과 readiness gate를 관리하며, 실제 모델 학습은 차단 상태입니다.
- DB 또는 저장소 구조: DB 없이 파일 시스템 기반으로 입력, 샘플, 데이터셋, 검토 결과를 관리합니다.
- 인증/보안/환경변수 처리 방식: 인증 기능은 미구현이며, 외부 API 호출도 현재 산출 문서상 수행하지 않는 것으로 기록되어 있습니다.
- 배포 구조가 있다면 설명: 없음.
- 배포 구조가 아직 없다면 “미구현”으로 표시: 미구현.

## 7. My Contribution

- 직접 구현했다고 설명 가능한 기능: 확인 필요. 코드 근거 기준으로는 PPT 생성/변환/검증 스크립트와 학습 데이터 readiness 워크플로를 설명할 수 있습니다.
- 설계했다고 설명 가능한 구조: 확인 필요. 파일 기반 워크스페이스 구조와 게이트 기반 검토 구조를 설명할 수 있습니다.
- 문서화 또는 기획 측면 기여: `AGENTS.md`, `V3_REVISION_BRIEF.md`, `projects/ai_safety_v3/*`, `output/*_summary.md` 수준의 요구사항·QA·검토 문서화
- 문제 해결 또는 디버깅 사례: PowerPoint 렌더러 기준 QA, 디자인 보존과 editability 간 트레이드오프 관리
- 면접에서 코드 수준으로 설명해야 할 부분: `generate_v3_full_review_deck.py`, `run_visual_ppt_conversion.py`, `validate_ai_training_workspace.py`, `check_ai_training_readiness.py`

## 8. Current Status

| 구분 | 기능 | 상태 | 근거 파일 | 이력서 반영 가능 여부 |
|---|---|---|---|---|
| 구현 완료 | PPTX/PDF 생성 및 QA 자동화 일부 | 구현 완료 | `output/v3_proposal.pptx`, `output/v3_proposal.pdf`, `scripts/generate_v3_full_review_deck.py` | 조건부 가능 |
| 구현 완료 | 디자인 보존 editable text-layer PPT conversion job | 구현 완료 | `jobs/visual_ppt_conversion/README.md`, `002_final_lock_status.md` | 가능 |
| 개발 중 | V3 full review deck 31장 사양 및 실행 계획 | 개발 중 | `output/v3_full_review_deck_preparation_summary.md` | 조건부 가능 |
| 개발 중 | AI training readiness 및 evaluator dry-run | 개발 중 | `ai_training/README.md`, readiness report | 조건부 가능 |
| 미구현 | 웹 UI, API 서버, 인증, DB, 배포 | 미구현 | 관련 manifest 없음 | 보류 |
| 검증 필요 | Windows PowerPoint render, 공식 증빙, 비용/KPI 전제 | 검증 필요 | `output/final_fix_readiness_report.md` | 보류 |
| 문서상 존재, 코드 근거 없음 | 실제 모델 학습 완료 | 코드 근거 없음 | readiness report의 training blocked 상태 | 보류 |

## 9. Evidence

- 주요 코드 파일: `scripts/generate_v3_full_review_deck.py`, `scripts/run_visual_ppt_conversion.py`, `scripts/analyze_pptx_editability_inventory.py`, `scripts/validate_ai_training_workspace.py`, `scripts/check_ai_training_readiness.py`
- 주요 함수/클래스: `audit_pptx`, `scan_terms`, `write_qa`, `workspace_report`, `FeatureReadiness`, `DatasetFileStatus`
- 주요 API 엔드포인트: 없음
- 설정 파일: `projects/ai_safety_v3/V3_FULL_REVIEW_DECK_SPEC.yaml`, `projects/ai_safety_v3/V3_STYLE_GUIDE.md`
- 실행 파일: `scripts/*.py`
- 테스트 파일: 독립 테스트 프레임워크는 확인되지 않으며 `validate_*`, `check_*`, `smoke_*` 스크립트가 검증 역할을 합니다.
- README 또는 문서 근거: `ai_training/README.md`, `jobs/visual_ppt_conversion/README.md`, `input/visual_ppt_conversion/README.md`
- 실행 방법이 명확한지: 일부 워크플로는 README에 명확하지만 의존성 설치 파일은 확인되지 않아 재현성 보완 필요
- 스크린샷/데모가 필요한 부분: 생성 PPT/PDF 화면, QA 리포트, training readiness report, 변환 전후 비교 이미지

## 10. Consulting Angle

| 프로젝트 요소 | 연결되는 컨설팅 역량 | 이력서/면접 표현 | 근거 |
|---|---|---|---|
| 제안서 V3 요구사항 정리 | 문제정의, 요구사항 구조화 | 공공 제안서 개정 요구를 슬라이드 사양과 검증 게이트로 구조화 | `AGENTS.md`, `V3_REVISION_BRIEF.md` |
| QA/게이트 문서 | 리스크 관리, 검토 프로세스 설계 | 산출물 검토 기준과 blocker/high risk 항목을 분리해 관리 | `output/final_fix_readiness_report.md` |
| AI training workspace | 데이터 검토, 품질 기준 설계 | 학습 실행 전 데이터셋 수량·유효성·다양성 게이트를 설계/운영 | `ai_training/README.md` |
| PPT 변환 워크플로 | 업무 자동화, 산출물 품질관리 | 디자인 보존과 편집 가능성의 균형을 검증 가능한 워크플로로 구현 | `jobs/visual_ppt_conversion/README.md` |

## 11. Safe vs Risky Expressions

### 써도 되는 표현

- Python 기반 공공 제안서 PPT 자동화 PoC
- 디자인 보존형 PPT 변환 및 QA 워크플로 개발 중
- 파일 기반 학습 데이터 readiness gate 구축
- PowerPoint 렌더 기준 검증 리포트 작성

### 조건부로 가능한 표현

- AI 학습 데이터셋 구축: 실제 학습 완료가 아니라 준비·검토 단계임을 함께 표시할 때 가능
- PPT 자동 생성: 일부 산출물이 존재하지만 검토/승인 게이트 상태를 함께 표시할 때 가능
- 공공 제안서 자동화: 특정 프로젝트 범위의 PoC임을 명확히 할 때 가능

### 쓰면 위험한 표현

- 주장 금지: 실제 모델 학습 완료
- 상용 서비스 배포 완료
- 완전 자동 제안서 생성 제품
- 공식 성과 수치 달성
- 모든 PPT 요소가 완전 native editable

### 위험한 이유

- repo 문서상 학습 실행은 차단 상태입니다.
- 배포 설정, 사용자 UI, API 서버, 인증/DB 근거가 없습니다.
- 최종 제출 전 확인해야 할 렌더링, 증빙, 비용/KPI 전제가 남아 있습니다.
- 일부 PPT 변환 결과는 디자인 보존을 위해 이미지 표면과 editable text-layer를 함께 쓰는 방식입니다.
