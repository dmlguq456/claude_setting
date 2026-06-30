# Codex Material Web Image Search Mode

This is a Codex-native realization guide generated from the portable mode
inventory. It is adapter-owned output, not a legacy runtime mode copy.

## Source Order

1. Read `roles/MODES.md`.
2. Read `roles/modes/material/web-image-search.md` for the portable mode contract.
3. Run `adapters/codex/bin/preflight.sh mode-info material/web-image-search`.
4. Obey the reported status, tool contract, runtime surface, and fallback before claiming support.

## Codex Runtime Mapping

- Status: `tool-contract`
- Realization: `portable-with-tool-contract`
- Tool Contract: `web-image-search`
- Tool Contract Check: `adapters/codex/bin/preflight.sh web-image-search --check <query>`
- Runtime Surface: `adapter-owned-web-image-search`
- Fallback: `satisfy-tool-contract-or-report-unavailable`
- Requirement: run the adapter-owned web image search launcher with a configured provider, or report unavailable
- Note: Codex may use the persona only after satisfying or explicitly downgrading the named tool contract.

## Use

- Use Codex file, terminal, approval, sandbox, hook, and skill surfaces.
- Run `adapters/codex/bin/preflight.sh write <file> [session-id]` before edits.
- For `tool-contract` modes, run the named contract check before claiming the tool-backed result.
- If a required local provider or executable is unavailable, report the unavailable contract instead of silently downgrading.
- Treat `adapters/codex/modes/material/web-image-search.md` as the adapter-owned mode guide for this runtime.
