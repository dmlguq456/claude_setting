#!/usr/bin/env sh
# Print the agent harness repository directory for the OpenCode adapter.
# Preferred override: AGENT_HOME
# Neutral default after migration: $HOME/agent_setting
# Optional OpenCode runtime pointer: $HOME/.config/opencode/agent-harness
set -eu

if [ "${AGENT_HOME:-}" ]; then
  printf '%s\n' "$AGENT_HOME"
elif [ -d "$HOME/agent_setting" ]; then
  printf '%s\n' "$HOME/agent_setting"
elif [ -e "$HOME/.config/opencode/agent-harness" ]; then
  printf '%s\n' "$HOME/.config/opencode/agent-harness"
else
  printf '%s\n' "$HOME/agent_setting"
fi
