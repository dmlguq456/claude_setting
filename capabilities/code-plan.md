# Capability: code-plan

This is the portable capability contract for `code-plan`. It defines runtime-neutral meaning and adapter obligations. It is not a Claude Skill file.

## Contract

| Field | Value |
|---|---|
| Identifier | `code-plan` |
| Group | `sub` |
| Supported modes | `none` |
| Portable meaning | 코드 분석 후 상세 구현 plan 작성. planning role과 QA loop를 사용한다. |
| Argument shape | `<task description> [--qa quick|light|standard|thorough|adversarial]` |

## Invocation Semantics

Create a detailed implementation plan based on actual codebase

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
| Claude Code | `adapters/claude/skills/code-plan/SKILL.md` is the Claude-native realization; `skills/code-plan/SKILL.md` is the compatibility reference. |
| Codex | Read this spec and run `adapters/codex/bin/preflight.sh capability-info code-plan`. Do not consume `skills/code-plan/SKILL.md` as native Codex configuration. |
| OpenCode | Read this spec and run `adapters/opencode/bin/preflight.sh capability-info code-plan`. Use `adapters/opencode/skills/code-plan/SKILL.md` and `adapters/opencode/commands/code-plan.md` as native OpenCode projections; do not consume `skills/code-plan/SKILL.md` or Claude command files as native OpenCode configuration. |

## Compatibility Reference

The historical Claude Skill compatibility reference remains at `skills/code-plan/SKILL.md`; Claude Code consumes `adapters/claude/skills/code-plan/SKILL.md` as the adapter-native realization while portable meaning moves here.
