#!/usr/bin/env python3
"""Codex PermissionRequest bridge — intentionally a no-op.

This bridge used to emit a harness status snapshot as
``hookSpecificOutput.additionalContext`` on every approval prompt. That was a
monitoring substitute for Codex's (then-absent) live statusline. Codex now ships
a native ``/statusline`` that owns runtime monitoring, so this bridge no longer
injects a status snapshot.

The ``PermissionRequest`` event stays registered as a trusted no-op so the Codex
hook projection/installation contract is preserved and an approval-time signal
can be reintroduced here without re-wiring projection. Harness status snapshots
remain available on demand via ``adapters/codex/bin/preflight.sh status`` (manual
lookups and headless-worker startup); Codex owns approval and sandbox decisions.
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    # Consume any hook payload on stdin so the runtime never sees a broken pipe,
    # then emit nothing — monitoring is owned by the native Codex /statusline.
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
