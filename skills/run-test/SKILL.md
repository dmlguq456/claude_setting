---
name: run-test
description: Run functional tests after execute-plan or on demand to verify code correctness
argument-hint: "<plan file path or test scope description>"
---

## Language Rule
- Think and reason in English internally.
- When reporting results to the user, write in Korean.

## Delegate to 테스트팀
Invoke the **test-team** (테스트팀) agent as a subagent with the following prompt:

- If $ARGUMENTS points to a plan file:
  ```
  Run graduated tests for plan: {$ARGUMENTS}
  Read the plan's 검증 방법 section and the log directory's checklist_eng.md to identify targets.
  Execute Level 1 → 2 → 3 → 4 → 5 in order, stopping on first failure.
  ```

- If $ARGUMENTS is a file/directory path:
  ```
  Run graduated tests on: {$ARGUMENTS}
  Execute Level 1 → 2 → 3 → 4 → 5 in order, stopping on first failure.
  Skip levels that don't apply (e.g., Level 4 if no plan file).
  ```

- If $ARGUMENTS is empty:
  ```
  Run graduated tests on recently changed files.
  Use git diff --name-only HEAD~1 to find targets.
  Execute Level 1 → 2 → 3 → 4 → 5 in order, stopping on first failure.
  Skip levels that don't apply (e.g., Level 4 if no plan file).
  ```

## Post-Test
After the test-runner agent returns:
1. Relay the test results to the user.
2. If all levels passed:
   - Check `git status` for uncommitted changes. If changes exist, run `git add -A && git commit` with a commit message that accurately describes the changes (analyze the diff to write a meaningful message).
   - Report success and stop.
3. If any level failed, enter the **Hotfix Loop** (max 2 attempts):

### Hotfix Loop
1. **Attempt 1**: Invoke a 개발팀 (dev-team) subagent in auto mode with:
   - The failing test level and error message
   - The list of files involved
   - Instruction: "Auto mode. Hotfix: fix the following test failure. Read the error, read the file, fix it directly. Write a step log to the plan's log directory if available, otherwise skip logging."
2. After the fix, re-invoke the 테스트팀 agent to re-run from the failed level onward.
3. If tests pass: check `git status` for uncommitted changes. If changes exist, run `git add -A && git commit` with a meaningful commit message. Report success and stop.
4. **Attempt 2**: If still failing, repeat with the new error context.
5. If still failing after 2 attempts: report the failure to the user with:
   - The original error
   - What was attempted
   - Suggested next steps (manual investigation or new plan-task)

## Task
Test: $ARGUMENTS
