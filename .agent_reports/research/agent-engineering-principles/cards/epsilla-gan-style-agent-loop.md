---
title: "The GAN-Style Agent Loop: Deconstructing Anthropic's Harness Architecture"
authors: Epsilla (blog, author not individually attributed)
venue: Epsilla Blog
year-month: 2026
url: https://www.epsilla.com/blogs/anthropic-harness-engineering-multi-agent-gan-architecture
raw_type: technology blog
tier: 2
---

## Core Claims

- Single-agent system 의 core failure mode 는 _objective self-awareness 의 부재_ — AI model 은 자기 결과를 평가할 때 "pathological optimists" 라서 안전하지만 평범한 해법으로 수렴한다. (섹션: *The Adversarial Insight: AI Cannot Judge Itself*)
- Anthropic 의 harness 는 generation 과 evaluation 을 분리한 adversarial loop 로 이를 푼다. Verbatim: "The Generator produces, the Evaluator critiques, and that feedback becomes the input for the Generator's next iteration." (섹션: *The Adversarial Insight*)

## Key Concepts & Definitions

- **Harness Engineering**: AI agent 가 reliable 하게 동작하도록 구조화된 environment 를 짓는 새 paradigm. Anthropic 의 internal harness architecture 가 대표 사례.
- **Generator / Evaluator dyad**: Generator 가 artifact 를 만들고, 별개의 Evaluator 가 ruthless·metric-driven critique 를 적용. 둘은 system prompt·역할이 분리됨.
- **Planner**: "Takes a high-level, one-to-four-sentence prompt and expands it into a full product specification, focusing on the 'what' and 'why,' not the granular 'how.'"
- **"Pathological optimists"**: model 이 자기 산출물을 후하게 평가하는 편향 — self-critique 가 신뢰 불가한 근거.

## Patterns Covered

- Planner → Generator → Evaluator 3-agent harness (build → evaluate → refine 를 quality threshold 도달까지 iterate).
- Adversarial feedback loop ("By engineering conflict, you engineer progress").
- Front-end/visual design 에서 "AI slop" 방지용 evaluator-forced creativity.

## Generation Mapping

- 매뉴얼의 **maker/verifier 분리·자기채점 금지** 근거 핵심 출처 — "AI Cannot Judge Itself" 가 self-scoring 금지 원칙의 가장 직접적인 blog-level 표현.
- 우리 파이프라인의 품질관리팀(verifier) 을 연구팀/실행팀(maker) 과 분리하는 구조의 외부 정당화로 매핑.
- Planner = autopilot-spec, Generator = autopilot-code, Evaluator = 품질관리팀 QA 의 3분할에 대응.

## Quotable

1. "The core failure mode of a single-agent system is its profound lack of objective self-awareness."
2. "By engineering conflict, you engineer progress."
3. "The Generator produces, the Evaluator critiques, and that feedback becomes the input for the Generator's next iteration."

## Limitations / Caveats

- Tier 2 (vendor blog, individual author 미표기). Anthropic 1차 자료의 재해석이므로 1차 출처 교차검증 권장.
- 저자 스스로 GAN 비유의 한계를 짚음: enterprise context 에서 Evaluator 가 "in a vacuum" 으로 동작 — corporate policy·compliance rule·organizational state 에 접근 못 함 (섹션 *The Enterprise Gap: Where the Local Loop Fails*). 즉 local maker/verifier loop 만으로는 조직 제약을 못 잡는다.
