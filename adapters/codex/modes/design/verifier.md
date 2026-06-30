# Codex Design Verifier Mode

This is the Codex-native realization guide for `roles/modes/design/verifier.md`.

## Source Order

1. Read `roles/MODES.md`.
2. Read `roles/modes/design/verifier.md` and `roles/modes/design/_design_rules.md`.
3. Run `adapters/codex/bin/preflight.sh mode-info design/verifier`.

## Runtime Contract

- Treat this mode as read-only.
- For HTML artifacts, run `adapters/codex/bin/preflight.sh visual-harness <file.html>` and inspect the screenshot and console summary.
- Report `verdict`, `breakage`, and concrete evidence from the harness output.
- If visual verification cannot run, report `status=unavailable` or the unavailable tool contract rather than marking the artifact verified.
- Do not edit artifacts in verifier mode.
