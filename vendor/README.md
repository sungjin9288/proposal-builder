# Vendor — External Tool Integrations

이 디렉토리는 외부 도구 연동 경계를 기록한다.
공개 포트폴리오 zip에는 `vendor/README.md`만 포함되며, `vendor/ppt-master/` 소스 트리는 포함하지 않는다.

## 등록된 프로젝트

### `ppt-master/` (hugohe3/ppt-master, MIT)

Source: https://github.com/hugohe3/ppt-master

용도: SVG → native editable PPTX 변환 도구 후보.
로컬 개발 환경에서 연동 가능한 외부 도구로 관리하며, 공개 패키지에는 소스 코드를 포함하지 않는다.

핵심 도구:
- `skills/ppt-master/scripts/svg_to_pptx.py` — SVG → PPTX 변환 메인 스크립트
- `skills/ppt-master/scripts/source_to_md/pdf_to_md.py` — PDF → Markdown 텍스트 추출
- `skills/ppt-master/templates/design_spec_reference.md` — design_spec 표준 템플릿
- `skills/ppt-master/templates/spec_lock_reference.md` — spec_lock 표준 템플릿

검증된 사용법:
```bash
python3 vendor/ppt-master/skills/ppt-master/scripts/svg_to_pptx.py \
  <project_dir> --only native -s <svg_dir_name> -o <output.pptx>
```

검증 범위:
- 로컬 개발 환경에서 SVG → PPTX 변환 도구 후보로 확인
- 공개 포트폴리오 zip에서는 재현 대상이 아님
- 공개 데모 CLI는 Python 표준 라이브러리 기반 OpenXML writer를 사용함

## 라이선스 / 출처

third-party source tree를 배포하는 경우 각 프로젝트의 LICENSE를 해당 디렉토리 하위에 보존해야 한다.
현재 공개 포트폴리오 zip에는 upstream source tree와 LICENSE 파일을 포함하지 않는다.
업데이트는 직접 git pull 또는 재clone:
```bash
gh repo clone hugohe3/ppt-master /tmp/ppt-master-update
# diff 확인 후 핵심 도구만 vendor/ppt-master/skills/ppt-master/scripts/로 복사
```

## Slim 정책

용량 관리를 위해 다음을 제거:
- `examples/` 일부 (1~2개 design_spec 예시만 보존)
- `templates/icons/` (47MB의 아이콘 라이브러리, 필요 시 upstream에서 별도 다운로드)
- `docs/zh/`, `docs/assets/*.gif`
