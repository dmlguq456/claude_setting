---
name: init-plan
description: Create a detailed implementation plan based on actual codebase
argument-hint: "<task description> [--qa light|standard|thorough]"
---

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## Pre-Check
- Check if a similar plan already exists in `.claude_reports/plans/`:
  - `active`: Notify the user and ask whether to continue it or create a new one. Do NOT proceed until confirmed.
  - `partial`: Notify the user that a previous attempt partially completed. Ask whether to create a new plan covering the failed steps or start fresh. Do NOT proceed until confirmed.
  - `done`/`failed`: Note it for reference, proceed with new plan creation.

## Delegate to 기획팀
Invoke the **plan-team** (기획팀) agent as a subagent with the following prompt:

```
Plan mode. Create a new implementation plan.

Task: {$ARGUMENTS}
Save English plan to: .claude_reports/plans/{YYYY-MM-DD}_{short-task-name}/plan/plan.md
Date: {YYYY-MM-DD}
{If a done/failed/partial plan exists: "Reference previous plan: [path], status: [status]"}
{If partial: "Failed steps from previous execution: [list from plan frontmatter failed_steps]"}

Read all relevant source files, analyze the current state, and create the plan.
Write the plan files directly. Return ONLY the file paths and a 3-5 line Korean summary. Do NOT return the plan content itself.
```

**IMPORTANT: Do NOT read, re-write, or duplicate the plan file yourself.** The agent writes it directly. You only receive paths and a summary.

## QA Scaling
If `$ARGUMENTS` contains `--qa light|standard|thorough`, use that level and strip the flag from the task description. Otherwise, auto-detect from the plan's scope. When `qa_level` is set in plan frontmatter, it overrides auto-detect.

| Level | Auto-detect condition | Action |
|---|---|---|
| **Light** | ≤3 steps, mechanical, single-variant | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | 4-10 steps, logic changes, single module | 1× 품질관리팀 (default opus) |
| **Thorough** | >10 steps, cross-module/variant, architectural | 2-3× 품질관리팀 in parallel (opus): Agent A correctness, B completeness, C risk (optional, >15 steps); each writes `round_{N}_{focus}.md`; all 🔴 issues must be resolved |

## Post-Plan Review Loop (max 3 revision rounds)

The log directory is the task root folder (parent of `plan/`). Example: `.claude_reports/plans/2026-03-18_task/plan/plan.md` → log dir is `.claude_reports/plans/2026-03-18_task/`. Run `mkdir -p {log_dir}/plan_reviews` before invoking QA.

**Round counting:** Initialize `round = 0`. A round = one plan-team fix → QA review cycle; all parallel Thorough agents count as one round. Increment `round` only when QA is re-invoked after a revision. "max 3 rounds" means 기획팀 is invoked at most 3 times to fix issues.

**QA level lock:** QA level is determined once at loop start; only upward escalation allowed (no downgrade). If `--qa` was NOT specified, the orchestrator MAY upgrade once (starting round 2) when 🔴 count ≥3 in the one-line verdict (no review file reading needed); round counter does NOT reset. If `--qa` was manually specified, no change allowed.

After the 기획팀 agent returns:
1. **Assess QA level** from plan scope per the QA Scaling table above.
2. **Invoke 품질관리팀:** Prompt: "Review this plan in plan review mode for feasibility. Plan file: [plan_path]. Write review results to: [log_dir]/plan_reviews/round_{N}.md. Return ONLY the file path and a one-line verdict."
   - Light: pass `model: 'sonnet'`. Thorough: 2-3 parallel agents with focus suffix and separate output files. Do NOT read the review file unless relaying verdict to user.
3. **Check one-line verdict:**
   - **No 🔴**: Loop ends → proceed to Korean Version Generation.
   - **🔴 found**: Re-invoke 기획팀: "Refine mode. Plan file: {plan_path}. QA review: {log_dir}/plan_reviews/round_{N}.md. Fix 🔴 issues. Return only changed steps + brief Korean summary." Increment `round`, re-invoke 품질관리팀. Repeat until no 🔴 or `round >= 3`.
4. **If 🔴 remain after `round >= 3`**: Invoke 기획팀: "Refine mode. Add remaining 🔴 issues to the plan's 리스크 section under ## 미해결 이슈. Return brief Korean summary." Then report to user: plan path, resolved issues, and unresolved issues with reasons.

## Korean Version Generation
After the review loop completes, invoke 기획팀 one final time:
```
Translate mode. English plan file: {plan_path}. Save Korean version to: {same directory}/plan_ko.md.
Full Korean translation (NOT a summary). Same detail level. Section titles: 목표, 현황 분석, 변경 계획, 리스크, 검증 방법. Code identifiers stay in English. Return ONLY the file path.
```
Then report to the user: English plan path, Korean plan path, plan summary, and QA verdict.

## Task
$ARGUMENTS
