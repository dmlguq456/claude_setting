# Codex Design Maker Mode

This is the Codex-native realization guide for `roles/modes/design/maker.md`.

## Source Order

1. Read `roles/MODES.md`.
2. Read `roles/modes/design/maker.md` and `roles/modes/design/_design_rules.md`.
3. Run `adapters/codex/bin/preflight.sh mode-info design/maker`.

## Runtime Contract

- Build visual artifacts with Codex file/edit tools and normal write guards.
- Before claiming a renderable HTML artifact is complete, run `adapters/codex/bin/preflight.sh visual-harness <file.html>` and inspect the screenshot.
- For SVG or diagram-only outputs, produce a browser-viewable HTML wrapper or explicitly report that the visual-harness contract is unavailable for that artifact.
- If the harness reports console errors, layout failure, or unavailable dependencies, fix or report the downgrade.
- Keep implementation decisions grounded in portable design rules; do not use non-Codex runtime tool names as executable instructions.
