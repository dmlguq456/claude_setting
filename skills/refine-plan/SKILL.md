---
name: refine-plan
description: Reflect user memos/comments in a plan and update it (do NOT implement)
argument-hint: "<path to plan file>"
---

## Language Rule
- Think and reason in English internally.
- When explaining something to the user, write in Korean.

## Delegate to 기획팀
Invoke the **plan-team** (기획팀) agent as a subagent with the following prompt:

```
Refine mode. Update an existing plan based on user memos.

Korean plan file: {$ARGUMENTS}
English plan file: {$ARGUMENTS with _ko.md replaced by .md}

Read the Korean plan, find all user memos, re-read source files if needed, update the Korean plan in-place, and sync changes to the English plan.
Return which steps were changed and a brief summary.
```

## Post-Refine Review Loop (max 3 rounds)
After the 기획팀 agent returns:
1. **Invoke the qa-team (품질관리팀) agent to review the changed steps.**
   - Prompt: "Review the changed steps in plan review mode. Plan file: [path], Changed steps: [list from 기획팀]"
2. **Check review results:**
   - **No 🔴 issues**: Loop ends. Report changed steps and review results to the user.
   - **🔴 issues found**: Re-invoke 기획팀 to fix:
     ```
     Refine mode. Update an existing plan based on QA review feedback.

     Plan file: {path}
     QA review feedback:
     {🔴 issues from 품질관리팀 review}

     Fix the issues identified by QA. Re-read source files if needed. Update the plan in-place.
     Return which steps were changed and a brief summary.
     ```
   - Then re-invoke 품질관리팀 to review. Repeat until no 🔴 issues or max rounds reached.
3. **If 🔴 issues remain after 3 rounds**: Add unresolved issues to the plan's **리스크** section with a `## 미해결 이슈` subsection, then report to the user including:
   - Which steps were changed by user memos
   - Which 🔴 issues were resolved during the loop
   - Which 🔴 issues remain unresolved and why

## Task
Refine the plan at: $ARGUMENTS
