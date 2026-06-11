# 야간 정찰 (read-only 점검 + 보고만)

어떤 수정·커밋·푸시·정리도 하지 않는다. 허용된 쓰기는 보고 파일 1개뿐.

## 점검 항목

1. **git 상태**: `/home/nas/user/Uihyeop` 에서 depth 3 이내 `.git` 보유 repo 탐색 (백업·`node_modules`·`_layer2*` 제외). 각 repo 에서:
   - merge / rebase / cherry-pick 진행 중인지
   - dirty 파일 수
   - DONE-BRANCH: 현재 브랜치가 origin 기본 브랜치에 ahead 0 인데 기본 브랜치가 아님 (= 머지 완료된 끝난 브랜치에 머묾)
   - prunable worktree (`git worktree list --porcelain`)
2. **산출물 누적 minor**: 각 `.claude_reports/*/pipeline_summary.md` 에서 마지막 audit 이후 minor 기록 5건 이상 → `/audit` 권장 표시.
3. **실험 방치**: `experiments/_RUNLOG.md` 의 ⏳ 상태 entry 중 7일 이상 갱신 없음 → 목록.

## 보고

- 발견이 하나라도 있으면 `/home/nas/user/Uihyeop/notes/scout/<오늘 날짜 YYYY-MM-DD>.md` 에 간결한 한국어 보고 작성 — 항목당 1~2줄, repo 경로·브랜치 명시, 권장 조치 한 줄.
- 발견 0 이면 파일을 만들지 않고 종료.
- 보고는 사실만 — 추정 수치·과장 금지 (빈칸 > 잘못 채우기).
