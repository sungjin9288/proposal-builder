---
asset: hexagon-network-navy-full.png
purpose: 풀폭 네이비 헤더용 hexagon 네트워크 장식 (가로 띠)
size: 1920 x 180 px (16:1.5 종횡비)
recommended_height_emu: ~988000 EMU (≈78pt, baseline 헤더 높이와 일치)
color:
  background: "#0D3462"
  hexagon_stroke: "#FFFFFF @ alpha 0.18, 2px"
  dotted: "#FFFFFF @ alpha 0.22, 1px"
  node_default: "#FFFFFF @ alpha 0.55"
  node_accent: "#F16A1F @ alpha 0.85"
source:
  base_image: "<baseline-reference-pptx>"
  page: 9 (Part 02 divider)
  region_sampled: "panel_top zone (x:50-200, y:30-100) — NAVY 평평한 영역"
  method: "baseline NAVY median 추출 (#0D3462) + PIL hexagon network 합성. 텍스트 미포함 보장 (OCR words=0 ✓)."
verified:
  ocr_words: 0
  generated_seed: hash('hexagon-network-navy-full') % 100000
usage:
  applies_to: ["p.2 개요", "p.3 모델 기획", "p.7 1-2 제청 논리"]
  placement: "슬라이드 헤더 풀폭 네이비 위에 layer 1로 배치. 좌측 텍스트(제목/부제) 영역에 alpha 마스크 권장."
---
