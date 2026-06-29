---
title: "Don't Build Multi-Agents"
authors: Walden Yan
venue: Cognition AI Blog
year-month: 2025
url: https://cognition.ai/blog/dont-build-multi-agents
raw_type: technology blog
tier: 1
---

## Core Claims

- 두 가지 원칙이 multi-agent architecture 를 default 로 배제할 만큼 critical 하다: **Principle 1** "Share context, and share full agent traces, not just individual messages" / **Principle 2** "Actions carry implicit decisions, and conflicting decisions carry bad results."
- Parallel subagent 협업은 본질적으로 fragile 하다. Verbatim: "Running multiple agents in collaboration only results in fragile systems."

## Key Concepts & Definitions

- **Context engineering**: agent 신뢰성의 핵심 — agent 가 충분한 full context 와 trace 를 공유해야 일관된 결정을 내린다.
- **Implicit decisions**: 모든 action 은 style·edge case 에 대한 암묵적 결정을 내포. subagent 들이 서로의 작업을 못 보면 incompatible premise 위에서 작동해 충돌 산출물 발생.
- **Single-threaded linear agent**: 가장 단순·신뢰 가능한 구조 — 결정이 한 곳에 모여 context 가 분산되지 않음.
- **Subagents-as-question-answerers**: Claude Code 식 subagent — 병렬로 _작업하지 않고_ 질문에만 답함 (read-only 보조).

## Patterns Covered

- (권장) Single-threaded linear agent.
- (권장) Claude Code Subagents — subtask 는 작업이 아니라 질문 응답만.
- (권장) Edit Apply Models — 결정을 single-model 로 통합.
- (반대) Parallel collaborating subagents — miscommunication cascade·conflicting assumption·dispersed decision-making 의 실패 모드.

## Generation Mapping

- 매뉴얼의 **서브에이전트 분업 찬반** 에서 _반대(write 작업 분산 금지)_ 축의 핵심 출처.
- 우리 오케스트레이션이 항상 main 에서 일어나고 서브에이전트 중첩을 1단으로 제한하는 설계의 외부 근거 — "decision-making 분산 금지" 와 직접 대응.
- write/decision 을 수반하는 작업은 단일 스레드에 모으고, 분업은 read·question-answering 으로 한정하라는 우리 규칙(실행팀 vs 연구팀 read/write 분리)의 정당화.

## Quotable

1. "The decision-making ends up being too dispersed and context isn't able to be shared thoroughly enough between the agents."
2. "Agents today are not quite able to engage in this style of long-context proactive discourse with much more reliability than you would get with a single agent."
3. "Running multiple agents in collaboration only results in fragile systems."

## Limitations / Caveats

- Tier 1 (Cognition 1차 자료, named author Walden Yan).
- 시점 한정 주장 — "agents today" 라는 단서가 명시적이며, 후속 글 [[cognition-multi-agents-working]] 에서 저자 진영이 입장을 일부 갱신한다 (모델 발전으로 일부 multi-agent 패턴이 동작). 따라서 이 글은 _절대 반대_ 가 아니라 _2025 시점의 default-against_ 로 읽어야 함. 두 글을 read vs write 축으로 종합 필요.
