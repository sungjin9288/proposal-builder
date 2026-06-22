# Case Study

## 1. 배경

- 이 프로젝트를 시작한 배경: 기존 공공 AI 안전서비스 제안서 V2를 V3 방향으로 개정하면서 원본 PPT 템플릿의 시각 톤을 보존해야 했습니다.
- 해결하려는 사용자 문제: 제안서 담당자가 반복적인 PPT 수정, 금지 문구 검토, 증빙 상태 확인, 렌더링 차이를 수작업으로 관리해야 하는 문제
- 이 문제가 중요한 이유: 공공 제안서는 문구, 근거, 서식, 검토 이력이 모두 중요하며 하나라도 누락되면 제출 품질이 떨어질 수 있습니다.
- 현재 개발 진행 상태: PPT/문서 자동화 MVP와 검증 스크립트가 존재하고, 학습 데이터 준비 워크스페이스는 일부 ready 상태이나 실제 모델 학습은 차단 상태입니다.

## 2. 문제 정의

### As-Is

- 현재 사용자는 어떤 방식으로 문제를 해결하고 있는가? PPT 파일, PDF 렌더, 검토 문서, 증빙표를 수작업으로 대조합니다.
- 기존 방식의 한계는 무엇인가? 슬라이드 수가 늘어날수록 문구 누락, 레이아웃 손상, 증빙 상태 혼선, 검토 이력 분산이 발생합니다.

### Pain Points

- 불편 1: 원본 템플릿을 유지한 채 텍스트와 구조를 바꾸는 작업이 반복적입니다.
- 불편 2: PPTX, PDF, 렌더 이미지, QA 리포트를 별도로 대조해야 합니다.
- 불편 3: 공식 증빙이 필요한 문구와 임시 산정 문구를 명확히 분리해야 합니다.

## 3. 목표

### MVP 목표

- V3 개정 사양과 산출물 생성/검증 흐름을 파일 기반으로 재현 가능하게 만들기

### 기술 목표

- Python으로 PPTX/PDF 산출, slide text audit, QA report, training readiness report를 자동화하기

### 사용자 목표

- 검토자가 현재 산출물의 상태, 남은 리스크, 다음 확인 질문을 빠르게 판단할 수 있게 만들기

### 학습 목표

- 문서 자동화, PPTX 구조 분석, QA 자동화, JSONL 기반 학습 데이터 준비 과정을 경험하기

## 4. 해결 접근

- 어떤 기능으로 문제를 해결하려 했는가? 슬라이드 사양 YAML, PPT 생성 스크립트, 변환 스크립트, QA 스크립트, readiness gate 문서를 조합했습니다.
- AI/IT 기술을 어디에 적용했는가? 실제 모델 실행보다 training-ready 데이터 구조, evaluator dry-run 준비, 자동 검증 리포트에 적용했습니다.
- 왜 이 기술스택을 선택했는가? 기존 산출물이 PPTX/PDF/Markdown/CSV/JSONL 중심이어서 Python 파일 처리와 문서 자동화가 가장 직접적입니다.
- 현재 구현된 접근과 향후 목표 접근:
  - 현재: 로컬 스크립트 기반 산출물 생성과 QA
  - 목표: 표준 입력 패킷, 검토자 승인 게이트, 학습 데이터 확충, 반복 가능한 변환 평가 체계

## 5. 구현 범위

### 구현 완료

- V3 개정 방향 문서화
- PPTX/PDF 산출물 생성 일부
- 디자인 보존 PPT conversion job lock 및 검증 기록
- AI training workspace readiness report 생성
- 여러 검증/스모크 스크립트 보유

### 개발 중

- V3 full review deck 31장 사양 기반 generation workflow
- planning documentation sample 확충
- editable PPT conversion evaluator dry-run package 검토

### 미구현 / 예정

- 웹 UI
- API 서버
- 사용자 인증
- DB 저장소
- 배포 자동화
- 미구현: 실제 모델 학습 완료

### 이번 MVP에서 제외한 범위

- 제외한 기능: 외부 서비스 배포, 자동 제출, 실제 모델 학습 실행
- 제외한 이유: repo 문서상 human review, evidence confirmation, training approval gate가 선행되어야 합니다.

## 6. 시스템 설계

- 전체 구조: `input/` -> `projects/ai_safety_v3/` -> `scripts/` -> `output/`, `jobs/`, `ai_training/`
- 데이터 흐름: 원본 파일과 사양 파일을 읽어 PPTX/PDF/Markdown/JSON/CSV/JSONL 산출물을 생성합니다.
- API 구조: 확인된 API 서버 없음.
- AI/LLM 처리 흐름이 있다면 설명: 학습 데이터셋과 evaluator용 row/preference pair를 준비하지만 actual training은 금지 상태입니다.
- 예외 처리: 스크립트별 validation/check/smoke report로 입력 누락, ambiguous input, approval gate, evidence gap을 기록합니다.
- 보안/환경변수 처리: API key 사용 근거는 확인되지 않았고, export package는 문서 중심으로 구성했습니다.
- 배포 계획: 미구현.

## 7. 나의 역할

- 기획: 확인 필요
- 요구사항 정의: 확인 필요
- 프론트엔드: 해당 없음
- 백엔드: 해당 없음
- AI/LLM: 학습 데이터 준비 워크플로 수준에서 설명 가능
- 데이터 처리: JSON/CSV/JSONL/Markdown 파일 기반 검증 흐름 설명 가능
- 배포: 미구현
- 문서화: 확인 필요

## 8. 결과

- 구현 완료 기능: PPT 산출물 생성/검증 일부, 디자인 보존 PPT conversion job, readiness gate 리포트
- 로컬 실행 가능 여부: 일부 README에 Python 실행 명령이 있음. 전체 재현은 의존성 파일 부재로 추가 확인 필요
- 테스트 여부: 검증/스모크 스크립트와 기존 report가 있음
- 배포 여부: 미배포
- 사용자 피드백: 확인 필요
- 수치 성과: 현재 없음. 임의 생성 금지

## 9. 배운 점

- 기술적으로 배운 점: PPTX 구조, PDF 렌더 차이, 파일 기반 QA 자동화, JSONL 데이터셋 검증
- 설계에서 배운 점: 산출물 자동화는 생성보다 검토 게이트와 evidence 상태 관리가 중요합니다.
- 사용자 관점에서 배운 점: 최종 사용자는 코드보다 현재 상태, 남은 리스크, 확인 질문을 먼저 봅니다.
- 다음 프로젝트에 반영할 점: 의존성 파일, 실행 가이드, 샘플 입력, 최소 CLI 사용법을 초기에 정리해야 합니다.

## 10. 이 프로젝트가 보여주는 역량

- 개발 역량: Python 파일 처리, PPTX/PDF 자동화, 검증 스크립트 작성
- 문제정의 역량: 공공 제안서 개정 과업을 슬라이드 사양과 게이트로 분해
- 데이터/AI 활용 역량: 학습 데이터 준비, row validation, readiness threshold 관리
- 커뮤니케이션/문서화 역량: runbook, QA report, handoff packet 작성
- 컨설팅형 사고: 요구사항, 검토 리스크, 증빙 상태, 산출물 품질을 구조화
