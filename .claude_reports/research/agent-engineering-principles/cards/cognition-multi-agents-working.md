---
title: "Multi-Agents: What's Actually Working"
authors: Cognition AI (follow-up to Walden Yan's "Don't Build Multi-Agents")
venue: Cognition AI Blog
year-month: 2026
url: https://cognition.ai/blog/multi-agents-working
raw_type: technology blog
tier: 1
---

## Core Claims

- 지난 ~10개월간 model 이 훨씬 더 자연스럽게 agentic 해지면서, 이전엔 비현실적이던 multi-agent deployment 가 실용화됐다 (enterprise 사용 ~8x 성장). (섹션: *What Changed in the Last 10 Months*)
- Multi-agent 가 동작하는 자리는 **single-threaded write + 부가 지능 보조** 와 **clean-context reviewer** 다. Verbatim: "A clean-context reviewer catches bugs the coder can't see" — context rot 감소가 attention 최적화로 model intelligence 를 높인다. (섹션: *Some Practical Multi-agent Experiments*)

## Key Concepts & Definitions

- **Read-only subagents (web/code search)**: 여전히 가장 안전한 multi-agent 패턴 — action 이 아니라 intelligence 만 기여.
- **Single-threaded writes**: 쓰기는 한 스레드로 유지하고, 추가 agent 는 _결정이 아니라 지능_ 을 보탬.
- **Context rot**: context bloat 가 attention 을 저하시키는 현상. clean context 가 decision quality 를 올린다.
- **Capability routing / cross-frontier communication**: sub-task 를 가장 잘 맞는 frontier model 로 라우팅 (예: Sonnet 4.5 planning).
- **Map-reduce management**: unstructured swarm 대신 manager-child 구조로 coordination.

## Patterns Covered

- **Code-Review Loop** — clean-context reviewer 가 coder 가 못 보는 버그를 잡음 (= maker/verifier 의 동작 사례).
- **Smart Friend** — 별도 model 이 조언자로 붙는 패턴.
- **Manager Coordination** — higher-level delegation, map-reduce 식 구조화.

## Generation Mapping

- 매뉴얼의 **서브에이전트 분업 찬반** 에서 _찬성(언제 동작하나)_ 축의 핵심 출처. [[cognition-dont-build-multi-agents]] 와 한 쌍으로 read vs write 종합.
- **핵심 종합 규칙**: read 작업(search/review)은 병렬 분업 OK, write/decision 은 single-thread 유지 — 우리의 "오케스트레이션은 main, 분업은 read·verifier" 설계와 정확히 일치.
- "clean-context reviewer catches bugs the coder can't see" = 우리 maker/verifier 분리·context 격리의 가장 강한 찬성 근거.
- Cross-frontier routing = 우리 mode 별 model 배정(opus/sonnet) 의 근거.

## Quotable

1. "A clean-context reviewer catches bugs the coder can't see."
2. "When paired with Sonnet 4.5 for 'planning,' we were able to make up for a small bit of the performance gap while keeping the low cost and fast speeds."
3. "Cross-frontier communication...produced real gains in the trickiest scenarios."

## Limitations / Caveats

- Tier 1 (Cognition 1차 자료, 선행 글의 official follow-up).
- 입장 갱신은 _번복이 아니라 조건부 완화_ — write/decision 분산 금지 원칙은 유지하되, read·review·planning 보조에 한해 multi-agent 를 허용. 두 글을 대립이 아닌 _보완_ 으로 읽어야 정확. 모델 능력 시점 의존성이 명시적이므로 future 모델에선 경계가 또 이동할 수 있음.
