#!/usr/bin/env sh
# Print the agent harness repository directory for the Codex adapter.
# Preferred override: valid AGENT_HOME
# Neutral default after migration: $HOME/agent_setting
# Optional Codex runtime pointer: $HOME/.codex/agent-harness
set -eu

if [ -n "${AGENT_HOME:-}" ] && [ -f "$AGENT_HOME/core/CORE.md" ]; then
  printf '%s\n' "$AGENT_HOME"
elif [ -f "$HOME/agent_setting/core/CORE.md" ]; then
  printf '%s\n' "$HOME/agent_setting"
elif [ -f "$HOME/.codex/agent-harness/core/CORE.md" ]; then
  printf '%s\n' "$HOME/.codex/agent-harness"
else
  printf '%s\n' "$HOME/agent_setting"
fi
