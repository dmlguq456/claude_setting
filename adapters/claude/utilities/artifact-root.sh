#!/usr/bin/env sh
# Print the artifact root for the current project.
# Default for new projects: .agent_reports
# Legacy fallback: .claude_reports, only when it already exists and .agent_reports does not.
set -eu

root="${1:-$PWD}"
if [ -d "$root/.agent_reports" ]; then
  printf '%s\n' "$root/.agent_reports"
elif [ -d "$root/.claude_reports" ]; then
  printf '%s\n' "$root/.claude_reports"
else
  printf '%s\n' "$root/.agent_reports"
fi
