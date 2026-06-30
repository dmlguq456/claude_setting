---
description: "Run the portable analyze-user capability through the OpenCode adapter. Meaning: cross-project 사용자 성향 프로필 작성·갱신. 코드·작성·분석 패턴을 추출한다."
---

Use the OpenCode adapter realization of portable capability `analyze-user`.
This is adapter-owned output generated from `capabilities/analyze-user.md`, not a runtime-specific command copy.

1. Read `capabilities/analyze-user.md` for the runtime-neutral contract.
2. Run `adapters/opencode/bin/preflight.sh capability-info analyze-user` and
   obey `instruction-only`, `tool-contract`, or `unsupported` status. For
   `tool-contract`, report the named `tool_contract`, run any
   `tool_contract_check`, and obey `runtime_surface` / `fallback` before
   claiming full support. For `unsupported`, stop or use the reported
   `fallback`.
3. Before edits, run `adapters/opencode/bin/preflight.sh write <file> [session-id]`.
4. Before spec-changing work, run
   `adapters/opencode/bin/preflight.sh capability analyze-user [cwd] [session-id]`.
5. If the command receives arguments, map them to the portable argument shape:
   `<aspect> [--source <path>] [--mode init|update] [--from discover|analyze|verify|qa|output|summary] [--user-refine]`.

Portable contract excerpt:

- Invocation semantics: 사용자의 cross-project 산출물 (paper / presentation / report / code / memory) 을 다단계로 스캔·분석해 DB `type=profile` 레코드 (`mem profile <stem>`) 의 _범용 작업 성향_ 을 누적·갱신. autopilot-* 와 동급 ceremony — 사용자 프로필은 _한 번 만들어지면 모든 sub-agent 가 default 로 따르는 자료_ 라 작은 오류도 propagating. 따라서 source discovery → aspect 별 분석 → cross-aspect 일관성 검증 → 다중 QA gate (adversarial 고정) → 산출 → pipeline summary 6 phase. QA level 은 _항상 adversarial_ — 사용자 협상 불가. Adapters may expose this capability through native commands, skill files, prompt instructions, or explicit wrappers. The adapter must report unsupported runtime mechanics instead of silently treating another runtime's native file format as portable.


User arguments from OpenCode: `$ARGUMENTS`

Do not use non-OpenCode command files or runtime-specific slash-command files
as OpenCode-native command source.
