---
title: "Context Compaction for AI Agents: A Complete Guide"
authors: Redis
venue: Redis Blog
year_month: 2025
url: https://redis.io/blog/context-compaction/
raw_type: blog
tier: 2
---

## Core Claims

1. **Compaction 은 raw history 를 structured 한 high-fidelity 표현으로 응축해 새 context window 를 재초기화하는 것이다.** "Context compaction takes a conversation approaching the context window limit, condenses its contents into a structured, high-fidelity representation, and reinitiates a new context window with that condensed form in place of the raw history."
2. **Context management 는 model-capability 문제가 아니라 practical design 문제다.** "Context management has become a practical design problem, not just a model-capability problem" — 더 큰 window·RAG 도 "don't replace deliberate context management".
3. **compaction 은 보존/폐기 대상을 명시적으로 구분한다.** 보존: active constraints, open decisions, completed task state. 폐기: exploratory process, redundant tool outputs, verbose intermediate steps.

## Key Concepts & Definitions

- **Context compaction** (verbatim): "condenses its contents into a structured, high-fidelity representation, and reinitiates a new context window with that condensed form in place of the raw history".
- **Two-tier memory model** (Redis Iris):
  - **Working Memory (L1)**: "session-scoped events bounded by a configurable time to live (TTL)".
  - **Long-term Memory (L2)**: "cross-session knowledge as vector embeddings retrieved through semantic search".
- **Reversible vs. Lossy compaction**: reversible = dropped content 가 외부에 존재해 다시 fetch 가능 / lossy = summarization 후 영구 폐기.
- **Context engine**: 매 reasoning step 에서 무엇을 context 에 넣을지 결정하는 architectural layer (selection·compression·retrieval·routing).
- **Engineering handoff note 비유**: 2주 sprint 후 senior engineer 가 전체 Slack export 가 아니라 decisions·reasoning·open issues·system state 를 담은 structured document 를 넘긴다.

## Patterns Covered

- **컨텍스트 절약·compaction**: ✓ 본 글의 주제. anchored/structured summarization (active constraint·open decision·task state 보존).
- **상태 파일·영속성 (memory hierarchy)**: ✓ L1 working memory(TTL) / L2 long-term(vector embedding) 2-tier 모델.
- **tool output offloading (just-in-time 인접)**: ✓ 큰 tool result 를 external store 에 쓰고 context 엔 reference pointer + preview 만 남김 (reversible).
- **staged compaction**: ✓ masking unused fields → pruning stale turns → lossy summarization 으로 점증적 압박 대응, lossy 를 최후수단화.
- **sliding window / token-threshold**: ✓ 단순 baseline 으로 소개 (predictable size 지만 permanent loss).
- 다루지 않음: maker-verifier, golden set/eval, 오답노트→케이스 승격, spec-first/plan-then-execute, worktree.

## Generation Mapping

매뉴얼 세대사의 **loop·영속성** 세대 — 특히 컨텍스트 절약·compaction 축의 실무 패턴 출처. Anthropic 의 compaction 정의(context-engineering 세대)를 받아 **memory hierarchy(L1 working / L2 long-term)** 와 **reversible→lossy 우선순위 스택**으로 구체화한 vendor 문서. 매뉴얼의 "raw → reversible compaction → lossy summarization" 단계적 폴백 원칙을 verbatim 으로 근거 지을 수 있고, tool output offloading 은 just-in-time retrieval 과 인접한 reversible 기법으로 연결된다. L1/L2 tiering 은 매뉴얼의 상태 파일·영속성 패턴을 인프라 레벨로 매핑.

## Quotable

1. "Context management has become a practical design problem, not just a model-capability problem."
2. "Start with raw context. Move to reversible compaction ... when the window gets tight. Only fall back to lossy summarization ... when nothing cheaper works."
3. "Context compaction matters because long agent sessions get expensive, slow, and forgetful fast."

## Limitations / Caveats

- compaction 을 피해야 할 경우: exact wording 이 중요할 때 (legal text, 정밀한 API response), 또는 task 가 현재 window 에 충분히 들어갈 때.
- lossy summarization 은 "permanently destroyed" — 되돌릴 수 없으므로 staged 접근의 최후수단으로만.
- vendor(Redis Iris) 자사 제품 맥락 — L1/L2 구현은 Redis 종속, 일반화 시 추상 패턴만 차용 권장.
