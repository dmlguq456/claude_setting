---
name: analyze-project
description: Analyze codebase and generate structured documentation in .claude_reports/docs_code/
argument-hint: "[target directory or scope]"
---

## Language Rule
- Think and reason in English internally.
- Write documentation files (.claude_reports/docs_code/) in English.
- When explaining something to the user, write in Korean.

## Phase 1: Codebase Analysis
Read all code in $ARGUMENTS and identify:
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
