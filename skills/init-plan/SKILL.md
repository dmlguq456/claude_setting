---
name: init-plan
description: Create a detailed implementation plan based on actual codebase
argument-hint: "<task description>"
---

## Language Rule
- Think and reason in English internally.
- When explaining something to the user, write in Korean.

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
Save English plan to: .claude_reports/plans/{YYYY-MM-DD}_{short-task-name}.md
Date: {YYYY-MM-DD}
{If a done/failed/partial plan exists: "Reference previous plan: [path], status: [status]"}
{If partial: "Failed steps from previous execution: [list from plan frontmatter failed_steps]"}

Read all relevant source files, analyze the current state, and create the plan.
Write the plan files directly. Return ONLY the file paths and a 3-5 line Korean summary. Do NOT return the plan content itself.
```

**IMPORTANT: Do NOT read, re-write, or duplicate the plan file yourself.** The agent writes it directly. You only receive paths and a summary.

## Post-Plan Review Loop (max 3 rounds)

Derive the review directory from the plan path: strip `.md` to get the folder name.
- Example: `.claude_reports/plans/2026-03-18_task.md` → `.claude_reports/plans/2026-03-18_task/`
- `mkdir -p {review_dir}` before invoking QA.

After the 기획팀 agent returns:
1. **Invoke the qa-team (품질관리팀) agent for plan feasibility review.**
   - Prompt: "Review this plan in plan review mode for feasibility. Plan file: [plan_path]. Write review results to: [review_dir]/review_round_{N}.md. Return ONLY the file path and a one-line verdict."
   - **Do NOT read the review file yourself unless you need to relay the verdict to the user.**
2. **Check the one-line verdict returned by the agent:**
   - **No 🔴 issues**: Loop ends. Proceed to **Korean Version Generation**.
   - **🔴 issues found**: Re-invoke 기획팀 to revise the plan based on the review:
     ```
     Refine mode. Update an existing plan based on QA review feedback.

     Plan file: {plan_path}
     QA review file: {review_dir}/review_round_{N}.md

     Read the QA review file, fix the 🔴 issues identified. Re-read source files if needed. Update the plan in-place.
     Return ONLY which steps were changed and a brief Korean summary. Do NOT return the plan content.
     ```
   - Then re-invoke 품질관리팀 to review the revised plan (write to `review_round_{N+1}.md`). Repeat until no 🔴 issues or max rounds reached.
3. **If 🔴 issues remain after 3 rounds**: Re-invoke 기획팀 one final time:
     ```
     Refine mode. Add unresolved issues to the plan.

     Plan file: {plan_path}
     QA review file: {review_dir}/review_round_{N}.md

     Add remaining 🔴 issues from the QA review to the plan's 리스크 section under a ## 미해결 이슈 subsection.
     Return a brief Korean summary of unresolved issues.
     ```
   - Then report to the user:
     - The plan path and summary
     - Which 🔴 issues were resolved during the loop
     - Which 🔴 issues remain unresolved and why

## Korean Version Generation
After the review loop completes (either no 🔴 issues or 3 rounds exhausted), invoke 기획팀 one final time:
```
Translate mode. Create the Korean version of the finalized plan.

English plan file: {plan_path}
Save Korean version to: {plan_path with .md replaced by _ko.md}

Create a full Korean translation of the English plan (NOT a summary). All sections with the same level of detail. Section titles: 목표, 현황 분석, 변경 계획, 리스크, 검증 방법. Code identifiers stay in English.
Return ONLY the file path.
```

Then report to the user:
- English plan path and Korean plan path
- Plan summary and QA verdict

## Task
$ARGUMENTS
