---
title: "What Is the Planner-Generator-Evaluator Pattern? The GAN-Inspired AI Coding Architecture"
authors: MindStudio (blog, author not individually attributed)
venue: MindStudio Blog
year-month: 2026-04
url: https://www.mindstudio.ai/blog/planner-generator-evaluator-pattern-gan-inspired-ai-coding
raw_type: technology blog
tier: 2
---

## Core Claims

- 같은 model 이 코드를 쓰고 리뷰하면 자기 실수를 놓친다 — generation 이 부분적으로 autocomplete 라서 동일한 reasoning error 가 generation·evaluation 양쪽에 재생산된다. Verbatim: "When the same model that wrote the code reviews it, it tends to overlook its own mistakes." (self-evaluation 실패 섹션)
- GAN 에서 영감받되 evaluator 는 진짜 adversarial 이 아니다. Verbatim: "The difference from a pure GAN: the evaluator isn't adversarial in a competitive sense. It's more like a senior engineer reviewing a pull request." (GAN analogy 섹션)

## Key Concepts & Definitions

- **Planner**: "Figures out what needs to be built" — request 를 input/output/edge case/constraint 를 담은 concrete specification 으로 decompose.
- **Generator**: planner spec 을 받아 "produces the actual code". 원 request 를 다시 추론하지 않고 execution 에 집중하는 narrower context.
- **Evaluator**: "Reads both the spec from the planner and the code from the generator, then produces a structured critique" — implementation accuracy·edge case·security·constraint compliance 점검.
- **Autocomplete bias**: model 의 generation 이 패턴 continuation 이라, 생성 단계의 오류가 평가 단계에도 그대로 반복되는 구조적 편향.

## Patterns Covered

- Planner-Generator-Evaluator 3-role 분업 (각 role 은 한 가지만 담당).
- Parallel generators: 여러 generator 가 같은 spec 의 서로 다른 implementation 을 병렬 생성하는 advanced setup.
- Context isolation: "agents shouldn't share full context histories to avoid contamination."

## Generation Mapping

- 매뉴얼의 **자기채점 금지(self-scoring ban)** 의 _메커니즘 수준 근거_ — 왜 self-eval 이 실패하는지를 autocomplete bias 로 설명하는 가장 명료한 출처.
- "evaluator ≠ pure GAN, more like a senior PR reviewer" 는 우리 verifier 를 적대적 무한경쟁이 아니라 _기준 기반 PR 리뷰어_ 로 규정하는 데 직접 인용 가능 — GAN 비유의 과대해석을 막는 caveat.
- "distinct system prompt per agent + no shared full context" = 우리 서브에이전트 분리·context 격리 설계 근거.

## Quotable

1. "When the same model that wrote the code reviews it, it tends to overlook its own mistakes."
2. "The difference from a pure GAN: the evaluator isn't adversarial in a competitive sense. It's more like a senior engineer reviewing a pull request."
3. "Each agent should have a distinct system prompt that defines its specific job, and ideally, agents shouldn't share full context histories to avoid contamination."

## Limitations / Caveats

- Tier 2 (vendor blog, 2026-04-01 게시, 개별 저자 미표기). 제품 마케팅 맥락.
- GAN 비유는 저자 스스로 한정함 — competitive adversarial 이 아니라 cooperative review 이므로, "GAN" 라벨을 문자 그대로 우리 시스템에 적용하면 오해 소지. 비유 차용 시 이 caveat 동반 필수.
