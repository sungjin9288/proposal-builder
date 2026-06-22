# Development Roadmap

## 1. 현재 상태 요약

- 현재 구현 완료: V3 제안서 방향 문서화, PPT 산출물 일부, 디자인 보존 PPT conversion 검증, training readiness report
- 개발 중: V3 full review deck generation workflow, evidence gate 보완, editable PPT evaluator dry-run
- 미구현: 웹 UI, API 서버, 인증, DB, 배포, 실제 모델 학습 완료
- 검증 필요: 의존성 재현성, Windows PowerPoint render, 공식 증빙, 비용/KPI 전제, 본인 기여 범위

## 2. Phase 1 - MVP 완성

- 목표: 로컬에서 대표 입력 파일로 PPTX/PDF/QA report를 재현 가능하게 만들기
- 해야 할 작업: root README 초안 반영, requirements/pyproject 작성, 대표 CLI 명령 정리, sample input/output 최소화
- 완료 기준: 새 환경에서 핵심 스크립트 1~2개가 성공 실행되고 산출물 경로가 문서와 일치
- 산출물: README, requirements, smoke report, demo screenshot

## 3. Phase 2 - 기능 고도화

- 목표: 검토자 feedback과 evidence gate를 자동화 흐름에 더 명확히 연결
- 해야 할 작업: reviewer response template 정리, evidence register 자동 갱신, QA blocker summary 생성
- 완료 기준: reviewer input 파일을 넣으면 patch 후보와 blocked item이 자동 분류됨
- 산출물: reviewer workflow report, updated QA report, issue log

## 4. Phase 3 - 서비스화 / 배포

- 목표: 로컬 CLI 또는 간단한 웹 UI로 산출물 상태를 확인할 수 있게 만들기
- 해야 할 작업: CLI entrypoint 통합, config 파일 표준화, 필요 시 lightweight dashboard 구현
- 완료 기준: 사용자가 명령 하나로 검증 summary와 output package를 생성
- 산출물: CLI command, packaging script, optional dashboard

## 5. Phase 4 - 포트폴리오 완성

- 목표: 이력서/면접에서 설명 가능한 대표 사례로 정리
- 해야 할 작업: before/after 이미지, architecture diagram, 핵심 코드 설명, 기여 범위 정리
- 완료 기준: 1분 소개, 3분 설명, 기술 질문 답변, 데모 파일이 모두 준비됨
- 산출물: case study, screenshots, demo video or GIF, interview notes

## 6. 우선순위 높은 다음 작업 5개

| 우선순위 | 작업 | 이유 | 예상 산출물 |
|---|---|---|---|
| 1 | root README 또는 README draft 반영 | 실행 방법과 프로젝트 설명이 현재 부족 | README.md |
| 2 | 의존성 파일 작성 | 새 환경 재현성 확보 필요 | requirements.txt 또는 pyproject.toml |
| 3 | 핵심 스크립트 통합 entrypoint 정리 | 478개 스크립트 중 사용자가 무엇을 실행할지 불명확 | `scripts/run_project_smoke.py` 또는 Makefile |
| 4 | 대표 화면/산출물 스크린샷 추가 | 포트폴리오 검토자가 결과를 빠르게 이해 | screenshots/ |
| 5 | 본인 기여 범위 기록 | 면접에서 설명 가능한 범위 명확화 | `docs/contribution-notes.md` 또는 DEV_LOG 보강 |
