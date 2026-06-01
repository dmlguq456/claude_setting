#!/usr/bin/env bash
# PreToolUse(Edit|Write|MultiEdit) — 모든 추적 산출물의 tracking 의도를 강제.
# 모델 (CLAUDE.md §0(0b) / WORKFLOW §0(b)):
#   📌tracked (기본)   — 추적 산출물 직접 Edit/Write 차단(exit 2) → 소유 스킬 경유(자체 버전관리).
#   ⚡untracked (flag) — .claude_reports/.untracked (mtime<60분) 있으면 직접 편집 허용, snapshot 없음.
#                        autopilot 파이프(소유 스킬) 편집도 이 flag 로 통과 → 스킬이 자체 버전관리.
# 가드 대상(0b 추적 산출물 전체):
#   spec/ canonical · plans/ · documents/ · experiments/ · ~/.claude/user_profile/0*.md
#   (_internal/ 스냅샷·spec/pipeline_state.yaml 등 기계관리 파일은 제외)
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

# _internal/ 기계관리 파일은 항상 통과 (스킬의 버전 snapshot 자리)
case "$fp" in */_internal/*) exit 0 ;; esac

# ---- 가드 대상 판정 + 소유 스킬 매핑 ----
kind=""; skill=""
case "$fp" in
  */.claude_reports/spec/*)
    case "$(basename "$fp")" in
      prd.md|stack.md|stack_decision.md|ship.md|api_contract.md|data_model.md|ui_flow.md)
        kind="spec 청사진"; skill="autopilot-spec update" ;;
      *) exit 0 ;;   # pipeline_state.yaml 등 기계관리 → 통과
    esac ;;
  */.claude_reports/plans/*)        kind="plans 코드작업"; skill="autopilot-code" ;;
  */.claude_reports/documents/*)    kind="documents 문서"; skill="autopilot-draft / autopilot-refine" ;;
  */.claude_reports/experiments/*)  kind="experiments 실험"; skill="autopilot-lab" ;;
  */.claude/user_profile/0*.md)     kind="user_profile 프로필"; skill="analyze-user / memo --scope user" ;;
  *) exit 0 ;;
esac

# ---- 프로젝트 루트 + untracked flag ----
d=$(dirname "$fp"); root=""
for _ in $(seq 1 40); do
  { [ -d "$d/.claude_reports" ] || [ -d "$d/user_profile" ]; } && { root="$d"; break; }
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done
[ -z "$root" ] && exit 0
# user_profile 는 ~/.claude 루트, 그 외는 프로젝트 .claude_reports 루트에 flag.
flag="$root/.claude_reports/.untracked"
[ -d "$root/.claude_reports" ] || flag="$root/.untracked"

# ---- untracked flag 신선도 (mtime < 3600s) → 직접 편집 허용 ----
if [ -f "$flag" ]; then
  mod=$(stat -c %Y "$flag" 2>/dev/null || stat -f %m "$flag" 2>/dev/null || echo 0)
  [ $(( $(date +%s) - mod )) -lt 3600 ] && exit 0
fi

# ---- tracked 모드(기본): ad-hoc 직접 편집 차단 ----
base=$(basename "$fp")
cat >&2 <<MSG
───────────────────────────────────────────
📌 tracked 산출물 — 직접 편집 차단 ($kind: $base)
───────────────────────────────────────────
추적 산출물은 소유 스킬로만 수정한다 (CLAUDE.md §0(0b)).
  · 정식 수정 → $skill (자체 버전관리)
  · 추적 불필요한 일회성 직접 수정이면 → touch $flag (⚡untracked, TTL 60분)
───────────────────────────────────────────
MSG
exit 2
