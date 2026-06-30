# Codex Design Critic Mode

This is the Codex-native realization guide for `roles/modes/design/critic.md`.

## Source Order

1. Read `roles/MODES.md`.
2. Read `roles/modes/design/critic.md` and `roles/modes/design/_design_rules.md`.
3. Run `adapters/codex/bin/preflight.sh mode-info design/critic`.

## Runtime Contract

- Critique only rendered or otherwise inspectable artifacts.
- For HTML artifacts, run `adapters/codex/bin/preflight.sh visual-harness <file.html>` and inspect the screenshot before giving quality findings.
- If rendering is unavailable, explicitly limit the critique to the evidence inspected and report the missing visual-harness contract.
- Return concise findings on hierarchy, spacing, accessibility, responsiveness, UX flow, and tone consistency.
- Do not edit artifacts in critic mode.
