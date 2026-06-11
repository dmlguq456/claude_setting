---
title: "How we built Claude Code auto mode"
authors: [John Hughes, et al.]
venue: Anthropic Engineering blog
year-month: 2026-03
url: https://www.anthropic.com/engineering/claude-code-auto-mode
raw_type: technology blog
tier: 1
---

## Core Claims
> "Auto mode is a new mode for Claude Code that delegates approvals to model-based classifiers—a middle ground between manual review and no guardrails."

> "The agent shouldn't be able to hide a dangerous operation behind a benign-looking wrapper."

## Key Concepts & Definitions
- **Auto mode**: human approval 대신 AI classifier 를 쓰는 autonomous execution. manual review 와 no-guardrails 사이의 중간 지점.
- **Headless execution**: interactive UI 없이 실행 (`claude -p` terminal mode).
- **Safety scaffolding**: prompt-injection probe + transcript classifier 의 2층 방어. "catch the dangerous actions that aren't aligned with user intent, while letting the rest run without approval prompts."
- 동기: "Claude Code users approve 93% of permission prompts" — 대부분 승인되니 prompt 가 마찰만 됨.

## Patterns Covered
- Scope escalation·credential exploration·agent-inferred parameter 탐지.
- 외부 서비스 통한 unauthorized data sharing 탐지.
- safety-check bypass 탐지.

## Generation Mapping
- **Loop Eng / headless·자율 실행 안전장치**: 매뉴얼 1부 'headless/cron 자율 실행' 안전장치의 1차 근거. classifier 기반 approval delegation = 사람 없는 루프에서의 guardrail. sandboxing(filesystem/network 격리)과 상보 — 이쪽은 intent-alignment classifier 층.

## Quotable
> "Claude Code users approve 93% of permission prompts."

> "The agent shouldn't be able to hide a dangerous operation behind a benign-looking wrapper."

## Limitations
- real overeager action 에 대해 17% false-negative rate.
- genuine user consent 와 blast radius 다른 prior approval 을 구분하기 어려움.
