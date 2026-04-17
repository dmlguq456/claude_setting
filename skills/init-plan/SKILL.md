---
name: init-plan
description: Create a detailed implementation plan based on actual codebase
argument-hint: "<task description> [--qa light|standard|thorough|adversarial] [--autonomy proactive|standard|passive]"
---

> Caller note: planning benefits from `high` or `xhigh` effort; lower effort may miss call sites in cross-file analysis.

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## Pre-Check
Parse `--autonomy proactive|standard|passive` from `$ARGUMENTS` (alongside `--qa`). Store the level; strip the flag from the task description passed downstream.

Check if a similar plan already exists in `.claude_reports/plans/`. Apply the following gating rules based on status and autonomy level:

- `active` **(Critical severity — always ask, regardless of autonomy level)**:
  Notify the user and ask: "기존에 진행 중인 plan이 있습니다. 이어서 진행할까요, 새로 만들까요?" Do NOT proceed until confirmed.

- `done`/`failed` **(Significant severity)**:
  - `proactive`: Note it for reference and auto-proceed with new plan creation (no prompt).
  - `standard`/`passive`: Note it for reference and ask: "이전에 완료/실패한 plan이 있습니다. 새로 생성할까요? (기본값: 생성)" Do NOT proceed until confirmed.

- `partial` **(Significant severity)**:
  - `proactive`: Auto-decide: create a new plan covering only the failed steps (read `failed_steps` from plan frontmatter). No prompt.
  - `standard`/`passive`: Notify the user that a previous attempt partially completed. Ask whether to create a new plan covering the failed steps or start fresh. Do NOT proceed until confirmed.

> After each gated decision, record the decision per the Decision Point Logging Rule. Decisions propagate up to the pipeline skill's pipeline_summary.md.

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

The agent writes the plan file directly; the orchestrator only receives paths and a summary.

## QA Scaling
If `$ARGUMENTS` contains `--qa light|standard|thorough|adversarial`, use that level and strip the flag from the task description. Otherwise, auto-detect from the plan's scope. When `qa_level` is set in plan frontmatter, it overrides auto-detect.

If `$ARGUMENTS` contains `--autonomy proactive|standard|passive`, store that level and strip the flag. It is passed through to the plan frontmatter by the calling pipeline skill.

| Level | Auto-detect condition | Action |
|---|---|---|
| **Light** | ≤3 steps, mechanical, single-variant | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | 4-10 steps, logic changes, single module | 1× 품질관리팀 (default opus) |
| **Thorough** | >10 steps, cross-module/variant, architectural | 2-3× 품질관리팀 in parallel (opus): Agent A correctness, B completeness, C risk (optional, >15 steps); each writes `round_{N}_{focus}.md`; all 🔴 issues must be resolved |
| **Adversarial** | Cross-variant (SE+SS+CSS), shared modules (utils/, network.py), or >20 steps with architectural impact — **AND Codex available** | Thorough-level 품질관리팀 + 1× codex-review-team (`adversarial-review`) in parallel; Codex writes `round_{N}_codex.md`; all 🔴 from ANY agent (including Codex) must be resolved |

**Codex availability check**: Before selecting Adversarial, run `codex --version` (suppress stderr). If the command fails or Codex is not authenticated, fall back to Thorough silently. This check is skipped if `--qa adversarial` is explicitly specified (fail loudly instead).

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
4. **If 🔴 remain after `round >= 3`**:
   - `proactive`: Auto-proceed — invoke 기획팀: "Refine mode. Add remaining 🔴 issues to the plan's 리스크 section under ## 미해결 이슈. Return brief Korean summary." Then report to user: plan path, resolved issues, and unresolved issues with reasons.
   - `standard`/`passive`: Ask the user: "QA 3라운드 후에도 🔴 이슈가 {N}개 남아있습니다. 리스크 섹션에 추가하고 진행할까요, 추가 수정을 시도할까요?" Do NOT proceed until confirmed. If user chooses to add to risk section, invoke 기획팀 as above and report. If user chooses additional revision, run one more 기획팀 → 품질관리팀 cycle (round counter is not incremented for this extra cycle) then proceed regardless of result.

> After each gated decision, record the decision per the Decision Point Logging Rule. Decisions propagate up to the pipeline skill's pipeline_summary.md.

## Korean Version Generation
After the review loop completes, invoke 기획팀 one final time:
```
Translate mode. English plan file: {plan_path}. Save Korean version to: {same directory}/plan_ko.md.
Full Korean translation (NOT a summary). Same detail level. Section titles: 목표, 현황 분석, 변경 계획, 리스크, 검증 방법. Code identifiers stay in English. Return ONLY the file path.
```
Then report to the user: English plan path, Korean plan path, plan summary, and QA verdict.

## Task
$ARGUMENTS
