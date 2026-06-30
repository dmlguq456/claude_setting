---
description: "Run the portable design-components capability through the OpenCode adapter. Meaning: UI component/mockup 구현과 preview artifact를 만든다."
---

Use the OpenCode adapter realization of portable capability `design-components`.
This is adapter-owned output generated from `capabilities/design-components.md`, not a runtime-specific command copy.

1. Read `capabilities/design-components.md` for the runtime-neutral contract.
2. Run `adapters/opencode/bin/preflight.sh capability-info design-components` and
   obey `instruction-only`, `tool-contract`, or `unsupported` status. For
   `tool-contract`, report the named `tool_contract`, run any
   `tool_contract_check`, and obey `runtime_surface` / `fallback` before
   claiming full support. For `unsupported`, stop or use the reported
   `fallback`.
3. Before edits, run `adapters/opencode/bin/preflight.sh write <file> [session-id]`.
4. Before spec-changing work, run
   `adapters/opencode/bin/preflight.sh capability design-components [cwd] [session-id]`.
5. If the command receives arguments, map them to the portable argument shape:
   `<design path or app path>`.

Portable contract excerpt:

- Invocation semantics: Component / visual asset creation — invokes 디자인팀 maker mode. Produces shadcn/Tailwind components (ui), composed full-screen pages (webapp), slide visual guides (slide), SVG icons (icon), or mermaid/direct-SVG/excalidraw diagrams (diagram). Every output is rendered and visually self-verified (render → Read → fix loop), and can be emitted as a self-contained single-file HTML preview artifact (--artifact standalone). Adapters may expose this capability through native commands, skill files, prompt instructions, or explicit wrappers. The adapter must report unsupported runtime mechanics instead of silently treating another runtime's native file format as portable.


User arguments from OpenCode: `$ARGUMENTS`

Do not use non-OpenCode command files or runtime-specific slash-command files
as OpenCode-native command source.
