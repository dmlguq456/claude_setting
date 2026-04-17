---
name: analyze-project
description: Analyze codebase and generate structured documentation in .claude_reports/docs_code/
argument-hint: "[target directory or scope]"
---

> Caller note: this skill performs deep cross-module analysis. Callers should invoke at `high` or `xhigh` effort when the runtime supports it; at lower effort, cross-module depth narrows automatically.

## Language Rule
- Think and reason in English internally.
- Write documentation files (.claude_reports/docs_code/) in English.
- When explaining something to the user, write in Korean.

## Argument Parsing

Parse flags from $ARGUMENTS before starting:
- `--skip-qa` — skip Phase 5 QA Verification entirely
- Remaining text after flag removal is treated as the target directory or scope

## Phase 1: Codebase Analysis
Determine the scope first:
- If `$ARGUMENTS` is a directory path → read files under that path recursively.
- If `$ARGUMENTS` is a keyword (e.g., "engine", "inference") → map to relevant modules by reading CLAUDE.md's structure section first, then read those modules.
- If `$ARGUMENTS` is empty or absent → read CLAUDE.md's Project Structure section if present and derive scope from it; otherwise fall back to reading top-level entry points (`*.py` / `*.ts` / `*.go` / `*.rs` / project's primary language) at the repo root plus obvious source directories (`src/`, `lib/`).
Read the in-scope code and identify:
- Role and interface of each file/module
- Data flow (input → processing → output)
- Dependencies between modules
- Design intent and core algorithms

## Phase 2: Documentation
Write analysis results as topic-separated md files in .claude_reports/docs_code/.
- Split by role, not one monolithic file
- Focus on code-level details (not usage guides)
- Write in English
- Each doc MUST end with an **## Interface Reference** section — a table summarizing the key classes/functions covered by that doc:
  ```
  ## Interface Reference

  | Class/Function | File | Signature | Called by |
  |---|---|---|---|
  | `ClassName` | file.py:L | `(arg1, arg2, ...) → return` | `caller_module.func` |
  | `function_name` | file.py:L | `(arg1, ...) → return` | `caller.func1`, `caller.func2` |
  ```
  - Include all public classes, key functions, and any function with cross-module callers.
  - The "Called by" column enables downstream agents (especially 기획팀) to quickly assess change impact without grepping source code.

## Phase 3: CLAUDE.md
CLAUDE.md should minimize code content and contain only:
- .claude_reports/docs_code/ document list with coverage table
- Behavioral guidelines (coding rules, restrictions, commit rules)
- Project structure overview (tree)
- Execution examples
- If CLAUDE.md already exists, preserve existing rules and merge new findings

## Phase 4: Verify Documentation Coverage
- Check that every code file in models/ and utils/ is covered by at least one .claude_reports/docs_code/ document.
- Documentation updates are handled as an explicit step in execute-plan, not by hooks.

## Phase 5: QA Verification (optional, skipped with --skip-qa)

After documentation is written, invoke 품질관리팀 in code review mode to cross-check Interface Reference entries against actual source code.

**QA scope**: Documentation files updated in the current run only.

**Minimum verification**: At least 2 Interface Reference entries per file — check signature, file path, and line number against actual source.

**QA model**: Light QA using sonnet — documentation is not as critical as code changes.
