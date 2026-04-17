---
name: final-report
description: Generate a detailed change report from plan + dev logs — focuses on key changes, principles, and insights for future reference
argument-hint: "<plan name or path>"
---

## Plan Resolution (canonical — keep in sync with execute-plan, run-test, final-report, refine-plan, autopilot-dev, autopilot-audit)
Resolve `$ARG` to a plan file path:
1. If it ends with `.md` → use as-is
2. If it's a directory path → append `/plan/plan.md`
3. Otherwise, fuzzy search: `ls -d .claude_reports/plans/*$ARG* 2>/dev/null`
   - **1 match** → use `{match}/plan/plan.md`
   - **Multiple matches** → prefer folder without `_audit`/`_fix_` suffix; if still multiple, ask user
   - **No match** → report error

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## QA Scaling
Use `qa_level` from plan frontmatter if present; otherwise auto-detect. Also read `autonomy_level` from plan frontmatter if present. Pass it to the 품질관리팀 prompt as context.

| Level | Auto-detect condition | Action |
|---|---|---|
| **Light** | ≤5 steps, single variant | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | 6-15 steps, moderate scope | 1× 품질관리팀 (default opus) |
| **Thorough** | >15 steps, cross-variant, or architectural | 1× 품질관리팀 (opus), sequential only |
| **Adversarial** | Cross-variant (SE+SS+CSS), shared modules (utils/, network.py), or >20 steps — **AND Codex available** | 1× 품질관리팀 (opus) sequential + 1× codex-review-team (`adversarial-review`) after report is written; Codex reviews the final report for missed issues and writes `{log_dir}/final_report_codex.md` |

**Thorough and Adversarial do NOT parallelize report generation** — report generation is a synthesis task. QA Scaling here affects model choice and applies only to the optional QA review step, not to report generation itself.

**Codex availability check**: Before selecting Adversarial, run `codex --version` (suppress stderr). If unavailable, fall back to Thorough silently. Skipped if `--qa adversarial` is explicit (fail loudly).

> `--qa` flag overrides auto-detect. `qa_level` in frontmatter overrides `--qa`.

## Delegate to 품질관리팀
Assess QA level from the plan scope (step count, variants affected) per the QA Scaling table above, then invoke the **qa-team** (품질관리팀) agent (with `model: "sonnet"` for Light level) as a subagent with the following prompt:

```
Generate a final change report.

Plan file: {$ARG} (resolved via Plan Resolution above)
Log directory: {task root folder — grandparent of plan/plan.md}
Korean plan: {same directory as plan.md}/plan_ko.md
Report output: {log_directory}/final_report.md
Date: {YYYY-MM-DD}
Autonomy level: {autonomy_level from frontmatter, or "proactive (default)" if absent}

Follow these instructions:

## Inputs
1. **Plan file**: the English plan
2. **Log directory**: Contains plan/ (plan.md, plan_ko.md, checklist.md), dev_logs/ (step_*.md), dev_reviews/ (phase reviews), plan_reviews/ (plan reviews), test_logs/, test_reviews/
3. **Korean plan** (_ko.md): for section titles and user-facing descriptions

## Procedure
1. Read the plan file to understand the goal, current state analysis, and change plan.
2. Read the checklist (plan/checklist.md) to identify which steps succeeded, failed, or were skipped.
3. Read all step log files (dev_logs/step_*.md) to extract every code change (old → new) with its Decision rationale, files modified, and what each change accomplished.
4. Read QA review files (dev_reviews/phase_*.md) to extract issues found and how they were resolved.
5. **Documentation Update**: Update .claude_reports/docs_code/ for successfully completed steps only. Mapping:
   - model.py, modules/module.py → model_modules.md
   - modules/network.py → network_modules.md
   - loss.py → loss_functions.md
   - dataset.py, util_dataset.py → dataset_pipeline.md
   - engine.py → engine_training.md
   - engine_infer.py, main_infer.py → engine_inference.md
   - utils/ → utilities.md
   - Overall design, config, data flow, cross-variant → architecture.md
   - Project structure, doc table, file renames → CLAUDE.md
   Update Interface Reference tables (signatures, callers, line numbers). Skip if no steps succeeded.
   **Verification**: Verify every class/function line number in the Interface Reference table against the **post-edit** source (use Grep or a fresh Read of the file *after* your own Step 5 edits complete). Line numbers from pre-edit reads, the plan, or dev logs may be stale.
6. **Confirm doc changes are real**: After step 5, run `git diff --stat -- .claude_reports/docs_code/ CLAUDE.md` to confirm that documentation files were actually modified. If the diff is empty but you expected changes, something went wrong — re-read and re-edit the files. Do NOT claim documentation was updated unless git diff confirms it.
7. **Read pipeline_summary.md** (log_directory/pipeline_summary.md) if it exists. Extract the Decision Points table for section 4.5. If the file does not exist or the table is empty, write "자율 판단 이벤트 없음 (proactive 모드, 클린 실행)" for section 4.5.
8. Synthesize the information into a report. Do NOT just list changes — explain the reasoning and connect them to the bigger picture.

## Report Structure

```
# 변경 보고서: {task name}
- **일시**: {YYYY-MM-DD} | **플랜**: {plan path} | **상태**: ✅/⚠️/❌

## 1. 변경 개요          — what was done and why (3-5 sentences)
## 2. 핵심 변경 사항     — grouped by logical category (not step number)
   ### 2.N {category} — {file/module}
   - **변경 내용** / **변경 이유** / **핵심 원리** / **영향 범위**
## 3. 설계 인사이트      — key takeaways for future work
## 4. QA 리뷰 요약       — 발견된 이슈 / 해결 방법 / 미해결
## 4.5 자율 판단 기록    — pipeline_summary.md의 Decision Points 테이블을 서사적 요약으로 합성. 자율 판단 이벤트가 없으면 "자율 판단 이벤트 없음 (proactive 모드, 클린 실행)"
## 5. 실패/스킵된 단계   — explain why, or "전체 단계 성공 ✅"
## 6. 향후 참고사항      — watch-outs and potential follow-ups
```

## Quality Guidelines
- Do NOT just summarize — extract insights. Focus on "why" and "what to remember".
- Be specific about impact — mention exact callers, tensor shapes, or config keys.
- Connect to project design when relevant.
- Write the report in Korean. Code identifiers, file paths, and technical terms stay in English.
- Aim for 1-3 pages total. Length should scale with change count: small plans (≤5 steps) can be 1 page; large refactors (>20 steps) may need 3.

Return ONLY the file path and a one-line summary. Do NOT return the full report content.
```

## Post-Report
After the 품질관리팀 agent returns:
1. Relay the report file path and a one-line summary to the user.
2. **Optional QA review**: After report writing is complete, invoke 품질관리팀 in code review mode per QA Scaling to review the report's accuracy AND docs_code/ update correctness. QA scope: (1) report content accuracy, (2) docs_code/ Interface Reference correctness.

Note: Thorough mode does NOT parallelize report generation — report generation is a synthesis task. QA Scaling applies only to the optional QA review step above, not to report generation itself.

## Task
Generate report for: $ARG
