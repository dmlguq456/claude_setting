#!/usr/bin/env bash
# Toggle artifact-guard mode for the project containing cwd.
# 📌tracked (flag 없음) ↔ ⚡untracked (.claude_reports/.untracked 존재, 끌 때까지 유지).
# /track slash command 에서 호출. 단독 실행도 가능.
set -euo pipefail

d="$PWD"; root=""
for _ in $(seq 1 40); do
  [ -d "$d/.claude_reports" ] && { root="$d"; break; }
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done
[ -z "$root" ] && { echo "⚠️  상위 트리에 .claude_reports 가 없어요 — 토글 대상 프로젝트가 아닙니다."; exit 0; }

f="$root/.claude_reports/.untracked"
if [ -f "$f" ]; then
  rm -f "$f"
  echo "📌 tracked(pipeline) 모드 — canonical 산출물 직접 편집 차단. 수정은 autopilot-spec 경유(자체 버전관리)."
else
  touch "$f"
  echo "⚡ untracked(ad-hoc) 모드 — 직접 편집 허용·snapshot 없음 (다시 /track 까지 유지). [$root]"
fi
