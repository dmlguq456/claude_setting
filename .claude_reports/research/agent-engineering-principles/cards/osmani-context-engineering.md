---
title: "Context Engineering: Bringing Engineering Discipline to Prompts"
authors: ["Addy Osmani"]
venue: "addyo.substack.com (Substack)"
year-month: "2025"
url: https://addyo.substack.com/p/context-engineering-bringing-engineering
raw_type: blog
tier: 1
---

# Context Engineering: Bringing Engineering Discipline to Prompts

## Core Claims

- (Definition) verbatim: **"Prompt engineering was about cleverly phrasing a question; context engineering is about constructing an entire information environment so the AI can solve the problem reliably."** — 세대 전환의 핵심 대비 문장.
- (body, Karpathy/quip) verbatim: **"Prompt engineering walked so context engineering could run."** — 세대 계승을 한 줄로 압축한 인용.

## Key Concepts & Definitions

- **Context engineering (def):** verbatim — "Context engineering means dynamically giving an AI everything it needs to succeed – the instructions, data, examples, tools, and history – all packaged into the model's input context at runtime."
- **prompt vs context 대비:** verbatim — "Prompt engineering was about cleverly phrasing a question; context engineering is about constructing an entire information environment so the AI can solve the problem reliably."
- **production 환경 비유:** verbatim — "We've learned that generative AI in production is less like casting a single magic spell and more like engineering an entire environment for the AI."

## Patterns Covered

- **RAG** — "Retrieval-Augmented Generation (RAG): fetching relevant knowledge to ground responses"
- **few-shot** — few-shot examples (출력 포맷 시연)
- **상태 파일·영속성 / 컨텍스트 절약** — state/memory management; conversation summary compression (compaction)
- **tool selection** — tool orchestration (tool 출력을 다음 호출의 context 로 포맷)
- **컨텍스트 절약** — context window management (token 한계 vs 정보 품질 균형)
- **structured context** — markdown/JSON/bullet 포맷; role/system instructions

## Generation Mapping

- **prompt engineering 한계 → context engineering 등장**, verbatim: "One analysis quipped: Prompt engineering walked so context engineering could run. In other words, a witty one-off prompt might have wowed us in demos, but building reliable, industrial-strength LLM systems demanded something more comprehensive." → _demo 용 one-off prompt_ 으로는 production 신뢰성을 못 냄.
- 추가 한계 진술, verbatim: "As applications grew more complex, the limitations of focusing only on a single prompt became obvious." → _single prompt 만 본 것_ 이 한계 = 다음 세대 동력.
- 세대사 위치: prompt → **context** 의 1차 명명/정당화 글. (이후 harness·loop 가 이 위에 쌓임.)
- Karpathy 균형 원칙(보조): "Too little or of the wrong form and the LLM doesn't have the right context... Too much or too irrelevant and the LLM costs might go up and performance might come down." → 컨텍스트 절약 패턴의 근거.

## Quotable

1. "LLMs are powerful but they aren't mind-readers. The quality of output is directly proportional to the quality and relevance of the context you provide."
2. "Too little or of the wrong form and the LLM doesn't have the right context for optimal performance. Too much or too irrelevant and the LLM costs might go up and performance might come down." — Karpathy
3. "We've learned that generative AI in production is less like casting a single magic spell and more like engineering an entire environment for the AI."

## Limitations

- **hallucination 잔존:** "Even with perfect context engineering, LLMs still hallucinate, make logical errors, and fail at complex reasoning."
- **context rot:** 긴 대화에 noise·false start·contradiction 누적 → 시간이 지날수록 성능 저하. (harness engineering 의 "battling context rot" 가 이 한계를 이어받음.)
- **방법론 미성숙:** "Much of current AI work lacks the rigor we expect from engineering disciplines. There's too much trial-and-error, not enough measurement..." → golden set·eval 세대로의 동력.
- **silver bullet 아님:** "Context engineering isn't a silver bullet—it's damage control and optimization within current constraints."

(Substack — paywall 없음, 전문 확보.)
