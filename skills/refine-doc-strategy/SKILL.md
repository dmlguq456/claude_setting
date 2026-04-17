---
name: refine-doc-strategy
description: Reflect user memos/review feedback in a document strategy or draft and update it
argument-hint: "<strategy or draft name or path>"
---

## Document Resolution
Resolve `$ARGUMENTS` to document file paths. Detect whether this is a **strategy** or **draft** refinement:

**Auto-detect document type**:
- If path contains `/draft/` → draft mode (resolve `draft.md` + `draft_ko.md`)
- If path contains `/strategy/` → strategy mode (resolve `strategy.md` + `strategy_ko.md`)
- If path is a directory → default to strategy mode

**Resolution rules** — always resolve BOTH English and Korean files:
1. If it ends with `.md` → use as-is; derive the other file by path swap (`draft.md` ↔ `draft_ko.md`, or `strategy.md` ↔ `strategy_ko.md`)
2. If it's a directory path → append `/strategy/strategy.md` (English) and `/strategy/strategy_ko.md` (Korean)
3. Otherwise, fuzzy search: `ls -d .claude_reports/documents/*$ARGUMENTS* 2>/dev/null`
   - **1 match** → use `{match}/strategy/strategy.md` and `{match}/strategy/strategy_ko.md`
   - **Multiple matches** → ask user
   - **No match** → report error

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## Delegate to 연구팀
Invoke the **research-team** (연구팀) agent as a subagent with the following prompt:

```
Refine mode. Update an existing document {doc_type} based on user memos and review feedback.

Korean {doc_type} file: {ko_path}
English {doc_type} file: {en_path}

Read the Korean {doc_type} and find all user memos. Memos can appear in any of these formats:
- `<!-- memo: ... -->` (standard memo tag)
- `<!-- ... -->` (HTML comment — treat any HTML comment as a user memo)
- `// ...` (inline comment)
- `[memo] ...` (bracketed annotation)
- `(**...**)` (parenthetical note)
- Any other text marked as a user annotation (e.g., a distinct block inserted between plan steps, or an inline sentence addressed to the planner). Do NOT treat the plan's original author-written prose as a memo.

Also check the analysis/ directory for any updated materials.
For draft refinement: also cross-check against the strategy document at {artifact_root}/strategy/ to verify the draft faithfully reflects all strategy points.

Re-read reference materials if needed to verify or strengthen arguments.
Update the Korean {doc_type} in-place, and sync changes to the English {doc_type}.
Remove the memo comments after incorporating them.
Return which sections were changed and a brief summary.
```

Where `{doc_type}` is either "strategy" or "draft" based on auto-detection.

## QA Scaling
Auto-detect from sections changed:

| Level | Condition | Action |
|---|---|---|
| **Light** | ≤3 sections | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | 4+ sections | 1× 품질관리팀 (default opus) |
| **Thorough** | Major overhaul or new evidence | 2× 품질관리팀 in parallel (opus) |

## Post-Refine Review Loop (max 2 rounds)
After 연구팀 returns:
1. **Resolve log dir**: artifact root (e.g., `.claude_reports/documents/2026-03-25_foo/`).
   - For strategy refinement: `mkdir -p {log_dir}/strategy_reviews`
   - For draft refinement: `mkdir -p {log_dir}/draft_reviews`
2. **Invoke 품질관리팀** with prompt: "Review changed sections. {Doc type}: [path]. Changed: [list]. For rebuttals, verify all reviewer points still addressed. Write to: {log_dir}/{review_subdir}/refine_round_{N}.md. Return ONLY path + one-line verdict."
3. **Check verdict:**
   - **No 🔴**: Report to user.
   - **🔴 found**: Re-invoke 연구팀. Max 2 rounds.
4. **If 🔴 remain after 2 rounds**: Add to `## 미해결 이슈`, report which sections changed, which issues resolved/unresolved and why.

## Task
Refine the document at: $ARGUMENTS
