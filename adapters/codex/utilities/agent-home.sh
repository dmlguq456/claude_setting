#!/usr/bin/env sh
# Print the agent harness repository directory for the Codex adapter.
# Preferred override: AGENT_HOME
# Neutral default after migration: $HOME/agent_setting
# Optional Codex runtime pointer: $HOME/.codex/agent-harness
set -eu

if [ "${AGENT_HOME:-}" ]; then
  printf '%s\n' "$AGENT_HOME"
elif [ -d "$HOME/agent_setting" ]; then
  printf '%s\n' "$HOME/agent_setting"
elif [ -e "$HOME/.codex/agent-harness" ]; then
  printf '%s\n' "$HOME/.codex/agent-harness"
else
  printf '%s\n' "$HOME/agent_setting"
fi
