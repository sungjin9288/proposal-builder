# Proposal Template (v1) — 한국 공공기관 제안서/제안서 표준 템플릿

> 001-dw_ai 프로젝트 v8 결과를 기반으로 추출한 재사용 가능 템플릿.
> 다음 제안서 작업 시 본 템플릿을 복사·수정해서 즉시 시작.

## 사용법

```bash
# 1. 새 프로젝트 디렉토리 생성
cp -R templates/proposal_template projects/002-NEW_PROJECT
cd projects/002-NEW_PROJECT

# 2. 발주처 변수 변경
edit data/spec_lock.yaml      # 색·폰트·레이아웃 (보통 그대로)
edit data/client_notes.md     # 발주처 톤·금지표현·핵심 메시지

# 3. 콘텐츠 작성
edit data/slides_content.json   # 슬라이드별 콘텐츠 입력

# 4. 빌드
python3 build.py
```

## 디렉토리 구조

```
proposal_template/
├── README.md                    # 본 파일
├── layouts/                     # 레이아웃 타입별 SVG 빌더 (재사용)
│   ├── cover.py                 # 표지 (사선 NAVY 패널)
│   ├── contents.py              # Contents (4 카드 + hex)
│   ├── part_divider.py          # Part divider (좌측 NAVY + 부섹션)
│   ├── card_grid.py             # 4 카드 + 하단 강조
│   ├── stats_grid.py            # 5 통계 카드 + 해석 + 정책
│   ├── scenario_3.py            # 3 시나리오 카드
│   ├── as_is_to_be.py           # 좌 As-Is + 우 To-Be
│   ├── diagram_intersection.py  # 십자교차로 도식
│   ├── diagram_school.py        # 학교+통학로 도식
│   ├── env_factor_chain.py      # 5요인 환경결합
│   ├── layered_arch.py          # 5계층 아키텍처
│   ├── logic_grade_table.py     # 입력+5등급 표
│   ├── priority_actions.py      # 1순위/보조/확장 3카드
│   ├── sop_5_step.py            # SOP 5단계 + 체크포인트
│   ├── criteria_table.py        # 선정 표 (3 카드 + 5단계 절차)
│   ├── gantt_cost.py            # gantt + 비용표
│   ├── kpi_table.py             # 정량+정성 KPI
│   ├── org_chart.py             # PM + 6 역할 트리
│   ├── dashboard_mockup.py      # 관제센터 + Before/After
│   ├── mockup_3panel.py         # 디지털트윈 + 모니터링 + What-if
│   ├── cert_badges.py           # 인증서 카드 4
│   ├── conclusion_stages.py     # 결론 + 3단계 사업화
│   └── org_info.py              # 제청기관 정보
├── components/                  # 재사용 컴포넌트 (svg_helpers.py 복사)
│   └── svg_helpers.py
├── data/                        # 발주처별 변경 항목
│   ├── spec_lock.yaml           # 디자인 사양 (색·폰트·레이아웃)
│   ├── client_notes.md          # 발주처 특수 사항
│   └── slides_content.json      # 슬라이드별 콘텐츠
├── docs/                        # 문서
│   ├── design_system.md         # 디자인 시스템 4축
│   ├── layout_catalog.md        # 23 레이아웃 타입 카탈로그
│   └── ai_image_prompts.md      # AI 이미지 프롬프트 가이드
└── build.py                     # 메인 빌더 (slides_content.json → final.pptx)
```

## 23 레이아웃 타입 카탈로그

