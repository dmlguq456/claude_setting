---
title: "Agentic Engineering Patterns"
authors: Simon Willison
venue: simonwillison.net (guide format) / Simon Willison's Newsletter
year-month: 2026-02
url: https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/
raw_type: technology blog (living guide)
tier: 1
---

## Core Claims

- Agentic Engineering 의 정의(verbatim): "Building software using coding agents—tools like Claude Code and OpenAI Codex, where the defining feature is that they can both generate and _execute_ code." 즉 코드를 생성할 뿐 아니라 실행·테스트·iterate 까지 turn-by-turn 인간 감독 없이 한다는 점이 핵심.
- 패턴은 *Design Patterns(GoF, 1994)* 형식에서 영감받은 chapter 단위 "guide" — frozen blog 가 아니라 evergreen·갱신형 콘텐츠.

## Key Concepts & Definitions

- **Guide (vs blog post)**: 시간에 따라 업데이트되는 chapter 모음. 첫 게시 시점에 고정되지 않음.
- **Agentic Engineering**: coding agent 로 소프트웨어를 짓는 professional 실천 — 기존 expertise 를 amplify.
- **Writing code is cheap now**: 초기 작동 코드 생성 비용이 거의 0 으로 떨어지면서 professional 실천·팀 역학이 재편된다는 중심 명제.
- **Red/green TDD**: test-first 개발이 agent 로 하여금 minimal prompting 으로 더 간결·신뢰성 높은 코드를 쓰게 함.

## Patterns Covered

게시 시점(2026-02-23) 기준 공개 chapter:
1. **Writing code is cheap now** — 코드 churn 비용 급락이 만드는 새 제약·기회.
2. **Red/green TDD** — test-first 가 agent reliability 를 끌어올리는 maker/verifier 의 실무 형태.
(예고: "Hoard things you know how to do" 등. 주 1–2 chapter 추가 예정.)

## Generation Mapping

- 매뉴얼의 **패턴 카탈로그** 메타 출처 — GoF 식 "pattern as named chapter" 포맷 자체가 우리 매뉴얼의 pattern catalog 구성 방식의 모델.
- **Red/green TDD** = maker(generate)/verifier(test) loop 의 가장 검증된 실무 패턴 — 우리 autopilot-code 의 test-driven QA 게이트와 직접 대응.
- "Writing code is cheap now → 검증·통합이 병목" 명제 = 우리가 verifier·spec·plan 단계에 비중을 두는 이유의 근거.
- "guide is evergreen" 철학 = 우리 산출물 versioning(autopilot-refine 갱신형) 과 정합.

## Quotable

1. "Building software using coding agents...where the defining feature is that they can both generate and _execute_ code."
2. "Red/green TDD ... test-first development enables agents to produce more succinct and reliable code with minimal additional prompting."
3. (편집 철학) "the words you read here will be my own" — AI 생성 산문을 자기 이름으로 게시하지 않는다는 정책.

## Limitations / Caveats

- Tier 1 (named author, 영향력 큰 1차 자료)이나 **게시 시점 기준 2개 chapter 만 공개** — 카탈로그가 미완성·living. 향후 chapter 가 추가되면 재방문 필요.
- mode=technology(블로그 skim) 한정 fetch — 전체 chapter 본문 deep-read 아님. 인용은 요약 기반이므로 verbatim 정확도는 원문 재확인 권장.
