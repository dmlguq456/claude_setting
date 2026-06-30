---
description: "Run the portable audit capability through the OpenCode adapter. Meaning: 산출물·파이프 사후 점검. drift·일관성·누락을 읽기 중심으로 진단한다."
---

Use the OpenCode adapter realization of portable capability `audit`.
This is adapter-owned output generated from `capabilities/audit.md`, not a runtime-specific command copy.

1. Read `capabilities/audit.md` for the runtime-neutral contract.
2. Run `adapters/opencode/bin/preflight.sh capability-info audit` and
   obey `instruction-only`, `tool-contract`, or `unsupported` status. For
   `tool-contract`, report the named `tool_contract`, run any
   `tool_contract_check`, and obey `runtime_surface` / `fallback` before
   claiming full support. For `unsupported`, stop or use the reported
   `fallback`.
3. Before edits, run `adapters/opencode/bin/preflight.sh write <file> [session-id]`.
4. Before spec-changing work, run
   `adapters/opencode/bin/preflight.sh capability audit [cwd] [session-id]`.
5. If the command receives arguments, map them to the portable argument shape:
   `<artifact_path> [--scope auto|facts|style|structure|cross-ref|coverage|all] [--read-only] [--report-only] [--no-fact-check]`.

Portable contract excerpt:

- Invocation semantics: Read-only multi-aspect audit / lint for `<artifact-root>/{plans,research,documents}/*` artifacts. Single global entry — auto-detects artifact type from path prefix (plans=code; research=field-survey; documents=doc deliverable). Per-type lint aspects: doc → facts / style / structure / cross-ref / coverage; research → cards 정합성 / Tier consistency / coverage / cross-card; plans → test results / lint / code review / TODO·미구현. Default `--scope auto` — artifact 특성 기반 자동 선택; 사용자 명시는 1순위 override. Report-only — never modifies the artifact. Complementary to autopilot-refine: refine = edit flow, audit = inspect flow. Adapters may expose this capability through native commands, skill files, prompt instructions, or explicit wrappers. The adapter must report unsupported runtime mechanics instead of silently treating another runtime's native file format as portable.


User arguments from OpenCode: `$ARGUMENTS`

Do not use non-OpenCode command files or runtime-specific slash-command files
as OpenCode-native command source.
