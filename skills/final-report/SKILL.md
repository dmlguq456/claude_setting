---
name: final-report
description: Generate a detailed change report from plan + dev logs — focuses on key changes, principles, and insights for future reference
argument-hint: "<path to plan file>"
---

## Language Rule
- Write the report in Korean.
- Code identifiers, file paths, and technical terms stay in English.

## Inputs
1. **Plan file**: the English plan at $ARGUMENTS
2. **Log directory**: derived from plan path (strip `.md` → folder). Contains:
   - `checklist.md` — execution status of each step
   - `step_*.md` — dev team's step logs with old/new code and Decision fields
   - `review_phase_*.md` — QA review results per phase
3. **Korean plan** (`_ko.md` suffix): for section titles and user-facing descriptions

## Procedure

1. **Read the plan file** to understand the goal, current state analysis, and change plan.
2. **Read the checklist** to identify which steps succeeded, failed, or were skipped.
3. **Read all step log files** (`step_*.md`) to extract:
   - Every code change (old → new) with its Decision rationale
   - Files modified and what each change accomplished
4. **Read QA review files** (`review_phase_*.md`) to extract:
   - Issues found during review
   - How they were resolved (or not)
5. **Synthesize** the information into a report. Do NOT just list changes — explain the reasoning and connect them to the bigger picture.

## Report Structure

Write the report to: `.claude_reports/final_reports/{YYYY-MM-DD}_{plan-short-name}.md`

```markdown
# 변경 보고서: {task name}

- **일시**: {YYYY-MM-DD}
- **플랜**: {plan path}
- **상태**: ✅ 완료 / ⚠️ 부분 완료 / ❌ 실패

---

## 1. 변경 개요
(What was done and why, 3-5 sentences. Connect to the project's design philosophy if relevant.)

## 2. 핵심 변경 사항

### 2.1 {Change category 1} — {file or module}
- **변경 내용**: (what changed)
- **변경 이유**: (why — from the Decision field, but rewritten for clarity)
- **핵심 원리**: (underlying principle or insight the user should remember)
- **영향 범위**: (what other code is affected, callers updated, etc.)

### 2.2 {Change category 2} — {file or module}
(same structure)

(... repeat for each meaningful change group. Group related small changes together.)

## 3. 설계 인사이트
Key takeaways the user should know for future work:
- (insight 1 — e.g., "X pattern was chosen over Y because...")
- (insight 2 — e.g., "This change reveals that module Z has implicit coupling with...")
- (insight 3)

## 4. QA 리뷰 요약
- **발견된 이슈**: (issues found by 품질관리팀)
- **해결 방법**: (how each was resolved)
- **미해결**: (remaining issues, or "없음")

## 5. 실패/스킵된 단계
(If any steps failed or were skipped, explain why and what to do about them. If all succeeded: "전체 단계 성공 ✅")

## 6. 향후 참고사항
- (things to watch out for in related future changes)
- (potential follow-up tasks identified during this work)
```

## Quality Guidelines
- **Do NOT just summarize** — extract insights. The user wants to understand "why" and "what to remember", not just "what happened".
- **Group related changes** by logical category, not by step number. Multiple steps that serve the same purpose should be one section.
- **Connect to project design** when relevant (e.g., "This aligns with the correlation-to-filter paradigm because...").
- **Be specific about impact** — mention exact callers, tensor shapes, or config keys that were affected.
- **Keep it concise but complete** — aim for 1-2 pages, not 5 pages.

## Output
Return ONLY the report file path and a one-line summary. Do NOT return the full report content.

## Task
Generate report for: $ARGUMENTS
