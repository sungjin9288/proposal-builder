---
asset: hexagon-network-corner-transparent.png
purpose: 우상단 코너 장식 (transparent 배경 — 본문 위에 자연 융합)
size: 320 x 320 px
recommended_size_emu: 2400000 x 1500000 EMU (≈189 x 118pt)
color:
  background: "transparent (alpha=0)"
  hexagon_stroke: "#0D3462 @ alpha 0.32, 2px"
  dotted: "#0D3462 @ alpha 0.30, 1px"
  node_default: "#0D3462 @ alpha 0.45"
  node_accent: "#F16A1F @ alpha 0.85"
source:
  base_image: "<baseline-reference-pptx> (baseline v2 p.9)"
  region_sampled: "panel_top zone NAVY 톤 (역 사용 — outline color)"
  method: "PIL hexagon network 합성, 배경 transparent, NAVY를 outline 색으로 사용. 전 hexagon-network-navy-corner의 NAVY-bg 사각 박스 두드러짐 문제 해결."
verified:
  ocr_words: 1 (점선이 ASCII 기호로 잘못 해석된 노이즈 — 의미 단어 아님)
  generated_seed: 7777
discovered_in: "001-dw_ai P1 (p.4 Contents) — NAVY-bg corner는 본문 위에 사각 박스로 두드러짐 → transparent 변형 필요"
usage:
  applies_to: ["p.4 Contents 우상단", "본문 위에 hex 장식이 필요한 모든 슬라이드"]
  placement: "z-order: 본문 도형 위(layer 2 이상). 단 텍스트는 corner 위에 두지 않음"
  recommended_scenarios:
    - "본문 슬라이드(NAVY 헤더 영역 외)에 hex 장식이 필요할 때"
    - "Contents/Part divider가 아닌 일반 슬라이드에 디자인 시스템 정체성을 추가하고 싶을 때"
---
