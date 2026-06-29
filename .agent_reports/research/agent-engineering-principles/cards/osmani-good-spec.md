---
title: "How to write a good spec for AI agents"
authors: ["Addy Osmani"]
venue: "addyosmani.com (blog)"
year-month: "2025"
url: https://addyosmani.com/blog/good-spec/
raw_type: blog
tier: 1
---

# How to write a good spec for AI agents

## Core Claims

- (Section 2) verbatim: **"Specs become the shared source of truth… living, executable artifacts that evolve with the project."** — spec 을 _살아있는 실행 가능 산출물_ 로 규정 (spec-first 세대의 정의).
- (Section 1) verbatim: **"Planning in advance matters even more with an agent - you can iterate on the plan first, then hand it off to the agent to write the code."** — plan-then-execute 의 명시 근거.

## Key Concepts & Definitions

- **good spec (정의):** verbatim — "documents that guide the agent clearly, stay within practical context sizes, and evolve with the project."
- **spec = shared source of truth:** verbatim — "Specs become the shared source of truth… living, executable artifacts that evolve with the project."
- **plan-first:** verbatim — "Use Plan Mode to enforce planning-first" (Section 1).

## Patterns Covered

- **spec-first / spec-driven** — Section 2 four-phase: Specify → Plan → Tasks → Implement
- **plan-then-execute** — Section 1 "Use Plan Mode to enforce planning-first"
- **3-tier constraints** — Section 4: Always do / Ask first / Never do (우리 파이프의 hard-constraint 양식과 동형)
- **decomposition / modular prompts** — Section 3: monolithic 대신 focused 조각으로 분해
- **acceptance criteria & conformance testing** — Section 4
- **self-verification** — Section 4: "After implementing, compare the result with the spec"
- **few-shot examples** — Section 4: "One quick example… anchor[s] the AI to the exact format you want"

## Generation Mapping

- **ad-hoc prompting → spec-driven 전환:** spec 은 "living, executable artifacts" 로서, "house of cards code" (정밀 검토에 무너지는 fragile 출력) 를 막는 장치로 프레이밍. → 즉흥 prompting 의 fragility 가 spec 세대 동력.
- 등장 근거(Introduction): verbatim — "Context window limits and the model's 'attention budget' get in the way." → 거대한 spec 을 통째로 주면 context/attention 한계로 실패 → _practical context size 안에서 진화하는 spec_ 이 답. (context engineering 의 컨텍스트 절약 원칙을 spec 작성에 적용한 후속.)
- long-running agents 글과의 연결: 그 글의 마지막 한계("Defining work crisply enough that an agent can run for a day on it is harder than doing the work yourself")에 대한 _실무 처방_ 이 이 good-spec 글.

## Quotable

1. "Context window limits and the model's 'attention budget' get in the way." (Introduction)
2. "Vague prompts mean wrong results." (Avoid Common Pitfalls — Baptiste Studer)
3. "I won't commit code I couldn't explain to someone else." (Avoid Common Pitfalls — Simon Willison)

## Limitations

- **context overload:** "As you pile on more instructions or data into the prompt, the model's performance in adhering to each one drops significantly" (Section 3, "curse of instructions" 연구 인용).
- **agent 고유 난점:** non-determinism ("same input, different outputs"); 속도가 인간 review 역량을 추월; cost 압박이 verification rigor 를 잠식.
- **spec 깊이 trade-off:** "Don't under-spec a hard problem… but don't over-spec a trivial one." → one-size-fits-all spec depth 는 없음.
