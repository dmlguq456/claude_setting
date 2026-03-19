---
name: auto-by-pm
description: Fully automated task pipeline via PM agent — init-plan → refine-plan (by PM) → execute-plan → run-test
argument-hint: "<task description>"
---

## Language Rule
- When explaining something to the user, write in Korean.

## Task
Invoke the **PM** agent as a subagent with the following prompt:

```
Autonomous task execution.

Task: {$ARGUMENTS}
Date: {YYYY-MM-DD}

Run the full pipeline: init-plan → refine-plan (1 round, you act as the user) → execute-plan → run-test.
Report results when complete.
```

**IMPORTANT:** Do NOT intervene or add your own steps. The PM agent handles the entire workflow. Simply relay the PM agent's final report to the user.
