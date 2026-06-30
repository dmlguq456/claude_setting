# Codex Design Rules Mode

This is the Codex-native realization guide for `roles/modes/design/_design_rules.md`.
It is adapter-owned and must not be treated as a legacy runtime mode file.

## Source Order

1. Read `roles/MODES.md`.
2. Read `roles/modes/design/_design_rules.md` for the portable design rules.
3. Run `adapters/codex/bin/preflight.sh mode-info design/_design_rules`.
4. For every renderable HTML design output, run `adapters/codex/bin/preflight.sh visual-harness <file.html>` and inspect the reported screenshot before claiming visual completion.

## Codex Runtime Mapping

- Use Codex file/edit tools for implementation.
- Use `adapters/codex/tools/design/visual-harness.sh` through preflight for render, screenshot, and console checks.
- If the visual harness exits 69 or reports an unavailable dependency, report the unavailable tool contract instead of claiming native visual verification.
- Do not invoke non-Codex runtime hook, command, statusline, or settings surfaces.
