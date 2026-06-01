#!/usr/bin/env bash
# PreToolUse(Edit|Write|MultiEdit) — canonical 산출물 ad-hoc 편집 차단 + 버전 snapshot.
# 목적: "동일 스킬 수정 = 버전 트래킹" 불변식을 advisory 가 아닌 harness 로 강제.
#   - 대상: .claude_reports/spec/ 아래 canonical 파일 (flat + monorepo spec/<feature>/ 모두).
#   - pipeline sentinel(.claude_reports/.pipeline_active, mtime<60분) 있으면 → 통과 + 이전 버전 snapshot.
#   - 없으면 → exit 2 차단, autopilot-spec update 경로로 라우팅.
# sentinel 생성 = autopilot 산출물-편집 스킬 호출 직전 touch (CLAUDE.md §0 ceremony). 일회성은 수동 touch/override.
# 단일 출처: CLAUDE.md §0(0b) + WORKFLOW.md §0(b).
set -euo pipefail

input=$(cat)
fp=$(printf '%s' "$input" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin); ti = d.get("tool_input") or {}
    print(ti.get("file_path", "") or "")
except Exception:
    print("")
' 2>/dev/null)
[ -z "$fp" ] && exit 0

# ---- 대상 판정: spec/ 아래 canonical 파일만 (그 외 전부 통과) ----
case "$fp" in
  */.claude_reports/spec/*) ;;
  *) exit 0 ;;
esac
case "$fp" in */_internal/*) exit 0 ;; esac   # 스냅샷/기계 파일은 제외
base=$(basename "$fp")
case "$base" in
  prd.md|stack.md|stack_decision.md|ship.md|api_contract.md|data_model.md|ui_flow.md) ;;
  *) exit 0 ;;
esac

# ---- 프로젝트 루트(.claude_reports 보유) 탐색 ----
d=$(dirname "$fp"); root=""
for _ in $(seq 1 40); do
  [ -d "$d/.claude_reports" ] && { root="$d"; break; }
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done
[ -z "$root" ] && exit 0
sentinel="$root/.claude_reports/.pipeline_active"

# ---- sentinel 신선도 (mtime < 3600s) ----
fresh=0
if [ -f "$sentinel" ]; then
  mod=$(stat -c %Y "$sentinel" 2>/dev/null || echo 0)
  now=$(date +%s)
  [ $((now - mod)) -lt 3600 ] && fresh=1
fi

# ---- 차단 경로 (sentinel 없음/만료) ----
if [ "$fresh" = "0" ]; then
  cat >&2 <<MSG
───────────────────────────────────────────
⛔ canonical 산출물 ad-hoc 편집 차단 — $base
───────────────────────────────────────────
이 파일은 그것을 만든 스킬로만 수정한다 (CLAUDE.md §0(0b) / WORKFLOW §0(b)).
  · spec 파일 → autopilot-spec update mode (prd 갱신 + _internal/versions/v{N}/ 자동 snapshot)
  · 정당한 pipeline 작업이면 → touch $sentinel 후 재시도 (TTL 60분, 자동 snapshot)
  · 순수 typo·1줄·일회성이면 위 touch 로 override
───────────────────────────────────────────
MSG
  exit 2
fi

# ---- 통과 경로: 기존 파일 이전 버전 자동 snapshot ----
if [ -f "$fp" ]; then
  specdir=$(dirname "$fp")
  vroot="$specdir/_internal/versions"
  mkdir -p "$vroot" 2>/dev/null || true
  max=0
  for v in "$vroot"/v[0-9]*; do
    [ -d "$v" ] || continue
    n=${v##*/v}; case "$n" in *[!0-9]*) continue ;; esac
    [ "$n" -gt "$max" ] && max="$n"
  done
  next=$((max + 1)); vdir="$vroot/v$next"
  mkdir -p "$vdir" 2>/dev/null || true
  cp -p "$fp" "$vdir/$base" 2>/dev/null || true
  msg="pipeline 편집 허용 ($base) — 이전 버전 _internal/versions/v$next/ 자동 snapshot. canonical 경로는 autopilot-spec update."
  python3 -c '
import json,sys
print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":sys.argv[1]}}))
' "$msg" 2>/dev/null || true
fi
exit 0
