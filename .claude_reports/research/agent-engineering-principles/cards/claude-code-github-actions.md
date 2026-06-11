---
title: "Claude Code GitHub Actions"
authors: Anthropic
venue: Claude Code Documentation (code.claude.com/docs)
year-month: 2025
url: https://code.claude.com/docs/en/github-actions
raw_type: vendor documentation
tier: 1
---

## Core Claims
- (verbatim) "Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow. With a simple `@claude` mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs - all while following your project's standards."
- (verbatim) "Claude Code GitHub Actions is built on top of the Claude Agent SDK, which enables programmatic integration of Claude Code into your applications."

## Key Concepts & Definitions
- **Two execution modes (v1 auto-detected)**: interactive mode (`@claude` mention 에 반응) vs automation mode (prompt 으로 즉시 실행). v1.0 부터 `mode:` config 제거 — 자동 감지.
- **Triggers**: `issue_comment`, `pull_request_review_comment`, `issues` (opened/assigned), `pull_request` (opened/synchronize), `schedule` (cron). 어떤 GitHub event 와도 동작.
- **핵심 input**: `prompt` (plain text 또는 skill 이름 `/skill-name`), `claude_args` (CLI passthrough — `--max-turns`, `--model`, `--mcp-config`, `--allowedTools`), `anthropic_api_key`, `trigger_phrase` (default `@claude`), `plugin_marketplaces`/`plugins`.
- **CLAUDE.md 준수**: repo root CLAUDE.md 의 code style·review criteria·project rule 을 따름.

## Patterns Covered
- **@claude 멘션 → PR 자동 생성**: issue/PR comment 에서 `@claude implement this feature` 류로 즉시 구현.
- **Scheduled automation (cron)**: `on: schedule: cron: "0 9 * * *"` + `prompt: "Generate a summary of yesterday's commits"` 식 daily report.
- **Skill/plugin 호출**: checkout 후 `/skill-name` 또는 `plugin_marketplaces`+`plugins` 로 namespaced skill 실행 (예: code-review plugin 을 PR 마다).
- **Enterprise routing**: Bedrock(`use_bedrock`) / Vertex AI(`use_vertex`) + OIDC/Workload Identity Federation (정적 키 불필요).
- **보안**: API key 는 항상 GitHub Secrets (`${{ secrets.ANTHROPIC_API_KEY }}`), 최소 권한 (Contents/Issues/PRs Read&Write), merge 전 사람 review.
- **비용 통제**: `--max-turns` 제한, workflow timeout, concurrency control.

## Generation Mapping
- 본 family 의 **GitHub Actions = "trigger from anywhere" (12-factor Factor 11) 의 실체** — headless Claude 를 CI 진입점으로. 메인 Claude 의 `gh` CLI 사용 권장과 연결.
- **prompt = skill 호출** 패턴 = 본 family 의 autopilot-* / 모드 invoke 를 CI 에서 재현 가능 (`.claude/skills/` checkout 후 `/skill-name`).
- **CLAUDE.md 준수** = 본 family 의 계층적 CLAUDE.md (글로벌/프로젝트) 부트스트랩과 동형 — CI 에서도 같은 standards 적용.
- **Agent SDK 기반** = 본 환경(Claude Agent SDK) 과 동일 토대 — headless·programmatic 통합의 공통 기반.
- **layered 보안 (secrets·최소권한·merge 전 review)** = 본 family 의 §5.10 merge 선별 책임·hook gate 와 정합.

## Quotable
- "With a simple `@claude` mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs."
- "The action now automatically detects whether to run in interactive mode ... or automation mode ... based on your configuration."
- "Never commit API keys directly to your repository."

## Limitations / Caveats
- GitHub Actions minutes + API token 이중 비용 — runaway job 방지 위해 `--max-turns`·timeout 필수.
- v1.0 breaking changes (beta→v1): `mode` 제거, `direct_prompt`→`prompt`, CLI 옵션은 `claude_args` 로 이동.
- repository admin 권한 필요 (GitHub app 설치·secret 추가).
- Claude commit 에 CI 가 안 돌면 GitHub App/custom app 사용 확인 (Actions user 로는 trigger 안 됨).
