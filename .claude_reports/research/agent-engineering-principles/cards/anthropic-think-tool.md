---
title: "The 'think' tool: Enabling Claude to stop and think in complex tool use situations"
authors: [Anthropic Engineering]
venue: Anthropic Engineering blog
year-month: 2025-03
url: https://www.anthropic.com/engineering/claude-think-tool
raw_type: technology blog
tier: 1
---

## Core Claims
> "This simple yet powerful technique has resulted in remarkable improvements in Claude's agentic tool use ability."

think tool 은 복잡한 task 중 structured thinking 을 위한 전용 공간을 만들어, tool use 시퀀스 도중 "필요한 정보가 다 있는지 멈춰 생각"하게 한다.

## Key Concepts & Definitions
- **think tool**: 응답 도중 reasoning step 을 삽입하는 도구. extended thinking (응답 생성 *이전* 발생)과 달리 tool use chain *도중* 에 reasoning 을 끼워넣음.
- 대상: tool output 분석·backtracking, policy-heavy environment 탐색, costly error 가 있는 sequential decision-making.

## Patterns Covered
- Tool output 분석 후 backtracking.
- Policy compliance 검증.
- 비용 큰 오류가 있는 순차 의사결정.
- 도메인별 예시와 함께 reasoning.

## Generation Mapping
- **Harness Eng / plan-then-execute**: 실행 도중 명시적 reasoning 공간을 harness 가 제공한다는 사례. 매뉴얼의 maker 단계 내 self-check·중간 reflection 패턴의 초기 근거 (2025-03, 비교적 이른 세대).

## Quotable
> "A 'think' tool that creates dedicated space for structured thinking during complex tasks."

> "The combination of the 'think' tool with optimized prompting delivered the strongest performance."

## Limitations
- Non-sequential tool call·단순 instruction-following 에는 이득 없음.
- Prompt 길이·output token 증가.
- 모든 use case 에 보편적으로 유익하지 않음.
