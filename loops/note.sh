#!/bin/bash
# autopilot-note 야간 루프 — crontab 에서 호출 (3 5 * * *)
# 전날 산출물을 worklog-board Layer 2 노트로 라우팅 (idempotent).
# 인자 없으면 default (--scope yesterday --qa light), 수동 호출 시 인자 전달 가능.
set -u
LOOP_DIR="$HOME/.claude/loops"
LOG="$LOOP_DIR/note.log"
# --- 일시 hold 가드 (토큰 절약, .hold 파일에 만료일 YYYY-MM-DD, 그날까지 skip 후 자동 재개) ---
if [ -f "$LOOP_DIR/.hold" ]; then _h=$(cat "$LOOP_DIR/.hold" 2>/dev/null); _t=$(date +%F);
  if [ -z "$_h" ] || [[ "$_t" < "$_h" ]] || [ "$_t" = "$_h" ]; then
    echo "[held until ${_h:-indefinite}] $(date -Iseconds)" >> "$LOG" 2>/dev/null || true; exit 0;
  fi;
fi

ARGS="${*:---scope yesterday --qa light}"

{
  echo "=== note run $(date -Iseconds) args: $ARGS ==="
  cd /home/nas/user/Uihyeop || exit 1
  # ⟨v52⟩ Turso 자격 주입 — 있으면 autopilot-note 의 DB 쓰기(migrate-fs-to-db 등)가
  #   클라우드 DB(앱과 동일)로 간다. 파일 없으면 로컬 file DB(이식 안 된 서버 graceful).
  [ -f "$LOOP_DIR/.worklog-turso.env" ] && . "$LOOP_DIR/.worklog-turso.env"
  timeout 2400 "$HOME/.local/bin/claude" -p "/autopilot-note $ARGS" \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Skill,Agent,TodoWrite" \
    2>&1
  echo "=== exit $? $(date -Iseconds) ==="
  # 통합 기억 store mirror — 하네스가 projects/<cwd>/memory 에 쓴 auto-memory 를 포터블 store 로 멱등 sync + 색인
  echo "--- mem sync $(date -Iseconds) ---"
  timeout 300 python3 "$HOME/.claude/tools/memory/mem.py" sync 2>&1 || echo "(mem sync 실패 — 비치명)"
} >> "$LOG"

tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
