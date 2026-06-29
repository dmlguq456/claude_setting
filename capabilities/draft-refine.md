# Capability: draft-refine

This is the portable capability contract for `draft-refine`. It defines runtime-neutral meaning and adapter obligations. It is not a Claude Skill file.

## Contract

| Field | Value |
|---|---|
| Identifier | `draft-refine` |
| Group | `sub` |
| Supported modes | `none` |
| Portable meaning | 초안 정련·다듬기. memo/review feedback을 문서 전략이나 draft에 반영한다. |
| Argument shape | `<strategy or draft name or path> [--qa quick|light|standard|thorough|adversarial]` |

## Invocation Semantics

Reflect user memos/review feedback in a document strategy or draft. Snapshots prior version under `_internal/versions/v{N}/` (modern; per CONVENTIONS.md §5) or `_v{N}.md` siblings (legacy). Auto-managed `changelog:` array inside YAML frontmatter (NOT a top-of-file HTML comment — that breaks markdown preview when frontmatter is also present). Mandatory ref-grounding per memo (re-read source; override memo if it conflicts with source).

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
| Claude Code | `adapters/claude/skills/draft-refine/SKILL.md` is the Claude-native realization; `skills/draft-refine/SKILL.md` is the compatibility reference. |
| Codex | Read this spec and run `adapters/codex/bin/preflight.sh capability-info draft-refine`. Use `adapters/codex/skills/draft-refine/SKILL.md` and `adapters/codex/plugins/agent-harness-codex/skills/draft-refine/SKILL.md` as native Codex Skill/plugin projections; do not consume `skills/draft-refine/SKILL.md` or Claude command files as native Codex configuration. |
| OpenCode | Read this spec and run `adapters/opencode/bin/preflight.sh capability-info draft-refine`. Use `adapters/opencode/skills/draft-refine/SKILL.md` and `adapters/opencode/commands/draft-refine.md` as native OpenCode projections; do not consume `skills/draft-refine/SKILL.md` or Claude command files as native OpenCode configuration. |

## Compatibility Reference

The historical Claude Skill compatibility reference remains at `skills/draft-refine/SKILL.md`; Claude Code consumes `adapters/claude/skills/draft-refine/SKILL.md` as the adapter-native realization while portable meaning moves here.
