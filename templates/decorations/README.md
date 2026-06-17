# Decorations 자산 카탈로그

`templates/decorations/`는 제안서 슬라이드에 재사용 가능한 장식 자산을 보관한다.
새 작업에서 디자인 보강 시 이 디렉토리를 **우선 검색**한다.

## 자산 등록 규칙

1. 각 자산은 `<asset-name>.png` + `<asset-name>.meta.md` 쌍으로 보관
2. meta.md는 frontmatter 형식 — 자산 출처, 색상, 권장 크기, 사용처 명시
3. 자산은 텍스트 미포함 보장 — `tesseract <asset>.png -l kor` 결과 단어 수 0
4. 새 발주처 톤이 다르면 신규 자산 추가, 동일하면 기존 자산 재사용

## 현재 등록 자산

### Hexagon Network (NAVY 계열)

| 자산 | 사이즈 | 용도 | 출처 |
|---|---|---|---|
| [hexagon-network-navy-full.png](hexagon-network-navy-full.png) | 1920×180 | 풀폭 헤더 띠 (NAVY 배경) | baseline v2 p.9 (NAVY #0D3462 sample) |
| [hexagon-network-navy-corner.png](hexagon-network-navy-corner.png) | 320×320 | NAVY-bg 우상단 코너 (헤더 영역) | 동일 합성 함수 |
| [hexagon-network-navy-panel.png](hexagon-network-navy-panel.png) | 480×1080 | Part divider 좌측 패널 (NAVY 배경) | 동일 합성 함수 |
| [hexagon-network-corner-transparent.png](hexagon-network-corner-transparent.png) | 320×320 | **transparent 우상단 코너 (본문용)** | NAVY를 outline 색으로 사용 |
| [header-fade-mask-navy.png](header-fade-mask-navy.png) | 1920×180 | 헤더 fade 마스크 (좌→우 alpha) | hex 헤더 위 좌측 텍스트 가독 보호 |

**색조**: 모두 baseline v2 panel_top NAVY median(#0D3462) 기준.
**합성 방식**: 텍스트 0% 보장 위해 PIL로 직접 합성. seed로 패턴 분포 다양화.
**검증**: tesseract kor OCR 결과 단어 수 0 ✓

## 신규 자산 추가 절차

1. baseline 또는 발주처 가이드에서 자산 후보 영역 식별
2. 텍스트 미포함 영역만 캡처 또는 합성
3. OCR 검증 (`tesseract` 단어 수 0)
4. `<name>.png` + `<name>.meta.md` 보관
5. 본 README의 표에 한 줄 추가
