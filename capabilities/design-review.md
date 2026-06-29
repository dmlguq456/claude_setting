# Capability: design-review

This is the portable capability contract for `design-review`. It defines runtime-neutral meaning and adapter obligations. It is not a Claude Skill file.

## Contract

| Field | Value |
|---|---|
| Identifier | `design-review` |
| Group | `sub` |
| Supported modes | `none` |
| Portable meaning | 디자인 결과물을 품질·토큰 계약·breakage 관점으로 점검한다. |
| Argument shape | `<design path or app path>` |

## Invocation Semantics

Visual review — two gates. (1) verifier (디자인팀 verifier mode, separate context, adapter visual harness) screens for breakage — console errors, layout collapse, intent mismatch — and must pass before critique. (2) critic (디자인팀 critic mode) gives a 6-axis quality critique (hierarchy, alignment, accessibility, responsiveness, UX flow, tone). Both render through the adapter-provided visual harness and inspect the image. Read-only — no auto-fix.

Adapters may expose this capability through native commands, skill files, prompt instructions, or explicit wrappers. The adapter must report unsupported runtime mechanics instead of silently treating another runtime's native file format as portable.

## Artifact Ownership

Use the shared artifact root rule: prefer `.agent_reports/`; use legacy `.claude_reports/` only when it already exists and `.agent_reports/` does not. Capability-specific output placement follows `core/CONVENTIONS.md` section 5 until this spec is expanded with a stricter per-capability artifact map.

## Role Requirements

Use portable role names from `roles/README.md` and `core/CONVENTIONS.md`. Concrete model names, subagent frontmatter, and runtime-specific tool lists belong in adapter files.

## Guard Requirements

Adapters must preserve the portable invariants relevant to this capability:

- resolve artifact root through `utilities/artifact-root.sh` or equivalent logic;
- enforce git/worktree safety before edits;
- enforce artifact ordering before new durable artifacts;
- enforce spec-read gating when this capability changes spec-backed code or specs;
- use DB memory paths, not runtime-native memory files.

## Adapter Realization

| Adapter | Realization |
|---|---|
| Claude Code | `adapters/claude/skills/design-review/SKILL.md` is the Claude-native realization; `tools/design-mcp/` provides the visual harness; `skills/design-review/SKILL.md` is the compatibility reference. |
| Codex | Read this spec and run `adapters/codex/bin/preflight.sh capability-info design-review`. Do not consume `skills/design-review/SKILL.md` as native Codex configuration. |

## Compatibility Reference

The historical Claude Skill compatibility reference remains at `skills/design-review/SKILL.md`; Claude Code consumes `adapters/claude/skills/design-review/SKILL.md` as the adapter-native realization while portable meaning moves here.
