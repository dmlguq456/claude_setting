---
description: "Run the portable sync-skills capability through the OpenCode adapter. Meaning: 정의 변경을 읽어 README/manifest/cross-doc invariant drift를 점검·동기화한다."
---

Use the OpenCode adapter realization of portable capability `sync-skills`.
This is adapter-owned output generated from `capabilities/sync-skills.md`, not a runtime-specific command copy.

1. Read `capabilities/sync-skills.md` for the runtime-neutral contract.
2. Run `adapters/opencode/bin/preflight.sh capability-info sync-skills` and
   obey `instruction-only`, `tool-contract`, or `unsupported` status. For
   `tool-contract`, report the named `tool_contract`, run any
   `tool_contract_check`, and obey `runtime_surface` / `fallback` before
   claiming full support. For `unsupported`, stop or use the reported
   `fallback`.
3. Before edits, run `adapters/opencode/bin/preflight.sh write <file> [session-id]`.
4. Before spec-changing work, run
   `adapters/opencode/bin/preflight.sh capability sync-skills [cwd] [session-id]`.
5. If the command receives arguments, map them to the portable argument shape:
   `[--check] [--force] [--auto-fix [--dry-run]]`.

Portable contract excerpt:

- Invocation semantics: Skills + Agents 정의 변경을 감지해 <agent-home>/README.md (GitHub) 의 대시보드 (워크플로우 map + cheat-sheet + 통합 가이드라인) 를 동기화한다. drift 체크 전용 모드도 지원. Adapters may expose this capability through native commands, skill files, prompt instructions, or explicit wrappers. The adapter must report unsupported runtime mechanics instead of silently treating another runtime's native file format as portable.


User arguments from OpenCode: `$ARGUMENTS`

Do not use non-OpenCode command files or runtime-specific slash-command files
as OpenCode-native command source.
