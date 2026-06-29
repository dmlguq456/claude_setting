#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ART="$ROOT/hooks/artifact-guard.sh"
GIT="$ROOT/hooks/git-state-guard.sh"
CODEX="$ROOT/adapters/codex/bin/preflight.sh"

PASS=0
FAIL=0
ok() { PASS=$((PASS+1)); printf '  ok  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf '  BAD %s\n' "$1"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "== artifact guard CLI =="
mkdir -p "$TMP/proj/.agent_reports/spec"
if "$ART" --file "$TMP/proj/.agent_reports/spec/prd.md" >/tmp/art.out 2>/tmp/art.err; then
  bad "new spec without research should fail"
else
  [ "$?" -eq 2 ] && ok "new spec without research exits 2" || bad "new spec wrong exit"
fi
mkdir -p "$TMP/proj/.agent_reports/research/seed"
if "$ART" --file "$TMP/proj/.agent_reports/spec/prd.md" --session test >/tmp/art.out 2>/tmp/art.err; then
  ok "new spec with research passes"
else
  bad "new spec with research should pass"
fi

echo "== git state guard CLI =="
mkdir -p "$TMP/repo"
(
  cd "$TMP/repo" || exit 1
  git init -q
  git config user.email test@example.com
  git config user.name Test
  printf 'a\n' > f
  git add f
  git commit -q -m init
)
if "$GIT" --file "$TMP/repo/f" >/tmp/git.out 2>/tmp/git.err; then
  ok "clean repo passes"
else
  bad "clean repo should pass"
fi
git -C "$TMP/repo" checkout --detach -q HEAD
if "$GIT" --file "$TMP/repo/f" >/tmp/git.out 2>/tmp/git.err; then
  bad "detached repo should fail"
else
  [ "$?" -eq 2 ] && ok "detached repo exits 2" || bad "detached repo wrong exit"
fi

echo "== codex preflight wrapper =="
git -C "$TMP/repo" switch -q -c work
if "$CODEX" write "$TMP/repo/f" testsid >/tmp/codex.out 2>/tmp/codex.err; then
  ok "codex preflight passes clean write"
else
  bad "codex preflight should pass clean write"
fi

printf 'PASS=%s FAIL=%s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
