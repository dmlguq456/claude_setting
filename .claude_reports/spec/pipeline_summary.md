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

## Next
open 결정 확정 → autopilot-code --mode dev
