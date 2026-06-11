---
title: Harness design for long-running application development
authors: Anthropic Engineering
venue: Anthropic Engineering Blog
year-month: 2025
url: https://www.anthropic.com/engineering/harness-design-long-running-apps
raw_type: engineering blog (technology)
tier: 1
---

## Core Claims
1. **generator-evaluator 분리** 가 출력 품질을 극적으로 끌어올린다 — agent 는 자기 작업을 신뢰성 있게 self-evaluate 못 한다 (특히 subjective task).
2. **context reset** (context window 를 비우고 structured handoff 로 새로 시작) 이 long-running coding 에서 compaction 을 능가한다 (Sonnet 4.5 기준; Opus 4.6 은 continuous session).
3. **multi-agent 아키텍처** (planner·generator·evaluator persona 분업) 가 단일 agent 한계 너머의 full-stack app 을 가능케 한다.
4. **harness 복잡도는 모델 개선에 따라 줄어야 한다** — 각 component 는 "load-bearing assumption" 으로 지속적 stress-test 대상. v2 에서 sprint construct 제거 (Opus 4.6 이 더 길게 sustain).

## Key Concepts & Definitions
- "harness" formal definition 없음 — 운영상 "여러 specialized agent·artifact handoff·evaluation loop 를 관리해 coherent long-running 자율 개발을 가능케 하는 structured orchestration system".
- **Sprint contract**: high-level spec 과 testable implementation 사이를 잇는 중간 계약 (code 실행 전).
- **generator-evaluator 핵심 명제**: "Separating the agent doing the work from the agent judging it proves to be a strong lever" (Frontend design 섹션).
- **harness assumption 명제**: 모든 component 가 모델이 혼자 못 하는 것에 대한 가정을 encode.

## Patterns Covered
- **plan-then-execute**: Planner agent 가 1-4 문장 prompt 를 full product spec 으로 확장.
- **maker-verifier 분리**: Generator/Evaluator split — evaluator 는 Playwright MCP 로 직접 interaction test.
- **서브에이전트 분업**: 3개 — Planner·Generator·Evaluator.
- **파이프라인 세분화**: sprint 기반 feature chunking (v1); v2 에서 모델 개선으로 제거.
- **golden set·eval**: 4-criterion 평가 (design quality·originality·craft·functionality).
- **컨텍스트 절약·compaction**: compaction 과 reset 둘 다 논의, Sonnet 4.5 는 reset 선호.
- **상태 파일·영속성**: file 기반 agent 간 통신 + generator 내 git version control.
- (미포함) headless/cron·worktree 격리·오답노트 케이스 승격 (evaluator log 는 반복 검토하나 formal error repository 없음).

## Generation Mapping
- **maker-verifier 분리 (generator-evaluator)** 의 1차 근거 — 사용자 매뉴얼 "maker-verifier 분리" 패턴의 핵심 출처. self-evaluation 불가 → 별도 judge agent.
- **harness engineering** 의 self-aware 버전 — component=가정, 모델 개선 시 harness 축소 (v1 sprint → v2 제거) 가 "원칙의 세대사" 의 _harness 가 모델 발전에 따라 얇아진다_ 논거.
- 등장 배경: 1-4문장 prompt 로 full-stack app(웹 앱, DAW 등)을 짓는 harness 를 v1→v2 로 진화시킨 실무 회고. file 기반 handoff·planner/generator/evaluator 3분업이 "서브에이전트 분업 / plan-then-execute / 상태 파일" 출처.

## Quotable
1. "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre." (Why naive implementations fall short 섹션) — self-eval 불가.
2. "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue." (Frontend design: making subjective quality gradable 섹션) — maker-verifier 분리.
3. "Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing." (Iterating on the harness 섹션) — harness=가정 집합, 모델 개선 시 축소.

## Limitations / Caveats
- evaluator 한계 자인: "small layout issues, interactions that felt unintuitive... undiscovered bugs in more deeply nested features that the evaluator hadn't exercised thoroughly".
- 높은 비용 overhead: v1 harness 가 solo run 대비 20배 ($200 vs $9); v2 도 $124.70 (3h50m).
- model-dependent — Sonnet 4.5 vs Opus 4.6 로 harness tuning 이 크게 달라지고, 가정이 모델 개선 시 stale.
- subjective taste encoding 의 brittleness: criterion wording 이 의도 못 한 방향으로 generator 를 steer.
- v2 DAW 에 stubbed feature 잔존 — creative(audio) evaluation 에선 QA loop 가 덜 효과적.
