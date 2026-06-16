#!/bin/bash
# worklog-board ops/digests/manual fs→DB ingest 루프 — crontab (25 5 * * *, sweep 뒤).
# NAS 파일(oncall 보고·digest·manual)을 DB(Turso 있으면 클라우드)로 upsert. read-only on fs.
# ⟨v52 C4⟩ DB write 만·idempotent — 앱(Vercel)이 이 테이블을 읽음.
set -u
# cron 최소 PATH 보정 (nvm node/npx)
export PATH="$HOME/.local/bin:$HOME/.nvm/versions/node/v20.20.2/bin:$PATH"
LOOP_DIR="$HOME/.claude/loops"
LOG="$LOOP_DIR/ingest-ops.log"
BOARD=/home/nas/user/Uihyeop/worklog-board
if [ -f "$LOOP_DIR/.hold" ]; then _h=$(cat "$LOOP_DIR/.hold" 2>/dev/null); _t=$(date +%F);
  if [ -z "$_h" ] || [[ "$_t" < "$_h" ]] || [ "$_t" = "$_h" ]; then
    echo "[held until ${_h:-indefinite}] $(date -Iseconds)" >> "$LOG" 2>/dev/null || true; exit 0;
  fi;
fi
{
  echo "=== ingest-ops run $(date -Iseconds) ==="
  cd "$BOARD" || exit 1
  set -a; . "$BOARD/.env.local" 2>/dev/null; set +a                       # ONCALL_DIR/DIGESTS_DIR/MANUAL_DIR 등
  set -a; [ -f "$LOOP_DIR/.worklog-turso.env" ] && . "$LOOP_DIR/.worklog-turso.env"; set +a  # Turso 있으면 클라우드
  timeout 600 "$HOME/.local/bin/npx" tsx scripts/ingest-ops.ts --apply 2>&1
  echo "=== exit $? $(date -Iseconds) ==="
} >> "$LOG"
tail -n 1000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
