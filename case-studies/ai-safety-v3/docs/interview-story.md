# Interview Story

## 1. 1분 프로젝트 소개

이 프로젝트는 공공 AI 안전서비스 제안서 개정 과정에서 발생하는 PPT 템플릿 보존, 문구 검토, 증빙 상태 관리 문제를 해결하기 위해 시작했습니다.
저는 확인 필요 역할을 맡아 현재 코드 기준으로 Python 기반 PPTX/PDF 생성, 디자인 보존 PPT conversion 검증, AI training readiness report 흐름을 개발했습니다.
기술적으로는 Python, python-pptx, lxml, Pillow, YAML/JSON/CSV/JSONL 파일 처리를 사용했고, 현재는 로컬 자동화 MVP와 검토 게이트 문서화까지 구현했습니다.
개발 과정에서 PowerPoint 렌더링과 editability 사이의 차이가 있었고, 이를 PowerPoint PDF export 기준 QA와 lock status 문서로 관리했거나 관리 중입니다.
이 프로젝트를 통해 문서 자동화에서는 생성 로직뿐 아니라 검토 기준, evidence gate, reviewer handoff가 중요하다는 점을 얻었고, 향후에는 실행 환경 정리와 reviewer feedback 반영 자동화로 고도화할 계획입니다.

## 2. 3분 상세 설명

- 프로젝트 배경: V2 제안서 PPT를 V3 방향으로 개정하면서 원본 디자인을 유지하고, 금지 문구와 증빙 상태를 함께 검토해야 했습니다.
- 문제정의: PPT 수정, PDF 렌더, QA 문서, evidence 상태가 분산되어 있어 반복 작업과 오류 가능성이 컸습니다.
- 기술 선택 이유: 산출물이 PPTX/PDF/Markdown/CSV/JSONL 중심이므로 Python 파일 처리와 PPTX 라이브러리가 적합했습니다.
- 핵심 구현: `generate_v3_full_review_deck.py`, `run_visual_ppt_conversion.py`, `analyze_pptx_editability_inventory.py`, `validate_ai_training_workspace.py`, `check_ai_training_readiness.py`
- 현재 상태: 로컬 자동화와 문서화 중심 MVP이며, 배포형 서비스와 실제 모델 학습은 아직 아닙니다.
- 앞으로의 개선 방향: 의존성 파일 정리, 대표 CLI 통합, sample input 확충, reviewer feedback patch workflow 강화
- 컨설팅 경험과의 자연스러운 연결: 요구사항을 산출물 구조와 검증 게이트로 바꾸고, 검토자가 의사결정하기 쉬운 문서로 정리한 점

## 3. 기술 면접 예상 질문 10개

| 예상 질문 | 답변 방향 | 코드 근거 | 보완 필요 지식 |
|---|---|---|---|
| PPTX를 어떻게 자동 생성했나요? | python-pptx로 슬라이드 텍스트와 shape를 조작하고 QA 문서를 생성 | `scripts/generate_v3_full_review_deck.py` | python-pptx 객체 모델 |
| 렌더링 차이는 어떻게 검증했나요? | PowerPoint PDF export를 기준으로 보고 renderer-specific difference를 문서화 | `jobs/visual_ppt_conversion/README.md`, lock status | 이미지 diff/RMS 개념 |
| forbidden expression scan은 어떤 방식인가요? | PPTX 텍스트를 추출해 term scan을 수행 | `scan_terms`, `pptx_ordered_text` | XML text extraction |
| AI 학습은 완료됐나요? | 아니며 readiness gate상 training blocked 상태 | `ai_training_readiness_report.md` | ML dataset split 기준 |
| 데이터셋은 어떻게 관리되나요? | JSONL/CSV split과 row count, validity를 파일 기반으로 검증 | `check_ai_training_readiness.py` | JSONL validation |
| API 서버가 있나요? | 현재 확인된 API 서버는 없음 | manifest 부재 | FastAPI 등 추후 설계 |
| 테스트는 어떻게 하나요? | pytest보다 validate/check/smoke 스크립트 중심 | `scripts/validate_*`, `scripts/smoke_*` | 자동 테스트 체계화 |
| 의존성은 어떻게 재현하나요? | 현재 requirements 파일이 없어 보완 필요 | manifest 부재 | dependency pinning |
| 대용량 asset은 어떻게 관리하나요? | jobs/output/ai_training로 분리되어 있고 export package에는 포함하지 않음 | folder structure | artifact management |
| 보안상 주의점은 무엇인가요? | 민감정보와 내부자료를 zip에서 제외하고 API key 사용 근거는 없음 | export manifest | secret scanning |

