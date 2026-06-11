---
title: "Building effective agents"
authors: Erik Schluntz, Barry Zhang (Anthropic)
venue: Anthropic Engineering Blog
year_month: 2024-12
url: https://www.anthropic.com/engineering/building-effective-agents
raw_type: blog
tier: 1
---

## Core Claims

1. **가장 성공적인 구현은 복잡한 framework 가 아니라 단순·조합 가능한 패턴을 쓴다.** "the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns." (Introduction)
2. **복잡성은 측정 가능한 개선이 정당화할 때만 추가한다.** "you should consider adding complexity _only_ when it demonstrably improves outcomes." (Combining and customizing these patterns)
3. **Workflow 와 agent 는 구분되는 시스템 범주다.** workflow 는 predefined code path 로 오케스트레이션, agent 는 LLM 이 동적으로 자기 프로세스를 통제 ("What are agents?").
4. **Agent 는 자율성의 대가로 비용·오류 누적 위험을 진다.** sandbox 테스트와 guardrail 이 필요 ("When to use agents").

## Key Concepts & Definitions

- **Workflows** (verbatim): "systems where LLMs and tools are orchestrated through predefined code paths."
- **Agents** (verbatim): "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- **Augmented LLM**: retrieval·tools·memory 로 증강된 LLM — 모든 패턴의 building block.

## Patterns Covered

- **파이프라인 세분화**: ✓ Prompt chaining — "decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one".
- **maker-verifier 분리**: ✓ Evaluator-optimizer — "one LLM call generates a response while another provides evaluation and feedback in a loop".
- **서브에이전트 분업**: ✓ Orchestrator-workers — "central LLM dynamically breaks down tasks, delegates them to worker LLMs".
- **병렬 격리**: ✓ Parallelization(sectioning/voting) — "Breaking a task into independent subtasks run in parallel".
- **plan-then-execute**: ✓ (Agents 섹션) "Once the task is clear, agents plan and operate independently".
- 다루지 않음: golden set/eval, 오답노트→케이스 승격, 상태 파일·영속성, headless/cron, compaction.

## Generation Mapping

이 글(2024-12)은 매뉴얼 세대사의 **harness engineering 세대의 정초 텍스트**다. workflow vs agent 구분과 6개 조합 패턴(augmented LLM, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer + autonomous agents)은 매뉴얼의 plan-then-execute / maker-verifier 분리 / 서브에이전트 분업 / 파이프라인 세분화 실무 패턴들의 직접 어원이다. 등장 배경: agent 붐 초기, framework 과잉을 경계하며 "오케스트레이션 구조를 직접 코드로 짠다"는 harness 사고를 제시. 매뉴얼이 인용할 때 evaluator-optimizer→maker-verifier, orchestrator-workers→서브에이전트 분업으로 매핑하면 된다.

## Quotable

1. "Success in the LLM space isn't about building the most sophisticated system. It's about building the _right_ system for your needs." (Summary)
2. "Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently..." (Agents)
3. "It is therefore crucial to design toolsets and their documentation clearly and thoughtfully." (Agents)

## Limitations / Caveats

- Framework 비판: "they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug." (When and how to use frameworks)
- Agent 비용/오류: "The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails."
- Latency/cost trade-off: "Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense."
