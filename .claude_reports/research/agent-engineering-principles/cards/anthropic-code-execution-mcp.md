---
title: "Code execution with MCP: Building more efficient agents"
authors: [Adam Jones, Conor Kelly]
venue: Anthropic Engineering blog
year-month: 2025-11
url: https://www.anthropic.com/engineering/code-execution-with-mcp
raw_type: technology blog
tier: 1
---

## Core Claims
> "Code execution can enable agents to interact with MCP servers more efficiently, handling more tools while using fewer tokens."

> "This reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%."

## Key Concepts & Definitions
- **Code execution with MCP**: MCP server 를 direct tool call 이 아니라 code API 로 제시, agent 가 코드를 작성해 tool 상호작용 처리.
- **Progressive disclosure**: tool 정의를 upfront 가 아니라 filesystem navigation 으로 on-demand 로드.
- **Token efficiency**: execution environment 안에서 데이터를 filter·transform 한 뒤 모델에 결과 반환 — intermediate result 가 환경에 머물러 context 노출 감소.

## Patterns Covered
- Filesystem 기반 tool discovery (server 를 디렉터리로 조직).
- 모델 반환 전 데이터 filtering/aggregation.
- chained tool call 대신 code 로 control flow (loop·conditional).
- PII tokenization 등 privacy-preserving operation.
- State persistence·reusable skill.

## Generation Mapping
- **Context Eng / 고정 오버헤드 절감**: tool 정의 upfront 로드 제거 + intermediate result 를 sandbox 에 가둬 context 절약. 매뉴얼 1부 '고정 오버헤드 절감'의 1차 출처. Agent Skills progressive disclosure 와 짝.

## Quotable
> "Code execution can enable agents to interact with MCP servers more efficiently, handling more tools while using fewer tokens."

> "This reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%."

## Limitations
- secure sandboxing·resource limit·monitoring 인프라 필요.
- 구현 overhead·보안 고려를 token/latency 이득과 저울질해야 함.
