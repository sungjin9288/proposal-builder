# Resume Bullets

## 1. 이력서용 프로젝트 제목 후보

1. 공공 AI 안전서비스 제안서 PPT 자동화 PoC
2. 디자인 보존형 PPT 변환 및 QA 워크플로 구축
3. 제안서 산출물 검증과 AI 학습 데이터 준비 자동화

## 2. 한 줄 소개 후보

1. 공공 AI 안전서비스 제안서 개정 과정을 Python 기반 PPTX/PDF 생성·검증 워크플로로 구조화한 프로젝트
2. 원본 PPT 템플릿을 보존하면서 문구, 레이아웃, 증빙 상태를 점검하는 문서 자동화 PoC
3. 제안서 산출물 QA와 editable PPT conversion evaluator 데이터 준비를 파일 기반으로 관리한 로컬 자동화 워크스페이스

## 3. 현재 이력서에 넣어도 되는 bullet

- 공공 AI 안전서비스 제안서 개정 요구를 `AGENTS.md`, `V3_REVISION_BRIEF.md`, YAML spec, QA 기준 문서로 구조화하고 산출물 검토 흐름을 정리
- Python 기반 PPTX/PDF 생성 스크립트와 QA 리포트 생성 흐름을 활용해 V3 제안서 산출물 생성·검증을 자동화
- `python-pptx`, `lxml`, `Pillow` 기반으로 슬라이드 텍스트 감사, 페이지 마커 보정, PPTX 구조 점검, PDF export 검토 흐름을 개발 중
- 디자인 보존형 PPT conversion 작업에서 PowerPoint 렌더 기준 검증, RMS 비교, forbidden-expression scan, editable text-layer 한계 기록을 수행
- `ai_training/` 워크스페이스를 구성해 planning documentation과 editable PPT conversion 데이터셋을 JSONL/CSV 기반으로 관리하고 readiness gate를 문서화
- 검토자 의사결정을 위해 evidence gap, fix readiness, QA checklist, handoff packet 등 산출물 리스크를 Markdown report로 정리

## 4. 구현 후 넣을 수 있는 bullet

- 구현 후 사용 가능: 표준 입력 패킷 업로드부터 PPTX/PDF 생성, QA, evidence gate, reviewer feedback 반영까지 하나의 CLI로 자동화
- 구현 후 사용 가능: editable PPT conversion evaluator를 실제 모델 평가 또는 보조 판단 워크플로에 연결
- 구현 후 사용 가능: 웹 UI를 통해 제안서 산출물 상태, evidence gate, render QA 결과를 대시보드로 제공

## 5. 기술스택 한 줄

- 현재 사용 중: Python, python-pptx, lxml, Pillow, YAML, Markdown, JSON, CSV, JSONL, PowerPoint PDF export 기반 QA
- 예정/검증 중: AI evaluator 학습 데이터 워크플로, 더 많은 real sample 기반 validation, reviewer approval pipeline

## 6. 지원 직무별 강조 포인트

### AI/IT 개발자

- Python 기반 파일 처리, PPTX 자동화, 검증 스크립트, 데이터셋 readiness gate 구현 경험

### AI 서비스 기획

- 공공 제안서 개정 요구를 사용자 흐름, 산출물, 검토 기준, 리스크 게이트로 구조화한 경험

### AI 솔루션 엔지니어

- 비정형 업무 산출물을 표준 입력, 자동 변환, QA 리포트, 검토자 승인 흐름으로 묶은 경험

### DX/AI 컨설팅 주니어

- 문서 업무의 반복 리스크를 식별하고 자동화 대상, 검증 기준, 보완 질문으로 전환한 경험

## 7. 쓰면 위험한 표현

- 주장 금지: 실제 모델 학습 완료
- 서비스 배포 완료
- 완전 자동 공공 제안서 생성 솔루션
- 공식 성과 수치 달성
- 모든 PPT 객체의 완전 native editability 확보

## 8. 보완 후 쓸 수 있는 표현

- 학습 데이터 기반 evaluator 검증 완료: 실제 학습 또는 평가 결과가 생긴 후 가능
- 배포형 문서 자동화 서비스: 웹 UI/API/인증/배포가 구현된 후 가능
- end-to-end 자동화: 표준 입력부터 reviewer feedback 반영까지 통합 CLI 또는 UI가 검증된 후 가능

## 9. 최종 판단

- 현재 이력서 반영 가능 여부: 조건부 가능
- 이유: 자동화 코드와 산출물 문서 근거가 풍부하지만, 제품형 서비스와 실제 AI 모델 완료로 표현하면 과장입니다.
- 이력서에 넣기 전 반드시 보완할 것: 실행 환경, 핵심 스크립트 사용법, 대표 before/after 이미지, 본인 기여 범위
- 가장 먼저 개선해야 할 것: 루트 README와 최소 재현 명령 정리
