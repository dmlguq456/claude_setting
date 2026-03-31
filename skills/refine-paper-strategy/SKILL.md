---
name: refine-paper-strategy
description: Reflect user memos/review feedback in a paper strategy and update it
argument-hint: "<strategy name or path>"
---

## Strategy Resolution
Resolve `$ARGUMENTS` to strategy file paths. Always resolve BOTH `strategy.md` and `strategy_ko.md`:
1. If it ends with `.md` → use as-is; derive the other file by path swap (`strategy.md` ↔ `strategy_ko.md`)
2. If it's a directory path → append `/strategy/strategy.md` (English) and `/strategy/strategy_ko.md` (Korean)
3. Otherwise, fuzzy search: `ls -d .claude_reports/papers/*$ARGUMENTS* 2>/dev/null`
   - **1 match** → use `{match}/strategy/strategy.md` and `{match}/strategy/strategy_ko.md`
   - **Multiple matches** → ask user
   - **No match** → report error

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## Delegate to 연구팀
Invoke the **research-team** (연구팀) agent as a subagent with the following prompt:

```
Refine mode. Update an existing paper strategy based on user memos and review feedback.

Korean strategy file: {ko_strategy_path}
English strategy file: {en_strategy_path}

Read the Korean strategy and find all user memos. Memos can appear in any of these formats:
- `<!-- memo: ... -->` (standard memo tag)
- `<!-- ... -->` (HTML comment — treat any HTML comment as a user memo)
- `// ...` (inline comment)
- `[memo] ...` (bracketed annotation)
- `(**...**)` (parenthetical note)
- Any text that clearly looks like a user-added note

Also check the analysis/ directory for any updated materials.

Re-read reference PDFs if needed to verify or strengthen arguments.
Update the Korean strategy in-place, and sync changes to the English strategy.
Remove the memo comments after incorporating them.
Return which sections were changed and a brief summary.
```

## QA Scaling
Auto-detect from sections changed:

| Level | Condition | Action |
|---|---|---|
| **Light** | ≤3 sections | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | 4+ sections | 1× 품질관리팀 (default opus) |
| **Thorough** | Major overhaul or new evidence | 2× 품질관리팀 in parallel (opus) |

## Post-Refine Review Loop (max 2 rounds)
After 연구팀 returns:
1. **Resolve log dir**: parent of `strategy/` (e.g., `.claude_reports/papers/2026-03-25_foo/`). Run `mkdir -p {log_dir}/strategy_reviews`.
2. **Invoke 품질관리팀** with prompt: "Review changed sections. Strategy: [path]. Changed: [list]. For rebuttals, verify all reviewer points still addressed. Write to: {log_dir}/strategy_reviews/refine_round_{N}.md. Return ONLY path + one-line verdict."
3. **Check verdict:**
   - **No 🔴**: Report to user.
   - **🔴 found**: Re-invoke 연구팀. Max 2 rounds.
4. **If 🔴 remain after 2 rounds**: Add to `## 미해결 이슈`, report which sections changed, which issues resolved/unresolved and why.

## Task
Refine the paper strategy at: $ARGUMENTS
