---
name: autopilot-dev
description: "Development pipeline — init-plan → refine-plan → execute-plan → run-test → final-report. Main Claude orchestrates via skills; research-team reviews plans as user proxy."
argument-hint: "<task description> [--from <step>] [--qa light|standard|thorough]"
---

## Language Rule
- When explaining something to the user, write in Korean.

## Argument Parsing
Parse `$ARGUMENTS` for optional flags:

**`--from <step>`** — resume from a specific step:
- `--from plan` → start from Step 1 (init-plan) — default
- `--from refine` → start from Step 2 (refine-plan)
- `--from execute` → start from Step 3 (execute-plan)
- `--from test` → start from Step 4 (run-test)
- `--from report` → start from Step 5 (final-report)

**`--qa <level>`** — override QA intensity for the entire pipeline:
- `--qa light` → sonnet, single reviewer
- `--qa standard` → opus, single reviewer (default)
- `--qa thorough` → opus, parallel reviewers
- If omitted, each skill auto-detects level based on scope.
- **Propagation**: Pass `--qa <level>` to init-plan and refine-plan as a flag. For execute-plan, run-test, and final-report, write `qa_level: <level>` into the English plan's frontmatter at Step 1 or Step 3 initialization.

The remaining text (after removing flags) is the task description or plan name.

**When starting from Step 2+**, the argument must be a plan name (not a task description). Use the Plan Resolution section below to locate the plan folder.

## Plan Resolution (canonical — keep in sync with execute-plan, run-test, final-report, refine-plan, autopilot-dev, autopilot-audit)
Resolve `$ARG` to a plan file path:
1. If it ends with `.md` → use as-is
2. If it's a directory path → append `/plan/plan.md`
3. Otherwise, fuzzy search: `ls -d .claude_reports/plans/*$ARG* 2>/dev/null`
   - **1 match** → use `{match}/plan/plan.md`
   - **Multiple matches** → prefer folder without `_audit`/`_fix_` suffix; if still multiple, ask user
   - **No match** → report error

## Pipeline
You (the main Claude) orchestrate by invoking each skill directly via the Skill tool. All tasks go through the full pipeline. The **연구팀** (research-team) agent is invoked only for Step 2 (plan review as user proxy) and Step 6 (meta-report).

### Step 1: init-plan
Invoke Skill: `init-plan` with the task description as args.
Wait for completion before proceeding.

### Step 2: refine-plan (연구팀 as user proxy)
1. Resolve the plan paths from the init-plan output:
   - `plan_folder` = `.claude_reports/plans/{YYYY-MM-DD}_{short-task-name}/`
   - `en_plan_path` = `{plan_folder}/plan/plan.md`
   - `ko_plan_path` = `{plan_folder}/plan/plan_ko.md`
   - `log_dir` = `{plan_folder}/`

2. Invoke the **연구팀** (research-team) agent:
   ```
   Review this plan as the user's proxy.

   Korean plan file: {ko_plan_path}
   English plan file: {en_plan_path}
   Review log file: {log_dir}/plan_reviews/research_review.md

   Read the Korean plan, cross-check against papers and domain knowledge,
   and write review memos as `<!-- memo: ... -->` comments in the Korean plan.
   Also write a structured review log to the specified log file path.
   Return a summary of memos added (or "no issues found").
   ```

3. If memos were added: Invoke Skill: `refine-plan` with the Korean plan path as args.
4. If no memos: Skip to Step 3.

### Step 3: execute-plan
Invoke Skill: `execute-plan` with the plan name/path as args.
Wait for completion before proceeding.

#### Status Check (between Step 3 and Step 4)
After execute-plan completes, read the English plan's frontmatter `status` field:
- `done` → proceed to Step 4.
- `partial` → proceed to Step 4 (test what succeeded).
- `failed` → execute-plan already rolled back source code. **STOP the pipeline.** Write pipeline_summary.md (status: failed) FIRST, then report failure to the user with the checklist summary. Do NOT proceed to run-test or final-report.

### Step 4: run-test
Invoke Skill: `run-test` with the plan name/path as args.
Wait for completion before proceeding.

## Retry Budget (Total)
- run-test internal hotfix loop: max 2 attempts per test run
- autopilot-dev retry loop: max 1 pipeline-level retry
- Total theoretical maximum: 2 (first run-test) + 2 (second run-test after retry) = 4 hotfix attempts
- At each run-test invocation, the hotfix counter resets.

#### Test Failure → Retry Loop (max 1 pipeline-level retry)
If run-test reports failure (after its internal hotfix loop of 2 attempts):

1. **Collect failure context**: Read `test_logs/test_report.md`, `test_reviews/test_review_coverage.md`, `test_reviews/test_review_accuracy.md`, and `plan/checklist.md`. Synthesize a concise failure summary (keep in memory).

2. **Rollback source code only** (preserve plan/log files):
   - Read Safety commit hash from `plan/checklist.md` header: `Safety commit: {hash}`
   - Run: `git checkout <safety-commit> -- <changed paths>` (NOT `.claude_reports/`)
   - Verify with `git status`

3. **Write failure memos into Korean plan**: Append `<!-- memo: [테스트 실패] Level N 실패. 에러: {error summary}. Hotfix 2회 실패. 대안 필요. 참조: test_logs/test_report.md -->` at relevant steps in `plan/plan_ko.md`.

4. **Reset checklist**: Reset all step marks in `plan/checklist.md` to `[ ]`.

5. **Loop back to Step 2**: Invoke Skill: `refine-plan` with the plan path (QA review loop runs as usual, max 3 rounds).

6. **Re-execute**: Invoke Skill: `execute-plan` with the same plan path.

7. **Re-test**: If plan status is not `failed`, invoke Skill: `run-test`.
   - **Pass** → continue to Step 5 (final-report).
   - **Fail again** → rollback, **STOP**. Write pipeline_summary.md (status: failed, note both attempts) FIRST, then report to user. Do NOT proceed to final-report.

### Step 5: final-report
Invoke Skill: `final-report` with the plan name/path as args.

### Step 6: Pipeline Summary Report
**Always write** `{log_dir}/pipeline_summary.md` — both on success AND failure.

**pipeline_summary.md must be written BEFORE reporting to the user, regardless of success/failure path.** This is the first action upon reaching any terminal state (success, partial, failed, or stop). Do NOT report to the user first and write the summary later.

This is a process log and artifact index — NOT a change analysis (that's final-report's job).

```markdown
# Pipeline Summary: {task name}

- **Date**: {YYYY-MM-DD}
- **Plan**: {en_plan_path}
- **Status**: done / partial / failed

## Process Log
| Step | Skill | Result | Notes |
|---|---|---|---|
| 1 | init-plan | | |
| 2 | refine-plan | | |
| 3 | execute-plan | | |
| 4 | run-test | | |
| 4R | retry (refine→execute→test) | | |
| 5 | final-report | | |

## Artifacts
- Plan (EN/KO), Checklist: {plan_folder}/plan/
- Dev logs/reviews: {plan_folder}/dev_logs/, dev_reviews/
- Test report/reviews: {test_log_path}
- Final report: {final_report_path}
```

Then report to the user: pipeline_summary.md path + 2-3 line verdict.

## Safety Rules
- If execution fails catastrophically (plan status = `failed`), stop and report to user immediately.
- Do NOT skip Step 4 (testing) — always verify.
- Do NOT intervene in individual skill execution — let each skill handle its own QA loops and phase reviews.
