---
name: autopilot-debug
description: "Debug pipeline — diagnose runtime errors, trace root cause, fix, and verify. Takes an error description or log, traces through code, creates a fix plan, and executes it."
argument-hint: "<error description or log> [--autonomy proactive|standard|passive] [--qa light|standard|thorough]"
---

## Language Rule
- When explaining something to the user, write in Korean.

## Argument Parsing
Parse `$ARGUMENTS` for optional flags:

**`--autonomy <level>`** — same as autopilot-dev. Default: `standard` (debug pipeline defaults to standard because diagnosis confirmation is a meaningful checkpoint).
Same validation rules as autopilot-dev (invalid value → fallback to `standard` for debug, with warning).
Propagated to all sub-skill invocations.

**`--qa <level>`** — override QA intensity:
- `--qa light` / `--qa standard` (default) / `--qa thorough`
- Propagated to all sub-skill invocations.

The remaining text is the **error description**. This can be:
- An error message (e.g., "KeyError: 'optimizer_state_dict' during training")
- A log snippet (e.g., pasted traceback)
- A symptom description (e.g., "학습 시 2 epoch 이후 loss가 NaN")
- A file path to an error log

## Autonomy Gating

| Decision Point | Severity | proactive | standard | passive |
|---|---|---|---|---|
| Confirm diagnosis before fix | Significant | auto-proceed | ask (current, default for debug) | ask |
| Ambiguous root cause (multiple possible) | Critical | ask (current) | ask | ask |
| Fix verification failed → stop | Critical | auto-rollback + report | ask | ask |
| Environment issue (not code bug) | Significant | auto-report env steps | ask: "환경 문제로 확인됩니다. 코드 수정 대신 환경 조치 안내만 할까요?" | ask |

When the pipeline reaches a gated decision point:
- If the current autonomy level includes that severity → **pause and ask** the user.
- Otherwise → **proceed with the default action** (described in the proactive column).
- All "ask" prompts must include: (1) the situation summary, (2) available options, (3) the default action if no response.
- **Logging**: After each decision (auto or user), record in memory: `{step} | {decision description} | {user response or "auto"} | {action taken}`. These records are written to the Decision Points table in `pipeline_summary.md` when it is created at pipeline end.

## Pipeline

### Step 1: Diagnose — trace root cause
Do NOT delegate this step. You (the main Claude) perform the diagnosis directly.

1. **Parse the error & check runtime context**: Extract error type, message, traceback, affected file/line. Run `git log --oneline -10` and `git diff HEAD~3`; check config/checkpoint files if relevant.
2. **Read the relevant code**: Follow the call stack or error location. Read the source files.
3. **Identify root cause**: Determine whether the issue is in:
   - Code logic (bug introduced by recent changes)
   - Environment (missing files, wrong config state, missing dependencies)
   - Data (corrupted checkpoint, wrong format, missing keys)
   - Interaction (code is correct individually but breaks when combined)
4. **Report diagnosis to user** in Korean:
   ```
   ## 진단 결과
   - **에러**: {error type and message}
   - **위치**: {file:line}
   - **근본 원인**: {root cause explanation}
   - **영향 범위**: {what else might be affected}
   - **수정 방향**: {proposed fix approach}
   ```
5. **Diagnosis confirmation** (gated):
   - If `proactive`: skip confirmation, auto-proceed to fix plan.
   - If `standard` or `passive`: ask for confirmation before proceeding to fix. If the user disagrees or wants a different approach, adjust.
   - Note: autopilot-debug defaults to `standard`, so diagnosis confirmation remains the default behavior.

### Step 2: Create fix plan
Invoke Skill: `init-plan` with a fix task description:
```
Fix: {root cause summary}

Error: {error message}
Location: {file:line}
Root cause: {diagnosis from Step 1}
Proposed fix: {fix approach}

Scope: Minimal — fix the root cause only. Do not refactor or improve surrounding code.
```

The plan folder will be: `.claude_reports/plans/{YYYY-MM-DD}_fix_{short-error-name}/`

### Step 3: Review fix plan (QA only, skip research-team)
- Skip 연구팀 review — debugging fixes should be fast.
- QA review still runs via init-plan's built-in Post-Plan Review Loop.
- If QA has 🔴 issues, let the review loop resolve them (max 3 rounds as usual).

### Step 4: Execute fix
Invoke Skill: `execute-plan` with the fix plan path.
- Status check: if `failed`, report to user and stop.

### Step 5: Verify fix
Invoke Skill: `run-test` with the fix plan path.

**Additional verification**: After run-test passes, reproduce the original error scenario:
- If the user provided a specific command that triggered the error, re-run it.
- If the error was during training, run a short training session (1-2 epochs).
- If the error was during inference, run an inference test.
- Report whether the original error is resolved.

If tests fail or the original error persists (gated):
- If `proactive`: auto-rollback and then proceed to reporting (current behavior).
- If `standard` or `passive`: ask before rollback: "수정 검증이 실패했습니다. 롤백할까요, 다시 시도할까요? (기본값: 롤백)"

On rollback path:
1. **Rollback**: Determine changed paths from checklist or git diff. Read the Safety commit hash from the fix plan's `plan/checklist.md` header line: `Safety commit: {hash}`. Run `git checkout <safety-commit> -- <changed paths>`
2. **Write pipeline_summary.md (status: unresolved)** BEFORE reporting to the user. See Step 6 for the format.
3. **Report to user** with:
   - Original diagnosis
   - What was attempted
   - Why it didn't work
   - Suggested manual investigation steps

### Step 6: Report
Invoke Skill: `final-report` with the fix plan path.

**pipeline_summary.md must be written BEFORE reporting to the user, regardless of success/failure path.** This is the first action upon reaching any terminal state (fixed, partial, unresolved, or stop). On failure path (Step 5 rollback), pipeline_summary.md is written as part of that failure path — do NOT skip it.

Write `{log_dir}/pipeline_summary.md`:
```markdown
# Debug Pipeline Summary: {error name}

- **Date**: {YYYY-MM-DD} | **Status**: fixed / partial / unresolved | **Attempts**: {N}
- **Error**: {error type and message}
- **Root Cause**: {diagnosis}
- **Fix Plan**: {plan path}
- **Autonomy**: {autonomy_level}

## Process Log
| Step | Action | Result |
|---|---|---|
| 1 | Diagnosis | {root cause} @ {file:line} |
| 2 | init-plan + QA | {plan path} |
| 4 | execute-plan | done / partial / failed |
| 5 | run-test | pass / fail |
| 6 | final-report | {report path} |

## Decision Points
| Step | Decision | User Response | Action Taken |
|---|---|---|---|
| (filled from orchestrator's in-memory decision log) |
```

When writing pipeline_summary.md, populate the Decision Points table from the in-memory decision records. If no decisions were recorded, write: `| - | No gated decisions triggered | - | - |`.

Report to user: summary + verdict.

## Safety Rules
- **Minimal scope**: Fix the bug only. Do not refactor, improve, or clean up surrounding code.
- **Preserve existing behavior**: The fix should not change behavior for cases that were already working.
- Before fixing, confirm the diagnosis per the Autonomy Gating rule (Diagnosis confirmation, Significant severity).
- If the root cause is ambiguous (multiple possible causes), list them and ask the user which to investigate first.
- If the root cause is an environment issue (not a code bug), follow the Environment issue autonomy gate: `proactive` auto-reports env fix steps, `standard`/`passive` asks per the Autonomy Gating table.
