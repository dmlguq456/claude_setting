#!/usr/bin/env sh
# OpenCode adapter-owned material web-image-search launcher.
set -eu

usage() {
  cat <<'EOF'
usage: web-image-search.sh [--check] <query> [--max-results N] [--out <file>]

Checks or runs a configured web image search provider through an OpenCode-owned
material tool-contract surface. Set OPENCODE_WEB_IMAGE_SEARCH_CMD or
AGENT_WEB_IMAGE_SEARCH_CMD to an executable provider command. Exit 69 means no
provider is configured or available.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

printf 'adapter=opencode\n'
printf 'runtime_surface=adapter-owned-web-image-search\n'
printf 'tool_contract=web-image-search\n'

if [ "$#" -eq 0 ]; then
  printf 'status=tool-contract\n'
  printf 'tool_contract_check=adapters/opencode/bin/preflight.sh web-image-search --check <query>\n'
  printf 'fallback=satisfy-tool-contract-or-report-unavailable\n'
  exit 0
fi

check_only=0
max_results=3
out=""
query=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --check)
      check_only=1
      shift
      ;;
    --max-results)
      [ "$#" -ge 2 ] || { echo "opencode web-image-search: --max-results requires a value" >&2; exit 64; }
      max_results=$2
      shift 2
      ;;
    --out)
      [ "$#" -ge 2 ] || { echo "opencode web-image-search: --out requires a file" >&2; exit 64; }
      out=$2
      shift 2
      ;;
    --*)
      echo "opencode web-image-search: unknown option: $1" >&2
      exit 64
      ;;
    *)
      if [ -z "$query" ]; then
        query=$1
      else
        query="$query $1"
      fi
      shift
      ;;
  esac
done

[ -n "$query" ] || { echo "opencode web-image-search: query required" >&2; exit 64; }
case "$max_results" in
  ''|*[!0-9]*) echo "opencode web-image-search: --max-results must be an integer" >&2; exit 64 ;;
esac

provider=${OPENCODE_WEB_IMAGE_SEARCH_CMD:-${AGENT_WEB_IMAGE_SEARCH_CMD:-}}
if [ -z "$provider" ] || ! command -v "$provider" >/dev/null 2>&1; then
  printf 'status=tool-contract\n'
  printf 'reason=web-image-search-provider-unavailable\n'
  printf 'query=%s\n' "$query"
  exit 69
fi

printf 'provider=%s\n' "$provider"
printf 'query=%s\n' "$query"
printf 'max_results=%s\n' "$max_results"
if [ "$check_only" -eq 1 ]; then
  printf 'check=provider-available\n'
  printf 'status=ok\n'
  exit 0
fi

if [ -n "$out" ]; then
  "$provider" "$query" "$max_results" >"$out"
  rc=$?
  printf 'output=%s\n' "$out"
else
  "$provider" "$query" "$max_results"
  rc=$?
fi
if [ "$rc" -eq 0 ]; then
  printf 'status=ok\n'
else
  printf 'status=failed\n'
fi
exit "$rc"
