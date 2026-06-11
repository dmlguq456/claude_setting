#!/bin/bash
# autopilot-note 야간 루프 — crontab 에서 호출 (3 5 * * *)
# 전날 산출물을 worklog-board Layer 2 노트로 라우팅 (idempotent).
# 인자 없으면 default (--scope yesterday --qa light), 수동 호출 시 인자 전달 가능.
set -u
LOOP_DIR="$HOME/.claude/loops"
LOG="$LOOP_DIR/note.log"
ARGS="${*:---scope yesterday --qa light}"

{
  echo "=== note run $(date -Iseconds) args: $ARGS ==="
  cd /home/nas/user/Uihyeop || exit 1
  timeout 2400 "$HOME/.local/bin/claude" -p "/autopilot-note $ARGS" \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Skill,Agent,TodoWrite" \
    2>&1
  echo "=== exit $? $(date -Iseconds) ==="
} >> "$LOG"

tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
