#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if command -v git >/dev/null 2>&1 && ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../../.." && pwd)
fi

usage() {
  cat <<'EOF'
usage: distill-worker.sh <session-id> [cwd]

OpenCode transcript distillation proposal worker.

STATUS: tool-contract. The shared memory CLI does not yet have an OpenCode
session source reader. OpenCode stores sessions in SQLite at
~/.local/share/opencode/opencode.db (tables: session, session_message) and
exposes `opencode export <session-id>` for JSON export. An OpenCodeDbSource
or OpenCodeExportSource implementing the .messages() interface
(Msg(role, ts, text, uuid, is_sidechain)) is required before delta extraction
works.

Even after a source reader exists, this worker must not auto-apply memory
mutations until an OpenCode no-tools worker contract is verified. Candidate:
`opencode run --agent <restricted-agent>` with deny permissions, or a future
plugin-mediated worker. Set OPENCODE_DISTILL_ENABLE=1 to attempt execution
once the source reader is implemented.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

[ "$#" -ge 1 ] || { usage >&2; exit 64; }

sid=$1
cwd=${2:-$PWD}

echo "opencode distill worker: tool-contract — session source reader not yet implemented" >&2
echo "opencode distill worker: OpenCode sessions live in SQLite (~/.local/share/opencode/opencode.db)" >&2
echo "opencode distill worker: implement OpenCodeDbSource or OpenCodeExportSource in tools/memory/mem.py" >&2
echo "opencode distill worker: automatic memory mutation remains disabled until a no-tools worker contract is verified" >&2
exit 69
