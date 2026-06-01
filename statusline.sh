#!/usr/bin/env bash
# Custom statusline — cwm HUD 대체 (의존성 없음, python3 로 JSON 파싱).
# 표시: 디렉토리 · git 브랜치 · spec-backed 게이트 상태 · 모델.
# 입력: stdin JSON (Claude Code statusLine schema). 출력: 한 줄.
set -euo pipefail
input=$(cat)

read -r cwd model <<EOF
$(printf '%s' "$input" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    print(". ?"); sys.exit()
cwd = d.get("cwd") or (d.get("workspace") or {}).get("current_dir") or "."
m = d.get("model") or {}
model = m.get("display_name") or m.get("id") or "?"
print(cwd, model)
' 2>/dev/null)
EOF
[ -z "${cwd:-}" ] && cwd="$PWD"

dir=$(basename "$cwd")

# git 브랜치
branch=""
if command -v git >/dev/null 2>&1; then
  branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
fi

# spec-backed 게이트 상태 (WORKFLOW harness 테마)
gate=""
d="$cwd"
for _ in $(seq 1 40); do
  if [ -f "$d/.claude_reports/spec/pipeline_state.yaml" ] || ls "$d"/.claude_reports/spec/*/pipeline_state.yaml >/dev/null 2>&1; then
    if [ -f "$d/.claude_reports/.pipeline_active" ]; then
      mod=$(stat -c %Y "$d/.claude_reports/.pipeline_active" 2>/dev/null || echo 0)
      now=$(date +%s)
      [ $((now - mod)) -lt 3600 ] && gate="◆spec:pipe" || gate="◇spec:gated"
    else
      gate="◇spec:gated"
    fi
    break
  fi
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done

# ANSI 색 (dim/cyan/yellow/green)
DIM=$'\033[2m'; CYAN=$'\033[36m'; YEL=$'\033[33m'; GRN=$'\033[32m'; RST=$'\033[0m'

out="${CYAN}${dir}${RST}"
[ -n "$branch" ] && out="${out} ${DIM}⎇${RST}${YEL}${branch}${RST}"
[ -n "$gate" ] && out="${out} ${GRN}${gate}${RST}"
out="${out} ${DIM}${model}${RST}"
printf '%s' "$out"
