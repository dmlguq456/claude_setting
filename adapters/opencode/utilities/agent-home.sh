#!/usr/bin/env sh
# Print the agent harness repository directory for the OpenCode adapter.
# Preferred override: valid AGENT_HOME
# Neutral default after migration: $HOME/agent_setting
# Optional OpenCode runtime pointer: $HOME/.config/opencode/agent-harness
set -eu

if [ -n "${AGENT_HOME:-}" ] && [ -f "$AGENT_HOME/core/CORE.md" ]; then
  printf '%s\n' "$AGENT_HOME"
elif [ -f "$HOME/agent_setting/core/CORE.md" ]; then
  printf '%s\n' "$HOME/agent_setting"
elif [ -f "$HOME/.config/opencode/agent-harness/core/CORE.md" ]; then
  printf '%s\n' "$HOME/.config/opencode/agent-harness"
else
  printf '%s\n' "$HOME/agent_setting"
fi
