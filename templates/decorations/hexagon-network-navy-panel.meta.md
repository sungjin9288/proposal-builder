---
asset: hexagon-network-navy-panel.png
purpose: Part divider 좌측 네이비 패널용 (세로 직사각)
size: 480 x 1080 px (4:9 종횡비)
recommended_size_emu: ~3500000 x 6858000 EMU (좌측 패널 28.7% 폭, 슬라이드 풀높이)
color:
  background: "#0D3462"
  hexagon_stroke: "#FFFFFF @ alpha 0.18, 2px"
  dotted: "#FFFFFF @ alpha 0.22, 1px"
  node_default: "#FFFFFF @ alpha 0.55"
  node_accent: "#F16A1F @ alpha 0.85"
source:
  base_image: "<baseline-reference-pptx> (baseline v2 p.9)"
  region_sampled: "panel_top zone NAVY 톤"
  method: "동일 합성 함수, panel divider seed로 세로 패턴 풍부화"
verified:
  ocr_words: 0
  generated_seed: hash('hexagon-network-navy-panel') % 100000
usage:
  applies_to: ["p.5 Part 01 divider (장식 예정)", "P2/P3에서 p.11 Part 02, p.20 Part 03, p.25 Part 04 divider에도 동일 활용 가능"]
  placement: "좌측 네이비 패널의 텍스트 영역(PART 번호, 섹션 제목, 하단 설명) 사이의 빈 공간에 layer 0로 배치. 텍스트는 항상 layer 1 이상."
---