| 타입 | 사용처 | 핵심 요소 |
|---|---|---|
| `cover` | 표지 | 사선 NAVY 패널 + 큰 제목 + 부제 + 로고 |
| `contents` | Contents | 4 부 카드 + hex 장식 |
| `part_divider` | Part 1/2/3/4 | 좌측 NAVY (PART 번호) + 우측 부섹션 |
| `card_grid` | 일반 본문 | 4 정보 카드 (좌측 컬러바) + 하단 강조 |
| `stats_grid` | 데이터 보기 | 5 통계 카드 (큰 숫자) + 해석 3 + 정책 시사점 |
| `scenario_3` | 시나리오 | 3 시나리오 카드 (번호+제목+위험요인+관리방향) |
| `as_is_to_be` | 한계→개선 | 좌 회색 As-Is 5 + 우 NAVY To-Be 5 |
| `diagram_intersection` | 우회전 위험 | 막대차트+십자교차로+노란차+화살표+보행자+라벨+4단계 |
| `diagram_school` | 스쿨존 | 5년 차트+학교+통학로+어린이+불법주정차+시야가림+위험원 |
| `env_factor_chain` | 환경 결합 | 5 요인 가로 흐름 (눈/사람/차/경고/방패) + 4 운영포인트 |
| `layered_arch` | 5계층 | 3 핵심 + 5계층 (각 계층 + 4 chips) |
| `logic_grade_table` | 위험판단 | 3 입력 + 5등급 표 + 운영자 노트 |
| `priority_actions` | 액션 | 1순위/보조/확장 3 카드 (각 3-5 항목) |
| `sop_5_step` | 운영절차 | 5단계 SOP + 운영체크포인트 + 산출물 |
| `criteria_table` | 선정 기준 | 3 카드 + 표 (b안 헤더) + 5단계 절차 |
| `gantt_cost` | 일정/비용 | 8개월 gantt + 5행 비용표 + 산정 전제 |
| `kpi_table` | KPI | 정량 표 + 정성 효과 + footnote |
| `org_chart` | 조직 | PM 박스 + 트리 + 6 역할 카드 (아이콘) |
| `dashboard_mockup` | 실적 | 관제센터 다크 mockup + Before/After 차트 + 본 과업 연결 |
| `mockup_3panel` | 시각화 | 3D 디지털트윈 + 실시간 모니터링 + What-if 시뮬 |
| `cert_badges` | 인증 | 5 인증 카드 placeholder + 3 영역 (품질/공급/특허) |
| `conclusion_stages` | 결론 | 결론 + 3단계 사업화 카드 |
| `org_info` | 제청기관 | 회사 로고 + 기관 정보 + 연락처 + 푸터 |

## 디자인 시스템 (불변)

### 컬러
- NAVY_HEADER `#0D3462` / NAVY_LIGHT `#10366B` / NAVY_DEEP `#0C2042`
- ORANGE `#F16A1F` (포인트, 핵심 데이터)
- GREEN `#27AE60` (긍정, 안전)
- WHITE / GRAY_BG `#F6F8FB` / GRAY_TEXT `#37425A` / BORDER `#D8DFE9`

### 타이포그래피
- 폰트: `'Apple SD Gothic Neo', 'Noto Sans CJK KR', 'Malgun Gothic', sans-serif`
- H1 28pt / H2 16pt / Body 13pt / Caption 11pt / Badge 16pt

### 레이아웃
- 캔버스: 1280×720 (16:9)
- 헤더: 100pt 높이 (풀폭 NAVY + 우상단 5 stripe)
- 카드: 14pt 라운드 + 6pt 좌측 컬러바
- 페이지번호: 우하단 (1232,690,38,22)

## 품질 임계값 (자동 검증)

```yaml
header_navy_ratio_min: 0.90
tone_delta_rgb_max: 5
card_density_tolerance: 0.15
ocr_forbidden_count_max: 0
native_shape_ratio_min: 1.0
slide_count_target: 32
```

## AI 학습 데이터 품질 (slides.json IR)

각 슬라이드에 다음 메타데이터:
- `id`, `section`, `rhetoric`, `title`, `layout_type`
- `elements` (text/shape/chart/diagram with role)
- `text_roles_distribution` (title/caption/body/badge counts)
- `design_meta` (has_chart/has_diagram/has_table/has_mockup)
- `origin` (codex_perfect / codex_part02_v6 / baseline_grade_v8 / hybrid)

→ 32장 × 6 versions = 224 records in `archive/slides.jsonl`

## 발주처 특수 사항 (client_notes.md)

각 발주처별 다음 항목 보관:
- 문서 정체성 (제안서/기획서/보고서 등)
- 핵심 메시지 + Part별 판단 문장
- 발주처 톤 보강 표현 (일반 → 권장)
- 금지 표현 (자가 확장 토큰)
- 비용·기간·KPI 표현 규칙
- 운영책임·거버넌스 필수 포함 항목

## 검증된 통계 Ledger (한국 보행자 안전, 2023 기준)

→ `docs/stats_ledger.md`에 분리. 다음 제안서에서 즉시 인용.
- 보행 사망 886명 (전체 34.7%, ▼5.0%)
- 65세 이상 전체 사망 1,240명 (48.6%)
- 스쿨존 486건 (▼5.4%) / 14~18시 52.9% / 5~6월 23.1%
- 야간 사고 41.1% / 사망 54.8% (1.74배↑)
- 결빙 치사율 +50%↑

## 라이선스

공개 포트폴리오 패키지에는 재사용 가능한 템플릿 구조와 공개-safe 메타데이터만 포함한다. 실제 고객사/기관별 원본 자료와 내부 산출물은 포함하지 않는다.

## 변경 이력

- v1 (2026-04-30): 001-dw_ai 프로젝트 v8 결과 기반 초판
