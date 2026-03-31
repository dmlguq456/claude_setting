---
name: autopilot-audit
description: "Audit pipeline — reviews all changes from a completed dev cycle with fresh eyes. Runs: init-plan → [review (optional)] → execute-plan → run-test → final-report"
argument-hint: "<dev plan name or path> [--from <step>] [--qa light|standard|thorough]"
---

## Language Rule
- When explaining something to the user, write in Korean.

## Argument Parsing
Parse `$ARGUMENTS` for optional flags:

**`--from <step>`** — resume from a specific step within the audit cycle:
- `--from plan` → start from Step 1 (init-plan) — default
- `--from execute` → start from Step 2 (execute-plan). Requires existing audit plan.
- `--from test` → start from Step 3 (run-test). Requires existing audit plan.
- `--from report` → start from Step 4 (final-report). Requires existing audit plan.

**`--qa <level>`** — override QA intensity:
- `--qa light` / `--qa standard` / `--qa thorough`
- Same propagation rules as autopilot-dev.

The remaining text (after removing flags) is the **dev plan name or path** (not a task description).

## Plan Resolution (canonical — keep in sync with execute-plan, run-test, final-report, refine-plan, autopilot-dev, autopilot-audit)
Resolve $ARG (remaining text after flag removal) to the dev plan file path:
1. Ends with `.md` → use as-is
2. Directory path → append `/plan/plan.md`
3. Otherwise fuzzy: `ls -d .claude_reports/plans/*$ARG* 2>/dev/null`
   - 1 match → `{match}/plan/plan.md`
   - Multiple → exclude `_audit`/`_fix_` folders; if still multiple, ask user
   - No match → report error

After resolving: read `status` from dev plan frontmatter — if `failed`, stop. Read `$DEV_SAFETY_COMMIT` from `plan/checklist.md` header (`Safety commit:` line); fallback: `git log --oneline -1`.

## Existing Audit Plan Detection
Before creating a new audit plan, check if an audit plan already exists:
- Search for `{dev_plan_folder_name}_audit` in `.claude_reports/plans/`
- If found AND `--from plan` (default):
  - Read its frontmatter `status`:
    - `active`: An incomplete audit exists. Ask the user: "기존 audit plan이 있습니다. 이어서 진행할까요, 새로 만들까요?"
    - `done`/`partial`/`failed`: Note for reference, create a new audit plan.
- If found AND `--from` is refine/execute/test/report: use the existing audit plan.

## Pipeline

### Step 1: Generate audit task + init-plan
Construct the audit task description:
```
Audit changes from: {dev_en_plan_path}
Git diff: {dev-safety-commit}..HEAD

Review all code changes and identify:
1. Bugs — logic errors, off-by-one, wrong variable, missing edge cases
2. Consistency — naming, style, patterns inconsistent with surrounding code
3. Safety — tensor shape mismatches, unchecked None/empty, device mismatches
4. Missed spots — callers not updated, dead code left behind, stale comments
5. Suboptimal patterns — unnecessary copies, redundant operations, unclear logic

Scope: ONLY files changed in the dev cycle.
```

Invoke Skill: `init-plan` with the audit task description.
- Plan folder: `.claude_reports/plans/{YYYY-MM-DD}_{original-task-name}_audit/`
- Wait for completion.

### Step 1.5: Quick review (optional)

**Trigger:** run if EITHER: (1) audit plan has >10 steps, OR (2) git diff touches `model.py`, `modules/module.py`, or `modules/network.py`.

**When triggered:** Invoke 연구팀 with the audit plan path for one lightweight review pass (memo insertion only — no refine-plan loop). Include: `Review log file: {log_dir}/plan_reviews/research_review.md`. Wait for completion.

**Otherwise:** skip and proceed to Step 2.

### Step 2: execute-plan
Invoke Skill: `execute-plan` with the audit plan path.
- Status check: same rules as autopilot-dev Step 3.

### Step 3: run-test
Invoke Skill: `run-test` with the audit plan path.
- **NO retry loop** (max 0 retries). If tests fail after the internal hotfix loop (2 attempts):
  - Rollback audit changes only: determine changed paths from checklist or git diff. The audit plan's safety commit is stored in its own `plan/checklist.md` header, written by execute-plan during audit execution. Run `git checkout <audit-safety-commit> -- <changed paths>`
  - This restores to post-dev state (dev changes are already committed).
  - Write pipeline_summary.md (status: failed) FIRST, then report to user, and stop.

### Step 4: final-report
Invoke Skill: `final-report` with the audit plan path.

### Step 5: Pipeline Summary Report
**pipeline_summary.md must be written BEFORE reporting to the user, regardless of success/failure path.** This is the first action upon reaching any terminal state (success, partial, failed, or stop).

Write `{audit_log_dir}/pipeline_summary.md`:

```markdown
# Audit Pipeline Summary: {task name}

- **Date**: {YYYY-MM-DD}
- **Dev Plan**: {dev_en_plan_path}
- **Audit Plan**: {audit_en_plan_path}
- **Dev Safety Commit**: {dev plan's checklist.md Safety commit hash}
- **Status**: done / partial / failed

## Process Log
| Step | Skill | Result | Notes |
|---|---|---|---|
| 1 | init-plan (audit) | created / resumed | plan path |
| 1.5 | 연구팀 review | done / skipped | trigger: step count >10 / hard constraint files / n/a |
| 2 | execute-plan (audit) | done / partial / failed | [x] N, [FAIL] N, [SKIP-DEP] N |
| 3 | run-test (audit) | pass / fail | levels passed, hotfix attempts if any |
| 4 | final-report (audit) | generated | report path |

## Artifacts
- Audit Plan (EN/KO): {path}
- Checklist: {path}
- Dev logs/reviews: {path}/dev_logs/, {path}/dev_reviews/
- Test report + reviews: {path}
- Final report: {path}
```

Then report to the user: pipeline_summary.md path + 2-3 line verdict.

## Safety Rules
- Audit failures do NOT roll back dev cycle changes — dev changes are already committed.
- Do NOT skip Step 4 (testing) — always verify.
- Do NOT intervene in individual skill execution — let each skill handle its own QA loops.
- If execution fails catastrophically (plan status = `failed`), stop and report to user immediately.
