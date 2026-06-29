---
title: "12-Factor Agents — Principles for building reliable LLM applications"
authors: HumanLayer (dexhorthy 외)
venue: GitHub (humanlayer/12-factor-agents)
year-month: 2025
url: https://github.com/humanlayer/12-factor-agents
raw_type: open-source manifesto / README
tier: 1
---

## Core Claims
- (verbatim) "Agents, at least the good ones, don't follow the loop until goal pattern. Rather, they are comprised of mostly just software."
- (verbatim) "The fastest way I've seen for builders to get good AI software in the hands of customers is to take small, modular concepts from agent building, and incorporate them into their existing product."

## Key Concepts & Definitions
12 factor 전체 목록:
1. **Natural Language to Tool Calls** — LLM 출력을 구조화된 실행 가능 tool invocation 으로 변환.
2. **Own your prompts** — framework default 에 맡기지 말고 prompt 를 직접 통제.
3. **Own your context window** — LLM context 에 무엇이 들어갈지 의도적으로 관리.
4. **Tools are just structured outputs** — tool call = 모델의 표준화된 출력 포맷.
5. **Unify execution state and business state** — agent workflow state 를 application/business data 와 동기화 (별도 추적 시스템 X, 제품이 쓰는 같은 자료구조를 갱신).
6. **Launch/Pause/Resume with simple APIs** — state 손실 없이 중단·재개 가능.
7. **Contact humans with tool calls** — human handoff 도 같은 tool-calling 메커니즘으로.
8. **Own your control flow** — framework routing 에 위임 말고 명시적 orchestration 작성.
9. **Compact Errors into Context Window** — error 를 압축해 context 공간 보존.
10. **Small, Focused Agents** — broad/open-ended 가 아니라 narrow·specific task. "good ones don't follow the loop until goal pattern."
11. **Trigger from anywhere, meet users where they are** — 다중 entry point·배포 컨텍스트 지원.
12. **Make your agent a stateless reducer** — agent 를 state 를 변환하는 pure function (stateless reducer) 으로 구조화.

## Patterns Covered
- **State management**: 실행 추적을 business logic 과 통합 (Factor 5).
- **Pause/resume 영속성**: 중단점·재개를 simple API 로 (Factor 6) — stateless reducer (Factor 12) 와 짝.
- **Control flow transparency**: implicit framework routing 을 explicit orchestration 으로 대체 (Factor 8).
- **Context optimization**: 전략적 pruning·압축 (Factor 3, 9).
- **Modular architecture**: 좁은 scope + composable tool interface (Factor 10).
- 핵심 메타-원칙: agent = "deterministic code with strategic LLM integration points" (자율 의사결정자가 아니라, LLM 을 전략적으로 끼운 결정론적 소프트웨어).

## Generation Mapping
- **Factor 5 (unify execution + business state)** = 본 family 의 `spec/pipeline_state.yaml`·`plans/*`·`_RUNLOG.md` 같은 **상태 파일 단일 출처** 철학. 산출물=상태, 별도 in-memory 추적 X.
- **Factor 6 + 12 (pause/resume, stateless reducer)** = autopilot-* 의 `--from <stage>` 재개, `post-it.md` 세션-간 연속성, ScheduleWakeup pause 와 동형. Claude 가 매 turn state 를 파일에서 재구성하는 reducer 형태.
- **Factor 10 (small, focused agents)** = 라우터→모드(연구팀 plan-review/research-survey/fact-check/claim-verify) 분해, "서브에이전트 중첩 1단" 평면 구조, mode 별 narrow scope 와 정확히 매핑.
- **Factor 8 (own your control flow)** = `WORKFLOW.md` 단일 라우터 + hard 순서 게이트 (research→spec→code) — framework 자동 routing 대신 명시적 파이프.
- **Factor 2/3 (own prompts/context)** = CLAUDE.md 얇은 부트스트랩 + on-demand Read (eager 로드 X) 의 의도적 context 관리.
- **Factor 11 (trigger from anywhere)** = headless/cron/GitHub Actions 진입점 다양화 (#3,4,5 카드와 연결).

## Quotable
- "Agents, at least the good ones, don't follow the loop until goal pattern. Rather, they are comprised of mostly just software."
- "Good ones, don't follow the prompt, bag of tools, loop until goal pattern."
- "take small, modular concepts from agent building, and incorporate them into their existing product."

## Limitations / Caveats
- manifesto/opinion 문서 — empirical 벤치마크 아님. "good agents" 의 정의가 저자 경험 기반.
- HumanLayer 제품(human-in-the-loop SaaS) 맥락 — Factor 7 (contact humans) 강조에 vendor bias 가능.
- "stateless reducer" (Factor 12) 는 이상적 형태 — 실제 LLM agent 는 완전 pure 하기 어려움 (context 누적·비결정성).
