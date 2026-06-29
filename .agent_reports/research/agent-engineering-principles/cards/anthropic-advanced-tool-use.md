---
title: "Advanced tool use on the Claude Developer Platform"
authors: [Bin Wu, et al.]
venue: Anthropic Engineering blog
year-month: 2025-11
url: https://www.anthropic.com/engineering/advanced-tool-use
raw_type: technology blog
tier: 1
---

## Core Claims
> "Agents should discover and load tools on-demand, keeping only what's relevant for the current task."

> "The future of AI agents is one where models work seamlessly across hundreds or thousands of tools."

## Key Concepts & Definitions
- **Tool Search Tool**: large library 에서 tool 을 동적 discovery — 모든 정의를 upfront 로드하지 않음.
- **Programmatic Tool Calling**: sandboxed code execution 으로 tool 호출, intermediate result 를 context window 밖에서 처리.
- **Tool Use Examples**: optional parameter·parameter 조합 사용법을 구체 패턴으로 제시.
- **Fixed overhead reduction**: 모든 tool 정의의 upfront 로드 제거로 context window capacity 보존.

## Patterns Covered
- MCP server 통합 (GitHub·Slack·Sentry·Grafana·Splunk·Jira).
- 병렬 tool 실행·conditional orchestration.
- large dataset aggregation/filtering.
- budget compliance·복잡한 multi-step query.

## Generation Mapping
- **Context Eng / 고정 오버헤드 절감**: code-execution-mcp 와 짝을 이루는 platform-level 구현. 매뉴얼 1부 '고정 오버헤드 절감'의 정량 근거 (85% / 37% 절감). tool 정의 upfront 로드 제거 = 본 survey 의 SKILL.md on-demand 패턴 일반화.

## Quotable
> "This represents an 85% reduction in token usage while maintaining access to your full tool library."

> "Average usage dropped from 43,588 to 27,297 tokens, a 37% reduction on complex research tasks."

## Limitations
- Tool Search 는 invocation 전 search step 으로 latency 추가.
- 10+ tool 일 때 유익, 작은 library 는 ROI 제한.
- Programmatic Tool Calling 은 단순 single-tool call 엔 overhead 가 비효율.
- Tool Use Examples 는 token 비용 증가 — ambiguous·complex tool 에만 적합.
