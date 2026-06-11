---
title: "Spec-driven development with AI: Get started with a new open source toolkit"
authors: GitHub
venue: GitHub Blog
year_month: 2025
url: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
raw_type: blog
tier: 2
---

## Core Claims

1. **진실의 원천이 코드에서 의도로 이동한다.** "We're moving from 'code is the source of truth' to 'intent is the source of truth.'" — spec 이 executable source of truth.
2. **upfront spec 이 coding agent 의 efficacy 를 높인다.** "providing a clear specification up front ... gives the coding agent more clarity, improving its overall efficacy." — 모호한 prompt 를 agent 가 신뢰성 있게 실행할 의도로 변환.
3. **spec 을 작은 검증 가능한 task 로 분해한다.** "Instead of 'build authentication,' you get concrete tasks like 'create a user registration endpoint that validates email format.'"

## Key Concepts & Definitions

- **Spec-driven development**: spec 을 executable source of truth 로 삼아 agent 를 implementation·testing·validation 으로 이끄는 방식 (코드 완성 후 문서화의 반대).
- **Spec Kit**: GitHub 오픈소스 toolkit — Copilot·Claude Code·Gemini CLI 호환, 모호한 prompt 를 명확한 intent 로 변환.
- **Four-phase workflow**:
  - **Specify**: 무엇을·왜 만드는지 high-level 기술 (user journey 중심, 기술 stack 아님) → AI 가 living artifact spec 생성.
  - **Plan**: 원하는 stack·architecture·constraint 등 기술 방향 제공 → AI 가 (비교용 variation 포함) 기술 plan 생성.
  - **Tasks**: spec/plan 을 작고 review 가능한 isolated work chunk 로 분해 (TDD 원리와 유사).
  - **Implement**: coding agent 가 focused task 를 순차 처리, 개발자는 대규모 code dump 대신 집중된 변경을 review.

## Patterns Covered

- **spec-first / plan-then-execute**: ✓ 본 글의 핵심 — Specify→Plan→Tasks→Implement 4단계 명시적 분리.
- **maker-verifier (인접)**: ✓ Implement 단계의 focused task 별 개발자 review — agent build / human review 분리.
- **파이프라인 세분화**: ✓ Tasks 단계가 spec 을 small isolated chunk 로 분해 (TDD 유사) — 세분화·검증가능성.
- **상태 파일·영속성 (인접)**: ✓ spec = "living artifacts" 로 영속.
- 다루지 않음: compaction/memory hierarchy, golden set/eval(단 Tasks 가 TDD 인접), 오답노트→케이스 승격, worktree, headless/cron, sub-agent 분업.

## Generation Mapping

매뉴얼의 **spec-first / plan-then-execute** 축의 *toolkit·프로세스* 1차 출처 — owainlewis-spec-driven 의 철학을 GitHub 이 4-phase 도구(Specify→Plan→Tasks→Implement)로 제도화한 버전. 매뉴얼의 spec-first 파이프(research/analyze → spec → code, plan 사이클)와 **단계 매핑이 거의 동형**: Specify/Plan ↔ autopilot-spec(prd·stack·design), Tasks ↔ autopilot-code 의 plan 분해, Implement ↔ code 사이클. "intent is the source of truth" 는 매뉴얼의 하드 순서 게이트(spec 없이 code 금지)의 철학적 근거. Plan 단계의 "multiple variations for comparison" 은 axis-decomposed plan review 발상과 인접.

## Quotable

1. "We're moving from 'code is the source of truth' to 'intent is the source of truth.'"
2. "Instead of 'build authentication,' you get concrete tasks like 'create a user registration endpoint that validates email format.'"
3. "providing a clear specification up front ... gives the coding agent more clarity, improving its overall efficacy."

## Limitations / Caveats

- vendor(GitHub) toolkit 홍보 맥락 — Spec Kit 채택 권유가 깔린 글, 패턴은 도구 독립적이나 워크플로우 디테일은 toolkit 종속.
- spec 작성 자체의 비용·작은 작업에 대한 overhead 는 깊이 다루지 않음 (owainlewis 와 공통 공백).
- "intent is the source of truth" 의 drift 위험(코드가 spec 을 벗어났을 때의 정합성)은 본 글 범위 밖.
