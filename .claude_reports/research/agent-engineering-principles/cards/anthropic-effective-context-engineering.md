---
title: "Effective context engineering for AI agents"
authors: Anthropic Applied AI team
venue: Anthropic Engineering Blog
year_month: 2025
url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
raw_type: blog
tier: 1
---

## Core Claims

1. **Context 는 finite resource 다.** "Context is a critical but finite resource for AI agents" (Introduction). LLM 은 context 가 차오를수록 성능이 저하되며, 이는 인간 working memory 의 한계와 유사하다.
2. **Context engineering 은 prompt engineering 의 상위 개념으로, multi-turn agent loop 전체의 token 상태를 큐레이션한다.** prompt engineering 이 "writing and organizing LLM instructions" 에 집중한다면, context engineering 은 "the entire context state (system instructions, tools, MCP, external data, message history, etc)" 를 다룬다 ("Context engineering vs. prompt engineering").
3. **Attention budget 는 token 마다 소진된다.** transformer 의 n² 구조가 "natural tension between context size and attention focus" 를 만들며, context 는 "diminishing marginal returns" 를 갖는 자원으로 다뤄야 한다 ("Why context engineering is important").
4. **Context rot 는 모든 모델에 공통으로 나타난다.** "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases" — 정도 차이는 있어도 "this characteristic emerges across all models".
5. **장기 과제는 compaction / note-taking / sub-agent 세 가지 기법으로 context 한계를 넘는다** ("Context engineering for long-horizon tasks").

## Key Concepts & Definitions

- **Context engineering** (verbatim): "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts".
- **Context rot**: token 수가 늘수록 모델의 정확한 recall 능력이 떨어지는 현상.
- **Compaction** (verbatim): "the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary".
- **Just-in-time retrieval**: 모든 데이터를 사전 로드하지 않고 "lightweight identifiers (file paths, queries, links)" 만 유지하다 runtime 에 tool 로 동적 로드.
- **Attention budget**: 매 token 이 소진시키는 유한한 주의 자원.

## Patterns Covered

- **서브에이전트 분업**: ✓ "specialized sub-agents can handle focused tasks with clean context windows" — 각 sub-agent 가 "condensed, distilled summary of its work (often 1,000-2,000 tokens)" 만 반환 ("Sub-agent architectures").
- **상태 파일·영속성**: ✓ structured note-taking — NOTES.md·to-do list 같은 외부 메모리에 "notes persisted to memory outside of the context window".
- **컨텍스트 절약·compaction**: ✓ 전용 섹션. Claude Code 는 "architectural decisions, unresolved bugs, and implementation details" 는 보존하고 redundant tool output 은 폐기.
- **just-in-time retrieval (파이프라인 세분화 인접)**: ✓ 사전 처리 대신 reference 기반 동적 로드 + hybrid("retrieve some data up front for speed, and pursuing further autonomous exploration at its discretion").
- 다루지 않음: maker-verifier 분리, golden set/eval, 오답노트→케이스 승격, worktree 격리, headless/cron.

## Generation Mapping

이 글은 매뉴얼 세대사의 **context engineering** 세대를 정의하는 1차 출처다. "prompt engineering → context engineering" 으로의 명시적 세대 전환을 Anthropic 이 직접 선언한 텍스트로, 매뉴얼의 prompt→context 축 경계를 verbatim 으로 근거 지을 수 있다. 등장 배경: agent 가 multi-turn·long-horizon 으로 확장되면서 단일 prompt 최적화로는 부족해지고, context window 라는 유한 자원을 전체 loop 에 걸쳐 관리해야 한다는 문제의식. compaction·note-taking·sub-agent 는 loop 세대(영속성·장기 실행)로 넘어가는 교량 역할을 한다.

## Quotable

1. "Context, therefore, must be treated as a finite resource with diminishing marginal returns." (Why context engineering is important)
2. "Find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome." (The anatomy of effective context)
3. "Even as models continue to improve, the challenge of maintaining coherence across extended interactions will remain central to building more effective agents." (Context engineering for long-horizon tasks)

## Limitations / Caveats

- Context rot 는 불가피 — 모든 모델에 나타나며 "some models exhibit more gentle degradation than others".
- Just-in-time 의 trade-off: "Runtime exploration is slower than retrieving pre-computed data" + 올바른 tool 제공에 "opinionated and thoughtful engineering" 필요. agent 가 "waste context by misusing tools, chasing dead-ends" 할 수 있음.
- Compaction 위험: "Overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later".
- 더 큰 context window 가 해법이 아님 — "context windows of all sizes will be subject to context pollution and information relevance concerns".
