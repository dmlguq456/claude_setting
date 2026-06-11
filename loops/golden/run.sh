#!/bin/bash
# Golden set runner — 지침 회귀 테스트. 사용: run.sh [case_id ...]
set -u
GOLD="$HOME/.claude/loops/golden"
CLAUDE_BIN="$HOME/.local/bin/claude"
TOOLS="Bash,Read,Write,Edit,Glob,Grep,Skill,Agent,TodoWrite"
STAMP=$(date +%F_%H%M)
RESULTS="$GOLD/results/$STAMP"
mkdir -p "$RESULTS"

cases=("$@")
[ ${#cases[@]} -eq 0 ] && cases=($(ls "$GOLD/cases"))

declare -A verdicts
for c in "${cases[@]}"; do
  CASE_DIR="$GOLD/cases/$c"
  [ -d "$CASE_DIR" ] || { echo "SKIP $c (없음)"; continue; }
  MAX_TURNS=""; TIMEOUT=1800
  [ -f "$CASE_DIR/config" ] && . "$CASE_DIR/config"

  WORK=$(mktemp -d "/tmp/golden-$c-XXXX")
  echo "▶ $c (work=$WORK)"
  bash "$CASE_DIR/fixture.sh" "$WORK" || { verdicts[$c]="FIXTURE-ERR"; continue; }

  T="$RESULTS/$c.transcript.txt"
  ( cd "$WORK/repo" && timeout "$TIMEOUT" "$CLAUDE_BIN" -p "$(cat "$CASE_DIR/prompt.md")" \
      --allowedTools "$TOOLS" ${MAX_TURNS:+--max-turns "$MAX_TURNS"} ) > "$T" 2>&1
  rc=$?

  if out=$(bash "$CASE_DIR/assert.sh" "$WORK" "$T" 2>&1); then
    verdicts[$c]="PASS"
  else
    verdicts[$c]="FAIL"
  fi
  echo "$out" | tee "$RESULTS/$c.assert.txt"
  echo "  → ${verdicts[$c]} (claude exit $rc)"

  # FAIL 자동 진단 — 원인 추정 + 수정안 초안까지 (적용은 사용자 서명)
  if [ "${verdicts[$c]}" = "FAIL" ]; then
    timeout 600 "$CLAUDE_BIN" -p "golden set 케이스 FAIL 진단. 케이스 정의: $CASE_DIR (prompt.md=사용자 발화, assert.sh=판정). assert 출력: $RESULTS/$c.assert.txt. transcript: $T. fixture 결과물: $WORK.
이 자료를 읽고 (1) 위반 행동이 정확히 무엇이었나 (2) 어느 지침이 닿지 않았거나 모호했나 (3) 수정안 — 지침 diff 초안 또는 hook 승격 제안 중 택1, 적용 명령 포함 — 을 $RESULTS/$c.diagnosis.md 에 한국어로 간결히 작성하라. 지침 파일을 직접 수정하지 말 것 (진단·제안만)." \
      --allowedTools "Bash,Read,Glob,Grep,Write" --max-turns 25 >> "$RESULTS/$c.diagnosis.log" 2>&1
    [ -f "$RESULTS/$c.diagnosis.md" ] && echo "  진단서: $RESULTS/$c.diagnosis.md"
  fi
done

{
  echo "# Golden run $STAMP"
  echo
  echo "| case | verdict |"
  echo "|---|---|"
  for c in "${cases[@]}"; do echo "| $c | ${verdicts[$c]:-?} |"; done
} | tee "$RESULTS/summary.md"

# 옵션: 응답규율 채점 pass (약자 풀이·번역체·약속-행동) — transcript 일괄 LLM 채점
if [ "${RUN_JUDGE:-0}" = "1" ]; then
  "$CLAUDE_BIN" -p "$(cat "$GOLD/judge.md")

대상 transcript 디렉토리: $RESULTS (각 *.transcript.txt)" \
    --allowedTools "Read,Glob,Grep,Write" > "$RESULTS/judge.md" 2>&1
  echo "judge → $RESULTS/judge.md"
fi
