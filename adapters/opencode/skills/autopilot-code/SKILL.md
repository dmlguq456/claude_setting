---
name: autopilot-code
description: "Use when the user requests autopilot-code: 코드 작업 entry. spec 컨텍스트를 감지하고 plan→execute→test→report 흐름을 닫는다. Read the portable capability spec and run the OpenCode preflight wrapper before claiming support."
metadata:
  portable_source: capabilities/autopilot-code.md
  adapter: opencode
---

# autopilot-code

This is an OpenCode-native Skill projection generated from the portable
capability contract. It is adapter-owned output, not a legacy compatibility Skill copy.

## Source

- Portable source: `capabilities/autopilot-code.md`
- Runtime check: `adapters/opencode/bin/preflight.sh capability-info autopilot-code`
- Bootstrap: `adapters/opencode/AGENTS.md`

## Use

1. Read `capabilities/autopilot-code.md` for the runtime-neutral contract.
2. Run `adapters/opencode/bin/preflight.sh capability-info autopilot-code`.
3. Obey the reported status:
   - `instruction-only`: use this Skill as OpenCode guidance plus explicit preflight guards.
   - `tool-contract`: report the named `tool_contract`, run any `tool_contract_check`, and obey `runtime_surface` / `fallback` before claiming full support.
   - `unsupported`: stop or use the reported `fallback`.

## Shape

- Identifier: `autopilot-code`
- Supported modes: `dev, debug, audit`
- Argument shape: `--mode dev|debug <task/plan/error description> [--from <step>] [--qa quick|light|standard|thorough|adversarial] [--user-refine]`
- Portable meaning: 코드 작업 entry. spec 컨텍스트를 감지하고 plan→execute→test→report 흐름을 닫는다.

## Required Guards

- Before edits: `adapters/opencode/bin/preflight.sh write <file> [session-id]`
- Before spec-changing work: `adapters/opencode/bin/preflight.sh capability autopilot-code [cwd] [session-id]`
- After actually reading a spec PRD: `adapters/opencode/bin/preflight.sh read <prd.md> [session-id]`
- For workflow state: `adapters/opencode/bin/preflight.sh mode [cwd] [session-id]`

Do not use legacy compatibility Skill files or non-native adapter Skill files
as OpenCode-native source. Those files are compatibility/reference surfaces only.
