---
title: "How I Code With AI Agents (Spec-Driven Development)"
authors: Owain Lewis
venue: Owain Lewis Newsletter
year_month: 2026-02
url: https://newsletter.owainlewis.com/p/how-i-code-with-ai-agents-spec-driven
raw_type: blog
tier: 3
---

## Core Claims

1. **같은 agent 에게 계획과 실행을 동시에 시키지 말라.** "don't ask the same agent to plan the work and do the work." planning(edge-case 분석)과 execution(shipping 우선)은 다른 cognitive mode 다.
2. **plan 은 대화에 살고, spec 은 repo 에 산다.** "A plan Claude generates lives in a conversation. A spec lives in your repo." — spec 은 review·edit·version control·handoff 가능한 영속 artifact.
3. **bottleneck 이 구현에서 명세로 이동한다.** agent 가 well-defined spec 을 빠르게 실행하므로 "the bottleneck shifts from implementation to specification" — 사람의 일은 요구를 명확히 articulate 하는 것.
4. **명세하지 않으면 agent 가 추측하고, 추측은 누적된다.** "add authentication" 엔 수십 개 결정이 있고, 명세 안 하면 agent 가 guess 하며 그 guess 가 compound.

## Key Concepts & Definitions

- **Spec-driven development**: agent 에 실행을 지시하기 전에 markdown spec 문서를 먼저 작성하는 방식 (즉시 구현 prompt 의 반대).
- **Spec 4-요소 구조**: Context(문제 1–2문장) / Scope(구체 feature·구현 디테일) / Constraints(library 선택·pattern·명시적 제외) / Tasks(검증 단계를 가진 개별 work unit).
- **Planning vs Execution 분리**: planning = edge-case 분석 mode / execution = shipping mode — 분리해야 각각 제대로 작동.
- **Spec as final translation layer**: "The spec is always the final translation layer before code." — 코드 직전의 최종 번역층.
- **Repository-based living document**: conversation 의 ephemeral plan 과 달리 version control 안 markdown 으로 영속·handoff 가능.

## Patterns Covered

- **spec-first / plan-then-execute**: ✓ 본 글의 핵심 — plan 과 execute 의 agent·mode 분리, spec 을 repo artifact 로.
- **상태 파일·영속성 (인접)**: ✓ spec 이 repo 안 versioned markdown 으로 영속 — conversation plan 대비 지속성.
- **maker-verifier (인접)**: ✓ "architect the work"(사람) vs "build it"(agent) 의 역할 분리 발상.
- 다루지 않음: compaction/memory hierarchy, golden set/eval, 오답노트→케이스 승격, worktree, headless/cron, sub-agent 분업.

## Generation Mapping

매뉴얼의 **spec-first / plan-then-execute** 축을 정의하는 individual-practitioner 출처 — github-spec-kit 의 toolkit 화된 버전에 대한 *철학적 핵심*. 특히 "don't ask the same agent to plan the work and do the work" 와 "A plan lives in a conversation. A spec lives in your repo." 는 매뉴얼이 *왜* plan 과 spec 을 분리하고 spec 을 영속 artifact 로 두는지를 verbatim 으로 뒷받침. "bottleneck shifts from implementation to specification" 은 매뉴얼의 spec-first 파이프(research/analyze → spec → code)의 동기를 직접 진술. spec-kit(GitHub)이 *프로세스/도구*라면 이 글은 *그 프로세스를 왜 따르는가*의 1차 근거.

## Quotable

1. "A plan Claude generates lives in a conversation. A spec lives in your repo."
2. "The spec is always the final translation layer before code."
3. "Your job is to architect the work. The agent's job is to build it."

## Limitations / Caveats

- tier 3 (medium skim) — 원 URL(잘린 .../spec-dri)은 404, WebSearch 로 정정 full URL 확보.
- 개인 블로그·일화적 — 정량 근거보다 practitioner 경험에 기반.
- spec 의 granularity·과도한 명세 비용(작은 작업까지 spec 화 시 overhead)은 깊이 다루지 않음.
