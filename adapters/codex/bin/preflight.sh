#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)

usage() {
  cat <<'EOF'
usage: preflight.sh write <file> [session-id]

Runs portable pre-write checks that Codex can call without consuming Claude
hook JSON or settings.json.
EOF
}

cmd=${1:-}
case "$cmd" in
  write) ;;
  -h|--help|"") usage; exit 0 ;;
  *) echo "codex preflight: unknown command: $cmd" >&2; usage >&2; exit 64 ;;
esac

[ "$#" -ge 2 ] || { echo "codex preflight: write requires a file path" >&2; exit 64; }
file=$2
sid=${3:-codex}

"$ROOT/hooks/git-state-guard.sh" --file "$file"
"$ROOT/hooks/artifact-guard.sh" --file "$file" --session "$sid"
