---
title: Effective harnesses for long-running agents
authors: Anthropic Engineering
venue: Anthropic Engineering Blog
year-month: 2025
url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
raw_type: engineering blog (technology)
tier: 1
---

## Core Claims
1. 장시간 agent 는 두 역할로 분리된다 — **initializer agent** 가 foundational environment scaffolding 을 세팅하고, **coding agent** 가 세션을 넘어가며 single-feature 단위로 점진 진행한다. context window 한계를 structured environment management + explicit feature tracking + git-based progress documentation 조합으로 우회한다.
2. 첫 context window 에는 **다른 prompt** 를 쓴다 ("a different prompt for the very first context window") — 초기화 단계와 반복 작업 단계의 prompt 를 분리.
3. 세션 간 연속성은 세 가지 artifact 로 유지: `claude-progress.txt` (세션별 행동 로그), `feature_list.json` (feature 완료 상태 — immutable by design), `git history` (rollback + commit message 로 semantic context 전달).
4. compaction 만으로는 부족하다 — handoff 가 다음 agent 에 항상 명확히 전달되지 않는다.
5. end-to-end 검증 누락이 핵심 실패 모드 — unit test·curl 은 통과해도 feature 가 실제로 동작 안 하는 걸 모델이 인지 못 하는 경향.

## Key Concepts & Definitions
- "harness" 의 formal definition 은 제시 안 됨. 문맥상 Claude Agent SDK 위에 얹힌 전체 agent framework (specialized prompt + agent behavior) 를 지칭.
- **Long-running agent 비유**: 매 세션 새 agent = 교대 근무자, "each new engineer arrives with no memory of what happened on the previous shift" (Long-running agent problem 섹션).
- **feature_list.json**: structured JSON 으로 feature 완료 상태 추적, immutable 설계 (acceptance criteria 역할).
- **테스트 불가침 원칙**: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality" (Environment management 섹션).

## Patterns Covered
- **plan-then-execute**: initializer 가 coding 전에 comprehensive feature specification 작성.
- **maker-verifier 분리**: 동일 agent 이되 행동 phase 가 구분됨 (implicit — 별도 agent 아님).
- **pipeline 세분화**: feature-by-feature 점진 진행.
- **golden set·eval**: feature list 가 acceptance criteria 로 기능.
- **상태 파일·영속성**: `claude-progress.txt`, `feature_list.json`, git log.
- **컨텍스트 절약·compaction**: 언급되나 "단독으로는 불충분" 명시.
- **오답노트→케이스 승격**: 미구현 (테스트 불가침 원칙이 인접).
- (미포함) worktree 격리·headless/cron·별도 verifier agent — sub-agent division 은 future work 로만 언급.

## Generation Mapping
- **harness engineering** 의 1차 근거 글 — initializer/coding 2단 구조, 첫 window 별도 prompt, 세 artifact 영속화가 모두 harness 층 설계.
- **context engineering** 과도 겹침 (compaction 한계·progress 파일로 state 외재화).
- 등장 배경: full-stack web app 을 단일 모델이 long-horizon 으로 짓게 하려다 context window 한계·교대 근무 망각 문제에 부딪힌 실무 회고. 사용자 매뉴얼의 "상태 파일·영속성 / 파이프라인 세분화 / plan-then-execute" 패턴의 직접 출처.

## Quotable
1. "each new engineer arrives with no memory of what happened on the previous shift" (Long-running agent problem 섹션) — 교대 근무 망각 비유, 세션-간 영속성 동기.
2. "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality" (Environment management 섹션) — 테스트 불가침.
3. "Claude tended to make code changes, and even do testing with unit tests or curl commands against a development server, but would fail [to] recognize that the feature didn't work end-to-end" (Testing 섹션) — end-to-end 검증 실패 모드.

## Limitations / Caveats
- compaction 이 "항상 깔끔히 다음 agent 에 instruction 을 넘기지는 못함".
- Puppeteer MCP 로 browser-native alert modal 을 못 봄 (vision/browser 한계).
- "Still unclear whether a single, general-purpose coding agent performs best across contexts" — 단일 범용 coding agent 최적성 미해결.
- 해법이 full-stack web app 개발에 optimized — scientific research·financial modeling 으로의 일반화 불명.
