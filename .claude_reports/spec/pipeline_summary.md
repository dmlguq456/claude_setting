# Spec Pipeline Summary: memory-store

- **Date**: 2026-06-15
- **Mode**: library + cli
- **Status**: spec in_progress (PRD 초안, open 결정 대기)

## Process Log
| Step | Action | Result |
|---|---|---|
| 1 | 정보 수집 | 입력 5종 확인, 이주 대상 59파일/22dir |
| 2 | mode 확정 | library + cli (메모리 저장소 모듈) |
| 3 | PRD 작성 | prd.md — D1~D7 locked + D-open 1~3 |

## 핵심 결정 (locked)
- D1 markdown 원본(추적) + SQLite FTS5 색인(파생) + projection(파생)
- D2 저장 위치 ↔ 스코프 분리 (통합 저장소 + cwd_origin 태그)
- D3 자동 write (기억 한정, 사람 게이트 없음, 품질필터만) — 불변식 의식적 전환
- D4 59파일 이주 / D5 하네스 projection / D6 recall 진화 / D7 injection 가드

## Open (사용자 확인)
- D-open-1 삭제 정책 / D-open-2 projection 갱신 시점 / D-open-3 이주 후 기존 폴더

## Update Log

### v1 → v2 (2026-06-15, update mode — drift 정정, snapshot `_internal/versions/v1/`)
구현이 spec 보다 앞서 만든 drift 정정 (코드가 진실, spec 후행):
- **D5** "주입은 Claude Code 가 projects/ 에서, 우리가 못 바꿈" (outdated) → **자체 하네스**로 정정: SessionStart `mem inject --hook`(store→additionalContext 직접 주입) + SessionEnd `mem sync`(projects/ auto-memory→store mirror+색인). store 가 세션 주입의 source.
- **Architecture mermaid**: PROJ→CC projection 주입 흐름(old) → `SRC ==mem inject==> CC`(주입) + `projects/ ==mem sync==> SRC`(회수) + 하네스 write→projects/ 로 교체.
- **D-4** projection 갱신 → inject(세션시작)+sync(세션종료) hook 자동.
- **cli 표·[library] API**: `mem inject`·`mem sync` 행 추가, `mem project` 는 "보조(주입은 inject)" 주석.
- 근거(검증): `settings.json` SessionStart=`mem.py inject --hook`·SessionEnd=`mem.py sync` 확인, 이번 세션 상단 inject 블록 실측.
- 스코프 한정: D1~D4·D6·D7·통합모델·데이터모델 불변.

## Next
지침 정합·mem.py 견고성·README → autopilot-code --mode dev (본 spec 따라)
