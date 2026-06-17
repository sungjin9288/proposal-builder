# Proposal HWP Generator (Placeholder)

`prd.md`를 기반으로 HWP 파일을 생성하는 스킬.
현재는 placeholder이며, Windows 워커 환경 구축 후 구현 예정.

## 입력

- `projects/[프로젝트명]/prd.md` — 사용자가 검토·확정한 PRD

## 출력

- `projects/[프로젝트명]/output.hwp` — 최종 HWP 파일

## 구현 계획

### 전제 조건 (미충족)

- Windows 환경
- 한컴 한글 설치
- pywin32 패키지
- 한글 COM API 접근

### 예정 절차

1. `prd.md`에서 섹션 구조를 읽는다.
2. 한글 COM API를 통해 HWP 문서를 생성한다.
3. 템플릿 HWP가 있으면 로드하여 내용을 채운다.
4. `output.hwp`로 저장한다.

## 현재 상태

> **미구현**: Windows 환경 및 한컴 한글 COM API 의존성으로 인해 추후 구현 예정.
> 이 스킬을 호출하면 미구현 안내 메시지를 출력한다.
