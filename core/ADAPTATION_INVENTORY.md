# Adaptation Inventory

This is the working inventory for turning the historical Claude Code setting
into a portable agent setting plus runtime adapters.

## Status Classes

| Status | Meaning |
|---|---|
| `portable` | Can be consumed by multiple runtimes as-is. |
| `adapter-native` | Belongs to one runtime adapter. |
| `projection` | Versioned mirror into a runtime home; symlink/generated only. |
| `compat-passthrough` | Still shared because Claude Code currently consumes it directly. |
| `needs-split` | Must be separated into portable source plus adapter-native realization. |

## Current Surfaces

| Surface | Current location | Status | Target split |
|---|---|---|---|
| Core operating contract | `core/CORE.md`, `core/WORKFLOW.md`, `core/CONVENTIONS.md`, `core/OPERATIONS.md`, `core/MEMORY.md`, `core/DESIGN_PRINCIPLES.md` | portable | Keep concrete runtime names out unless documenting adapter mapping. |
| Adapter boundary | `core/ADAPTATION.md`, `adapters/*/ADAPTATION.md` | portable / adapter-native | Single source for what symlink means and what still needs adaptation. |
| Claude bootstrap | `adapters/claude/CLAUDE.md` | adapter-native | Keep Claude Code response, routing, hook, statusline, and command rules here. |
| Codex bootstrap | `adapters/codex/AGENTS.md` | adapter-native | Expand only with behavior that Codex can actually perform. |
| Claude settings/hooks registration | `adapters/claude/settings.json` | adapter-native | Codex must get wrapper/preflight equivalents, not this JSON. |
| Slash commands | `adapters/claude/commands/` | adapter-native | Future runtimes need native command wrappers or instruction entries. |
| Skills | `skills/*/SKILL.md` | compat-passthrough, needs-split | Extract `capabilities/<name>.md` portable specs, then generate/maintain `adapters/claude/skills/<name>/SKILL.md`. |
| Agents | `agents/*.md` | compat-passthrough, needs-split | Extract portable role profiles, then map model frontmatter per adapter. |
| Hooks | `hooks/*.sh` | mixed | Split invariant checks from runtime hook payload wrappers. |
| Memory distiller | `hooks/mem-distill-dispatch.sh`, `tools/memory/` | mixed | Keep DB/CLI portable; move session log reader and model invocation to adapters. |
| Design MCP | `tools/design-mcp/`, design skills | mixed | Keep render/check semantics portable; move Claude MCP registration paths to adapter docs. |
| Projection directories | `claude_setting/`, `codex_setting/` | projection | Must contain only symlinks or generated adapter output. |

## Migration Order

1. **Role vocabulary first**: replace portable docs' concrete model names with
   `fast reviewer`, `deep reviewer`, `external adversary`, and related roles.
   Adapter docs own `sonnet`, `opus`, `gpt-*`, and CLI-specific choices.
2. **Capability specs second**: for each `skills/*/SKILL.md`, create or extract
   a portable capability contract before moving Claude Skill syntax under the
   Claude adapter.
3. **Agent profiles third**: split each `agents/*.md` into a portable profile
   plus adapter-native frontmatter/model mapping.
4. **Hook payloads fourth**: keep invariant scripts portable, but isolate
   Claude event JSON, statusline JSON, ScheduleWakeup, and MCP registration.
5. **Projection last**: after a surface has an adapter-native realization,
   update `claude_setting/` or `codex_setting/` to point at that adapter output.

## Acceptance Tests

A surface is not considered adapted until all of the following are true:

- The portable document can be read without knowing Claude Code file formats.
- The Claude adapter still exposes the old runtime path and behavior.
- The Codex adapter either exposes an equivalent behavior or explicitly marks
  the behavior unsupported with fallback instructions.
- Concrete model/runtime names appear only in adapter-native files, tests, or
  legacy compatibility notes.
- `claude_setting/` and `codex_setting/` remain projections, not independent
  semantic sources.