## 4. 프로젝트 면접 예상 질문 10개

| 예상 질문 | 답변 방향 | 근거 | 보완 필요 사항 |
|---|---|---|---|
| 왜 이 프로젝트를 만들었나요? | 반복적인 제안서 개정과 QA를 자동화하기 위해 | `AGENTS.md`, `V3_REVISION_BRIEF.md` | 사용자 인터뷰 |
| 현재 완성도는 어느 정도인가요? | 로컬 자동화 MVP와 고도화 중 | readiness/report 문서 | 대표 데모 |
| 가장 큰 리스크는 무엇인가요? | 공식 증빙, 렌더링 검토, sample 부족 | `final_fix_readiness_report.md` | 외부 검토 |
| 산출물은 무엇인가요? | PPTX/PDF, QA report, training readiness report | `output/`, `ai_training/` | 포트폴리오용 스크린샷 |
| 사용자는 누구인가요? | 제안서 작성자, 검토자, 산출물 QA 담당자 | repo 목적 문서 | 실제 persona 정리 |
| 기존 방식과 차이는 무엇인가요? | 수작업 대조를 스크립트와 게이트로 전환 | scripts/reports | 정량 시간 절감 측정 |
| 왜 웹앱이 아닌 로컬 스크립트인가요? | 초기 문제는 산출물 재현성과 검증이 우선 | repo 구조 | UI roadmap |
| 본인 기여는 어디까지인가요? | 확인 필요로 답하고 코드/문서 근거 중심으로 설명 | 전체 파일 | 역할 명확화 |
| 다음 단계는 무엇인가요? | README, 의존성, 통합 CLI, sample 확충 | roadmap | 일정 수립 |
| 이력서에 어떻게 표현할 건가요? | PoC/개발 중으로 조건부 표현 | resume bullets | 과장 표현 제거 |

## 5. 컨설팅 경험과의 연결 질문 5개

| 예상 질문 | 답변 방향 | 주의할 점 |
|---|---|---|
| 컨설팅 경험이 개발에 어떻게 도움 됐나요? | 요구사항과 검토 리스크를 구조화하는 데 도움 | 특정 무관 도메인으로 억지 연결 금지 |
| 제안서 업무를 어떻게 자동화 대상으로 정의했나요? | 반복 대조, 문구 리스크, 산출물 검증을 기준으로 분해 | 완전 자동화라고 과장 금지 |
| 사용자 관점은 어떻게 반영했나요? | 검토자가 보는 readiness, blocker, next action을 문서화 | 실제 사용자 검증은 확인 필요 |
| 기대효과는 무엇인가요? | 검토 누락 감소와 재현성 향상 | 수치 임의 생성 금지 |
| 문서화 역량은 어디서 보이나요? | runbook, QA, manifest, revision log | 본인 작성 범위 확인 필요 |

## 6. 내가 추가로 공부해야 할 부분

- 기술: python-pptx 심화, PPTX OpenXML 구조
- 아키텍처: CLI 구조화, configuration management
- 보안: secret scanning, 민감자료 분리 정책
- 배포: Docker, CI, artifact release
- 테스트: pytest, golden file test, visual regression test
- AI/LLM: dataset split, evaluator design, human review loop
- CS 기초: 파일 I/O, XML parsing, hashing, image comparison
