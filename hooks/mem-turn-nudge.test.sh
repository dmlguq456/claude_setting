#!/usr/bin/env bash
# Regression test for mem-turn-nudge.sh (B2 turn-counter, spec v5 Cluster B).
# Fully isolated via MEM_STORE temp dir + MEM_NUDGE_INTERVAL — never touches real ~/.claude state.
# Added 2026-06-16 (Cluster B doc-sync cycle) — commit 5a9ea18 claimed standalone-verified but committed no test.
set -u

HOOK="$(cd "$(dirname "$0")" && pwd)/mem-turn-nudge.sh"
[ -f "$HOOK" ] || { echo "FAIL: hook not found at $HOOK"; exit 1; }

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf '  ✅ %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf '  ❌ %s\n' "$1"; }

run() {  # $1=event $2=prompt ; uses $TMP/$N/$SID env ; echoes hook stdout
  printf '{"hook_event_name":"%s","session_id":"%s","prompt":"%s"}' "$1" "$SID" "$2" \
    | MEM_STORE="$TMP" MEM_NUDGE_INTERVAL="$N" bash "$HOOK"
}

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
N=3; SID="testsid"

# seed a memory.db with a stable mtime (simulates an already-populated store)
: > "$TMP/memory.db"; touch -d '2026-06-16 00:00:00' "$TMP/memory.db"

echo "== T1: turns 1..N-1 silent, turn N emits nudge =="
out1="$(run UserPromptSubmit 'hello one')"
out2="$(run UserPromptSubmit 'hello two')"
[ -z "$out1$out2" ] && ok "turns 1..N-1 ($((N-1))) silent" || bad "turns 1..N-1 should be silent, got: $out1$out2"
out3="$(run UserPromptSubmit 'hello three')"
echo "$out3" | grep -q '"hookSpecificOutput"' && echo "$out3" | grep -q "turn-counter" && ok "turn N emits nudge" || bad "turn N should emit nudge, got: $out3"
echo "$out3" | grep -q "${N}턴" && ok "nudge text interpolates actual N (=$N)" || bad "nudge should mention N=$N, got: $out3"

echo "== T2: counter resets after firing (turn N+1 silent) =="
out4="$(run UserPromptSubmit 'hello four')"
[ -z "$out4" ] && ok "turn N+1 silent (counter reset after fire)" || bad "turn N+1 should be silent, got: $out4"

echo "== T3: memory write (db mtime bump) resets counter + silent =="
run UserPromptSubmit 'hello five' >/dev/null    # counter -> 2 (T2 turn4 reset to 1, here ->2)
touch -d '2026-06-16 12:00:00' "$TMP/memory.db"  # simulate a memory write (later mtime)
outw="$(run UserPromptSubmit 'hello six')"
[ -z "$outw" ] && ok "write detected → counter reset, silent" || bad "post-write turn should be silent, got: $outw"
saved_cnt="$(sed -n '1p' "$TMP/.turn-state-$SID")"
[ "$saved_cnt" = "1" ] && ok "post-write counter restarted at 1" || bad "post-write counter should be 1, got: $saved_cnt"

echo "== T4: no phantom write on first turn (fresh session) =="
SID2="freshsid"
printf '{"hook_event_name":"UserPromptSubmit","session_id":"%s","prompt":"x"}' "$SID2" \
  | MEM_STORE="$TMP" MEM_NUDGE_INTERVAL="$N" bash "$HOOK" >/dev/null
fc="$(sed -n '1p' "$TMP/.turn-state-$SID2")"
[ "$fc" = "1" ] && ok "first turn → counter 1 (no phantom-write inflation)" || bad "first turn counter should be 1, got: $fc"

echo "== T5: non-UserPromptSubmit event → silent exit 0 =="
out_se="$(run SessionStart 'x')"; rc=$?
[ -z "$out_se" ] && [ "$rc" = "0" ] && ok "SessionStart → silent, exit 0" || bad "SessionStart should be silent exit0 (out='$out_se' rc=$rc)"

echo "== T6: broken stdin → exit 0 fail-safe (no crash) =="
printf 'not json at all' | MEM_STORE="$TMP" MEM_NUDGE_INTERVAL="$N" bash "$HOOK" >/dev/null 2>&1
[ "$?" = "0" ] && ok "broken stdin → exit 0" || bad "broken stdin should exit 0"

echo "== T7: stale state-file GC (3일+ 비활성 삭제) =="
old="$TMP/.turn-state-stalesession"; : > "$old"; touch -d '2026-06-10 00:00:00' "$old"  # 6 days old
run UserPromptSubmit 'trigger gc' >/dev/null
[ ! -e "$old" ] && ok "stale (>3d) state file GC'd" || bad "stale state file should be deleted"
[ -e "$TMP/.turn-state-$SID" ] && ok "fresh state file preserved by GC" || bad "fresh state file wrongly deleted"

echo
echo "RESULT: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" = "0" ]
