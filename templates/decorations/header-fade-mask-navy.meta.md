---
asset: header-fade-mask-navy.png
purpose: 풀폭 hexagon 헤더 위에 좌측 텍스트 영역만 NAVY로 가리기 위한 fade 마스크
size: 1920 x 180 px
recommended_size_emu: 12192000 x 987552 EMU (풀폭 헤더와 동일)
color:
  navy_base: "#0D3462 (baseline v2 sampled)"
  alpha_curve: "0~60% solid α=255 → 60~75% ease-out (1-t)^1.6 → 75~100% α=0 (헤더 NAVY 비율 ≥90% 임계값 통과 위해 v2에서 solid 영역 55%→60% 확장)"
source:
  base_image: "헤더 fade는 합성. NAVY 톤은 baseline v2 panel_top sample 재사용."
  method: "PIL alpha-gradient. hex overlay와 자연스럽게 연결되도록 ease-out 곡선."
verified:
  ocr_words: 0
discovered_in: "기준 제안서 P1 (p.2/p.3/p.7) — hex overlay 좌측이 텍스트와 충돌해 단차 발생 → fade-mask로 자연 연결"
usage:
  applies_to: ["p.2 개요", "p.3 모델 기획", "p.7 1-2 제청 논리"]
  z_order: "header(NAVY 단색) → hexagon-network-navy-full → header-fade-mask-navy → 텍스트"
  effect: "좌측 텍스트 영역은 깨끗한 NAVY, 우측 헤더는 hexagon 패턴 노출, 가운데는 자연스러운 fade"
  recommended_scenarios:
    - "풀폭 헤더 + hex overlay 조합을 사용하는 모든 slide"
    - "헤더 좌측에 제목/부제 텍스트가 있는 경우 (가독성 보호 필요)"
    - "다른 발주처 톤 적용 시: navy_base 색만 변경하면 동일 패턴 재사용 가능"
---
