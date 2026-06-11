---
title: "The Rise of AI Harness Engineering"
authors: Cobus Greyling
venue: Medium
year_month: 2026-03 (Mar 13, 2026)
url: https://cobusgreyling.medium.com/the-rise-of-ai-harness-engineering-5f5220de393e
raw_type: blog
tier: 2
role: 정리·대중화 — harness 를 SDK/Framework/Scaffolding 위 4번째 architectural layer 로 정리, 다수 원 출처 호명
---

## Core Claims (verbatim)

1. "A harness is not the agent. It's the software system that governs how the agent operates. It manages the full lifecycle…tools, memory, retries, human approvals, context engineering, sub-agents…so the model can focus on reasoning."
2. "Harness Engineering is the missing architectural layer that determines whether AI Agents actually work in production."

## Key Concepts & Definitions

- **Harness 정의**: agent 가 아니라 agent 가 _어떻게 동작하는지_ 를 지배하는 software system. lifecycle 관리(tools/memory/retries/human approvals/context engineering/sub-agents).
- **4번째 architectural approach**: SDK / Framework / Scaffolding (flexibility-vs-structure 스펙트럼 위 셋, "how you build an agent") 위에 2026 에 등장. Harness 는 다른 질문에 답함 — "how the agent runs". 셋 중 무엇으로든 harness 구축 가능, 대체 아니라 위 layer.
- **Philipp Schmid 의 computer analogy** (Greyling 인용): model = raw processing, context window = limited working memory, **harness = operating system**(context·init sequence·standard tool driver 관리), agent = 위에서 도는 application.
- **Six components of a harness (parallel.ai team 식별)**: Tool Integration Layer / Memory & State Management(Anthropic 은 progress file + git history 로 session bridge) / Context Engineering & Prompt Management(static template 아닌 active context selection) / Planning & Decomposition / Verification & Guardrails(self-correcting loop — agent 가 struggle 하면 harness 가 "뭐가 빠졌나" 신호로 취급) / Modularity & Extensibility.
- **Framework layer 의 붕괴(collapse into harness)**: "The intelligence moves into the model. The infrastructure moves into the harness." model 이 framework 의 ~80%(agent definition·message routing·task lifecycle·dependency·worker spawning) 흡수, 남은 20%(persistence·deterministic replay·cost control·observability·error recovery)가 harness.
- **Markdown/prompt harness**: CLAUDE.md skills 처럼 orchestration instruction 을 system prompt/markdown 에 직접 embed. "The LLM itself becomes the loop controller" — model 이 harness rule 읽고 따름. (configured-not-coded·loop-engineering 과 연결 고리.)

## Patterns Covered

- harness as OS analogy (Schmid)
- 6-component harness anatomy (parallel.ai)
- atomic tools + model-makes-plan + add guardrails/retries/verification ("Start simple")
- self-correcting loop (struggle = signal of what's missing)
- maker/checker via sub-agents
- markdown/prompt harness (LLM as loop controller)

## Generation Mapping

세대 서사의 **harness 단계 정초 글**. "AI Agents needed SDKs, then Frameworks, then Scaffolding. Now they need a Harness." 부제로 진화 계보 명시. prompt/context → **harness** 의 harness 측 핵심 1차-정리 출처. (이후 loop-engineering 이 harness 위에 loop 를 얹음.)

## Quotable

1. "A framework tells the developer how to structure an application. A harness tells the agent how to operate safely."
2. "With a framework, the developer writes the orchestration logic. With a harness, the model makes the plan. The harness keeps it on track."
3. "It's no longer 'which framework should we use?' It's 'what does our harness look like?'"

## Limitations / Caveats

- **출처 인용 관행 (이 글이 가장 권위-호명 밀도 높음)**: Greyling 은 harness 를 _자기 명명_ 하지 않고 외부 권위로 정당화 — "Both OpenAI and Anthropic are now using the term formally", "Martin Fowler has written about it", "An arXiv paper formalises it"(미특정), 6-component 는 "parallel.ai team identified", OS analogy 는 "Philipp Schmid put it best". 즉 다수 1차 출처를 _묶어 소개_ 하는 정리자 역할이 명확. 매뉴얼 명명-권위 vs 정리-역할 구분에서 harness 의 권위는 OpenAI/Anthropic/Fowler/parallel.ai 에 있고 Greyling 은 큐레이터.
- 실 production 예시(Claude Code·OpenAI Codex 1M-line no-typed-code·CUA Sample App)는 사례 인용 — 1차 검증/측정 본인 수행 X.
- "arXiv paper formalises it" 미특정 인용 — 추적 불가 (agent-model-harness 카드의 Harness-Bench 와 동일/별개 여부 불명).
- "roughly 80%/20%" 수치는 본인 추정(이전 글 "disappearing framework layer" 자기참조), 측정 근거 없음.
