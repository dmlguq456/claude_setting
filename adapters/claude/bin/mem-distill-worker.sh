#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
usage: mem-distill-worker.sh <mode> <model> <prompt-file>

Claude Code realization of the portable memory distillation worker contract.
Reads a prompt file and writes JSON-lines proposals to stdout.
EOF
}

[ "${1:-}" != "-h" ] && [ "${1:-}" != "--help" ] || { usage; exit 0; }
[ "$#" -eq 3 ] || { usage >&2; exit 64; }

mode=$1
model=$2
prompt_file=$3

case "$mode" in
  increment|curate) ;;
  *) echo "mem-distill-worker: unknown mode: $mode" >&2; exit 64 ;;
esac

case "$model" in
  fast-distiller)
    model="${CLAUDE_MEM_DISTILL_MODEL:-claude-sonnet-4-6}"
    ;;
  deep-curator)
    model="${CLAUDE_MEM_DISTILL_MODEL_SESSIONEND:-claude-opus-4-8}"
    ;;
esac

[ -f "$prompt_file" ] || { echo "mem-distill-worker: prompt file not found: $prompt_file" >&2; exit 64; }
command -v claude >/dev/null 2>&1 || exit 0

if command -v timeout >/dev/null 2>&1; then
  timeout_cmd=(timeout 120)
else
  timeout_cmd=()
fi

DISALLOW='Bash Read Write Edit Glob Grep Agent NotebookEdit WebFetch WebSearch Task'

MEM_DISTILL=1 setsid "${timeout_cmd[@]}" claude -p "$(cat "$prompt_file")" \
  --model "$model" \
  --disallowedTools "$DISALLOW"
