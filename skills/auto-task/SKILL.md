---
name: auto-task
description: Fully automated task pipeline — plan, execute, and test without user intervention
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

Read relevant project documentation, assess complexity, and run the full pipeline autonomously.
Report results when complete.
```

**IMPORTANT:** Do NOT intervene or add your own steps. The PM agent handles the entire workflow. Simply relay the PM agent's final report to the user.
