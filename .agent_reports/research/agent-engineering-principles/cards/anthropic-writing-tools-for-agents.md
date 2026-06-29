---
title: "Writing effective tools for agents — with agents"
authors: Anthropic
venue: Anthropic Engineering Blog
year_month: 2025
url: https://www.anthropic.com/engineering/writing-tools-for-agents
raw_type: blog
tier: 1
---

## Core Claims

1. **Agent 는 도구만큼만 유능하다.** "Agents are only as effective as the tools we give them" (opening thesis).
2. **도구는 전통 software 와 다른 agent affordance 에 맞춰 설계해야 한다 — API wrapping 이 아니다.** "agents have distinct 'affordances' to traditional software—that is, they have different ways of perceiving potential actions" ("Choosing the right tools for agents").
3. **Evaluation-driven 반복 + agent 협업이 도구 성능을 크게 끌어올린다.** "most of the advice in this post came from repeatedly optimizing our internal tool implementations with Claude Code" ("Collaborating with agents").
4. **작은 description 개선이 큰 효과를 낸다.** "Even small refinements to tool descriptions can yield dramatic improvements" ("Prompt-engineering your tool descriptions").

## Key Concepts & Definitions

- **Good agent tool**: 다중 discrete operation 을 한 high-impact workflow 로 consolidate 하고, context-efficient 결정을 가능케 하며, high-signal 정보만 반환. "tools can consolidate functionality, handling potentially multiple discrete operations (or API calls) under the hood".
- **Evaluation-driven development**: "Building an evaluation allows you to systematically measure the performance of your tools" — agentic loop 으로 실제 task 수행 후 reasoning/error 분석.
- **Token efficiency**: pagination·filtering·truncation 으로 응답 context 소비를 줄이고 steering instruction 제공(예: 206→72 tokens, 응답 25,000 token 상한).
- **Namespacing** (verbatim): "Namespacing (grouping related tools under common prefixes) can help delineate boundaries between lots of tools" (예: `asana_projects_search`).

## Patterns Covered

- **golden set/eval**: ✓ 핵심. 실제 사용 기반 evaluation task 생성 — "Strong evaluation tasks might require multiple tool calls—potentially dozens".
- **maker-verifier 분리**: ✓ "Each evaluation prompt should be paired with a verifiable response or outcome".
- **파이프라인 세분화(역방향: consolidation)**: ✓ 개별 API wrapping 대신 통합 — "Instead of implementing a list_users, list_events, and create_event tools, consider implementing a schedule_event tool".
- **오답노트→케이스 승격**: ✓ agent transcript 로 도구 개선 — "Simply concatenate the transcripts from your evaluation agents and paste them into Claude Code".
- **plan-then-execute**: ✓ 약하게 — "Start by standing up a quick prototype of your tools" 후 eval.
- **컨텍스트 절약·compaction**: ✓ ResponseFormat enum(DETAILED vs CONCISE)로 응답 verbosity 제어.
- 다루지 않음: 서브에이전트 분업(직접 X), worktree 격리, headless/cron, 상태 파일·영속성.

## Generation Mapping

이 글은 매뉴얼 세대사의 **harness engineering 세대 중 "도구 표면(tool surface)" 설계**의 1차 근거이자, **loop/eval 세대의 golden set·오답노트 패턴**을 도구 맥락에서 구체화한다. tool 을 LLM 의 affordance 에 맞춰 설계하고(harness), eval task 로 측정하고(golden set), transcript 를 다시 도구 개선에 먹이는(오답노트→케이스 승격) 순환은 매뉴얼의 eval·오답노트 절에 직접 매핑된다. 등장 배경: MCP/tool 생태계가 커지며 "도구를 어떻게 써먹게 만들 것인가"가 agent 성능의 병목이 됨 — building-effective-agents 의 "design toolsets thoughtfully" 를 evaluation-driven 으로 체계화한 후속편. 특히 "agent 가 자기 도구를 같이 개선한다"는 메타-루프가 loop engineering 세대의 자기개선 사고를 보여준다.

## Quotable

1. "Agents are only as effective as the tools we give them." (opening thesis)
2. "Even small refinements to tool descriptions can yield dramatic improvements." (Prompt-engineering your tool descriptions)
3. "LLM agents have limited 'context'... whereas computer memory is cheap and abundant." (Choosing the right tools for agents)

## Limitations / Caveats

- 만능 응답 포맷 없음 — "there is no one-size-fits-all solution" (XML vs JSON vs Markdown); eval 로 task 별 테스트 필요.
- Namespacing 효과는 모델별 상이 — "Effects vary by LLM" (prefix vs suffix).
- Agent 예측 불가성 — "call the wrong tools, call the right tools with the wrong parameters... or process tool responses incorrectly"; 도구만으로 성능 보장 불가, system-level safeguard 필요.
- 현 context window 가 동시 접근 가능한 도구/정보를 제약 — 향후 진화 예상.
