---
name: execute-plan
description: Execute an implementation plan with progress tracking
argument-hint: "<path to plan file>"
---

## Language Rule
- Think and reason in English internally.
- When reporting progress or results to the user, write in Korean.

## Git Safety Checkpoint
Before any code changes, ensure the working tree is clean and up-to-date:
1. Run `git fetch && git pull` to sync with the remote.
   - If pull fails due to merge conflicts: abort the pull (`git merge --abort`), warn the user, and stop. Do NOT proceed with execution.
2. Run `git status` to check for uncommitted changes.
3. If there are uncommitted changes:
   - Run `git add -A && git commit` with a commit message that accurately describes the current uncommitted changes (analyze the diff to write a meaningful message).
   - This commit serves as a restore point if rollback fails later.
4. Record the current commit hash: `git rev-parse HEAD` → save as `$SAFETY_COMMIT`.
   - `$SAFETY_COMMIT` is persisted into the checklist header during Initialization.

## Initialization
- Read the plan file at $ARGUMENTS.
- Derive the log directory path: strip `.md` from the plan file path to get the folder name.
  - Example: `.claude_reports/plans/2026-03-18_refactor_engine.md` → `.claude_reports/plans/2026-03-18_refactor_engine/`
- **Check for existing log directory** at `{log_dir}`:
  - If `{log_dir}/checklist.md` already exists with `[x]`/`[FAIL]`/`[SKIP-DEP]` marks: this is a **resume**. Read the checklist, update the `Safety commit:` line with the current `$SAFETY_COMMIT`, and skip all completed steps. Continue from the first `[ ]` step.
  - Otherwise: this is a **fresh execution**. Proceed to create the log directory and checklist.
- **Create the log directory** and the checklist:
  1. `mkdir -p {log_dir}`
  2. Write `{log_dir}/checklist.md` — checklist derived directly from the English plan with the following header and body:
  ```
  Safety commit: {$SAFETY_COMMIT}

  Phase A: [description]
    [ ] Step 1: [file] — [what to change]
    [ ] Step 2: [file] — [what to change]
  Phase B: [description]
    [ ] Step 3: [file] — [what to change]
  ```
- Subagents will create their own step log files inside this directory (they have the Write tool).
- Use this checklist file as the sole tracking document for orchestration.
  - Mark `[x]` or `[FAIL]` as steps complete or fail.
  - Do NOT modify the plan files (neither English nor Korean) during execution.

## Rules
- Read the English checklist file before each step to decide what to do next.
- Implement all steps in the plan, in order of dependencies.
- **Delegate implementation to the dev-team (개발팀) agent as a subagent.**
  - Include "auto mode" in the prompt, and specify files/changes concretely.
  - Include the log directory path so the subagent can write its own step log file (e.g., `step_01_model_py.md`).
  - Launch multiple dev-team (개발팀) subagents in parallel for independent steps.
- After completing each step:
  - Mark `[x]` in the English checklist file
  - Syntax/import verification is handled by the code reviewer during phase review
- Do NOT stop until all processable steps are done (marked `[x]` or `[FAIL]`).

## Change Log & Phase Review
- Each 개발팀 subagent writes its own step log file in the log directory (e.g., `step_01_model_py.md`).
  - The log contains exact old/new per Edit with a `Decision:` field explaining the rationale — the subagent creates this file itself.
- **When a phase completes**:
  1. Invoke the 품질관리팀 agent as a subagent.
     - Prompt must include: the step log file names for THIS phase, the log directory path, the list of changed source files, and the review output file name.
     - Example: "Review this phase in code review mode. Log dir: [path]. Step logs for this phase: [file list]. Changed source files: [file list]. Write review results to: [path]/review_phase_01.md. Return the file path and a one-line verdict only."
     - The 품질관리팀 reads step logs (including Decision fields) and source files directly, then writes the review report to the specified file.
  2. **Read the review file** to determine next action:
     - 🟡 issues only: log them in the English checklist and continue.
     - 🔴 minor (simple fix): invoke a new 개발팀 subagent to fix the issue once → re-invoke 품질관리팀 to verify (output to `review_phase_{NN}_fix.md`). If still 🔴 after one fix attempt, treat as 🔴 major.
     - 🔴 major (structural/cascading problem): **rollback this phase and skip it.**
       1. Delegate rollback to a new 개발팀 subagent — pass the step log file names for this phase and instruct it to restore every `old_string` from the logs.
       2. If rollback fails (subagent reports errors or files cannot be restored): read `$SAFETY_COMMIT` from `checklist.md` header and run `git checkout .` to restore all files to that state. **WARNING: this reverts ALL uncommitted changes, including successfully completed phases.**
          - After `git checkout .`: mark ALL steps (this phase AND all previously `[x]` phases) as `[FAIL]` with reason "Reverted by git checkout due to rollback failure in Phase N".
          - **Stop execution entirely** — do not continue to the next phase. Proceed directly to Final Report.
       3. If rollback succeeded (no `git checkout .` needed): mark all steps in this phase as `[FAIL]` with a brief reason in the English checklist.
       4. **Continue to the next phase** — do not stop execution entirely.
       5. If the next phase depends on the failed phase, mark those dependent steps as `[SKIP-DEP]` and continue to the next independent phase.
- For small plans (3 steps or fewer), skip phase grouping and invoke the reviewer once after all steps complete.

## Safety Rules (CRITICAL)
- Before changing any function signature (args, return type, dict keys, tensor shapes):
  1. Grep all call sites across the entire project
  2. Update every caller
  3. Check for implicit contracts (None checks, .shape assumptions, dict key access)
- If a step causes errors that cascade beyond the plan's scope:
  - Mark the step as `[FAIL]` with error description in the English checklist
  - Rollback the step using the step log, then continue to the next step
- Do NOT change code outside the plan's scope unless required by a signature change.

## Documentation Update
After all phases are processed, check which .claude_reports/docs_code/ files need updating based on **successfully completed** steps only:
- `run.py`, `main.py` → `01_entry_and_config.md`
- `model.py`, `modules/` → `02_model_architecture.md`
- `loss.py` → `03_loss_functions.md`
- `dataset.py`, `util_dataset.py` → `04_dataset_pipeline.md`
- `engine*.py` → `05_engine_training.md`
- `utils/util_*`, `utils/decorators.py` → `06_utils.md`
- Cross-variant changes → `07_variant_differences.md`

Update the relevant docs to reflect the changes made, including the **Interface Reference** table at the end of each doc (update signatures, callers, line numbers as needed). Skip this step if no steps succeeded.

## Final Report
After all phases are processed, read the English checklist and report a summary to the user:
- List only `[FAIL]` and `[SKIP-DEP]` steps with their reasons.
- If all steps are `[x]`: report success, no need to list individual steps.
- At the end of the report, recommend the user run `/run-test <plan file path>` to verify functional correctness.
- This is the only progress report the user sees — keep it concise.

## Plan Status Update
- When all steps are marked `[x]`: change the English plan's frontmatter `status` to `done`.
- When some steps are `[x]` and some are `[FAIL]`/`[SKIP-DEP]`: change status to `partial` and add a `failed_steps` field listing the failed step numbers.
- When ALL steps are `[FAIL]`/`[SKIP-DEP]` (no `[x]` steps): change status to `failed` and add a `failed_steps` field listing all step numbers.

## Task
Execute the plan at: $ARGUMENTS
