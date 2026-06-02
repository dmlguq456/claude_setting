#!/usr/bin/env bash
# workflow-guard-hook — WORKFLOW.md (tracked-mode 계약) 를 컨텍스트로 전달.
#   SessionStart    : 라우팅 코어 전체 주입 (+ spec-backed 면 §7 디테일).
#   UserPromptSubmit: 매 프롬프트 _모드 신호_ (cr_root 프로젝트) — 📌tracked(WORKFLOW 따름·skill 경유)
#                     vs ⚡untracked(면제·자유). Claude 가 "WORKFLOW 지킬지" 를 positive 하게 인지.
# 규칙의 단일 출처 = WORKFLOW.md §0/§7 (본 hook 은 _전달_ 만; UserPromptSubmit 은 재서술 없이 상기만).
# 등록: ~/.claude/settings.json 의 hooks.SessionStart + hooks.UserPromptSubmit.
set -euo pipefail

input=$(cat 2>/dev/null || true)
eval "$(printf '%s' "$input" | python3 -c '
import json, sys, shlex
try: d = json.load(sys.stdin)
except Exception: d = {}
print("EVENT="+shlex.quote(d.get("hook_event_name","") or ""))
print("SID="+shlex.quote(d.get("session_id","") or ""))
' 2>/dev/null || true)"
EVENT="${EVENT:-}"; SID="${SID:-}"

# ---- 프로젝트 cwd 판정 (git work tree 또는 .claude_reports/ 보유) ----
is_project=0
if command -v git >/dev/null 2>&1 && git -C "$PWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  is_project=1
fi

# cwd 에서 위로 올라가며 .claude_reports/ 와 spec-backed 루트 탐색.
d="$PWD"; cr_root=""; spec_root=""
for _ in $(seq 1 40); do
  [ -z "$cr_root" ] && [ -d "$d/.claude_reports" ] && cr_root="$d"
  if [ -z "$spec_root" ]; then
    if [ -f "$d/.claude_reports/spec/pipeline_state.yaml" ] || ls "$d"/.claude_reports/spec/*/pipeline_state.yaml >/dev/null 2>&1; then
      spec_root="$d"
    fi
  fi
  { [ "$d" = "/" ] || [ "$d" = "$HOME" ]; } && break
  d=$(dirname "$d")
done
[ -n "$cr_root" ] && is_project=1

# ⚡untracked 세션별 flag 판정.
untracked=0
if [ -n "$cr_root" ]; then
  flag="$cr_root/.claude_reports/.untracked"; [ -n "$SID" ] && flag="$flag.$SID"
  [ -f "$flag" ] && untracked=1
fi

emit() {  # $1 = hookEventName, stdin = ctx 본문
  local ctx j
  ctx=$(cat)
  j=$(printf '%s' "$ctx" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
  printf '{"hookSpecificOutput":{"hookEventName":"%s","additionalContext":%s}}\n' "$1" "$j"
}

# ============================================================
# UserPromptSubmit — 매 프롬프트 thin reminder (tracked 일 때만)
# ============================================================
if [ "$EVENT" = "UserPromptSubmit" ]; then
  # .claude_reports 없음 → tracked/untracked 토글 자체가 무관 → 침묵.
  [ -z "$cr_root" ] && exit 0
  # 모드를 _양쪽 다 명시_ — Claude 가 "WORKFLOW 를 지킬지" 를 매 프롬프트 positive 하게 결정.
  if [ "$untracked" = "1" ]; then
    emit UserPromptSubmit <<'EOF'
🧭 ⚡untracked — WORKFLOW 면제. 산출물·소스 코드 직접 편집 자유 (추적·trail 없음). 정식 파이프로 돌리려면 /track.
EOF
  else
    spec_tail=""
    [ -n "$spec_root" ] && spec_tail=" spec-backed → 수정·기능은 WORKFLOW §7 (spec-drift 체크 → autopilot-code)."
    emit UserPromptSubmit <<EOF
🧭 📌tracked — WORKFLOW(§0/§7) 따름. 작업(코드/스펙/문서/실험)이면 직접 편집 말고 autopilot-* skill 경유; 산출물은 만든 스킬로. 단발·throwaway 만 직접.${spec_tail}
EOF
  fi
  exit 0
fi

# ============================================================
# SessionStart (default) — 라우팅 코어 전체 주입
# ============================================================
# 스케일·잔여 ⚡untracked flag GC (>1일) — 세션 시작에 1회.
if [ -n "$cr_root" ]; then
  find "$cr_root/.claude_reports" -maxdepth 1 -name '.untracked.*' -mmin +1440 -delete 2>/dev/null || true
fi

[ "$is_project" = "0" ] && exit 0       # scratch/home dir → 조용히 종료

read -r -d '' ctx <<'EOF' || true
🧭 WORKFLOW 단일 라우터 — 작업 흐름 불변식 (~/.claude/WORKFLOW.md §0 = tracked 모드 계약)

모든 작업 발화는 WORKFLOW §2 작업-본질 매핑을 먼저 거친다. 직접 처리·codex 플러그인·빌트인 스킬도 WORKFLOW 가 배치하는 자리에서만 쓴다.

■ 하드 순서 게이트 (앞 단계 산출물 없이 다음 단계 진입 금지):
  [코드]  research / analyze-project(code) → autopilot-spec (spec/) → autopilot-code (plans/)
  [문서]  research / analyze-project(paper·doc) → autopilot-draft → autopilot-refine
  · spec 없이 코드 작업 X — 코드 요청인데 spec/ 없으면 autopilot-spec 먼저.
  · 사전 산출물 없이 spec X — research/ 또는 analysis_project/ 없으면 그것 먼저.
  · throwaway 1 회성만 예외 (반복되면 spec 승격).

■ 동일 스킬 수정 = 버전 트래킹 (convention): 산출물은 그것을 만든 스킬로만 수정한다.
  spec→autopilot-spec update / plans→autopilot-code / documents→autopilot-draft·refine / experiments→autopilot-lab.
  artifact-guard hook 은 _생성 순서_ 만 하드 차단(신규 산출물 ← 앞 단계, 코드 ← plan); 기존 산출물 _편집_ 은 convention. ⚡untracked(/track) = 전부 우회.
EOF

if [ -n "$spec_root" ]; then
  proj=$(basename "$spec_root")
  read -r -d '' spec_ctx <<EOF || true

⚠️ SPEC-BACKED 프로젝트 감지 — ${proj}/.claude_reports/spec/ → WORKFLOW §7 (사후 수정 라우팅) 필수:
0. 손대기 전 기존 산출물 파악 — spec/prd.md · pipeline_state.yaml · 최근 plans/* 를 먼저 읽어 상태 파악.
1. (필요 시) analyze 갱신 — analysis_project/code/ stale·낯선 영역이면 analyze-project --mode code 먼저.
2. spec-drift 사전 체크 (code 경유 _전_) — prd.md 대조. spec-significant(route/schema/UI-flow/외부연동/마이그레이션) 또는 기존 drift → autopilot-spec update (prd + _internal/versions/v{N}/ snapshot). 명확하면 자율 진행, 애매하면 사용자 확인. (autopilot-code pre-flight Step 0 으로도 강제.)
3. autopilot-code 경유 — 작은 자연어 요청도 --qa quick 으로 plans/<date>_<slug>/ 에 산출물 남김.
EOF
  ctx="${ctx}${spec_ctx}"
fi

printf '%s' "$ctx" | emit SessionStart
