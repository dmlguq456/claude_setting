#!/usr/bin/env bash
# SessionStart guard — spec-backed cwd 감지 시 spec-first 라우팅을 컨텍스트로 주입.
# 목적: 새 세션에서 WORKFLOW.md §7 / CLAUDE.md §0 를 우회하고 ad-hoc Edit 으로 가는 것 차단.
# 등록: ~/.claude/settings.json 의 hooks.SessionStart.
# 동작: cwd·상위에 .claude_reports/spec/pipeline_state.yaml (flat, 1 repo = 1 spec)
#       또는 .claude_reports/spec/*/pipeline_state.yaml (모노레포 예외) 있으면만 출력.
set -euo pipefail

# cwd 에서 위로 올라가며 spec-backed 루트 탐색 (서브디렉토리에서 열어도 잡도록).
d="$PWD"; root=""
for _ in $(seq 1 40); do
  if [ -f "$d/.claude_reports/spec/pipeline_state.yaml" ] || ls "$d"/.claude_reports/spec/*/pipeline_state.yaml >/dev/null 2>&1; then
    root="$d"; break
  fi
  { [ "$d" = "/" ] || [ "$d" = "$HOME" ]; } && break
  d=$(dirname "$d")
done
[ -z "$root" ] && exit 0

proj=$(basename "$root")

read -r -d '' ctx <<EOF || true
⚠️ SPEC-BACKED 프로젝트 감지 — ${proj}/.claude_reports/spec/

이 cwd 의 코드·기능·수정 요청은 ad-hoc 직접 Edit 으로 끝내지 않는다. 반드시 ~/.claude/WORKFLOW.md §7 (사후 수정 라우팅) 을 탄다:

0. 손대기 전 기존 산출물 파악 — spec/prd.md · pipeline_state.yaml · 최근 plans/* 를 필요에 따라 먼저 읽어 프로젝트 상태를 잡는다.
1. (필요 시) analyze 갱신 — analysis_project/code/ stale·낯선 영역이면 analyze-project --mode code 먼저.
2. spec-drift 사전 체크 (code 경유 _전_) — prd.md 대조. spec-significant (route/schema/UI-flow/외부연동/마이그레이션) 또는 기존 drift → autopilot-spec update (prd 갱신 + _internal/versions/v{N}/ 스냅샷). drift 명확하면 자율 진행, 애매하면 사용자 확인.
3. autopilot-code 경유 — 작은 자연어 요청도 --qa quick 으로 산출물 남기며 진행 → plans/<date>_<slug>/.

직접 Edit 허용 = 순수 typo·1줄 포맷뿐.
EOF

ctx_json=$(printf '%s' "$ctx" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$ctx_json"
