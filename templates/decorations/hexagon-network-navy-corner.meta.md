---
asset: hexagon-network-navy-corner.png
purpose: 우상단 코너 장식 (정사각형, Contents/일반 본문 슬라이드용)
size: 320 x 320 px
recommended_size_emu: ~2200000 x 2200000 EMU (≈173 x 173pt)
color:
  background: "#0D3462"
  hexagon_stroke: "#FFFFFF @ alpha 0.18, 2px"
  dotted: "#FFFFFF @ alpha 0.22, 1px"
  node_default: "#FFFFFF @ alpha 0.55"
  node_accent: "#F16A1F @ alpha 0.85"
source:
  base_image: "<baseline-reference-pptx> (baseline v2 p.9)"
  region_sampled: "panel_top zone NAVY 톤"
  method: "동일 합성 함수, 다른 seed로 패턴 분포 다양화"
verified:
  ocr_words: 0
  generated_seed: hash('hexagon-network-navy-corner') % 100000
usage:
  applies_to: ["p.4 Contents (우상단 장식 예정)"]
  placement: "헤더 우상단에 정사각으로 배치. baseline Contents의 hexagon 장식 위치 모방."
---
